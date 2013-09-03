#!/usr/bin/env python
#
# Copyright 2011 Joel Addison
#
import fix_path
import cgi
import os

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.api import memcache
from google.appengine.ext import db

# Set up Django version and settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from google.appengine.dist import use_library
use_library('django', '1.2')
from google.appengine.ext.webapp import template

import common
import models

class BaseHandler(webapp.RequestHandler):
    """ Defines a class for handling page requests """
    
    def render(self, template_filename, app='', 
               template_args=None, check_reg=True):
        """ A function to render a page view using Google App Engine
        
        render(str, str, str, dict) -> webpage
        template_filename - string containing the template html filename
        app - string: calendar, tasks or projects
        template_args - dictionary of template variables
                
        """

        user = users.get_current_user()
        #uaq = db.GqlQuery("SELECT * FROM UserAccount where user= :1", user)
        #ua = uaq.get()
        ua = common.get_current_user()
        
        
        if user and not ua:
            # If user logged in, but they have no account, redirect them to the
            # create account page
            if check_reg:
                self.redirect('/accounts/create')
        if user and ua:
            # User is logged in, and they have an account
            user_message = "Welcome, %s | <a href=\"%s\">Logout</a>" % \
                            (ua.first_name, users.create_logout_url("/"))
        else:
            # No logged in user
            user_message = "<a href=\"%s\">Login or Register</a>" % \
                            (users.create_login_url("/"))

        # Set up template_args if template does not define any
        if template_args is None:
            template_args = {}
        
        # Template arguments common for all pages
        template_args['current_uri'] = self.request.uri
        template_args['user'] = user
        template_args['ua'] = ua
        template_args['is_admin'] = users.is_current_user_admin()
        template_args['user_message'] = user_message
        
        # Set up the template filepath
        template_file = os.path.join(os.path.dirname(__file__), 'templates', 
                                app, template_filename)
        
        self.response.out.write(template.render(template_file, template_args))
        


class IndexHandler(BaseHandler):
    def get(self):
        self.render("index.html")



