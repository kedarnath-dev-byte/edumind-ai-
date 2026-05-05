"""
@module     test_serving.py
@description Test suite for all 5 serving engines in EduMind AI.
             Tests: FastAPI, TorchServe, Triton, BentoML, vLLM servers.
             Covers: load_model, predict, health_check, factory pattern.
             Target: 25/25 tests passing.
@author     EduMind AI Engineering
"""

import pytest
from modules.serving.fastapi_server import FastAPIServer
from modules.serving.torchserve_server import TorchServeServer
from modules.serving.triton_server import TritonServer
from modules.serving.bentoml_server import BentoMLServer
from modules.serving.vllm_server import VLLMServer
from modules.serving.serving_factory import ServingFactory


# ─────────────────────────────────────
# SHARED TEST DATA
# ─────────────────────────────────────
MODEL_NAME = "test-model"
MODEL_PATH = "models/test-model"
INPUT_DATA = {"query": "What is machine learning?"}


# ─────────────────────────────────────
# FASTAPI SERVER TESTS
# ─────────────────────────────────────
class TestFastAPIServer:

    def test_load_model(self):
        server = FastAPIServer(MODEL_NAME, MODEL_PATH)
        result = server.load_model()
        assert result is True
        assert server.is_loaded is True

    def test_predict(self):
        server = FastAPIServer(MODEL_NAME, MODEL_PATH)
        server.load_model()
        result = server.predict(INPUT_DATA)
        assert result["status"] == "success"
        assert result["server"] == "FastAPIServer"
        assert "output" in result

    def test_health_check(self):
        server = FastAPIServer(MODEL_NAME, MODEL_PATH)
        server.load_model()
        result = server.health_check()
        assert result["status"] == "healthy"
        assert result["is_loaded"] is True

    def test_predict_without_load_raises(self):
        server = FastAPIServer(MODEL_NAME, MODEL_PATH)
        with pytest.raises(RuntimeError):
            server.predict(INPUT_DATA)

    def test_get_server_info(self):
        server = FastAPIServer(MODEL_NAME, MODEL_PATH)
        info = server.get_server_info()
        assert info["server_type"] == "FastAPIServer"
        assert info["model_name"] == MODEL_NAME


# ─────────────────────────────────────
# TORCHSERVE SERVER TESTS
# ─────────────────────────────────────
class TestTorchServeServer:

    def test_load_model(self):
        server = TorchServeServer(MODEL_NAME, MODEL_PATH)
        result = server.load_model()
        assert result is True
        assert server.is_loaded is True

    def test_predict(self):
        server = TorchServeServer(MODEL_NAME, MODEL_PATH)
        server.load_model()
        result = server.predict(INPUT_DATA)
        assert result["status"] == "success"
        assert result["server"] == "TorchServeServer"

    def test_health_check(self):
        server = TorchServeServer(MODEL_NAME, MODEL_PATH)
        server.load_model()
        result = server.health_check()
        assert result["status"] == "healthy"

    def test_predict_without_load_raises(self):
        server = TorchServeServer(MODEL_NAME, MODEL_PATH)
        with pytest.raises(RuntimeError):
            server.predict(INPUT_DATA)

    def test_get_server_info(self):
        server = TorchServeServer(MODEL_NAME, MODEL_PATH)
        info = server.get_server_info()
        assert info["server_type"] == "TorchServeServer"


# ─────────────────────────────────────
# TRITON SERVER TESTS
# ─────────────────────────────────────
class TestTritonServer:

    def test_load_model(self):
        server = TritonServer(MODEL_NAME, MODEL_PATH)
        result = server.load_model()
        assert result is True
        assert server.is_loaded is True

    def test_predict(self):
        server = TritonServer(MODEL_NAME, MODEL_PATH)
        server.load_model()
        result = server.predict(INPUT_DATA)
        assert result["status"] == "success"
        assert result["server"] == "TritonServer"

    def test_health_check(self):
        server = TritonServer(MODEL_NAME, MODEL_PATH)
        server.load_model()
        result = server.health_check()
        assert result["status"] == "healthy"

    def test_predict_without_load_raises(self):
        server = TritonServer(MODEL_NAME, MODEL_PATH)
        with pytest.raises(RuntimeError):
            server.predict(INPUT_DATA)

    def test_get_server_info(self):
        server = TritonServer(MODEL_NAME, MODEL_PATH)
        info = server.get_server_info()
        assert info["server_type"] == "TritonServer"


# ─────────────────────────────────────
# BENTOML SERVER TESTS
# ─────────────────────────────────────
class TestBentoMLServer:

    def test_load_model(self):
        server = BentoMLServer(MODEL_NAME, MODEL_PATH)
        result = server.load_model()
        assert result is True
        assert server.is_loaded is True

    def test_predict(self):
        server = BentoMLServer(MODEL_NAME, MODEL_PATH)
        server.load_model()
        result = server.predict(INPUT_DATA)
        assert result["status"] == "success"
        assert result["server"] == "BentoMLServer"

    def test_health_check(self):
        server = BentoMLServer(MODEL_NAME, MODEL_PATH)
        server.load_model()
        result = server.health_check()
        assert result["status"] == "healthy"

    def test_predict_without_load_raises(self):
        server = BentoMLServer(MODEL_NAME, MODEL_PATH)
        with pytest.raises(RuntimeError):
            server.predict(INPUT_DATA)

    def test_get_server_info(self):
        server = BentoMLServer(MODEL_NAME, MODEL_PATH)
        info = server.get_server_info()
        assert info["server_type"] == "BentoMLServer"


# ─────────────────────────────────────
# VLLM SERVER TESTS
# ─────────────────────────────────────
class TestVLLMServer:

    def test_load_model(self):
        server = VLLMServer(MODEL_NAME, MODEL_PATH)
        result = server.load_model()
        assert result is True
        assert server.is_loaded is True

    def test_predict(self):
        server = VLLMServer(MODEL_NAME, MODEL_PATH)
        server.load_model()
        result = server.predict(INPUT_DATA)
        assert result["status"] == "success"
        assert result["server"] == "VLLMServer"
        assert result["algorithm"] == "PagedAttention"

    def test_health_check(self):
        server = VLLMServer(MODEL_NAME, MODEL_PATH)
        server.load_model()
        result = server.health_check()
        assert result["status"] == "healthy"

    def test_predict_without_load_raises(self):
        server = VLLMServer(MODEL_NAME, MODEL_PATH)
        with pytest.raises(RuntimeError):
            server.predict(INPUT_DATA)

    def test_get_server_info(self):
        server = VLLMServer(MODEL_NAME, MODEL_PATH)
        info = server.get_server_info()
        assert info["server_type"] == "VLLMServer"


# ─────────────────────────────────────
# SERVING FACTORY TESTS
# ─────────────────────────────────────
class TestServingFactory:

    def test_get_fastapi_server(self):
        server = ServingFactory.get_server("fastapi", MODEL_NAME, MODEL_PATH)
        assert isinstance(server, FastAPIServer)

    def test_get_torchserve_server(self):
        server = ServingFactory.get_server("torchserve", MODEL_NAME, MODEL_PATH)
        assert isinstance(server, TorchServeServer)

    def test_get_triton_server(self):
        server = ServingFactory.get_server("triton", MODEL_NAME, MODEL_PATH)
        assert isinstance(server, TritonServer)

    def test_get_bentoml_server(self):
        server = ServingFactory.get_server("bentoml", MODEL_NAME, MODEL_PATH)
        assert isinstance(server, BentoMLServer)

    def test_get_vllm_server(self):
        server = ServingFactory.get_server("vllm", MODEL_NAME, MODEL_PATH)
        assert isinstance(server, VLLMServer)

    def test_invalid_engine_raises(self):
        with pytest.raises(ValueError):
            ServingFactory.get_server("unknown_engine", MODEL_NAME, MODEL_PATH)

    def test_list_engines(self):
        engines = ServingFactory.list_engines()
        assert "fastapi" in engines
        assert "torchserve" in engines
        assert "triton" in engines
        assert "bentoml" in engines
        assert "vllm" in engines

