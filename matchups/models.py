from django.db import models
# Create your models here.


class Team(models.Model):
    class Meta:
        db_table = "teams"
    
    statfox_name = models.CharField(max_length=200, null=True, blank=True)
    name = models.CharField(max_length=200, primary_key=True)

class Matchup(models.Model):
    class Meta:
        db_table = "matchups"
    insider_game_id = models.CharField(max_length=100)
    url = models.CharField(max_length=1024, null=True)
    filepath = models.CharField(max_length=1024, null=True)
    insider_matchup_path = models.CharField(max_length=1024, null=True)
    current_line = models.FloatField(max_length=4,null=True, blank=True)
    starting_line = models.FloatField(max_length=4,null=True, blank=True)
    over_under = models.FloatField(max_length=4,null=True, blank=True)
    home_score = models.IntegerField(max_length=4, null=True, blank=True)
    away_score = models.IntegerField(max_length=4, null=True, blank=True)
    home_team = models.ForeignKey('Team', related_name='home_matchups')
    away_team = models.ForeignKey('Team', related_name='away_matchups')
    rank = models.DecimalField(max_digits=10, decimal_places=2, null=True,blank=True)
    gametime = models.DateTimeField()
    season = models.IntegerField(max_length=6)
    """
    we can add this in later
    home_team = models.CharField(max_length=50)
    away_team = models.CharField(max_length=50)
    """

class MatchupTrend(models.Model):
    class Meta:
        db_table = "matchup_trends"
    team = models.ForeignKey('Team', related_name='team_trends')
    game_matchup = models.ForeignKey('Matchup', related_name='matchup_trends')
    description = models.CharField(max_length=1024)
    current_win = models.IntegerField(max_length=5)
    current_loss =  models.IntegerField(max_length=5) 
    last3_win = models.IntegerField(max_length=5) 
    last3_loss = models.IntegerField(max_length=5) 
    since1992_win = models.IntegerField(max_length=5)   
    since1992_loss = models.IntegerField(max_length=5)  
