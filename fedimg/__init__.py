import ConfigParser

config = ConfigParser.RawConfigParser()
config.read('fedimg.cfg')

# koji_server is the location of the Koji hub that should be used
# to initialize the Koji connection.
KOJI_SERVER = config.get('koji', 'server')

# The two slashes ("//") in the following URL are NOT a mistake.
BASE_KOJI_TASK_URL = config.get('koji', 'base_task_url')

LOCAL_DOWNLOAD_DIR = config.get('general', 'local_download_dir')

DOWNLOAD_PROGRESS = config.get('general', 'download_progress')
