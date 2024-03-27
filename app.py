from flask import *
import pymysql

app = Flask(__name__)

mydb = pymysql.connect(
	host="localhost",
	user="root",
	password="",
	database="nrcm"
)

cursor = mydb.cursor()
is_login = False

userId = ""
rollNumber = ""
userRole = ""


@app.route("/", methods=["GET","POST"])
def login():
	error = ""
	if request.method == "POST":
		roll = request.form['username']
		cursor.execute("SELECT * FROM users WHERE roll_number=%s",(roll,))
		data = cursor.fetchone()
		
		if data == None:
			error = "Invalid User"
		else:
			global is_login
			global userId
			global rollNumber
			global userRole


			is_login = True
			userId = data[0]
			rollNumber = data[2]
			userRole = data[6]

			return redirect("dashboard")
	return render_template("index.html", data=error)


@app.route("/dashboard")
def dashboardPage():
	if is_login:
		return render_template("dashboard.html")
	else:
		return redirect("/")

@app.route("/regform", methods=["GET","POST"])
def register():
	return render_template('index.html')


@app.route("/registration", methods=["GET","POST"])
def reg():
	msg=""
	if request.method == "POST":
		uname = request.form['username']
		roll = request.form['roll_number']
		email = request.form['email']
		mobile = request.form['mobile']
		passwd = request.form['pwd']

		try:
			cursor.execute("INSERT INTO users SET username=%s, roll_number=%s, email=%s, mobile=%s, password=%s",(uname, roll, email, mobile, passwd))
			mydb.commit()
			msg=1
		except:
			msg=0	
	return render_template("form.html", msg=msg)

@app.route("/users")
def usersList():
	cursor.execute("SELECT * FROM users")

	data = cursor.fetchall()
	return render_template("users.html", users=data)



@app.route("/myInfo")
def details():
	if is_login:
		cursor.execute("SELECT * FROM users WHERE roll_number=%s",(rollNumber,))
		userData = cursor.fetchone()
		return render_template("information.html", data=userData)
	else:
		return redirect("/")




@app.route("/editInfo", methods=["GET","POST"])
def editData():
	userId = request.args.get('id')

	if request.method == "POST":
		username = request.form['username']

		email = request.form['email']

		try:
			cursor.execute("UPDATE users SET username=%s,email=%s WHERE id=%s", (username,email,userId,))
			mydb.commit
			return redirect("/users")
		except:
			return redirect("/users")

	cursor.execute("SELECT * FROM users WHERE id=%s",(userId,))
	userData1 = cursor.fetchone()
	return render_template("edit.html", userData=userData1)



@app.route("/delUser")
def deleteUser():
	userId = request.args.get('delId')
	try:
		cursor.execute("DELETE FROM users WHERE id=%s",(userId,))
		mydb.commit()
		return redirect("/users")
	except EXCEPTION as e:
		print(str(e))
		return redirect('/users')


if __name__ == "__main__":
	app.run(debug=True)