# DeepLearning - Project - V2
This is a open project for building LLMS - generation solution code. ses Qwen2.5-Coder-7B-Instruct to generate Python solutions from natural-language programming problems and evaluates the generated solutions against predefined test cases.

## Table of Contents
- [Project Overview](#project-overview)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Installation](#installation)
- [Download](#download)
- [Generate](#generate)
- [Evaluate Generated](#evaluate-generated)
- [Notes](#notes)
- [References](#references)

## Project Overview
This project was developed for a programming assignment that explores the use of large language models (LLMs).

Given a programming problem written in Markdown, the model generates a Python solution. The generated code can then be evaluated using predefined test cases to measure its correctness.

The project consists of two main components:

- Code Generation (uet_coder.py): Loads a local language model, processes a programming problem, generates Python code, and saves the result to a file.
- Code Evaluation (uet_marker.py): Executes the generated solution against predefined test cases and reports the number and percentage of passed tests.

## Model
This project uses Qwen2.5-Coder-7B-Instruct, a code-focused language model from the Qwen team.

The model is downloaded from Hugging Face and stored locally in the model_weights/ directory. The project uses the safetensors format for model weights.

Project Structure

## Project Structure

```text
DeepLearning_V2/
├── model_weights/
│   └── # Downloaded model files
│
├── problems/
│   └── problem01/
│       ├── problem.md
│       ├── problem02.md
│       ├── problem03.md
│       ├── problem04.md
│       ├── problem05.md
│       ├── test01.json
│       ├── test02.json
│       ├── test03.json
│       ├── test04.json
│       ├── test05.json
│       └── solutions/
│           ├── solution01.py
│           ├── solution02.py
│           ├── solution03.py
│           ├── solution04.py
│           ├── solution05.py
│           └── generated.py
├── Assignment 1.md
├── requirements.txt
├── tesst1.ipynb
├── uet_coder.py
├── uet_marker.py
├── README.md
└── .venv/                 # Local virtual environment
```

The .venv/ directory is created locally and should not be committed to Git.

### File and Directory Descriptions

| File or directory | Description |
|---|---|
| `model_weights/` | Stores the downloaded Qwen model configuration, tokenizer files, and model weights. |
| `problems/` | Contains programming problem descriptions, test cases, and reference solutions. |
| `Assignment 1.md` | Contains the original assignment requirements and evaluation rules. |
| `requirements.txt` | Lists the Python dependencies required by the project. |
| `uet_coder.py` | Loads the model and generates Python solutions from problem descriptions. |
| `uet_marker.py` | Evaluates generated solutions using JSON test cases. |
| `tesst1.ipynb` | Experimental notebook for testing code and dependencies. |
| `.venv/` | Isolated Python environment for project dependencies. |

## Requirements
- Python 3.12 (64-bit recommended)
- pip
- Git (optional)
- An NVIDIA GPU with a compatible CUDA driver is recommended for faster inference.
- Sufficient RAM and/or VRAM to load the selected model.

The project uses PyTorch, Transformers, Accelerate, BitsAndBytes, and Safetensors.

**Hardware note:** Qwen2.5-Coder-7B-Instruct is a 7-billion-parameter model. Its original FP16 weights require approximately 14–15 GB of memory before accounting for additional runtime memory. This project configures 4-bit quantization for supported NVIDIA GPUs to reduce memory requirements.

## Installation 
#### 1. Clone the Repository 
```bash
git clone <YOUR_REPOSITORY_URL>
cd DeepLearning_V2
```

#### 2. Create a Virtual Environment
On Windows, run the following commands in PowerShell(cd to project folder):
```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
```

If PowerShell blocks script execution, activate the environment from Command Prompt instead:
```bash
.venv\Scripts\activate.bat
```

#### 3. Install Dependencies
With the virtual environment activated, install the required packages:
```bash
python -m pip install -r requirements.txt
```

The provided requirements file specifies PyTorch CUDA 12.8 wheels. A compatible NVIDIA driver is required to use CUDA.

To verify the installation:
```bash
python -c "import torch; print('PyTorch:', torch.__version__); print('CUDA available:', torch.cuda.is_available()); print('GPU:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU')"
```

If CUDA is unavailable, check the installed PyTorch build, NVIDIA driver, and GPU compatibility before running the model.

## Download 
The model files are not required to be committed to GitHub. Download them separately into the model_weights/ directory.

**Model:** [Qwen2.5-Coder-7B-Instruct](https://huggingface.co/Qwen/Qwen2.5-Coder-7B-Instruct/tree/main)

#### 1. Install the Hugging Face Hub Client
```bash
python -m pip install -U huggingface_hub
```

#### 2. Download the Model Files
Run the following Python command from the repository root:
```bash
python -c "from huggingface_hub import snapshot_download; snapshot_download(repo_id='Qwen/Qwen2.5-Coder-7B-Instruct', local_dir='model_weights')"
```

This downloads the model repository into model_weights/, including the configuration, tokenizer, weight shards, and model index.

The directory should contain files similar to the following:
```text
model_weights/
├── config.json
├── generation_config.json
├── model.safetensors.index.json
├── model-00001-of-00004.safetensors
├── model-00002-of-00004.safetensors
├── model-00003-of-00004.safetensors
├── model-00004-of-00004.safetensors
├── tokenizer.json
└── tokenizer_config.json
```

The exact file list may change between model revisions. Keep all files downloaded from the same repository revision.

## Generate
The `uet_coder.py` script accepts a Markdown problem description and an output path.

**Command**
```bash
python uet_coder.py --problem problems/problem01/problem.md --output problems/problem01/solutions/generated.py
```

The script loads the local model, prepares the problem prompt, generates Python code, and saves the generated solution to the specified output file.

The model directory and maximum number of new tokens can also be specified:

```bash
python uet_coder.py --problem problems/problem01/problem.md --output problems/problem01/solutions/generated.py --model_dir model_weights --max_tokens 256
```

The script detects the available compute device and configures model loading accordingly. On supported NVIDIA GPUs, it uses 4-bit NF4 quantization; otherwise, it can use Apple MPS or CPU execution.

CPU inference may be significantly slower and requires sufficient system memory.

## Evaluate Generated
The `uet_marker.py` script evaluates a Python solution using a JSON test-case file.

**Command**
```bash
python uet_marker.py --source_code_file problems/problem01/solutions/generated.py --test_cases problems/problem01/test01.json
```

**Test-Case Format**

Example:

```text
{
    "function_name": "sum_of_two_largest",
    "test_cases": [
        {
            "parameters": {
                "nums": [1, 2, 3, 4, 5]
            },
            "expected_output": 9
        },
        {
            "parameters": {
                "nums": [1, 2, 3, 4, 0, 6]
            },
            "expected_output": 10
        }
    ]
}
```

The marker executes the specified function with each test case's parameters and compares the returned value with the expected output.

The evaluation report includes:
- The result of each test case.
- The number of passed and failed test cases.
- The overall score as a percentage.

For example, if 8 out of 10 test cases pass, the score is 80%.

**Important:** The marker is intended for trusted code in a controlled environment. It executes generated Python using exec() and should not be used to run untrusted code on a machine containing sensitive data.

## Notes
- Offline execution: Once the model files and required dependencies are available locally, inference can be performed locally without making requests to the Hugging Face model repository. 
- Reproducibility: Keep the model revision and Python dependency versions consistent when comparing results.
- Generated code: Always test generated solutions against the provided test cases. Passing the supplied tests does not guarantee correctness on unseen inputs.

## References
- [Qwen2.5-Coder-7B-Instruct — Hugging Face](https://huggingface.co/Qwen/Qwen2.5-Coder-7B-Instruct)
- [Hugging Face Transformers Documentation](https://huggingface.co/docs/transformers)
- [PyTorch Installation Guide](https://pytorch.org/get-started/locally/)
