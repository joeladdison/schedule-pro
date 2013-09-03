#!/usr/bin/env python
#
# Copyright 2011 Joel Addison
#
# Calendar interface

from google.appengine.ext import db
from google.appengine.api import users

import cgi
from datetime import datetime
import models
import views
import common

class CalendarHandler(views.BaseHandler):
    def get(self):
        """ Renders the Calendar page of the website """
        calendars = models.Calendar.all()
        calendars.filter("owner = ", common.get_current_user())
        calendars.order("name")
        self.render('calendar.html', 'calendar', {'calendars': calendars})


class CalendarCreateHandler(views.BaseHandler):
    def get(self):
        """ Renders the Create Calendar page of the website """
        projects = models.Project.all()
        projects.filter("owner = ", common.get_current_user())
        projects.order("name")
        
        rand_col = common.get_rand_colour()
        self.render('calendar-create.html', 'calendar', {'rand_col':rand_col,
                                                  'projects':projects})
        
    def post(self):
        """ Process the new Calendar data, to store in the database """
        name = cgi.escape(self.request.get('name'))
        share_type = self.request.get('share_type')
        colour = cgi.escape(self.request.get('colour'))
        
        try:
            project = db.key(self.request.get('project'))
        except AttributeError:
            # Set project to None, as project was set to 'none' by user
            project = None
                
        # Save the data to the database
        calendar = models.Calendar()
        calendar.owner = common.get_current_user()
        calendar.name = name
        calendar.share_type = share_type
        calendar.colour = colour
        calendar.visible = True
        calendar.project = project
        calendar.put()

        # Redirect the user to the Calendar page after saving the calendar
        self.redirect('/calendar')


class CalendarModifyHandler(views.BaseHandler):
    def get(self, cal_key):
        """ Renders the Modify Calendar form to the user """
        calendar = db.get(cal_key)
        
        projects = models.Project.all()
        projects.filter("owner = ", common.get_current_user())
        projects.order("name")
        
        self.render('calendar-modify.html', 'calendar', {'projects':projects,
                                                  'calendar':calendar})
    
    def post(self, cal_key):
        """ Process the new Calendar data, to store in the database """
        name = cgi.escape(self.request.get('name'))
        share_type = self.request.get('share_type')
        colour = cgi.escape(self.request.get('colour'))
        
        try:
            project = db.key(self.request.get('project'))
        except AttributeError:
            # Set project to None, as project was set to 'none' by user
            project = None
                
        # Save the data to the database
        calendar = db.get(cal_key)
        calendar.owner = common.get_current_user()
        calendar.name = name
        calendar.share_type = share_type
        calendar.colour = colour
        calendar.visible = calendar.visible
        calendar.project = project
        calendar.put()
        
        # Redirect the user to the Calendar page after saving the calendar
        self.redirect('/calendar')


class EventCreateHandler(views.BaseHandler):
    def get(self):
        """ Renders the Create Event form to the user """
        calendars = models.Calendar.all()
        calendars.filter("owner = ", common.get_current_user())
        calendars.order("name")
        
        self.render('event-create.html', 'calendar', {'calendars':calendars})
        
    def post(self):
        """ Process the Event data to store in the database """
        name = cgi.escape(self.request.get('name'))
        start_date = self.request.get('start_date')
        start_time = self.request.get('start_time')
        end_date = self.request.get('end_date')
        end_time = self.request.get('end_time')
        calendar = db.Key(self.request.get('calendar'))
        location = cgi.escape(self.request.get('location'))
        notes = cgi.escape(self.request.get('notes'))
        sharing = self.request.get('sharing')
        
        if self.request.get('all_day') == "1":
            all_day = True
            start = start_date
            end = end_date
            time_format = "%d/%m/%Y"
        else:
            all_day = False
            start = "%s %s" % (start_date, start_time)
            end = "%s %s" % (end_date, end_time)
            time_format = "%d/%m/%Y %I:%M%p"

        # Change strings into datetime for database
        start_dt = datetime.strptime(start, time_format)
        end_dt = datetime.strptime(start, time_format)

        # Store the event in the database
        event = models.Event()
        event.name = name #db.StringProperty()
        event.start_time = start_dt #db.DateTimeProperty()
        event.end_time = end_dt #db.DateTimeProperty()
        event.all_day = all_day #db.BooleanProperty()
        event.calendar = calendar #db.ReferenceProperty()
        event.location = location #db.StringProperty(multiline=True)
        event.notes = notes #db.TextProperty()
        event.sharing = sharing #db.StringProperty()
        event.put()
        
        #self.response.out.write(start_dt)
        #self.response.out.write("&nbsp;&nbsp;,&nbsp;&nbsp;")
        #self.response.out.write(end_dt)
        #self.response.out.write("<br /><br />")
        #self.response.out.write((name, start_date, start_time, end_date, end_time))
        #self.response.out.write(str(all_day))
        
        # Redirect user to Calendar page after saving the event
        self.redirect('/calendar')
    
class EventModifyHandler(views.BaseHandler):
    def get(self, event_key):
        """ Render the Modify Event form to the user """
        event = db.get(event_key)
        
        calendars = models.Calendar.all()
        calendars.filter("owner = ", common.get_current_user())
        calendars.order("name")
        
        self.render('event-modify.html', 'calendar', {'event':event,
                                                  'calendars':calendars})

    def post(self, event_key):
        pass
    

class EventViewHandler(views.BaseHandler):
    def get(self, event_key):
        """ Render the Event Details page of the website """
        event = db.get(event_key)
        calendar = db.get(event.calendar.key())
        
        self.render('event-view.html', 'calendar', {'event':event,
                                                  'calendar':calendar})
    