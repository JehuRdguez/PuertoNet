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
const iconoHamburguesa = document.querySelector('.hamburguesa');

let allowScrollFunction = true;

window.addEventListener('scroll', () => {
    if (allowScrollFunction) {
        let value = window.scrollY;
        if (value > 50) {
            barraSuperior.style.backgroundColor = '#00132d';
            opcionesMenu.forEach(opcion => opcion.classList.add('hover-activo'));
            logo.forEach(option => option.classList.add('barra-activa'));
            logoImg.src = 'static/assets/img/logo/logo.png';
            iconoHamburguesa.style.color = 'rgb(66, 135, 137)';
        } else {
            barraSuperior.style.backgroundColor = 'rgba(255, 255, 255, 0)';
            opcionesMenu.forEach(opcion => opcion.classList.remove('hover-activo'));
            logo.forEach(opcion => opcion.classList.remove('barra-activa'));
            logoImg.src = 'static/assets/img/logo/logoAzul.png';
            iconoHamburguesa.style.color = '';
        }
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
function toggleMenu() {
    allowScrollFunction = !allowScrollFunction; 
    navegacion.classList.toggle('mostrar-menu');
    barraFondoMenu.classList.toggle('mostrar-fondo');

    let value = window.scrollY;

    if (navegacion.classList.contains('mostrar-menu')) {
        menuHamburguesa.style.color = 'rgb(66, 135, 137)';
        logo.forEach(option => option.classList.add('barra-activa'));
        logoImg.src = 'static/assets/img/logo/logo.png';
    } else if (value === 0) { 
        menuHamburguesa.style.color = '';
        logo.forEach(opcion => opcion.classList.remove('barra-activa'));
        logoImg.src = 'static/assets/img/logo/logoAzul.png';
    }
}

function closeMenu() {
    allowScrollFunction = true; 
    navegacion.classList.remove('mostrar-menu');
    barraFondoMenu.classList.remove('mostrar-fondo');
    menuHamburguesa.style.color = '';
    logo.forEach(opcion => opcion.classList.remove('barra-activa'));
    logoImg.src = 'static/assets/img/logo/logoAzul.png';
}

const menuHamburguesa = document.getElementById('menuHamburguesa');
const navegacion = document.querySelector('.navegacion');
const barraFondoMenu = document.querySelector('.barra-fondo-menu');

menuHamburguesa.addEventListener('click', toggleMenu);
navegacion.addEventListener('click', (event) => {
    if (event.target.tagName === 'A') {
        closeMenu();
    }
});

window.addEventListener('resize', () => {
    if (window.innerWidth >= 800) {
        closeMenu();
    }
});

document.addEventListener('DOMContentLoaded', function () {
    // Verifica si la URL actual contiene "cursos.html"
    // Tu código AJAX aquí

    $(document).ready(function () {
        // Función para realizar la búsqueda
        function realizarBusqueda() {
            var query = $('#search-input').val().toLowerCase();

            // Oculta todos los videos
            $('.video-item').hide();

            // Muestra los videos que contienen la consulta en el título o descripción
            $('.video-item').each(function () {
                var tituloVideo = $(this).find('.video-title').text().toLowerCase();
                var descripcionVideo = $(this).find('.video-description').text().toLowerCase();

                if (tituloVideo.includes(query)) {
                    $(this).show();
                }
            });
        }

        // Asigna la función al evento input del campo de búsqueda
        $('#search-input').on('input', function () {
            realizarBusqueda();
        });

        // Captura el cambio en el filtro de categorías
        $('#filtro-categorias').change(function () {
            var selectedCategoria = $(this).val();

            // Oculta todos los videos
            $('.video-item').hide();

            // Muestra los videos que tienen la categoría seleccionada o todos si es "Todos"
            if (selectedCategoria === 'Todos') {
                $('.video-item').show();
            } else {
                // Itera sobre los elementos y muestra aquellos que tienen la categoría seleccionada
                $('.video-item').each(function () {
                    var categoriasVideo = $(this).data('categorias');

                    if (categoriasVideo.includes(selectedCategoria)) {
                        $(this).show();
                    }
                });
            }
        });

        // Captura el cambio en el filtro de orden
        $('#ordenar-por').change(function () {
            var opcionSeleccionada = $(this).val();

            if (opcionSeleccionada === 'AgregadosRecientemente') {
                // Ordena los videos por fecha de agregado
                ordenarPorFecha();
            } else if (opcionSeleccionada === 'Alfabeticamente') {
                // Ordena los videos alfabéticamente por título
                ordenarAlfabeticamente();
            }
        });
    });

    /*// Función para ordenar los videos por fecha de agregado
    function ordenarPorFecha() {
        var videos = $('.video-item').toArray();
        videos.sort(function (a, b) {
            var fechaA = new Date($(a).data('fecha'));
            var fechaB = new Date($(b).data('fecha'));
            return fechaB - fechaA;
        });
        console.log(videos)
        $('.video-container').empty().append(videos);
    }

    // Función para ordenar los videos alfabéticamente por título
    function ordenarAlfabeticamente() {
        var videos = $('.video-item').toArray();
        videos.sort(function (a, b) {
            var tituloA = $(a).find('.video-title').text().toLowerCase();
            var tituloB = $(b).find('.video-title').text().toLowerCase();
            return tituloA.localeCompare(tituloB);
        });

        $('.video-container').empty().append(videos);
    }*/
});


var mostrarAlert = document.querySelectorAll('.mostrarAlerta');

mostrarAlert.forEach(function(mostrarAlert) {
  mostrarAlert.addEventListener('click', function() {
    var contenido = document.getElementById('AlertaInicioSesion');
    contenido.style.display = (contenido.style.display === 'none' || contenido.style.display === '') ? 'block' : 'none';
    var elementosInicioForzado = document.querySelectorAll('.inicioForzado');
    elementosInicioForzado.forEach(function(elemento) {
      elemento.style.display = 'none';
    });
});

});