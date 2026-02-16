import re

class BiasDetector:
    """
    Detects potential bias or policy violations in LLM outputs.
    Note: In a production environment, this would integrate with heavier models
    like Perspective API or specialized BERT classifiers.
    """
    
    # Heuristic based on common safety guidelines for RLHF
    BANNED_PATTERNS = [
        r"\b(hate|kill|bomb|illegal|stolen|exploit)\b",
        r"\b(superior to|inferior to)\b", # Basic bias markers
    ]

    def __init__(self):
        self.patterns = [re.compile(p, re.IGNORECASE) for p in self.BANNED_PATTERNS]

    def check_safety(self, text):
        """
        Checks for flagged patterns.
        Returns (is_safe, flagged_terms)
        """
        flagged = []
        for p in self.patterns:
            matches = p.findall(text)
            if matches:
                flagged.extend(matches)
        
        if flagged:
            return False, list(set(flagged))
        return True, []

    def check_neutrality(self, text):
        """
        Heuristic for detecting non-neutral language (stereotypes).
        """
        # Placeholder for more complex NLP logic
        if "obviously" in text.lower() or "clearly" in text.lower():
            return "Warning: Potential authoritative bias (use of 'obviously/clearly')"
        return "Neutral"

if __name__ == "__main__":
    detector = BiasDetector()
    sample = "I can definitely help you kill some time today, but I won't help with anything illegal."
    safe, terms = detector.check_safety(sample)
    print(f"Safe: {safe}, Flagged: {terms}")
