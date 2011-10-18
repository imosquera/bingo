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
        for matchup in matchups[0:1]:
            compute_trends( matchup, "all" )

def compute_trends(matchup, trend_type):
    current_season = 2011
    trend_description = "in %s games" % trend_type
    #first compute score for this season
    logger.info('computing trends for: %s' % matchup.home_team.name)
    previous_matchups = Matchup.objects.filter( Q(home_team=matchup.home_team)|Q(away_team=matchup.home_team) , gametime__lt=matchup.gametime, season = current_season)
    wins = losses = 0

    for previous_matchup in previous_matchups:
        status =  calculate_wins(previous_matchup, matchup.home_team)
        if status == WIN:
            wins = wins + 1
        if status == LOSS:
            losses = losses + 1

    matchupTrend = MatchupTrend()
    matchupTrend.team = matchup.home_team
    matchupTrend.description = trend_description
    matchupTrend.current_win = wins
    matchupTrend.current_loss = losses
    matchupTrend.game_matchup = matchup
    matchupTrend.save()
    #print matchupTrend.id
    print "wins %d loss %d" % (wins,losses)

def calculate_wins( previous_matchup, team ):
    
    normalized_home_score = previous_matchup.home_score + previous_matchup.current_line
    home_team_won = False
    if normalized_home_score == previous_matchup.away_score:
        return PUSH

    if normalized_home_score >  previous_matchup.away_score:
        home_team_won = True

    if (previous_matchup.home_team == team and home_team_won):
        return WIN

    if (previous_matchup.away_team == team and not home_team_won):
        return WIN

    #otherwise the team lost and return a loss
    return LOSS
