import logging
import json
import re
from html.parser import HTMLParser
from urllib.parse import urlparse

from flask import jsonify, render_template, Markup, current_app
from flask.ext.mail import Message
from requests import Request, Session
from requests.exceptions import ConnectTimeout

logger = logging.getLogger(__name__)


"""
Email
"""


def extract_domain(url):
    """
    Extracts the "domain.tld" from the url
    Strips out subdomains
    Does *not* work with tlds that have a dot in them, like .co.uk
    """
    if not url:
        return None
    o = urlparse(url)

    # find the hostname
    host = o.hostname
    if not host:
        if o.path:
            host = o.path
        else:
            return None

    # remove subdomain
    if host.count('.') == 0:
        raise ValueError('Incomplete domain')
    elif host.count('.') == 1:
        domain = host
    else:
        subdomain, domain = host.split('.', 1)
    return domain


class PostmarkAppBase(object):

    def __init__(self, api_key, account=False):
        self.api_key = api_key
        self.token_type = "X-Postmark-Account-Token" if account else "X-Postmark-Server-Token"
        self.get_header = {
            "Accept": "application/json",
            self.token_type: api_key
        }
        self.post_header = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            self.token_type: api_key
        }

    def has_body(self, method):
        return method in ('POST', 'PUT')

    def get_request(self, data, method, endpoint):
        # print(data)
        request = Request(
            method=method,
            url='http://api.postmarkapp.com/'+endpoint,
            headers=self.post_header if self.has_body(method) else self.get_header,
            data=json.dumps(data) if self.has_body(method) else None,
            params=data if not self.has_body(method) else None)
        # timeout=20
        return request.prepare()

    def json_response(self, message, method, endpoint):
        try:
            request = self.get_request(message, method, endpoint)
            s = Session()
            response = s.send(request)
            json_response = response.json()
        except ConnectTimeout as ct:
            logger.error(ct)
            return {"ErrorCode": "ConnectTimeout", "Message": "Connection timed out"}
        except Exception as failed:
            logger.error(failed)
            # response = failed.response
            # json_response = json.loads(failed.message)
            # raise Exception(response)
            return {"ErrorCode": type(failed), "Message": failed.message}
        # logger.info(dir(response))
        if response.status_code != 200 or json_response.get('ErrorCode', 0) != 0:
            logger.error("%s: %s", response.status_code, response.text)
            # raise Exception(json_response)
            return json_response
        else:
            pass
            # logger.info(json_response)
        # TODO: Record the MessageID on the customer
        return json_response


class Mailer(PostmarkAppBase):

    """
    Wraps the Postmark app REST API for sending emails.
    There is a Mailer instance stored in app.config['mailer'] (created in server.py)

    This Mail Message Format (JSON) is POSTed:
    {
      "From" : "sender@example.com",
      "To" : "John Does <receiver@example.com>",
      "Cc" : "copied@example.com",
      "Bcc": "blank-copied@example.com",
      "Subject" : "Test",
      "Tag" : "Invitation",
      "HtmlBody" : "<b>Hello</b>",
      "TextBody" : "Hello",
      "ReplyTo" : "reply@example.com",
      "Headers" : [{ "Name" : "CUSTOM-HEADER", "Value" : "value" }]
    }
    """

    def __init__(self, api_key):
        super().__init__(api_key)
        self.html_stripper = HTMLToPlainConverter()

    def send(self, message):
        return self._send(message.subject,
                          message.body,
                          message.html,
                          message.sender,
                          message.recipients,
                          message.reply_to,
                          message.cc)

    def _send(self, subject, body, html, sender, recipients, reply_to, cc):
        """
        Sends an html message to the receiver
        Returns a JSON dict where ErrorCode == 0 indicates success, any other value is failure

        Returns Success Response:
        {
          "ErrorCode" : 0,
          "Message" : "OK",
          "MessageID" : "b7bc2f4a-e38e-4336-af7d-e6c392c2f817",
          "SubmittedAt" : "2010-11-26T12:01:05.1794748-05:00",
          "To" : "receiver@example.com"
        }

        Returns Success Response, but with issues:
        {'MessageID': '76fbc507-6684-4f69-82bc-82358d779815',
         'ErrorCode': 0,
         'Message': 'Message OK, but will not deliver to these inactive addresses: unknown@unknown.pub. Inactive recipients are ones that have generated a hard bounce or a spam complaint.',
         'SubmittedAt': '2015-07-09T02:16:11.909255-04:00',
         'To': 'henrik@authors.rocks'}


        Returns Failure Response:
        {
          "ErrorCode": 300,
          "Message": "Zero recipients specified"
        }
        """
        message = {
            'From': sender,
            'To': ','.join(recipients),
           'Subject': subject,
        }
        if html:
           message['HtmlBody'] = html
        if body:
            message['TextBody'] = body
        elif html:
            message['TextBody'] = self.html_stripper.html_to_plain_text(html)
        if reply_to:
            message['ReplyTo'] = reply_to
        if cc:
            message['Cc'] = cc
        return self.json_response(message, 'POST', 'email')


def get_message(subject, recipient, template, **context):
    """Send an email via the Flask-Mail extension.

    :param subject: Email subject
    :param recipient: Email recipient
    :param template: The name of the email template
    :param context: The context to render the template with
    """
    msg = Message(subject,
                  recipients=[recipient])

    ctx = ('security/email', template)
    msg.body = render_template('%s/%s.txt' % ctx, **context)
    msg.html = render_template('%s/%s.html' % ctx, **context)

    return msg


def send_mail_to_admin(subject, body, admin_only=False):
    authors_email = current_app.config.get('AUTHORS_EMAIL')
    authors_admin_email = current_app.config.get('AUTHORS_ADMIN_EMAIL')
    mailer = Mailer(current_app.config.get('MAIL_PASSWORD'))
    recipients = [authors_admin_email]
    if not admin_only:
        recipients.append(authors_email)
    return mailer._send(subject, body, None, authors_email, recipients, None, None)


def send_mail(subject, recipient, template, cc_us=False, **context):
    """
    Replacement for Flask-Security send_mail
    :param subject:
    :param recipient:
    :param template:
    :param context:
    :return:
    """
    msg = get_message(subject, recipient, template, **context)
    authors_email = current_app.config.get('AUTHORS_EMAIL')
    authors_admin_email = current_app.config.get('AUTHORS_ADMIN_EMAIL')
    msg.sender = authors_email
    if cc_us:
        msg.cc = ','.join([authors_email, authors_admin_email])
    mailer = Mailer(current_app.config.get('MAIL_PASSWORD'))
    return mailer.send(msg)


class HTMLToPlainConverter(HTMLParser):
    """Custom html parser to convert html code to plain text."""
    def __init__(self, ignored_elements=None, newline_before_elements=None,
                 newline_after_elements=None, stroke_before_elements=None,
                 stroke_after_elements=None, stroke_text=None,
                 link_footnote=False):
        super().__init__()
        self.reset()
        self.text = ''  # Used to push the results into a variable
        self.links = []  # List of aggregated links
        self.link_footnote = link_footnote
        self.href = None

        # Settings
        if ignored_elements is None:
            self.ignored_elements = [
                'html', 'head', 'body', 'style', 'meta', 'title', 'img']
        else:
            self.ignored_elements = ignored_elements

        if newline_before_elements is None:
            self.newline_before_elements = [
                'br', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'div', 'p', 'li']
        else:
            self.newline_before_elements = newline_before_elements

        if newline_after_elements is None:
            self.newline_after_elements = [
                'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'div', 'p', 'td']
        else:
            self.newline_after_elements = newline_after_elements

        if stroke_before_elements is None:
            self.stroke_before_elements = ['tr']
        else:
            self.stroke_before_elements = stroke_before_elements

        if stroke_after_elements is None:
            self.stroke_after_elements = ['tr']
        else:
            self.stroke_after_elements = stroke_after_elements

        if stroke_text is None:
            self.stroke_text = '------------------------------\n'
        else:
            self.stroke_text = stroke_text

    def handle_starttag(self, tag, attrs):
        """Handles every start tag like e.g. <p>."""
        if (tag in self.newline_before_elements):
            self.text += '\n'
        if (tag in self.stroke_before_elements
                and not self.text.endswith(self.stroke_text)):
            # Put a stroke in front of every relevant element, if there is some
            # content between it and its predecessor
            self.text += self.stroke_text
        if tag == 'a':
            # If it's a link, append it to the link list
            for attr in attrs:
                if attr[0] == 'href':
                    if self.link_footnote:
                        self.links.append((len(self.links) + 1, attr[1]))
                    else:
                        self.href = attr[1]

    def handle_data(self, data):
        """Handles data between tags."""
        # Only proceed with unignored elements
        if self.lasttag not in self.ignored_elements:
            # Remove any predefined linebreaks
            text = data.replace('\n', '')
            # If there's some text left, proceed!
            if text:
                if self.lasttag == 'li':
                    # Use a special prefix for list elements
                    self.text += '  * '
                self.text += text
                # NOTE: Commented out since it added unwanted newlines
                # if self.lasttag in self.newline_after_elements:
                #     # Add a linebreak at the end of the content
                #     self.text += '\n'

    def handle_endtag(self, tag):
        """Handles every end tag like e.g. </p>."""
        if tag in self.stroke_after_elements:
            if self.text.endswith(self.stroke_text):
                # Only add a stroke if there isn't already a stroke posted
                # In this case, there was no content between the tags, so
                # remove the starting stroke
                self.text = self.text[:-len(self.stroke_text)]
            else:
                # If there's no linebreak before the stroke, add one!
                if not self.text.endswith('\n'):
                    self.text += '\n'
                self.text += self.stroke_text
        if tag == 'a':
            if self.link_footnote:
                # If it's a link, add a footnote
                self.text += '[{}]'.format(len(self.links))
            else:
                self.text += ': '
                self.text += self.href
                self.href = None

        elif tag == 'br' and self.text and not self.text.endswith('\n'):
            # If it's a break, check if there's no break at the end of the
            # content. If there's none, add one!
            self.text += '\n'
        # Reset the lasttag, otherwise this parse can geht confused, if the
        # next element is not wrapped in a new tag.

        # TODO: Is this needed?
        # if tag in self.newline_after_elements:
        #     # Add a linebreak at the end of the content
        #     self.text += '\n'

        if tag == self.lasttag:
            self.lasttag = None

    def html_to_plain_text(self, html):
        """Converts html code into formatted plain text."""
        # Use BeautifulSoup to normalize the html
        # soup = BeautifulSoup(html)
        # Init the parser
        # self.feed(str(soup))
        self.feed(html)
        # Strip the end of the plain text
        result = self.text.strip()
        # Add footnotes
        if self.links:
            result += '\n\n'
            for link in self.links:
                result += '[{}]: {}\n'.format(link[0], link[1])
        return result