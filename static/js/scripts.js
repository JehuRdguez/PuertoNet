// Efecto parallax
let titulo = document.getElementById('titulo');
let fondo2 = document.getElementById('fondo2');

window.addEventListener('scroll', () => {
    let value = window.scrollY;

    titulo.style.marginTop = value * 0.5 + 'px';
})

// Animaciones al entrar (en progreso)
let timeline = gsap.timeline();
// timeline.from(".puerto" ,{
//         y: window.innerHeight - document.querySelector(".puerto").getBoundingClientRect().top,
//         duration: 1,
//     }, "1   "
// );

// Barra del menú
const barraSuperior = document.querySelector('.barra-superior');
const opcionesMenu = document.querySelectorAll('.linea-hover');

window.addEventListener('scroll', () => {
    let value = window.scrollY;
    if (value > 50) {
        barraSuperior.style.backgroundColor = '#00132d';
        opcionesMenu.forEach(opcion => opcion.classList.add('hover-activo'));
    } else {
        barraSuperior.style.backgroundColor = 'rgba(255, 255, 255, 0)';
        opcionesMenu.forEach(opcion => opcion.classList.remove('hover-activo'));
    }
});