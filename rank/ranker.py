import math
from bingo.matchups.models import Matchup, MatchupTrend
import logging
logger = logging.getLogger(__name__)
from decimal import *
class Ranker():

    def rank(self, *args):
        getcontext().prec = 2
        game_filter = None
        if len(args) > 0 and len(args[0]) > 0:
            game_filter = args[0][0]
        matchups = None
        if game_filter:
            matchups = Matchup.objects.filter(game_id__contains=game_filter)
        else:
            matchups = Matchup.objects.all()
        for matchup in matchups:
            matchup_trends = matchup.matchup_trends.all()
            team_scores = dict()
            for trend in matchup_trends:
                if trend.team not in team_scores:
                    team_scores[trend.team] = 0 
                team_scores[trend.team] = team_scores[trend.team] + self.boost_from_trend(trend)
            team_one, team_two = team_scores.keys() 
            final_rank = Decimal( math.fabs(team_scores[team_one] - team_scores[team_two]) )
            logger.info("team scores are: " + str(team_scores))
            logger.info("final rank is: " + str(final_rank))
            matchup.rank = final_rank
            matchup.save()
                
    def boost_from_trend(self, trend):
        if trend.description.find("in road games") > -1:
            return self.rank_road_games(trend)
        if trend.description.find("in home games") > -1:
            return self.rank_home_games(trend)
        if trend.description.find("in all games") > -1:
            return self.rank_all_games(trend)
        return 0

    def rank_road_games(self,trend):
        current_ratio = trend.current_win / float( trend.current_win + trend.current_loss)
        last3_ratio = ( trend.last3_win / float(trend.last3_win + trend.last3_loss) ) * .9
        road_score = (current_ratio * .5) + last3_ratio
        logger.info(trend.team + ":score for ROAD game is: " + str(road_score))
        return road_score

    def rank_home_games(self, trend):
        current_ratio = trend.current_win / float( trend.current_win + trend.current_loss + 1 )
        last3_ratio = ( trend.last3_win / float(trend.last3_win + trend.last3_loss) ) * .9
        home_score = (current_ratio * .5) + last3_ratio
        logger.info(trend.team + ": score for HOME game is: " + str(home_score))
        return home_score

    def rank_all_games(self, trend):
        current_ratio = trend.current_win / float( trend.current_win + trend.current_loss)
        last3_ratio = trend.last3_win / float(trend.last3_win + trend.last3_loss)
        all_games_score = (current_ratio * .5) + last3_ratio
        logger.info(trend.team + ":score for ALL GAMES game is: " + str(all_games_score))
        return all_games_score * .9
