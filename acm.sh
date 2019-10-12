#!/bin/bash
domain=$1
if [ $# -lt 1 ]
then
    echo ./acm.sh domain
    exit 1
fi
certificateArn=`aws acm request-certificate --domain-name $domain --validation-method DNS --options CertificateTransparencyLoggingPreference=DISABLED | jq -r '.CertificateArn'`

echo $certificateArn