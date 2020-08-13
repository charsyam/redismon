#!/bin/bash

HOST=`cat hosts`
GROUP_ID=$1
curl -i -X DELETE -H "content-type: application/json" "http://$HOST/api/v1/groups/$GROUP_ID"
