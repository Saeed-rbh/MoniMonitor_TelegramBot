import boto3
import json

def record_to_db(record_entry, user_id, record_type):

    inputParams = {
            "record_entry"   : record_entry,
        }
    recordClient = boto3.client('lambda')
    response = recordClient.invoke(
        FunctionName='arn:aws:lambda:us-east-1:533267242577:function:MoniMonitor_Openai',
        InvocationType='RequestResponse',
        Payload=json.dumps(inputParams)
    )
    response_payload = json.loads(response['Payload'].read())
    label = response_payload['body']
    
    record_entry['Label'] = label
    
    inputParams = {
            'status': 'record',
            "record_entry"   : record_entry,
            "user_id"      : user_id,
            "record_type"     : record_type
        }

    recordClient = boto3.client('lambda')
    response = recordClient.invoke(
        FunctionName='arn:aws:lambda:us-east-1:533267242577:function:MoniMonitor_ToDB',
        InvocationType='RequestResponse',
        Payload=json.dumps(inputParams)
    )
    
    response_payload = json.loads(response['Payload'].read())
    response = response_payload['body']
    
    