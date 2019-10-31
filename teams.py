#! /usr/bin/python3
import cgi
import cgitb
import MySQLdb
import passwords
import json
import os
cgitb.enable()

ip = 'http://54.234.68.237'

conn = MySQLdb.connect(host   = passwords.SQL_HOST,
                        user   = passwords.SQL_USER,
                        passwd = passwords.SQL_PASSWD,
                        db     = "db1")


cursor = conn.cursor()
form = cgi.FieldStorage()




if 'PATH_INFO' in os.environ:
	path = os.environ['PATH_INFO']
else:
	path = ""



if path == "":
	print('Status: 302 Redirect')
	print('Location: {}/cgi-bin/teams/'.format(ip))	

elif path ="/home":
	print("Content-Type: text/html")
	print("Status: 200 OK")
	print()
	print('''<!DOCTYPE html>
	<html lang="en" dir="ltr">
	   <head>
	      <meta charset="utf-8">
	      <title>Home</title>
	   </head>
	   <h1> Home </h1>
	   <body>
	   	<a href="/cgi-bin/view">View teams</a>
	   	<br>
	   	<a href="/cgi-bin/add">Add a new team</a>
	   </body>
	</html>''')

elif path == '/add':
	if 'name' in form and 'chips' in form and 'city' in form:
		name =form['name'].value
		chips = form['chips'].value
		city = form['city'].value

		cursor.execute("INSERT INTO teams(name, city, championships) VALUES (%s,%s,%s)", (name,city,chips))
		new_id = cursor.lastrowid
		
		print('Status: 302 Redirect')
		print('Location: {}/cgi-bin/rest/{}'.format(ip,new_id))
	
	elif 'name' in form or 'chips' in form or 'city' in form:
		print("Content-Type: text/html")
		print("Status: 200 OK")
		print()
		print('''<!DOCTYPE html>
		<html lang="en" dir="ltr">
		   <head>
		      <meta charset="utf-8">
		      <title>Add Team</title>
		   </head>
		   <body>
		      <h1>Add Team</h1>
		      <center> Please fill all fields </center>
		      <form action="%s/cgi-bin/teams/add" method="get">
		         Team Name: <br><input type="text" name="name"><br>
		         City: <br><input type="text" name="city"><br>
		         Number of Championships: <br><input type="text" name="chips"><br>
		         <input type="submit">
		      </form>
		   </body>
		</html>''' % ip)

	else:
		print("Content-Type: text/html")
		print("Status: 200 OK")
		print()
		print('''<!DOCTYPE html>
		<html lang="en" dir="ltr">
		   <head>
		      <meta charset="utf-8">
		      <title>Add Team</title>
		   </head>
		   <body>
		      <h1>Add Team</h1>
		      <form action="%s/cgi-bin/pets/add" method="get">
		         Team Name <input type="text" name="name"><br>
		         City <input type="text" name="city"><br>
		         Number of Championships <input type="text" name="chips"><br>
		         <input type="submit">
		      </form>
		   </body>
		</html>''' % ip)



elif path=='/view':
	cursor.execute("SELECT * FROM teams;")
	results = cursor.fetchall()
	formatted = []
	for i in range(len(results)):
		formatted.append({'id':i[0],'team':i[1],'championships':i[2],'url':ip+'/cgi-bin/teams/'+str(i[0])})
	print('Content-Type: application/json')
	print("Status: 200 OK")
	print()
	print(json.dumps(formatted))


elif path[1:].isnumeric() == True:
	results = cursor.execute('SELECT * FROM teams WHERE id=%s',(path[1:],))
	formatted = []
	for i in range(len(results)):
		formatted.append({'id':i[0],'team':i[1],'championships':i[2],'url':ip+'/cgi-bin/teams/'+str(i[0])})
	print('Content-Type: application/json')
	print("Status: 200 OK")
	print()
	print(json.dumps(formatted))


else:
	print("Content-Type: text/html")
	print("Status: 200 OK")
	print()
	print('''<!DOCTYPE html>
	<html lang="en" dir="ltr">
	   <head>
	      <meta charset="utf-8">
	      <title>Home</title>
	   </head>
	   <body>
	   <center>Invalid path: %s</center>
	   	<a href="/cgi-bin/view">View teams</a>
	   	<br>
	   	<a href="/cgi-bin/add">Add a new team</a>
	   </body>
	</html>''' % (path,))







cursor.close()
con.commit()

