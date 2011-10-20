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
year = "2011"
class Command(BaseCommand):

    args = '<poll_id poll_id ...>'
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        path = "/usr/local/bingodata/insider_matchups/%s/" % year
        paths = [path + f + "/matchup" for f in os.listdir(path)]
        for p in paths:
            logger.info(p)
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
        logger.error("couldn't find teams")
        logger.error(matchup_table)
        return

    date_re = re.compile("date/(.*?)/time")
    anchor_tag = matchup_table.find(href=date_re)
    matchup_date_str = date_re.search(anchor_tag['href']).group(1)
    matchup_date = time.strptime(matchup_date_str,"%m-%d-%y")

    matchup = Matchup()
    insider_game_id = "%s-@-%s" % (away_team.name.replace(' ','-'), home_team.name.replace(' ','-'))
    gametime = strftime("%Y-%m-%d",  matchup_date)
    found_matchups = Matchup.objects.filter(insider_game_id=insider_game_id, gametime=gametime, season=year)
    if len(found_matchups) > 1:
        logger.error("!! there can't be more than one matchup for:%s and time %s",(insider_game_id, gametime))
    if len(found_matchups) == 1:
        matchup = found_matchups[0]


    matchup.insider_game_id = insider_game_id
    matchup.gametime = gametime
    matchup.home_team = home_team
    matchup.away_team = away_team
    matchup.season = year
    get_lines( matchup, matchup_table )
    try:
        matchup.save()
    except:
        logger.exception("problem saving matchup for game id: " + matchup.insider_game_id)
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
        return (None, None)

def get_clean_stat(column_data):
    clean_stat = column_data.string.strip().replace("&nbsp;", "")
    if clean_stat == "XX":
        return None
    if clean_stat == "PK":
        clean_stat = 0
    if clean_stat == "":
        return None
    return float(clean_stat)

def get_abs_value(column_data, i):
    if column_data and i == 4:
        return math.fabs(column_data)
    else:
        return column_data

def get_lines( matchup, matchup_table ):
    rows = matchup_table.findAll("tr")

    for i in (4,5):
        column_data = rows[i].findAll("td")
        column_stat1 = get_clean_stat( column_data[3])
        column_stat2 = get_clean_stat( column_data[4])
        if column_stat1 == "" and  column_stat2 == "":
            return

        is_over_under = False
        if column_stat1 >0 or column_stat2 >0:
            is_over_under =True

        if is_over_under:
            matchup.over_under = column_stat2
        else:
            matchup.starting_line = get_abs_value(column_stat1,i)
            matchup.current_line = get_abs_value(column_stat2,i)

    ### now we'll get the results if possible
    result_spread = None
    total_score = None
    home_win_ats = False
    for i in (4,5):
        all_column_data = rows[i].findAll("td")
        if len(all_column_data) < 9:
            continue

        result_data = all_column_data[8]
        result_data_str = result_data.string.strip()
        if result_data_str == "Push":
            matchup.home_win_ats = "push"
            matchup.away_win_ats = "push"

        try:
            if result_data_str.find("Cover") > -1 and i == 4:
                matchup.home_win_ats = "loss"
                matchup.away_win_ats = "win"

            if result_data_str.find("Cover") > -1 and i == 5:
                matchup.home_win_ats = "win"
                matchup.away_win_ats = "loss"
        except:
            logger.exception("error when find result spread: " + matchup.insider_game_id )
