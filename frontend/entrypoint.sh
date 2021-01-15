#!/bin/bash

COMMAND="$*"

if [[ -z ${COMMAND} ]]; then
    COMMAND="start"
fi

exec bash -c "npm --prefix ./frontend run ${COMMAND}"
