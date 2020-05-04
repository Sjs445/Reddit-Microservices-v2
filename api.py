# Flask modules
import flask_api
from flask import request, jsonify
from flask_api import status, exceptions
from flask_dynamo import Dynamo
import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key, Attr
import json
import decimal

#   start dynamo with
#                   java -Djava.library.path=./DynamoDBLocal_lib -jar DynamoDBLocal.jar -sharedDb
#   run 'flask init' to initialize the database
#   run 'flask run' to run the microservice

# app instance
app = flask_api.FlaskAPI(__name__)

# Table definitions and key definitions
app.config['DYNAMO_TABLES'] = [
    dict(
        TableName='posts',
        KeySchema=[dict(AttributeName='id', KeyType='HASH'),
        dict(AttributeName='sub', KeyType='RANGE')],
        AttributeDefinitions=[dict(AttributeName='id', AttributeType='N'),
        dict(AttributeName='sub', AttributeType='S')],
        ProvisionedThroughput=dict(ReadCapacityUnits=5, WriteCapacityUnits=5)
    )
]

# Pass app to the Dynamo constructor
dynamo = Dynamo(app)

# Helper class to convert a DynamoDB item to JSON.
# Credit from  https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GettingStarted.Python.03.html#GettingStarted.Python.03.02
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


# Initialize the database by running 'flask init'
@app.cli.command('init')
def init_db():
    with app.app_context():
        dynamo.create_all()
        r = dynamo.tables['posts'].put_item(Item={
        'id': 0,
        'title': 'test title',
        'body': 'Example body',
        'user': 'example_user123',
        'sub': 'example_sub',
        'url': 'www.example.com',
        'posted_time': '2020-01-27 12:20:10'
        })

        if(r):
            print("Initialized database!")

# Homepage
@app.route('/', methods=['GET'])
def home():
    return '''<h1>The New Reddit</h1>
<p>Welcome to the new reddit microservice for posts...</p>'''


# Get all posts
@app.route('/api/v2/resources/posts/all', methods=['GET'])
def all_posts():
    try:
        response = dynamo.tables['posts'].scan()
        return (json.dumps(response['Items'], cls=DecimalEncoder)), status.HTTP_200_OK
    except:
        return("Failed"), status.HTTP_404_NOT_FOUND


# Get post by id and delete post by id *** user specificies the sub ***
@app.route('/api/v2/resources/posts/<string:sub>/<int:id>', methods=['GET', 'DELETE'])
def post(id, sub):
    if request.method == 'GET':
        with app.app_context():
            try:
                response = dynamo.tables['posts'].get_item(
                Key={
                'id': id,
                'sub': sub,
                })
                item = response['Item']
                return(json.dumps(item, indent=4, cls=DecimalEncoder)), status.HTTP_200_OK  
            except:
                return("<h1>404 NOT FOUND</h1><br><h2>post unavailable</h2>"), status.HTTP_404_NOT_FOUND
    elif request.method == 'DELETE':
        try:
            response = dynamo.tables['posts'].delete_item(
            Key={
                'id': id,
                'sub': sub,
            }
        )
        except ClientError as e:
            if e.response['Error']['Code'] == "ConditionalCheckFailedException":
                return(e.response['Error']['Message'])
            else:
                raise
        else:
            print("DeleteItem succeeded!")
            return(json.dumps(response, indent=4, cls=DecimalEncoder))     
    

# POST request for a new post
@app.route('/api/v2/resources/posts', methods = ['POST'])
def posts():
    if request.method == 'POST':
        return create_post(request.data)

# Create a post
def create_post(post):
    posted_fields = {*post.keys()}
    required_fields = {'id', 'title', 'body', 'user', 'sub', 'url', 'posted_time'}

    if not required_fields <= posted_fields:
        message = f'Missing fields: {required_fields - posted_fields}'
        raise exceptions.ParseError(message)
    try:
        response = dynamo.tables['posts'].put_item(
        Item={
            **post
        }
        )
    except Exception as e:
        return { 'error': str(e) }, status.HTTP_409_CONFLICT

    return (json.dumps(response, indent=4, cls=DecimalEncoder)), status.HTTP_201_CREATED, {
        'Location': f'/api/v2/resources/posts/{post["id"]}'
    }

# Get n most recent posts from all communities
@app.route('/api/v2/resources/posts/recent/<int:number_of_posts>', methods = ['GET'])
def recent_posts(number_of_posts):
    try:
        fe = Key('id').between(0, number_of_posts)
        response = dynamo.tables['posts'].scan(
            FilterExpression = fe
        )
        if(not response['Items']):
            return("<h1>404 NOT FOUND</h1><br><h2>Sorry, this post is gone.<h2>"), status.HTTP_404_NOT_FOUND 
        else:
            return(json.dumps(response['Items'], indent=4, cls=DecimalEncoder))
    except:
        return("<h1>404 NOT FOUND</h1><br>"), status.HTTP_404_NOT_FOUND


# Get n most recent posts from specific community
@app.route('/api/v2/resources/posts/recent/<string:sub>/<int:number_of_posts>', methods = ['GET'])
def recent_posts_sub(sub, number_of_posts):
    try:
        fe = Key('id').between(0, number_of_posts) and Key('sub').begins_with(sub)
        response = dynamo.tables['posts'].scan(
            FilterExpression = fe
        )
        if(not response['Items']):
            return("<h1>404 NOT FOUND</h1><br><h2>Sorry, this post is gone.<h2>"), status.HTTP_404_NOT_FOUND 
        else:
            return(json.dumps(response['Items'], indent=4, cls=DecimalEncoder))
    except:
        return("<h1>404 NOT FOUND</h1><br>"), status.HTTP_404_NOT_FOUND
