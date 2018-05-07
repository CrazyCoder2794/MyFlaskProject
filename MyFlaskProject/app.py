from flask import Flask, render_template,request,redirect,session
import MySQLdb
app = Flask(__name__)


@app.route('/')
def index():
	return render_template('index.html')

@app.route('/Aboutus.html')
def Aboutus():
	return render_template('Aboutus.html')


@app.route('/register.html',methods=['GET','POST'])
def register():
	#Config MySQL
	db = MySQLdb.connect("localhost","root","","myflask" )

	if request.method=='POST':
		name=request.form['name']
		user=request.form['username']
		password=request.form['password']
		email=request.form['email']
		cur = db.cursor()
		cur.execute("INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)", (name, email, user, password))
		db.commit()
		cur.close()
		return redirect('/login.html')
	return render_template('register.html')


@app.route('/login.html',methods=['GET','POST'])
def login():
	if request.method=='POST':
		username=request.form["username"]
		password=request.form["password"]
		db = MySQLdb.connect("localhost","root","","myflask" )
		cur = db.cursor()
		if cur.execute("SELECT * FROM users WHERE username=%s and password =%s", [username,password]) > 0:
			session['username']=username
			return redirect('/my_dashboard.html')
		else:
			return redirect('/invalid.html')
	return render_template('/login.html')

@app.route('/my_dashboard.html')
def my_dashboard():
	db = MySQLdb.connect("localhost","root","","myflask" )
	cur = db.cursor()
	if cur.execute("SELECT * FROM todo where username=%s",[session['username']]) > 0:
		tasks=cur.fetchall()
		l=[]
		di={}
		for i in tasks:
			di = {'id': i[0], 'username': i[1], 'task':i[2],'deadline': i[3]}
			l.append(di)
			di={}
		return render_template('/my_dashboard.html',tasks=l)
	else:
		return render_template('/my_dashboard.html')
	db.commit()
	db.close()

	

@app.route('/logout.html')
def logout():
	session.clear()
	return render_template('/logout.html')

@app.route('/invalid.html')
def invalid():
	return render_template("invalid.html")


@app.route('/add_task.html',methods=['GET','POST'])
def add_task():
	#Config MySQL
	db = MySQLdb.connect("localhost","root","","myflask" )

	if request.method=='POST':
		task=request.form['task']
		deadline=request.form['deadline']
		username=session['username']
		cur = db.cursor()
		cur.execute("INSERT INTO todo(username, task, deadline) VALUES(%s, %s, %s)", (username,task,deadline))
		db.commit()
		cur.close()
		return redirect('/my_dashboard.html')
	return render_template('add_task.html')

@app.route('/edit_task/<string:id>',methods=['GET','POST'])
def edit_task(id):
	#Config MySQL
	db = MySQLdb.connect("localhost","root","","myflask" )

	if request.method=='POST':
		task=request.form['task']
		deadline=request.form['deadline']
		cur = db.cursor()
		cur.execute("UPDATE todo SET task=%s, deadline=%s WHERE id=%s", (task,deadline,id))
		db.commit()
		cur.close()
		return redirect('/my_dashboard.html')
	return render_template('/edit_task.html')


@app.route('/delete_task/<string:id>',methods=['GET','POST'])
def delete_task(id):
	#Config MySQL
	db = MySQLdb.connect("localhost","root","","myflask" )

	if request.method=='POST':
		cur = db.cursor()
		cur.execute("DELETE FROM todo WHERE id=%s", [id])
		db.commit()
		cur.close()
		return redirect('/my_dashboard.html')
	return render_template('/delete_task.html')

if __name__=='__main__': 
	app.config['SECRET_KEY'] = 'some secret string here'
	app.run(debug=True)