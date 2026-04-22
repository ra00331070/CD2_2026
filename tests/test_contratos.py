# @title
# tests/test_contratos.py
# A fixture 'client' vem do conftest.py — não é necessário redeclará-la aqui.


def test_contrato_get_prato(client):
    response = client.get("/pratos/1")
    assert response.status_code == 200
    prato = response.json()

    campos_obrigatorios = {"id", "nome", "categoria", "preco", "disponivel"}
    assert campos_obrigatorios.issubset(prato.keys())

    assert isinstance(prato["id"], int)
    assert isinstance(prato["nome"], str)
    assert isinstance(prato["categoria"], str)
    assert isinstance(prato["preco"], (int, float))
    assert isinstance(prato["disponivel"], bool)
    assert prato["preco"] > 0
    assert len(prato["nome"]) >= 3


def test_contrato_post_prato(client):
    novo = {
        "nome": "Prato Contrato Teste",
        "categoria": "massa",
        "preco": 45.0
    }
    response = client.post("/pratos", json=novo)
    assert response.status_code in [200, 201]
    prato = response.json()

    assert "id" in prato
    assert isinstance(prato["id"], int)
    assert prato["nome"] == "Prato Contrato Teste"

    if "criado_em" in prato:
        assert isinstance(prato["criado_em"], str)
        assert len(prato["criado_em"]) > 0


def test_contrato_erro_404(client):
    response = client.get("/pratos/9999")
    assert response.status_code == 404
    corpo = response.json()

    # A API pode usar 'detail' (padrão FastAPI) ou 'erro' (handler customizado)
    assert "detail" in corpo or "erro" in corpo
    mensagem = corpo.get("detail") or corpo.get("erro")
    assert isinstance(mensagem, str)
    assert len(mensagem) > 0


def test_contrato_erro_422(client):
    # Payload com múltiplos erros para garantir estrutura rica na resposta
    response = client.post("/pratos", json={"nome": "X", "preco": -1})
    assert response.status_code == 422
    corpo = response.json()

    # Formato padrão do FastAPI: {"detail": [...]}
    # Handler customizado pode usar: {"detalhes": [...]}
    erros = corpo.get("detail") or corpo.get("detalhes")
    assert erros is not None, "Resposta 422 deve conter 'detail' ou 'detalhes'"
    assert isinstance(erros, list), "Os erros devem ser uma lista"
    assert len(erros) > 0, "Deve haver pelo menos um erro reportado"

    # Verifica a estrutura de cada erro (formato padrão FastAPI)
    if "detail" in corpo:
        for erro in erros:
            assert "loc" in erro, "Cada erro deve ter 'loc' (localização)"
            assert "msg" in erro, "Cada erro deve ter 'msg' (mensagem)"
            assert isinstance(erro["loc"], list)
            assert isinstance(erro["msg"], str)
            assert len(erro["msg"]) > 0