# import Flask, flash, render_template, request, url_for, redirect, jsonify, session from flask
# impost db, User, Condo, Like from models
# LoginForm, SignupForm from forms
# sha256_crypt from passlib.hash
from flask import Flask, flash, render_template, request, url_for, redirect, jsonify, session
from models import db, Users, Condos, Likes
from forms import LoginForm, SignupForm
from passlib.hash import sha256_crypt

from flask_heroku import Heroku

app = Flask(__name__)

app.secret_key = "cscie14a-midterm"

# local postgresql or heroku postgresql 
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Winchester110283@localhost:5432/midterm_db'
heroku = Heroku(app)

db.init_app(app)

# index route
@app.route('/')
@app.route('/index')
# the home page
def index():
	# send number of condos to index for display
	condos = Condos.query.all()
	num_condos = len(condos)
	# index needs to know if the user is logged in or not
	if 'username' in session:
		session_user = Users.query.filter_by(username=session['username']).first()
		return render_template('index.html', title='Home', session_username=session_user.username, num_condos=num_condos)
	else:
		return render_template('index.html', title='Home', num_condos=num_condos)

# signup route
@app.route('/signup', methods=['GET', 'POST'])
# register a new user
def signup():
	# if the user is already logged in, do not go to sign up page
	if 'username' in session:
		return redirect(url_for('index'))
	form = SignupForm()
	# if the method is called after information was submitted, receive the information and insert into the database, if valid
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		repeatPassword = request.form['repeatPassword']

		# the username is unique, so make sure the input does not already exist
		existing_user = Users.query.filter_by(username=username).first()
		if existing_user:
			flash('The username already exists. Please pick another one.')
			return redirect(url_for('signup'))
		# the passwords must match
		if password != repeatPassword:
			flash('The passwords do not match. Please try again.')
			return redirect(url_for('signup'))
		# the information is valid, add to the database with password encrypted
		else:
			user = Users(username=username, password=sha256_crypt.hash(password))
			db.session.add(user)
			db.session.commit()
			flash('Congratulations, you are now a registered user!')
			return redirect(url_for('login'))
	# send to page to receive information from user
	else:
		return render_template('signup.html', title='Signup', form=form)

# login route
@app.route('/login', methods=['GET', 'POST'])
# log in an existing user
def login():
	# if the user is already logged in, do not go to login page
	if 'username' in session:
		return redirect(url_for('index'))

	form = LoginForm()
	# if the method is called after information submitted through the form, receive the information and check if valid
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']

		user = Users.query.filter_by(username=username).first()

		# make sure that the given username exists in the database and that the given password matches the one in the database for this user
		if user is None or not sha256_crypt.verify(password, user.password):
			flash('Invalid username or password')
			return redirect(url_for('login'))
		else:
			session['username'] = username
			return redirect(url_for('index'))
	# send to page to receive information from user
	else:
		return render_template('login.html', title='Login', form=form)

# logout route
@app.route('/logout', methods=['POST'])
# log the user out of the current session
def logout():
	session.clear()
	return redirect(url_for('index'))

# info route
@app.route('/info/<mlsnum>', methods=['GET'])
# show the information for the condo with the given mlsnum
def info(mlsnum):
	info_condo = Condos.query.filter_by(mlsnum=mlsnum).first()

	# make sure that a valid mlsnum is given
	if info_condo is None:
		return redirect(url_for('index'))

	# the info page needs to know if the user is logged in so that the correct information is shown
	if "username" in session:
		session_user = Users.query.filter_by(username=session['username']).first()
		# the info page also needs to know if the user has already liked this condo
		if Likes.query.filter_by(liker=session_user.uid, liked=info_condo.cid).first():
			liked = True
		else:
			liked = False
		# send the user to the info page for this condo
		return render_template('info.html', condo=info_condo, liked=liked, session_username=session_user.username)
	# send the user to the info page for this condo
	return render_template('info.html', condo=info_condo, liked=False)

# like route
@app.route('/like/<mlsnum>', methods=['POST'])
# the user wants to save a specific condo to their favorites
def like(mlsnum):
	# get the information for the user and the condo they want to favorite
	session_user = Users.query.filter_by(username=session['username']).first()
	condo_to_like = Condos.query.filter_by(mlsnum=mlsnum).first()

	# add the new relationship into the likes database
	new_like = Likes(liker=session_user.uid, liked=condo_to_like.cid)
	flash("You've successfully saved this property to Favorites")

	db.session.add(new_like)
	db.session.commit()
	return redirect(url_for('info', mlsnum=mlsnum))

# unlike route
@app.route('/unlike/<mlsnum>/<from_url>', methods=['POST'])
# remove a condo from a user's favorites
def unlike(mlsnum, from_url):
	# get the information for the user and the condo they want to unlike
	session_user = Users.query.filter_by(username=session['username']).first()
	condo_to_unlike = Condos.query.filter_by(mlsnum=mlsnum).first()

	delete_like = Likes.query.filter_by(liker=session_user.uid, liked=condo_to_unlike.cid).first()

	flash("You've successfully deleted this property from Favorites")

	# delete the relationship from the likes database
	db.session.delete(delete_like)
	db.session.commit()
	return redirect(url_for(from_url, mlsnum=mlsnum))

# profile route
@app.route('/profile', methods=['GET'])
# show the user's profile and their favorites
def profile():
	# the profile page needs to have the user logged in
	if "username" in session:
		session_user = Users.query.filter_by(username=session['username']).first()
		# get the list of like relationships involving the current user
		condos_liked = Likes.query.filter_by(liker=session_user.uid).all()
		# turn the list into only the cids for the condos liked
		cids_liked = [l.liked for l in condos_liked]
		# this is the list of condos liked by the user from the condos database
		favorites = Condos.query.filter(Condos.cid.in_(cids_liked)).all()

		# send the user to their profile page
		return render_template('profile.html', session_username=session_user.username, condos=favorites)
	else:
		# there has been a mistake, this page should not be accessed if not logged in, return to index
		return redirect(url_for('index'))	

# load_data route (for D3 vis)
@app.route('/load_data', methods=['GET'])
# load the condo database for use in the javascript files
def load_data():
	condos_json = {'condos': []}
	condos = Condos.query.all()
	for condo in condos:
		condo_info = condo.__dict__
		del condo_info['_sa_instance_state']
		condos_json['condos'].append(condo_info)
	return jsonify(condos_json)

if __name__ == "__main__":
    app.run(debug=True)
