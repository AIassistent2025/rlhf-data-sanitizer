from src.dataset_cleaner import DatasetCleaner
from src.bias_detector import BiasDetector

def run_tests():
    print("[*] Starting Manual Verification...")
    
    # Test Cleaner
    cleaner = DatasetCleaner(min_length=10)
    is_valid, reason, _ = cleaner.validate_response("Valid long response")
    print(f"[Cleaner] Valid Test: {'PASS' if is_valid else 'FAIL'} ({reason})")
    
    # Test Gibberish
    is_valid, reason, _ = cleaner.validate_response("aaaaaaaaaaaaaaaaaaaa")
    print(f"[Cleaner] Gibberish Test: {'PASS' if not is_valid else 'FAIL'} ({reason})")
    
    # Test Bias Safety
    detector = BiasDetector()
    is_safe, flagged = detector.check_safety("I will help you kill time.")
    print(f"[Bias] Safety Test: {'PASS' if not is_safe else 'FAIL'} (Flagged: {flagged})")
    
    # Test Neutrality
    findings = detector.detect_bias_indicators("In my opinion, this is obviously great.")
    print(f"[Bias] Neutrality Test: {'PASS' if 'authoritative' in findings else 'FAIL'} (Findings: {findings})")

if __name__ == "__main__":
    run_tests()
