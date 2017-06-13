import logging
import os
from auth import generate_jwt

import cvtool_cli_client
from cvtool_cli_client.rest import ApiException
from cvtool_cli_client import ImageRequest, Annotations

# create an instance of the API class
cvtool_cli_client.configuration.host = os.environ['IMAGES_API_HOST']
cvtool_cli_client.configuration.debug = os.environ.get('DEBUG', None) is not None
api_instance = cvtool_cli_client.ImageApi()


def new_image(tenant_id, job_id, original_uri, exif_annotations):
    new_image_request = ImageRequest(job_id=job_id, original_uri=original_uri,
                                     exif_annotations=_exif_annotations(exif_annotations))
    try:
        cvtool_cli_client.configuration.access_token = generate_jwt()
        api_response = api_instance.add(tenant_id, new_image_request, _request_timeout=60)
        return api_response
    except ApiException as e:
        if e.status == 400:
            logging.info(e.body)
        else:
            logging.error("Exception when calling JobApi->create: %s\n" % e)


def annotation_from_row(headers, row):
    split_headers = headers.split(',')
    columns = row.split(',')
    return Annotations()


def _exif_annotations(exif_dict):

    def to_str(s):
        return unicode(s).encode('ascii', errors='backslashreplace')

    return {to_str(k): to_str(v) for k, v in exif_dict.iteritems()} if exif_dict else None
