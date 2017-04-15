import fresh_tomatoes
import media
import httplib
import config
import json

# API Key is located in my config.py file
API_KEY = config.API_KEY

# this is establishing an HTTPS connection to TheMovieDB's API
connection = httplib.HTTPSConnection("api.themoviedb.org")

def buildMovie(movie):
	POSTER_BASE_URL = "https://image.tmdb.org/t/p/w500"

	movie_title = movie["title"]
	movie_description = movie["overview"]
	movie_poster = POSTER_BASE_URL + movie["poster_path"]

	MOVIE_ID = movie["id"]
	payload = "{}"
	connection.request("GET", "/3/movie/" + str(MOVIE_ID) + 
						"/videos?language=en-US&api_key=" + API_KEY, payload)
	videos_response = connection.getresponse()
	videos_data = videos_response.read()
	jsonVideos = json.loads(videos_data)
	try:
		VIDEO_KEY = jsonVideos['results'][0]['key']
	except:
		VIDEO_KEY = ""
		print "[!][!] ERROR: NO VIDEO KEY"

	movie_trailer = "https://www.youtube.com/watch?v=" + VIDEO_KEY

	return media.Movie(movie_title,
					movie_description,
					movie_poster,
					movie_trailer)

def main():

	# This is the movie ID. TheMovieDB call is a VIDEO_KEY.
	VIDEO_KEY = ""

	payload = "{}"

	# Making a GET request to The Movie DB for the top movies
	connection.request("GET", "/3/movie/top_rated?page=1&language=en-US&api_key=" +
					API_KEY, payload)

	# Response data from the top movies
	response = connection.getresponse()

	# Data is read in a format that can be parsed.
	data = response.read()

	# Store data into a json object
	jsonData = json.loads(data)


	movies = []
	for movie in jsonData['results']:
		new_movie = buildMovie(movie)
		movies.append(new_movie)
		VIDEO_KEY = ""

	return movies


if __name__ == "__main__":
	movies = main()
	fresh_tomatoes.open_movies_page(movies)
