import logging

from google.appengine.api import app_identity

import cloudstorage as gcs
from image_ingestion_client import CreateCsvIngestionJobRequest
from images import new_image
from jobs import start_job, end_job
from mapreduce import base_handler, mapreduce_pipeline, context

log = logging.getLogger(__name__)


# https://sookocheff.com/post/appengine/pipelines/fan-in-fan-out/

class CreateCsvIngestionJob(base_handler.PipelineBase):
    def run(self, ingestion_request):
        r = CreateCsvIngestionJobRequest.from_dict(ingestion_request)
        headers, start_position = get_headers(r.csv_uri)
        log.info(start_job(r.tenant_id, r.job_id))

        yield CsvIngestionMapPipeline(headers=headers, start_position=start_position,
                                      ingestion_request=ingestion_request)


def get_headers(filename):
    gcs_file = gcs.open(filename)
    headers = gcs_file.readline()
    start_position = gcs_file.tell()
    gcs_file.close()
    return headers, start_position


def ingest_image_mapper(row):
    ctx = context.get()
    # log.debug('ctx: %s', dir(ctx))
    # log.debug('ctx.counters: %s', ctx.counters)
    # log.debug('ctx.mapreduce_spec: %s', dir(ctx.mapreduce_spec))
    # job_params = ctx.mapreduce_spec.params
    # log.debug('ctx.mapreduce_spec.params: %s', job_params)

    mapper_params = ctx.mapreduce_spec.mapper.params
    log.debug('ctx.mapreduce_spec.mapper.params: %s', mapper_params)

    init_position, line_data = row
    log.info('init: %s, line: %s', init_position, line_data)

    cols = line_data.split(',')

    image_original_uri = cols[0]
    log.debug('image_original_uri: %s', image_original_uri)

    ingestion_request = CreateCsvIngestionJobRequest.from_dict(mapper_params.get('ingestion_request', dict()))
    image = new_image(ingestion_request.tenant_id, ingestion_request.project_id, ingestion_request.job_id,
                      image_original_uri)

    return image


class CsvIngestionMapPipeline(base_handler.PipelineBase):
    def run(self, headers, start_position, ingestion_request):
        yield mapreduce_pipeline.MapPipeline(
            "gcs_csv_reader_job",
            "image_processor.ingest_image_mapper",
            "input_readers.GoogleStorageLineInputReader",

            params={
                "bucket_name": app_identity.get_default_gcs_bucket_name(),
                "headers": headers,
                "ingestion_request": ingestion_request,
                "input_reader": {
                    "start_position": start_position,
                    "file_paths": [
                        ingestion_request.get('csv_uri')
                    ]
                }
            })

    def _get_ingestion_request(self):
        log.debug('kwargs items: %s', self.kwargs.items())
        params = self.kwargs.get('ingestion_request')
        ingestion_request = CreateCsvIngestionJobRequest.from_dict(params)
        return ingestion_request

    def finalized(self):
        ir = self._get_ingestion_request()
        r = end_job(ir.tenant_id, ir.job_id)
        log.info('Finished job ingestion: %s', ir)
