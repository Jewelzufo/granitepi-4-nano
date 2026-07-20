#!/usr/bin/env python3
"""Tests for chat_loop.py module."""

import pytest
import sys
from unittest.mock import patch, MagicMock, call
import requests

# Import the module functions
sys.path.insert(0, '/workspace/examples')
from chat_loop import check_ollama_service, OLLAMA_URL, MODEL_NAME, REQUEST_TIMEOUT


class TestCheckOllamaService:
    """Tests for the check_ollama_service function."""

    @patch('chat_loop.requests.get')
    def test_service_running(self, mock_get):
        """Test when Ollama service is running and accessible."""
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        result = check_ollama_service()
        
        assert result is True
        mock_get.assert_called_once_with("http://localhost:11434/api/tags", timeout=5)

    @patch('chat_loop.requests.get')
    def test_service_not_running(self, mock_get):
        """Test when Ollama service is not running."""
        mock_get.side_effect = requests.exceptions.ConnectionError()
        
        result = check_ollama_service()
        
        assert result is False

    @patch('chat_loop.requests.get')
    def test_service_timeout(self, mock_get):
        """Test when Ollama service times out."""
        mock_get.side_effect = requests.exceptions.Timeout()
        
        result = check_ollama_service()
        
        assert result is False

    @patch('chat_loop.requests.get')
    def test_http_error(self, mock_get):
        """Test when Ollama returns an HTTP error."""
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError()
        mock_get.return_value = mock_response
        
        result = check_ollama_service()
        
        assert result is False


class TestChatSession:
    """Tests for the chat_session function."""

    @patch('chat_loop.input', side_effect=['Hello', 'exit'])
    @patch('chat_loop.requests.post')
    @patch('chat_loop.check_ollama_service', return_value=True)
    @patch('builtins.print')
    def test_chat_session_basic(self, mock_print, mock_check, mock_post, mock_input):
        """Test basic chat session flow."""
        from chat_loop import chat_session
        
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            'model': MODEL_NAME,
            'response': 'Hello! How can I help you?',
            'context': [1, 2, 3]
        }
        mock_post.return_value = mock_response
        
        chat_session()
        
        # Verify the API was called once
        assert mock_post.call_count == 1

    @patch('chat_loop.input', side_effect=['Hello', 'exit'])
    @patch('chat_loop.requests.post')
    @patch('chat_loop.check_ollama_service', return_value=True)
    def test_chat_session_timeout(self, mock_check, mock_post, mock_input):
        """Test chat session with timeout error."""
        from chat_loop import chat_session
        
        mock_post.side_effect = requests.exceptions.Timeout()
        
        # Should not raise an exception
        chat_session()

    @patch('chat_loop.input', side_effect=['Hello', 'exit'])
    @patch('chat_loop.requests.post')
    @patch('chat_loop.check_ollama_service', return_value=True)
    def test_chat_session_connection_error(self, mock_check, mock_post, mock_input):
        """Test chat session with connection error."""
        from chat_loop import chat_session
        
        mock_post.side_effect = requests.exceptions.ConnectionError()
        
        # Should not raise an exception
        chat_session()

    @patch('chat_loop.input', side_effect=['Hello', 'exit'])
    @patch('chat_loop.requests.post')
    @patch('chat_loop.check_ollama_service', return_value=True)
    def test_chat_session_http_error(self, mock_check, mock_post, mock_input):
        """Test chat session with HTTP error."""
        from chat_loop import chat_session
        
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError()
        mock_post.return_value = mock_response
        
        # Should not raise an exception
        chat_session()

    @patch('chat_loop.input', side_effect=[KeyboardInterrupt(), 'exit'])
    @patch('chat_loop.requests.post')
    @patch('chat_loop.check_ollama_service', return_value=True)
    def test_chat_session_keyboard_interrupt(self, mock_check, mock_post, mock_input):
        """Test chat session with keyboard interrupt."""
        from chat_loop import chat_session
        
        # Should not raise an exception
        chat_session()

    @patch('chat_loop.check_ollama_service', return_value=False)
    @patch('builtins.print')
    def test_chat_session_service_not_running(self, mock_print, mock_check):
        """Test chat session when service is not running."""
        from chat_loop import chat_session
        
        with pytest.raises(SystemExit) as exc_info:
            chat_session()
        
        assert exc_info.value.code == 1


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
