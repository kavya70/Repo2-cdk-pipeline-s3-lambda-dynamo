import json
import boto3

def handler(event, context):
    # TODO implement
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    try:
        s3 = boto3.client('s3')
        response = s3.get_object(Bucket=bucket, Key=key)
        csvcontent = response['Body'].read().split(b'\n')
        for line in csvcontent:
            data = line.decode('utf8').strip().split(',')
            put_movie(data[0],data[1],data[2],data[3])
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        return {
        'statusCode': 500,
        'body': json.dumps('Failed to insert data into db')
        }
        raise e
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda! Completed inserting data into db')
    }

def put_movie(moviename, title, plot, rating, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table('movieDetails')
    response = table.put_item(
       Item={
            'movieName': moviename,
            'title': title,
            'info': {
                'plot': plot,
                'rating': rating
            }
        }
    )