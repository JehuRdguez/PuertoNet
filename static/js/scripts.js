
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

    //restablecer
    $('.Restablecer').click(function (event) {
        event.preventDefault(); // Evita que el enlace redireccione directamente
        location.href = "Cursos"

    });

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
        // Obtiene la categoría de la URL
        var categoriaEnUrl = obtenerCategoriaDeUrl();

        // Si hay una categoría en la URL, establece el valor del select y activa el filtrado
        if (categoriaEnUrl) {
            $('#filtro-categorias').val(categoriaEnUrl);

            // Aquí puedes agregar la lógica de filtrado directamente o activar el evento 'change'
            // dependiendo de cómo estés manejando el filtro en tu código actual
            $('#filtro-categorias').trigger('change');
        }

        // Maneja clics en los enlaces de categoría
        $('.filtro-link').click(function (event) {
            event.preventDefault(); // Evita que el enlace redireccione directamente

            var categoria = $(this).data('categoria');
            window.location.href = $(this).attr('href'); // Redirige a la URL del enlace

            // Aquí puedes ajustar la lógica según tus necesidades, como activar el filtrado directamente
            // o realizar otras acciones antes de la redirección
        });
        });

        function obtenerCategoriaDeUrl() {
        var urlParams = new URLSearchParams(window.location.search);
        return urlParams.get('categoria');
        }

        // Resto de tu código de filtrado AJAX
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


var currentPage = 1;
var commentsPerPage = 3;
var comments = document.querySelectorAll('.card');

function showPage(page) {
    var startIndex = (page - 1) * commentsPerPage;
    var endIndex = startIndex + commentsPerPage;

    comments.forEach(function (comment, index) {
        comment.style.display = (index >= startIndex && index < endIndex) ? 'block' : 'none';
    });

    // Elimina la clase 'active' de todos los círculos
    document.querySelectorAll('.page').forEach(function (circle) {
        circle.classList.remove('active');
    });

    // Añade la clase 'active' al círculo actual
    document.querySelector('.page:nth-child(' + page + ')').classList.add('active');
}

function changePage(action) {
    if (action === 'prev' && currentPage > 1) {
        currentPage--;
    } else if (action === 'next' && currentPage < Math.ceil(comments.length / commentsPerPage)) {
        currentPage++;
    } else if (typeof action === 'number') {
        currentPage = action;
    }

    showPage(currentPage);
}

// Mostrar la primera página al cargar la página
showPage(currentPage);

