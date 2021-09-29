from storage import all_movies, liked_movies, disliked_movies, did_not_watch
from demographic_filtering import output
from content_filtering import get_recommendations
from flask import Flask,jsonify,Request
import csv
all_movies=[]
with open("movies.csv",encoding="utf-8") as f :
    reader=csv.reader(f)
    data=list(reader)
    all_movies=data[1:]

liked_movies=[]
disliked_movies=[]
did_not_watch=[]

app=Flask(__name__)
@app.route("/get-movie")
def get_movie():
    movies={
        "title":all_movies[0][19],
        "poster_link": all_movies[0][27],
        "release_date": all_movies[0][13] or "N/A",
        "duration": all_movies[0][15],
        "rating": all_movies[0][20],
        "overview": all_movies[0][9]

    }
    return jsonify({
        "data":movies[0],
        "status":"succes"
    })

@app.route("/liked-movie", methods=["POST"])
def liked_movie():
    movie = all_movies[0]
    liked_movies.append(movie)
    all_movies.pop(0)
    return jsonify({
        "status": "success"
    }), 201
@app.route("/disliked-movie",methods=["POST"])
def disliked_movie():
        movie = all_movies[0]
        disliked_movies.append(movie)
        all_movies.pop(0)
        return jsonify({
            "status":"succes"
        }),201
@app.route("/did-not-watch", methods=["POST"])
def did_not_watch():
    movie = all_movies[0]
    did_not_watch.append(movie)
    all_movies.pop(0)
    return jsonify({
        "status": "success"
    }), 201
@app.route("/popular-movies")
def popular_movies():
    movie_data = []
    for movie in all_movies:
        _d = {
            "title": movie[0],
            "poster_link": movie[1],
            "release_date": movie[2] or "N/A",
            "duration": movie[3],
            "rating": movie[4],
            "overview": movie[5]
        }
        movie_data.append(_d)
    return jsonify({
        "data": movie_data,
        "status": "success"
    }), 200
@app.route("/recommended-movie")
def recommended_movie():
    all_recommended=[]
    for liked_movies in liked_movie:
        output=get_recommendations(liked_movie[19])
        for data in output:
            all_recommended.append(data)
    import itertools
    all_recommended.sort()
    all_recommended=list(all_recommended for all_recommended,_ in itertools.groupby(all_recommended))
    movie_data=[]
    for recommended in all_recommended:
        _d = {
            "title": recommended[0],
            "poster_link": recommended[1],
            "release_date": recommended[2] or "N/A",
            "duration": recommended[3],
            "rating": recommended[4],
            "overview": recommended[5]
        }
        movie_data.append(_d)
    return jsonify({
        "data": movie_data,
        "status": "success"
    }), 200

if __name__=="__main__":
    app.run()
