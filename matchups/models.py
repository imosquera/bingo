from django.db import models
# Create your models here.


class Team(models.Model):
    class Meta:
        db_table = "teams"
    
    name = models.CharField(max_length=1024)

class Matchup(models.Model):
    class Meta:
        db_table = "matchups"
    game_id = models.CharField(max_length=40, primary_key=True)
    url = models.CharField(max_length=1024)
    current_line = models.IntegerField(max_length=4,null=True, blank=True)
    starting_line = models.IntegerField(max_length=4,null=True, blank=True)
    home_score = models.IntegerField(max_length=4, null=True, blank=True)
    away_score = models.IntegerField(max_length=4, null=True, blank=True)
    rank = models.DecimalField(max_digits=10, decimal_places=2, null=True,blank=True)
    """
    we can add this in later
    home_team = models.CharField(max_length=50)
    away_team = models.CharField(max_length=50)
    """

class MatchupTrend(models.Model):
    class Meta:
        db_table = "matchup_trends"
    team = models.CharField(max_length=1024)
    game_matchup = models.ForeignKey('Matchup', related_name='matchup_trends')
    description = models.CharField(max_length=1024)
    current_win = models.IntegerField(max_length=5)
    current_loss =  models.IntegerField(max_length=5) 
    last3_win = models.IntegerField(max_length=5) 
    last3_loss = models.IntegerField(max_length=5) 
    since1992_win = models.IntegerField(max_length=5)   
    since1992_loss = models.IntegerField(max_length=5)  
