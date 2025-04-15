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
app.config['MYSQL_DB'] = 'mainlogindatabase'
app.secret_key = 'your_secret_key_here'

mysql = MySQL(app)

@app.route('/')
def home():
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


@app.route('/exploreenginerring')
def exploreenginerring():
   
   if 'user_id' in session:
       user_id = session.get('user_id')

       cursor = mysql.connection.cursor()
       cursor.execute("SELECT * FROM users WHERE id=%s",(user_id,))
       user = cursor.fetchone()
       cursor.close()
       
       if user:
        response = make_response(render_template('exploreenginerrify.html', user=user))
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response
   
   return render_template('exploreenginerrify.html')

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

@app.route('/explore')
def explore():
   if 'user_id' in session:
       user_id = session.get('user_id')

       cursor = mysql.connection.cursor()
       cursor.execute("SELECT * FROM users WHERE id=%s",(user_id,))
       user = cursor.fetchone()
       cursor.close()

       if user:
          response = make_response(render_template('explore.html', user=user))
          response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
          response.headers['Pragma'] = 'no-cache'
          response.headers['Expires'] = '0'
          return response
   return render_template('explore.html')

@app.route('/quizinstructions')
def quizinstructions():
   if 'user_id' not in session:
    flash("Login First")
    return redirect(url_for('login'))
   else:
    return render_template('quizinstruction.html')

@app.route('/GKquiz')
def GKquiz():
   
   if 'user_id' not in session:
    flash("Login First")
    return redirect(url_for('login'))
   
   if 'user_id' in session:
       user_id = session.get('user_id')
       cursor = mysql.connection.cursor()
       cursor.execute("SELECT * FROM users WHERE id=%s",(user_id,))
       cursor.close()
     
   return render_template(('gkquiz.html'))

@app.route('/save_score', methods={'GET','POST'})
def save_score():
    
    user_id = session.get('user_id')

    if 'user_id' in session:   
       try:
        data = request.get_json()
        score = data.get('intValue') 

        if not isinstance(score, int):
            return jsonify({'error': 'Invalid input; must be an integer'}), 400
       
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE users SET ceet_points = %s WHERE id = %s",(score,user_id))
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Data inserted successfully'})
       except Exception as e:
         return jsonify({'error': str(e)}), 500
    else:
     
     return redirect(url_for ('login'))

@app.route('/quizinstructionsjee')
def quizinstructionsjee():
   if 'user_id' not in session:
    flash("Login First")
    return redirect(url_for('login'))
   else:
    return render_template('quizinstruction-jee.html')

@app.route('/jeequiz')
def jee_quiz():
   
   if 'user_id' not in session:
    flash("Login First")
    return redirect(url_for('login'))
   
   if 'user_id' in session:
       user_id = session.get('user_id')
       cursor = mysql.connection.cursor()
       cursor.execute("SELECT * FROM users WHERE id=%s",(user_id,))
       cursor.close()
     
   return render_template(('gkquiz-jee.html'))

@app.route('/save_score_jee', methods={'GET','POST'})
def save_score_jee():
    
    user_id = session.get('user_id')

    if 'user_id' in session:   
       try:
        data = request.get_json()
        score = data.get('intValue') 

        if not isinstance(score, int):
            return jsonify({'error': 'Invalid input; must be an integer'}), 400
       
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE users SET jee_points = %s WHERE id = %s",(score,user_id))
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Data inserted successfully'})
       except Exception as e:
         return jsonify({'error': str(e)}), 500
    else:
     
     return redirect(url_for ('login'))
    
@app.route('/quizinstructionsbitsat')
def quizinstructionsbitsat():
   if 'user_id' not in session:
    flash("Login First")
    return redirect(url_for('login'))
   else:
    return render_template('quizinstruction-bitsat.html')

@app.route('/bitsatquiz')
def bitsat_quiz():
   
   if 'user_id' not in session:
    flash("Login First")
    return redirect(url_for('login'))
   
   if 'user_id' in session:
       user_id = session.get('user_id')
       cursor = mysql.connection.cursor()
       cursor.execute("SELECT * FROM users WHERE id=%s",(user_id,))
       cursor.close()
     
   return render_template(('gkquiz-bitsat.html'))

@app.route('/save_score_bitsat', methods={'GET','POST'})
def save_score_bitsat():
    
    user_id = session.get('user_id')

    if 'user_id' in session:   
       try:
        data = request.get_json()
        score = data.get('intValue') 

        if not isinstance(score, int):
            return jsonify({'error': 'Invalid input; must be an integer'}), 400
       
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE users SET bitsat_points = %s WHERE id = %s",(score,user_id))
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Data inserted successfully'})
       except Exception as e:
         return jsonify({'error': str(e)}), 500
    else:
     
     return redirect(url_for ('login'))


@app.route('/leaderboard', methods=['GET'])
def leaderboard():
    if 'user_id' not in session:
     flash("Login First")
     return redirect(url_for('login'))
    
    if 'user_id' in session:
       user_id = session.get('user_id')
       cursor = mysql.connection.cursor()
       cursor.execute("SELECT * FROM users WHERE id=%s",(user_id,))
       user = cursor.fetchone()
       cursor.close()
       if user :  
         cursor = mysql.connection.cursor()
         
         try:
           # Execute the query to fetch leaderboard data, sorted by points
           cursor.execute("""
            SELECT ROW_NUMBER() OVER (ORDER BY ceet_points DESC) AS `rank`, id, name, email, ceet_points
            FROM users ;
           """)

           # Fetch the results
           rows = cursor.fetchall()
           

           leaderboard_data = []
           for row in rows:
            leaderboard_data.append({
                'rank': row[0],
                'id': row[1],
                'name': row[2],
                'email': row[3],
                'points': row[4]
            })

           

           if not leaderboard_data:
            response = make_response(render_template('leaderboard.html', leaderboard_data=[], user=user))
            response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
            response.headers['Pragma'] = 'no-cache'
            response.headers['Expires'] = '0'
            return response
           
           response = make_response(render_template('leaderboard.html', leaderboard_data=leaderboard_data, user=user, current_email=user[2]))
           response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
           response.headers['Pragma'] = 'no-cache'
           response.headers['Expires'] = '0'
           return response

         except Exception as e:
          print(f"Error executing query: {e}")
          response = make_response(render_template('leaderboard.html', leaderboard_data=[], user=user,current_email=user[2]))
          response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
          response.headers['Pragma'] = 'no-cache'
          response.headers['Expires'] = '0'
          return response
      
@app.route('/leaderboardjee', methods=['GET'])
def leaderboardjee():
    if 'user_id' not in session:
     flash("Login First")
     return redirect(url_for('login'))
    
    if 'user_id' in session:
       user_id = session.get('user_id')
       cursor = mysql.connection.cursor()
       cursor.execute("SELECT * FROM users WHERE id=%s",(user_id,))
       user = cursor.fetchone()
       cursor.close()
       if user :  
         cursor = mysql.connection.cursor()
         
         try:
           # Execute the query to fetch leaderboard data, sorted by points
           cursor.execute("""
            SELECT ROW_NUMBER() OVER (ORDER BY jee_points DESC) AS `rank`, id, name, email, jee_points
            FROM users ;
           """)

           # Fetch the results
           rows = cursor.fetchall()
           

           leaderboard_data = []
           for row in rows:
            leaderboard_data.append({
                'rank': row[0],
                'id': row[1],
                'name': row[2],
                'email': row[3],
                'points': row[4]
            })

           

           if not leaderboard_data:
            response = make_response(render_template('leaderboardjee.html', leaderboard_data=[], user=user))
            response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
            response.headers['Pragma'] = 'no-cache'
            response.headers['Expires'] = '0'
            return response
           
           response = make_response(render_template('leaderboardjee.html', leaderboard_data=leaderboard_data, user=user, current_email=user[2]))
           response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
           response.headers['Pragma'] = 'no-cache'
           response.headers['Expires'] = '0'
           return response

         except Exception as e:
          print(f"Error executing query: {e}")
          response = make_response(render_template('leaderboardjee.html', leaderboard_data=[], user=user,current_email=user[2]))
          response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
          response.headers['Pragma'] = 'no-cache'
          response.headers['Expires'] = '0'
          return response
         

@app.route('/leaderboardbitsat', methods=['GET'])
def leaderboardbitsat():
    if 'user_id' not in session:
     flash("Login First")
     return redirect(url_for('login'))
    
    if 'user_id' in session:
       user_id = session.get('user_id')
       cursor = mysql.connection.cursor()
       cursor.execute("SELECT * FROM users WHERE id=%s",(user_id,))
       user = cursor.fetchone()
       cursor.close()
       if user :  
         cursor = mysql.connection.cursor()
         
         try:
           # Execute the query to fetch leaderboard data, sorted by points
           cursor.execute("""
            SELECT ROW_NUMBER() OVER (ORDER BY bitsat_points DESC) AS `rank`, id, name, email, bitsat_points
            FROM users ;
           """)

           # Fetch the results
           rows = cursor.fetchall()
           

           leaderboard_data = []
           for row in rows:
            leaderboard_data.append({
                'rank': row[0],
                'id': row[1],
                'name': row[2],
                'email': row[3],
                'points': row[4]
            })

           

           if not leaderboard_data:
            response = make_response(render_template('leaderboardbitsat.html', leaderboard_data=[], user=user))
            response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
            response.headers['Pragma'] = 'no-cache'
            response.headers['Expires'] = '0'
            return response
           
           response = make_response(render_template('leaderboardbitsat.html', leaderboard_data=leaderboard_data, user=user, current_email=user[2]))
           response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
           response.headers['Pragma'] = 'no-cache'
           response.headers['Expires'] = '0'
           return response

         except Exception as e:
          print(f"Error executing query: {e}")
          response = make_response(render_template('leaderboard.html', leaderboard_data=[], user=user,current_email=user[2]))
          response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
          response.headers['Pragma'] = 'no-cache'
          response.headers['Expires'] = '0'
          return response

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

@app.route('/Myprofile')
def myprofile():
   if 'user_id' not in session:
     flash("Login First")
     return redirect(url_for('login'))
   if 'user_id' in session:
       user_id = session.get('user_id')

       cursor = mysql.connection.cursor()
       cursor.execute("SELECT * FROM users WHERE id=%s",(user_id,))
       user = cursor.fetchone()
       cursor.close()

       if user:
          response = make_response(render_template('Myprofile.html', user=user))
          response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
          response.headers['Pragma'] = 'no-cache'
          response.headers['Expires'] = '0'
          return response
   return render_template('Myprofile.html')


class updateForm(FlaskForm):
    name = StringField(validators=[DataRequired()])
    phone_no = StringField()
    country = StringField()
    submit = SubmitField("Update Profile")

@app.route('/editprofile' , methods=['GET','POST'])
def editprofile():
   if 'user_id' not in session:
     flash("Login First")
     return redirect(url_for('login'))
   if 'user_id' in session:
       user_id = session.get('user_id')

       cursor = mysql.connection.cursor()
       cursor.execute("SELECT * FROM users WHERE id=%s",(user_id,))
       user = cursor.fetchone()
       cursor.close()

       form = updateForm()
       if form.validate_on_submit():
         uname = form.name.data
         uphoneno = form.phone_no.data
         ucountry = form.country.data
       
         cursor = mysql.connection.cursor()

         cursor.execute("""
         UPDATE users
         SET name = %s, phone_no = %s, country = %s
         WHERE id = %s
         """, (uname, uphoneno, ucountry, user[0]))
         mysql.connection.commit()
         cursor.close()
         flash("Profile Updated Successfully")
         return redirect(url_for('myprofile'))
       
       if user:
          response = make_response(render_template('editprofile.html', user=user,form=form))
          response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
          response.headers['Pragma'] = 'no-cache'
          response.headers['Expires'] = '0'
          return response

       
   return render_template('editprofile.html',form=form, user=user)




if __name__ == '__main__':
    app.run(debug=True)    