import json
from types import SimpleNamespace


class QwenClient:
    def __init__(self, model_id="Qwen/Qwen3-8B"):
        self.model_id = model_id
        self.model = None
        self.messages = self

    def _load_model(self):
        if self.model is not None:
            return

        import torch
        from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig

        self.torch = torch
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_id)
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_id,
            device_map="auto",
            quantization_config=BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_compute_dtype=torch.float16,
            ),
            torch_dtype=torch.float16,
        )
        self.model.eval()

    def _generate(self, messages, max_tokens, output_format=None):
        self._load_model()
        from pydantic import TypeAdapter

        chat = list(messages)
        if output_format is not None:
            schema = TypeAdapter(output_format).json_schema()
            chat = [{
                "role": "system",
                "content": (
                    "Return only valid JSON matching this JSON schema. "
                    "Do not invent missing information.\n"
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
