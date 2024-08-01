import json
import boto3

def read_from_db(user_id):
    inputParams = {
        'status': 'read',
        'user_id': user_id,
    }
    
    recordClient = boto3.client('lambda')
    
    response = recordClient.invoke(
        FunctionName='arn:aws:lambda:us-east-1:533267242577:function:MoniMonitor_ToDB',
        InvocationType='RequestResponse',
        Payload=json.dumps(inputParams)
    )
    
    # Read and decode the response payload
    response_payload = json.loads(response['Payload'].read())
    
    # Extract the body from the response payload
    response_body = json.loads(response_payload['body'])
    
    # Print the response body for debugging
    print(response_body)
    
    # Assuming response_body is a list of transactions
    daily_records = [transaction for transaction in response_body if transaction['Type'] == 'daily']
    monthly_records = [transaction for transaction in response_body if transaction['Type'] == 'monthly']

    return daily_records, monthly_records
