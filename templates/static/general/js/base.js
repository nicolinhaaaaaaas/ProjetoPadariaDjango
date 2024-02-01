let sidebar = document.querySelector(".sidebar");
let closeBtn = document.querySelector("#btn");
let searchBtn = document.querySelector(".bx-search");

closeBtn.addEventListener("click", ()=>{
    sidebar.classList.toggle("open");
    menuBtnChange();
});

//searchBtn.addEventListener("click", ()=>{ 
//    sidebar.classList.toggle("open");
//    menuBtnChange();
//});

function menuBtnChange() {
if(sidebar.classList.contains("open")){
    closeBtn.classList.replace("bx-menu", "bx-menu-alt-right");
}else {
    closeBtn.classList.replace("bx-menu-alt-right","bx-menu");
}
}


// Função para exibir a mensagem de confirmação e realizar o logout
function confirmarLogout() {
    if (confirm("Tem certeza que deseja sair?")) {
        window.location.href = "{% url 'logout' %}";
    }
}

// Adiciona um ouvinte de evento de clique ao botão de logout
document.getElementById("logout-btn").addEventListener("click", function(event) {
    event.preventDefault(); // Evita o comportamento padrão de redirecionamento
    confirmarLogout(); // Chama a função para exibir a mensagem de confirmação
});
