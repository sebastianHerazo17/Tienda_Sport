function registroAbono(idVenta, debe){
    const abonoInput = document.getElementById('abono-'+idVenta);
    let info = {
        idVenta: idVenta,
        valor: Number(abonoInput.value.replace(/[$ .]/gi,''))
    }
    if(info.valor<=debe)
    Swal.fire({
        title: 'Confirmar abono de '+abonoInput.value+' para la venta TS00'+idVenta,
        icon: 'info',
        showCancelButton: true,
        cancelButtonColor: '#3085d6',
        confirmButtonText: 'CONFIRMAR'
    }).then((result) => {
        if (result.isConfirmed) {
            axios.post('/abono', info)
            .then(resp=>{
                msg = resp.data;
                if(msg == "registrado"){
                    Swal.fire('ABONO REGISTRADO', '', 'success');
                    setTimeout(() => {
                        window.location.href = "/factura/"+info.idVenta;
                    }, 1000);
                } else {
                    Swal.fire('ALGO FALLÓ', 'Vuelve a recargar la página', 'error');
                }
            })
            .catch(err => {
                Swal.fire("Ocurrio un error", "Intentalo nuevamente", "error");
            });
        }
    });
    else Swal.fire('EL VALOR SUPERA LA DEUDA', '', 'warning');
     
}
