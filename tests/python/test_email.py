import unittest, json

from app.email import Mailer


class EmailTests(unittest.TestCase):

	def setUp(self):
		pass

	def tearDown(self):
		pass

	def test_email_sends(self):
		mailer = Mailer("ba7663a2-19ba-4a42-bf69-5b4485fcab6f")
        response = mailer._send(subject='test', body='yo son, this is a test of email!',
		        html=None, sender='info@pythondevhouse.com',
		        recipients=['cchilder@mail.usf.edu'],
		        reply_to='unittest@chode.com', cc=None)
		python_response = json.loads(response)
		error_code = python_response['ErrorCode']
		self.assertEqual(error_code, 0)
		
	
		
	
	
	
if __name__ == '__main__':
	