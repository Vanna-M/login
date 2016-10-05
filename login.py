from flask import Flask, render_template, request
import hashlib, csv

app = Flask(__name__)

@app.route('/')
@app.route('/login')
def loginPage():
    return render_template('login.html')

@app.route('/authenticate', methods=["POST"])
def authenticate():
    #if you need to register
    if request.form['submit'] == "New User? Register":
        return render_template('newUser.html')

    #username and pass
    name = request.form['user']
    passw = hashlib.sha224(request.form['pass']).hexdigest()

    #makes dictionary of csv file
    instream = open('data/users.csv','r')
    userFile = csv.reader(instream)
    users = {rows[0]:rows[1] for rows in userFile}
    instream.close()

    #if user exists
    if name in users:

        #if correct password
        if users[name] == passw:
            return render_template('loginResults.html')
        else:
            return render_template('login.html',msg = 'Incorrect password')
    else:
        return render_template('login.html',msg = 'User does not exist')
    #you have logged in
    return render_template('login.html',msg = "You broke the system. Nice job.")

@app.route('/register', methods=["POST"])
def register():
    username = request.form['user']
    passw = request.form['pass']
    pass2 = request.form['pass2']

    #username taken
    if username in open('data/users.csv','r'):
        return render_template('newUser.html', msg = 'Username taken, try again')
    #passwords much match
    elif passw == pass2:

        instream = open('data/users.csv','a')

        #current users data
        writer = csv.writer(instream)

        #add new user data
        writer.writerow([username,hashlib.sha224(passw).hexdigest()])

        #close file
        instream.close()

        #you registered
        return render_template('login.html', msg = "Success! Log in")
    return render_template('newUser.html', msg = 'Passwords do not match, try again')

if __name__ == '__main__':
    app.debug = True
    app.run()
