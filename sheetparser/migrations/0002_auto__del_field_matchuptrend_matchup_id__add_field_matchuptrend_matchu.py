# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'MatchupTrend.matchup_id'
        db.delete_column('matchup_trends', 'matchup_id_id')

        # Adding field 'MatchupTrend.matchup'
        db.add_column('matchup_trends', 'matchup', self.gf('django.db.models.fields.related.ForeignKey')(default=2, to=orm['sheetparser.Matchup']), keep_default=False)


    def backwards(self, orm):
        
        # Adding field 'MatchupTrend.matchup_id'
        db.add_column('matchup_trends', 'matchup_id', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['sheetparser.Matchup']), keep_default=False)

        # Deleting field 'MatchupTrend.matchup'
        db.delete_column('matchup_trends', 'matchup_id')


    models = {
        'sheetparser.matchup': {
            'Meta': {'object_name': 'Matchup', 'db_table': "'matchups'"},
            'game_id': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'sheetparser.matchuptrend': {
            'Meta': {'object_name': 'MatchupTrend', 'db_table': "'matchup_trends'"},
            'current_loss': ('django.db.models.fields.IntegerField', [], {'max_length': '5'}),
            'current_win': ('django.db.models.fields.IntegerField', [], {'max_length': '5'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last3_loss': ('django.db.models.fields.IntegerField', [], {'max_length': '5'}),
            'last3_win': ('django.db.models.fields.IntegerField', [], {'max_length': '5'}),
            'matchup': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sheetparser.Matchup']"}),
            'since1992_loss': ('django.db.models.fields.IntegerField', [], {'max_length': '5'}),
            'since1992_win': ('django.db.models.fields.IntegerField', [], {'max_length': '5'}),
            'team': ('django.db.models.fields.CharField', [], {'max_length': '1024'})
        },
        'sheetparser.team': {
            'Meta': {'object_name': 'Team', 'db_table': "'teams'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1024'})
        }
    }

    complete_apps = ['sheetparser']
