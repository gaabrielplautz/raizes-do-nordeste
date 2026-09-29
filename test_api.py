import requests

BASE_URL = "http://127.0.0.1:8001"

def test_docs_disponivel():
    """Garante que a documentação Swagger está online e respondendo."""
    response = requests.get(f"{BASE_URL}/docs")
    assert response.status_code == 200

def test_login_credenciais_invalidas():
    """Cenário Negativo: Verifica se a API rejeita um login com dados errados."""
    payload = {
        "email": "usuario_falso@exemplo.com",
        "senha": "senhaerrada123"
    }
    response = requests.post(f"{BASE_URL}/auth/login", json=payload)
    # Aceita 400, 401, 404 ou 422 (erro de validação do Pydantic)
    assert response.status_code in [400, 401, 404, 422]

def test_rota_protegida_sem_autenticacao():
    """Cenário Negativo: Tenta acessar uma rota restrita sem enviar token JWT."""
    response = requests.get(f"{BASE_URL}/pedidos")
    # Aceita 401 (Não autorizado) ou 405 (Método não permitido caso mude a URL)
    assert response.status_code in [401, 405]

def test_criacao_pedido_com_multicanalidade():
    """
    Testa o envio de um pedido estruturado contendo o atributo essencial
    'canalPedido' (exigido no projeto).
    """
    payload = {
        "canalPedido": "TOTEM",
        "unidadeId": 1,
        "itens": [
            {"produtoId": 1, "quantidade": 2}
        ],
        "formaPagamento": "MOCK"
    }
    response = requests.post(f"{BASE_URL}/pedidos", json=payload)
    # Aceita 401 (sem token) ou 422/400 dependendo da validação de rota
    assert response.status_code in [401, 400, 422]