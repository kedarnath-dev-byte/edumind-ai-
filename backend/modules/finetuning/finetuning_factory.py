"""
@module     FineTunerFactory
@description Factory class for instantiating any of the 8 fine-tuning
             frameworks by name. Implements the Factory Design Pattern —
             decouples framework selection from business logic.
             Add new frameworks here without changing any other file.
@author     EduMind AI Engineering
"""

from typing import Any, Dict
from .base_finetuner import BaseFineTuner
from .sft_finetuner import SFTFineTuner
from .lora_finetuner import LoRAFineTuner
from .qlora_finetuner import QLoRAFineTuner
from .dpo_finetuner import DPOFineTuner
from .adapter_finetuner import AdapterFineTuner
from .prefix_tuning_finetuner import PrefixTuningFineTuner
from .rlhf_finetuner import RLHFFineTuner
from .peft_finetuner import PEFTFineTuner


# Registry maps string names → classes
# To add a new framework: just add one line here. Nothing else changes.
FINETUNER_REGISTRY: Dict[str, Any] = {
    "sft": SFTFineTuner,
    "lora": LoRAFineTuner,
    "qlora": QLoRAFineTuner,
    "dpo": DPOFineTuner,
    "adapter": AdapterFineTuner,
    "prefix_tuning": PrefixTuningFineTuner,
    "rlhf": RLHFFineTuner,
    "peft": PEFTFineTuner,
}


class FineTunerFactory:
    """
    Factory for creating fine-tuner instances by name.
    Usage:
        tuner = FineTunerFactory.get("lora", config)
        tuner.load_model()
        dataset = tuner.prepare_dataset("data/train.jsonl")
        results = tuner.train(dataset)
    """

    @staticmethod
    def get(framework: str, config: Dict[str, Any]) -> BaseFineTuner:
        """
        Returns an instance of the requested fine-tuner.

        Args:
            framework: One of: sft, lora, qlora, dpo, adapter,
                       prefix_tuning, rlhf, peft
            config:    Dictionary of hyperparameters.

        Returns:
            An instance of the requested BaseFineTuner subclass.

        Raises:
            ValueError: If the framework name is not recognised.
        """
        framework = framework.lower().strip()
        if framework not in FINETUNER_REGISTRY:
            available = list(FINETUNER_REGISTRY.keys())
            raise ValueError(
                f"Unknown framework '{framework}'. "
                f"Available options: {available}"
            )
        return FINETUNER_REGISTRY[framework](config)

    @staticmethod
    def list_frameworks() -> list:
        """Returns a list of all available fine-tuning framework names."""
        return list(FINETUNER_REGISTRY.keys())