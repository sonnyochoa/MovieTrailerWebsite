import fresh_tomatoes
import media
import httplib
import config
import json

#top_movies_connection = httplib.HTTPSConnection("api.themoviedb.org")
connection = httplib.HTTPSConnection("api.themoviedb.org")

API_KEY = config.API_KEY
VIDEO_KEY = ""

payload = "{}"

# Making an GET request to The Movie DB for the top movies
connection.request("GET", "/3/movie/top_rated?page=1&language=en-US&api_key=" + API_KEY, payload)

# Response from the top movies
response = connection.getresponse()

# Data from top movies
data = response.read()

# Store data into a json object
jsonData = json.loads(data)

POSTER_BASE_URL = "https://image.tmdb.org/t/p/w500"
movies = []
for movie in jsonData['results']:
	movie_title = movie["title"]
	movie_description = movie["overview"]
	movie_poster = POSTER_BASE_URL + movie["poster_path"]

	MOVIE_ID = movie["id"]
	connection.request("GET", "/3/movie/" + str(MOVIE_ID) + "/videos?language=en-US&api_key=" + API_KEY, payload)
	videos_response = connection.getresponse()
	videos_data = videos_response.read()
	jsonVideos = json.loads(videos_data)
	try:
		VIDEO_KEY = jsonVideos['results'][0]['key']
	except:
		VIDEO_KEY = ""
		print "[!][!] ERROR: NO VIDEO KEY"

	movie_trailer = "https://www.youtube.com/watch?v=" + VIDEO_KEY

	movies.append(
		media.Movie(movie_title,
					movie_description,
					movie_poster,
					movie_trailer)
	)

	VIDEO_KEY = ""


fresh_tomatoes.open_movies_page(movies)
