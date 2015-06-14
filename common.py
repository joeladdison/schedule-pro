#!/usr/bin/env python
#
# Copyright 2011 Joel Addison
#
# Common functions
from google.appengine.api import users
import random
import models


def get_current_user():
    """ Returns a UserAccount object for the current user """
    user = users.get_current_user()
    uaq = models.UserAccount.query() \
        .filter(models.UserAccount.userid == user.user_id())
    ua = uaq.get()
    return ua


def get_rand_colour():
    """ Returns a random colour from the colour list. Used when creating
    projects, calendars and task lists """
    colours = ['000000', '993300', '333300', '000080', '333399', '333333',
               '800000', 'FF6600', '808000', '008000', '008080', '0000FF',
               '666699', '808080', 'FF0000', 'FF9900', '99CC00', '339966',
               '33CCCC', '3366FF', '800080', '999999', 'FF00FF', 'FFCC00']
    rand_colour = "#%s" % colours[random.randrange(1, 24)]
    return rand_colour
