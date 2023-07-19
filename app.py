from flask import Flask, render_template, request, redirect, url_for, flash, get_flashed_messages, session
#Importing classes and functions from the Flask framework, for building web application in Python
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
#Importing classes and functions from the Flask-Login extension, for user authentication and session management functionality.
from datamanager.json_data_manager import JSONDataManager
#implementing the methods
import requests
# importing for making HTTP requests to external resources


app = Flask(__name__)
# Initializing a Flask application instance
app.config['SECRET_KEY'] = 'your_secret_key_here'
#Setting secret key for  encrypting session cookies and secure data

# Creating a LoginManager instance and setting login view for the LoginManager.
login_manager = LoginManager(app)
login_manager.login_view = 'login'


data_manager = JSONDataManager('data/movies.json')
#Createing instance of the JSONDataManager class and initializing with the filename of the JSON data file.


#Representing a user object with attributes and methods.
class User(UserMixin):
    def __init__(self, id, username, password):
        """Constructor method of the User class.Takes the id, username, and password parameters
        and initializes attributes. """
        self.id = id
        self.username = username
        self.password = password

    def get_id(self):
        """returns the string form of the user's ID """
        return str(self.id)

@login_manager.user_loader #decorator registers the load_user
def load_user(user_id):
    """Gets user data from the JSONDataManager instance based on the user ID, creates a User object, and returns it. """
    user_data = data_manager.get_user(user_id)  # Retrieve user by ID
    if user_data:
        return User(user_id, user_data['username'], user_data['password'])
    return None



#route with the home function
@app.route('/')
def home():
    """Gets user's information  and renders the index.html template """
    users = data_manager.get_all_users()
    return render_template('index.html', users=users)



#route with the register function. Accepting both GET and POST HTTP methods.
@app.route('/register', methods=['GET', 'POST'])
def register():
    """Handles the registration form submission,
    adds a new user using the add_user method
    and renders the register.html template. """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        message = data_manager.add_user(username, password)

        if message.startswith('User'):
            flash('Registration successful. Please log in.', 'success')
            return redirect(url_for('login'))

        flash(message, 'error')

    return render_template('register.html')

#route with the login function.Accepts both GET and POST HTTP methods.
@app.route('/login/', methods=['GET', 'POST'])
def login():
    """Handles the login form submission, validates the user's credentials using the get_user_by_username method
     and logs in the user using the login_user function"""
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

@app.route('/logout') #route with the logout function.
@login_required #Logout function can only be accessed by authenticated users.
def logout():
    """Logs out the current user using the logout_user function"""
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('home'))

#route with the list_movies function. It accepts a user ID parameter in the URL.
@app.route('/users/<int:user_id>/list_movies')
@login_required
def list_movies(user_id):
    """Gets the movie list for a specific user using the get_user method
    and renders the list_movies.html template"""
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

#route with the add_movie function. Accepts both GET and POST HTTP methods.
@app.route('/users/<int:user_id>/add_movie', methods=['GET', 'POST'])
@login_required
def add_movie(user_id):
    """Handles the movie addition form submission,
    adds a new movie using the add_movie method
    and renders the add_movie.html template"""
    if request.method == 'POST':
        movie_name = request.form['movie_name']
        message = data_manager.add_movie(user_id, movie_name)
        flash(message)  # Add flash message here
        return redirect(url_for('list_movies', user_id=user_id))

    return render_template('add_movie.html', user_id=user_id)

# route with the update_movie function. Accepts both GET and POST HTTP methods.
@app.route('/users/<int:user_id>/update_movie/<int:movie_id>', methods=['GET', 'POST'])
@login_required
def update_movie(user_id, movie_id):
    """Handles the movie update form submission,
    updates a movie using the update_movie method
    and renders the update_movie.html template. """
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

#route with the delete_movie function
@app.route('/users/<int:user_id>/delete_movie/<int:movie_id>')
@login_required
def delete_movie(user_id, movie_id):
    """deletes a movie using the delete_movie method"""
    message = data_manager.delete_movie(user_id, movie_id)
    flash(message)  # Add flash message here
    return redirect(url_for('list_movies', user_id=user_id))



@app.errorhandler(404)
def page_not_found(e):
    """Error handler for 404 Not Found errors.Renders the 404.html template"""
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    """Error handler for 500 Internal Server Error.Renders the 500.html template. """
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
    # runs the Flask application on the local development server with the specified host, port, and debug mode enabled.