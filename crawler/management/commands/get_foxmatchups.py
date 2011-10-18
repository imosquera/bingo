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
        start_date = datetime.date(2011, 10, 14)
        end_date = datetime.date(2011, 10, 24)
        
        matchups = Matchup.objects.filter(gametime__range=(start_date, end_date))
        for matchup in matchups:
            gametime_str = matchup.gametime.strftime( "%Y%m%d" )
            teamname = matchup.home_team.name.upper()
            if teamname.find(" ") < 0 and matchup.home_team.statfox_name is None:
                matchup.home_team.statfox_name = teamname
                matchup.home_team.save()
            if matchup.home_team.statfox_name is None:
                print "### could find team name for: " + teamname
            else:
                url = param_url % (gametime_str, matchup.home_team.statfox_name)
                download_matchup(matchup, url)
                matchup.save()
                        
def download_matchup(matchup,url):

    m = md5.new()
    m.update( url )
    html_file_path = settings.SITE_DATA_DIR + "/fox_matchups/" + m.hexdigest()
    logger.info("saving here %s" % html_file_path)
    if os.path.exists(html_file_path) and  os.path.getsize(html_file_path) > 40000:
        logger.info("size: " + str(os.path.getsize(html_file_path)) + " so I'm skipping url: " + url)
        return

    html_file = open( html_file_path, "w" )
    html_data = None
    try:
        logger.info("downloading %s" % url)
        html_data = urllib2.urlopen(url).read()
    except urllib2.HTTPError, error:
        if error.code == 500:
            html_data = error.read()
        else:
            logger.exception("error getting contents for url")
            exit(1)
    except:
        logger.exception("could not retrieve matchup: %s %s " % (matchup.insider_game_id,url)  )
        exit(1)
    matchup.filepath = html_file_path
    matchup.save()
    logger.info("saving matchup!")
    html_file.write( html_data )
    html_file.close()
     
