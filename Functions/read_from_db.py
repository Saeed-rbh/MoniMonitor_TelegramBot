import json
import boto3

def read_from_db(user_id):
    inputParams = {
        'status': 'read',
        "user_id": user_id,
    }
    
    recordClient = boto3.client('lambda')
    
    response = recordClient.invoke(
        FunctionName='arn:aws:lambda:us-east-1:533267242577:function:MoniMonitor_ToDB',
        InvocationType='RequestResponse',
        Payload=json.dumps(inputParams)
    )
    
    response_payload = json.loads(response['Payload'].read())
    response = response_payload['body']
    
    daily_records = [transaction for transaction in response if transaction['Type'] == 'daily']
    monthly_records = [transaction for transaction in response if transaction['Type'] == 'monthly']

    return daily_records, monthly_records
