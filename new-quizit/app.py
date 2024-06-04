from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
# we got the secret key using the secrets.token_hex(16) module
app.config['SECRET_KEY'] = 'f650f7404bead892619d1fddec56ce56'

@app.route("/", strict_slashes=False)
@app.route("/home", strict_slashes=False)
def home():
    """Renders the landing pages"""
    return render_template("landing_page.html")

@app.route("/layout", strict_slashes=False)
def layout():
    return render_template('layout.html')

@app.route("/register", methods=['GET', 'POST'], strict_slashes=False)
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('layout'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'], strict_slashes=False)
def login():
    form = LoginForm()
    return render_template('login.html', title='Login', form=form)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)