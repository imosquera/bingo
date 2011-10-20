import settings
import urllib2,re, time, datetime, os
from BeautifulSoup import BeautifulSoup
from django.core.management.base import BaseCommand, CommandError
from bingo.matchups.models import Matchup, MatchupTrend, Team
from time import strftime
import math
import logging
logger = logging.getLogger(__name__)
DEBUG=False
YEAR = "2008"

class Command(BaseCommand):

    args = '<poll_id poll_id ...>'
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        path = "/usr/local/bingodata/insider_boxscore_seasons/%s/" % YEAR
        paths = [path + f for f in os.listdir(path)]
        #paths = ["/usr/local/bingodata/insider_boxscore_seasons/2011/b51bdc5b69502c4f9fac30bbac7618e9"]
        for p in paths:
            logger.info("path is %s" % p)
            parse_path(p)

def parse_path(path):
    f = open(path, "r")
    html = f.read() 
    soup = BeautifulSoup(html)
    all_matchups = soup.findAll("td",  { "class" : "sportPicksBorder" })
    for matchup_data in all_matchups:
        parse_matchup(matchup_data)
    
def parse_matchup(matchup_data):
    matchup_table = matchup_data.find("table")    
    team_rx = re.compile(".*college-football/teams/team-page.cfm/team.*")
    teams = matchup_table.findAll("a", href=team_rx)
    away_team, home_team = get_teams(teams)
    if away_team == None or home_team == None:
        #if we dont find a team go onto the next team matchup
        return

    matchup_date = None
    try:
        date_re = re.compile("date/(.*)")
        anchor_tag = matchup_table.find(href=date_re)
        matchup_date_str = date_re.search(anchor_tag['href']).group(1)
        matchup_date = datetime.datetime.strptime(matchup_date_str,"%m-%d-%y")
    except:
        logger.exception( "matchup date could not be found" )
        logger.error( "anchor tag: " + str(anchor_tag ) )    
        logger.error( "matchup: " + matchup_table.prettify() )    
        return

    matchup = Matchup()
    insider_game_id = "%s-@-%s" % (away_team.name.replace(' ','-'), home_team.name.replace(' ','-'))
    found_matchups = Matchup.objects.filter(insider_game_id=insider_game_id, gametime=matchup_date, season=YEAR)
    if len(found_matchups) > 0:
        matchup = found_matchups[0]
    else:
        logger.info("!! could not find matchup for: " +insider_game_id + " and date: " + str(matchup_date_str) )
    matchup.insider_game_id = insider_game_id
    matchup.gametime = matchup_date
    matchup.home_team = home_team
    matchup.away_team = away_team
    matchup.season = int(YEAR)
    get_lines_and_score( matchup, matchup_table )
    logger.info("final score was: %s to %s for game: %s " % (str(matchup.away_score), str(matchup.home_score), matchup.insider_game_id) )
    try:
        if not DEBUG:
            matchup.save()
    except:
        logger.exception("problem saving matchup for game id: " + matchup.insider_game_id)
        logger.exception("path: " + path)
        exit(1)
 
def clean_team_name(team_tag):
    team_re = re.compile("team/(.*)")
    team_name = team_re.search( team_tag['href'] ).group(1)
    team_name = team_name.replace("(oh)", "ohio")
    team_name = team_name.replace("(fl)", "florida")
    return team_name

def get_teams(teams):
    try: 

        away_team_name = clean_team_name(teams[0])
        home_team_name = clean_team_name(teams[1])

        home_team = Team(name=home_team_name)
        away_team = Team(name=away_team_name)
        if not DEBUG:
            home_team.save()
            away_team.save()
        return (away_team, home_team)
    except: 
        logger.exception("problem parsing teams!")
        logger.error(teams)
        logger.error("continuing....")
        exit(1)
        return (None, None)


def get_clean_stat(data):
    return data.string.strip().replace("&nbsp;", "")

def get_lines_and_score( matchup, matchup_table ):
    rows = matchup_table.findAll("tr")
    for i in (3,4):
        column_data = rows[i].findAll("td")
        line_stat = get_clean_stat(column_data[2])
        if line_stat == "":
            logger.error("line stat was empty for matchup: " + str(matchup.id) + " matchup insider: " + matchup.insider_game_id )
            logger.error("potentially there is no line for this game")
        else:
            line_stat = float(line_stat)
            if line_stat > 0:
                matchup.over_under = line_stat
                #logger.info("matchup over under is: " + str(matchup.over_under) )
            else:
                if i == 3:
                    line_stat = math.fabs( float(line_stat) )
                matchup.current_line = line_stat
                #logger.info("current line is: " + str(line_stat))
            #now we need to get the final score if it has been played
        today = datetime.date.today()
        if matchup.gametime.date() < today:
            try:
                final_score_stat = None
                if column_data[7].font:
                    final_score_stat = get_clean_stat(column_data[7].font.b)
                else:
                    #overtime score has moved over to the right by one column
                    final_score_stat = get_clean_stat(column_data[8].font.b)
                if i == 4:
                    matchup.home_score = int(final_score_stat)
                else:
                    matchup.away_score = int(final_score_stat)
            except:
                logger.exception("could not get final score for game: %s" % matchup.insider_game_id)
                logger.error(column_data[7].prettify())
                exit(1)
