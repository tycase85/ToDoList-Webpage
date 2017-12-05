#!/usr/bin/env python3.6

from flask import Flask, jsonify, abort, request, make_response, session, Response
from flask_restful import reqparse, Resource, Api
from flask_session import Session
import pymysql.cursors
import pymysql
import json
import ldap
import json
from ldap3 import Server, Connection, ALL
import ssl
import cgitb
import cgi
import sys
import settings # Our server and db settings, stored in settings.py

cgitb.enable()

app = Flask(__name__, static_url_path='/static')
api = Api(app)

# Set Server-side session config: Save sessions in the local app directory.
app.secret_key = settings.SECRET_KEY
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_COOKIE_NAME'] = 'todolist'
app.config['SESSION_COOKIE_DOMAIN'] = settings.APP_HOST
Session(app)


class Root(Resource):
	def get(self):
		return app.send_static_file('index.html')
####################################################################################
#
# Error handlers
#
@app.errorhandler(400) # decorators to add to 400 response
def not_found(error):
	return make_response(jsonify( { 'status': 'Bad request' } ), 400)

@app.errorhandler(404) # decorators to add to 404 response
def not_found(error):
	return make_response(jsonify( { 'status': 'Resource not found' } ), 404)


####################################################################################
####################################################################################
#
# Routing: GET and POST using Flask-Session
#
class SignIn(Resource):
	def post(self):
	# Set Session and return Cookie
	#
	# Example curl command:
	# curl -i -H "Content-Type: application/json" -X POST -d '{"username": "'$username'", "password": "'$password'"}'
	#		-c cookie-jar -k https://info3103.cs.unb.ca:52799/signin


		if not request.json:

			abort(400) # bad request
		parser = reqparse.RequestParser()

		try:
			# Check for required attributes in json document, create a dictionary


			parser.add_argument('username', type=str, required=True)
			parser.add_argument('password', type=str, required=True)
			request_params = parser.parse_args()

		except Exception as e:
			print(str(e))
			abort(400) # bad request

		if request_params['username'] in session:

			response = {'status': 'success'}
			responseCode = 200

		else:
			try:
				ldapServer = Server(host=settings.LDAP_HOST)
				ldapConnection = Connection(ldapServer,
					raise_exceptions=True,
					user='uid='+request_params['username']+', ou=People,ou=fcs,o=unb',
					password = request_params['password'])
				ldapConnection.open()
				ldapConnection.start_tls()
				ldapConnection.bind()
				# At this point we have sucessfully authenticated.
				username = request.json['username'];

				session['username'] = request_params['username']
				response = {'status': 'success' }
				responseCode = 201

				dbConnection = pymysql.connect(settings.DB_HOST,
					settings.DB_USER,
					settings.DB_PASSWD,
					settings.DB_DATABASE,
					charset='utf8mb4',
					cursorclass= pymysql.cursors.DictCursor)


				#Check if the user exist in the database
				sql = 'userExist'
				cursor = dbConnection.cursor()
				cursor.callproc(sql,[username])
				rows_count = cursor.rowcount

				if rows_count == 0:
					sqlCall = 'createAUser'
					cursor = dbConnection.cursor()
					cursor.callproc(sqlCall,[username])
					rows = cursor.fetchone()
					dbConnection.commit()


			finally:
				ldapConnection.unbind()
		return make_response(jsonify(response), responseCode)
#
#
	# GET: Check Cookie data with Session data
	# Example curl command:
	# curl -i -H "Content-Type: application/json" -X GET -b cookie-jar -k https://info3103.cs.unb.ca:52799/signin

	def get(self):
		if 'username' in session:
			response = {'status': 'success'}
			responseCode = 200
		else:
			response = {'status': 'fail'}
			responseCode = 403

		return make_response(jsonify(response), responseCode)

#
# DELETE: for logout
#curl -i -H "Content-Type: application/json" -X DELETE -b cookie-jar -k https://info3103.cs.unb.ca:52799/signin
	def delete(self):
		if 'username' in session:
			response = {'status': 'successfully logged out'}
			responseCode = 200
			session.clear() #clear current session
		else:
			response = {'status': 'no session found'}
			responseCode = 404
		return make_response(jsonify(response), responseCode)


####################################################################################



#########################################################################################################################
class Lists(Resource):
	# curl -i -H "Content-Type: application/json" -X GET -b cookie-jar -k https://info3103.cs.unb.ca:52799/lists
###########
	def get(self):

		if 'username' in session:
			try:
				#GET ALL LISTS
				dbConnection = pymysql.connect(settings.DB_HOST,
					settings.DB_USER,
					settings.DB_PASSWD,
					settings.DB_DATABASE,
					charset='utf8mb4',
					cursorclass= pymysql.cursors.DictCursor)

				user = session['username']

				data = [[user]]

				sql = 'getAllLists'
				cursor = dbConnection.cursor()
				cursor.callproc(sql,data) # stored procedure
				rows = cursor.fetchall() # get all the results

				responseCode = 200
			except:
				abort(500) # Nondescript server error
			finally:
				cursor.close()
				dbConnection.close()
		else:
			responseCode = 401
		return make_response(jsonify(rows), responseCode)


# curl -i -H "Content-Type: application/json" -X POST -d '{"listName":"grocery"}' -b cookie-jar -k https://info3103.cs.unb.ca:52799/lists
############
	def post(self):
		if 'username' in session:
			try:
				#POST A NEW LIST
				#Get the list name from request.json['listName']
				dbConnection = pymysql.connect(settings.DB_HOST,
					settings.DB_USER,
					settings.DB_PASSWD,
					settings.DB_DATABASE,
					charset='utf8mb4',
					cursorclass= pymysql.cursors.DictCursor)

				listName = request.json['listName']
				user = session['username']

				data = [[user],[listName]]

				sql = 'createAList'
				cursor = dbConnection.cursor()
				cursor.callproc(sql,data) # stored procedure
				dbConnection.commit()

				response = {'status': 'Successfully posted'}
				responseCode = 200
			except:
				abort(500)

			finally:
				cursor.close()
				dbConnection.close()

		else:
			response = {'status': 'Unauthorized'}
			responseCode = 401
		return make_response(jsonify(response), responseCode)

###################################################################################################################333

class List(Resource):
	# curl -i -H "Content-Type: application/json" -X GET -b cookie-jar -k https://info3103.cs.unb.ca:52799/lists/{1}
###########
	def get(self, listID):
		if 'username' in session:
			try:
				#GET A LIST {listID}
				dbConnection = pymysql.connect(settings.DB_HOST,
					settings.DB_USER,
					settings.DB_PASSWD,
					settings.DB_DATABASE,
					charset='utf8mb4',
					cursorclass= pymysql.cursors.DictCursor)

				listID = [listID]

				data = [[listID]]

				sql = 'getAList'
				cursor = dbConnection.cursor()
				cursor.callproc(sql,data) # stored procedure
				rows = cursor.fetchall() # get all the results

				responseCode = 200
			except:
				abort(500)

			finally:
				cursor.close()
				dbConnection.close()
		else:
			response = {'status': 'Unauthorized'}
			responseCode = 401
		return make_response(jsonify(rows), responseCode)


	# curl -i -H "Content-Type: application/json" -X POST -d '{"itemName":"apple"}' -b cookie-jar -k https://info3103.cs.unb.ca:52799/lists/{1}
############
	def post(self, listID):
		if 'username' in session:
			try:
				#POST A NEW ITEM TO {listID}
				#Get the item name from request.json['itemName']
				dbConnection = pymysql.connect(settings.DB_HOST,
					settings.DB_USER,
					settings.DB_PASSWD,
					settings.DB_DATABASE,
					charset='utf8mb4',
					cursorclass= pymysql.cursors.DictCursor)

				itemName = request.json['itemName']
				data = [[listID],[itemName]]

				sql = 'createAItem'
				cursor = dbConnection.cursor()
				cursor.callproc(sql,data) # stored procedure
				dbConnection.commit()

				response = {'status': 'Successfully posted'}
				responseCode = 200


			except:
				abort(500)

			finally:
				cursor.close()
				dbConnection.close()
		else:
			response = {'status': 'Unauthorized'}
			responseCode = 401

		return make_response(jsonify(response), responseCode)

###########
	# def put(self, listID):
	# 	if 'username' in session:
	# 		try:
	# 			#UPDATE A LIST {listID}
	# 			#Get the new list name from request.json['...']
    #
	# 		except:
	# 			abort(500)
	# 	else:
	# 		response = {'status': 'Unauthorized'}
	# 		responseCode = 401
	# 	return make_response(jsonify(response), responseCode)

##############
	def delete(self, listID):
	#	curl -i -H "Content-Type: application/json" -X DELETE -b cookie-jar -k https://info3103.cs.unb.ca:52799/lists/{1}
		if 'username' in session:
			try:
				#DELETE A LIST {listID}
				dbConnection = pymysql.connect(settings.DB_HOST,
					settings.DB_USER,
					settings.DB_PASSWD,
					settings.DB_DATABASE,
					charset='utf8mb4',
					cursorclass= pymysql.cursors.DictCursor)

				data = [[listID]]

				sql = 'deleteList'
				cursor = dbConnection.cursor()
				cursor.callproc(sql,data) # stored procedure
				dbConnection.commit()

				response = {'status': 'Successfuly deleted list'}
				responseCode = 200
			except:
				abort(500)

			finally:
				cursor.close()
				dbConnection.close()
		else:
			response = {'status': 'Unauthorized'}
			responseCode = 401
		return make_response(jsonify(response), responseCode)

#######################################################################################################

class Item(Resource):
##############
	def delete(self,listID,ItemID): #DELETE {itemName}
	#	curl -i -H "Content-Type: application/json" -X DELETE -b cookie-jar -k https://info3103.cs.unb.ca:52799/lists/{1}/{3}
		if 'username' in session:
			try:
				#DELETE AN ITEM {itemName}
				dbConnection = pymysql.connect(settings.DB_HOST,
					settings.DB_USER,
					settings.DB_PASSWD,
					settings.DB_DATABASE,
					charset='utf8mb4',
					cursorclass= pymysql.cursors.DictCursor)

				data = [[listID],[ItemID]]

				sql = 'deleteItem'
				cursor = dbConnection.cursor()
				cursor.callproc(sql,data) # stored procedure
				dbConnection.commit()

				response = {'status': 'Successfuly deleted item'}
				responseCode = 200
			except:
				abort(500)

			finally:
				cursor.close()
				dbConnection.close()
		else:
			response = {'status': 'Unauthorized'}
			responseCode = 401
		return make_response(jsonify(response), responseCode)

########################################################################################################
#
# Identify/create endpoints and endpoint objects
#
api = Api(app)
api.add_resource(Root, '/')
api.add_resource(SignIn, '/signin')

#Get all lists
#Post a single list
api.add_resource(Lists, '/lists') #GET, POST

#Get a single list
#Post an item
#Update list name
#Delete a list
api.add_resource(List, '/lists/<int:listID>') #GET, POST, PUT, DELETE

#Delete an item
api.add_resource(Item, '/lists/<int:listID>/<int:ItemID>') #DELETE

####################################################################################

# xxxxx= last 5 digits of your studentid. If xxxxx > 65535, subtract 30000
if __name__ == "__main__":
	#
	# You need to generate your own certificates. To do this:
	#	1. cd to the directory of this app
	#	2. run the makeCert.sh script and answer the questions.
	#	   It will by default generate the files with the same names specified below.
	#
	context = ('cert.pem', 'key.pem') # Identify the certificates you've generated.
	app.run(
		host=settings.APP_HOST,
		port=settings.APP_PORT,
		ssl_context=context,
		debug=settings.APP_DEBUG)
