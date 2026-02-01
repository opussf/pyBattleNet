import pytest
from unittest.mock import patch, mock_open, Mock

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
			BN = pybattlenet.PyBattleNet(region="us")

		# Verify it exited with code 1
		assert exc_info.value.code == 1

	@patch('os.path.exists')
	@patch('os.path.expanduser')
	def test_missing_passedsecret_exits(self, mock_expanduser, mock_exists):
		# setup mocks
		mock_expanduser.return_value = '/home/testuser/.file.json'
		mock_exists.return_value = False

		with pytest.raises(SystemExit) as exc_info:
			BN = pybattlenet.PyBattleNet(region="us", clientID="Frank")
		assert exc_info.value.code == 1

	@patch('os.path.exists')
	@patch('os.path.expanduser')
	def test_missing_passedclinetID_exits(self, mock_expanduser, mock_exists):
		# setup mocks
		mock_expanduser.return_value = '/home/testuser/.file.json'
		mock_exists.return_value = False

		with pytest.raises(SystemExit) as exc_info:
			BN = pybattlenet.PyBattleNet(region="us", secret="Frank")
		assert exc_info.value.code == 1

	@patch('urllib.request.urlopen')
	@patch('builtins.open', new_callable=mock_open, read_data='{"CLIENTID": "Frank", "BLSECRET": "Shhhh"}')
	@patch('os.path.exists')
	@patch('os.path.expanduser')
	def test_success_sets_access_token(self, mock_expanduser, mock_exists, mock_file, mock_urlopen):
		""" Test that a missing secrets file exits the object """
		# setup mocks
		mock_expanduser.return_value = '/home/testuser/.file.json'
		mock_exists.return_value = True

		mock_response = Mock()
		mock_response.read.return_value = b'{"access_token": "t0k3n"}'
		mock_response.status = 200  # This should work

		# Set up the context manager
		mock_urlopen.return_value.__enter__.return_value = mock_response
		mock_urlopen.return_value.__exit__.return_value = None

		BN = pybattlenet.PyBattleNet(region="us")
		assert BN.access_token == "t0k3n"




#   @patch('urllib.request.urlopen')
#     def test_fetch_existing_character(self, mock_urlopen):
#         """Test fetching an existing character"""
#         mock_response = Mock()
#         mock_response.read.return_value = json.dumps({
#             "name": "Arthas",
#             "level": 80,
#             "class": "Paladin"
#         }).encode('utf-8')
#         mock_urlopen.return_value.__enter__.return_value = mock_response





	# @patch('builtins.open', new_callable=mock_open, read_data='{"CLIENTID": "clientID","BLSECRET": "secret"}')
	# @patch('os.path.exists')
	# @patch('os.path.expanduser')
	# def test_missing_secretsfile_exits(self, mock_expanduser, mock_exists, mock_file):
	# 	# setup mocks
	# 	mock_expanduser.return_value = '/home/testuser/.file.json'
	# 	mock_exists.return_value = False

	# 	with pytest.raises(SystemExit) as exc_info:
	# 		BN = pybattlenet.PyBattleNet(region = "us")

	# 	# Verify it exited with code 1
	# 	assert exc_info.value.code == 1




# import pytest
# from unittest.mock import patch, mock_open, Mock
# import os


# class TestConfigFile:
#     """Test cases involving config files in home directory"""

#     @patch('os.path.expanduser')
#     @patch('builtins.open', new_callable=mock_open, read_data='{"api_key": "test123"}')
#     def test_read_config_from_home(self, mock_file, mock_expanduser):
#         """Test reading config file from home directory"""
#         # Mock the home directory expansion
#         mock_expanduser.return_value = '/home/testuser/.pybattlenet/config.json'

#         # Your code that does something like:
#         # config_path = os.path.expanduser('~/.pybattlenet/config.json')
#         # with open(config_path) as f:
#         #     config = json.load(f)

#         # Verify expanduser was called with '~/.pybattlenet/config.json'
#         # mock_expanduser.assert_called_with('~/.pybattlenet/config.json')

#         # Verify file was opened
#         # mock_file.assert_called_with('/home/testuser/.pybattlenet/config.json')
#         pass

#     @patch('os.path.exists')
#     @patch('os.path.expanduser')
#     def test_config_file_missing(self, mock_expanduser, mock_exists):
#         """Test handling when config file doesn't exist"""
#         mock_expanduser.return_value = '/home/testuser/.pybattlenet/config.json'
#         mock_exists.return_value = False  # Pretend file doesn't exist

#         # Your code should handle missing file gracefully
#         # result = load_config()
#         # assert result == {}  # or whatever default behavior
#         pass

#     @patch('os.makedirs')
#     @patch('builtins.open', new_callable=mock_open)
#     @patch('os.path.expanduser')
#     def test_write_config_to_home(self, mock_expanduser, mock_file, mock_makedirs):
#         """Test writing config file to home directory"""
#         mock_expanduser.return_value = '/home/testuser/.pybattlenet/config.json'

#         # Your code that writes config
#         # save_config({"api_key": "new_key"})

#         # Verify directory creation was attempted
#         # mock_makedirs.assert_called()

#         # Verify file was written
#         # mock_file.assert_called_with('/home/testuser/.pybattlenet/config.json', 'w')
#         pass