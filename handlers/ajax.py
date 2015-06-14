#!/usr/bin/env python
#
# Copyright 2011 Joel Addison
#
# AJAX handlers

from google.appengine.ext import ndb
import json
from datetime import datetime

import models
import views


class AjaxPDetailsHandler(views.BaseHandler):
    def get(self, proj_key):
        """ Renders a table with information on the selected project """
        proj_key = ndb.Key(urlsafe=proj_key)
        project = proj_key.get()
        owner = project.owner.get()
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
        """ % (project.name, owner.name, owner.userid,
               project.description, project.key.urlsafe())
        self.response.out.write(details)


class AjaxTlTasksHandler(views.BaseHandler):
    def get(self, tl_key):
        tl_key = ndb.Key(urlsafe=tl_key)
        task_list = tl_key.get()
        owner = task_list.owner.get()

        project_details = ""
        if task_list.project:
            project = task_list.project.get()
            project_details = """
              <tr>
                <td>Project:</td>
                <td><a href="/projects/view/%s">%s</a></td>
              </tr>
            """ % (project.key.urlsafe(), project.name)

        details = """
        <h3>Task List: %s</h3>
        <table>
          <tr>
            <td width="150">Owner:</td>
            <td width="300">%s (%s)</td>
          </tr>
          <tr>
            <td>Description:</td>
            <td>%s</td>
          </tr>%s
        </table>
        <p><a href="/tasks/list/edit/%s">Edit Task List</a></p>
        """ % (task_list.name, owner.name, owner.userid,
               task_list.description, project_details, task_list.key.urlsafe())
        self.response.out.write(details)


class AjaxCalEventsHandler(views.BaseHandler):
    def get(self, cal_key):
        """ Returns a JSON object with events during a given time range from
        the selected calendar """
        cal_key = ndb.Key(urlsafe=cal_key)

        # Change times into datetime structures, instead of UNIX times
        start_date = datetime.fromtimestamp(float(self.request.get('start')))
        end_date = datetime.fromtimestamp(float(self.request.get('end')))

        # Set up query to get events within given time range
        events = models.Event.query() \
            .filter(models.Event.calendar == cal_key) \
            .filter(models.Event.start_time >= start_date) \
            .filter(models.Event.start_time <= end_date) \
            .order(models.Event.start_time)

        events_list = []

        for event in events:
            ev_details = {}
            ev_details['id'] = event.key.urlsafe()
            ev_details['title'] = event.name
            ev_details['location'] = event.location
            ev_details['calendar'] = event.calendar.urlsafe()
            # check for all day event
            if not event.all_day:
                ev_details['allDay'] = False

            # Get start and end times in UNIX times
            # ev_details['start'] = int(time.mktime(event.start_time.timetuple()))
            # ev_details['end'] = int(time.mktime(event.end_time.timetuple()))

            # Get start and end times in ISO8601 format
            ev_details['start'] = event.start_time.strftime('%Y-%m-%dT%H:%M:%S%z')
            ev_details['end'] = event.end_time.strftime('%Y-%m-%dT%H:%M:%S%z')

            # should set the URL to be the location to get more info on event
            ev_details['url'] = "/calendar/event/%s" % event.key.urlsafe()

            # Add the event to the events list
            events_list.append(ev_details)

        # Generate the JSON structure for use by the calendar, and output it
        self.response.content_type = 'application/json'
        self.response.out.write(json.dumps(events_list))


class AjaxCalDetailsHandler(views.BaseHandler):
    def get(self):
        """ Returns a JSON object with details of the selected calendar """
        cal_key = ndb.Key(urlsafe=self.request.get('calendar'))
        calendar = cal_key.get()

        cal_details = {}
        cal_details['key'] = calendar.key.urlsafe()
        cal_details['name'] = calendar.name
        cal_details['colour'] = calendar.colour
        cal_details['visible'] = calendar.visible
        # cal_details['project'] = calendar.project.name

        self.response.content_type = 'application/json'
        self.response.out.write(json.dumps(cal_details))

    def post(self):
        """ Updates the database with new details for the selected calendar """
        cal_key = ndb.Key(urlsafe=self.request.get('calendar'))
        cal_visible = self.request.get('visible')
        if cal_visible == "true":
            visible = True
        else:
            visible = False
        calendar = cal_key.get()
        # calendar.owner = users.get_current_user()
        # calendar.name = name
        # calendar.share_type = share_type
        # calendar.colour = colour
        calendar.visible = visible
        # calendar.project = project
        calendar.put()
