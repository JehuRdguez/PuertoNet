// Efecto parallax
let titulo = document.getElementById('titulo');
let logoTitulo = document.getElementById('logoImg');
let fondo2 = document.getElementById('fondo2');

window.addEventListener('scroll', () => {
    let value = window.scrollY;

    titulo.style.marginTop = value * 0.5 + 'px';
    logoTitulo.style.marginTop = value * 0.5 + 'px';
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
const logo = document.querySelectorAll('.logo');
const logoImg = document.querySelector('.logo img');

window.addEventListener('scroll', () => {
    let value = window.scrollY;
    if (value > 50) {
        barraSuperior.style.backgroundColor = '#00132d';
        opcionesMenu.forEach(opcion => opcion.classList.add('hover-activo'));
        logo.forEach(option => option.classList.add('barra-activa'));
        logoImg.src = 'static/assets/img/logo/logo.png';
    } else {
        barraSuperior.style.backgroundColor = 'rgba(255, 255, 255, 0)';
        opcionesMenu.forEach(opcion => opcion.classList.remove('hover-activo'));
        logo.forEach(opcion => opcion.classList.remove('barra-activa'));
        logoImg.src = 'static/assets/img/logo/logoAzul.png';
    }
});


var iframe = document.querySelector('iframe');

// Verificar si el iframe existe
if (iframe) {
    // Modificar el tamaño del iframe
    iframe.width = 900;
    iframe.height = 500;
}


    var mostrarTextos = document.querySelectorAll('.mostrarTexto');

    mostrarTextos.forEach(function(mostrarTexto) {
      mostrarTexto.addEventListener('click', function() {
        var commentId = mostrarTexto.getAttribute('data-target');
        var contenido = document.getElementById('Mcontenido-' + commentId);
        contenido.style.display = (contenido.style.display === 'none' || contenido.style.display === '') ? 'block' : 'none';
      });
    });


// Menú hamburguesa
const menuHamburguesa = document.getElementById('menuHamburguesa');
const navegacion = document.querySelector('.navegacion');

menuHamburguesa.addEventListener('click', () => {
    navegacion.classList.toggle('mostrar-menu');
});

navegacion.addEventListener('click', (event) => {
    if (event.target.tagName === 'A') {
        navegacion.classList.remove('mostrar-menu');
    }
});

window.addEventListener('resize', () => {
    if (window.innerWidth >= 768) {
        navegacion.classList.remove('mostrar-menu');
    }
});