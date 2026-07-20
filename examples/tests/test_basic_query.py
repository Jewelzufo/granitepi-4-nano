#!/usr/bin/env python3
"""Tests for basic_query.py module."""

import pytest
import sys
from unittest.mock import patch, MagicMock
import requests

# Import the module functions
sys.path.insert(0, '/workspace/examples')
from basic_query import check_ollama_service, query_granite, OLLAMA_URL, MODEL_NAME, REQUEST_TIMEOUT


class TestCheckOllamaService:
    """Tests for the check_ollama_service function."""

    @patch('basic_query.requests.get')
    def test_service_running(self, mock_get):
        """Test when Ollama service is running and accessible."""
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        result = check_ollama_service()
        
        assert result is True
        mock_get.assert_called_once_with("http://localhost:11434/api/tags", timeout=5)

    @patch('basic_query.requests.get')
    def test_service_not_running(self, mock_get):
        """Test when Ollama service is not running."""
        mock_get.side_effect = requests.exceptions.ConnectionError()
        
        result = check_ollama_service()
        
        assert result is False

    @patch('basic_query.requests.get')
    def test_service_timeout(self, mock_get):
        """Test when Ollama service times out."""
        mock_get.side_effect = requests.exceptions.Timeout()
        
        result = check_ollama_service()
        
        assert result is False

    @patch('basic_query.requests.get')
    def test_http_error(self, mock_get):
        """Test when Ollama returns an HTTP error."""
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError()
        mock_get.return_value = mock_response
        
        result = check_ollama_service()
        
        assert result is False


class TestQueryGranite:
    """Tests for the query_granite function."""

    @patch('basic_query.requests.post')
    def test_successful_query(self, mock_post):
        """Test a successful query to the model."""
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            'model': MODEL_NAME,
            'response': 'This is a test response.'
        }
        mock_post.return_value = mock_response
        
        # Capture print output
        with patch('builtins.print') as mock_print:
            result = query_granite("Test prompt")
        
        assert result == 'This is a test response.'
        mock_post.assert_called_once()
        call_args = mock_post.call_args
        assert call_args[1]['json']['prompt'] == "Test prompt"
        assert call_args[1]['json']['model'] == MODEL_NAME
        assert call_args[1]['json']['stream'] is False

    @patch('basic_query.requests.post')
    def test_timeout_error(self, mock_post):
        """Test when the request times out."""
        mock_post.side_effect = requests.exceptions.Timeout()
        
        with patch('builtins.print') as mock_print:
            result = query_granite("Test prompt")
        
        assert result is None
        mock_print.assert_any_call(f"Error: Request timed out after {REQUEST_TIMEOUT} seconds.")

    @patch('basic_query.requests.post')
    def test_connection_error(self, mock_post):
        """Test when there's a connection error."""
        mock_post.side_effect = requests.exceptions.ConnectionError()
        
        with patch('builtins.print') as mock_print:
            result = query_granite("Test prompt")
        
        assert result is None
        mock_print.assert_any_call("Error: Could not connect to Ollama service. Is it running on localhost:11434?")

    @patch('basic_query.requests.post')
    def test_http_error(self, mock_post):
        """Test when there's an HTTP error."""
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Client Error")
        mock_post.return_value = mock_response
        
        with patch('builtins.print') as mock_print:
            result = query_granite("Test prompt")
        
        assert result is None

    @patch('basic_query.requests.post')
    def test_empty_response(self, mock_post):
        """Test when response has no 'response' key."""
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {'model': MODEL_NAME}
        mock_post.return_value = mock_response
        
        with patch('builtins.print') as mock_print:
            result = query_granite("Test prompt")
        
        assert result is None


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
