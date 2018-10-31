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
def index():
	condos = Condos.query.all()
	if 'username' in session:
		session_user = Users.query.filter_by(username=session['username']).first()
		return render_template('index.html', title='Home', session_username=session_user.username)
	else:
		return render_template('index.html', title='Home', condos=condos)

# signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
	if 'username' in session:
		return redirect(url_for('index'))
	form = SignupForm()
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		repeatPassword = request.form['repeatPassword']

		existing_user = Users.query.filter_by(username=username).first()
		if existing_user:
			flash('The username already exists. Please pick another one.')
			return redirect(url_for('signup'))
		if password != repeatPassword:
			flash('The passwords do not match. Please try again.')
			return redirect(url_for('signup'))
		else:
			user = Users(username=username, password=sha256_crypt.hash(password))
			db.session.add(user)
			db.session.commit()
			flash('Congratulations, you are now a registered user!')
			return redirect(url_for('login'))
	else:
		return render_template('signup.html', title='Signup', form=form)

# login route
@app.route('/login', methods=['GET', 'POST'])
def login():
	if 'username' in session:
		return redirect(url_for('index'))

	form = LoginForm()
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']

		user = Users.query.filter_by(username=username).first()

		if user is None or not sha256_crypt.verify(password, user.password):
			flash('Invalid username or password')
			return redirect(url_for('login'))
		else:
			session['username'] = username
			return redirect(url_for('index'))
	else:
		return render_template('login.html', title='Login', form=form)

# logout route
@app.route('/logout', methods=['POST'])
def logout():
	session.clear()
	return redirect(url_for('index'))

# info route
@app.route('/info/<mlsnum>', methods=['GET'])
def info(mlsnum):
	info_condo = Condos.query.filter_by(mlsnum=mlsnum).first()

	if "username" in session:
		session_user = Users.query.filter_by(username=session['username']).first()
		if Likes.query.filter_by(liker=session_user.uid, liked=info_condo.cid).first():
			liked = True
		else:
			liked = False
		return render_template('info.html', condo=info_condo, liked=liked, session_username=session_user.username)
	return render_template('info.html', condo=info_condo, liked=False)

# like route
@app.route('/like/<mlsnum>', methods=['POST'])
def like(mlsnum):
	session_user = Users.query.filter_by(username=session['username']).first()
	condo_to_like = Condos.query.filter_by(mlsnum=mlsnum).first()
	new_like = Likes(liker=session_user.uid, liked=condo_to_like.cid)
	flash("You've successfully saved this property to Favorites")

	db.session.add(new_like)
	db.session.commit()
	return redirect(url_for('info', mlsnum=mlsnum))

# unlike route
@app.route('/unlike/<mlsnum>', methods=['POST'])
def unlike(mlsnum):
	session_user = Users.query.filter_by(username=session['username']).first()
	condo_to_unlike = Condos.query.filter_by(mlsnum=mlsnum).first()
	delete_like = Likes.query.filter_by(liker=session_user.uid, liked=condo_to_unlike.cid).first()
	flash("You've successfully deleted this property from Favorites")

	db.session.delete(delete_like)
	db.session.commit()
	return redirect(url_for('info', mlsnum=mlsnum))

# profile route
@app.route('/profile', methods=['GET'])
def profile():
	if "username" in session:
		session_user = Users.query.filter_by(username=session['username']).first()
		condos_liked = Likes.query.filter_by(liker=session_user.uid).all()
		cids_liked = [l.liked for l in condos_liked]
		favorites = Condos.query.filter(Condos.cid.in_(cids_liked)).all()

		return render_template('profile.html', session_username=session_user.username, condos=favorites)
	else:
		return redirect(url_for('index'))	

# load_data route (for D3 vis)
@app.route('/load_data', methods=['GET'])
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
