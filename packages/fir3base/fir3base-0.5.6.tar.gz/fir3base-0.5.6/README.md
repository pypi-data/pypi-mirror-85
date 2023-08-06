# Fir3base
Author(s):  Daan van den Bergh<br>
Copyright:  © 2020 Daan van den Bergh All Rights Reserved<br>
<br>
<br>
<p align="center">
  <img src="https://github.com/vandenberghinc/storage/blob/master/images/logo.png?raw=true" alt="Bergh-Encryption" width="50"/>
</p>

## Installation
	pip3 install fir3base

## Python Examples.

### The FireBase() object class.
The FireBase() object class.  
```python

# import the package.
from fir3base import Firebase

# initialize firebase.
firebase = Firebase(key="/path/to/credentials.json")

# loading documents.
response = firebase.load("my-collection/my-document")
if response["success"]:
	print(response["document"])

# saving documents.
response = firebase.save("my-collection/my-document", {
	"Hello":"World"
})

# deleting documents.
response = firebase.delete("my-collection/my-document")

# list the documents of a collectoin.
response = firebase.list("my-collection/")

```

### Response Object.
When a function completed successfully, the "success" variable will be "True". When an error has occured the "error" variable will not be "None". The function returnables will also be included in the response.

	{
		"success":False,
		"message":None,
		"error":None,
		"...":"...",
	}