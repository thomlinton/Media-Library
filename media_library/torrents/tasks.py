from django.core.management import call_command
from celery.task import Task


class ImportTorrentsTask(Task):
    name = 'media_library.torrents.import'
    max_retries = 0

    def run(self, *args, **kwargs):
        logger = self.get_logger(**kwargs)
        call_command('import_torrents', *args, **kwargs)
        return True
