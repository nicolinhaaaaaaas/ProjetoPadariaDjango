// Função para buscar sugestões
function buscarSugestoes(termoPesquisa) {
    $.ajax({
        url: '/buscar_sugestoes/',  // Substitua pela URL correta
        data: { termo: termoPesquisa },
        success: function(data) {
            exibirSugestoes(data.sugestoes);
        }
    });
}

// Função para exibir sugestões no dropdown
function exibirSugestoes(sugestoes) {
    const dropdown = document.getElementById('sugestoes-dropdown');
    dropdown.innerHTML = '';

    sugestoes.forEach(sugestao => {
        const li = document.createElement('li');
        const img = document.createElement('img');
        img.src = sugestao.imagem_url;
        img.alt = sugestao.nome;
        li.appendChild(img);

        const info = document.createElement('div');
        info.className = 'sugestao-info';
        info.innerHTML = `<p>${sugestao.nome}</p><p>R$ ${sugestao.preco}</p>`;
        li.appendChild(info);

        li.addEventListener('click', function() {
            expandirProduto(sugestao.nome, 'Descrição do produto', sugestao.preco, sugestao.imagem_url);
            // Ocultar dropdown após selecionar um produto
            dropdown.style.display = 'none';
        });

        dropdown.appendChild(li);
    });

    dropdown.style.display = sugestoes.length > 0 ? 'block' : 'none';
}

// Manipulador de eventos para a barra de pesquisa
const barraPesquisa = document.getElementById('barra-pesquisa');
barraPesquisa.addEventListener('input', function() {
    const termoPesquisa = barraPesquisa.value;
    buscarSugestoes(termoPesquisa);
});

function getCookie(name) {
    // Função para obter um cookie específico pelo nome
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

document.addEventListener('DOMContentLoaded', function() {
    // Selecione todos os botões de filtro
    var filterButtons = document.querySelectorAll('.filter-card.category-filter');

    // Adicione um ouvinte de evento de clique a cada botão
    filterButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            // Remova a classe 'ativo' de todos os botões de filtro
            filterButtons.forEach(function(btn) {
                btn.classList.remove('ativo');
            });

            // Adicione a classe 'ativo' ao botão clicado
            button.classList.add('ativo');

            // Lógica de filtragem aqui
            var category = button.getAttribute('data-category');
            console.log('Categoria selecionada:', category);

            // Adicione a lógica de filtragem que você precisa
            // Atualize a exibição dos produtos conforme necessário
        });
    });
});

