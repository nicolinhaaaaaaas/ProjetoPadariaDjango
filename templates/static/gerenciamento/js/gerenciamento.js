

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
    console.log(id)
    nome_funcionario = document.getElementById("nome_funcionario").value;
    console.log(nome_funcionario)
    telefone_funcionario = document.getElementById("telefone_funcionario").value;
    console.log(telefone_funcionario)
    cargo = document.getElementById("cargo").value;
    console.log(cargo)
    salario = document.getElementById("salario").value;
    console.log(salario)

    fetch('/gerenciamento/updateFuncionario/' + id, {
        method: "POST",
        headers: {
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
            nome_funcionario: nome_funcionario,
            telefone_funcionario: telefone_funcionario,
            cargo: cargo,
            salario: salario,
        })
    }).then(function (result){
        return result.json()
    }).then (function(data){
        console.log(data)
        nome_funcionario = data['nome_funcionario'];
        telefone_funcionario = data['telefone_funcionario'];
        cargo = data['cargo'];
        salario = data['salario'];
        console.log('Sucesso')
    })
}

function dados_funcionario() {
    funcionario = document.getElementById('funcionario-select')
    csrf_token = document.querySelector('[name=csrfmiddlewaretoken]').value;
    id_funcionario = funcionario.value;
    console.log(id_funcionario)

    data =  new FormData();
    data.append('id_funcionario', id_funcionario);

    fetch('/gerenciamento/dados_funcionario/', {
        method: "POST",
        headers: {
            'X-CSRFToken': csrf_token,
        },
        body: data
    }).then(function(result){
        return result.json()
    }).then(function(data){
        console.log(data)
        document.getElementById('form-att-funcionario').style.display = 'block'

        id_funcionario = document.getElementById('id_funcionario')
        id_funcionario.value = data['id_funcionario']

        nome_funcionario = document.getElementById('nome_funcionario')
        nome_funcionario.value = data['nome_funcionario']

        telefone_funcionario = document.getElementById('telefone_funcionario')
        telefone_funcionario.value = data['telefone_funcionario']

        cargo = document.getElementById('cargo')
        cargo.value = data['cargo']
        console.log(data['cargo'])

        salario = document.getElementById('salario')
        salario.value = data['salario']
        console.log(data['salario'])

    })
    .catch(error => console.error('Erro ao buscar dados do funcionário:', error));
}



