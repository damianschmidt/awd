#!/bin/bash

COMMAND="$*"

if [[ -z ${COMMAND} ]]; then
    COMMAND="flask run"
fi

exec bash -c "${COMMAND}"
