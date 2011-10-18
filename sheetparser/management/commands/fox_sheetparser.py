#!/usr/bin/env python
import settings
import urllib2,re, datetime
from BeautifulSoup import BeautifulSoup
from django.core.management.base import BaseCommand, CommandError
from bingo.matchups.models import Matchup, MatchupTrend
import logging
logger = logging.getLogger(__name__)
class Command(BaseCommand):

    args = '<poll_id poll_id ...>'
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        start_date = datetime.date(2011, 10, 14)
        end_date = datetime.date(2011, 10, 24)
        
        matchups = Matchup.objects.filter(gametime__range=(start_date, end_date))
        for matchup in matchups[0:1]:
            parse_sheet(matchup)
        return

def parse_sheet(matchup):
    logger.info("parsing matchup: " + matchup.insider_game_id)
    sheet_page_html = open(matchup.filepath, "r").read()
    soup = BeautifulSoup(sheet_page_html)
    all_matchup_trends = matchup.matchup_trends.all().delete()
    #gameid_form = soup.find("form", action=re.compile("gameid=(.*?)&"))
    team_trends = soup.find(text=re.compile('.*Key Performance Information.*'))
    team_trends = team_trends.findNext("table")
    
    f = open("/tmp/write.html", "w")
    data_table = team_trends.findAll("tr")[1].td.table
    
    f.write(data_table.prettify())
    f.close()

    """
    for team_trend in team_trends:
        team_name = team_trend.string.split("-")[0].strip()
        logger.info("processing team: " + team_name)
        matchup_table = team_trend.findParent("table")     
        trend_rows = matchup_table.findAll("tr")
        new_trends = list()
        for idx in range(4, len(trend_rows)):
            trend_row = trend_rows[idx]
            data_columns = trend_row.findAll("td")
            
            #instantiate the matchup and set the rigth matchup
            matchupTrend = MatchupTrend()
            matchupTrend.game_matchup = matchup

            matchupTrend.team = team_name
            matchupTrend.description = data_columns[0].string.strip()
            logger.debug("trend description: " + matchupTrend.description)
            matchupTrend.current_win, matchupTrend.current_loss = return_win_loss(data_columns[1])
            matchupTrend.last3_win, matchupTrend.last3_loss = return_win_loss(data_columns[2])
            matchupTrend.since1992_win, matchupTrend.since1992_loss = return_win_loss(data_columns[3])
            matchupTrend.save()
            new_trends.append( matchupTrend )

        matchup.matchup_trends = new_trends
    """
def return_win_loss( data_column ):
    return [stat.strip() for stat in data_column.string.split("-")]
