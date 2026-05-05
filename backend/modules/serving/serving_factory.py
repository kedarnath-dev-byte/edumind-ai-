"""
@module     serving_factory.py
@description Factory class for creating model serving engine instances.
             Follows the Strategy Pattern — caller picks which serving
             engine to use at runtime without changing any other code.
             Supports: FastAPI, TorchServe, Triton, BentoML, vLLM.
             Same pattern used in finetuning_factory.py (Feature 6).
@author     EduMind AI Engineering
"""

from typing import Any, Dict
from backend.modules.serving.base_server import BaseServer
from backend.modules.serving.fastapi_server import FastAPIServer
from backend.modules.serving.torchserve_server import TorchServeServer
from backend.modules.serving.triton_server import TritonServer
from backend.modules.serving.bentoml_server import BentoMLServer
from backend.modules.serving.vllm_server import VLLMServer


# Registry of all available serving engines
SERVING_ENGINES = {
    "fastapi": FastAPIServer,
    "torchserve": TorchServeServer,
    "triton": TritonServer,
    "bentoml": BentoMLServer,
    "vllm": VLLMServer,
}


class ServingFactory:
    """
    Factory class that creates the correct serving engine on demand.
    Caller passes engine name as a string — factory returns ready instance.
    """

    @staticmethod
    def get_server(
        engine: str,
        model_name: str,
        model_path: str
    ) -> BaseServer:
        """
        Get a serving engine instance by name.

        Args:
            engine (str): One of: fastapi, torchserve, triton, bentoml, vllm
            model_name (str): Human-readable model name.
            model_path (str): Path or identifier to load model from.

        Returns:
            BaseServer: Ready-to-use serving engine instance.

        Raises:
            ValueError: If engine name is not recognized.
        """
        try:
            engine_key = engine.lower().strip()
            if engine_key not in SERVING_ENGINES:
                raise ValueError(
                    f"Unknown serving engine: '{engine}'. "
                    f"Available: {list(SERVING_ENGINES.keys())}"
                )
            server_class = SERVING_ENGINES[engine_key]
            return server_class(model_name=model_name, model_path=model_path)
        except ValueError:
            raise
        except Exception as e:
            raise RuntimeError(f"ServingFactory.get_server failed: {e}")

    @staticmethod
    def list_engines() -> Dict[str, Any]:
        """
        Return all available serving engines.

        Returns:
            Dict: Engine names and their class names.
        """
        return {
            name: cls.__name__
            for name, cls in SERVING_ENGINES.items()
        }