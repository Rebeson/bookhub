CREATE TABLE usuario (
    id INTEGER GENERATED ALWAYS AS IDENTITY,
    nome VARCHAR(100) NOT NULL,
    nome_usuario VARCHAR(50) NOT NULL,
    email VARCHAR(255) NOT NULL,
    senha_hash VARCHAR(255) NOT NULL,
    data_cadastro TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    foto_perfil VARCHAR(500),
    biografia TEXT,
    tipo_usuario VARCHAR(20) NOT NULL DEFAULT 'USUARIO',
    ativo BOOLEAN NOT NULL DEFAULT TRUE,

    CONSTRAINT pk_usuario
        PRIMARY KEY (id),

    CONSTRAINT uq_usuario_nome_usuario
        UNIQUE (nome_usuario),

    CONSTRAINT uq_usuario_email
        UNIQUE (email),

    CONSTRAINT ck_usuario_tipo
        CHECK (tipo_usuario IN ('USUARIO', 'ADMIN'))
);

CREATE TABLE editora (
    id INTEGER GENERATED ALWAYS AS IDENTITY,

    nome VARCHAR(150) NOT NULL,

    descricao TEXT,

    site VARCHAR(500),

    CONSTRAINT pk_editora
        PRIMARY KEY (id),

    CONSTRAINT uq_editora_nome
        UNIQUE (nome)
);

CREATE TABLE autor (
    id INTEGER GENERATED ALWAYS AS IDENTITY,

    nome VARCHAR(150) NOT NULL,

    biografia TEXT,

    data_nascimento DATE,

    foto VARCHAR(500),

    CONSTRAINT pk_autor
        PRIMARY KEY (id)
);

CREATE TABLE genero (
    id INTEGER GENERATED ALWAYS AS IDENTITY,

    nome VARCHAR(100) NOT NULL,

    descricao TEXT,

    CONSTRAINT pk_genero
        PRIMARY KEY (id),

    CONSTRAINT uq_genero_nome
        UNIQUE (nome)
);

CREATE TABLE livro (
    id INTEGER GENERATED ALWAYS AS IDENTITY,

    titulo VARCHAR(255) NOT NULL,

    subtitulo VARCHAR(255),

    isbn VARCHAR(20),

    sinopse TEXT,

    ano_publicacao SMALLINT,

    numero_paginas INTEGER,

    idioma VARCHAR(50),

    capa VARCHAR(500),

    editora_id INTEGER NOT NULL,

    data_cadastro TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT pk_livro
        PRIMARY KEY (id),

    CONSTRAINT uq_livro_isbn
        UNIQUE (isbn),

    CONSTRAINT ck_livro_ano
        CHECK (ano_publicacao IS NULL OR ano_publicacao > 0),

    CONSTRAINT ck_livro_paginas
        CHECK (numero_paginas IS NULL OR numero_paginas > 0),

    CONSTRAINT fk_livro_editora
        FOREIGN KEY (editora_id)
        REFERENCES editora(id)
);

CREATE TABLE livro_autor (
    livro_id INTEGER NOT NULL,

    autor_id INTEGER NOT NULL,

    CONSTRAINT pk_livro_autor
        PRIMARY KEY (livro_id, autor_id),

    CONSTRAINT fk_livro_autor_livro
        FOREIGN KEY (livro_id)
        REFERENCES livro(id),

    CONSTRAINT fk_livro_autor_autor
        FOREIGN KEY (autor_id)
        REFERENCES autor(id)
);

CREATE TABLE livro_genero (
    livro_id INTEGER NOT NULL,

    genero_id INTEGER NOT NULL,

    CONSTRAINT pk_livro_genero
        PRIMARY KEY (livro_id, genero_id),

    CONSTRAINT fk_livro_genero_livro
        FOREIGN KEY (livro_id)
        REFERENCES livro(id),

    CONSTRAINT fk_livro_genero_genero
        FOREIGN KEY (genero_id)
        REFERENCES genero(id)
);

CREATE TABLE usuario_livro (
    usuario_id INTEGER NOT NULL,

    livro_id INTEGER NOT NULL,

    status_leitura VARCHAR(20) NOT NULL DEFAULT 'QUERO_LER',

    pagina_atual INTEGER NOT NULL DEFAULT 0,

    data_adicao TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    data_inicio DATE,

    data_conclusao DATE,

    CONSTRAINT pk_usuario_livro
        PRIMARY KEY (usuario_id, livro_id),

    CONSTRAINT fk_usuario_livro_usuario
        FOREIGN KEY (usuario_id)
        REFERENCES usuario(id),

    CONSTRAINT fk_usuario_livro_livro
        FOREIGN KEY (livro_id)
        REFERENCES livro(id),

    CONSTRAINT ck_usuario_livro_status
        CHECK (
            status_leitura IN (
                'QUERO_LER',
                'LENDO',
                'LIDO',
                'ABANDONADO'
            )
        ),

    CONSTRAINT ck_usuario_livro_pagina
        CHECK (pagina_atual >= 0)
);

CREATE TABLE avaliacao (
    id INTEGER GENERATED ALWAYS AS IDENTITY,

    usuario_id INTEGER NOT NULL,

    livro_id INTEGER NOT NULL,

    nota SMALLINT NOT NULL,

    data_avaliacao TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    data_atualizacao TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT pk_avaliacao
        PRIMARY KEY (id),

    CONSTRAINT fk_avaliacao_usuario
        FOREIGN KEY (usuario_id)
        REFERENCES usuario(id),

    CONSTRAINT fk_avaliacao_livro
        FOREIGN KEY (livro_id)
        REFERENCES livro(id),

    CONSTRAINT uq_avaliacao_usuario_livro
        UNIQUE (usuario_id, livro_id),

    CONSTRAINT ck_avaliacao_nota
        CHECK (nota BETWEEN 1 AND 5)
);

CREATE TABLE resenha (
    id INTEGER GENERATED ALWAYS AS IDENTITY,

    usuario_id INTEGER NOT NULL,

    livro_id INTEGER NOT NULL,

    titulo VARCHAR(200) NOT NULL,

    conteudo TEXT NOT NULL,

    data_publicacao TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    data_atualizacao TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT pk_resenha
        PRIMARY KEY (id),

    CONSTRAINT fk_resenha_usuario
        FOREIGN KEY (usuario_id)
        REFERENCES usuario(id),

    CONSTRAINT fk_resenha_livro
        FOREIGN KEY (livro_id)
        REFERENCES livro(id),

    CONSTRAINT uq_resenha_usuario_livro
        UNIQUE (usuario_id, livro_id)
);

CREATE TABLE favorito (
    usuario_id INTEGER NOT NULL,
    livro_id INTEGER NOT NULL,
    data_adicao TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT pk_favorito
        PRIMARY KEY (usuario_id, livro_id),

    CONSTRAINT fk_favorito_usuario
        FOREIGN KEY (usuario_id)
        REFERENCES usuario(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_favorito_livro
        FOREIGN KEY (livro_id)
        REFERENCES livro(id)
        ON DELETE CASCADE
);