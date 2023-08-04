#!/bin/bash

set -e

THIS_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

function install {
    set -x
    python -m pip install --upgrade pip
    python -m pip install -r requirements.test.txt
    python -m pip install cookiecutter
}

# (example) ./run.sh test tests/test_slow.py::test__slow_add
function test {
    # run only specified tests, if none specified, run all
    PYTEST_EXIT_STATUS=0
    python -m pytest -m 'not slow' "$THIS_DIR/tests/" \
        --cov "$THIS_DIR/packaging_demo" \
        --cov-report html \
        --cov-report term \
        --cov-report xml \
        --junit-xml "$THIS_DIR/test-reports/report.xml" \
        --cov-fail-under 60 || ((PYTEST_EXIT_STATUS+=$?))
    mv coverage.xml "$THIS_DIR/test-reports/"
    mv htmlcov "$THIS_DIR/test-reports/"
    mv .coverage "$THIS_DIR/test-reports/"
    return $PYTEST_EXIT_STATUS
}

function generate-sample-project {
    set -x
    SAMPLE_REPO_NAME="sample-repo"
    SAMPLE_REPO_DIR="${THIS_DIR}/sample/$SAMPLE_REPO_NAME"

    cat <<EOF > "${THIS_DIR}/cookiecutter.yaml"
default_context:
    repo_name: $SAMPLE_REPO_NAME
EOF

    cookiecutter "$THIS_DIR" \
        --output-dir "$SAMPLE_REPO_DIR" \
        --no-input \
        --config-file "${THIS_DIR}/cookiecutter.yaml" \
        --overwrite-if-exists

}

function clean {
    rm -rf dist build coverage.xml test-reports cookiecutter.yaml
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
