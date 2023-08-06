#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from fir3base.v1.classes.config import *

# the firebase class.
class Firebase(object):
	def __init__(self, key=None):
		
		# initialize firestore.
		# (in classes.config)
		cred = credentials.Certificate(key) # must still be edited through env variables.
		firebase_admin.initialize_app(cred)
		self.firestore = FireStore()
		self.users = Users()

		#

# the users class.
class Users(object):
	def __init__(self):
		a=1
		#
	def get(self, 
		# define one of the following parameters.
		uid=None,
		email=None,
		phone_number=None,
	):
		user, variable = None, None
		if uid != None:
			user = auth.get_user(uid)
			variable = str(uid)
		elif email != None:
			user = auth.get_user_by_email(email)
			variable = str(email)
		elif phone_number != None:
			user = auth.get_user_by_phone_number(phone_number)
			variable = str(phone_number)
		else:
			return r3sponse.error_response("Invalid usage, define one of the following parameters: [uid, email, phone_number].")

		# check success.
		if user == None: 
			return r3sponse.error_response(f"Failed to retrieve user [{variable}].")
		else:
			return r3sponse.success_response(f"Successfully retrieved user [{variable}].", {"user":user})


		#
	def create(self,
		# required:
		email=None,
		password=None,
		verify_password=None,
		# optionals:
		name=None,
		phone_number=None,
		photo_url=None,
	):

		# check parameters.
		response = r3sponse.check_parameters(empty_value=None, parameters={
			"email":email,
			"password":password,
			"verify_password":verify_password,
		})

		# check password.
		password = str(password)
		verify_password = str(verify_password)
		if len(password) < 8:
			return r3sponse.error_response("The password must contain at least 8 characters.")
		elif password.lower() == password:
			return r3sponse.error_response("The password must regular and capital letters.")
		elif password != verify_password:
			return r3sponse.error_response("Passwords do not match.")

		# create.
		try:
			user = auth.create_user(
			    email=email,
			    email_verified=False,
			    phone_number=phone_number,
			    password=password,
			    display_name=name,
			    photo_url=photo_url,
			    disabled=False)
			success = True
		except Exception as e: 
			success = False
			error = e

		# handle success.
		if success:
			return r3sponse.success_response(f"Successfully created user [{email}].", {
				"user":user,
				"uid":user.uid,
			})
		else:
			return r3sponse.error_response(f"Failed to create user [{email}], error: {error}")

		#
	def update(self,
		# required:
		uid=None,
		# optionals:
		name=None,
		email=None,
		password=None,
		phone_number=None,
		photo_url=None,
		email_verified=None,
	):

		# check parameters.
		response = r3sponse.check_parameters(empty_value=None, parameters={
			"uid":uid,
		})

		# load.
		response = self.get(uid=uid)
		if response["error"] != None: return response
		user = response["user"]

		# set defaults.
		if name == None: name = user.display_name
		if email == None: email = user.email
		if phone_number == None: phone_number = user.phone_number
		if photo_url == None: photo_url = user.photo_url
		if email_verified == None: email_verified = user.email_verified

		# create
		try:
			user = auth.update_user(
				uid,
				email=email,
				phone_number=phone_number,
				email_verified=email_verified,
				password=password,
				display_name=name,
				photo_url=photo_url,
				disabled=False)
			success = True
		except Exception as e: 
			success = False
			error = e

		# handle success.
		if success:
			return r3sponse.success_response(f"Successfully updated user [{uid}].")
		else:
			return r3sponse.error_response(f"Failed to update user [{uid}], error: {error}")

		#
	def delete(self, 
		# the user's uid.
		uid=None,
	):
		try:
			auth.delete(uid)
			success = True
		except Exception as e: 
			success = False
			error = e
		if success:
			return r3sponse.success_response(f"Successfully deleted user [{uid}].")
		else:
			return r3sponse.error_response(f"Failed to delete user [{uid}], error: {error}")
	def iterate(self):
		return auth.list_users().iterate_all()
	def verify_id_token(self, id_token):
		"""
			Javascript:
				firebase.auth().currentUser.getIdToken(/* forceRefresh */ true).then(function(idToken) {
				  // Send token to your backend via HTTPS
				  // ...
				}).catch(function(error) {
				  // Handle error
				});
		"""
		try:
			decoded_token = auth.verify_id_token(id_token)
			uid = decoded_token['uid']
			if uid == None: success = False
			else: success = True
		except Exception as e: 
			success = False
			error = e
		if success:
			return r3sponse.success_response("You are signed in.", {"uid":uid})
		else:
			return r3sponse.error_response(f"You are not signed in, error: {error}")

		#

# the firestore class.
class FireStore(object):
	def __init__(self):
		
		# initialize firestore.
		self.db = firestore.client()

		#
	# system functions.
	def list(self, reference):
		doc = self.__get_doc__(reference)
		try:
			doc = doc.get()
			success = True
		except: success = False
		if not success:
			return r3sponse.error_response(f"Failed to load document [{reference}].")
		if not isinstance(doc, list):
			return r3sponse.error_response(f"Reference [{reference}] leads to a document, not a collection.")
		return r3sponse.success_response(f"Successfully listed the content of collection [{reference}].", {"collection":doc})
	def load(self, reference):
		doc = self.__get_doc__(reference)
		try:
			doc = doc.get()
			success = True
		except: success = False
		if not success:
			return r3sponse.error_response(f"Failed to load document [{reference}].")
		if isinstance(doc, list):
			return r3sponse.error_response(f"Reference [{reference}] leads to a collection, not a document.")
		if not doc.exists:
			return r3sponse.error_response(f"Document [{reference}] does not exist.")
		else:
		    data = doc.to_dict()
		    return r3sponse.success_response(f"Successfully loaded document [{reference}].", {"document":data})
	def save(self, reference, data):
		doc = self.__get_doc__(reference)
		try:
			doc.set(data)
			success = True
		except: success = False
		if success:
			return r3sponse.success_response(f"Successfully saved document [{reference}].")
		else:
			return r3sponse.error_response(f"Failed to save document [{reference}].")
	def delete(self, reference):
		doc = self.__get_doc__(reference)
		try:
			doc.delete()
			success = True
		except: success = False
		if success:
			return r3sponse.success_response(f"Successfully deleted document [{reference}].")
		else:
			return r3sponse.error_response(f"Failed to delete document [{reference}].")
	# system functions.
	def __get_doc__(self, reference):
		reference = reference.replace("//", "/")
		if reference[len(reference)-1] == "/": reference = reference[:-1]
		doc, c = None, 0
		for r in reference.split("/"):
			if doc == None:
				doc = self.db.collection(r)
				c = 1
			else:
				if c == 1:
					doc = doc.document(r)
					c = 0
				else:
					doc = doc.collection(r)
					c = 1
		return doc

		


