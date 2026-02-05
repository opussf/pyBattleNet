import os
import json
import logging
import urllib
import urllib.request
import urllib.error
import ssl
import base64


class PyBattleNet():
	clientID  = None
	secret    = None
	token     = ""
	secretsFile = "~/.bnet_secrets.json"

	def __init__(self, region: str, logger: logging.Logger | None = None,
				clientID: str | None = None, secret: str | None = None) -> None:
		self.logger = logger
		self.region = region
		self.__set_secrets(clientID, secret)
		self.__get_access_token()

	def __make_request(self, data: bytes | None = None):
		try:
			result = urllib.request.urlopen(self.request, context=self.context, data=data)
			if result.status != 200:
				self.__logError(f"Unexpected status code: {result.status}")
				raise RuntimeError(f"HTTP request failed with status code {result.status}")
			else:
				return result
		except urllib.error.HTTPError as e:
			# This handles HTTP status codes like 404, 500, etc.
			self.__logError(f"HTTP error: {e.code} - {e.reason}")
			raise e
		except urllib.error.URLError as e:
			# This handles connection errors, DNS errors, etc.
			self.__logError(f"URL error: {e.reason}")
			raise e
		except Exception as e:
			# Any other unexpected errors
			self.__logError(f"Unexpected error: {e}")
			raise e

	def __get_access_token(self):
		self.request = urllib.request.Request("https://oauth.battle.net/token")
		userpassword = base64.b64encode((f'{self.clientID}:{self.secret}').encode('ascii'))
		self.request.add_header("Authorization", "Basic %s" % (userpassword.decode('ascii'),))
		self.context = ssl._create_unverified_context()
		self.request.add_header("User-Agent",
				'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36')
		data = urllib.parse.urlencode({'grant_type': 'client_credentials'}).encode('utf-8')
		tokenJSON = self.__make_request(data).read().decode('utf-8')
		self.access_token = json.loads(tokenJSON)['access_token']

	def __makeAPIRequest(self, endPoint: str):
		""" This sets self.request """
		url = f'https://{self.region}.api.blizzard.com{endPoint}'
		self.request = urllib.request.Request(url)
		self.request.add_header("Authorization", "Bearer %s" % self.access_token)
		return self.__make_request()

	def __set_secrets(self, clientID: str | None = None, secret: str | None = None):
		""" This sets the required secrets needed to access bnet API services.
		The secrets are attempted to be retrieved in order of:
		passed to object, environment, self.secretsFile
		This is a good place to throw an exception (not exit), if they cannot be set."""
		self.clientID = clientID
		self.secret = secret

		if not self.clientID or not self.secret:
			self.clientID = os.environ.get("CLIENTID")
			self.secret = os.environ.get("BLSECRET")

		if not self.clientID or not self.secret:
			secretsFile = os.path.expanduser(self.secretsFile)
			if os.path.exists(secretsFile):
				with open(os.path.expanduser(self.secretsFile), "r", encoding="utf-8") as f:
					secrets = json.loads(f.read())
				try:
					self.clientID = secrets["CLIENTID"]
					self.secret = secrets["BLSECRET"]
				except KeyError as ke:
					raise EnvironmentError(f"Missing required configuration key: {ke.args[0]}") from ke

		if not self.clientID or not self.secret:
			self.__logError("CLIENTID or BLSECRET are not set.")
			self.__logError(f"Create {secretsFile}, set them in the environment, or pass them to the object.")
			raise EnvironmentError("CLIENTID or BLSECRET are not set")

	def __printMessage(self, msg: str) -> None:
		print(msg)

	def __logError(self, msg: str) -> None:
		if self.logger:
			self.logger.error(msg)
		else:
			self.__printMessage(msg)

	def getPetIndex(self, local: str = "en_US") -> dict | None:
		# https://us.api.blizzard.com/data/wow/pet/index?namespace=static-us&locale=en_US
		result = self.__makeAPIRequest(f'/data/wow/pet/index?namespace=static-{self.region}&locale={local}')
		if result:
			return json.loads(result.read().decode('utf-8'))

	def getTokenIndex(self, local: str = "en_US") -> dict | None:
		# https://us.api.blizzard.com/data/wow/token/index?namespace=dynamic-us&locale=en_US
		result = self.__makeAPIRequest(f'/data/wow/token/index?namespace=dynamic-{self.region}&locale={local}')
		if result:
			return json.loads(result.read().decode('utf-8'))
