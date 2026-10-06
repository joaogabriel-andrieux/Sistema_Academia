# Sistema de Gestão de Academia (Sistema_Academia)

Aplicação desktop e API para gestão completa de academia, desenvolvida em Python com Flask e Tkinter, com suporte a persistência de dados e regras de negócio complexas.

---

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** Python 3
- **Backend / API:** Flask & Flask-SQLAlchemy
- **Interface Gráfica (GUI):** Tkinter & `ttkbootstrap`
- **Banco de Dados:** SQLite / PostgreSQL
- **Contentorização:** Docker & Docker Compose

---

## 📋 Funcionalidades Principais

- **Autenticação:** Controlo de acesso por perfis (Administrador e Instrutores).
- **Gestão de Produtos e Inventário:** Controlo de stock, alertas visuais para stock mínimo e preservação de histórico de vendas.
- **Módulo de Vendas:** Validações em tempo real (datas futuras, limite de 30% de desconto e cálculo automático).
- **Relatórios:** Previsão de procura e análise de histórico de clientes.

---

## 🔑 Credenciais de Teste

Para aceder à aplicação no modo de demonstração:
- **Login:** `admin` | **Senha:** `admin`
- **Login:** `sergio` | **Senha:** `123`

---

## 🚀 Como Executar o Projeto

### Pré-requisitos
- Python 3.10 ou superior instalado.

### Passo a Passo

1. **Clonar o repositório:**
   ```bash
   git clone [https://github.com/joaogabriel-andrieux/Sistema_Academia.git](https://github.com/joaogabriel-andrieux/Sistema_Academia.git)
   cd Sistema_Academia
