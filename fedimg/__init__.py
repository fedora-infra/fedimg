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

# AMAZON WEB SERVICES (EC2)
AWS_ACCESS_ID = config.get('aws', 'access_id')
AWS_SECRET_KEY = config.get('aws', 'secret_key')
AWS_AMIS = config.get('aws', 'amis')
AWS_IAM_PROFILE = config.get('aws', 'iam_profile')
