// =====================================================
// PÁGINA DE DETALHES DO LIVRO
// =====================================================


// -----------------------------------------------------
// Ao carregar a página
// -----------------------------------------------------

document.addEventListener('DOMContentLoaded', () => {

    carregarLivro();

});


// -----------------------------------------------------
// Carrega o livro através do ID da URL
// -----------------------------------------------------

async function carregarLivro() {

    const params = new URLSearchParams(window.location.search);

    const livroId = params.get('id');


    // Verifica se existe um ID na URL

    if (!livroId) {

        mostrarErro('Livro não informado.');

        return;

    }


    try {

        const livro = await getLivro(livroId);

        preencherLivro(livro);

        await carregarAutores(livroId);

        await carregarGeneros(livroId);

    } catch (error) {

        console.error('Erro ao carregar livro:', error);

        mostrarErro('Não foi possível carregar as informações do livro.');

    }

}


// -----------------------------------------------------
// Preenche as informações principais
// -----------------------------------------------------

function preencherLivro(livro) {


    // Título

    document.getElementById('book-title').innerText =
        livro.titulo || 'Título não informado';


    // Subtítulo

    const subtitleElement =
        document.getElementById('book-subtitle');

    if (livro.subtitulo) {

        subtitleElement.innerText = livro.subtitulo;

    } else {

        subtitleElement.innerText = '';

    }


    // Ano

    document.getElementById('book-year').innerText =
        livro.ano_publicacao || 'Não informado';


    // Páginas

    document.getElementById('book-pages').innerText =
        livro.numero_paginas
            ? `${livro.numero_paginas} páginas`
            : 'Não informado';


    // Idioma

    document.getElementById('book-language').innerText =
        livro.idioma || 'Não informado';


    // ISBN

    document.getElementById('book-isbn').innerText =
        livro.isbn || 'Não informado';


    // Sinopse

    const synopsisElement =
        document.getElementById('book-synopsis');

    if (livro.sinopse) {

        synopsisElement.innerHTML =
            `<p>${livro.sinopse}</p>`;

    } else {

        synopsisElement.innerHTML =
            `<p class="text-muted">
                Sinopse não informada.
            </p>`;

    }


    // Capa

    const coverContainer =
        document.getElementById('book-cover-container');


    if (livro.capa) {

        coverContainer.innerHTML = `
            <img
                src="${livro.capa}"
                alt="Capa de ${livro.titulo}"
                class="book-detail-cover"
            >
        `;

    } else {

        coverContainer.innerHTML = `
            <div class="book-cover-placeholder">
                📚
            </div>
        `;

    }


    // Data de cadastro

    if (livro.data_cadastro) {

        const data =
            new Date(livro.data_cadastro);

        document.getElementById(
            'book-registration-date'
        ).innerText =
            data.toLocaleDateString('pt-BR');

    }


    // Editora

    // Por enquanto o GET /livros/{id} retorna apenas editora_id.
    document.getElementById('book-publisher').innerText =
        livro.editora_id
            ? `Editora #${livro.editora_id}`
            : 'Não informado';

}


// -----------------------------------------------------
// Avaliações
// -----------------------------------------------------

const ratingElement =
    document.getElementById('book-rating');

ratingElement.innerHTML = `
    <span class="text-muted">
        <i class="fa-regular fa-star me-1"></i>
        Avaliações serão carregadas em breve.
    </span>
`;




// -----------------------------------------------------
// Carrega autores
// -----------------------------------------------------

async function carregarAutores(livroId) {

    const container =
        document.getElementById('book-authors');


    try {

        const autores =
            await getAutoresDoLivro(livroId);


        if (!autores || autores.length === 0) {

            container.innerHTML = `
                <p class="text-muted">
                    Autor não informado.
                </p>
            `;

            return;

        }


        container.innerHTML = autores.map(autor => `

            <div class="author-card">

                <div class="author-icon">

                    <i class="fa-solid fa-user"></i>

                </div>

                <div>

                    <h5 class="mb-1">
                        ${autor.nome}
                    </h5>

                </div>

            </div>

        `).join('');


    } catch (error) {

        console.error(
            'Erro ao carregar autores:',
            error
        );

        container.innerHTML = `
            <p class="text-muted">
                Não foi possível carregar os autores.
            </p>
        `;

    }

}


// -----------------------------------------------------
// Carrega gêneros
// -----------------------------------------------------

async function carregarGeneros(livroId) {

    const container =
        document.getElementById('book-genre');


    try {

        const generos =
            await getGenerosDoLivro(livroId);


        if (!generos || generos.length === 0) {

            container.innerText =
                'Gênero não informado.';

            return;

        }


        container.innerText =
            generos
                .map(genero => genero.nome)
                .join(' • ');


    } catch (error) {

        console.error(
            'Erro ao carregar gêneros:',
            error
        );

        container.innerText =
            'Não foi possível carregar o gênero.';

    }

}


// -----------------------------------------------------
// Exibe erro na página
// -----------------------------------------------------

function mostrarErro(mensagem) {

    document.getElementById('book-title').innerText =
        'Não foi possível carregar o livro.';

    document.getElementById('book-synopsis').innerHTML = `
        <p class="text-danger">
            ${mensagem}
        </p>
    `;

}

