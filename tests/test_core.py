import pytest
from src.dataset_cleaner import DatasetCleaner
from src.bias_detector import BiasDetector

def test_cleaner_valid():
    cleaner = DatasetCleaner(min_length=10)
    is_valid, reason, meta = cleaner.validate_response("This is a valid long enough response.")
    assert is_valid is True

def test_cleaner_too_short():
    cleaner = DatasetCleaner(min_length=50)
    is_valid, reason, meta = cleaner.validate_response("Too short.")
    assert is_valid is False
    assert "Too short" in reason

def test_cleaner_gibberish():
    cleaner = DatasetCleaner()
    is_valid, reason, meta = cleaner.validate_response("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
    assert is_valid is False
    assert "gibberish" in reason

def test_bias_safety():
    detector = BiasDetector()
    is_safe, flagged = detector.check_safety("I will help you kill time.")
    assert is_safe is False
    assert "kill" in flagged

def test_bias_indicators():
    detector = BiasDetector()
    findings = detector.detect_bias_indicators("In my opinion, this is obviously great.")
    assert "authoritative" in findings
    assert "opinionated" in findings
