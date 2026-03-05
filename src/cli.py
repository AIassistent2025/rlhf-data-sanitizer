import argparse
import json
import sys
from src.dataset_cleaner import DatasetCleaner
from src.bias_detector import BiasDetector
from src.response_ranker import ResponseRanker

def process_file(input_path, output_path):
    cleaner = DatasetCleaner()
    detector = BiasDetector()
    ranker = ResponseRanker()
    results = []

    print(f"[*] Processing {input_path}...")

    if not input_path.endswith(".jsonl"):
        print("[!] Error: Only .jsonl files are supported. Please convert your file to JSONL format.")
        sys.exit(1)

    with open(input_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
            except json.JSONDecodeError as e:
                print(f"[!] Skipping line {line_num}: invalid JSON — {e}")
                continue

            response_a = data.get("response_a", data.get("response", ""))
            response_b = data.get("response_b", "")

            is_valid, reason, meta = cleaner.validate_response(response_a)
            is_safe, flagged = detector.check_safety(response_a)
            bias_findings = detector.detect_bias_indicators(response_a)

            eval_status = {
                "valid": is_valid,
                "reason": reason,
                "safe": is_safe,
                "flagged": flagged,
                "bias": bias_findings,
            }

            if response_b:
                winner, score_w, score_l = ranker.rank_responses(response_a, response_b)
                eval_status["ranking"] = {
                    "winner": winner,
                    "score_a": score_w if winner == "A" else score_l,
                    "score_b": score_w if winner == "B" else score_l,
                }

            data["eval_status"] = eval_status
            results.append(data)

    with open(output_path, 'w', encoding='utf-8') as f:
        for r in results:
            f.write(json.dumps(r) + "\n")

    print(f"[+] Done. {len(results)} records saved to {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="RLHF Data Sanitizer CLI")
    parser.add_argument("--input", required=True, help="Path to input .jsonl file")
    parser.add_argument("--output", required=True, help="Path to save results .jsonl")

    args = parser.parse_args()
    process_file(args.input, args.output)
