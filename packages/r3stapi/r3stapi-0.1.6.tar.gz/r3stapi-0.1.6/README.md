# r3stapi
Author(s):  Daan van den Bergh<br>
Copyright:  © 2020 Daan van den Bergh All Rights Reserved<br>
<br>
<br>
<p align="center">
  <img src="https://github.com/vandenberghinc/storage/blob/master/images/logo.png?raw=true" alt="Bergh-Encryption" width="50"/>
</p>

## Installation
	pip3 install r3stapi

## Python Examples.

### Initializing the rest api.
Using the r3stapi.RestAPI object class.
```python

# import the package.
import r3stapi, fir3base

# initialize the firebase object (or pass the credentials to the rest api).
# 	(https://github.com/vandenberghinc/fir3base)
firebase = fir3base.Firebase("/path/to/firebase-credentials.json")

# initialize the restapi class.
restapi = r3stapi.RestAPI(
	# Pass either the firebase credentials or initialzed firebase object.
	# 	the firebase credentials.
	firebase_credentials=None,
	# 	the fir3base.FireBase object (optional).
	firebase=None,
	# Pass the stripe keys.
	# 	the stripe secret key.
	stripe_secret_key=None,
	# 	the stripe publishable key.
	stripe_publishable_key=None,)

```
### Configurating the rest api.
The users will be stored in firestore with the following structure:
```python
	users/
		$uid/
			api_key: null
			membership: $plan_id
			requests: 0
			timestamp: null
			... your additional data ...
```
Define your additional user data.
```python
restapi.__default_user_data__ = {
	"api_key":None,
	"membership":"free",
	"requests":0,
	"timestamp":None,
}
```
Define your plans.

	the "rate_limit" is total requests per "rate_reset"
	the "rate_reset" is the total days before rate limit reset.
	the "plan_id" is the stripe plan id.

```python
restapi.__plans__ = {
	"developer": {
		"plan_id":None,
		"rate_limit":None,
		"rate_reset":None,
		"api_keys":[],
	},
	"free": {
		"plan_id":None,
		"rate_limit":3,
		"rate_reset":1, # in days.
		"api_keys":[],
	},
	"premium": {
		"plan_id":"prod_I41OYB42aGgfNJ",
		"rate_limit":10000,
		"rate_reset":30, # in days.
		"api_keys":[],
	},
	"pro": {
		"plan_id":"prod_IPiu7aUFXgz53f",
		"rate_limit":25000,
		"rate_reset":30, # in days.
		"api_keys":[],
	},
}
```

