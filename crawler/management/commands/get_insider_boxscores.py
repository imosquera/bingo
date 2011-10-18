#!/usr/bin/env python
import settings
import urllib2,re
from django.core.management.base import BaseCommand, CommandError
import logging
import os,shutil
import md5
logger = logging.getLogger(__name__)
class Command(BaseCommand):

    args = '<poll_id poll_id ...>'
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        matchups_dir = settings.SITE_DATA_DIR + "/insider_boxscore_seasons/2011/"
        if not os.path.exists( matchups_dir ):
            os.makedirs(matchups_dir)

        param_url = "http://www.vegasinsider.com/college-football/scoreboard/scores.cfm/week/%i/season/2010"
        for i in range(1,16):
            url = param_url%i
            print url
            m = md5.new()
            m.update(url)
            filename = matchups_dir + m.hexdigest()
            logger.info( filename + " for url: " + url )
            url_html = urllib2.urlopen( url ).read()
            print filename
            f = open( filename , "w")
            f.write( url_html )
            f.close()
