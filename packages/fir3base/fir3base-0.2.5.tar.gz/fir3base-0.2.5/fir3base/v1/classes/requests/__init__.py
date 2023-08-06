#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from fir3base.v1.classes.config import *
from fir3base.v1.classes.firebase import *
from django.http import JsonResponse

# universal variables.
firebase = None

# the users requests.
class users():

	# the sign up request.
	class signup():
		def view(request):

			# get parameters.
			parameters, response = r3sponse.get_request_parameters(request, [
				"email",
				"name",
				"password",
				"verify_password",])
			if response["error"] != None: return JsonResponse(response)

			# check firebase set.
			if firebase == None:
				return r3sponse.error_response("Set the firebase of the requests.users class. [fir3base.requests.users.firebase = your_firebase_object", django=True)

			# make request.
			return firebase.users.create_user(
				name=parameters["name"],
				email=parameters["email"],
				password=parameters["password"],
				verify_password=parameters["verify_password"],
			)
