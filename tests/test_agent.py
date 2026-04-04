import pytest
from unittest.mock import patch, MagicMock
from agent import  get_open_prs, already_commented, save_tests_to_file
import os

# --- get_open_prs tests ---

def test_get_open_prs_returns_list_on_success():
    # Verifies that a successful API response returns a list of PRs
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [
        {"number": 1, "title": "Test PR", "user": {"login": "dev"}, "html_url":"http://github.com"}
        ]
    with patch('agent.requests.get', return_value=mock_response):
        result = get_open_prs("owner", "repo")
        assert isinstance(result, list)
        assert len(result) == 1

def test_get_open_prs_returns_empty_list_on_failure():
    # Verifies that a failed API response returns an empty list, not an exception
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_response.text = "Not Found"
    with patch("agent.requests.get", return_value=mock_response):
        result = get_open_prs("owner", "repo")
    assert result == []

# --- already_commented tests ---

def test_already_commented_returns_true_when_comment_exists():
    # Verifies agent correctly detects its own previous comment
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [
        {"body": "## 🤖 QA Agent — Auto-generated Pytest Tests"}
    ]
    with patch("agent.requests.get", return_value=mock_response):
        result = already_commented("owner", "repo", 1)
    assert result is True

def test_already_commented_returns_false_when_no_comment():
    # Verifies agent correctly identifies PRs it hasn't processed yet
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [
        {"body": "Looks good to me!"}
    ]
    with patch("agent.requests.get", return_value=mock_response):
        result = already_commented("owner", "repo", 1)
    assert result is False

# --- save_tests_to_file tests ---

def test_save_tests_to_file_creates_file(tmp_path, monkeypatch):
    # Verifies that generated tests are written to disk correctly
    monkeypatch.chdir(tmp_path)
    save_tests_to_file(99, "def test_example():\n    assert True")
    expected = tmp_path / "generated_tests" / "test_pr_99.py"
    assert expected.exists()

def test_save_tests_to_file_correct_content(tmp_path, monkeypatch):
    # Verifies the file content matches what was passed in
    monkeypatch.chdir(tmp_path)
    content = "def test_example():\n    assert True"
    save_tests_to_file(99, content)
    result = (tmp_path / "generated_tests" / "test_pr_99.py").read_text()
    assert result == content
