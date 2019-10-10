#!/bin/bash
subdomain=$1.
type=${2^^}
value=$3
if [ $# -lt 3 ]
then
    echo Run: ./route53.sh subdomain type value
    exit 1
    
fi
arr=(${subdomain//./ })
zoneName=${arr[-2]}\.${arr[-1]}\.

zoneId=`aws route53 list-hosted-zones-by-name | jq -r '.HostedZones[] | select(.Name=="'$zoneName'") | .Id'`
echo $zoneName 
echo $zoneId
aws cloudformation deploy --stack-name route53 --template-file ./route53.yml --parameter-overrides HostedZoneId=$zoneId Type=$type Value=$value Name=$subdomain