from flask import Flask, render_template, request, redirect, url_for
from datamanager.json_data_manager import JSONDataManager

app = Flask(__name__)
data_manager = JSONDataManager('data/movies.json')  # Use the appropriate path to your JSON file

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/users')
def list_users():
    users = data_manager.get_all_users()
    return render_template('users.html', users=users)

@app.route('/users/<int:user_id>')
def list_movies(user_id):
    movies = data_manager.get_user_movies(user_id)
    return render_template('movies.html', movies=movies)

@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        user_name = request.form['user_name']
        message = data_manager.add_user(user_name)
        return render_template('add_user.html', message=message)
    return render_template('add_user.html')

@app.route('/users/<int:user_id>/add_movie', methods=['GET', 'POST'])
def add_movie(user_id):
    if request.method == 'POST':
        movie_name = request.form['movie_name']
        message = data_manager.add_movie(user_id, movie_name)
        return render_template('add_movie.html', user_id=user_id, message=message)
    return render_template('add_movie.html', user_id=user_id)


@app.route('/users/<int:user_id>/update_movie/<int:movie_id>', methods=['GET', 'POST'])
def update_movie(user_id, movie_id):
    if request.method == 'POST':
        director = request.form.get('director')
        year = request.form.get('year')
        rating = request.form.get('rating')

        result = data_manager.update_movie(user_id, movie_id, director, year, rating)
        return result
    else:
        # Retrieve movie information from the database or JSON file
        # Implement your logic here
        movie = data_manager.get_movie(user_id, movie_id)  # Replace with your logic to retrieve movie info

        if movie:
            return render_template('update_movie.html', user_id=user_id, movie_id=movie_id, movie=movie)
        else:
            movie_name = data_manager.get_movie_name(movie_id)  # Replace with your logic to retrieve movie name
            user_name = data_manager.get_user_name(user_id)  # Replace with your logic to retrieve user name
            return f"Movie '{movie_name}' not found for user '{user_name}'."
@app.route('/users/<int:user_id>/delete_movie/<int:movie_id>')
def delete_movie(user_id, movie_id):
    message = data_manager.delete_movie(user_id, movie_id)
    return redirect(url_for('list_movies', user_id=user_id))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
