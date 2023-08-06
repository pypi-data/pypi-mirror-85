#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from fir3base.v1.classes.config import *

# the firebase class.
class Firebase(object):
	def __init__(self, credentials=None):
		
		# initialize firestore.
		# (in classes.config)
		cred = credentials.Certificate(credentials) # must still be edited through env variables.
		firebase_admin.initialize_app(cred)
		self.db = firestore.client()

		#
	# system functions.
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

# initialized objects.
firebase = Firebase()
