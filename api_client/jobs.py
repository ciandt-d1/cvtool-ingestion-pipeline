import logging
import os

import cvtool_cli_client
from auth import generate_jwt
from cvtool_cli_client.rest import ApiException

# create an instance of the API class
cvtool_cli_client.configuration.host = os.environ['JOBS_API_HOST']
cvtool_cli_client.configuration.debug = os.environ.get('DEBUG', None) is not None
api_instance = cvtool_cli_client.JobApi()


def new_job(tenant_id):
    new_job_request = cvtool_cli_client.Job()
    try:
        cvtool_cli_client.configuration.access_token = generate_jwt()
        api_response = api_instance.create(tenant_id, new_job_request)
        return api_response
    except ApiException as e:
        logging.error("Exception when calling JobApi->create: %s\n" % e)


def start_job(tenant_id, job_id):
    try:
        cvtool_cli_client.configuration.access_token = generate_jwt()
        return api_instance.start_job(tenant_id, job_id)
    except ApiException as e:
        logging.error("Exception when calling JobApi->start_job: %s\n" % e)


def end_job(tenant_id, job_id):
    try:
        cvtool_cli_client.configuration.access_token = generate_jwt()
        return api_instance.end_job(tenant_id, job_id)
    except ApiException as e:
        logging.error("Exception when calling JobApi->end_job: %s\n" % e)

