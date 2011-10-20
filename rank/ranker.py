import math, os
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
            matchups = Matchup.objects.filter(insider_game_id__contains=game_filter)
        else:
            matchups = Matchup.objects.all()
        for matchup in matchups:
            matchup_trends = matchup.matchup_trends.all()
            final_rank = 0
            try:
                team_scores = dict()

                for trend in matchup_trends:
                    if trend.team not in team_scores:
                        team_scores[trend.team] = 0 
                    boost = self.boost_from_trend(trend)
                    team_scores[trend.team] = team_scores[trend.team] + boost

                team_one, team_two = team_scores.keys() 
                    

                final_rank = 0
                if team_scores[matchup.home_team] > team_scores[matchup.away_team]:
                    matchup.team_advantage = matchup.home_team
                else:
                    matchup.team_advantage = matchup.away_team

                if matchup.current_line <= -22:
                    team_scores[matchup.home_team] += .8
 
                final_rank = Decimal( math.fabs(team_scores[team_one] - team_scores[team_two]) )

                if team_scores[team_one] == 0 or team_scores[team_two] == 0:
                    final_rank = 0
                logger.info("team scores are: %s:%f %s:%f " % ( matchup.home_team.name, team_scores[matchup.home_team], matchup.away_team.name, team_scores[matchup.away_team])  )
            except:
                logging.exception("couldnt calc for game id:" + str(matchup.id))

            matchup.rank = final_rank
            matchup.save()
            logger.info("final rank is: " + str(matchup.rank) + " for game id: " + str(matchup.id))
    def boost_from_trend(self, trend):
        if trend.description.find("in away games") > -1:
            return self.rank_road_games(trend)
        if trend.description.find("in home games") > -1:
            return self.rank_home_games(trend)
        if trend.description.find("in all games") > -1:
            return self.rank_all_games(trend)
        return 0

    def rank_road_games(self,trend):
        current_ratio = last3_ratio = 0
        modifier = 0
        if trend.last3_win + trend.last3_loss < 3:
            modifier = -0.3
        if trend.current_win + trend.current_loss < 3:
            modifer = modifier + -0.3
        current_ratio = trend.current_win / float( trend.current_win + trend.current_loss) * .9
        last3_ratio = ( trend.last3_win / float(trend.last3_win + trend.last3_loss) )  
        away_score = (current_ratio * .2) + last3_ratio + modifier
        logger.info(trend.team.name + ": score for AWAY game is: " + str(away_score))
        return away_score * .9
 
    def rank_home_games(self, trend):
        current_ratio = last3_ratio = 0
        modifier = 0
        if trend.last3_win + trend.last3_loss < 3:
            modifier = -0.3
        if trend.current_win + trend.current_loss < 3:
            modifer = modifier + -0.3
        current_ratio = trend.current_win / float( trend.current_win + trend.current_loss)
        last3_ratio = ( trend.last3_win / float(trend.last3_win + trend.last3_loss) )  
        home_score = (current_ratio * .2) + last3_ratio + modifier
        logger.info(trend.team.name + ": score for HOME game is: " + str(home_score))
        return home_score * 1.2

    def rank_all_games(self, trend):
        modifier = 0
        if trend.last3_win + trend.last3_loss < 3:
            modifier = -0.3
        if trend.current_win + trend.current_loss < 3:
            modifier = modifier + -0.3
        current_ratio = trend.current_win / float( trend.current_win + trend.current_loss)
        last3_ratio = trend.last3_win / float(trend.last3_win + trend.last3_loss)
        all_games_score = (current_ratio * .2) + last3_ratio + modifier
        logger.info(trend.team.name + ":score for ALL GAMES game is: " + str(all_games_score))
        return all_games_score 
