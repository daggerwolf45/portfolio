let active_btn = document.querySelector('.cb');

function updateWidget(el) {
    active_btn.classList.remove('active');
    el.classList.add('active');
    active_btn = el;
}
