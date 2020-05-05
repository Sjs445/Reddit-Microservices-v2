# Reddit-Microservices-v2

## Shane Spangenberg, Brendon Linthurst, Collin Campbell

#### Before running initialize the database by running  ```flask init```

#### Open a new terminal and ```cd dynamodb_local_latest``` and run  ```java -Djava.library.path=./DynamoDBLocal_lib -jar DynamoDBLocal.jar -sharedDb``` to start dynamodb

#### Then start the service by running ```flask run```

### Posts in Json Format

```json
{
    "id": "Number",
    "title": "Post Title",
    "body": "Body of Post",
    "user": "username",
    "sub": "sub community",
    "url": "www.example.com",
    "posted_time": "YYY-MM-DD HH:MM:SS"
}
```

## Homepage

```/``` Method = GET

Returns the homepage of the Reddit Microservices.


## Post Routes


### Get all posts

```/api/v2/resources/posts/all``` Method = GET

Returns all posts in json format.

### Get post by ID and delete post by ID 

```/api/v2/resources/posts/<string:sub>/<int:id>``` Methods = GET && DELETE

Note: the user must supply the sub.

Returns the specified post by ID in json format.

#### To test delete run the deletepost.sh as follows

First make the shell file executable by running ```chmod +x deletepost.sh```

Then run the shell command like ```./deletepost.sh <:id>``` where <:id> is the id of the post you want to delete.


### Create a new post

```/api/v2/resources/posts``` Method = POST

#### To test create a new post run the newpost.sh as follows

First make the shell file executable by running```chmod +x newpost.sh```

Then run the shell command like```./newpost.sh```

After the post is created it should return```201 Created ```with the ID of the post that was created. If there is already a post with that same ID it will return```409 Conflict```. 

### Get n most recent posts from all communities

```/api/v2/resources/posts/recent/<int:number_of_posts>``` Method = GET

Simply returns the most recent posts limited to size n from every community.

### Get n most recent posts from specific community

```/api/v2/resources/posts/recent/<string:sub>/<int:number_of_posts>``` Method = GET

Simply returns the most recent posts limited to size n from a specified community.

## Vote routes

### Retrieve all posts that have votes.

```/votes/all``` Method = GET

View all posts receiving votes

### Upvote a post

```/upvote/<int:id>``` Method = GET / PUT

When a PUT is requested, it will upvote the post with id matching the request.

e.g. ```curl -X PUT http://localhost:5000/upvote/1```

When a GET is requested, it simply shows the number of upvotes

### Downvote a post

```/downvote/<int:id>``` Method = GET / PUT

When a PUT is requested, it will downvote the post with id matching the request.

e.g. ```curl -X PUT http://localhost:5000/downvote/1```

When a GET is requested, it simply shows the number of downvotes

### Retrieve total votes for post with ID

```/votes/<int:id>``` Method = GET

Returns upvotes and downvotes for a post

### List top N scoring posts

```/top/<int:id>``` Method = GET

View the top N scoring post where N = id

### Return sorted list by score for all

```/votes/highscore``` Method = GET

View the top scoring posts sorted by score.

### Seed fake voting data

```/debug/create``` Method = GET

You may wish to create fake vote data. Calling a GET request will seed the Redis database with 10 posts with serialized ID and random number of upvotes and downvotes.

