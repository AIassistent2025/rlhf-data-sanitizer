import pytest
from src.dataset_cleaner import DatasetCleaner
from src.bias_detector import BiasDetector
from src.response_ranker import ResponseRanker

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

def test_ranker_structured_wins():
    ranker = ResponseRanker()
    resp_a = "Here is the answer:\n- Step 1\n- Step 2"
    resp_b = "Just do it."
    winner, score_w, score_l = ranker.rank_responses(resp_a, resp_b)
    assert winner == "A"
    assert score_w > score_l

def test_ranker_code_block_wins():
    ranker = ResponseRanker()
    resp_a = "Use this:\n```python\nprint('hello')\n```"
    resp_b = "Just print something."
    winner, _, _ = ranker.rank_responses(resp_a, resp_b)
    assert winner == "A"

def test_ranker_tie_returns_a():
    ranker = ResponseRanker()
    resp_a = "Short answer."
    resp_b = "Short answer."
    winner, score_w, score_l = ranker.rank_responses(resp_a, resp_b)
    assert winner == "A"
    assert score_w == score_l
