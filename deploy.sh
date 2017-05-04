#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset
# set -o xtrace

# Set magic variables for current file & dir
__dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
__file="${__dir}/$(basename "${BASH_SOURCE[0]}")"
__base="$(basename ${__file} .sh)"
__root="$(cd "$(dirname "${__dir}")" && pwd)" # <-- change this as it depends on your app

PROJECT_ID="${1:-}"
VERSION="${2:-}"

source ${__dir}/settings.bash
envsubst < ${__dir}/app.yaml.tpl > ${__dir}/app.yaml
gcloud app deploy --project ${PROJECT_ID} --version ${VERSION} app.yaml