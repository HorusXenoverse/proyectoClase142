from flask import Flask, jsonify
import pandas as pd
from demographic_filtering import output
from content_filtering import get_recommendations

movies_data = pd.read_csv('final.csv')

app = Flask(__name__)

# extraer información importante de dataframe
movies_columns = movies_data[['original_title', 'poster_link', 'release_date', 'runtime', 'weighted_rating']]

# variables para almacenar información
liked_movies = []
not_liked_movies = []
did_not_watch = []

# método para obtener información de la base de datos
def get_info():
  first_movie = {
    "original_title": movies_columns.iloc[0,0],
    "poster_link": movies_columns.iloc[0,1],
    "release_date": movies_columns.iloc[0,2],
    "duracion": movies_columns.iloc[0,3],
    "rating": movies_columns.iloc[0,4] 
  }
  return first_movie


# /movies api
@app.route("/movies")
def get_movies():
  movies_dates = get_info()
  return jsonify({
    "data": movies_dates,
    "status": "success"
  })

# /like api+
@app.route("/like")
def liked_movie():
  global movies_columns
  movie_data = get_info()
  liked_movies.append(movie_data)
  movies_columns.drop([0], inplace=True)
  movies_columns = movies_columns.reset_index(drop=True) 
  return jsonify({
     "status": "success" 
     })

# ruta /liked de la segunda pantalla, mostrar las que están en la lista de /like
@app.route("/liked")
def like_movie():
  global liked_movies
  return jsonify({
    "data" : liked_movies,
    "status" : "success"
  })


# /dislike api
@app.route("/dislike")
def dislike_movie():
  global movies_columns
  movies_data = get_info()
  not_liked_movies.append(movies_data)
  movies_columns.drop([0], inplace = True)
  movies_columns = movies_columns.reset_index(drop = True)
  return jsonify({
    "status" : "success"
    })


# /did_not_watch api
@app.route("/did_not_watch")
def did_not_watch_movie():
  global movies_columns
  movies_data = get_info()
  did_not_watch.append(movies_data)
  movies_columns.drop([0], inplace = True)
  movies_columns = movies_columns.reset_index(drop = True)
  return jsonify({
    "status" : "success"
  })

# ruta /popular_movies de la segunda pantalla, mostrar las 10 movies más populares por el filtrado demográfico
@app.route("/popular_movies")
def popular_movie():
  popular_movies_data = []
  for filas, columnas in output.iterrows():
    dic_popular_movies = {
    "original_title": columnas['original_title'],
    "poster_link": columnas['poster_link'] ,
    "release_date": columnas['release_date'] ,
    "duracion": columnas['runtime'],
    "rating": columnas['weighted_rating'] 
    }
    
    popular_movies_data.append(dic_popular_movies)
  return jsonify({
    "data" : popular_movies_data,
    "status" : "success"
  })

# ruta /recommended_movies de la segunda pantalla, mostrar las movies que me recomiendan según a las que le dí me gusta por el filtrado de contenido   
@app.route("/recommneded_movies")
def recommended_movie():
  global liked_movies
  liked_columns = ['original_title', 'poster_link', 'release_date', 'runtime', 'weighted_rating']
  get_liked_columns = pd.DataFrame(columns = liked_columns)
  for liked_index in liked_movies:
    liked_recommendations = get_recommendations(liked_index['original_title'])
    get_liked_columns = get_liked_columns.append(liked_recommendations)

  get_liked_columns.drop_duplicates(subset = ['original_title'], inplace = True)

  recommended_movies_data = []
  for filas, columnas in get_liked_columns.iterrows():
    dic_recommended_movies = {
    "original_title": columnas['original_title'],
    "poster_link": columnas['poster_link'] ,
    "release_date": columnas['release_date'] ,
    "duracion": columnas['runtime'],
    "rating": columnas['weighted_rating'] 
    }
    
    recommended_movies_data.append(dic_recommended_movies)
  return jsonify({
    "data" : recommended_movies_data,
    "status" : "success"
  })
    





if __name__ == "__main__":
  app.run()
