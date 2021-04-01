#!/bin/bash

HOSTED_ZONE=$1
RECORD=$2

# Check arguments
if [ -z "$RECORD" ]; then
    echo "ERROR: $(basename $0) HOSTED_ZONE RECORD"
    exit 1
fi

# Escape wildcard records
RECORD=$(echo "$RECORD" |sed -e "s/\*/\\\\\\\052/")

# Check aws access
zones=$(aws route53 list-hosted-zones --output json 2>/dev/null)
if [ $? -ne 0 ]; then
    echo "ERROR: Unable to list AWS Route53 hosted zones"
    exit 1
fi

# Get zone id
select=".HostedZones[] | select(.Name==\"$HOSTED_ZONE.\") | .Id"
zone_id=$(echo "$zones" |jq "$select" |cut -f 3 -d / |tr -d \")

# Get zone records
records=$(aws route53 list-resource-record-sets --hosted-zone-id $zone_id)

# Get zone record value
select=".ResourceRecordSets[] | select (.Name == \"$RECORD.\")"
record_value=$(echo "$records" |jq "$select" |jq .ResourceRecords[].Value)

# Exit if no records found
if [ -z "$record_value" ]; then
    exit
fi

# Create changeset
(
cat <<EOF
{
  "Comment": "Delete record set",
  "Changes": [
    {
      "Action": "DELETE",
      "ResourceRecordSet": {
        "Name": "$RECORD.",
        "Type": "CNAME",
        "TTL": 3600,
        "ResourceRecords": [
          {
            "Value": ${record_value}
          }
        ]
      }
    }
  ]
}
EOF
) > /tmp/$zone_id.json

# Delete record
aws route53 change-resource-record-sets --hosted-zone-id $zone_id --change-batch file:///tmp/$zone_id.json
