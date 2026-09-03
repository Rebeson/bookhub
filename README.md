# 📚 BookHub

Uma plataforma web para descoberta, organização e avaliação de livros, permitindo que usuários explorem obras, criem sua biblioteca pessoal, avaliem livros, adicionem favoritos e compartilhem suas opiniões por meio de resenhas.

## 👥 Integrantes

- **[Hailton Thé](https://github.com/hailtonthe)**
- **[Rebeson Vitalino](https://github.com/Rebeson)**

## 📖 Sobre o projeto

O **BookHub** é uma aplicação web desenvolvida com o objetivo de oferecer um espaço para leitores explorarem, organizarem e registrarem suas experiências com livros.

A plataforma permite que os usuários consultem informações sobre diferentes obras, organizem seus livros em uma estante pessoal, avaliem suas leituras, adicionem títulos aos favoritos e escrevam resenhas compartilhando suas opiniões.

O projeto foi desenvolvido no contexto acadêmico, envolvendo diferentes etapas do desenvolvimento de software, desde a definição dos requisitos e modelagem do banco de dados até a implementação do backend, frontend, API, autenticação e infraestrutura da aplicação.

Além de proporcionar uma experiência simples para gerenciamento de livros e interações dos usuários, o BookHub também foi desenvolvido buscando aplicar na prática conceitos de **desenvolvimento web, banco de dados, APIs REST, autenticação e containerização**.

## 🎯 Objetivos

### Objetivo geral

Desenvolver uma plataforma web para gerenciamento e interação com livros, proporcionando aos usuários recursos para descobrir novas obras, organizar sua biblioteca pessoal, registrar avaliações, adicionar favoritos e compartilhar suas experiências por meio de resenhas.

### Objetivos específicos

- Desenvolver uma interface web simples e intuitiva para consulta e interação com livros;
- Permitir o cadastro e a autenticação de usuários;
- Disponibilizar recursos para organização de livros em uma estante pessoal;
- Implementar um sistema de avaliações e cálculo da média das notas dos livros;
- Permitir que os usuários adicionem livros aos favoritos;
- Disponibilizar a criação, edição e exclusão de resenhas;
- Organizar e disponibilizar informações sobre livros, autores e gêneros;
- Desenvolver uma API REST para comunicação entre o frontend e o backend;
- Utilizar um banco de dados relacional para armazenamento e gerenciamento das informações da aplicação;
- Aplicar práticas de desenvolvimento e infraestrutura, incluindo autenticação, documentação da API e containerização da aplicação.

## ✨ Funcionalidades

O BookHub oferece diferentes recursos para gerenciamento, organização e interação com livros:

- 📚 **Catálogo de livros** — consulta de livros cadastrados na plataforma, com informações como título, autor, gênero, editora e ano de publicação;
- 🔎 **Busca e filtragem** — localização de livros por meio da busca e dos filtros disponíveis;
- 👤 **Cadastro de usuários** — criação e gerenciamento de contas de usuário;
- 🔐 **Autenticação** — login seguro para acesso aos recursos exclusivos dos usuários;
- 📖 **Estante pessoal** — organização dos livros na biblioteca pessoal do usuário;
- ⭐ **Avaliações** — atribuição de notas aos livros, com cálculo da média das avaliações;
- ❤️ **Favoritos** — possibilidade de adicionar e remover livros da lista de favoritos;
- ✍️ **Resenhas** — criação, edição e exclusão de resenhas sobre os livros;
- 👨‍💼 **Gerenciamento de autores e gêneros** — organização das informações relacionadas aos autores e categorias dos livros;
- 🛡️ **Controle de usuários** — diferenciação entre usuários comuns e administradores, de acordo com as permissões do sistema;
- 📱 **Interface web responsiva** — acesso à plataforma por diferentes tamanhos de tela.

## 🛠️ Tecnologias utilizadas

O BookHub foi desenvolvido utilizando diferentes tecnologias para construção da interface, desenvolvimento da API, gerenciamento dos dados, autenticação e execução da aplicação.

### 🎨 Frontend

- **HTML5** — estruturação das páginas da aplicação;
- **CSS3** — estilização e definição da identidade visual;
- **JavaScript** — implementação da lógica e interatividade da interface;
- **Bootstrap 5** — utilização de componentes e recursos para construção da interface responsiva;
- **Font Awesome** — utilização de ícones na interface.

### ⚙️ Backend

- **Python** — linguagem utilizada no desenvolvimento do backend;
- **FastAPI** — framework utilizado para construção da API REST;
- **SQLAlchemy** — ORM utilizado para comunicação e gerenciamento das operações com o banco de dados;
- **Pydantic** — validação e estruturação dos dados utilizados pela API;
- **Uvicorn** — servidor utilizado para execução da aplicação FastAPI.

### 🗄️ Banco de dados

- **PostgreSQL** — sistema de gerenciamento de banco de dados relacional utilizado para armazenamento das informações do BookHub.

### 🔐 Segurança e autenticação

- **JWT (JSON Web Token)** — utilizado para autenticação e gerenciamento de sessões;
- **Argon2** — utilizado para armazenamento seguro das senhas dos usuários por meio de hashing.

### 🐳 Infraestrutura

- **Docker** — utilizado para criação e execução dos containers da aplicação;
- **Docker Compose** — utilizado para orquestrar os diferentes serviços que compõem o BookHub.

### 📡 Documentação da API

- **Swagger / OpenAPI** — utilizado para disponibilizar a documentação interativa dos endpoints da API.

## 🚀 Execução com Docker

O BookHub utiliza **Docker** e **Docker Compose** para facilitar a configuração e execução da aplicação. Dessa forma, o ambiente necessário para o funcionamento do sistema é criado por meio dos containers, sem a necessidade de realizar manualmente a configuração do banco de dados ou das dependências do projeto.

### Pré-requisito

Para executar o BookHub, é necessário ter o **Docker Desktop** instalado e em execução.

### 1. Clonar o repositório

Clone o repositório do projeto utilizando o Git:

```bash
git clone https://github.com/Rebeson/bookhub
```

Em seguida, entre na pasta do projeto:

```bash
cd BookHub
```

### 2. Iniciar a aplicação

Na **primeira execução** do projeto, utilize o comando abaixo para construir as imagens e iniciar os containers:

```bash
docker compose up --build
```

O parâmetro `--build` faz com que o Docker construa as imagens necessárias para a aplicação.

Após a primeira construção das imagens, **não é necessário utilizar o parâmetro `--build` novamente**, desde que não tenham sido realizadas alterações que exijam uma nova construção das imagens.

Nas execuções seguintes, basta utilizar:

```bash
docker compose up
```

> **Resumo:**
>
> - 🆕 **Primeira execução:** `docker compose up --build`
> - ▶️ **Execuções seguintes:** `docker compose up`
> - 🔨 **Após alterações que exigem reconstrução:** `docker compose up --build`

### 3. Acessar o BookHub

Após os containers serem iniciados, a aplicação estará disponível no navegador através do endereço:

```text
http://localhost
```

A API também possui documentação interativa através do Swagger, disponível em:

```text
http://localhost/docs
```

### 4. Encerrar a aplicação

Para interromper a execução dos containers, pressione:

```text
Ctrl + C
```

Caso seja necessário parar os containers posteriormente, também é possível utilizar:

```bash
docker compose down
```
