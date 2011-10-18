#!/usr/bin/env python
import settings
import urllib2,re
from BeautifulSoup import BeautifulSoup
from django.core.management.base import BaseCommand, CommandError
from bingo.matchups.models import Matchup, MatchupTrend
import logging
logger = logging.getLogger(__name__)
class Command(BaseCommand):

    args = '<poll_id poll_id ...>'
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        """
        all_reports_url = "http://statfox.nypost.com/matchups/default.aspx?page=cfb/daily"
        all_reports_html = urllib2.urlopen(all_reports_url).read()
        """
        all_reports_html = open("/tmp/reports.html", "r").read()
        all_reports_soup = BeautifulSoup(all_reports_html)
        all_report_hrefs = all_reports_soup.findAll(href=re.compile("gameid=(.*)&"))
        all_hrefs = ["http://statfox.nypost.com/" + report_href['href'] for report_href in all_report_hrefs]
        for href in all_hrefs:
            parse_sheet(href)
        return

def parse_sheet(url):
    sheet_page_html = urllib2.urlopen(url).read()
    soup = BeautifulSoup(sheet_page_html)

    gameid_re = re.compile("gameid=(.*?)&")
    gameid_str = soup.find("form", action=gameid_re)['action']
    gameid = gameid_re.search(gameid_str).group(1)
    matchup = Matchup()
    matchup.game_id = gameid
    matchup.save()

    all_matchup_trends = matchup.matchup_trends.all().delete()
    #gameid_form = soup.find("form", action=re.compile("gameid=(.*?)&"))
    team_trends = soup.findAll(text=re.compile('.*Recent ATS Trends.*'))
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

def return_win_loss( data_column ):
    return [stat.strip() for stat in data_column.string.split("-")]
