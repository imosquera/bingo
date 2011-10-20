# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Matchup.over_under_line'
        db.add_column('matchups', 'over_under_line', self.gf('django.db.models.fields.FloatField')(max_length=4, null=True, blank=True), keep_default=False)

        # Adding field 'Matchup.home_win_ats'
        db.add_column('matchups', 'home_win_ats', self.gf('django.db.models.fields.CharField')(max_length=8, null=True), keep_default=False)

        # Adding field 'Matchup.away_win_ats'
        db.add_column('matchups', 'away_win_ats', self.gf('django.db.models.fields.CharField')(max_length=8, null=True), keep_default=False)

        # Changing field 'Matchup.over_under'
        db.alter_column('matchups', 'over_under', self.gf('django.db.models.fields.CharField')(max_length=8, null=True))


    def backwards(self, orm):
        
        # Deleting field 'Matchup.over_under_line'
        db.delete_column('matchups', 'over_under_line')

        # Deleting field 'Matchup.home_win_ats'
        db.delete_column('matchups', 'home_win_ats')

        # Deleting field 'Matchup.away_win_ats'
        db.delete_column('matchups', 'away_win_ats')

        # Changing field 'Matchup.over_under'
        db.alter_column('matchups', 'over_under', self.gf('django.db.models.fields.FloatField')(max_length=4, null=True, blank=True))


    models = {
        'matchups.matchup': {
            'Meta': {'object_name': 'Matchup', 'db_table': "'matchups'"},
            'away_score': ('django.db.models.fields.IntegerField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'away_team': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'away_matchups'", 'to': "orm['matchups.Team']"}),
            'away_win_ats': ('django.db.models.fields.CharField', [], {'max_length': '8', 'null': 'True'}),
            'current_line': ('django.db.models.fields.FloatField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'filepath': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True'}),
            'gametime': ('django.db.models.fields.DateTimeField', [], {}),
            'home_score': ('django.db.models.fields.IntegerField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'home_team': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'home_matchups'", 'to': "orm['matchups.Team']"}),
            'home_win_ats': ('django.db.models.fields.CharField', [], {'max_length': '8', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'insider_game_id': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'insider_matchup_path': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True'}),
            'over_under': ('django.db.models.fields.CharField', [], {'max_length': '8', 'null': 'True'}),
            'over_under_line': ('django.db.models.fields.FloatField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'rank': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'season': ('django.db.models.fields.IntegerField', [], {'max_length': '6'}),
            'starting_line': ('django.db.models.fields.FloatField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True'})
        },
        'matchups.matchuptrend': {
            'Meta': {'object_name': 'MatchupTrend', 'db_table': "'matchup_trends'"},
            'current_loss': ('django.db.models.fields.IntegerField', [], {'max_length': '5'}),
            'current_win': ('django.db.models.fields.IntegerField', [], {'max_length': '5'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'game_matchup': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'matchup_trends'", 'to': "orm['matchups.Matchup']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last3_loss': ('django.db.models.fields.IntegerField', [], {'max_length': '5'}),
            'last3_win': ('django.db.models.fields.IntegerField', [], {'max_length': '5'}),
            'since1992_loss': ('django.db.models.fields.IntegerField', [], {'max_length': '5'}),
            'since1992_win': ('django.db.models.fields.IntegerField', [], {'max_length': '5'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'team_trends'", 'to': "orm['matchups.Team']"})
        },
        'matchups.team': {
            'Meta': {'object_name': 'Team', 'db_table': "'teams'"},
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'primary_key': 'True'}),
            'statfox_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['matchups']
