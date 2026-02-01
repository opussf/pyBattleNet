import os
import sys
import json
import logging
import urllib
import urllib.request
import urllib.error
import ssl
import base64


class PyBattleNet():
	clientID  = ""
	secret    = ""
	token     = ""
	secretsFile = "~/.bnet_secrets.json"

	def __init__(self, region: str, logger: logging.Logger | None = None) -> None:
		self.logger = logger
		self.__getSecrets()
		if self.clientID is None or self.secret is None:
			self.__logError("CLINETID and BLSECRET need to set in %s." % (self.secretsFile,))
			sys.exit(1)
		# get the access token
		self.region = region
		self.request = urllib.request.Request( "https://oauth.battle.net/token" )
		userpassword = base64.b64encode( (f'{self.clientID}:{self.secret}').encode('ascii') )
		self.request.add_header( "Authorization", "Basic %s" % userpassword.decode('ascii') )
		self.context = ssl._create_unverified_context()
		self.request.add_header( "User-Agent", 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36' )
		data = urllib.parse.urlencode( { 'grant_type': 'client_credentials' } ).encode('utf-8')
		try:
			result = urllib.request.urlopen( self.request, context=self.context, data=data )
			if result.status != 200:
				self.__logError(f"Unexpected status code: {result.status}")
				sys.exit(result.status)
			else:
				tokenJSON = result.read().decode('utf-8')
				self.access_token = json.loads( tokenJSON )['access_token']
		except urllib.error.HTTPError as e:
			# This handles HTTP status codes like 404, 500, etc.
			self.__logError(f"HTTP error: {e.code} - {e.reason}")
			sys.exit(1)
		except urllib.error.URLError as e:
			# This handles connection errors, DNS errors, etc.
			self.__logError(f"URL error: {e.reason}")
			sys.exit(1)
		except Exception as e:
			# Any other unexpected errors
			self.__logError(f"Unexpected error: {e}")
			sys.exit(1)
	def __makeAPIRequest(self, endPoint: str):
		""" This sets self.request """
		url = f'https://{self.region}.api.blizzard.com{endPoint}'
		self.request = urllib.request.Request( url )
		self.request.add_header( "Authorization", "Bearer %s" % self.access_token )
		try:
			result = urllib.request.urlopen( self.request, context=self.context )
			if result.status != 200:
				self.__logError(f"Unexpected status code: {result.status}")
				sys.exit(result.status)
			else:
				return result
		except urllib.error.HTTPError as e:
			# This handles HTTP status codes like 404, 500, etc.
			self.__logError(f"HTTP error: {e.code} - {e.reason}")
		except urllib.error.URLError as e:
			# This handles connection errors, DNS errors, etc.
			self.__logError(f"URL error: {e.reason}")
		except Exception as e:
			# Any other unexpected errors
			self.__logError(f"Unexpected error: {e}")
	def __getSecrets(self):
		secretsFile = os.path.expanduser(self.secretsFile)
		if not os.path.exists(secretsFile):
			self.__logError("Figure out what I want to do here. if no secrets file exists.")
			sys.exit(1)
		with open(os.path.expanduser(self.secretsFile), "r", encoding="utf-8") as f:
			secrets = json.loads(f.read())
		self.clientID = secrets["CLIENTID"]
		self.secret = secrets["BLSECRET"]
	def __printMessage(self, msg: str) -> None:
		print(msg)
	def __logError(self, msg: str) -> None:
		if self.logger:
			self.logger.error(msg)
		else:
			self.__printMessage(msg)

	def getPetIndex(self, local: str="en_US") -> dict | None:
		# https://us.api.blizzard.com/data/wow/pet/index?namespace=static-us&locale=en_US
		result = self.__makeAPIRequest(f'/data/wow/pet/index?namespace=static-{self.region}&locale={local}')
		if result:
			return json.loads(result.read().decode('utf-8'))
	def getTokenIndex(self, local: str="en_US") -> dict | None:
		# https://us.api.blizzard.com/data/wow/token/index?namespace=dynamic-us&locale=en_US
		result = self.__makeAPIRequest(f'/data/wow/token/index?namespace=dynamic-{self.region}&locale={local}')
		if result:
			return json.loads(result.read().decode('utf-8'))

