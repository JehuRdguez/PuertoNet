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
const logo = document.querySelectorAll('.logo');

window.addEventListener('scroll', () => {
    let value = window.scrollY;
    if (value > 50) {
        barraSuperior.style.backgroundColor = '#00132d';
        opcionesMenu.forEach(opcion => opcion.classList.add('hover-activo'));
        logo.forEach(option => option.classList.add('barra-activa'));
    } else {
        barraSuperior.style.backgroundColor = 'rgba(255, 255, 255, 0)';
        opcionesMenu.forEach(opcion => opcion.classList.remove('hover-activo'));
        logo.forEach(opcion => opcion.classList.remove('barra-activa'));
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
