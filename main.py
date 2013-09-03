#!/usr/bin/env python
#
# Copyright 2011 Joel Addison
#
# Main handler for Schedule-Pro
# All page requests are routed to the relevant page handler by this script

import fix_path
import cgi
#import wsgiref.handlers
import os

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.api import users
from google.appengine.ext import db

from handlers import calendar
from handlers import tasks
from handlers import projects
from handlers import accounts
from handlers import ajax
import models
import views
    

# List of URLs and their assigned handler
url_map = [('/', views.IndexHandler),
           ('/accounts/create', accounts.AccountCreateHandler),
           ('/accounts/edit', accounts.AccountModifyHandler),
           ('/calendar', calendar.CalendarHandler),
           ('/calendar/event/add', calendar.EventCreateHandler),
           ('/calendar/event/edit/([-\w]+)', calendar.EventModifyHandler),
           ('/calendar/event/([-\w]+)', calendar.EventViewHandler),
           ('/calendar/event/delete', calendar.EventModifyHandler),
           ('/calendar/add', calendar.CalendarCreateHandler),
           ('/calendar/edit/([-\w]+)', calendar.CalendarModifyHandler),
           ('/calendar/delete', calendar.CalendarModifyHandler),
           ('/tasks', tasks.TasksHandler),
           ('/tasks/list/add', tasks.ListCreateHandler),
           ('/tasks/list/edit/([-\w]+)', tasks.ListModifyHandler),
           ('/tasks/list/delete', tasks.ListModifyHandler),
           ('/tasks/task/add', tasks.TaskCreateHandler),
           ('/tasks/task/edit/([-\w]+)', tasks.TaskModifyHandler),
           ('/tasks/task/delete', tasks.TaskModifyHandler),
           ('/tasks/task/view/([-\w]+)', tasks.TaskViewHandler),
           ('/projects', projects.ProjectsHandler),
           ('/projects/add', projects.ProjectCreateHandler),
           ('/projects/edit/([-\w]+)', projects.ProjectModifyHandler),
           ('/projects/delete', projects.ProjectModifyHandler),
           ('/projects/view/([-\w]+)', projects.ProjectViewHandler),
           ('/ajax/p/details/([-\w]+)', ajax.AjaxPDetailsHandler),
           ('/ajax/tl/tasks/([-\w]+)', ajax.AjaxTlTasksHandler),
           ('/ajax/c/events/([-\w]+)', ajax.AjaxCalEventsHandler),
           ('/ajax/c/details', ajax.AjaxCalDetailsHandler)]

"""
url_map = [ ('/', views.IndexHandler),
        ('/feed', feed.FeedHandler),
        ('/post/(\d+)/([-\w]+)', views.PostHandler),
        ('/tag/([-\w]+)', views.TagHandler),
        ('/about', about.AboutHandler),
        ('/admin', admin.AdminHandler),
        ('/admin/create', admin.CreateHandler),
        ('/admin/edit', admin.EditHandler),
        ('/.*', err.Err404Handler),]
"""
application = webapp.WSGIApplication(url_map, debug=True)
"""
def main():
    wsgiref.handlers.CGIHandler().run(application)
"""

def main():
      
    #application = webapp.WSGIApplication([('/', MainPage)], debug=True)
    #application = webapp.WSGIApplication(url_map, debug=True)
    util.run_wsgi_app(application)

if __name__ == "__main__":
    main()