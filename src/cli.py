import argparse
import json
import csv
import sys
from src.dataset_cleaner import DatasetCleaner
from src.bias_detector import BiasDetector

def process_file(input_path, output_path):
    cleaner = DatasetCleaner()
    detector = BiasDetector()
    results = []

    print(f"[*] Processing {input_path}...")

    # Basic support for JSONL
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            for line in f:
                data = json.loads(line)
                response = data.get("response", "")
                
                # Run Pipeline
                is_valid, reason, meta = cleaner.validate_response(response)
                is_safe, flagged = detector.check_safety(response)
                bias_findings = detector.detect_bias_indicators(response)

                data["eval_status"] = {
                    "valid": is_valid,
                    "reason": reason,
                    "safe": is_safe,
                    "flagged": flagged,
                    "bias": bias_findings
                }
                results.append(data)

        # Write results
        with open(output_path, 'w', encoding='utf-8') as f:
            for r in results:
                f.write(json.dumps(r) + "\n")
        
        print(f"[+] Success! Results saved to {output_path}")

    except Exception as e:
        print(f"[!] Error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="RLHF Eval Kit CLI")
    parser.add_argument("--input", required=True, help="Path to input JSONL/CSV file")
    parser.add_argument("--output", required=True, help="Path to save results")
    
    args = parser.parse_args()
    process_file(args.input, args.output)
