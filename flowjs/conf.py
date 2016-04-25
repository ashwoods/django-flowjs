from django.conf import settings  # noqa

from appconf import AppConf


class FlowjsStorageConf(AppConf):
    # Media path where the files are saved
    PATH = 'flowjs/'

    # Remove the upload files when the model is deleted
    REMOVE_FILES_ON_DELETE = True

    # Remove temporary chunks after file have been upload and created
    AUTO_DELETE_CHUNKS = True

    # Time in days to remove non completed uploads
    EXPIRATION_DAYS = 1

    # When flowjs should join files in background. Options: 'none', 'media' (audio and video), 'all' (all files).
    JOIN_CHUNKS_IN_BACKGROUND = 'none'

    # Check if FLOWJS should use Celery
    WITH_CELERY = 'celery' in settings.INSTALLED_APPS

    # always send signals e.g. even with foreground processing
    ALWAYS_SEND_SIGNALS = False
















