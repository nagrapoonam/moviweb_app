from flask import Flask, render_template, request, redirect, url_for, flash, get_flashed_messages, session
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from datamanager.json_data_manager import JSONDataManager
import requests


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'

login_manager = LoginManager(app)
login_manager.login_view = 'login'


data_manager = JSONDataManager('data/movies.json')


class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def get_id(self):
        return str(self.id)

@login_manager.user_loader
def load_user(user_id):
    user_data = data_manager.get_user(user_id)  # Retrieve user by ID
    if user_data:
        return User(user_id, user_data['username'], user_data['password'])
    return None




@app.route('/')
def home():
    users = data_manager.get_all_users()
    return render_template('index.html', users=users)
    # return render_template('index.html', users=users, url_for_login=lambda user_id: url_for('login', user_id=user_id))



@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        message = data_manager.add_user(username, password)

        if message.startswith('User'):
            flash('Registration successful. Please log in.', 'success')
            return redirect(url_for('login'))

        flash(message, 'error')

    return render_template('register.html')


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('list_movies', user_id=current_user.id))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = data_manager.get_user_by_username(username)

        if user and user['password'] == password:
            login_user(User(user['id'], username, user['password']))
            flash('Login successful.')
            return redirect(url_for('list_movies', user_id=user['id']))

        flash('Invalid username or password.')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('home'))


@app.route('/users/<int:user_id>/list_movies')
@login_required
def list_movies(user_id):
    if current_user.id != str(user_id):
        flash("You do not have permission to access this user's movies.")
        flash("Logout and login back to access this user's movies.")
        return redirect(url_for('home'))

    user = data_manager.get_user(user_id)
    flash_message = request.args.get('flash_message')

    if user:
        movies = user.get('movies', {})
        return render_template('list_movies.html', movies=movies, user_id=user_id, flash_message=flash_message)
    else:
        flash('User not found.')
        return redirect(url_for('home'))

@app.route('/users/<int:user_id>/add_movie', methods=['GET', 'POST'])
@login_required
def add_movie(user_id):
    if request.method == 'POST':
        movie_name = request.form['movie_name']
        message = data_manager.add_movie(user_id, movie_name)
        flash(message)  # Add flash message here
        return redirect(url_for('list_movies', user_id=user_id))

    return render_template('add_movie.html', user_id=user_id)

@app.route('/users/<int:user_id>/update_movie/<int:movie_id>', methods=['GET', 'POST'])
@login_required
def update_movie(user_id, movie_id):
    if request.method == 'POST':
        director = request.form.get('director')
        year = request.form.get('year')
        rating = request.form.get('rating')

        result = data_manager.update_movie(user_id, movie_id, director, year, rating)
        flash(result)  # Add flash message here
        return redirect(url_for('list_movies', user_id=user_id))
    else:
        movie = data_manager.get_movie(user_id, movie_id)
        if movie:
            return render_template('update_movie.html', user_id=user_id, movie_id=movie_id, movie=movie)
        else:
            flash(f"Movie not found for user with ID {user_id}.", 'error')
            return redirect(url_for('list_movies', user_id=user_id))

@app.route('/users/<int:user_id>/delete_movie/<int:movie_id>')
@login_required
def delete_movie(user_id, movie_id):
    message = data_manager.delete_movie(user_id, movie_id)
    flash(message)  # Add flash message here
    return redirect(url_for('list_movies', user_id=user_id))



@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
