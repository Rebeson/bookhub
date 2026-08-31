const API_URL = "http://127.0.0.1:8000";

async function getLivros() {
    const response = await fetch(`${API_URL}/livros/`);

    if (!response.ok) {
        throw new Error("Erro ao buscar livros.");
    }

    return await response.json();
}


// =====================================================
// LIVRO
// =====================================================

async function getLivro(id) {

    const response = await fetch(
        `${API_URL}/livros/${id}`
    );


    if (!response.ok) {

        throw new Error(
            `Erro ao buscar livro: ${response.status}`
        );

    }


    return await response.json();

}


// =====================================================
// AUTORES DO LIVRO
// =====================================================

async function getAutoresDoLivro(id) {

    const response = await fetch(
        `${API_URL}/livros/${id}/autores`
    );


    if (!response.ok) {

        throw new Error(
            `Erro ao buscar autores: ${response.status}`
        );

    }


    return await response.json();

}


// =====================================================
// GÊNEROS DO LIVRO
// =====================================================

async function getGenerosDoLivro(id) {

    const response = await fetch(
        `${API_URL}/livros/${id}/generos`
    );


    if (!response.ok) {

        throw new Error(
            `Erro ao buscar gêneros: ${response.status}`
        );

    }


    return await response.json();

}

