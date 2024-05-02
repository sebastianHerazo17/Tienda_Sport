function eliminarCliente(id){
    Swal.fire({
        title: 'ANTES DE ELIMINAR',
        text: "Al borrar este cliente se dejaran sus ventas, pero aparecerá como \" Borrado\" en el registro.",
        icon: 'info',
        showCancelButton: true,
        confirmButtonText: 'QUIERO BORRARLO'
    }).then((result) => {
        if (result.isConfirmed) {
            Swal.fire({
                title: '¿Estás seguro de eliminar al cliente?',
                text: "No podrás revertir esto.",
                icon: 'warning',
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