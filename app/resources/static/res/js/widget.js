let active_btn = document.querySelector('.cb.active');

function updateWidget(el) {
    console.log('thwack')
    try {
        active_btn.classList.remove('active');
    } catch {}
    el.classList.add('active');
    active_btn = el;
}
