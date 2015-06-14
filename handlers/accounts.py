#!/usr/bin/env python
#
# Copyright 2011 Joel Addison
#
# User Account interface

from google.appengine.api import users

import models
import views
import common


class AccountCreateHandler(views.BaseHandler):
    def get(self):
        """ Renders the Create Account page to the user """
        self.render("account-create.html", "account", check_reg=False)

    def post(self):
        """ Process the new Account data and store in the database """
        current_user = users.get_current_user()
        account = models.UserAccount()
        account.first_name = self.request.get("first_name")
        account.last_name = self.request.get("last_name")
        account.userid = current_user.user_id()
        account.email = current_user.email()
        account.put()

        task_list = models.TaskList()
        task_list.name = account.name
        task_list.owner = account.key
        task_list.description = ''
        task_list.colour = '#000000'
        task_list.put()

        calendar = models.Calendar()
        calendar.owner = account.key
        calendar.name = account.name
        calendar.share_type = "hybrid"
        calendar.colour = '#000000'
        calendar.visible = True
        calendar.put()

        self.redirect("/")


class AccountModifyHandler(views.BaseHandler):
    def get(self):
        ua = common.get_current_user()
        self.render("account-modify.html", "account", {'account': ua})

    def post(self):
        account = common.get_current_user()
        account.first_name = self.request.get("first_name")
        account.last_name = self.request.get("last_name")
        account.userid = users.get_current_user().user_id()
        account.put()
        self.redirect("/")


class AccountLogoutHandler(views.BaseHandler):
    def get(self):
        self.redirect(users.create_logout_url("/"))
