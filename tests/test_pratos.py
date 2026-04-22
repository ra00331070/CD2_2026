import pytest
from fastapi.testclient import TestClient

# --- SMOKE TESTS (Caminho Feliz / Disponibilidade) ---

@pytest.mark.smoke
def test_raiz_retorna_200(client):
    """Verifica se a API está online."""
    response = client.get("/")
    assert response.status_code == 200
    assert "restaurante" in response.json()

@pytest.mark.smoke
def test_listar_pratos_vazio_ou_populado(client):
    """Verifica se a rota de listagem responde corretamente."""
    response = client.get("/pratos")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


# --- TESTES DE VALIDAÇÃO (Regras de Negócio e Erros) ---

@pytest.mark.validacao
def test_criar_prato_com_sucesso(client, prato_valido):
    """Testa o cadastro de um prato com dados perfeitos."""
    response = client.post("/pratos", json=prato_valido)
    assert response.status_code in [200, 201]
    dados = response.json()
    assert dados["nome"] == prato_valido["nome"]
    assert "id" in dados

@pytest.mark.validacao
def test_erro_id_inexistente(client):
    response = client.get("/pratos/999999")
    print(f"Status: {response.status_code}")
    print(f"Corpo: {response.text}") # Veja o que está vindo aqui
    assert response.status_code == 404
    
@pytest.mark.validacao
@pytest.mark.parametrize("campo, valor_invalido", [
    ("preco", -5.0),            # Preço negativo (gt=0)
    ("preco", 0.0),             # Preço zero (gt=0)
    ("categoria", "japonesa"),  # Categoria fora do Enum/Literal permitido
    ("nome", "Ab"),             # Nome curto demais (min_length=3)
    ("nome", "A" * 101),        # Nome longo demais (max_length=100)
])
def test_validacoes_pydantic_pratos(client, prato_valido, campo, valor_invalido):
    """Caso de Erro: Testa múltiplos disparos de erro 422 (Unprocessable Entity)."""
    prato_valido[campo] = valor_invalido
    response = client.post("/pratos", json=prato_valido)
    assert response.status_code == 422

@pytest.mark.validacao
def test_erro_preco_promocional_maior_que_original(client, prato_valido):
    """
    Caso de Erro: Validação customizada (@model_validator).
    O preço promocional não pode ser maior que o preço base.
    """
    prato_valido["preco"] = 50.0
    prato_valido["preco_promocional"] = 60.0 # Inválido
    
    response = client.post("/pratos", json=prato_valido)
    assert response.status_code == 422

@pytest.mark.validacao
def test_filtro_categoria_funciona(client, prato_valido):
    """Verifica se o Query Parameter 'categoria' realmente filtra os resultados."""
    # 1. Garante que existe um prato da categoria 'sobremesa'
    prato_valido["categoria"] = "sobremesa"
    client.post("/pratos", json=prato_valido)
    
    # 2. Filtra
    response = client.get("/pratos?categoria=sobremesa")
    dados = response.json()
    
    assert response.status_code == 200
    assert len(dados) > 0
    for prato in dados:
        assert prato["categoria"] == "sobremesa"

@pytest.mark.validacao
def test_alterar_disponibilidade_sucesso(client, prato_valido):
    """Testa a rota PUT de alteração de estado."""
    # Cria um prato primeiro
    res_post = client.post("/pratos", json=prato_valido)
    prato_id = res_post.json()["id"]
    
    # Altera para indisponível
    response = client.put(f"/pratos/{prato_id}/disponibilidade", json={"disponivel": False})
    assert response.status_code == 200
    assert response.json()["disponivel"] is False