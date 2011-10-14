# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Matchup.current_line'
        db.add_column('matchups', 'current_line', self.gf('django.db.models.fields.IntegerField')(max_length=4, null=True, blank=True), keep_default=False)

        # Adding field 'Matchup.starting_line'
        db.add_column('matchups', 'starting_line', self.gf('django.db.models.fields.IntegerField')(max_length=4, null=True, blank=True), keep_default=False)

        # Adding field 'Matchup.home_score'
        db.add_column('matchups', 'home_score', self.gf('django.db.models.fields.IntegerField')(max_length=4, null=True, blank=True), keep_default=False)

        # Adding field 'Matchup.away_score'
        db.add_column('matchups', 'away_score', self.gf('django.db.models.fields.IntegerField')(max_length=4, null=True, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Matchup.current_line'
        db.delete_column('matchups', 'current_line')

        # Deleting field 'Matchup.starting_line'
        db.delete_column('matchups', 'starting_line')

        # Deleting field 'Matchup.home_score'
        db.delete_column('matchups', 'home_score')

        # Deleting field 'Matchup.away_score'
        db.delete_column('matchups', 'away_score')


    models = {
        'sheetparser.matchup': {
            'Meta': {'object_name': 'Matchup', 'db_table': "'matchups'"},
            'away_score': ('django.db.models.fields.IntegerField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'current_line': ('django.db.models.fields.IntegerField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'game_id': ('django.db.models.fields.CharField', [], {'max_length': '40', 'primary_key': 'True'}),
            'home_score': ('django.db.models.fields.IntegerField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'starting_line': ('django.db.models.fields.IntegerField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '1024'})
        },
        'sheetparser.matchuptrend': {
            'Meta': {'object_name': 'MatchupTrend', 'db_table': "'matchup_trends'"},
            'current_loss': ('django.db.models.fields.IntegerField', [], {'max_length': '5'}),
            'current_win': ('django.db.models.fields.IntegerField', [], {'max_length': '5'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'game_matchup': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'matchup_trends'", 'to': "orm['sheetparser.Matchup']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last3_loss': ('django.db.models.fields.IntegerField', [], {'max_length': '5'}),
            'last3_win': ('django.db.models.fields.IntegerField', [], {'max_length': '5'}),
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
