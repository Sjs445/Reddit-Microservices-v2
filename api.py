# Flask modules
import flask_api
from flask import request, jsonify
from flask_api import status, exceptions
from flask_dynamo import Dynamo

# app instance
app = flask_api.FlaskAPI(__name__)

# Table definitions
app.config['DYNAMO_TABLES'] = [
    dict(
        TableName='posts',
        KeySchema=[dict(AttributeName='id', KeyType='HASH')],
        AttributeDefinitions=[dict(AttributeName='id', AttributeType='N')],
        ProvisionedThroughput=dict(ReadCapacityUnits=5, WriteCapacityUnits=5)
    )
]

# Pass app to the Dynamo constructor
dynamo = Dynamo(app)

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
<p>Welcome to the new reddit for posts...</p>'''


# Get all posts
@app.route('/api/v2/resources/posts/all', methods=['GET'])
def all_posts():
    pass
   

# Get post by id and delete post by id
@app.route('/api/v2/resources/posts/<int:id>', methods=['GET', 'DELETE'])
def post(id):
    if request.method == 'GET':
        with app.app_context():
            response = dynamo.tables['posts'].get_item(
            Key={
                'id': id,
                }
                )
            return str(response['Item']), status.HTTP_200_OK
    elif request.method == 'DELETE':
        pass

# POST request for a new post
@app.route('/api/v1/resources/posts', methods=['POST'])
def posts():
    if request.method == 'POST':
        pass

# Create a post
def create_post(post):
    pass

# Get n most recent posts from all communities
@app.route('/api/v1/resources/posts/recent/<int:number_of_posts>', methods=['GET'])
def recent_posts(number_of_posts):
    pass


# Get n most recent posts from specific community
@app.route('/api/v1/resources/posts/recent/<string:sub>/<int:number_of_posts>', methods=['GET'])
def recent_posts_sub(sub, number_of_posts):
    pass

