# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'Team.name'
        db.delete_column('teams', 'name')

        # Adding field 'Team.statfox_name'
        db.add_column('teams', 'statfox_name', self.gf('django.db.models.fields.CharField')(default=None, max_length=1024), keep_default=False)

        # Adding field 'Team.insider_name'
        db.add_column('teams', 'insider_name', self.gf('django.db.models.fields.CharField')(default=None, max_length=1024), keep_default=False)


    def backwards(self, orm):
        
        # Adding field 'Team.name'
        db.add_column('teams', 'name', self.gf('django.db.models.fields.CharField')(default=None, max_length=1024), keep_default=False)

        # Deleting field 'Team.statfox_name'
        db.delete_column('teams', 'statfox_name')

        # Deleting field 'Team.insider_name'
        db.delete_column('teams', 'insider_name')


    models = {
        'matchups.matchup': {
            'Meta': {'object_name': 'Matchup', 'db_table': "'matchups'"},
            'away_score': ('django.db.models.fields.IntegerField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'current_line': ('django.db.models.fields.IntegerField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'game_id': ('django.db.models.fields.CharField', [], {'max_length': '40', 'primary_key': 'True'}),
            'home_score': ('django.db.models.fields.IntegerField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'rank': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'starting_line': ('django.db.models.fields.IntegerField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '1024'})
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
            'team': ('django.db.models.fields.CharField', [], {'max_length': '1024'})
        },
        'matchups.team': {
            'Meta': {'object_name': 'Team', 'db_table': "'teams'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'insider_name': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'statfox_name': ('django.db.models.fields.CharField', [], {'max_length': '1024'})
        }
    }

    complete_apps = ['matchups']
