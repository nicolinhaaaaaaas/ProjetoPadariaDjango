function exibir_perfil(tipo){

    att_perfil = document.getElementById('att-perfil');
    mostrar_pedidos = document.getElementById('mostrar-pedidos');

    if(tipo == 1){
        att_perfil.style.display = 'none';
        mostrar_pedidos.style.display = 'block';
    }else if(tipo == 2){
        att_perfil.style.display = 'none';
        mostrar_pedidos.style.display = 'block';
    }
}

