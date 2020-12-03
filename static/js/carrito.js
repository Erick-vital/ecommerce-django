// Agarra los elementos html boton 'agregar al carrito'
var updateBtns = document.getElementsByClassName('update-carrito')

// recorre el array updateBtns y actua al evento click del boton
for (var i = 0; i < updateBtns.length; i++) {
    // Funcion al hacer click
    updateBtns[i].addEventListener('click', function () {
        // agarra el valor de los dataset
        var productId = this.dataset.producto;
        var accion = this.dataset.action;
        console.log('productId: ', productId, 'accion: ', accion)

        console.log('usuario: ', user)
        if (user === 'AnonymousUser') {
            console.log('no estas logeado')
        } else {
            ActualizarPedidoUsuario(productId, accion)
        }
    })
}


function ActualizarPedidoUsuario(productId, accion) {
    console.log('estas logeado, enviando data...')

    // abosulte url path
    var url = 'http://127.0.0.1:8000/update_item/'

    /* fetch es una api que usamos para acceder y manipular
    peticiones y respuestas HTTP.
    fetch-documentacion:
    https://developer.mozilla.org/es/docs/Web/API/Fetch_API/Utilizando_Fetch */
    fetch(url, {
        method: 'POST',
        headers: {
            // la data enviada sera de tipo JSON
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        // body sera la data que enviaremos
        body: JSON.stringify({ 'productId': productId, 'accion': accion })
    })

        // promesa
        .then((response) => {
            return response.json()
        })
        .then((data) => {
            console.log('data: ', data)
            // recarga la pagina
            location.reload()
        })
}
