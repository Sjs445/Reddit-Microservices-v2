import flask_api
import random
from flask import request
from flask_api import status, exceptions
from flask_redis import Redis

# Initializing Flask API with Redis
app = flask_api.FlaskAPI(__name__)
r = Redis(app)
#app.config.from_envvar('APP_CONFIG')

# Configure Redis
app.config['REDIS_HOST'] = 'localhost'
app.config['REDIS_TIMEOUT'] = None
app.config['REDIS_PORT'] = 6379
app.config['REDIS_DB'] = 0
app.config['REDIS_PASSWORD'] = None

# Seed fake posts for manipulation
# Call a GET to seed some fake data into DB
@app.route('/debug/create', methods=['GET'])
def create():
	if request.method == 'GET':
            for i in range(10):
                postid = r.incr("next")
                upvotes = random.randint(0, 100)
                downvotes = random.randint(0, 100)
                properties = {
                    "post_id":"{}".format(postid),
                    "upvotes": upvotes,
                    "downvotes": downvotes,
                    "score": upvotes-downvotes
                }
                r.sadd("all","post{}".format(postid))
                r.hmset("post{}".format(postid), properties)
            return "Successfully seeded post data", status.HTTP_200_OK


# Homepage
@app.route('/', methods=['GET'])
def home():
    return r.keys(), status.HTTP_200_OK

# Retrieve all votes
@app.route('/votes/all', methods=['GET'])
def retrieve_all_votes():
    return r.keys(), status.HTTP_200_OK

# Upvote
@app.route('/upvote/<int:id>', methods=['GET', 'PUT'])
def upvote(id):
    if request.method == 'GET':
        return r.hgetall("post{}".format(id))
    elif request.method == 'PUT':
        r.hincrby("post{}".format(id), "upvote", 1)
        r.hincrby("post{}".format(id), "score", 1)
        return {"upvote": r.hget("post{}".format(id),"upvote")}
    else:
        return "No such entry", status.HTTP_404_NOT_FOUND

# Downvote
@app.route('/downvote/<int:id>', methods = ['GET', 'PUT'])
def downvote(id):
    if request.method == 'GET':
        return r.hgetall("post{}".format(id))
    elif request.method == 'PUT':
        r.hincrby("post{}".format(id), "downvote", 1)
        r.hincrby("post{}".format(id), "score", -1)
        return {"downvote": r.hget("post{}".format(id),"downvote")}
    else:
        return "No such entry", status.HTTP_404_NOT_FOUND

# Retrieve the total number of votes for a post with a specific ID
@app.route('/votes/<int:id>', methods=['GET'])
def report_number_of_votes(id):
    upvotes = r.hget("post{}".format(id),"upvotes")
    downvotes = r.hget("post{}".format(id),"downvotes")
    return {"upvotes": upvotes,
            "downvotes": downvotes
            }, status.HTTP_200_OK

# List the n top scoring posts
@app.route('/top/<int:top_n>', methods=['GET'])
def top_scoring_posts(top_n):
    return r.sort("all", start=0, num=top_n, by="*->score", desc=True), status.HTTP_200_OK

# Return the list sorted by score for all posts
@app.route('/votes/highscore', methods=['GET'])
def sorted_by_score():
    return r.sort("all", by="*->score", desc=True), status.HTTP_200_OK
