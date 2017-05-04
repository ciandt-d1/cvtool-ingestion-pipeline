import logging
import os

import cvtool_images_client
from cvtool_images_client.rest import ApiException
from cvtool_images_client import Annotation, ImageRequest

# create an instance of the API class
cvtool_images_client.configuration.host = os.environ['IMAGES_API_HOST']
cvtool_images_client.configuration.debug = os.environ.get('DEBUG', None) is not None
api_instance = cvtool_images_client.ImageApi()


def new_image(tenant_id, project_id, job_id, original_uri):
    new_image_request = ImageRequest(job_id=job_id, original_uri=original_uri)
    try:
        api_response = api_instance.add(tenant_id, project_id, new_image_request)
        return api_response
    except ApiException as e:
        logging.error("Exception when calling JobApi->create: %s\n" % e)


def annotation_from_row(headers, row):
    split_headers = headers.split(',')
    columns = row.split(',')
    return Annotation()
