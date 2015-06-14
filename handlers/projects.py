#!/usr/bin/env python
#
# Copyright 2011 Joel Addison
#
# Project interface

from google.appengine.ext import ndb

import cgi
import models
import views
import common


class ProjectsHandler(views.BaseHandler):
    def get(self):
        """ Renders the Projects page of the Schedule-Pro website """
        projects = models.Project.query() \
            .filter(models.Project.owner == common.get_current_user().key) \
            .order(models.Project.name)

        self.render('projects.html', 'projects', {'projects': projects})


class ProjectCreateHandler(views.BaseHandler):
    def get(self):
        """ Renders the Create Project page of the website """
        rand_col = common.get_rand_colour()
        self.render('project-create.html', 'projects', {'rand_col': rand_col})

    def post(self):
        """ Processes the data from the Create Project page
        Creates a Task List and Calendar for the project

        """
        project = models.Project()
        project.name = cgi.escape(self.request.get('name'))
        project.owner = common.get_current_user().key
        project.description = cgi.escape(self.request.get('description'))
        # members = db.ListProperty(users.User)
        project.colour = self.request.get('colour')
        project.put()

        # Create a Task List for the project
        tl = models.TaskList()
        tl.name = project.name
        tl.owner = project.owner
        tl.description = project.description
        tl.project = project.key
        tl.colour = project.colour
        tl.put()

        # Create a calendar for the project
        calendar = models.Calendar()
        calendar.owner = project.owner
        calendar.name = project.name
        calendar.share_type = "hybrid"
        calendar.colour = project.colour
        calendar.visible = True
        calendar.put()

        # self.redirect('/projects/view/%s' % (project.key))
        self.redirect('/projects')


class ProjectModifyHandler(views.BaseHandler):
    def get(self, proj_key):
        """ Renders the Edit Project page of the website """
        proj_key = ndb.Key(urlsafe=proj_key)
        project = proj_key.get()
        self.render('project-modify.html', 'projects', {'project': project})

    def post(self, proj_key):
        """ Processes the data from the Edit Project page """
        proj_key = ndb.Key(urlsafe=proj_key)
        project = proj_key.get()
        project.name = self.request.get('name')
        project.owner = common.get_current_user().key
        project.description = self.request.get('description')
        project.colour = self.request.get('colour')
        project.put()

        # members = db.ListProperty(users.User)
        # self.redirect('/projects/view/%s' % (proj_key))
        self.redirect('/projects')


class ProjectViewHandler(views.BaseHandler):
    def get(self, proj_key):
        """ Renders the Project Details page of the website """
        proj_key = ndb.Key(urlsafe=proj_key)
        project = proj_key.get()
        self.render('project-view.html', 'projects', {'project': project})
