from flask import Flask, render_template, request
import hashlib, csv

app = Flask(__name__)

#makes dictionary of csv file
instream = open('data/users.csv','r')
userFile = csv.reader(instream)
users = {rows[0]:rows[1] for rows in userFile}
instream.close()

@app.route('/')
@app.route('/login')
def loginPage():
    return render_template('login.html')

@app.route('/authenticate', methods=["POST"])
def authenticate():
    #if you need to register
    if request.form['submit'] == "New User? Register":
        return render_template('newUser.html')

    #declare message
    msg = ""

    #username and pass
    name = request.form['user']
    passw = hashlib.sha224(request.form['pass']).hexdigest()

    #if user exists
    if name in users:
        #if correct password
        if users[name] == passw:
            msg = 'Sucessful login!'
        else:
            msg = 'Incorrect password'
    else:
        return render_template('login.html',specialMessage = 'User does not exist')
    #you have logged in
    return render_template('loginResults.html', result = msg, specialMessage = "")

@app.route('/register', methods=["POST"])
def register():
    user = request.form['user']
    passw = request.form['pass']
    pass2 = request.form['pass2']

    #username taken
    if user in users:
        return render_template('newUser.html', specialMessage = 'Username taken, try again')
    #passwords much match
    if passw == pass2:

        #current users data
        instream = open('data/users.csv','a')
        writer = csv.writer(instream)

        #add new user data
        writer.writerow([user,hashlib.sha224(passw).hexdigest()])

        #close file
        instream.close()

        #you registered
        return render_template('login.html', specialMessage = "Success! Log in")
    return render_template('newUser.html', specialMessage = 'Passwords do not match, try again')

if __name__ == '__main__':
    app.debug = True
    app.run()
