const API_URL = "http://127.0.0.1:8000";

// =====================================================
// LISTAR LIVROS
// =====================================================

async function getLivros() {


const response = await fetch(
    `${API_URL}/livros/`
);

if (!response.ok) {
    throw new Error(
        `Erro ao buscar livros: ${response.status}`
    );
}

return await response.json();


}

// =====================================================
// BUSCAR LIVRO
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
// LOGIN
// =====================================================

// Cadastro de usuário
async function cadastrarUsuario(dados) {


const response = await fetch(
    `${API_URL}/usuarios/`,
    {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(dados)
    }
);

const resultado = await response.json();

if (!response.ok) {

    console.error('Erro retornado pela API:', resultado);

    let mensagem = 'Erro ao cadastrar usuário.';

    if (typeof resultado.detail === 'string') {

        mensagem = resultado.detail;

    } else if (Array.isArray(resultado.detail)) {

        mensagem = resultado.detail
            .map(erro => erro.msg)
            .join('\n');

    }

    throw new Error(mensagem);
}

return resultado;


}


// Login
async function fazerLogin(email, senha) {


const response = await fetch(
    `${API_URL}/auth/login`,
    {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            email: email,
            senha: senha
        })
    }
);

const resultado = await response.json();

if (!response.ok) {

    console.error('Erro retornado pela API:', resultado);

    let mensagem = 'Erro ao realizar login.';

    if (typeof resultado.detail === 'string') {

        mensagem = resultado.detail;

    } else if (Array.isArray(resultado.detail)) {

        mensagem = resultado.detail
            .map(erro => erro.msg)
            .join('\n');

    }

    throw new Error(mensagem);
}

localStorage.setItem(
    'bookhub_token',
    resultado.access_token
);

return resultado;


}


// Buscar usuário autenticado
async function getUsuarioAtual() {


if (!estaLogado()) {
    return null;
}

const response = await apiFetch('/usuarios/me');

if (!response.ok) {

    localStorage.removeItem('bookhub_token');
    localStorage.removeItem('bookhub_user');

    return null;
}

return await response.json();


}


// Logout
function fazerLogout() {


localStorage.removeItem('bookhub_token');
localStorage.removeItem('bookhub_user');


}

// Retorna o token atual
function getToken() {


return localStorage.getItem('bookhub_token');


}


// =====================================================
// REQUISIÇÕES AUTENTICADAS
// =====================================================

async function apiFetch(endpoint, options = {}) {


const token = getToken();

const headers = {
    ...options.headers
};

// Adiciona o token quando o usuário estiver autenticado
if (token) {
    headers['Authorization'] = `Bearer ${token}`;
}

// Adiciona JSON automaticamente quando houver um body
if (options.body && !headers['Content-Type']) {
    headers['Content-Type'] = 'application/json';
}

const response = await fetch(
    `${API_URL}${endpoint}`,
    {
        ...options,
        headers: headers
    }
);

// Se o token expirou ou não é mais válido
if (response.status === 401) {

    localStorage.removeItem('bookhub_token');
    localStorage.removeItem('bookhub_user');

    currentUser = null;

    updateAuthUI();
}

return response;


}


// Verifica se existe usuário autenticado
function estaLogado() {


return !!localStorage.getItem('bookhub_token');


}


