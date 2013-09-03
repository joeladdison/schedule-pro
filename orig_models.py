#!/usr/bin/env python
#
# Copyright 2011 Joel Addison
#
# Database Models

from google.appengine.ext import db
from google.appengine.api import users

class UserAccount(db.Model):
    """ Defines a class for storing user information """
    first_name = db.StringProperty()
    last_name = db.StringProperty()
    user = db.UserProperty()
    
    
class Project(db.Model):
    name = db.StringProperty()
    owner = db.UserProperty()
    description = db.StringProperty(multiline=True)
    members = db.ListProperty(users.User)
    colour = db.StringProperty()
    

class TaskList(db.Model):
    """ Defines a database model for storing TaskLists """
    name = db.StringProperty()
    owner = db.UserProperty()
    description = db.StringProperty(multiline=True)
    project = db.ReferenceProperty(Project)
    colour = db.StringProperty()
    
    
class Task(db.Model):
    """ Defines a database model for storing Tasks """
    owner = db.UserProperty()
    name = db.StringProperty(multiline=False)
    task_list = db.ReferenceProperty(TaskList) #reference to a TaskList
    due_date = db.DateTimeProperty()
    start_date = db.DateTimeProperty()
    percent_complete = db.IntegerProperty() 
    assigned_members = db.ListProperty(users.User) #list of Users
    notes = db.TextProperty()
    parent_task = db.SelfReferenceProperty(collection_name='parent_set')
    # add data by passing parent=xx to store who owns the task
    

class Calendar(db.Model):
    name = db.StringProperty()
    owner = db.UserProperty()
    share_type = db.StringProperty()
    colour = db.StringProperty()
    visible = db.BooleanProperty()
    project = db.ReferenceProperty(Project)
    

class Event(db.Model):
    name = db.StringProperty()
    start_time = db.DateTimeProperty()
    end_time = db.DateTimeProperty()
    all_day = db.BooleanProperty()
    calendar = db.ReferenceProperty(Calendar)
    location = db.StringProperty(multiline=True)
    notes = db.TextProperty()
    sharing = db.StringProperty()
