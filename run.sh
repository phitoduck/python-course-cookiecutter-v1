#!/bin/bash

set -e

THIS_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

function install {
    python -m pip install --upgrade pip
    python -m pip install cookiecutter
}

function generate-sample-project {
    set -x
    SAMPLE_REPO_NAME="sample-repo"
    SAMPLE_REPO_DIR="${THIS_DIR}/sample/$SAMPLE_REPO_NAME"

    cat <<EOF > "${THIS_DIR}/cookiecutter.yaml"
default_context:
    repo_name: $SAMPLE_REPO_NAME
EOF

    cookiecutter ./ \
        --output-dir "$SAMPLE_REPO_DIR"

}

function clean {
    rm -rf dist build coverage.xml test-reports
    find . \
      -type d \
      \( \
        -name "*cache*" \
        -o -name "*.dist-info" \
        -o -name "*.egg-info" \
        -o -name "*htmlcov" \
      \) \
      -not -path "*env/*" \
      -exec rm -r {} +

    find . \
      -type f \
      -name "*.pyc" \
      -not -path "*env/*" \
      -exec rm {} +
}

function help {
    echo "$0 <task> <args>"
    echo "Tasks:"
    compgen -A function | cat -n
}

TIMEFORMAT="Task completed in %3lR"
time ${@:-help}
