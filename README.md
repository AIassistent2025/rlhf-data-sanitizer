# RLHF Automation Suite: `rlhf-eval-kit` 🤖⚖️

A professional Python toolkit designed to automate critical steps in the **Reinforcement Learning from Human Feedback (RLHF)** pipeline. 

This suite is optimized for AI Training specialists and Model Evaluation engineers who need to ensure high-quality training datasets and bias-free model outputs.

## 🚀 Overview

Manual evaluation of Thousands of LLM responses is time-consuming and prone to human error. `rlhf-eval-kit` provides a programmatic layer to:
- **Clean Datasets:** Automatically filter out low-quality, too short, or nonsensical training pairs.
- **Detect Bias:** Identify potential safety violations or non-neutral language using heuristic pattern matching.
- **Automated Ranking:** Compare model outputs (Response A vs B) based on structural quality and formatting indicators.

## 🛠 Features

- **`DatasetCleaner`**: Validates response length, removes whitespace noise, and detects gibberish.
- **`BiasDetector`**: Flags banned patterns and detects over-authoritative language (e.g., "obviously").
- **`ResponseRanker`**: A framework for A/B testing model responses to simulate human preference.

## 📦 Installation

```bash
git clone https://github.com/AIassistent2025/rlhf-eval-kit.git
cd rlhf-eval-kit
pip install -r requirements.txt
```

## 📖 Usage

Each module can be run independently or integrated into a larger evaluation pipeline.

```python
from src.dataset_cleaner import DatasetCleaner

cleaner = DatasetCleaner()
is_valid, reason = cleaner.validate_response("Your sample text here...")
```

---
*Developed as a showcase of AI Engineering expertise in RLHF and Model Vetting.*
