
#!/usr/bin/env python
    
from app import application
from app.template_tags import render_collaborative, render_skill

application.jinja_env.globals["render_collaborative"] = render_collaborative
application.jinja_env.globals["render_skill"] = render_skill

if __name__ == '__main__':
    application.run(host='0.0.0.0', debug=True)