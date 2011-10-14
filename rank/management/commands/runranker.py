 #!/usr/bin/env python
import settings
import urllib2,re
from django.core.management.base import BaseCommand, CommandError
import logging
from rank import ranker
logger = logging.getLogger(__name__)
class Command(BaseCommand):

    args = '<poll_id poll_id ...>'
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        rankerObj = ranker.Ranker()
        rankerObj.rank(args)
        return
