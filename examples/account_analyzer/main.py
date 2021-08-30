from flask import Flask

# __name__ is a build-in variable that refer to the local python file
# that you're working with
app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<h1>World!</h1>"

@app.route("/") # write a python decorator, "/" as the root url of your website
def index():
    return "it's a web app!"

@app.route('/api/users', methods=['POST'])
def register_user():
    dbengine.connection(**dbconnect)
    finduser = users()
    allusers = finduser.find_by('order by id desc')
    newid = newnowid(allusers)
    newpw = request.form.get('password1')
    newemail = request.form.get('email')
    newname = request.form.get('name')
    newuser = users(id=newid, email=newemail, password=newpw, admin=0, name=newname, image="http://www.gravatar.com/avatar/12?d=mm&s=120", created_at=nowdate())
    try:
        newuser.insert()
        dbengine.closeconnection()
        return render_template('register_success.html')
    except Exception:
        print("Exception: register failed")
        dbengine.closeconnection()
        return render_template('register_failed.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=2002, debug=True)
