#!/usr/bin/env python
#
# Copyright 2011 Joel Addison
#
# Tasks interface

from google.appengine.ext import db
from google.appengine.api import users
from datetime import datetime
import cgi
import models
import views
import common

class TasksHandler(views.BaseHandler):
    def get(self):
        """ Renders the Tasks page of the website """
        task_lists = models.TaskList.all()
        task_lists.filter("owner = ", common.get_current_user())
        task_lists.order("name")
        
        tasks = models.Task.all()
        tasks.filter("owner = ", common.get_current_user())
        tasks.order("due_date")
            
        self.render('tasks.html', 'tasks', {'task_lists':task_lists, 
                                            'tasks':tasks})

       
class TaskCreateHandler(views.BaseHandler):
    def get(self):
        """ Renders the Add Task form to the user """
        task_lists = models.TaskList.all()
        task_lists.filter("owner = ", common.get_current_user())
        task_lists.order("name")
        
        self.render('task-create.html', 'tasks', {'task_lists':task_lists})
    
    def post(self):
        """ Process the new Task data, to store in the database """
        task_name = cgi.escape(self.request.get('task_name'))
        due_date = datetime.strptime(self.request.get('due_date'), '%Y-%m-%d')
        start_date = datetime.strptime(self.request.get('start_date'), '%Y-%m-%d')
        task_list = db.Key(self.request.get('task_list'))
        percent_complete = int(self.request.get('complete'))
        
        # Save the data to the database
        task = models.Task()
        task.owner = common.get_current_user()
        task.name = task_name
        task.task_list = task_list
        task.due_date = due_date
        task.start_date = start_date
        task.percent_complete = percent_complete
        task.put()
        
        # Redirect the user to the task view page after saving the new task
        self.redirect('/tasks/task/view/%s' % (task.key()))


class TaskModifyHandler(views.BaseHandler):
    def get(self, task_key):
        """ Show the Modify Task form to the user """
        task = db.get(task_key)
        
        task_lists = models.TaskList.all()
        task_lists.filter("owner = ", common.get_current_user())
        task_lists.order("name")
        
        tasks = models.Task.all()
        tasks.filter("task_list = ", task.task_list.key())
        tasks.order("name")     
        
        self.render('task-modify.html', 'tasks', 
                    {'task_lists':task_lists, 'tasks':tasks, 'task': task})
    
    def post(self, task_key):
        """ Process the new Task data, to store in the database """
        task_name = cgi.escape(self.request.get('task_name'))
        due_date = datetime.strptime(self.request.get('due_date'), '%Y-%m-%d')
        start_date = datetime.strptime(self.request.get('start_date'), '%Y-%m-%d')
        task_list = db.Key(self.request.get('task_list'))
        percent_complete = int(self.request.get('complete'))
                
        # Save the data to the database
        task = db.get(task_key)
        task.owner = common.get_current_user()
        task.name = task_name
        task.task_list = task_list
        task.due_date = due_date
        task.start_date = start_date
        task.percent_complete = percent_complete
        task.put()
        
        # Redirect the user to the Task view page after saving the task
        #self.redirect('/tasks/task/view/%s' % (task_key))
        self.redirect('/tasks')
        
class TaskViewHandler(views.BaseHandler):
    def get(self, task_key):
        """ Renders the Task Details page of the website """        
        task = db.get(task_key)
        self.render('task-view.html', 'tasks', {'task': task})


class ListModifyHandler(views.BaseHandler):
    def get(self, tl_key):
        """ Renders the Modify Task List form to the user """
        tl = db.get(tl_key)
        
        projects = models.Project.all()
        projects.filter("owner = ", common.get_current_user())
        projects.order("name")
        
        self.render('list-modify.html', 'tasks', {'projects':projects, 'tl':tl})
    
    def post(self, tl_key):
        """ Process the new Task List data, to store in the database """
        tl_name = cgi.escape(self.request.get('tl_name'))
        description = cgi.escape(self.request.get('description'))
        colour = cgi.escape(self.request.get('colour'))
        
        try:
            project = db.key(self.request.get('project'))
        except AttributeError:
            # Set project to None, as project was set to 'none' by user
            project = None
                    
        # Save the data to the database
        tl = db.get(tl_key)
        tl.owner = common.get_current_user()
        tl.name = tl_name
        tl.description = description
        tl.project = project
        tl.colour = colour
        tl.put()
        
        # Redirect the user to the Task view page after saving the task
        self.redirect('/tasks')

  
class ListCreateHandler(views.BaseHandler):
    def get(self):
        projects = models.Project.all()
        projects.filter("owner = ", common.get_current_user())
        projects.order("name")
        
        rand_col = common.get_rand_colour()
        self.render('list-create.html', 'tasks', {'rand_col':rand_col,
                                                  'projects':projects})
        
    def post(self):
        """ Process the new Task List data, to store in the database """
        tl_name = cgi.escape(self.request.get('tl_name'))
        description = cgi.escape(self.request.get('description'))
        colour = cgi.escape(self.request.get('colour'))
        
        try:
            project = db.key(self.request.get('project'))
        except AttributeError:
            # Set project to None, as project was set to 'none' by user
            project = None
                
        # Save the data to the database
        tl = models.TaskList()
        tl.owner = common.get_current_user()
        tl.name = tl_name
        tl.description = description
        tl.project = project
        tl.colour = colour
        tl.put()
        
        # Redirect the user to the Task view page after saving the task
        #self.redirect('/tasks/task/view/%s' % (task_key))
        self.redirect('/tasks')