from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_listar_bebidas_sucesso():
    response = client.get("/bebidas")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_cadastrar_bebida_valida():
    nova_bebida = {
        "nome": "Suco de Uva Integral",
        "tipo": "suco",
        "preco": 12.50,
        "volume_ml": 500,
        "alcoolica": False
    }
    response = client.post("/bebidas", json=nova_bebida)
    assert response.status_code == 201  # Ou 200, dependendo da sua rota
    assert response.json()["nome"] == "Suco de Uva Integral"

def test_erro_bebida_volume_invalido():
    # Testando a validação: volume deve ser entre 50 e 2000ml
    bebida_ruim = {
        "nome": "Super Drink",
        "tipo": "suco",
        "preco": 10.0,
        "volume_ml": 5000  # Valor acima do permitido
    }
    response = client.post("/bebidas", json=bebida_ruim)
    assert response.status_code == 422  # Erro de validação do Pydantic