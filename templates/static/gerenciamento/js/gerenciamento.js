function addIngrediente(){
    container = document.getElementById("form-ingrediente")

    html += "<br> <div class='row'> <div class='label-text'> <label for='nome-ingrediente'>Nome</label> <input type='text' id='nome-ingrediente' name='nome-ingrediente' placeholder='Nome do ingrediente' value='{{nome_ingrediente}}'> </div>"
    html += "<br> <div class='row'> <div class='label-text'> <label for='unidadeMedida'>Unidade de medida</label> <input type='text' id='unidadeMedida' name='unidadeMedida' placeholder='Unidade de medida' value='{{unidade_Medida}}'> </div>"
    html += "<br> <div class='row'> <div class='label-text'> <label for='quantidade'>Quantidade</label> <input type='text' id='quantidade' name='quantidade' placeholder='Quantidade' value='{{quantidade_usada}}'> </div> </div>"

    container.innerHTML += html
}