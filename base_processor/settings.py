import os
import json
import time
import boto3
import logging
import logging.config

class Settings(object):
    def __init__(self):
        '''
        The Settings class enables processors to initiate settings
        within the scope of the processor itself. This is a beneficial approach
        since our settings load values dynamically from AWS SSM. By avoiding the
        singleton pattern of a flat settings module, we are able to effectively
        test settings in local development with mock SSM per test.
        '''

        self.job_id            = os.environ.get('IMPORT_ID')
        self.environment       = os.environ.get('ENVIRONMENT')
        self.aws_batch_job_id  = os.environ.get('AWS_BATCH_JOB_ID')
        self.aws_region_name   = os.environ.get('AWS_REGION_NAME', 'us-east-1')
        self.scratch_dir       = os.environ.get('SCRATCH_DIR', '/docker_scratch')
        self.encryption_key_id = os.environ.get('ENCRYPTION_KEY_ID')
        self.storage_directory = os.environ.get('STORAGE_DIRECTORY')

        # get inputs from JSON file (useful for testing)
        self.input_file       = os.environ.get('INPUT_FILE', None)

        # optional endpoints for local testing
        self.s3_endpoint      = os.environ.get('S3_ENDPOINT', None)
        self.ssm_endpoint     = os.environ.get('SSM_ENDPOINT', None)

        self.local_directory  = '{dir}/{base}'.format(
            dir   = self.scratch_dir,
            base  = self.aws_batch_job_id)

        # load
        env = self.environment
        self._load_values(
            storage_bucket = "{env}-etl-storage-bucket".format(env=env),
            upload_bucket  = "{env}-etl-upload-bucket".format(env=env)
        )

    def _load_values(self, **keys):
        '''
        Load values from SSM for all keys. Keys should be in the
        format key=ssm_variable. This method injects the value of
        each key into class variables, such that self.key = <ssm-value>

        For example, if:

        keys = {
            'key1': 'ssm-field1',
            'key2:  'ssm-field2'
        }

        It results in:

        self.key1 = ssm-field1-value
        self.key2 = ssm-field2-value

        '''
        ssm_client = boto3.client('ssm', region_name=self.aws_region_name, endpoint_url=self.ssm_endpoint)
        response = ssm_client.get_parameters(
            Names=keys.values(),
            WithDecryption=True
        )

        if len(response['InvalidParameters']) > 0:
            raise Exception('Invalid SSM parameters: {}'.format(response['InvalidParameters']))

        for i, resp in enumerate(response['Parameters']):
            var = keys.keys()[keys.values().index(resp['Name'])]
            value = resp['Value']
            if str(var) in self.__dict__:
                raise Exception('Settings variable already exists: {}'.format(var))
            self.__dict__[var] = value


class UTCFormatter(logging.Formatter):
    '''Convert logging timestamp to UTC'''
    converter = time.gmtime

class Logging(object):
    def __init__(self, *args, **kwargs):
        '''Configure logging format'''

        log_level        = os.environ.get('LOG_LEVEL', 'INFO')
        log_level_sentry = os.environ.get('LOG_LEVEL_SENTRY', 'ERROR')
        sentry_address   = os.environ.get('SENTRY_ADDRESS', '')

        LOGGING = {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'utc': {
                    '()': UTCFormatter,
                    'format': '[%(levelname)s] [%(module)s] - %(message)s',
                    'datefmt': '%Y-%m-%dT%H:%M:%OS'
                }
            },
            'handlers': {
                'blackfynn': {
                    'class': 'logging.StreamHandler',
                    'formatter': 'utc',
                }
            },
            'root': {
                'handlers': ['blackfynn'],
                'level': log_level,
           }
        }

        logging.config.dictConfig(LOGGING)
        self.logger = logging.getLogger()
