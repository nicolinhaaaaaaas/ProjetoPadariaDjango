
function confirmarExclusao() {
    if (window.confirm("Tem certeza de que deseja excluir o perfil?")) {
        excluirPerfil();
    } else {
        // Código a ser executado se o usuário cancelar a exclusão
        console.log("Exclusão cancelada pelo usuário.");
    }
}

function excluirPerfil() {
    fetch('/usuarios/excluir_perfil/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({})
    })
    .then(response => {
        if (response.ok) {
            alert("Perfil excluído com sucesso!");
            window.location.href = '/usuarios/cadastro/';
        } else {
            alert("Ocorreu um erro ao excluir o perfil.");
        }
    })
    .catch(error => console.error('Erro ao excluir o perfil:', error));
}
