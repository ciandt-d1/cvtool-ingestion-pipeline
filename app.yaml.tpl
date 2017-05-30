runtime: python27
api_version: 1
threadsafe: yes
service: cvtool-ingestion-pipeline

handlers:

- url: /_ah/pipeline(/.*)?
  script: pipeline.handlers._APP

- url: .*  # This regex directs all routes to main.app
  script: main.app

includes:
- lib/mapreduce/include.yaml

skip_files:
- ^(.*/)?#.*#$
- ^(.*/)?.*~$
- ^(.*/)?.*\.py[co]$
- ^(.*/)?.*/RCS/.*$
- ^(.*/)?\..*$
- ^(.*/)?\.bak$
- ^(.*/)?\.sh$
- ^venv$
- \.idea/.*$

libraries:
- name: ssl
  version: 2.7.11

env_variables:
  JOBS_API_HOST: ${JOBS_API_HOST}
  IMAGES_API_HOST: ${IMAGES_API_HOST}
  DEBUG: ${DEBUG}

#libraries:
#- name: jinja2
#  version: latest
