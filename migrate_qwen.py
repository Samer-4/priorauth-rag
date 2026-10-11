"""Minimal Qwen migration; run from the Prior-Auth-Appeals repository root."""
from pathlib import Path
import re
import subprocess

root = Path.cwd()
assert (root / 'src/stage1_extraction.py').exists(), 'Run this from the repository root.'
assert (root / 'pyproject.toml').exists(), 'pyproject.toml missing.'

adapter = '''import json
from types import SimpleNamespace


class QwenClient:
    def __init__(self, model_id="Qwen/Qwen3-8B"):
        import torch
        from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig

        self.torch = torch
        self.tokenizer = AutoTokenizer.from_pretrained(model_id)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_id,
            device_map="auto",
            quantization_config=BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_compute_dtype=torch.float16,
            ),
            torch_dtype=torch.float16,
        )
        self.model.eval()
        self.messages = self

    def _generate(self, messages, max_tokens, output_format=None):
        from pydantic import TypeAdapter

        chat = list(messages)
        if output_format is not None:
            schema = TypeAdapter(output_format).json_schema()
            chat = [{
                "role": "system",
                "content": (
                    "Return only valid JSON matching this JSON schema. "
                    "Do not invent missing information.\\n"
                    + json.dumps(schema)
                ),
            }] + chat

        prompt = self.tokenizer.apply_chat_template(
            chat,
            tokenize=False,
            add_generation_prompt=True,
            enable_thinking=False,
        )
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
        with self.torch.inference_mode():
            output = self.model.generate(
                **inputs,
                max_new_tokens=max_tokens,
                do_sample=False,
                pad_token_id=self.tokenizer.eos_token_id,
            )
        generated = output[0][inputs["input_ids"].shape[-1]:]
        return self.tokenizer.decode(generated, skip_special_tokens=True).strip()

    def parse(self, *, model=None, max_tokens, messages, output_format, **kwargs):
        from pydantic import TypeAdapter

        text = self._generate(messages, max_tokens, output_format)
        parsed = TypeAdapter(output_format).validate_json(text)
        return SimpleNamespace(parsed_output=parsed)

    def create(self, *, model=None, max_tokens, messages, **kwargs):
        text = self._generate(messages, max_tokens)
        return SimpleNamespace(content=[SimpleNamespace(type="text", text=text)])


_client = None


def get_client():
    global _client
    if _client is None:
        _client = QwenClient()
    return _client
'''

paths = [root / 'src' / f'stage{i}_{name}.py' for i, name in [
    (1, 'extraction'), (2, 'lookup'), (3, 'evidence_extraction'),
    (4, 'sufficiency_judgement'), (5, 'generation'), (6, 'verification')
]]
paths.append(root / 'smoke_test.py')

# Validate all substitutions before writing anything.
changes = {}
for path in paths:
    source = path.read_text()
    if 'import anthropic' not in source or 'client = anthropic.Anthropic()' not in source:
        raise RuntimeError(f'Expected Claude initialization not found in {path}')
    new_import = 'from src.llm_client import get_client' if path.name == 'smoke_test.py' else 'from llm_client import get_client'
    updated = source.replace('import anthropic', new_import, 1)
    updated = updated.replace('client = anthropic.Anthropic()', 'client = get_client()', 1)
    changes[path] = updated

project = root / 'pyproject.toml'
project_text = project.read_text()
required = ['torch>=2.5', 'transformers>=4.51.0,<5', 'accelerate>=1.0', 'bitsandbytes>=0.45']
for dependency in required:
    if not re.search(r'^\s*"' + re.escape(dependency.split('>')[0]) + r'[<>=]', project_text, re.M):
        project_text = project_text.replace('dependencies = [', f'dependencies = [\n    "{dependency}",', 1)
changes[project] = project_text

(root / 'src' / 'llm_client.py').write_text(adapter)
for path, content in changes.items():
    path.write_text(content)

subprocess.run(['python', '-m', 'compileall', '-q', 'src', 'smoke_test.py'], check=True)
print('Migration applied. Stage prompts, schemas, and verification logic were not edited.')
print('Review changes with: git diff -- src pyproject.toml smoke_test.py')
