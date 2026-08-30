// Base de dados 
const booksData = [
    { id: 1, title: '1984', author: 'George Orwell', genre: 'FICÇÃO', genreColor: '#6c5ce7', rating: 4.9, reviews: 3100, color: '#e67e22', emoji: '🏰' },
    { id: 2, title: 'Hábitos Atômicos', author: 'James Clear', genre: 'DESENVOLVIMENTO PESSOAL', genreColor: '#6c5ce7', rating: 4.8, reviews: 1420, color: '#00b894', emoji: '💡' },
    { id: 3, title: 'Entendendo Algoritmos', author: 'Aditya Bhargava', genre: 'ACADÊMICO E CIENTÍFICO', genreColor: '#6c5ce7', rating: 4.8, reviews: 640, color: '#a29bfe', emoji: '🧠' },
    { id: 4, title: 'Sapiens: Uma Breve História da Humanidade', author: 'Yuval Noah Harari', genre: 'NÃO-FICÇÃO', genreColor: '#6c5ce7', rating: 4.8, reviews: 2750, color: '#00cec9', emoji: '🌍' },
    { id: 5, title: 'O Pequeno Príncipe', author: 'Antoine de Saint-Exupéry', genre: 'INFANTOJUVENIL', genreColor: '#6c5ce7', rating: 4.8, reviews: 2750, color: '#00cec9', emoji: '🎈' }
];

// Inicialização de estados
let currentUser = JSON.parse(localStorage.getItem('bookhub_user')) || null;
let userFavorites = JSON.parse(localStorage.getItem('bookhub_favs')) || [];
let userShelf = JSON.parse(localStorage.getItem('bookhub_shelf')) || {};

// Ao carregar a página
document.addEventListener('DOMContentLoaded', () => {
    updateAuthUI();
    renderBooks(booksData, 'books-grid', 'explorar');
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
        document.getElementById('book-count').innerText = `${books.length} livro(s) encontrado(s)`;
    }

    books.forEach(book => {
        const isFav = userFavorites.includes(book.id) ? 'active' : '';
        const heartIcon = isFav ? 'fa-solid' : 'fa-regular';
        
        let shelfHtml = '';
        if (currentUser) {
            const currentStatus = userShelf[book.id] || "";
            shelfHtml = `
                <select class="form-select form-select-sm shelf-control mt-3" onchange="updateShelf(${book.id}, this.value)">
                    <option value="">Adicionar à estante...</option>
                    <option value="Desejo Ler" ${currentStatus === 'Desejo Ler' ? 'selected' : ''}>Desejo Ler</option>
                    <option value="Lendo" ${currentStatus === 'Lendo' ? 'selected' : ''}>Lendo</option>
                    <option value="Concluído" ${currentStatus === 'Concluído' ? 'selected' : ''}>Concluído</option>
                </select>`;
        }

        const card = `
            <div class="col-md-6 col-lg-3 mb-4">
                <div class="book-card">
                    <div class="book-card-top" style="background-color: ${book.color};">
                        <span class="book-emoji">${book.emoji}</span>
                        <button class="fav-btn ${isFav}" onclick="toggleFavorite(${book.id})">
                            <i class="${heartIcon} fa-heart"></i>
                        </button>
                    </div>
                    <div class="book-info">
                        <div class="book-genre" style="color: ${book.genreColor};">${book.genre}</div>
                        <h3 class="book-title">${book.title}</h3>
                        <div class="book-author">${book.author}</div>
                        <div class="book-rating">
                            <i class="fa-solid fa-star star-icon"></i> <strong>${book.rating}</strong> (${book.reviews} avaliações)
                        </div>
                        ${shelfHtml}
                    </div>
                </div>
            </div>
        `;
        container.innerHTML += card;
    });
}

// Filtro e Busca
function filterBooks() {
    const term = document.getElementById('searchInput').value.toLowerCase();
    const genre = document.getElementById('genreFilter').value;
    
    const filtered = booksData.filter(book => {
        const matchesTerm = book.title.toLowerCase().includes(term) || book.author.toLowerCase().includes(term);
        const matchesGenre = genre === 'Todos' || book.genre === genre;
        return matchesTerm && matchesGenre;
    });
    
    renderBooks(filtered, 'books-grid', 'explorar');
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
    const favBooks = booksData.filter(b => userFavorites.includes(b.id));
    renderBooks(favBooks, 'fav-grid', 'favoritos');
    if(favBooks.length === 0) document.getElementById('fav-grid').innerHTML = '<p class="text-muted">Nenhum livro favoritado ainda.</p>';
}

function loadShelf() {
    const shelfBooks = booksData.filter(b => userShelf[b.id]);
    renderBooks(shelfBooks, 'shelf-grid', 'estante');
    if(shelfBooks.length === 0) document.getElementById('shelf-grid').innerHTML = '<p class="text-muted">Sua estante está vazia.</p>';
}

// Autenticação (Login / Cadastro)
function register() {
    const nome = document.getElementById('regNome').value;
    const email = document.getElementById('regEmail').value;
    const senha = document.getElementById('regSenha').value;

    if (nome && email && senha) {
        const user = { nome, email, senha };
        localStorage.setItem('bookhub_account', JSON.stringify(user));
        alert('Cadastro realizado com sucesso! Você pode fazer login agora.');
        bootstrap.Modal.getInstance(document.getElementById('registerModal')).hide();
    }
}

function login() {
    const email = document.getElementById('loginEmail').value;
    const senha = document.getElementById('loginSenha').value;
    const account = JSON.parse(localStorage.getItem('bookhub_account'));

    if (account && account.email === email && account.senha === senha) {
        currentUser = account;
        localStorage.setItem('bookhub_user', JSON.stringify(currentUser));
        updateAuthUI();
        bootstrap.Modal.getInstance(document.getElementById('loginModal')).hide();
        filterBooks(); // Recarrega para mostrar controles de estante
    } else {
        alert('Credenciais inválidas!');
    }
}

function logout() {
    currentUser = null;
    localStorage.removeItem('bookhub_user');
    updateAuthUI();
    navigate('explorar');
    filterBooks(); // Remove controles de estante da view
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
