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


def drange(start, stop, step):
    r = start
    while r < stop:
        yield r
        r += step

class Command(BaseCommand):

    args = '<poll_id poll_id ...>'
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):


        for i in drange(.5,1.5,0.1):
            matchups = Matchup.objects.filter(rank__gt=i,current_line__lte=-22,  home_win_ats__isnull=False, season__gte=2010) 
            games = len(matchups)
            wins = 0
            for matchup in matchups:

               wins = wins + calc_wins( matchup )
            print "%f :: wins: %d games: %d and perc win %f " % (i, wins, games, float(wins)/float(games) )
def calc_wins(matchup):
    if matchup.home_win_ats == "push":
        return 1
    if matchup.home_win_ats == "win" and matchup.team_advantage == matchup.home_team:
        return 1
    if matchup.away_win_ats == "loss" and matchup.team_advantage == matchup.away_team:
        return 1
    return 0
