from django.core.management.base import BaseCommand
from django.conf import settings

from media_library.torrents.models import Tracker, Torrent
from media_library.torrents import enums
from media_library import enums as core_enums

from optparse import make_option
import logging
import os

logger = logging.getLogger('media_library.torrents.management.commands.import_torrents')


class Command(BaseCommand):
    help = 'Inspects the given tracker\'s torrent directory for unregistered torrents'
    args = '[tracker]'

    def handle(self, *args, **options):
        (tracker_slug,) = args
        try:
            tracker = Tracker.objects.get(slug=tracker_slug)
        except Tracker.DoesNotExist, exc:
            logger.error(exc)
            return 0
        else:
            imported = 0
            for element in os.listdir(tracker.torrent_directory):
               try:
                   torrent_path = os.path.join( tracker.torrent_directory, element )
                   torrent = Torrent.objects.get(path=torrent_path)
               except Torrent.DoesNotExist:
                   torrent = Torrent()
                   torrent.type = core_enums.MEDIA_OBJECT_TORRENT
                   torrent.tracker = tracker
                   torrent.path = torrent_path
                   torrent.save()

                   imported += 1
                   logger.info( "Added torrent %s" % (torrent.path) )
            return imported
        return 0
