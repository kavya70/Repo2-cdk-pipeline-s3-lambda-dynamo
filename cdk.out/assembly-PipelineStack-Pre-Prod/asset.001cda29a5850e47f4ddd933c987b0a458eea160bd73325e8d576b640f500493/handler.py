import json
import boto3

def handler(event, context):
    # TODO implement
    put_movie('movie2','2012','suspense','4.5')
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }



def put_movie(title, year, plot, rating, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table('movieDetails')
    response = table.put_item(
       Item={
            'movieName': title,
            'title': title,
            'info': {
                'plot': plot,
                'rating': rating
            }
        }
    )
    return response
