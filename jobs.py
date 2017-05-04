import logging
import os

import cvtool_jobs_client
from cvtool_jobs_client.rest import ApiException

# create an instance of the API class
cvtool_jobs_client.configuration.host = os.environ['JOBS_API_HOST']
cvtool_jobs_client.configuration.debug = os.environ.get('DEBUG', None) is not None
api_instance = cvtool_jobs_client.JobApi()


def new_job(tenant_id, project_id):
    new_job_request = cvtool_jobs_client.Job()
    try: 
        api_response = api_instance.create(tenant_id, project_id, new_job_request)
        return api_response
    except ApiException as e:
        logging.error("Exception when calling JobApi->create: %s\n" % e)
    

def start_job(tenant_id, job_id):
    try:
        return api_instance.start_job(tenant_id, job_id)
    except ApiException as e:
        logging.error("Exception when calling JobApi->start_job: %s\n" % e)


def end_job(tenant_id, job_id):
    try:
        return api_instance.end_job(tenant_id, job_id)
    except ApiException as e:
        logging.error("Exception when calling JobApi->end_job: %s\n" % e)

