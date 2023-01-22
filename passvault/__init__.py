from flask import flash, redirect, render_template, request, session, url_for

from passvault.app import create_app
from passvault.models import User

app = create_app()

@app.route("/")
def index():
    return render_template('index.html', title='PassVault')

@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['login--username']
        password = request.form['login--password']
        user = User.query.filter_by(username=username).first()

        if not user:
            flash('Please check login details and try again','danger')
            return redirect(url_for('login'))
        if user.check_password(password):
            flash('Successfully logged in','success')
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))
        else:
            flash('Incorrect password','fail')
    return render_template('auth/login.html', error='', title='Login')

@app.route('/logout')
def logout():
    session['user_id'] = None
    return redirect('/')

@app.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['register--username']
        password = request.form['register--password']
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            user = User.query.filter_by(username=username).first()
            if user is None:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("login"))
        flash(error)
    return render_template('auth/register.html', error='', title='Register')

@app.errorhandler(404)
def not_found(error):
	app.logger.error('Page not found: %s', (request.path))
	return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
	app.logger.error('Page not found: %s', (request.path))
	return render_template('errors/500.html'), 500

@app.errorhandler(Exception)
def exception_unhandled(e):
	app.logger.error('Unhandled Exception: %s', (e))
	return render_template('errors/500.html'), 500