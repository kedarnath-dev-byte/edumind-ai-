"""
@module     BaseFineTuner
@description Abstract base class for all fine-tuning frameworks in EduMind AI.
             Defines the contract that every fine-tuner must follow.
             Implements SOLID Open/Closed Principle — open for extension,
             closed for modification.
@author     EduMind AI Engineering
"""

from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseFineTuner(ABC):

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.model = None
        self.tokenizer = None

    @abstractmethod
    def load_model(self) -> None:
        """Load the base model and tokenizer from HuggingFace."""
        pass

    @abstractmethod
    def prepare_dataset(self, data_path: str) -> Any:
        """Load and tokenize the training dataset."""
        pass

    @abstractmethod
    def train(self, dataset: Any) -> Dict[str, Any]:
        """Run the fine-tuning training loop."""
        pass

    def get_framework_name(self) -> str:
        return self.__class__.__name__

    def summary(self) -> Dict[str, Any]:
        return {
            "framework": self.get_framework_name(),
            "config": self.config,
            "model_loaded": self.model is not None,
        }