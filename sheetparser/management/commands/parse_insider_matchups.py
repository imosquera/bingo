#!/usr/bin/env python
import settings
import urllib2,re, time, datetime, os
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
        path = "/usr/local/bingodata/insider_matchups/2011/"
        paths = [path + f for f in os.listdir(path)]
        paths = ["/usr/local/bingodata/insider_matchups/e85fecad623edbb7d1af651079a44d4a"]
        for p in paths:
            logger.debug(p)
            parse_path(p)

def parse_path(path):
    f = open(path, "r")
    html = f.read() 
    soup = BeautifulSoup(html)
    all_matchups = soup.findAll("td",  { "class" : "viHeaderNorm" })
    for matchup_data in all_matchups:
        parse_matchup(matchup_data)
    
def parse_matchup(matchup_data):
    matchup_table = matchup_data.findParent("table")    
    team_rx = re.compile(".*college-football/teams/team-page.cfm/team.*")
    teams = matchup_table.findAll("a", href=team_rx)
    away_team, home_team = get_teams(teams)
    if away_team == None or home_team == None:
        #if we dont find a team go onto the next team matchup
        return
    
    date_re = re.compile("date/(.*?)/time")
    anchor_tag = matchup_table.find(href=date_re)
    matchup_date_str = date_re.search(anchor_tag['href']).group(1)
    matchup_date = time.strptime(matchup_date_str,"%m-%d-%y")

    matchup = Matchup()
    insider_game_id = "%s-@-%s" % (away_team.name.replace(' ','-'), home_team.name.replace(' ','-'))
    gametime = strftime("%Y-%m-%d",  matchup_date)
    found_matchups = Matchup.objects.filter(insider_game_id=insider_game_id, gametime=gametime)
    if len(found_matchups) > 0:
        matchup = found_matchups[0]

    matchup.insider_game_id = insider_game_id
    matchup.gametime = gametime
    matchup.home_team = home_team
    matchup.away_team = away_team
    get_lines( matchup, matchup_table )
    try:
        matchup.save()
    except:
        logger.exception("problem saving matchup for game id: " + matchup.insider_game_id)
        logger.exception("path: " + path)
        exit(1)
 
def clean_team_name(team_name):
    team_name = team_name.replace("(oh)", "ohio")
    team_name = team_name.replace("(fl)", "florida")
    return team_name

def get_teams(teams):
    try: 
        away_team_name = clean_team_name(teams[0].string.strip().lower())
        home_team_name = clean_team_name(teams[1].string.strip().lower())

        home_team = Team(name=home_team_name)
        away_team = Team(name=away_team_name)
        home_team.save()
        away_team.save()
        return (away_team, home_team)
    except: 
        logger.error("problem parsing teams!")
        logger.error(teams)
        logger.error("continuing....")
        return (None, None)
 
def get_lines( matchup, matchup_table ):
    rows = matchup_table.findAll("tr")
    for i in (4,5):
        column_data = rows[i].findAll("td")
        column_stat1 = column_data[3].string.strip().replace("&nbsp;", "")
        column_stat2 = column_data[4].string.strip().replace("&nbsp;", "")
        if column_stat1 == "" and column_stat2 == "":
            return

        is_over_under = False
        if column_stat1 == "": is_over_under = True
        if is_over_under:
            matchup.over_under = column_stat2
        else:
            if i == 4:
                column_stat1 = math.fabs( float(column_stat1) )
                column_stat2 = math.fabs( float(column_stat2) )
            matchup.starting_line = column_stat1
            matchup.current_line = column_stat2
