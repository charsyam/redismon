#!/bin/bash

HOST=`cat hosts`
curl -i -X GET -H "content-type: application/json" "http://$HOST/api/v1/groups"
