import re

class BiasDetector:
    """
    Detects potential bias or policy violations in LLM outputs.
    Note: In a production environment, this would integrate with heavier models
    like Perspective API or specialized BERT classifiers.
    """
    
    # Expanded heuristics for RLHF safety and neutrality
    BANNED_PATTERNS = [
        r"\b(hate|kill|bomb|illegal|stolen|exploit|scam|hack)\b",
        r"\b(superior to|inferior to|better than those|worse than those)\b",
        r"\b(all [a-z]+ are [a-z]+|every [a-z]+ is [a-z]+)\b", # Basic generalization patterns
    ]

    NEUTRALITY_MARKERS = {
        "authoritative": [r"\bobviously\b", r"\bclearly\b", r"\bundoubtedly\b", r"\bdefinitely\b"],
        "opinionated": [r"\bI believe\b", r"\bIn my opinion\b", r"\bIt is common knowledge\b"],
        "biased_adjectives": [r"\bdisgusting\b", r"\bterrible\b", r"\bhorrible\b", r"\bexcellent\b", r"\bperfect\b"]
    }

    def __init__(self):
        self.safety_patterns = [re.compile(p, re.IGNORECASE) for p in self.BANNED_PATTERNS]
        self.neutrality_patterns = {
            category: [re.compile(p, re.IGNORECASE) for p in patterns]
            for category, patterns in self.NEUTRALITY_MARKERS.items()
        }

    def check_safety(self, text):
        """
        Checks for flagged safety violations.
        Returns: (is_safe: bool, flagged_terms: list)
        """
        flagged = []
        for p in self.safety_patterns:
            matches = p.findall(text)
            if matches:
                flagged.extend(matches)
        
        return len(flagged) == 0, list(set(flagged))

    def detect_bias_indicators(self, text):
        """
        Identifies potential non-neutral language and linguistic bias.
        Returns: dict of findings by category
        """
        findings = {}
        text_lower = text.lower()
        
        for category, patterns in self.neutrality_patterns.items():
            discovered = []
            for p in patterns:
                if p.search(text_lower):
                    discovered.append(p.pattern.replace("\\b", ""))
            if discovered:
                findings[category] = discovered
                
        return findings

if __name__ == "__main__":
    detector = BiasDetector()
    sample = "I can definitely help you kill some time today, but I won't help with anything illegal."
    safe, terms = detector.check_safety(sample)
    print(f"Safe: {safe}, Flagged: {terms}")
    
    bias = detector.detect_bias_indicators("In my opinion, this is obviously the best approach.")
    print(f"Bias Indicators: {bias}")
