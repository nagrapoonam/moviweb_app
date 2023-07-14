import json

import requests

from .data_manager_interface import DataManagerInterface


class JSONDataManager(DataManagerInterface):
    def __init__(self, filename):
        self.filename = filename

    def get_all_users(self):
        try:
            with open(self.filename, "r") as json_file:
                data = json.load(json_file)
                users = []
                for user_id, user_info in data.items():
                    user = {
                        'id': user_id,
                        'name': user_info['name'],
                        'movies': user_info['movies']
                    }
                    users.append(user)
                return users
        except IOError as e:
            # Handle the IOError exception (e.g., log the error, return an error message, etc.)
            # ...
            return []

    def get_user_movies(self, user_id):
        try:
            with open(self.filename) as json_file:
                data = json.load(json_file)
                user_info = data.get(str(user_id))
                if user_info:
                    user_movies = user_info.get("movies", {})
                    movies = []
                    for movie_id, movie_info in user_movies.items():
                        movie = {
                            'id': movie_id,
                            'name': movie_info['name'],
                            'director': movie_info['director'],
                            'year': movie_info['year'],
                            'rating': movie_info['rating']
                        }
                        movies.append(movie)
                    return movies
        except IOError as e:
            # Handle the IOError exception
            # ...
            return []

        return []

    def add_user(self, user_name):
        try:
            with open(self.filename, "r+") as json_file:
                data = json.load(json_file)
                user_ids = list(data.keys())
                new_user_id = str(int(max(user_ids)) + 1) if user_ids else '1'
                for user_info in data.values():
                    if user_info['name'] == user_name:
                        return f"Username '{user_name}' already exists. Please choose a different username."
                data[new_user_id] = {
                    'name': user_name,
                    'movies': {}
                }
                json_file.seek(0)
                json.dump(data, json_file, indent=4)
                json_file.truncate()
                return f"User '{user_name}' added successfully."
        except IOError as e:
            # Handle the IOError exception
            # ...
            return f"An error occurred while adding a user."

    def add_movie(self, user_id, movie_name):
        try:
            api_url = f"http://www.omdbapi.com/?apikey=4bf81bd7&t={movie_name}"
            response = requests.get(api_url)
            movie_data = response.json()

            if movie_data.get("Response") != "True":
                return f"Movie '{movie_name}' not found in OMDB data."

            movie = {
                'name': movie_name,
                'director': movie_data.get("Director"),
                'year': movie_data.get("Year"),
                'rating': movie_data.get("imdbRating")
            }

            user_id = str(user_id)
            with open(self.filename, "r+") as json_file:
                data = json.load(json_file)
                user_info = data.get(user_id)
                if user_info:
                    user_movies = user_info.setdefault('movies', {})
                    movie_id = str(len(user_movies) + 1)
                    user_movies[movie_id] = movie

                    json_file.seek(0)
                    json.dump(data, json_file, indent=4)
                    json_file.truncate()

                    return f"Movie '{movie_name}' added for user {self.get_user_name(user_id)} successfully."

            return f"User with ID {user_id} not found."
        except requests.RequestException as e:
            # Handle the RequestException (e.g., log the error, return an error message, etc.)
            # ...
            return f"An error occurred while adding the movie."

    def update_movie(self, user_id, movie_id, director, year, rating):
        try:
            user_id = str(user_id)
            movie_id = str(movie_id)

            with open(self.filename, "r+") as json_file:
                data = json.load(json_file)
                user_info = data.get(user_id)

                if user_info:
                    movie = user_info.get("movies", {}).get(movie_id)

                    if movie:
                        movie["director"] = director
                        movie["year"] = year
                        movie["rating"] = rating

                        json_file.seek(0)
                        json.dump(data, json_file, indent=4)
                        json_file.truncate()
                        return f"Movie '{movie['name']}' updated for user '{user_info['name']}' successfully."

                    return f"Movie '{self.get_movie_name(movie_id)}' not found for user '{self.get_user_name(user_id)}'."

                return f"User with ID '{self.get_user_name(user_id)}' not found."
        except IOError as e:
            # Handle the IOError exception
            # ...
            return f"An error occurred while updating the movie."

    def delete_movie(self, user_id, movie_id):
        try:
            user_id = str(user_id)
            movie_id = str(movie_id)

            with open(self.filename, "r+") as json_file:
                data = json.load(json_file)
                user_info = data.get(user_id)
                if user_info:
                    movies = user_info.get("movies", {})
                    movie = movies.get(movie_id)
                    if movie:
                        del movies[movie_id]
                        json_file.seek(0)
                        json.dump(data, json_file, indent=4)
                        json_file.truncate()
                        return f"Movie '{movie['name']}' deleted for user with ID {user_id} successfully."
                    return f"Movie not found for user with ID {user_id}."
                return f"User with ID {user_id} not found."
        except IOError as e:
            # Handle the IOError exception
            # ...
            return f"An error occurred while deleting the movie."

    def get_movie(self, user_id, movie_id):
        try:
            user_id = str(user_id)
            movie_id = str(movie_id)

            with open(self.filename, "r") as json_file:
                data = json.load(json_file)
                user_info = data.get(user_id)
                if user_info:
                    movies = user_info.get("movies", {})
                    movie = movies.get(movie_id)
                    if movie:
                        return {
                            'id': movie_id,
                            'name': movie['name'],
                            'director': movie['director'],
                            'year': movie['year'],
                            'rating': movie['rating']
                        }
        except IOError as e:
            # Handle the IOError exception
            # ...
            return None

    def get_movie_name(self, movie_id):
        # Replace with your logic to retrieve movie name based on movie ID
        return f"Movie Name for ID {movie_id}"

    def get_user_name(self, user_id):
        # Replace with your logic to retrieve user name based on user ID
        return f"User Name for ID {user_id}"
