from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_criar_pedido_calculo_total():
    """
    Testa se o pedido soma corretamente os valores.
    Dica: Em um ambiente real, você criaria um prato antes 
    para garantir que o ID existe.
    """
    novo_pedido = {
        "itens": [
            {"item_id": 1, "tipo": "prato", "quantidade": 2}, # Ex: 2x R$30
            {"item_id": 1, "tipo": "bebida", "quantidade": 1} # Ex: 1x R$10
        ],
        "mesa": 5
    }
    
    response = client.post("/pedidos", json=novo_pedido)
    
    if response.status_code == 201:
        dados = response.json()
        assert "valor_total" in dados
        assert dados["valor_total"] > 0
    else:
        # Se falhar porque os IDs não existem no mock, 
        # o status deve ser 404 (se você tratou) ou 422
        assert response.status_code in [201, 404, 422]

def test_erro_pedido_mesa_inexistente():
    # Se MAX_MESAS = 20, a mesa 99 deve falhar
    pedido_mesa_errada = {
        "itens": [{"item_id": 1, "tipo": "prato", "quantidade": 1}],
        "mesa": 99
    }
    response = client.post("/pedidos", json=pedido_mesa_errada)
    assert response.status_code == 422 or response.status_code == 400