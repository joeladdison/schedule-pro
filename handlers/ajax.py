#!/usr/bin/env python
#
# Copyright 2011 Joel Addison
#
# AJAX handlers

from google.appengine.ext import db
from google.appengine.api import users
from django.utils import simplejson as json
from datetime import datetime
import time

import models
import views
import common

class AjaxPDetailsHandler(views.BaseHandler):
    def get(self, proj_key):
        """ Renders a table with information on the selected project """
        project = db.get(proj_key)

        details = """
        <h3>Project: %s</h3>
        <table>
          <tr>
            <td width="150">Project Owner:</td>
            <td width="300">%s (%s)</td>
          </tr>
          <tr>
            <td>Description:</td>
            <td>%s</td>
          </tr>
          <tr>
            <td>Assigned Members:</td>
            <td>&nbsp;</td>
          </tr>
        </table>
        <p><a href="/projects/edit/%s">Edit Project</a></p>
        """ % (project.name, project.owner.name, project.owner.user,
                project.description, project.key())
        self.response.out.write(details) 
        
        
class AjaxTlTasksHandler(views.BaseHandler):
    def get(self, tl_key):
        
        project = db.get(tl_key)
        # Get owner details
        owner_qry = db.GqlQuery("SELECT * FROM UserAccount where user= :1",
                                    project.owner)
        owner = owner_qry.get()
        
        details = """
        <h3>Project: %s</h3>
        <table>
          <tr>
            <td width="150">Project Owner:</td>
            <td width="300">%s %s (%s)</td>
          </tr>
          <tr>
            <td>Description:</td>
            <td>%s</td>
          </tr>
          <tr>
            <td>Assigned Members:</td>
            <td>&nbsp;</td>
          </tr>
        </table>
        <p><a href="/projects/edit/%s">Edit Project</a></p>
        """ % (project.name, owner.first_name, owner.last_name,
                           project.owner, project.description, project.key())
        self.response.out.write(details)
        

class AjaxCalEventsHandler(views.BaseHandler):
    def get(self, cal_key):
        """ Returns a JSON object with events during a given time range from 
        the selected calendar """
        cal_key = db.Key(cal_key)
        
        # Change times into datetime structures, instead of UNIX times
        start_date = datetime.fromtimestamp(float(self.request.get('start')))
        end_date = datetime.fromtimestamp(float(self.request.get('end')))
        
        # Set up query to get events within given time range
        events = models.Event.all()
        events.filter("calendar = ", cal_key)
        events.filter("start_time >= ", start_date)
        events.filter("start_time <= ", end_date)
        events.order("start_time")
        
        events_list = []
        
        for event in events:
            ev_details = {}
            ev_details['id'] = str(event.key())
            ev_details['title'] = event.name
            ev_details['location'] = event.location
            # check for all day event
            if not event.all_day:
                ev_details['allDay'] = False
                
            # Get start and end times in UNIX times
            #ev_details['start'] = int(time.mktime(event.start_time.timetuple()))
            #ev_details['end'] = int(time.mktime(event.end_time.timetuple()))
            
            # Get start and end times in ISO8601 format
            ev_details['start'] = event.start_time.strftime('%Y-%m-%dT%H:%M:%S%z')
            ev_details['end'] = event.end_time.strftime('%Y-%m-%dT%H:%M:%S%z')
            
            # should set the URL to be the location to get more info on event
            ev_details['url']= "/calendar/event/%s" % event.key()
            
            # Add the event to the events list
            events_list.append(ev_details)
        
        # Generate the JSON structure for use by the calendar, and output it
        self.response.out.write(json.dumps(events_list))
            
        
class AjaxCalDetailsHandler(views.BaseHandler):
    def get(self):
        """ Returns a JSON object with details of the selected calendar """
        cal_key = db.Key(self.request.get('calendar'))
        calendar = db.get(cal_key)
        
        cal_details = {}
        cal_details['key'] = str(calendar.key())
        cal_details['name'] = calendar.name
        cal_details['colour'] = calendar.colour
        cal_details['visible'] = calendar.visible
        #cal_details['project'] = calendar.project.name
        
        self.response.out.write(json.dumps(cal_details))
        
    def post(self):
        """ Updates the database with new details for the selected calendar """
        cal_key = db.Key(self.request.get('calendar'))
        cal_visible = self.request.get('visible')
        if cal_visible == "true":
            visible = True
        else:
            visible = False
        calendar = db.get(cal_key)
        #calendar.owner = users.get_current_user()
        #calendar.name = name
        #calendar.share_type = share_type
        #calendar.colour = colour
        calendar.visible = visible
        #calendar.project = project
        calendar.put()

        
        
