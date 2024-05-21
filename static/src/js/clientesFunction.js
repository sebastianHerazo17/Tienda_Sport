function eliminarCliente(id, cliente){
    Swal.fire({
        title: 'ANTES DE ELIMINAR',
        text: "Al borrar a "+cliente+" se dejaran sus ventas y aparecerá como \"Borrado\" en el registro de ventas.",
        icon: 'info',
        showCancelButton: true,
        confirmButtonText: 'QUIERO BORRARLO'
    }).then((result) => {
        if (result.isConfirmed) {
            Swal.fire({
                title: '¿Estás seguro de eliminar al cliente: '+cliente+'?',
                text: "No podrás revertir esto.",
                icon: 'question',
                showCancelButton: true,
                confirmButtonText: 'BORRAR'
            }).then((Rr) => {
                if (Rr.isConfirmed) {
                    window.location.href = '/eliminar_cliente/'+id
                };
            });
        };
    });
}

function modificarCliente(id){
    let nombre = document.getElementById('nombreCli-'+id)
    let celular = document.getElementById('numeroCli-'+id)
    let cliente = {
        nombre: nombre.value,
        celular: celular.value

    }
    Swal.fire({
        title: '¿Está seguro de modificar este cliente?',
        icon: 'info',
        showCancelButton: true,
        confirmButtonText: 'Sí'
    }).then((result) => {
        if (result.isConfirmed) axios.post('/modificar_cliente/'+id, cliente)
            .then(resp => {
                Swal.fire("CLIENTE MODIFICADO", "", "success");
                setTimeout(() => {
                window.location.href = "/clientes"
                }, 1200);
            }).catch(err => {
                Swal.fire("OCURRIÓ UN ERROR", "Intentelo nuevamente.", "error");
            })
    });
}