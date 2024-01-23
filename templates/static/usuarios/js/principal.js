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

function adicionarAoCarrinho(nomeProduto, precoProduto) {
    // Lógica para adicionar o produto ao carrinho
    // Isso pode incluir uma solicitação AJAX para o Django, onde você salvará o produto no carrinho do usuário

    // Exemplo de uma solicitação AJAX usando Fetch API
    fetch('/adicionar_ao_carrinho/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),  // Função para obter o token CSRF do cookie
        },
        body: JSON.stringify({
            nome_produto: nomeProduto,
            preco_produto: precoProduto,
        }),
    })
    .then(response => response.json())
    .then(data => {
        alert(data.mensagem);
        // Você pode adicionar mais lógica aqui, como atualizar dinamicamente o conteúdo do carrinho na interface do usuário
    })
    .catch(error => {
        console.error('Erro ao adicionar ao carrinho:', error);
        alert('Ocorreu um erro ao adicionar o produto ao carrinho.');
    });
}

function getCookie(name) {
    // Função para obter um cookie específico pelo nome
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}