#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from r3stapi.v1.classes.config import *

# the api object class.
class RestAPI(object):
	"""
	1:	Do not forget to fill the self api keys variables!
		Requires variable [firebase] to be set:
			
			firebase = Firebase(...)
	"""
	def __init__(self,
		# Pass either the firebase credentials or initialzed firebase object.
		# 	the firebase credentials.
		firebase_credentials=None,
		# 	the fir3base.FireBase object (optional).
		firebase=None,
		# Pass the stripe keys.
		# 	the stripe secret key.
		stripe_secret_key=None,
		# 	the stripe publishable key.
		stripe_publishable_key=None,
	):
		"""
		The users will be stored in firestore with the following structure:
			users/
				$uid/
					api_key: null
					membership: $plan_id
					requests: 0
					timestamp: null
					... your additional data ...
		Define your additional user data in the __default_user_data__ variable.
		"""
		self.__default_user_data__ = {
			"api_key":None,
			"membership":"free",
			"requests":0,
			"timestamp":None,
		}

		"""
		The plans.
			the "rate_limit" is total requests per "rate_reset"
			the "rate_reset" is the total days before rate limit reset.
			the "plan_id" is the stripe plan id.
		"""
		self.__plans__ = {
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

		# system variables.
		self.uid_api_keys = {
			"$uid":"$api_key..."
		}

		# stripe.
		if not isinstance(stripe_secret_key, str):
			raise ValueError("Define the parameter [stripe_secret_key].")
		self.stripe_secret_key = stripe_secret_key
		self.stripe_publishable_key = stripe_publishable_key
		self.stripe = stripe
		self.stripe.api_key = stripe_secret_key

		# firebase.
		if not isinstance(firebase, object) and  not isinstance(firebase_credentials, str):
			raise ValueError("Pass the either the firebase credentials (str/dict) or the initialized Firebase object from library fir3base. [from fir3base import FireBase]")
		if isinstance(firebase, object):
			self.firebase = firebase
		else:
			self.firebase = Firebase(firebase_credentials)

		#
	def generate_key(self):
		for attempt in range(101):
			key = Formats.String("").generate(length=68, capitalize=True, digits=True)
			if key not in self.__plans__["developer"]["api_keys"]:
				new = True
				for plan, info in self.__plans__.items():
					if key in info["api_keys"]: 
						new = False 
						break
				if new:
					return r3sponse.success_response("Successfully generated a new unique api key.", {
						"api_key":key
					})
		return r3sponse.error_response("Failed to generate a new unique api key.")
	def identify_key(self, api_key=None):

		# check developer success.
		plan = None
		if str(api_key) in self.__plans__["developer"]["api_keys"]:
			plan = "developer"

		# check api key.
		else:
			for _plan_, info in self.__plans__.items():
				if api_key in info["api_keys"]:
					plan = _plan_
					break

		# get uid.
		response = self.get_uid_by_key(api_key)
		if response["error"] != None: return response
		uid = response["uid"]

		# return success.
		return r3sponse.success_response(f"Successfully identified API Key [{api_key}].", {
			"plan":plan,
			"uid":uid,
		})

		#
	def verify_key(self, api_key=None, plan=None):

		# check developer success.
		try:
			if str(api_key) in self.__plans__["developer"]["api_keys"]:
				return r3sponse.success_response(f"Successfully authorized API Key [{api_key}].") 
		except KeyError: a=1

		# check api key.
		try: 
			if api_key in self.__plans__[plan]["api_keys"]:
				return r3sponse.success_response(f"Successfully authorized API Key [{api_key}].")
			else:
				return r3sponse.error_response(f"API Key [{api_key}] is not authorized.")	
		except KeyError:
			return r3sponse.error_response(f"API Key [{api_key}] is not authorized.")

		#
	def verify_rate_limit(self, 
		# required.
		api_key=None, 
		# optional to increase speed.
		# the uid from the api key.
		uid=None,
		# the plan from the api key.
		plan=None,
	):

		# check info.
		if plan == None or uid == None:
			response = self.identify_key(api_key)
			if response["error"] != None: return response
			plan = response["plan"]
			uid = response["uid"]

		# pro / developer.
		if self.__plans__[plan]["rate_limit"] in [None, False]:
			return r3sponse.success_response("Successfully verified the rate limit.")

		# load data.
		response = firebase.users.load_data(uid)
		if response["error"] != None: return response
		data = response["data"]
		timestamp = response["data"]["timestamp"]

		# check timestamp.
		date = Formats.Date()
		success = False
		if timestamp == None:
			success = True
			data["timestamp"] = date.date
			data["requests"] = 0
		else:
			altered = date.increase(timestamp, days=self.__plans__[plan]["rate_reset"], format="%d-%m-%y")
			#decreased_timestamp = date.from_seconds(decreased)
			if date.compare(altered, date.date, format="%d-%m-%y") in ["present", "past"]:
				success = True
				data["timestamp"] = date.date
				data["requests"] = 0

			# check rate limit.
			if not success and int(data["requests"]) <= self.__plans__[plan]["rate_limit"]: 
				success = True

		# response.
		if success:
			data["requests"] += 1
			response = firebase.users.save_data(uid, data)
			if response["error"] != None: return response
			return r3sponse.success_response("Successfully verified the rate limit.")
		else:
			if plan in ["free"]:
				return r3sponse.error_response("You have exhausted your monthly rate limit. Upgrade your membership to premium or pro for more requests.")
			elif plan in ["premium"]:
				return r3sponse.error_response("You have exhausted your monthly rate limit. Upgrade your membership to pro for unlimited requests.")
			else:
				return r3sponse.error_response("You have exhausted your monthly rate limit.")

		# 
	def get_key_by_uid(self, uid):
		api_key = None
		try:
			api_key = self.uid_api_keys[uid]
		except KeyError:
			api_key == None
		if api_key != None:
			return r3sponse.success_response(f"Successfully found the uid for the specified user [{uid}].", {"api_key":self.uid_api_keys[uid]})
		else:
			return r3sponse.error_response(f"Failed to find the uid for the specified user [{uid}].")
	def get_uid_by_key(self, api_key):
		for uid, _api_key_ in self.uid_api_keys.items():
			if str(_api_key_) == str(api_key):
				return r3sponse.success_response("Successfully found the uid for the specified api key.", {"uid":uid})
		return r3sponse.error_response("Failed to find the uid for the specified api key.")
	def get_subscriptions(self):
		try:
			subscriptions = {}
			for subscription in self.stripe.Subscription.list()['data']:
				
				customer = subscription["customer"]
				email = self.stripe.Customer.retrieve(customer)["email"]					
				#	-	subscription plan summary:
				subscription_plans = subscription['items']['data']
				for subscription_plan in subscription_plans:
					id = subscription_plan['plan']['id']
					try: subscriptions[id]
					except KeyError: subscriptions[id] = {}
					subscriptions[id][email] = {
						"customer_id" : customer,
						"email" : email,
						"subscription_id" : subscription_plan['id'],
						"plan_id" : subscription_plan['plan']['id'],
						"plan_nickname" : subscription_plan['plan']['nickname'],
						"plan_active_status" : subscription_plan['plan']['active'],
					}
			return r3sponse.success_response("Successfully retrieved the subscriptions.", {
				"subscriptions":subscriptions,
			})
		except Exception as e:
			return r3sponse.error_response("Failed to retrieve the subscriptions.")

		#


