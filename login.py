from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
@app.route('/login')
def loginPage():
    return render_template('login.html')

@app.route('/authenticate', methods=["POST"])
def authenticate():
    msg = ""
    #I am the only person who can log in
    if (request.form['user'].lower() == 'vanna') & (request.form['pass'] == 'rocks'):
        msg = "Sucessful login!"
    else:
        msg = 'No one loves you'
    return render_template('loginResults.html', result = msg)

if __name__ == '__main__':
    app.debug = True
    app.run()
