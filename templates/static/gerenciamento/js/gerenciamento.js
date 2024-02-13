$(document).ready(function() {
    $('.search-btn').on('click', function() {
        pesquisarProdutos();
    });
});

var contadorIngrediente = 1; // Variável para contar o número de ingredientes adicionados

function addIngrediente() {
    var container = document.getElementById("form-ingrediente");
    
    var html = "<div class='row'>";
    html += "<div class='col-md'>";
    html += "<input type='text' class='ingrediente-entrada' id='nome_ingrediente_" + contadorIngrediente + "' name='nome_ingrediente_" + contadorIngrediente + "' placeholder='Nome do ingrediente' >";
    html += "</div>";
    html += "<div class='col-md'>";
    html += "<input type='text' class='ingrediente-entrada' id='unidade_medida_" + contadorIngrediente + "' name='unidade_medida_" + contadorIngrediente + "' placeholder='Unidade de medida' >";
    html += "</div>";
    html += "</div>";

    container.innerHTML += html;

    contadorIngrediente++; // Incrementa o contador de ingredientes
}

function exibir_produto(tipo){
    
    var add_produto = document.getElementById("add-produto");
    var att_produto = document.getElementById("att-produto");

    if(tipo == '1'){
        
        add_produto.style.display = "block";
        att_produto.style.display = "none";
        console.log("ADD produto")
    }else if(tipo == '2'){
        console.log("ATT produto")
        add_produto.style.display = "none";
        att_produto.style.display = "block";
    }
}

function exibir_funcionario(tipo){
    
    var add_funcionario = document.getElementById("add-funcionario");
    var att_funcionario = document.getElementById("att-funcionario");

    if(tipo == '1'){
        
        add_funcionario.style.display = "block";
        att_funcionario.style.display = "none";
        console.log("ADD funcionario")
    }else if(tipo == '2'){
        console.log("ATT funcionario")
        add_funcionario.style.display = "none";
        att_funcionario.style.display = "block";
    }
}

function update_funcionario(){
    id = document.getElementById("id_funcionario").value;
    nome = document.getElementById("nome_funcionario").value;
    telefone = document.getElementById("telefone_funcionario").value;
    cargo = document.getElementById("cargo").value;
    salario = document.getElementById("salario").value;

    fetch('/gerenciamento/updateFuncionario/' + id, {
        method: "POST",
        headers: {
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
            nome_funcionario: nome,
            telefone_funcionario: telefone,
            cargo: cargo,
            salario: salario,
        })
    }).then(function (result){
        return result.json()
    }).then (function(data){
        if(data['status'] == 200){
            nome_funcionario = data['nome_funcionario'];
            telefone_funcionario = data['telefone_funcionario'];
            cargo = data['cargo'];
            salario = data['salario'];
            console.log('Sucesso')
        }else{
            console.log('Erro')
        }
    })
}

function dados_funcionario() {
    funcionario = document.getElementById('funcionario-select')
    csrf_token = document.querySelector('[name=csrfmiddlewaretoken]').value;
    id_funcionario = funcionario.value;
    console.log(id_funcionario)

    fetch('/gerenciamento/dados_funcionario/', {
        method: "POST",
        headers: {
            'X-CSRFToken': csrf_token,
        },
        body: JSON.stringify({ id_funcionario: id_funcionario }),
    }).then(response => response.json())
    .then(data => {
        // Preencher os campos de input com os dados do funcionário
        document.getElementById('nome_funcionario').value = data.funcionario.nome_funcionario;
        document.getElementById('telefone_funcionario').value = data.funcionario.telefone_funcionario;
        document.getElementById('cargo').value = data.funcionario.cargo;
        document.getElementById('salario').value = data.funcionario.salario;
    })
    .catch(error => console.error('Erro ao buscar dados do funcionário:', error));
}



