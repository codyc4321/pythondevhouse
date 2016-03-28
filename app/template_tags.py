from jinja2 import Markup, escape

def render_collaborative(css_class, duration, header, paragraph):
    duration = str(duration)
    return Markup("{0}{1}{2}{3}{4}{5}{6}".format(
                """<div class="col-sm-4">""",
                """    <div class="single_feature wow slideInUp" data-wow-duration="{}s">""".format(duration),
                """    <i class="fa {}"></i>""".format(css_class),
                """<h3>{}</h3>""".format(header),
                """<p>{}</p>""".format(paragraph),
                """    </div>""",
                """</div>"""))
        
def render_skill(skill, aria_now, aria_value):
    aria_now = str(aria_now)
    aria_value = str(aria_value)
    return Markup("{0}{1}{2}{3}{4}".format(
                """<p>{}</p>""".format(skill),
                """<div class="maintainer progress wow slideInUp">""",
                """    <div class="bar progress-bar" role="progressbar" aria-valuenow="{aria_now}" \
aria-valuemin="0" aria-valuemax="{aria_value}" style="width: 0%;">""".format(aria_now=aria_now, aria_value=aria_value),
                """    </div>""",
                """</div>"""
                ))