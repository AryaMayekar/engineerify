from flask import Flask,render_template, redirect, url_for,flash, session, make_response,request, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired, Email, ValidationError
from flask_mysqldb import MySQL

app= Flask(__name__)

#MySQL Configuration 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'p_engineerify'
app.secret_key = 'your_secret_key_here'

mysql = MySQL(app)

@app.route('/')
def home():
  print("homepage")
  
#   if 'user_id' not in session:
#     flash("Login First")
#     return redirect(url_for('login'))
  if 'user_id' in session:
       user_id = session.get('user_id')

       cursor = mysql.connection.cursor()
       cursor.execute("SELECT * FROM users WHERE id=%s",(user_id,))
       user = cursor.fetchone()
       cursor.close()

       if user:
          response = make_response(render_template('home.html', user=user))
          response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
          response.headers['Pragma'] = 'no-cache'
          response.headers['Expires'] = '0'
          return response
  return render_template('home.html')

#this class checks if the infut by the user is valid or not
class RegisterForm(FlaskForm):
  name = StringField(validators=[DataRequired()])
  email = StringField(validators=[DataRequired()])
  password = StringField(validators=[DataRequired()])
  submit = SubmitField("Sign Up")

  def validate_email(self,field):
     cursor = mysql.connection.cursor()
     cursor.execute("SELECT * FROM users where email=%s",(field.data,))
     user= cursor.fetchone()
     cursor.close()
     if user:
        raise ValidationError('Email Already Taken,Please Log In ')

@app.route('/signup', methods={'GET','POST'})
def signup():
    form = RegisterForm()
    #calls the RegisterForm class and checks if the data is valid and if it is valid then only it will store the data in the variables
    if form.validate_on_submit():
      name = form.name.data
      email = form.email.data
      password = form.password.data
      # store data in database
      cursor = mysql.connection.cursor()
      cursor.execute("INSERT INTO users (name,email,password) VALUES (%s,%s,%s)",(name,email,password))
      mysql.connection.commit()
    
      cursor.close()
      return redirect(url_for('login'))

    return render_template('signup.html', form=form)

class LoginForm(FlaskForm):
  email = StringField(validators=[DataRequired()])
  password = PasswordField(validators=[DataRequired()])
  submit = SubmitField("Log in")

@app.route('/login', methods={'GET','POST'})
def login():
  form = LoginForm()
  #calls the RegisterForm class and checks if the data is valid and if it is valid then only it will store the data in the variables
  if form.validate_on_submit():
    uemail = form.email.data
    upassword = form.password.data
    
    # store data in database
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id, password FROM users WHERE email = %s",(uemail,))
    user = cursor.fetchone()
    cursor.close()
    
    if user and upassword == user[1]:
     session['user_id'] = user[0]
     return redirect(url_for ('home'))
    else:
     flash("Login failed. Please check your email and password")
     return redirect(url_for ('login'))
          
  return render_template('login.html',form=form)

@app.route('/logout')
def logout():
   session.pop('user_id',None)
   flash("You have been logged out successfully")
  
   return redirect(url_for('home'))

@app.route('/contactus')
def contactus():
    if 'user_id' in session:
       user_id = session.get('user_id')

       cursor = mysql.connection.cursor()
       cursor.execute("SELECT * FROM users WHERE id=%s",(user_id,))
       user = cursor.fetchone()
       cursor.close()

       if user:
          response = make_response(render_template('contact.html', user=user))
          response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
          response.headers['Pragma'] = 'no-cache'
          response.headers['Expires'] = '0'
          return response
    return render_template('contact.html')


if __name__ == '__main__':
    app.run(debug=True)    