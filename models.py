#!/usr/bin/env python
#
# Copyright 2011 Joel Addison
#
# Database Models

from google.appengine.ext import ndb


class UserAccount(ndb.Model):
    """ Defines a class for storing user information """
    first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()
    userid = ndb.StringProperty()
    email = ndb.StringProperty()

    @property
    def name(self):
        """ Returns the name of the user - "First Last" """
        return "%s %s" % (self.first_name, self.last_name)


class Project(ndb.Model):
    name = ndb.StringProperty()
    owner = ndb.KeyProperty(kind=UserAccount)
    description = ndb.StringProperty()
    members = ndb.KeyProperty(kind=UserAccount, repeated=True)
    colour = ndb.StringProperty()


class TaskList(ndb.Model):
    """ Defines a database model for storing TaskLists """
    name = ndb.StringProperty()
    owner = ndb.KeyProperty(kind=UserAccount)
    description = ndb.StringProperty()
    project = ndb.KeyProperty(kind=Project)
    colour = ndb.StringProperty()


class Task(ndb.Model):
    """ Defines a database model for storing Tasks """
    owner = ndb.KeyProperty(kind=UserAccount)
    name = ndb.StringProperty()
    task_list = ndb.KeyProperty(kind=TaskList)
    due_date = ndb.DateTimeProperty()
    start_date = ndb.DateTimeProperty()
    percent_complete = ndb.IntegerProperty()
    assigned_members = ndb.KeyProperty(kind=UserAccount, repeated=True)
    notes = ndb.TextProperty()
    parent_task = ndb.KeyProperty(kind='Task')
    # add data by passing parent=xx to store who owns the task


class Calendar(ndb.Model):
    name = ndb.StringProperty()
    owner = ndb.KeyProperty(kind=UserAccount)
    share_type = ndb.StringProperty()
    colour = ndb.StringProperty()
    visible = ndb.BooleanProperty()
    project = ndb.KeyProperty(kind=Project)


class Event(ndb.Model):
    name = ndb.StringProperty()
    start_time = ndb.DateTimeProperty()
    end_time = ndb.DateTimeProperty()
    all_day = ndb.BooleanProperty()
    calendar = ndb.KeyProperty(kind=Calendar)
    location = ndb.StringProperty()
    notes = ndb.TextProperty()
    sharing = ndb.StringProperty()
