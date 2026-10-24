import argparse
import re
import time
from pathlib import Path

import torch
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    GenerationConfig,
    BitsAndBytesConfig,
)

def detect_device():
    """Detect the available device and configure model loading."""

    if torch.cuda.is_available():
        device_name = torch.cuda.get_device_name(0)
        total_vram = (
            torch.cuda.get_device_properties(0).total_memory
            / (1024 ** 3)
        )

        print(">>> Compute device: NVIDIA GPU (CUDA)")
        print(f">>> GPU: {device_name}")
        print(f">>> Total VRAM: {total_vram:.1f} GB")
        print(">>> Model quantization: 4-bit NF4")

        quantization_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_use_double_quant=True,
            bnb_4bit_compute_dtype=torch.float16,
        )

        return {
            "torch_dtype": torch.float16,
            "device_map": "auto",
            "quantization_config": quantization_config,
            "max_memory": {0: "7GiB", "cpu": "24GiB"},
        }

    if hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
        print(">>> Compute device: Apple GPU (MPS)")

        return {
            "torch_dtype": torch.float16,
            "device_map": {"": "mps"},
        }

    print(">>> No supported GPU detected; using CPU.")
    print(">>> Warning: 7B FP32 inference may require substantial RAM.")

    return {
        "torch_dtype": torch.float32,
        "device_map": {"": "cpu"},
    }


def load_model(model_dir="model_weights"):
    model_path = Path(model_dir)
    if not model_path.exists():
        raise FileNotFoundError(
            f"Model directory not found: {model_path.resolve()}\n"
            "Download the complete model repository into this directory first."
        )

    load_config = detect_device()

    print(f">>> Loading tokenizer from: {model_path.resolve()}")
    tokenizer = AutoTokenizer.from_pretrained(
        str(model_path),
        trust_remote_code=True,
    )

    if tokenizer.pad_token_id is None and tokenizer.eos_token_id is not None:
        tokenizer.pad_token = tokenizer.eos_token

    print(">>> Loading model (this may take a while)...")

    model = AutoModelForCausalLM.from_pretrained(
        str(model_path),
        low_cpu_mem_usage=True,
        trust_remote_code=True,
        use_safetensors=True,
        **load_config,
    )

    model.eval()

    devices = sorted({str(parameter.device) for parameter in model.parameters()})
    print(f">>> Model loaded. Parameter devices: {', '.join(devices)}")
    if any(device.startswith("cuda") for device in devices):
        print(">>> CUDA GPU is being used for at least part of the model.")
    elif any(device == "mps" for device in devices):
        print(">>> Apple GPU (MPS) is being used.")
    else:
        print(">>> Model parameters are running on CPU.")

    return tokenizer, model


def build_model_inputs(tokenizer, prompt, model):
    """Use the model's chat template when available (recommended for Qwen Instruct)."""
    if getattr(tokenizer, "chat_template", None):
        messages = [
            {
                "role": "system",
                "content": (
                    "You are an expert programming assistant. Solve the programming "
                    "problem and return a complete Python solution. Prefer code only; "
                    "do not wrap the answer in Markdown fences."
                ),
            },
            {"role": "user", "content": prompt},
        ]
        formatted_prompt = tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
        )
        inputs = tokenizer(
            formatted_prompt,
            return_tensors="pt",
            truncation=True,
            max_length=4096,
        )
    else:
        inputs = tokenizer(
            prompt,
            return_tensors="pt",
            truncation=True,
            max_length=4096,
        )

    input_device = getattr(model, "device", torch.device("cpu"))
    return {key: value.to(input_device) for key, value in inputs.items()}


def generate_code(model, tokenizer, prompt, max_new_tokens=1024):
    print(">>> Tokenizing input...")
    inputs = build_model_inputs(tokenizer, prompt, model)

    print(">>> Generating code...")
    start_time = time.time()
    gen_config = GenerationConfig(
        max_new_tokens=max_new_tokens,
        do_sample=False,
        pad_token_id=tokenizer.pad_token_id,
        eos_token_id=tokenizer.eos_token_id,
    )

    with torch.inference_mode():
        outputs = model.generate(**inputs, generation_config=gen_config)

    # Decode only newly generated tokens, not the original prompt.
    input_length = inputs["input_ids"].shape[1]
    generated_tokens = outputs[0][input_length:]
    code = tokenizer.decode(generated_tokens, skip_special_tokens=True).strip()

    elapsed = time.time() - start_time
    print(f">>> Code generation time: {elapsed:.2f}s")
    if torch.cuda.is_available():
        allocated = torch.cuda.memory_allocated() / (1024 ** 3)
        reserved = torch.cuda.memory_reserved() / (1024 ** 3)
        print(f">>> CUDA memory: {allocated:.2f} GB allocated / {reserved:.2f} GB reserved")

    return code


def extract_python_code(text):
    pattern = r"```(?:python)?\s*(.*?)```"
    matches = re.findall(pattern, text, flags=re.DOTALL | re.IGNORECASE)
    if matches:
        return "\n".join(match.strip() for match in matches)
    return text.strip()


def main():
    parser = argparse.ArgumentParser(
        description="Generate a Python solution using a local Hugging Face causal language model."
    )
    parser.add_argument(
        "--problem", type=str, required=True,
        help="Path to problem.md",
    )
    parser.add_argument(
        "--output", type=str, required=True,
        help="Path to save solution.py",
    )
    parser.add_argument(
        "--model_dir", type=str, default="model_weights",
        help="Directory containing the downloaded model files (default: model_weights)",
    )
    parser.add_argument(
        "--max_tokens", type=int, default=256,
        help="Maximum number of new tokens to generate",
    )
    args = parser.parse_args()

    with open(args.problem, "r", encoding="utf-8") as file:
        prompt = file.read().strip()

    tokenizer, model = load_model(args.model_dir)
    raw_code = generate_code(model, tokenizer, prompt, max_new_tokens=args.max_tokens)
    python_code = extract_python_code(raw_code)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(python_code + "\n", encoding="utf-8")
    print(f">>> Code generated and saved to {output_path.resolve()}")


if __name__ == "__main__":
    main()
