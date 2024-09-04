import pytest
from unittest.mock import patch, MagicMock, mock_open
import pandas as pd
import json
import csv
from datetime import datetime

# Import the class to be tested
from consensus_services.hcs_stats import HCSServices

# Mock class for Txn to be used in the read_data method
class MockTxn:
    def __init__(self, **kwargs):
        self.data = kwargs
    
    def dict(self):
        return self.data

@pytest.fixture
def base_script():
    with patch('consensus_services.hcs_stats.HCSServices.__init__', lambda x, y: None):  # Skip the actual init
        base_script_instance = HCSServices("test_log")
        base_script_instance.options = MagicMock()
        base_script_instance.options.input_file = 'input.json'
        base_script_instance.options.output_folder = 'output'
        base_script_instance.options.output_format = 'json'
        base_script_instance.options.log_level = 'INFO'
        base_script_instance.logger = MagicMock()
        base_script_instance.starttime = datetime(2024, 1, 1)
        return base_script_instance

def test_init_env_var(base_script):
    with patch.dict('os.environ', {'PATH': '/mock/path'}):
        base_script.__init_env_var__()
        base_script.logger.info.assert_called_with("Environment variable PATH=%s", '/mock/path')

    with patch.dict('os.environ', {}, clear=True), pytest.raises(Exception, match="Environment variable PATH is not set"):
        base_script.__init_env_var__()


def test_read_data_json(base_script):
    # Test JSON reading
    json_data = '{"key1": "value1", "key2": "value2"}\n'
    with patch('builtins.open', mock_open(read_data=json_data)), \
         patch('json.loads', side_effect=json.loads) as mock_json_loads:
        result = base_script.read_data('input.json', MockTxn)
        assert result == [{"key1": "value1", "key2": "value2"}]

def test_read_data_csv(base_script):
    # Test CSV reading
    csv_data = "key1,key2\nvalue1,value2\n"
    with patch('builtins.open', mock_open(read_data=csv_data)), \
         patch('csv.DictReader', return_value=[{"key1": "value1", "key2": "value2"}]):
        result = base_script.read_data('input.csv', MockTxn)
        assert result == [{"key1": "value1", "key2": "value2"}]

def test_read_data_invalid_format(base_script):
    # Attempt to read a file with an invalid format (e.g., .txt file)
    result = base_script.read_data("invalid_format.txt", MagicMock)
    # Verify that the method returned None
    assert result is None
    # Verify that the correct log message was produced
    base_script.logger.error.assert_called_once_with("Invalid input file format")

def test_read_data_file_not_found(base_script):
    # Simulate FileNotFoundError
    with patch("builtins.open", side_effect=FileNotFoundError):
        result = base_script.read_data("non_existent_file.json", MagicMock)
    
    # Verify that None is returned
    assert result is None
    
    # Check that the appropriate log message was generated
    base_script.logger.error.assert_called_once_with("File not found: non_existent_file.json")

def test_read_data_json_decode_error(base_script):
    # Simulate JSONDecodeError
    mock_file_content = '{"invalid_json": "missing end quote}'
    with patch("builtins.open", mock_open(read_data=mock_file_content)), \
         patch("json.loads", side_effect=json.JSONDecodeError("Expecting value", "", 0)):
        result = base_script.read_data("invalid.json", MagicMock)
    
    # Verify that None is returned
    assert result is None
    
    # Check that the appropriate log message was generated
    base_script.logger.error.assert_called_once_with("Error decoding JSON from file: invalid.json")

def test_read_data_csv_error(base_script):
    # Simulate csv.Error
    with patch("builtins.open", mock_open()), \
         patch("csv.DictReader", side_effect=csv.Error):
        result = base_script.read_data("invalid.csv", MagicMock)
    
    # Verify that None is returned
    assert result is None
    
    # Check that the appropriate log message was generated
    base_script.logger.error.assert_called_once_with("Error reading CSV file: invalid.csv")

def test_read_data_generic_exception(base_script):
    # Simulate a generic exception
    with patch("builtins.open", side_effect=Exception("Some error")):
        result = base_script.read_data("any_file.json", MagicMock)
    
    # Verify that None is returned
    assert result is None
    
    # Check that the appropriate log message was generated
    base_script.logger.error.assert_called_once_with("An error occurred while reading the file: Some error")

def test_write_df_to_file_json(base_script):
    output_df = pd.DataFrame([{'a': 1, 'b': 2}])
    with patch('pandas.DataFrame.to_json') as mock_to_json:
        base_script.write_df_to_file('output/test', output_df)
        mock_to_json.assert_called_once()

def test_write_df_to_file_csv(base_script):
    output_df = pd.DataFrame([{'a': 1, 'b': 2}])
    base_script.options.output_format = 'csv'
    with patch('pandas.DataFrame.to_csv') as mock_to_csv:
        base_script.write_df_to_file('output/test', output_df)
        mock_to_csv.assert_called_once()

def test_write_df_to_file_invalid_format(base_script):
    base_script.options.output_format = 'invalid_format'
    with pytest.raises(Exception, match="Invalid output format"):
        base_script.write_df_to_file('output/test', pd.DataFrame())

def test_rcdstreams_to_pd_df(base_script):
    records = [{'a': 1, 'b': 2}, {'a': 3, 'b': 4}]
    result_df = base_script.rcdstreams_to_pd_df(records)
    assert isinstance(result_df, pd.DataFrame)
    assert len(result_df) == 2
