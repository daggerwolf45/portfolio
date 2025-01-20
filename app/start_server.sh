#!/usr/bin/env bash

# Load env
[[ -z "${DEPLOY_DIR}" ]] && directory='/home/www/portfolio' || directory="${DEPLOY_ENV}"
cd "$directory"

source .venv/bin/activate
source config

$LAUNCH
