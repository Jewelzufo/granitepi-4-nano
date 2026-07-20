#!/usr/bin/env python3
"""Tests for doc_chat.py module."""

import pytest
import sys
from unittest.mock import patch, MagicMock, mock_open
import requests
import os

# Import the module functions
sys.path.insert(0, '/workspace/examples')
from doc_chat import check_ollama_service, load_document, MAX_CONTEXT_CHARS, REQUEST_TIMEOUT


class TestCheckOllamaService:
    """Tests for the check_ollama_service function."""

    @patch('doc_chat.requests.get')
    def test_service_running(self, mock_get):
        """Test when Ollama service is running and accessible."""
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        result = check_ollama_service()
        
        assert result is True
        mock_get.assert_called_once_with("http://localhost:11434/api/tags", timeout=5)

    @patch('doc_chat.requests.get')
    def test_service_not_running(self, mock_get):
        """Test when Ollama service is not running."""
        mock_get.side_effect = requests.exceptions.ConnectionError()
        
        result = check_ollama_service()
        
        assert result is False

    @patch('doc_chat.requests.get')
    def test_service_timeout(self, mock_get):
        """Test when Ollama service times out."""
        mock_get.side_effect = requests.exceptions.Timeout()
        
        result = check_ollama_service()
        
        assert result is False

    @patch('doc_chat.requests.get')
    def test_http_error(self, mock_get):
        """Test when Ollama returns an HTTP error."""
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError()
        mock_get.return_value = mock_response
        
        result = check_ollama_service()
        
        assert result is False


class TestLoadDocument:
    """Tests for the load_document function."""

    @patch('doc_chat.os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data="This is test content.")
    def test_load_small_file(self, mock_file, mock_exists):
        """Test loading a file smaller than max context."""
        result = load_document("/path/to/file.txt")
        
        assert result == "This is test content."
        mock_exists.assert_called_once_with("/path/to/file.txt")

    @patch('doc_chat.os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data="x" * (MAX_CONTEXT_CHARS + 100))
    def test_load_large_file(self, mock_file, mock_exists):
        """Test loading a file larger than max context."""
        result = load_document("/path/to/large_file.txt")
        
        assert len(result) == MAX_CONTEXT_CHARS + len("\n...[TRUNCATED]")
        assert result.endswith("\n...[TRUNCATED]")

    @patch('doc_chat.os.path.exists', return_value=False)
    def test_file_not_found(self, mock_exists):
        """Test when file doesn't exist."""
        with pytest.raises(FileNotFoundError) as exc_info:
            load_document("/nonexistent/file.txt")
        
        assert "File not found" in str(exc_info.value)

    @patch('doc_chat.os.path.exists', return_value=True)
    @patch('builtins.open')
    def test_read_error(self, mock_file, mock_exists):
        """Test when file reading fails."""
        mock_file.side_effect = IOError("Permission denied")
        
        with pytest.raises(RuntimeError) as exc_info:
            load_document("/path/to/file.txt")
        
        assert "Failed to read file" in str(exc_info.value)


class TestChatLoop:
    """Tests for the chat_loop function."""

    @patch('doc_chat.input', side_effect=['What is this?', 'exit'])
    @patch('doc_chat.requests.post')
    @patch('builtins.print')
    def test_chat_loop_basic(self, mock_print, mock_post, mock_input):
        """Test basic chat loop flow."""
        from doc_chat import chat_loop
        
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            'model': 'test-model',
            'response': 'This is the answer based on the document.'
        }
        mock_post.return_value = mock_response
        
        # Should not raise an exception
        chat_loop("Test document content", "test.txt")
        
        # Verify the API was called once
        assert mock_post.call_count == 1

    @patch('doc_chat.input', side_effect=['What is this?', 'exit'])
    @patch('doc_chat.requests.post')
    @patch('builtins.print')
    def test_chat_loop_timeout(self, mock_print, mock_post, mock_input):
        """Test chat loop with timeout error."""
        from doc_chat import chat_loop
        
        mock_post.side_effect = requests.exceptions.Timeout()
        
        # Should not raise an exception
        chat_loop("Test document content", "test.txt")

    @patch('doc_chat.input', side_effect=['What is this?', 'exit'])
    @patch('doc_chat.requests.post')
    @patch('builtins.print')
    def test_chat_loop_connection_error(self, mock_print, mock_post, mock_input):
        """Test chat loop with connection error."""
        from doc_chat import chat_loop
        
        mock_post.side_effect = requests.exceptions.ConnectionError()
        
        # Should not raise an exception
        chat_loop("Test document content", "test.txt")

    @patch('doc_chat.input', side_effect=['What is this?', 'exit'])
    @patch('doc_chat.requests.post')
    @patch('builtins.print')
    def test_chat_loop_http_error(self, mock_print, mock_post, mock_input):
        """Test chat loop with HTTP error."""
        from doc_chat import chat_loop
        
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError()
        mock_post.return_value = mock_response
        
        # Should not raise an exception
        chat_loop("Test document content", "test.txt")

    @patch('doc_chat.input', side_effect=[KeyboardInterrupt(), 'exit'])
    @patch('doc_chat.requests.post')
    @patch('builtins.print')
    def test_chat_loop_keyboard_interrupt(self, mock_print, mock_post, mock_input):
        """Test chat loop with keyboard interrupt."""
        from doc_chat import chat_loop
        
        # Should not raise an exception
        chat_loop("Test document content", "test.txt")

    @patch('doc_chat.input', side_effect=['', 'exit'])
    @patch('doc_chat.requests.post')
    @patch('builtins.print')
    def test_chat_loop_empty_query(self, mock_print, mock_post, mock_input):
        """Test chat loop with empty query."""
        from doc_chat import chat_loop
        
        # Should not call the API for empty queries
        chat_loop("Test document content", "test.txt")
        
        assert mock_post.call_count == 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
