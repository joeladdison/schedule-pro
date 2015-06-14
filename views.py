#!/usr/bin/env python
#
# Copyright 2011 Joel Addison
#

import os
import datetime
import webapp2
from webapp2_extras import jinja2
from google.appengine.api import users

import common


class BaseHandler(webapp2.RequestHandler):
    """ Defines a class for handling page requests """

    @webapp2.cached_property
    def jinja2(self):
        return jinja2.get_jinja2(app=self.app)

    def render(self, template_filename, app='',
               template_args=None, check_reg=True):
        """ A function to render a page view using Google App Engine

        render(str, str, str, dict) -> webpage
        template_filename - string containing the template html filename
        app - string: calendar, tasks or projects
        template_args - dictionary of template variables
        """

        user = users.get_current_user()
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
        template_args['now'] = datetime.datetime.now()

        # Set up the template filepath
        filename = os.path.join(app, template_filename)

        self.response.write(
            self.jinja2.render_template(filename, **template_args))


class IndexHandler(BaseHandler):
    def get(self):
        self.render("index.html")
