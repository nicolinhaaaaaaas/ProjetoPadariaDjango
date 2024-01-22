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
