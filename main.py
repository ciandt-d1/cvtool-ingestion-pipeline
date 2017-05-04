import logging

from flask import Flask, redirect, request, jsonify
from image_ingestion_client import CreateCsvIngestionJobRequest
from image_processor import CreateCsvIngestionJob
from mapreduce import mapreduce_pipeline

app = Flask(__name__)


@app.route('/jobs', methods=['POST'])
def trigger_csv_ingestion():
    json = request.get_json(force=True)
    ingestion_request = CreateCsvIngestionJobRequest.from_dict(json)
    pipeline = CreateCsvIngestionJob(ingestion_request=ingestion_request.to_dict())
    pipeline.start()
    return jsonify(
        ingestion_request=json,
        pipeline_id=pipeline.pipeline_id,
        pipeline_results_uri="%s/status?root=%s" % (pipeline.base_path, pipeline.pipeline_id)
    )


@app.route('/start')
def start():
    job_id = request.args.get('job_id')
    tenant_id = request.args.get('tenant_id')
    project_id = request.args.get('project_id')
    csv_uri = str(request.args.get('csv_uri'))
    ingestion_request = CreateCsvIngestionJobRequest(tenant_id, project_id, csv_uri, job_id)
    pipeline = CreateCsvIngestionJob(ingestion_request=ingestion_request.to_dict())
    pipeline.start()
    redirect_url = "%s/status?root=%s" % (pipeline.base_path, pipeline.pipeline_id)
    return redirect(redirect_url, code=302)


@app.route('/wait')
def wait():
    pipeline_id = request.get("pipeline")
    pipeline = mapreduce_pipeline.MapreducePipeline.from_id(pipeline_id)
    if pipeline.has_finalized:
        # MapreducePipeline has completed
        pass
    else:
        # MapreducePipeline is still running
        pass


@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500
