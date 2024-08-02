/** Отображение главного меню ***/
const main_menu = document.querySelector("#main-menu");
const switch_menu_display_btn = document.querySelector("#switch-menu-display");

// показ меню
switch_menu_display_btn.onclick = () => {
    if(main_menu.classList.contains("d-none")) {
        main_menu.classList.remove("d-none");
    } else{
        main_menu.classList.add("d-none");
    }
}

// клик не по меню
window.onclick = event => {
    parentNodeId = event.target.parentNode.id;
    if (parentNodeId != "switch-menu-display") {
        main_menu.classList.add("d-none");
    }
};


// наведение на элемент имени пользователя, если нет авторизации
const auth_auther_link = document.querySelector('#no-auth-user');
if(auth_auther_link) {
    auth_auther_link.onmouseover = () => {
        main_menu.classList.remove('d-none');
    }
}
