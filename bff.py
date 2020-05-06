import flask_api
import requests
from feedgen.feed import FeedGenerator
from flask import make_response

app = flask_api.FlaskAPI(__name__)

@app.route("/")
def main():
    response = requests.get("http://localhost:2015/posts").text
    return response

@app.route("/<string:community>", methods=['GET'])
def top_25_Posts(community):
    response = requests.get('http://localhost:2015/posts/api/v2/resources/posts/recent/' + community + "/25")
    rData = response.json()
    fg = FeedGenerator()
    fg.id(community)
    fg.title(community + " top 25 posts")
    fg.link(href='http://localhost:2015/posts/api/v2/resources/posts/recent/' + community + "/25")
    fg.description("This feed is to generate the top posts from a specific sub.")

    for post in rData:
        fe = fg.add_entry()
        fe.id(str(post['id']))
        fe.title(post['title'])
        fe.link(href=post['url'])
        fe.content(post['body'])

    rssFeed = make_response(fg.rss_str())
    rssFeed.headers.set('Content-Type', 'application/rss+xml')
    return rssFeed


@app.route("/all", methods=['GET'])
def all_top_25_Posts():
    response = requests.get("http://localhost:2015/posts/api/v2/resources/posts/recent/25")
    rData = response.json()
    fg = FeedGenerator()
    fg.id("Top_Posts")
    fg.title("Top 25 posts")
    fg.link(href="http://localhost:2015/posts/api/v2/resources/posts/recent/25")
    fg.description("This feed is to generate the top posts from the entire site")

    for post in rData:
        fe = fg.add_entry()
        fe.id(str(post['id']))
        fe.title(post['title'])
        fe.link(href=post['url'])
        fe.content(post['body'])

    rssFeed = make_response(fg.rss_str())
    rssFeed.headers.set('Content-Type', 'application/rss+xml')
    return rssFeed

@app.route("/votes/<string:community>", methods=['GET'])
def top_25_Posts_Votes(community):
    response = requests.get('http://localhost:2015/posts/api/v2/resources/posts/recent/' + community + "/25")
    rData = response.json()
    fg = FeedGenerator()
    fg.id(community)
    fg.title(community + " top 25 posts")
    fg.link(href='http://localhost:2015/posts/api/v2/resources/posts/recent/' + community + "/25")
    fg.description("This feed is to generate the top posts from a specific sub.")

    for post in rData:
        fe = fg.add_entry()
        fe.id(str(post['id']))
        fe.title(post['title'])
        fe.link(href=post['url'])
        fe.content(post['body'])

    rssFeed = make_response(fg.rss_str())
    rssFeed.headers.set('Content-Type', 'application/rss+xml')
    return rssFeed

@app.route("/postVotes", methods=['GET'])
def all_top_25_Posts_Votes():
    response = requests.get("http://localhost:2015/posts/api/v2/resources/posts/recent/25")
    rData = response.json()
    fg = FeedGenerator()
    fg.id("Top_Posts")
    fg.title("Top 25 posts")
    fg.link(href="http://localhost:2015/posts/api/v2/resources/posts/recent/25")
    fg.description("This feed is to generate the top posts from the entire site")

    for post in rData:
        fe = fg.add_entry()
        fe.id(str(post['id']))
        fe.title(post['title'])
        fe.link(href=post['url'])
        fe.content(post['body'])

    rssFeed = make_response(fg.rss_str())
    rssFeed.headers.set('Content-Type', 'application/rss+xml')
    return rssFeed

@app.route("/reddit")
def all():
    response = requests.get("http://localhost:2015/posts/api/v2/resources/posts/recent/25")
    rData = response.json()
    post = response.json()
    fg = FeedGenerator()
    fg.id("Top_Posts")
    fg.title("Top 25 posts")
    fg.link(href="http://localhost:2015/posts/api/v2/resources/posts/recent/25")
    fg.description("This feed is to generate the top posts from the entire site")

    for post in rData:
        fe = fg.add_entry()
        fe.id(str(post['id']))
        fe.title(post['title'])
        fe.link(href=post['url'])
        fe.content(post['body'])

    rssFeed = make_response(fg.rss_str())
    rssFeed.headers.set('Content-Type', 'application/rss+xml')
    return rssFeed

if __name__=="__main__":
    app.run(host='127.0.0.1', debug=True)