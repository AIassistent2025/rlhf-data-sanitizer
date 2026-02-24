import re

class DatasetCleaner:
    """
    Utility to filter and clean RLHF training datasets.
    """
    def __init__(self, min_length=20, max_length=2000):
        self.min_length = min_length
        self.max_length = max_length

    def is_gibberish(self, text):
        """
        Detects potential nonsensical strings based on character distribution.
        """
        if not text:
            return False
            
        # 1. Repeated character pattern check
        if re.search(r'(.)\1{4,}', text):
            return True
            
        # 2. Vowel-to-Consonant Ratio (Heuristic for English/Romanized text)
        vowels = len(re.findall(r'[aeiouAEIOU]', text))
        consonants = len(re.findall(r'[bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ]', text))
        
        if (vowels + consonants) > 0 and (vowels / (vowels + consonants)) < 0.1:
            return True # Too few vowels often indicates nonsense or acronym-heavy strings
            
        # 3. Special character density
        special_chars = len(re.findall(r'[^a-zA-Z0-9\s]', text))
        if len(text) > 0 and (special_chars / len(text)) > 0.3:
            return True # Over 30% special chars is usually a sign of corrupted data
            
        return False

    def clean_text(self, text):
        """Removes extra whitespaces, newlines, and trailing punctuation."""
        if not isinstance(text, str):
            return ""
        # Remove extra whitespace
        text = " ".join(text.split())
        return text

    def validate_response(self, text):
        """
        Comprehensive validation of a single model response.
        Returns: (is_valid: bool, reason: str, metadata: dict)
        """
        cleaned = self.clean_text(text)
        metadata = {
            "original_length": len(text) if text else 0,
            "cleaned_length": len(cleaned),
            "is_empty": not bool(cleaned)
        }
        
        if not cleaned:
            return False, "Input is empty", metadata
        
        if len(cleaned) < self.min_length:
            return False, f"Too short (min {self.min_length})", metadata
        
        if len(cleaned) > self.max_length:
            return False, f"Too long (max {self.max_length})", metadata
        
        if self.is_gibberish(cleaned):
            return False, "Detected as gibberish or corrupted data", metadata
            
        return True, "Valid", metadata

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
        valid, reason, _ = cleaner.validate_response(s)
        print(f"Sample: '{s[:30]}...' -> {valid} ({reason})")
