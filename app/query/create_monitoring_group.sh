#!/bin/bash

HOST=`cat hosts`
QUERY=create_monitoring_group.query
curl -i -X POST -H "content-type: application/json" -d @$QUERY "http://$HOST/api/v1/groups"
