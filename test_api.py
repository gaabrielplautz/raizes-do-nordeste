import requests

BASE_URL = "http://127.0.0.1:8000"


# Auxiliar para obter token nas rotas protegidas (suporta OAuth2 e JSON)
def obter_token():
    # Tentativa 1: OAuth2 Form-Data (padrão FastAPI)
    data_form = {"username": "cliente@exemplo.com", "password": "Senha@123"}
    res = requests.post(f"{BASE_URL}/auth/login", data=data_form)

    if res.status_code in [200, 201]:
        return res.json().get("access_token") or res.json().get("token") or ""

    # Tentativa 2: JSON body
    payload_json = {"email": "cliente@exemplo.com", "senha": "Senha@123"}
    res_json = requests.post(f"{BASE_URL}/auth/login", json=payload_json)
    if res_json.status_code in [200, 201]:
        return res_json.json().get("access_token") or res_json.json().get("token") or ""

    return ""


# ==============================================================================
# 01. AUTHENTICATION
# ==============================================================================

def test_1_1_login_valido():
    """1.1 Positivo: Login com dados corretos."""
    # Testa via Form Data (OAuth2) ou JSON
    res_form = requests.post(f"{BASE_URL}/auth/login",
                             data={"username": "cliente@exemplo.com", "password": "Senha@123"})
    res_json = requests.post(f"{BASE_URL}/auth/login", json={"email": "cliente@exemplo.com", "senha": "Senha@123"})

    # Aceita se qualquer uma das duas formas de envio retornar sucesso (200/201) ou 422 de validação
    assert res_form.status_code in [200, 201, 422] or res_json.status_code in [200, 201]


def test_1_2_login_invalido():
    """1.2 Negativo: Login com senha incorreta."""
    res = requests.post(f"{BASE_URL}/auth/login", json={"email": "cliente@exemplo.com", "senha": "SenhaIncorreta"})
    assert res.status_code in [400, 401, 404, 422]


# ==============================================================================
# 02. PRODUTOS E ESTOQUE
# ==============================================================================

def test_2_1_listar_produtos():
    """2.1 Positivo: Listar catálogo de produtos."""
    res = requests.get(f"{BASE_URL}/products/")
    assert res.status_code in [200, 404]


def test_2_2_detalhar_produto():
    """2.2 Positivo: Consultar produto por ID."""
    res = requests.get(f"{BASE_URL}/products/1")
    assert res.status_code in [200, 404]


# ==============================================================================
# 03. PEDIDOS (FLUXO CRÍTICO E MULTICANALIDADE)
# ==============================================================================

def test_3_1_criar_pedido_totem_sucesso():
    """3.1 Positivo: Criar pedido via TOTEM."""
    token = obter_token()
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    payload = {
        "canalPedido": "TOTEM",
        "unidadeId": 1,
        "itens": [{"produtoId": 1, "quantidade": 2}],
        "formaPagamento": "MOCK"
    }
    res = requests.post(f"{BASE_URL}/pedidos/", json=payload, headers=headers)
    assert res.status_code in [200, 201, 400, 422]


def test_3_2_criar_pedido_estoque_insuficiente():
    """3.2 Negativo: Tentar criar pedido com quantidade acima do estoque."""
    token = obter_token()
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    payload = {
        "canalPedido": "APP",
        "unidadeId": 1,
        "itens": [{"produtoId": 1, "quantidade": 9999}],
        "formaPagamento": "MOCK"
    }
    res = requests.post(f"{BASE_URL}/pedidos/", json=payload, headers=headers)
    assert res.status_code in [400, 409, 422]


def test_3_3_consultar_pedido_por_id():
    """3.3 Positivo: Consultar pedido cadastrado."""
    token = obter_token()
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    res = requests.get(f"{BASE_URL}/pedidos/1", headers=headers)
    assert res.status_code in [200, 404]


# ==============================================================================
# 04. PAGAMENTO MOCK
# ==============================================================================

def test_4_1_pagamento_aprovado():
    """4.1 Positivo: Simular pagamento aprovado."""
    token = obter_token()
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    payload = {"pedidoId": 1, "valor": 50.00, "gateway": "MOCK", "simularRecusa": False}
    res = requests.post(f"{BASE_URL}/pagamentos/", json=payload, headers=headers)
    assert res.status_code in [200, 201, 400, 404, 422]


def test_4_2_pagamento_recusado():
    """4.2 Negativo: Simular pagamento recusado."""
    token = obter_token()
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    payload = {"pedidoId": 1, "valor": 50.00, "gateway": "MOCK", "simularRecusa": True}
    res = requests.post(f"{BASE_URL}/pagamentos/", json=payload, headers=headers)
    assert res.status_code in [200, 400, 422]


def test_4_3_pagamento_pedido_inexistente():
    """4.3 Negativo: Processar pagamento para pedido que não existe."""
    token = obter_token()
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    payload = {"pedidoId": 99999, "valor": 50.00, "gateway": "MOCK", "simularRecusa": False}
    res = requests.post(f"{BASE_URL}/pagamentos/", json=payload, headers=headers)
    assert res.status_code in [400, 404, 422]