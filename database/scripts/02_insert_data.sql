INSERT INTO editora (nome, descricao, site)
VALUES
(
    'Companhia das Letras',
    'Editora brasileira fundada em 1986.',
    'https://www.companhiadasletras.com.br'
),
(
    'Aleph',
    'Editora brasileira especializada em ficção científica e fantasia.',
    'https://editoraaleph.com.br'
),
(
    'DarkSide Books',
    'Editora brasileira especializada em literatura de fantasia, terror e ficção.',
    'https://darksidebooks.com.br'
);

INSERT INTO usuario (
    nome,
    nome_usuario,
    email,
    senha_hash
)
VALUES (
    'João da Silva',
    'joaosilva',
    'joao@email.com',
    'HASH_DE_TESTE'
);

INSERT INTO autor (
    nome,
    biografia,
    data_nascimento
)
VALUES
(
    'George Orwell',
    'Escritor e jornalista britânico, conhecido por obras como 1984 e A Revolução dos Bichos.',
    '1903-06-25'
),
(
    'Machado de Assis',
    'Escritor brasileiro considerado um dos maiores nomes da literatura brasileira.',
    '1839-06-21'
),
(
    'J. R. R. Tolkien',
    'Escritor, professor e filólogo britânico, autor de O Hobbit e O Senhor dos Anéis.',
    '1892-01-03'
);

INSERT INTO genero (nome, descricao)
VALUES
(
    'Romance',
    'Obras centradas em relações amorosas e afetivas.'
),
(
    'Fantasia',
    'Obras que apresentam elementos mágicos ou sobrenaturais.'
),
(
    'Ficção científica',
    'Obras que exploram ciência, tecnologia e possíveis futuros.'
),
(
    'Distopia',
    'Obras que apresentam sociedades imaginárias marcadas por condições negativas ou opressivas.'
),
(
    'Terror',
    'Obras destinadas a provocar medo, tensão ou suspense.'
);

INSERT INTO livro (
    titulo,
    isbn,
    sinopse,
    ano_publicacao,
    numero_paginas,
    idioma,
    editora_id
)
VALUES
(
    '1984',
    '9780451524935',
    'Romance distópico que apresenta uma sociedade submetida a vigilância e controle constantes.',
    1949,
    328,
    'Português',
    2
),
(
    'Dom Casmurro',
    '9788535914849',
    'Romance de Machado de Assis narrado por Bento Santiago.',
    1899,
    256,
    'Português',
    1
),
(
    'O Hobbit',
    '9788595084742',
    'A aventura de Bilbo Bolseiro em uma jornada pela Terra-média.',
    1937,
    336,
    'Português',
    3
);

INSERT INTO livro_autor (livro_id, autor_id)
VALUES
(1, 1),
(2, 2),
(3, 3);

INSERT INTO livro_genero (livro_id, genero_id)
VALUES
(1, 3), -- 1984 → Ficção científica
(1, 4), -- 1984 → Distopia
(2, 1), -- Dom Casmurro → Romance
(3, 2); -- O Hobbit → Fantasia

INSERT INTO resenha (
    usuario_id,
    livro_id,
    titulo,
    conteudo)
VALUES (
    1,
    1,
    'Uma obra impressionante',
    'Uma leitura muito interessante e relevante.'
);

INSERT INTO avaliacao (
    usuario_id,
    livro_id,
    nota)
VALUES (
    1,
    1,
    5
);

