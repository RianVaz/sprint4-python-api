# 📖 Sprint 4 - TerraLAB 🗺️

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.x-black.svg)](https://flask.palletsprojects.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14+-blue.svg)](https://www.postgresql.org/)

Este projeto é um backend em Python desenvolvido com Flask para gerenciar usuários e pontos de interesse geográficos. Ele foi projetado para ser uma API simples e funcional, utilizando PostgreSQL com a extensão PostGIS para armazenar e manipular dados espaciais de forma nativa e eficiente.

---

## ✨ Funcionalidades

* **Gerenciamento de Usuários**: Criar, listar, alterar e remover usuários.
* **Gerenciamento de Pontos**: Criar, listar por usuário, alterar e remover pontos geográficos.
* **Dados Geoespaciais**: Armazena a geometria dos pontos de forma nativa usando PostGIS.
* **API REST-like**: Endpoints claros para interagir com os dados (utilizando método GET com parâmetros).
* **Testes Automatizados**: Suíte de testes completa com Pytest para garantir a qualidade e o funcionamento da aplicação.

---

## 🚀 Tecnologias Utilizadas

* **Linguagem**: Python 3
* **Framework Web**: Flask
* **Banco de Dados**: PostgreSQL
* **Extensão Geoespacial**: PostGIS
* **Testes**: Pytest
* **Driver do Banco**: Psycopg2
* **Variáveis de Ambiente**: Dotenv

---

## ⚙️ Instalação e Configuração

Siga estes passos para configurar e executar o projeto em sua máquina local.

### 1. Pré-requisitos
Antes de começar, certifique-se de que você tem os seguintes softwares instalados:
* [Python 3.9+](https://www.python.org/downloads/)
* [PostgreSQL](https://www.postgresql.org/download/)

### 2. Configurar o Banco de Dados
1.  Abra o **pgAdmin4**
2.  Crie um usuário, um banco de dados para desenvolvimento e outro para testes:
    ```sql
    -- 1. Crie o usuário
    CREATE USER user WITH PASSWORD 'sua_senha';

    -- 2. Crie os bancos de dados
    CREATE DATABASE geopoints_db;
    CREATE DATABASE test_geopoints_db;

    -- 3. Dê as permissões necessárias
    GRANT ALL PRIVILEGES ON DATABASE geopoints_db TO user;
    GRANT ALL PRIVILEGES ON DATABASE test_geopoints_db TO user;
    ```
3.  **Ative a extensão PostGIS** em ambos os bancos. Conecte-se a cada um deles e execute o comando:
    

### 4. Configurar Variáveis de Ambiente
Na raiz do projeto, existe um arquivo chamado `.env`. Ele guardará suas senhas e credenciais de forma segura.

Vá até o file `.env` e preencha com seus dados:
```env
# Credenciais do Banco de Dados
DB_HOST=localhost
DB_NAME=geopoints_db
DB_USER=user
DB_PASSWORD=sua_senha

# Banco de Dados para Testes
TEST_DB_NAME=test_geopoints_db
```

### 5. Configurar o Ambiente Virtual Python
Com o terminal na pasta raiz do projeto, execute os seguintes comandos:

```powershell
# Criar o ambiente virtual (usando o Python launcher para Windows)
py -m venv venv

# Ativar o ambiente virtual
.\venv\Scripts\activate

# Instalar todas as dependências do projeto
pip install -r requirements.txt
```

---

## ▶️ Executando a Aplicação

Com o ambiente virtual ativado (`(venv)` deve aparecer no seu terminal), inicie o servidor Flask:

```powershell
py run.py
```
A API estará rodando e pronta para receber requisições em `http://localhost:8080`.

---

## 🧪 Executando os Testes

Para verificar a integridade e o funcionamento de todas as partes da aplicação, execute a suíte de testes automatizados.

Com o ambiente virtual ativado, rode o comando:
```powershell
pytest
```
---

## 🌐 Referência da API (Endpoints)

Todas as operações são feitas via requisições `GET` com parâmetros na URL.

Apenas a operação de Adicionar Usuarios è feita via requisições `POST` com parâmetros no corpo JSON.

### Endpoints de Usuário 🧑‍💻
| Ação | URL e Parâmetros | Exemplo Completo |
| :--- | :--- | :--- |
| **Listar Todos** | `/ListarUsuarios/` | `http://localhost:8080/ListarUsuarios/` |
| **Adicionar** | `POST /usuarios` com corpo JSON | **URL:** `http://localhost:8080/usuarios`<br>**Body (JSON):**<br>```json<br>{<br> "email": "novo@email.com",<br>  "nome": "Novo Usuario"<br>}<br>``` |
| **Alterar** | `/AlterarUsuario/?email=<email>&nome=<novo_nome>`| `http://localhost:8080/AlterarUsuario/?email=joao@email.com&nome=Joao da Silva`|
| **Remover** | `/RemoverUsuario/?email=<email>` | `http://localhost:8080/RemoverUsuario/?email=joao@email.com`|

### Endpoints de Pontos Geográficos 📍
| Ação | URL e Parâmetros | Exemplo Completo |
| :--- | :--- | :--- |
| **Adicionar** | `/AdicionarPonto/?latitude=<lat>&longitude=<lon>&descricao=<desc>&email=<email>`|`http://localhost:8080/AdicionarPonto/?latitude=-19.91&longitude=-43.93&descricao=Praça Sete&email=joao@email.com`|
| **Listar** | `/ListarPontos/?email=<email>` |`http://localhost:8080/ListarPontos/?email=joao@email.com`|
| **Alterar** | `/AlterarPonto/?id=<id>&latitude=<lat>&longitude=<lon>&descricao=<desc>` |`http://localhost:8080/AlterarPonto/?id=1&latitude=-19.92&longitude=-43.94&descricao=Mercado Central`|
| **Remover** | `/RemoverPonto/?id=<id>`|`http://localhost:8080/RemoverPonto/?id=1`|

---

## 🏛️ Estrutura do Projeto
```
├── app/                  # Pacote principal da aplicação
│   ├── routes/           # Módulo para os arquivos de rota
│   │   ├── routes_point.py
│   │   └── routes_user.py
│   ├── __init__.py     # Fábrica da aplicação (cria e configura o app)
│   └── database.py     # Camada de acesso aos dados (interação com o BD)
│
├── test_app.py           # Arquivo com os testes automatizados
├── run.py                # Ponto de entrada para executar a aplicação
├── .env                  # Arquivo local com as variáveis de ambiente (NÃO VERSIONADO)
├── .gitignore            # Arquivos e pastas a serem ignorados pelo Git
└── requirements.txt      # Lista de dependências Python
```

---

## 📄 Resultados

Representação dos pontos do tipo **geometry** criados a partir da **latitude** e **longitude** informados:

![representacao pontos](/images/ImagemGeomPontos.jpg)
![databese pontos](/images/ImagemBdPonto.jpg)

Resultados apresentados pelo **pytest**:

![PytestResult](/images/ImagemPytest.jpg)

## 🙋‍♂️ Meu Perfil

* **Nome: Rian Vaz Maurício**

* [![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/rianvaz)
* [![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/RianVaz)
* [![GitLab](https://img.shields.io/badge/GitLab-FC6D26?style=for-the-badge&logo=gitlab&logoColor=white)](https://gitlab.com/RianVaz)
