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


// =====================================================
// AVALIAÇÕES DO LIVRO
// =====================================================

async function getAvaliacoesDoLivro(id) {

    const response = await fetch(
        `${API_URL}/avaliacoes/livro/${id}`
    );


    if (!response.ok) {

        throw new Error(
            `Erro ao buscar avaliações: ${response.status}`
        );

    }


    return await response.json();

}


// =====================================================
// MÉDIA DAS AVALIAÇÕES
// =====================================================

async function getMediaAvaliacoes(id) {

    const response = await fetch(
        `${API_URL}/avaliacoes/livro/${id}/media`
    );


    if (!response.ok) {

        throw new Error(
            `Erro ao buscar média das avaliações: ${response.status}`
        );

    }


    return await response.json();

}


// =====================================================
// USUÁRIO AUTENTICADO
// =====================================================

async function getUsuarioAtual() {

    const token = localStorage.getItem('bookhub_token');

    if (!token) {
        return null;
    }


    const response = await fetch(
        `${API_URL}/usuarios/me`,
        {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        }
    );


    if (!response.ok) {

        // Token inválido ou expirado

        if (response.status === 401) {

            localStorage.removeItem('bookhub_token');

        }

        return null;

    }


    return await response.json();

}

