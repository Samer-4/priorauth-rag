import json
from types import SimpleNamespace


class QwenClient:
    def __init__(self, model_id="Qwen/Qwen3-8B"):
        self.model_id = model_id
        self.model = None
        self.messages = self

    def _load_model(self):
        global _active_client

        if self.model is not None:
            return

        import gc
        import torch
        from transformers import AutoTokenizer, BitsAndBytesConfig

        # Keep only one large model in GPU memory at a time.
        if _active_client is not None and _active_client is not self:
            _active_client.model = None
            _active_client.tokenizer = None
            gc.collect()
            torch.cuda.empty_cache()
            _active_client = None

        if "Qwen3.5" in self.model_id:
            from transformers import Qwen3_5ForCausalLM
            model_class = Qwen3_5ForCausalLM
        else:
            from transformers import AutoModelForCausalLM
            model_class = AutoModelForCausalLM

        self.torch = torch
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_id)
        self.model = model_class.from_pretrained(
            self.model_id,
            device_map="auto",
            quantization_config=BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_compute_dtype=torch.float16,
            ),
            dtype=torch.float16,
            low_cpu_mem_usage=True,
        )
        self.model.eval()
        _active_client = self

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
        device = self.model.get_input_embeddings().weight.device
        inputs = self.tokenizer(prompt, return_tensors="pt").to(device)
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
        payload = json.loads(text)

        if (
            isinstance(payload, dict)
            and isinstance(payload.get("items"), list)
            and TypeAdapter(output_format).json_schema().get("type") == "array"
        ):
            payload = payload["items"]

        parsed = TypeAdapter(output_format).validate_python(payload)
        return SimpleNamespace(parsed_output=parsed)

    def create(self, *, model=None, max_tokens, messages, **kwargs):
        text = self._generate(messages, max_tokens)
        return SimpleNamespace(content=[SimpleNamespace(type="text", text=text)])


_clients = {}
_active_client = None


def get_client(model_id="Qwen/Qwen3-8B"):
    if model_id not in _clients:
        _clients[model_id] = QwenClient(model_id)
    return _clients[model_id]
