# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Renaming column for 'MatchupTrend.team' to match new field type.
        db.rename_column('matchup_trends', 'team', 'team_id')
        # Changing field 'MatchupTrend.team'
        db.alter_column('matchup_trends', 'team_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['matchups.Team']))

        # Adding index on 'MatchupTrend', fields ['team']
        db.create_index('matchup_trends', ['team_id'])


    def backwards(self, orm):
        
        # Renaming column for 'MatchupTrend.team' to match new field type.
        db.rename_column('matchup_trends', 'team_id', 'team')
        # Changing field 'MatchupTrend.team'
        db.alter_column('matchup_trends', 'team', self.gf('django.db.models.fields.CharField')(max_length=1024))

        # Removing index on 'MatchupTrend', fields ['team']
        db.delete_index('matchup_trends', ['team_id'])


    models = {
        'matchups.matchup': {
            'Meta': {'object_name': 'Matchup', 'db_table': "'matchups'"},
            'away_score': ('django.db.models.fields.IntegerField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'away_team': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'away_matchups'", 'to': "orm['matchups.Team']"}),
            'current_line': ('django.db.models.fields.FloatField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'filepath': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True'}),
            'gametime': ('django.db.models.fields.DateTimeField', [], {}),
            'home_score': ('django.db.models.fields.IntegerField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'home_team': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'home_matchups'", 'to': "orm['matchups.Team']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'insider_game_id': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'insider_matchup_path': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True'}),
            'over_under': ('django.db.models.fields.FloatField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
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
