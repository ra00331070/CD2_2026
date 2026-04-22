# @title
# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from main import app   # ajuste se necessário


@pytest.fixture
def client():
    """
    Cria um novo TestClient para cada função de teste.
    Fixtures sem escopo explícito têm escopo 'function' por padrão —
    ou seja, são recriadas a cada teste.

    Importante: isso melhora a organização e evita variável global,
    mas NÃO reinicializa o estado interno da aplicação. Se a API
    mantém dados em listas globais, esses dados persistem entre testes.
    A solução é escrever testes que verificam comportamentos relativos
    (veja o Exercício 4.2), não testes que assumem estado absoluto.
    """
    return TestClient(app)


@pytest.fixture
def prato_valido():
    """Payload de prato válido para reutilizar nos testes."""
    return {
        "nome": "Prato de Fixture",
        "categoria": "massa",
        "preco": 45.0,
        "disponivel": True
    }


@pytest.fixture
def bebida_valida():
    """Payload de bebida válida para reutilizar nos testes."""
    return {
        "nome": "Água de Fixture",
        "tipo": "agua",
        "preco": 8.0,
        "alcoolica": False,
        "volume_ml": 500
    }


