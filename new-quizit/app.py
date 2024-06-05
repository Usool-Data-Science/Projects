from flask import Flask, render_template, url_for, flash, redirect, request
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
# we got the secret key using the secrets.token_hex(16) module

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
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'], strict_slashes=False)
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == "ade@gmail.com" and form.password.data == "password":
            flash(f'Login successful!', 'success')
            return redirect(url_for('upload'))
        else:
            flash(f'Login not successful!', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/upload", methods=['GET', 'POST'], strict_slashes=False)
def upload():
    if request.method == "POST":
        file_type = request.content_type
        print(file_type)

    # If the method is post and their is a file in the request body,
    # accept the content and send it back to the front end 
    return render_template("upload.html", title="Upload")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)