import sqlite3 as sql
from flask import Flask,render_template,flash, redirect,url_for,session,logging,request

app = Flask(__name__)

@app.route('/')
def index():
	return render_template("index.html")

@app.route('/register', methods=['POST','GET'])
def register():
	if request.method == 'POST':
		try:
			email = request.form['email']
			username = request.form['username']
			password = request.form['password']
			nohp = request.form['nohp']
			with sql.connect('coba.db') as con:
				cur = con.cursor()
				cur.execute("INSERT INTO users (email,username,password,noHP) VALUES(?,?,?,?)", (email,username,password,nohp))
				con.commit()
				con.close()
				# msg = "Record successfully added"
		except:
			con.rollback()
			# msg = "Error in insert operation"

		finally:
			return render_template("index.html")
	return render_template("register.html")


@app.route('/login', methods=['POST','GET'])
def login():
	salah ='Invalid Username/Password'
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		with sql.connect('coba.db') as con:
			cur = con.cursor()
			usernamedb = cur.execute("SELECT * FROM users WHERE username = ? and password = ?", (username,password)).fetchall()
			# passworddb = cur.execute("SELECT password FROM users WHERE password = ?",password).fetchone()

			if len(usernamedb)==0:
				return render_template('login.html', error = salah)
			else:
				return render_template('hasil.html', username=username)
				#return redirect(url_for('login'))
	else:
		return render_template('login.html')


@app.route('/display', methods=['GET','POST'])
def display():
	global username
	
	username = request.args.get('username')
	with sql.connect('coba.db') as con:
		# con.row_factory = sql.Row
		curs = con.cursor()
		curs.execute("PRAGMA busy_timeout = 30000")
		if request.method == 'GET':
			row = curs.execute("SELECT email,username,noHP FROM users WHERE username = ?", [username])
			return render_template('update.html',rows= row,username=username)
		con.commit()
		curs.close()
	with sql.connect('coba.db') as con:
		curs = con.cursor()
		curs.execute("PRAGMA busy_timeout = 30000")
		if request.method == 'POST':
			# user = request.args.get('username')
	
			emailBaru = request.form['email']
			usernameBaru = request.form['nama']
			noHPbaru = request.form['nohp']
			user = request.form['username']
			if emailBaru == "" and noHPbaru == "":
				error = 'E-Mail dan No HP Tidak Boleh Kosong, Anda boleh Mengisi sesuai dengan E-Mail dan No HP anda sebelumnya'
				return render_template('update.html', error=error)
			if emailBaru == "":
				error = 'E-Mail Tidak Boleh Kosong, Anda boleh Mengisi sesuai dengan E-Mail anda sebelumnya'
				return render_template('update.html', error=error)
			if noHPbaru == "":
				error = 'No HP Tidak Boleh Kosong, Anda boleh Mengisi sesuai dengan No HP anda sebelumnya'
				return render_template('update.html', error=error)


			curs.execute('UPDATE users SET email = ?, username = ?, noHP = ? WHERE username = ?',(emailBaru,usernameBaru,noHPbaru,user))
			con.commit()
			curs.close()
			error = 'successfully change password'
			return render_template('update.html', error=error)
		else:
			error = 'Fail to change Password'
			return render_template('update.html', error=error)




@app.route('/change', methods=['GET', 'POST'])
def change():
	global username
	
	username = request.args.get('username')
	with sql.connect('coba.db') as con:
		curs = con.cursor()
		curs.execute("PRAGMA busy_timeout = 30000")
		if request.method == 'GET':
			# passLama = cur.execute("SELECT password FROM users WHERE username = ?",[username])
			return render_template('changePassword.html',username=username)
		if request.method == 'POST':
			# user = request.args.get('username')
	
			passBaru = request.form['passBaru']
			passBaruValidate = request.form['passBaruValidate']
			user = request.form['user']
			if passBaru == passBaruValidate:
				curs.execute('UPDATE users SET password = ? WHERE username = ?',(passBaru,user))
				con.commit()
				curs.close()
				error = 'successfully change password'
				return render_template('changePassword.html', error=error)
			else:
				error = 'Fail to change Password'
				return render_template('changePassword.html', error=error)
				

if __name__ == '__main__':
	app.secret_key = 'super secret key'
	app.config['SESSION_TYPE'] = 'filesystem'
	# sess.init_app(app)
	app.run(host='127.0.0.1', debug=True, threaded=True)
	