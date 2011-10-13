# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Team'
        db.create_table('teams', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=1024)),
        ))
        db.send_create_signal('sheetparser', ['Team'])

        # Adding model 'Matchup'
        db.create_table('matchups', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('game_id', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('sheetparser', ['Matchup'])

        # Adding model 'MatchupTrend'
        db.create_table('matchup_trends', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('team', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('matchup_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sheetparser.Matchup'])),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('current_win', self.gf('django.db.models.fields.IntegerField')(max_length=5)),
            ('current_loss', self.gf('django.db.models.fields.IntegerField')(max_length=5)),
            ('last3_win', self.gf('django.db.models.fields.IntegerField')(max_length=5)),
            ('last3_loss', self.gf('django.db.models.fields.IntegerField')(max_length=5)),
            ('since1992_win', self.gf('django.db.models.fields.IntegerField')(max_length=5)),
            ('since1992_loss', self.gf('django.db.models.fields.IntegerField')(max_length=5)),
        ))
        db.send_create_signal('sheetparser', ['MatchupTrend'])


    def backwards(self, orm):
        
        # Deleting model 'Team'
        db.delete_table('teams')

        # Deleting model 'Matchup'
        db.delete_table('matchups')

        # Deleting model 'MatchupTrend'
        db.delete_table('matchup_trends')


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
            'matchup_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sheetparser.Matchup']"}),
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
