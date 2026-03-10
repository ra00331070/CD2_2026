# 🍝 Bella Tavola API

API REST de um restaurante italiano fictício, construída com **FastAPI** como projeto prático da disciplina **Ciência de Dados e IA (CD2 — 2026)**.

O projeto cobre roteamento, validação de dados, tratamento de erros e organização modular de código — passando pelos três blocos do caderno de exercícios.

---

## 📁 Estrutura do Projeto

```
bella_tavola/
├── main.py              # Aplicação FastAPI, exception handlers e registro dos routers
├── config.py            # Configurações via variáveis de ambiente (BaseSettings)
├── .env                 # Valores das variáveis de ambiente (não versionar em produção)
├── requirements.txt     # Dependências do projeto
│
├── models/              # Modelos Pydantic de entrada e saída
│   ├── prato.py
│   ├── bebida.py
│   ├── pedido.py
│   └── reserva.py
│
└── routers/             # Rotas organizadas por domínio
    ├── pratos.py
    ├── bebidas.py
    ├── pedidos.py
    └── reservas.py
```

---

## 🚀 Como Rodar

### Pré-requisitos

- Python 3.10+
- pip

### Instalação

```bash
# Clone o repositório
git clone <url-do-repositorio>
cd bella_tavola

# Instale as dependências
pip install -r requirements.txt
```

### Executando o servidor

```bash
uvicorn main:app --reload
```

A flag `--reload` reinicia o servidor automaticamente a cada alteração no código.

### Acessando a documentação

Com o servidor rodando, acesse no navegador:

| URL | Descrição |
|-----|-----------|
| `http://localhost:8000/docs` | Swagger UI (interativo) |
| `http://localhost:8000/redoc` | ReDoc (leitura) |
| `http://localhost:8000/` | Informações do restaurante |

---

## 🗺️ Rotas Disponíveis

### Geral
| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/` | Informações do restaurante |

### Pratos
| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/pratos` | Lista pratos (filtros: `categoria`, `preco_maximo`, `apenas_disponiveis`) |
| GET | `/pratos/{id}` | Busca um prato por ID (parâmetro `formato`: `completo` ou `resumido`) |
| POST | `/pratos` | Cadastra um novo prato |
| PUT | `/pratos/{id}/disponibilidade` | Altera a disponibilidade de um prato |

### Bebidas
| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/bebidas` | Lista bebidas (filtros: `tipo`, `alcoolica`) |
| GET | `/bebidas/{id}` | Busca uma bebida por ID |
| POST | `/bebidas` | Cadastra uma nova bebida |

### Pedidos
| Método | Rota | Descrição |
|--------|------|-----------|
| POST | `/pedidos` | Cria um pedido (calcula valor total automaticamente) |

### Reservas
| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/reservas` | Lista reservas (filtros: `data`, `apenas_ativas`) |
| GET | `/reservas/{id}` | Busca uma reserva por ID |
| GET | `/reservas/mesa/{numero}` | Lista reservas de uma mesa específica |
| POST | `/reservas` | Cria uma reserva antecipada |
| DELETE | `/reservas/{id}` | Cancela uma reserva |

---

## ✅ Validações Implementadas

### Pratos
- `nome`: 3 a 100 caracteres
- `categoria`: `pizza`, `massa`, `sobremesa`, `entrada` ou `salada`
- `preco`: maior que zero
- `preco_promocional`: menor que o preço original e desconto máximo de 50%

### Bebidas
- `nome`: 3 a 100 caracteres
- `tipo`: `vinho`, `agua`, `refrigerante`, `suco` ou `cerveja`
- `preco`: maior que zero
- `volume_ml`: entre 50 ml e 2000 ml

### Reservas
- `mesa`: entre 1 e `MAX_MESAS` (configurável)
- `pessoas`: entre 1 e `MAX_PESSOAS_POR_MESA` (configurável)
- `data_hora`: deve ser pelo menos 1 hora no futuro
- Não permite duas reservas ativas para a mesma mesa no mesmo dia

---

## ⚙️ Configurações

As configurações ficam no arquivo `.env` na raiz do projeto:

```env
APP_NAME=Bella Tavola API
APP_VERSION=1.0.0
DEBUG=true
MAX_MESAS=20
MAX_PESSOAS_POR_MESA=10
```

Todas as variáveis têm valores padrão definidos em `config.py` e podem ser sobrescritas sem alterar o código.

---

## 📦 Dependências

```
fastapi
uvicorn
pydantic-settings
```

---

## 📚 Contexto Acadêmico

Este projeto foi desenvolvido como atividade prática da disciplina **CD2 (2026)** do curso de **Ciência de Dados e IA**. O caderno de exercícios (`CDIA_CD2_2026_e02_fastAPI.ipynb`) guia a construção da API em três blocos progressivos:

- **Bloco 1 — Surface:** roteamento, path/query parameters, modelos Pydantic
- **Bloco 2 — Robustez:** HTTPException, validações com `Field` e `@field_validator`, exception handlers globais
- **Bloco 3 — Estrutura:** `APIRouter`, separação de modelos, `BaseSettings`