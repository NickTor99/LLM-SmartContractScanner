from llm.hf_llm import HFLLM
from llm.openai_llm import OpenAILLM

class LLMFactory:
    @staticmethod
    def build(model_config: dict):
        source = model_config.get("source")

        if source == "huggingface":
            return HFLLM(
                model_name=model_config["model_name"],
                device=model_config.get("device", "auto")
            )

        elif source == "openai":
            return OpenAILLM(
                api_key=model_config["api_key"],
                model_name=model_config.get("model_name", "gpt-4"),
                base_url=model_config.get("base_url", None)
            )

        else:
            raise ValueError(f"Fonte del modello LLM non supportata: {source}")

