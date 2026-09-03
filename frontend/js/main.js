// =====================================================
// DADOS DOS LIVROS
// =====================================================

let livrosData = [];

// =====================================================
// ESTADOS DO USUÁRIO
// =====================================================

let currentUser =
    JSON.parse(localStorage.getItem('bookhub_user')) || null;

let userFavorites =
    JSON.parse(localStorage.getItem('bookhub_favs')) || [];

let userShelf =
    JSON.parse(localStorage.getItem('bookhub_shelf')) || {};

// Ao carregar a página
document.addEventListener('DOMContentLoaded', async () => {


// Verifica se existe uma sessão salva
if (estaLogado()) {

    const usuario = await getUsuarioAtual();

    if (usuario) {

        currentUser = usuario;

        localStorage.setItem(
            'bookhub_user',
            JSON.stringify(usuario)
        );

    } else {

        currentUser = null;
        localStorage.removeItem('bookhub_user');
    }
}

updateAuthUI();

try {

    const livros = await getLivros();

    console.log("Livros recebidos da API:", livros);

    livrosData = livros;

    console.log("livrosData:", livrosData);

    renderBooks(
        livrosData,
        'books-grid',
        'explorar'
    );

} catch (error) {

    console.error('Erro ao carregar livros:', error);

    document.getElementById('books-grid').innerHTML = `
        <p class="text-danger">
            Não foi possível carregar os livros.
        </p>
    `;
}


});



// Navegação entre abas
function navigate(section) {
    document.querySelectorAll('.page-section').forEach(el => el.classList.add('d-none'));
    document.querySelectorAll('.nav-link').forEach(el => el.classList.remove('active'));
    
    document.getElementById(`${section}-section`).classList.remove('d-none');
    document.getElementById(`nav-${section}`).classList.add('active');

    if (section === 'favoritos') loadFavorites();
    if (section === 'estante') loadShelf();
}

// Renderização dos cards de livros
function renderBooks(books, containerId, context) {

    const container = document.getElementById(containerId);

    container.innerHTML = '';

    if (context === 'explorar') {
        document.getElementById('book-count').innerText =
            `${books.length} livro(s) encontrado(s)`;
    }

    books.forEach(book => {

        const isFav = userFavorites.includes(book.id) ? 'active' : '';
        const heartIcon = isFav ? 'fa-solid' : 'fa-regular';

        // Autor
        const autores = book.autores && book.autores.length > 0
            ? book.autores.map(autor => autor.nome).join(', ')
            : 'Autor não informado';

        // Gênero
        const genero = book.generos && book.generos.length > 0
            ? book.generos[0].nome
            : 'Gênero não informado';

        // Avaliação
        const rating = book.media_avaliacoes !== null
            ? book.media_avaliacoes
            : 'Sem avaliações';

        const reviews = book.quantidade_avaliacoes;

        // Capa
        const capa = book.capa
            ? `
                <img
                    src="${book.capa}"
                    alt="Capa de ${book.titulo}"
                    class="book-cover"
                >
              `
            : `
                <div class="book-cover-placeholder">
                    📚
                </div>
              `;

        // Controle da estante
        let shelfHtml = '';

        if (currentUser) {

            const currentStatus = userShelf[book.id] || "";

            shelfHtml = `
                <select
                    class="form-select form-select-sm shelf-control mt-3"
                    onchange="updateShelf(${book.id}, this.value)"
                >

                    <option value="">
                        Adicionar à estante...
                    </option>

                    <option value="Desejo Ler"
                        ${currentStatus === 'Desejo Ler' ? 'selected' : ''}>
                        Desejo Ler
                    </option>

                    <option value="Lendo"
                        ${currentStatus === 'Lendo' ? 'selected' : ''}>
                        Lendo
                    </option>

                    <option value="Concluído"
                        ${currentStatus === 'Concluído' ? 'selected' : ''}>
                        Concluído
                    </option>

                </select>
            `;
        }

        const card = `
            <div class="col-md-6 col-lg-3 mb-4">
                <div
                    class="book-card"
                    onclick="abrirLivro(${book.id})"
                >
                    <div class="book-card-top">
                        ${capa}
                    </div>

                    <div class="book-info">
                        <div class="book-genre">
                            ${genero}
                        </div>

                        <h3 class="book-title">
                            ${book.titulo}
                        </h3>

                        <div class="book-author">
                            ${autores}
                        </div>

                        <div class="book-rating">
                            <i class="fa-solid fa-star star-icon"></i>
                            <strong>${rating}</strong>
                            (${reviews} avaliações)
                        </div>

                        ${shelfHtml}
                    </div>
                </div>
            </div>
        `;

        container.innerHTML += card;
    });
}



// =====================================================
// FILTRO E BUSCA
// =====================================================

function filterBooks() {

    const term =
        document
            .getElementById('searchInput')
            .value
            .toLowerCase()
            .trim();

    const genre =
        document.getElementById('genreFilter').value;

    const filtered = livrosData.filter(book => {

        // =================================================
        // TÍTULO
        // =================================================

        const titulo =
            book.titulo?.toLowerCase() || '';

        // =================================================
        // AUTORES
        // =================================================

        const autores =
            book.autores && book.autores.length > 0
                ? book.autores
                    .map(autor => autor.nome.toLowerCase())
                    .join(' ')
                : '';

        // =================================================
        // GÊNEROS
        // =================================================

        const generos =
            book.generos && book.generos.length > 0
                ? book.generos.map(
                    genero => genero.nome
                )
                : [];

        // =================================================
        // BUSCA
        // =================================================

        const matchesTerm =
            titulo.includes(term) ||
            autores.includes(term);

        // =================================================
        // FILTRO DE GÊNERO
        // =================================================

        const matchesGenre =
            genre === 'Todos' ||
            generos.some(
                generoNome =>
                    generoNome.toLowerCase() === genre.toLowerCase()
            );

        return matchesTerm && matchesGenre;
    });

    renderBooks(
        filtered,
        'books-grid',
        'explorar'
    );
}



// Funcionalidades: Favoritos e Estante
function toggleFavorite(id) {
    if (!currentUser) return alert('Faça login para favoritar livros!');
    
    if (userFavorites.includes(id)) {
        userFavorites = userFavorites.filter(favId => favId !== id);
    } else {
        userFavorites.push(id);
    }
    localStorage.setItem('bookhub_favs', JSON.stringify(userFavorites));
    
    // Atualiza a visualização dependendo da aba ativa
    filterBooks();
    loadFavorites();
}

function updateShelf(id, status) {
    if (!status) {
        delete userShelf[id];
    } else {
        userShelf[id] = status;
    }
    localStorage.setItem('bookhub_shelf', JSON.stringify(userShelf));
    if (!document.getElementById('estante-section').classList.contains('d-none')) {
        loadShelf();
    }
}

function loadFavorites() {

    const favBooks =
        livrosData.filter(
            b => userFavorites.includes(b.id)
        );

    renderBooks(
        favBooks,
        'fav-grid',
        'favoritos'
    );

    if (favBooks.length === 0) {
        document.getElementById('fav-grid').innerHTML =
            '<p class="text-muted">Nenhum livro favoritado ainda.</p>';
    }
}

function loadShelf() {

    const shelfBooks =
        livrosData.filter(
            b => userShelf[b.id]
        );

    renderBooks(
        shelfBooks,
        'shelf-grid',
        'estante'
    );

    if (shelfBooks.length === 0) {
        document.getElementById('shelf-grid').innerHTML =
            '<p class="text-muted">Sua estante está vazia.</p>';
    }
}

// Autenticação (Login / Cadastro)
async function register() {


const nome = document.getElementById('regNome').value.trim();
const nomeUsuario = document.getElementById('regNomeUsuario').value.trim();
const email = document.getElementById('regEmail').value.trim();
const senha = document.getElementById('regSenha').value;

if (!nome || !nomeUsuario || !email || !senha) {

    alert('Preencha todos os campos.');

    return;
}

try {

    await cadastrarUsuario({
        nome: nome,
        nome_usuario: nomeUsuario,
        email: email,
        senha: senha
    });

    alert(
        'Cadastro realizado com sucesso! Você já pode fazer login.'
    );

    bootstrap.Modal
        .getInstance(
            document.getElementById('registerModal')
        )
        .hide();

    document.getElementById('regNome').value = '';
    document.getElementById('regNomeUsuario').value = '';
    document.getElementById('regEmail').value = '';
    document.getElementById('regSenha').value = '';

} catch (error) {

    console.error('Erro no cadastro:', error);

    alert(error.message);
}


}




async function login() {


const email = document.getElementById('loginEmail').value.trim();
const senha = document.getElementById('loginSenha').value;

if (!email || !senha) {
    alert('Preencha o e-mail e a senha.');
    return;
}

try {

    // Faz login e recebe o JWT
    await fazerLogin(email, senha);

    // Busca os dados reais do usuário
    const usuario = await getUsuarioAtual();

    if (!usuario) {
        throw new Error('Não foi possível obter os dados do usuário.');
    }

    // Guarda os dados públicos do usuário
    currentUser = usuario;

    localStorage.setItem(
        'bookhub_user',
        JSON.stringify(usuario)
    );

    updateAuthUI();

    bootstrap.Modal
        .getInstance(document.getElementById('loginModal'))
        .hide();

    // Limpa os campos
    document.getElementById('loginEmail').value = '';
    document.getElementById('loginSenha').value = '';

    // Atualiza os livros
    filterBooks();

} catch (error) {

    console.error('Erro no login:', error);

    alert(error.message);
}


}



function logout() {


fazerLogout();

currentUser = null;

updateAuthUI();

navigate('explorar');

filterBooks();


}



function updateAuthUI() {
    const authSection = document.getElementById('auth-section');
    if (currentUser) {
        authSection.innerHTML = `
            <span class="me-3 text-dark fw-medium">Olá, ${currentUser.nome}</span>
            <a href="#" class="auth-link" onclick="logout()">Sair</a>
        `;
    } else {
        authSection.innerHTML = `
            <a href="#" class="auth-link me-3" data-bs-toggle="modal" data-bs-target="#loginModal">Entrar</a>
            <a href="#" class="auth-link" data-bs-toggle="modal" data-bs-target="#registerModal">Cadastrar</a>
        `;
    }
}


function abrirLivro(id) {
    window.location.href = `pages/livro.html?id=${id}`;
}
