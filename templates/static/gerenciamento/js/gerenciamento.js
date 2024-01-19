function addIngrediente() {
    var container = document.getElementById("form-ingrediente");

    var html = "";
    html += "<br> <div class='row'> <div class='col-md'> <input type='text' class='ingrediente-entrada' id='nome-ingrediente' name='nome-ingrediente' placeholder='Nome do ingrediente'> </div>";
    html += "<br> <div class='col-md'> <input type='text' class='ingrediente-entrada' id='unidadeMedida' name='unidadeMedida' placeholder='Unidade de medida'> </div>";
    html += "<br> <div class='col-md'> <input type='text' class='ingrediente-entrada' id='quantidade' name='quantidade' placeholder='Quantidade'> </div> </div>";

    container.innerHTML += html;
}

function exibir_funcionario(tipo){
    
    add_funcionario = document.getElementById("add_funcionario");
    att_funcionario = document.getElementById("att_funcionario");

    if(tipo == '1'){
        console.log("ADD funcionario")
        add_funcionario.style.display = "none";
        att_funcionario.style.display = "block";
    }else if(tipo == '2'){
        console.log("ATT funcionario")
        add_funcionario.style.display = "block";
        att_funcionario.style.display = "none";
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

function dados_funcionario(){
    funcionario = document.getElementById('funcionario-select')
    csrf_token = document.querySelector('[name=csrfmiddlewaretoken]').value;
    id_funcionario = funcionario.value;

    data = new FormData()
    data.append('id_funcionario', id_funcionario)

    
}

