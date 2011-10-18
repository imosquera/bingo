# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'Team.id'
        db.delete_column('teams', 'id')

        # Changing field 'Team.insider_name'
        db.alter_column('teams', 'insider_name', self.gf('django.db.models.fields.CharField')(max_length=200, primary_key=True))

        # Adding unique constraint on 'Team', fields ['insider_name']
        db.create_unique('teams', ['insider_name'])

        # Changing field 'Team.statfox_name'
        db.alter_column('teams', 'statfox_name', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True))


    def backwards(self, orm):
        
        # Adding field 'Team.id'
        db.add_column('teams', 'id', self.gf('django.db.models.fields.AutoField')(default=None, primary_key=True), keep_default=False)

        # Changing field 'Team.insider_name'
        db.alter_column('teams', 'insider_name', self.gf('django.db.models.fields.CharField')(max_length=1024))

        # Removing unique constraint on 'Team', fields ['insider_name']
        db.delete_unique('teams', ['insider_name'])

        # Changing field 'Team.statfox_name'
        db.alter_column('teams', 'statfox_name', self.gf('django.db.models.fields.CharField')(max_length=1024, null=True, blank=True))


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
            'insider_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'primary_key': 'True'}),
            'statfox_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['matchups']
