import pytest
from unittest.mock import patch, mock_open, Mock
import urllib

import pybattlenet


class TestBuiltInFunctions:
	"""Test cases involving base functionality"""

	@patch('builtins.open', new_callable=mock_open, read_data='')
	@patch('os.path.exists')
	@patch('os.path.expanduser')
	def test_missing_secretsfile_exits(self, mock_expanduser, mock_exists, mock_file):
		""" Test that a missing secrets file exits the object """
		# setup mocks
		mock_expanduser.return_value = '/home/testuser/.file.json'
		mock_exists.return_value = False

		with pytest.raises(SystemExit) as exc_info:
			pybattlenet.PyBattleNet(region="us")

		# Verify it exited with code 1
		assert exc_info.value.code == 1

	@patch('os.path.exists')
	@patch('os.path.expanduser')
	def test_missing_passedsecret_exits(self, mock_expanduser, mock_exists):
		# setup mocks
		mock_expanduser.return_value = '/home/testuser/.file.json'
		mock_exists.return_value = False

		with pytest.raises(SystemExit) as exc_info:
			pybattlenet.PyBattleNet(region="us", clientID="Frank")
		assert exc_info.value.code == 1

	@patch('os.path.exists')
	@patch('os.path.expanduser')
	def test_missing_passedclinetID_exits(self, mock_expanduser, mock_exists):
		# setup mocks
		mock_expanduser.return_value = '/home/testuser/.file.json'
		mock_exists.return_value = False

		with pytest.raises(SystemExit) as exc_info:
			pybattlenet.PyBattleNet(region="us", secret="Frank")
		assert exc_info.value.code == 1

	@patch('urllib.request.urlopen')
	@patch('builtins.open', new_callable=mock_open, read_data='{"CLIENTID": "Frank", "BLSECRET": "Shhhh"}')
	@patch('os.path.exists')
	@patch('os.path.expanduser')
	def test_success_sets_access_token_fromFile(self, mock_expanduser, mock_exists, mock_file, mock_urlopen):
		""" Test that a missing secrets file exits the object """
		# setup mocks
		mock_expanduser.return_value = '/home/testuser/.file.json'
		mock_exists.return_value = True

		mock_response = Mock()
		mock_response.read.return_value = b'{"access_token": "t0k3n"}'
		mock_response.status = 200  # This should work

		mock_urlopen.return_value = mock_response

		BN = pybattlenet.PyBattleNet(region="us")
		assert BN.access_token == "t0k3n"

	@patch('urllib.request.urlopen')
	@patch('builtins.open', new_callable=mock_open, read_data='')
	@patch('os.path.exists')
	@patch('os.path.expanduser')
	def test_success_sets_access_token_passed(self, mock_expanduser, mock_exists, mock_file, mock_urlopen):
		""" Test that a missing secrets file exits the object """
		# setup mocks
		mock_expanduser.return_value = '/home/testuser/.file.json'
		mock_exists.return_value = False

		mock_response = Mock()
		mock_response.read.return_value = b'{"access_token": "t0k3n"}'
		mock_response.status = 200  # This should work

		mock_urlopen.return_value = mock_response

		BN = pybattlenet.PyBattleNet(region="us", clientID="Frank", secret="Shhh")
		assert BN.access_token == "t0k3n"

	@patch('urllib.request.urlopen')
	@patch('builtins.open', new_callable=mock_open, read_data='')
	@patch('os.path.exists')
	@patch('os.path.expanduser')
	def test_odd_return_status(self, mock_expanduser, mock_exists, mock_file, mock_urlopen):
		""" Test that a missing secrets file exits the object """
		# setup mocks
		mock_expanduser.return_value = '/home/testuser/.file.json'
		mock_exists.return_value = False

		mock_response = Mock()
		mock_response.read.return_value = b'{"access_token": "t0k3n"}'
		mock_response.status = 207  # This should work

		mock_urlopen.return_value = mock_response

		with pytest.raises(SystemExit) as excinfo:
			pybattlenet.PyBattleNet(region="us", clientID="Frank", secret="Shhh")

		assert excinfo.value.code == 207

	@patch('urllib.request.urlopen')
	@patch('builtins.open', new_callable=mock_open, read_data='')
	@patch('os.path.exists')
	@patch('os.path.expanduser')
	def test_httperror_404_token_passed(self, mock_expanduser, mock_exists, mock_file, mock_urlopen):
		""" Test that a missing secrets file exits the object """
		# setup mocks
		mock_expanduser.return_value = '/home/testuser/.file.json'
		mock_exists.return_value = False

		# create an HTTPError
		http_error = urllib.error.HTTPError(
			url='https://example.com/token',
			code=401,
			msg='Unauthorized',
			hdrs=None,
			fp=None,
		)
		mock_urlopen.side_effect = http_error

		with pytest.raises(SystemExit) as excinfo:
			pybattlenet.PyBattleNet(region="us", clientID="Frank", secret="Shhh")

		assert excinfo.value.code == 1

	@patch('urllib.request.urlopen')
	@patch('builtins.open', new_callable=mock_open, read_data='')
	@patch('os.path.exists')
	@patch('os.path.expanduser')
	def test_urlerror_token_passed(self, mock_expanduser, mock_exists, mock_file, mock_urlopen):
		""" Test that a missing secrets file exits the object """
		# setup mocks
		mock_expanduser.return_value = '/home/testuser/.file.json'
		mock_exists.return_value = False

		# create an URLError
		url_error = urllib.error.URLError("Connection refused")
		mock_urlopen.side_effect = url_error

		with pytest.raises(SystemExit) as excinfo:
			pybattlenet.PyBattleNet(region="us", clientID="Frank", secret="Shhh")

		assert excinfo.value.code == 1

	@patch('urllib.request.urlopen')
	@patch('builtins.open', new_callable=mock_open, read_data='')
	@patch('os.path.exists')
	@patch('os.path.expanduser')
	def test_unknown_exception(self, mock_expanduser, mock_exists, mock_file, mock_urlopen):
		""" Test that a missing secrets file exits the object """
		# setup mocks
		mock_expanduser.return_value = '/home/testuser/.file.json'
		mock_exists.return_value = False

		mock_urlopen.side_effect = Exception("Boom")

		with pytest.raises(SystemExit) as excinfo:
			pybattlenet.PyBattleNet(region="us", clientID="Frank", secret="Shhh")

		assert excinfo.value.code == 1

	@patch('urllib.request.urlopen')
	@patch('builtins.open', new_callable=mock_open, read_data='{"CLIENTID": "Frank", "BLSECRET": "Shhhh"}')
	@patch('os.path.exists')
	@patch('os.path.expanduser')
	def test_success_getPets(self, mock_expanduser, mock_exists, mock_file, mock_urlopen):
		""" Test that a missing secrets file exits the object """
		# setup mocks
		mock_expanduser.return_value = '/home/testuser/.file.json'
		mock_exists.return_value = True

		mock_response = Mock()
		mock_response.read.return_value = b'{"access_token": "t0k3n"}'
		mock_response.status = 200  # This should work

		mock_urlopen.return_value = mock_response

		BN = pybattlenet.PyBattleNet(region="us")

		mock_response = Mock()
		mock_response.read.return_value = b'{"petInfo": "Bob"}'
		mock_response.status = 200  # This should work

		mock_urlopen.return_value = mock_response

		pets = BN.getPetIndex()

		assert pets == {"petInfo": "Bob"}

	@patch('urllib.request.urlopen')
	@patch('builtins.open', new_callable=mock_open, read_data='{"CLIENTID": "Frank", "BLSECRET": "Shhhh"}')
	@patch('os.path.exists')
	@patch('os.path.expanduser')
	def test_success_getToken(self, mock_expanduser, mock_exists, mock_file, mock_urlopen):
		""" Test that a missing secrets file exits the object """
		# setup mocks
		mock_expanduser.return_value = '/home/testuser/.file.json'
		mock_exists.return_value = True

		mock_response = Mock()
		mock_response.read.return_value = b'{"access_token": "t0k3n"}'
		mock_response.status = 200  # This should work

		mock_urlopen.return_value = mock_response

		BN = pybattlenet.PyBattleNet(region="us")

		mock_response = Mock()
		mock_response.read.return_value = b'{"TokenInfo": "Bob"}'
		mock_response.status = 200  # This should work

		mock_urlopen.return_value = mock_response

		pets = BN.getTokenIndex()

		assert pets == {"TokenInfo": "Bob"}
