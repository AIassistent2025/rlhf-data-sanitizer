class ResponseRanker:
    """
    Simulates the ranking step of RLHF where Response A and Response B 
    are compared based on logic and quality metrics.
    """
    
    def evaluate_quality(self, response):
        # High quality responses often contain structured formatting
        score = 0
        if "```" in response: score += 2 # Coding blocks
        if "\n-" in response or "\n1." in response: score += 2 # Lists
        if len(response) > 50: score += 1
        return score

    def rank_responses(self, response_a, response_b):
        """
        Returns 'A' or 'B' as the winner.
        """
        score_a = self.evaluate_quality(response_a)
        score_b = self.evaluate_quality(response_b)
        
        if score_a >= score_b:
            return "A", score_a, score_b
        else:
            return "B", score_b, score_a

if __name__ == "__main__":
    ranker = ResponseRanker()
    resp_a = "To fix this, use a for loop:\n- Step 1: Open file\n- Step 2: Read lines"
    resp_b = "I think you should just use a loop and it will work fine."
    
    winner, s_w, s_l = ranker.rank_responses(resp_a, resp_b)
    print(f"Winner: {winner} (Score {s_w} vs {s_l})")
