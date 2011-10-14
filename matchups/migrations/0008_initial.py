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
        db.send_create_signal('matchups', ['Team'])

        # Adding model 'Matchup'
        db.create_table('matchups', (
            ('game_id', self.gf('django.db.models.fields.CharField')(max_length=40, primary_key=True)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('current_line', self.gf('django.db.models.fields.IntegerField')(max_length=4, null=True, blank=True)),
            ('starting_line', self.gf('django.db.models.fields.IntegerField')(max_length=4, null=True, blank=True)),
            ('home_score', self.gf('django.db.models.fields.IntegerField')(max_length=4, null=True, blank=True)),
            ('away_score', self.gf('django.db.models.fields.IntegerField')(max_length=4, null=True, blank=True)),
            ('rank', self.gf('django.db.models.fields.IntegerField')(max_length=4, null=True, blank=True)),
        ))
        db.send_create_signal('matchups', ['Matchup'])

        # Adding model 'MatchupTrend'
        db.create_table('matchup_trends', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('team', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('game_matchup', self.gf('django.db.models.fields.related.ForeignKey')(related_name='matchup_trends', to=orm['matchups.Matchup'])),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('current_win', self.gf('django.db.models.fields.IntegerField')(max_length=5)),
            ('current_loss', self.gf('django.db.models.fields.IntegerField')(max_length=5)),
            ('last3_win', self.gf('django.db.models.fields.IntegerField')(max_length=5)),
            ('last3_loss', self.gf('django.db.models.fields.IntegerField')(max_length=5)),
            ('since1992_win', self.gf('django.db.models.fields.IntegerField')(max_length=5)),
            ('since1992_loss', self.gf('django.db.models.fields.IntegerField')(max_length=5)),
        ))
        db.send_create_signal('matchups', ['MatchupTrend'])


    def backwards(self, orm):
        
        # Deleting model 'Team'
        db.delete_table('teams')

        # Deleting model 'Matchup'
        db.delete_table('matchups')

        # Deleting model 'MatchupTrend'
        db.delete_table('matchup_trends')


    models = {
        'matchups.matchup': {
            'Meta': {'object_name': 'Matchup', 'db_table': "'matchups'"},
            'away_score': ('django.db.models.fields.IntegerField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'current_line': ('django.db.models.fields.IntegerField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'game_id': ('django.db.models.fields.CharField', [], {'max_length': '40', 'primary_key': 'True'}),
            'home_score': ('django.db.models.fields.IntegerField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'rank': ('django.db.models.fields.IntegerField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1024'})
        }
    }

    complete_apps = ['matchups']
