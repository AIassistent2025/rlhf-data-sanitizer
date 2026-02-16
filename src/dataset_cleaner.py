import re

class DatasetCleaner:
    """
    Utility to filter and clean RLHF training datasets.
    """
    def __init__(self, min_length=20, max_length=2000):
        self.min_length = min_length
        self.max_length = max_length

    def is_gibberish(self, text):
        # A very basic check for nonsensical strings (e.g., repeated characters)
        if re.search(r'(.)\1{4,}', text):
            return True
        # Check for lack of vowels (heuristic for English gibberish)
        if not re.search(r'[aeiouAEIOU]', text):
            return True
        return False

    def clean_text(self, text):
        """Removes extra whitespaces and newlines."""
        if not isinstance(text, str):
            return ""
        return " ".join(text.split())

    def validate_response(self, text):
        """
        Main validation pipeline.
        Returns (is_valid, reason)
        """
        cleaned = self.clean_text(text)
        
        if len(cleaned) < self.min_length:
            return False, "Too short"
        
        if len(cleaned) > self.max_length:
            return False, "Too long"
        
        if self.is_gibberish(cleaned):
            return False, "Detected as gibberish/pattern repeated"
            
        return True, "Valid"

if __name__ == "__main__":
    cleaner = DatasetCleaner()
    samples = [
        "This is a perfectly valid and helpful response for a coding task.",
        "short",
        "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        "wth n vwls",
        "   Clean   me   up    "
    ]
    
    for s in samples:
        valid, reason = cleaner.validate_response(s)
        print(f"Sample: '{s[:30]}...' -> {valid} ({reason})")
