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
    python -m pytest \
        -m 'not slow' \
        --ignore-glob 'tests/artifacts/*' \
        --numprocesses auto \
        "$THIS_DIR/tests/"
}

# inputs:
#   REPO_NAME
#   PUBLIC_OR_PRIVATE literal "public" or "private"
#   TEST_PYPI_TOKEN, PROD_PYPI_TOKEN
#   SOURCE_REPO_DIR
function create-repo {
    gh repo create "phitoduck/$REPO_NAME" \
        "--$PUBLIC_OR_PRIVATE" \
        --source $SOURCE_REPO_DIR \
        --remote github \
        --push
    gh secret set TEST_PYPI_TOKEN --body "$TEST_PYPI_TOKEN" --repos "phitoduck/$REPO_NAME"
    gh secret set PROD_PYPI_TOKEN --body "$PROD_PYPI_TOKEN" --repos "phitoduck/$REPO_NAME"
}

# REPO_NAME="sample-repo-2" PACKAGE_IMPORT_NAME="sample_repo_2" bash run.sh generate-project

function generate-project {
    set -x

    REPO_NAME="${REPO_NAME:-sample-repo}"
    PACKAGE_IMPORT_NAME="${PACKAGE_IMPORT_NAME:-sample_import_name}"

    cat <<EOF > "${THIS_DIR}/cookiecutter.yaml"
default_context:
    repo_name: $REPO_NAME
    package_import_name: $PACKAGE_IMPORT_NAME
EOF

    cookiecutter "$THIS_DIR" \
        --output-dir "$THIS_DIR" \
        --no-input \
        --config-file "${THIS_DIR}/cookiecutter.yaml" \
        --overwrite-if-exists
}

function open-pr {
    
}

function clean {
    rm -rf dist \
        build \
        coverage.xml \
        test-reports \
        tests/artifacts \
        cookiecutter.yaml \
        sample \
        .coverage
    find . \
      -type d \
      \( \
        -name "*cache*" \
        -o -name "*.dist-info" \
        -o -name "*.egg-info" \
        -o -name "*htmlcov" \
      \) \
      -not -path "*env/*" \
      -exec rm -r {} + || true

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
