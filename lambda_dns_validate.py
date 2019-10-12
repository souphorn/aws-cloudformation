import boto3
import time
import re
def upsert_route53(dns):
    route53 = boto3.client("route53")
    # To be replaced
    zoneId = 'Z1R068PF2D9IYP'
    route53.change_resource_record_sets(
        HostedZoneId = zoneId,
        ChangeBatch = {
            'Changes': [{
                'Action': 'UPSERT',
                'ResourceRecordSet': {
                    'Type': dns['Type'],
                    'Name': dns['Name'],
                    'TTL': 60,
                    'ResourceRecords': [{
                        'Value': dns['Value']
                    }]
                }
            }]
        }
    )
def get_dns(event):
    reason = event['ResourceStatusReason']
    m = re.search(r'\{Name\: (.+),\s?Type\: (.+),\s?Value\: (.+)\}', reason)
    if m:
        dns = {
            'Name': m.group(1),
            'Type': m.group(2),
            'Value': m.group(3)
        }
        print(dns)
        return dns
    return None
def get_stack_event():
    try:
        client = boto3.client("cloudformation")
        param = {'StackName': 'acm'}
        events = client.describe_stack_events(**param)
        for e in events['StackEvents']:
            if (
                e['ResourceType'] == 'AWS::CertificateManager::Certificate' and
                e['ResourceStatus'] == 'CREATE_IN_PROGRESS' and 
                'ResourceStatusReason' in e and
                'Content of DNS Record' in e['ResourceStatusReason']
            ):
                return e
    except Exception as e:
        return None
    # print(events)
def handler(event, context):
    while event is None:
        event = get_stack_event()
        if (event is None):
            print("Sleep for 5 seconds")
            time.sleep(5)
        else:
            dns = get_dns(event)
            upsert_route53(dns)
if __name__ == '__main__':
   
    handler(None, None)