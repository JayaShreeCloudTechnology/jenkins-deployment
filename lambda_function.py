import json
import boto3

# Initialize AWS clients
s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')

# DynamoDB table name
TABLE_NAME = "EmployeeRecords"

def lambda_handler(event, context):
    """
    Lambda function to process an S3 upload event and store parsed data in DynamoDB.
    """
    try:
        # Extract bucket name and file key from event
        bucket_name = event['Records'][0]['s3']['bucket']['name']
        object_key = event['Records'][0]['s3']['object']['key']
        print(f"Processing file: {object_key} from bucket: {bucket_name}")

        # Download the file from S3
        response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
        file_content = response['Body'].read().decode('utf-8')

        # Parse file content (assuming JSON file)
        data = json.loads(file_content)
        print("File content:", data)

        # Write to DynamoDB
        table = dynamodb.Table(TABLE_NAME)
        for employee in data.get('employees', []):
            table.put_item(Item={
                'employee_id': employee['id'],
                'name': employee['name'],
                'department': employee['department'],
                'location': employee['location']
            })
        print("Data successfully written to DynamoDB.")

        return {
            'statusCode': 200,
            'body': json.dumps('Data processed successfully!')
        }

    except Exception as e:
        print("Error:", str(e))
        return {
            'statusCode': 500,
            'body': json.dumps('Error processing file.')
        }
