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

function run-upsert-workflow {

    REPO_NAME="${REPO_NAME:-test}"
    PACKAGE_IMPORT_NAME="${PACKAGE_IMPORT_NAME:-test_pkg}"
    CREATE_REPO="${CREATE_REPO:-false}"
    PUBLIC="${PUBLIC:-false}"
    UPSERT_PYPI_SECRETS="${UPSERT_PYPI_SECRETS:-false}"
    POPULATE_FROM_TEMPLATE="${POPULATE_FROM_TEMPLATE:-true}"

    # commit the workflow and push to branch
    function push-workflow-to-branch {
        git checkout -b debug-workflow || git checkout debug-workflow
        git add run.sh .github/workflows/create-or-update-repo.yaml
        git commit -m "ci: update workflow"
        git push --set-upstream origin debug-workflow
    }
    push-workflow-to-branch || true

    # Run the workflow
    gh workflow run .github/workflows/create-or-update-repo.yaml \
        --repo phitoduck/python-course-cookiecutter-v1 \
        --ref debug-workflow \
        --field repo_name=$REPO_NAME \
        --field create_repo=$CREATE_REPO \
        --field public=$PUBLIC \
        --field package_import_name=$PACKAGE_IMPORT_NAME \
        --field upsert_pypi_secrets=$UPSERT_PYPI_SECRETS \
        --field populate_from_template=$POPULATE_FROM_TEMPLATE
}

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
