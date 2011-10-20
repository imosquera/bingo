#!/usr/bin/env python
import settings
import urllib2,re
from django.core.management.base import BaseCommand, CommandError
import logging
import os,shutil
import md5
logger = logging.getLogger(__name__)
year = "2007"

class Command(BaseCommand):

    args = '<poll_id poll_id ...>'
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
     
        param_url = "http://www.vegasinsider.com/college-football/matchups/matchups.cfm/week/%i/season/%s"
        matchup_dir_param = settings.SITE_DATA_DIR + "/insider_matchups/%s/%i" 
        for i in range(1,16):
            matchups_dir = matchup_dir_param % (year, i)
            if not os.path.exists( matchups_dir):
                os.makedirs(matchups_dir)

            url = param_url%(i, year)
            logger.info("URL: %s" % url)

            filename = matchups_dir + "/matchup"
            logger.info( filename + " for url: " + url )
            url_html = urllib2.urlopen( url ).read()
            print filename
            f = open( filename , "w")
            f.write( url_html )
            f.close()
