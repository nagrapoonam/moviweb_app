import json, requests
# importing for working with JSON data and making HTTP requests to external resources
from datamanager.data_manager_interface import DataManagerInterface
#implementing the methods

class JSONDataManager:
    def __init__(self, filename):
        """ Takes a filename parameter and initializes the self.filename attribute with the provided value
        """
        self.filename = filename

    def get_all_users(self):
        """ reads the JSON file, extracts the user data, and returns a list of user dictionaries
        """
        try:
            with open(self.filename, "r") as json_file:
                data = json.load(json_file)
                users = []
                for user_id, user_info in data.items():
                    user = {
                        'id': user_id,
                        'name': user_info['name'],
                        'username': user_info['username'],  # Include the 'username' key
                        'password': user_info['password'],
                        'movies': user_info['movies']
                    }
                    users.append(user)
                return users
        except IOError as e:
            # Handle the IOError exception
            # ...
            return []


    def add_user(self, username, password):
        """ Checks if the username already exists. Otherwise, generates a unique user ID,
         and adds the user's information
         """
        try:
            with open(self.filename, "r+") as json_file:
                data = json.load(json_file)
                user_ids = list(data.keys())
                new_user_id = str(int(max(user_ids)) + 1) if user_ids else '1'
                for user_info in data.values():
                    if user_info.get('username') == username:
                        return f"Username '{username}' already exists. Please choose a different username."
                data[new_user_id] = {
                    'name': username,
                    'username': username,
                    'password': password,
                    'movies': {}
                }
                json_file.seek(0)
                json.dump(data, json_file, indent=4)
                json_file.truncate()
                return f"User '{username}' added successfully with ID {new_user_id}."
        except IOError as e:
            return f"An error occurred while adding a user"

    def add_movie(self, user_id, movie_name):
        """Adds a new movie to a user's movie list.
        It uses the OMDB API to fetch additional movie information based on the movie name,
        checks if the movie exists in the API response,
        adds the movie information to the user's movies."""
        try:
            api_url = f"http://www.omdbapi.com/?apikey=4bf81bd7&t&t={movie_name}"
            response = requests.get(api_url)
            movie_data = response.json()

            if movie_data.get("Response") != "True":
                return f"Movie '{movie_name}' not found in OMDB data."

            movie = {
                'name': movie_name,
                'director': movie_data.get("Director"),
                'year': movie_data.get("Year"),
                'rating': movie_data.get("imdbRating"),
                'poster': movie_data.get("Poster")
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

                    return f"Movie '{movie_name}' added for user {user_info['name']} successfully."

            return f"User with {user_info['name']} not found."
        except requests.RequestException as e:
            # Handle the RequestException
            # ...
            return f"An error occurred while adding the movie."

    def update_movie(self, user_id, movie_id, director, year, rating):
        """Updates the information of movie for user in the JSON file.
        Retrieves the user and movie information and updates provided fields"""
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

                    return f"Movie not found for user '{user_info['name']}'."

                return f"User '{user_info['name']}' not found."
        except IOError as e:
            # Handle the IOError exception
            # ...
            return f"An error occurred while updating the movie."

    def delete_movie(self, user_id, movie_id):
        """Deletes movie from user's movie list in the JSON file.
         Retrieves the user and movie information, deletes the movie from the user's movies"""
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
                        return f"Movie '{movie['name']}' deleted for user '{user_info['name']}' successfully."
                    return f"Movie not found for user '{user_info['name']}'."
                return f"User '{user_info['name']}' not found."
        except IOError as e:
            # Handle the IOError exception
            # ...
            return f"An error occurred while deleting the movie."

    def get_user(self, user_id):
        """Gets the information of a user from the JSON file based on the user ID. """
        try:
            user_id = str(user_id)

            with open(self.filename, "r") as json_file:
                data = json.load(json_file)
                return data.get(user_id)
        except IOError as e:
            # Handle the IOError exception
            # ...
            return None

    def get_user_by_username(self, username):
        """Gets the information of user from the JSON file based on the username. """
        try:
            with open(self.filename, "r") as json_file:
                data = json.load(json_file)
                for user_id, user_info in data.items():
                    if user_info.get('username') == username:
                        return {'id': user_id, **user_info}
        except IOError as e:
            # Handle the IOError exception
            # ...
            return None

    def get_movie(self, user_id, movie_id):
        """Gets the information of  movie from a user's movie list in the JSON file. """
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



