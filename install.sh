#!/usr/bin/env bash
PYTHON_VERSION="3.8.7"
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

pyenv install --skip-existing ${PYTHON_VERSION}
rc=$?
if [[ ${rc} -ne 0 ]]; then
    >&2 echo "pyenv install of Python ${PYTHON_VERSION} failed"
    exit 1
fi

pyenv local ${PYTHON_VERSION}
rc=$?
if [[ ${rc} -ne 0 ]]; then
    >&2 echo "Failed to change local pyenv version to ${PYTHON_VERSION}"
    exit 2
fi

$(pyenv which python) -m venv "${DIR}/venv"
rc=$?
if [[ ${rc} -ne 0 ]]; then
    >&2 echo "Failed to create virtualenv using python version ${PYTHON_VERSION}"
    exit 3
fi

echo "export PYTHONPATH=$DIR/src" >> $DIR/venv/bin/activate
. $DIR/venv/bin/activate

pip install --upgrade pip
for REQ_FILE in requirements.txt
do
    pip install -r $DIR/$REQ_FILE
    rc=$?
    if [[ ${rc} -ne 0 ]]; then
        >&2 echo "Failed to install ${REQ_FILE}"
        exit 4
    fi
done