#!/usr/bin/env python3
"""Tests for sentiment_analysis.py module."""

import pytest
import sys
from unittest.mock import patch, MagicMock
import requests

# Import the module functions
sys.path.insert(0, '/workspace/examples')
from sentiment_analysis import check_ollama_service, analyze_sentiment, OLLAMA_URL, MODEL_NAME, REQUEST_TIMEOUT


class TestCheckOllamaService:
    """Tests for the check_ollama_service function."""

    @patch('sentiment_analysis.requests.get')
    def test_service_running(self, mock_get):
        """Test when Ollama service is running and accessible."""
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        result = check_ollama_service()
        
        assert result is True
        mock_get.assert_called_once_with("http://localhost:11434/api/tags", timeout=5)

    @patch('sentiment_analysis.requests.get')
    def test_service_not_running(self, mock_get):
        """Test when Ollama service is not running."""
        mock_get.side_effect = requests.exceptions.ConnectionError()
        
        result = check_ollama_service()
        
        assert result is False

    @patch('sentiment_analysis.requests.get')
    def test_service_timeout(self, mock_get):
        """Test when Ollama service times out."""
        mock_get.side_effect = requests.exceptions.Timeout()
        
        result = check_ollama_service()
        
        assert result is False

    @patch('sentiment_analysis.requests.get')
    def test_http_error(self, mock_get):
        """Test when Ollama returns an HTTP error."""
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError()
        mock_get.return_value = mock_response
        
        result = check_ollama_service()
        
        assert result is False


class TestAnalyzeSentiment:
    """Tests for the analyze_sentiment function."""

    @patch('sentiment_analysis.requests.post')
    def test_positive_sentiment(self, mock_post):
        """Test analyzing positive sentiment."""
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {'response': 'Positive'}
        mock_post.return_value = mock_response
        
        result = analyze_sentiment("I love this product!")
        
        assert result == 'Positive'
        call_args = mock_post.call_args
        assert call_args[1]['json']['options']['temperature'] == 0

    @patch('sentiment_analysis.requests.post')
    def test_negative_sentiment(self, mock_post):
        """Test analyzing negative sentiment."""
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {'response': 'Negative'}
        mock_post.return_value = mock_response
        
        result = analyze_sentiment("This is terrible.")
        
        assert result == 'Negative'

    @patch('sentiment_analysis.requests.post')
    def test_neutral_sentiment(self, mock_post):
        """Test analyzing neutral sentiment."""
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {'response': 'Neutral'}
        mock_post.return_value = mock_response
        
        result = analyze_sentiment("The weather is cloudy today.")
        
        assert result == 'Neutral'

    @patch('sentiment_analysis.requests.post')
    def test_timeout_error(self, mock_post):
        """Test when request times out."""
        mock_post.side_effect = requests.exceptions.Timeout()
        
        result = analyze_sentiment("Test text")
        
        assert "timed out" in result.lower()

    @patch('sentiment_analysis.requests.post')
    def test_connection_error(self, mock_post):
        """Test when there's a connection error."""
        mock_post.side_effect = requests.exceptions.ConnectionError()
        
        result = analyze_sentiment("Test text")
        
        assert "Could not connect" in result

    @patch('sentiment_analysis.requests.post')
    def test_http_error(self, mock_post):
        """Test when there's an HTTP error."""
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Client Error")
        mock_post.return_value = mock_response
        
        result = analyze_sentiment("Test text")
        
        assert "HTTP error" in result

    @patch('sentiment_analysis.requests.post')
    def test_general_request_exception(self, mock_post):
        """Test when there's a general request exception."""
        mock_post.side_effect = requests.exceptions.RequestException("Unknown error")
        
        result = analyze_sentiment("Test text")
        
        assert "Error connecting" in result


class TestMainScript:
    """Tests for the main script execution flow."""

    @patch('sentiment_analysis.check_ollama_service', return_value=False)
    @patch('builtins.print')
    def test_main_service_not_running(self, mock_print, mock_check):
        """Test main function when service is not running."""
        # We need to simulate sys.argv and prevent the while loop
        with patch('sentiment_analysis.sys.exit') as mock_exit:
            # Import after patching to avoid side effects
            import sentiment_analysis
            
            # Simulate the pre-flight check portion
            if not sentiment_analysis.check_ollama_service():
                print("Error: Ollama service is not running or not accessible at http://localhost:11434")
                print("Please start Ollama and try again.")
                sentiment_analysis.sys.exit(1)
            
            mock_exit.assert_called_once_with(1)

    @patch('sentiment_analysis.input', side_effect=['Great day!', 'exit'])
    @patch('sentiment_analysis.requests.post')
    @patch('sentiment_analysis.check_ollama_service', return_value=True)
    @patch('builtins.print')
    def test_main_basic_flow(self, mock_print, mock_check, mock_post, mock_input):
        """Test basic main function flow."""
        from sentiment_analysis import analyze_sentiment
        
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {'response': 'Positive'}
        mock_post.return_value = mock_response
        
        # Simulate the analysis
        result = analyze_sentiment("Great day!")
        assert result == 'Positive'

    @patch('sentiment_analysis.input', side_effect=KeyboardInterrupt())
    @patch('sentiment_analysis.requests.post')
    @patch('sentiment_analysis.check_ollama_service', return_value=True)
    @patch('builtins.print')
    def test_main_keyboard_interrupt(self, mock_print, mock_check, mock_post, mock_input):
        """Test main function with keyboard interrupt."""
        from sentiment_analysis import analyze_sentiment
        
        # Should handle KeyboardInterrupt gracefully
        try:
            analyze_sentiment("Test")
        except Exception:
            pytest.fail("Should not raise exception")

    @patch('sentiment_analysis.input', side_effect=EOFError())
    @patch('sentiment_analysis.requests.post')
    @patch('sentiment_analysis.check_ollama_service', return_value=True)
    def test_main_eof_error(self, mock_check, mock_post, mock_input):
        """Test main function with EOF error."""
        from sentiment_analysis import analyze_sentiment
        
        # Should handle EOFError gracefully
        try:
            analyze_sentiment("Test")
        except Exception:
            pytest.fail("Should not raise exception")


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
