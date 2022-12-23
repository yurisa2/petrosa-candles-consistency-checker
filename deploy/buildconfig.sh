#!/usr/bin/env bash

eval "echo \"$(cat deploy/newrelic.ini.tmpl)\" > newrelic.ini"