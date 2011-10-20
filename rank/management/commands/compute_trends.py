 #!/usr/bin/env python
import settings
import urllib2,re
from django.core.management.base import BaseCommand, CommandError
import logging
from django.db.models import Q
from rank import ranker
from matchups.models import Matchup, MatchupTrend
logger = logging.getLogger(__name__)

WIN = 1
LOSS = -1
PUSH = 0

class Command(BaseCommand):

    args = '<poll_id poll_id ...>'
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        matchups = Matchup.objects.all() 
        for matchup in matchups:
            matchup.matchup_trends.all().delete()
            compute_trends( matchup, "all" )
            compute_trends( matchup, "home" )
            compute_trends( matchup, "away" )

def compute_trends(matchup, trend_type):
    trend_description = "in %s games" % trend_type
    #first compute score for this season
    for team in (matchup.home_team, matchup.away_team):
        calculate_trends_for_team(matchup, team, trend_type)

def calculate_trends_for_team(matchup, team, trend_type):
    if matchup.home_team == team and trend_type == "away":
        return

    if matchup.away_team == team and trend_type == "home":
        return

    logger.info('computing trends for: %s %s' % (team.name, str(matchup.id)))
    trend_description = "in %s games" % trend_type
    matchupTrend = MatchupTrend()
    matchupTrend.team =team
    matchupTrend.description = trend_description
    matchupTrend.current_win, matchupTrend.current_loss = calculate_win_loss_for(matchup,team, trend_type,0)
    matchupTrend.last3_win, matchupTrend.last3_loss = calculate_win_loss_for(matchup, team,trend_type,3)
    matchupTrend.game_matchup = matchup
    matchupTrend.save()

def calculate_win_loss_for(matchup, team, trend_type, length):

    seasons_back = matchup.season - length
    previous_matchups = None
    if trend_type == "all":
        previous_matchups = Matchup.objects.filter( Q(home_team=team)|Q(away_team=team) , gametime__lt=matchup.gametime, season__gte=seasons_back)
    if trend_type == "home":
        previous_matchups = Matchup.objects.filter( home_team=team , gametime__lt=matchup.gametime, season__gte=seasons_back)
    if trend_type == "away":
        previous_matchups = Matchup.objects.filter( away_team=team , gametime__lt=matchup.gametime, season__gte=seasons_back)
 
    wins = losses = 0
        
    logger.info("past games for: " + team.name + " is: " + str(len(previous_matchups)))
    for previous_matchup in previous_matchups:
        status =  calculate_wins(previous_matchup,team)
        if status == WIN:
            wins = wins + 1
        if status == LOSS:
            losses = losses + 1
    return (wins, losses) 

def calculate_wins( previous_matchup, team ):
    
    home_team_won = False
    if previous_matchup.home_win_ats == "push":
        return PUSH

    if previous_matchup.home_win_ats == "win":
        home_team_won = True

    if (previous_matchup.home_team == team and home_team_won):
        return WIN

    if (previous_matchup.away_team == team and not home_team_won):
        return WIN

    #otherwise the team lost and return a loss
    return LOSS
