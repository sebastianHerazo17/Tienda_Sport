// FUNCIONES PARA INPUT QUE MUESTRE EN FORMATO MONEDA
function moneda(valor) {
    const formato = new Intl.NumberFormat('es-CO', {
        style: 'currency',
        currency: 'COP',
        minimumFractionDigits: 0, 
    });

    return formato.format(valor);
}


function entrada(event, i) {
    const input = event.target;
    let cambio = input.value.replace(/[^\d]/g, ''); // Elimina caracteres no numéricos
    if (cambio === '') {
        input.value = 0; // Si está vacío, deja el campo en 0
    } else {
        const valorNumerico = parseInt(cambio, 10); // Convierte a número
        input.value = moneda(valorNumerico); // Aplica el formato de moneda
        carrito[i].descuento = Number(document.getElementById('descuento-'+i).value.replace(/[$ .]/gi,'')); // Si se quiere guardar el valor se deben reemplazar los siguientes signos
        document.getElementById('desc').innerText = moneda(totalDescuento());
        document.getElementById('total').innerText = moneda(total());
    }
}

//ENVIO DE VENTA
// inputs
const tipoPago = document.getElementById('tipoPago');
const nombreCli = document.getElementById('nombreCli');
const numeroCli = document.getElementById('numeroCli');
const selectCli = document.getElementById('selectCli');

//Registrar un cliente
function registrarCliente() {
    let cliente = {nombre: nombreCli.value, celular: numeroCli.value}
    axios.post('/cliente', cliente)
    .then(msg => {
        clientes = msg.data;
        listarClientes();
        nombreCli.value = "";
        numeroCli.value = "";
    })
    .catch(err=>{
        console.log(err);
    })
}


