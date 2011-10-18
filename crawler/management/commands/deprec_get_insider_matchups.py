import settings
import urllib2,re, time, datetime, os, md5
from BeautifulSoup import BeautifulSoup
from django.core.management.base import BaseCommand, CommandError
from bingo.matchups.models import Matchup, MatchupTrend, Team
from time import strftime
import math
import logging
logger = logging.getLogger(__name__)
class Command(BaseCommand):

    args = '<poll_id poll_id ...>'
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):

        param_url = "http://www.statfox.com/cfb/expanded~sportid~cfb~gameid~%s%s.htm"
        param_url = "http://www.vegasinsider.com/college-football/scoreboard/boxscores/%s-@-%s.cfm/date/%s"
        start_date = datetime.date(2011, 10, 14)
        end_date = datetime.date(2011, 10, 24)
        
        matchups = Matchup.objects.filter(gametime__range=(start_date, end_date))
        for matchup in matchups:
            gametime_str = matchup.gametime.strftime( "%m-%-d-%y" )
            teamname = matchup.home_team.name.upper()
            if teamname.find(" ") < 0 and matchup.home_team.statfox_name is None:
                matchup.home_team.statfox_name = teamname
                matchup.home_team.save()
            if matchup.home_team.statfox_name is None:
                print "### could find team name for: " + teamname
            else:
                url = param_url % (matchup.away_team.name.replace(" ", "-"),matchup.home_team.name.replace(" ","-"),gametime_str)
                download_matchup(matchup, url)
                matchup.save()
                        
def download_matchup(matchup,url):

    m = md5.new()
    m.update( url )
    html_file_path = settings.SITE_DATA_DIR + "/insider_matchups/" + m.hexdigest()
    logger.info("saving here %s" % html_file_path)
    if os.path.exists(html_file_path) and  os.path.getsize(html_file_path) > 40000:
        logger.info("size: " + str(os.path.getsize(html_file_path)) + " so I'm skipping url: " + url)
        return

    html_file = open( html_file_path, "w" )
    html_data = None
    try:
        logger.info("downloading %s" % url)
        html_data = urllib2.urlopen(url).read()
        logger.info("size of html: " + str(len(html_data)) )
    except:
        logger.exception("could not retrieve matchup: %s %s " % (matchup.insider_game_id,url)  )
        exit(1)
    matchup.insider_matchup_path = html_file_path
    matchup.save()
    logger.info("saving matchup!")
    html_file.write( html_data )
    html_file.close()
     
