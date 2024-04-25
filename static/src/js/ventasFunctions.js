// FUNCIONES PARA LA TABLA DE PRODUCTOS
let tabPro = document.getElementById('tabPro');


if(productos.length>0) listarProductos();
if(clientes.length>0) listarClientes();

function listarProductos() {
    tabPro.innerHTML = "";
    productos.forEach(p => {
        let i = p.idProducto;
        tabPro.innerHTML += `
        <tr class="bg-white hover:bg-gray-50 ">
            <td class="px-6 py-4 font-medium text-gray-900">
                ${ p.tipo }
            </td>
            <td class="px-6 py-4">
                ${ p.referencia }
            </td>
            <td class="px-6 py-4 text-center">
                ${ p.cantidad }
            </td>
            <td class="px-6 py-4">
                ${ moneda(p.precio) }
            </td>
            <td class="px-6 py-4">
                <input name="cantidad-${i}" type="number" value="1" id="cantidad-${i}" min="1" max="${p.cantidad}" class="bg-gray-50 w-14 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block px-2.5 py-1 " placeholder="1" required />
            </td>
            <td class="px-6 py-4 flex gap-2">
                <button type="button" onclick="accionCarrito(${i}, 'sv')" class="focus:outline-none text-white bg-indigo-50 hover:bg-indigo-200 focus:ring-2 focus:ring-indigo-300 font-medium rounded-lg text-sm p-2">
                    <svg class="w-5 h-5 text-indigo-800 " aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24">
                        <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 4h1.5L9 16m0 0h8m-8 0a2 2 0 1 0 0 4 2 2 0 0 0 0-4Zm8 0a2 2 0 1 0 0 4 2 2 0 0 0 0-4Zm-8.5-3h9.25L19 7h-1M8 7h-.688M13 5v4m-2-2h4"/>
                    </svg>                                              
                </button>
                <button type="button" onclick="accionCarrito(${i}, 'dt')" class="focus:outline-none text-white bg-red-100 hover:bg-red-200 focus:ring-2 focus:ring-red-300 font-medium rounded-lg text-sm p-2">
                    <svg class="w-5 h-5 text-red-500 hover:text-red-800" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24">
                        <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7.757 12h8.486M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z"/>
                    </svg>                         
                </button>
            </td>
        </tr>`;
    });
}




// FUNCIONES DE CARRITO DE COMPRAS

function accionCarrito(id, action) {
    const cantidad = Number(document.getElementById('cantidad-'+id).value);
    let producto = productos.find(p=>p.idProducto === id);
    let productoCarrito = carrito.find(p=> p.idProducto === producto.idProducto);
    if(action === 'sv'){
        if(productoCarrito === undefined) carrito.push({...producto, orden: cantidad, descuento: 0});
        else {
        if(productoCarrito.orden<producto.cantidad&&(productoCarrito.orden+cantidad)<=producto.cantidad) carrito.find(p=> p.idProducto === productoCarrito.idProducto).orden += cantidad
        else Swal.fire("LA CANTIDAD SUPERA EL STOCK DISPONIBLE", "", "warning");
        }
    } else if(action === 'dt'){
        if(productoCarrito === undefined) Swal.fire("EL PRODUCTO NO ESTÁ EN EL CARRITO", "", "warning");
        else if((productoCarrito.orden-cantidad) <= 0){
            let i = carrito.findIndex(p => p.idProducto === productoCarrito.idProducto);
            carrito.splice(i, 1);
        }
        else if(productoCarrito.orden>0) carrito.find(p=> p.idProducto === productoCarrito.idProducto).orden -= cantidad;
    }
    listarCarrito();
}


function listarCarrito() {
    tabBody.innerHTML = '';
    carrito.forEach((prod, i) => {
        tabBody.innerHTML += `
        <tr class="bg-white">
            <td class="px-6 py-4 font-semibold text-gray-900 ">
                ${prod.tipo}
            </td>
            <td class="px-6 py-4 font-semibold text-gray-900 ">
                ${prod.referencia}
            </td>
            <td class="px-6 py-4">
                ${prod.orden}
            </td>
            <td class="px-6 py-4">
                ${moneda((prod.precio*prod.orden))}
            </td>
            <td class="px-6 py-4">
                <div class="flex items-center">
                        <input type="text" id="descuento-${i}" onblur="entrada(event,${i})" oninput="entrada(event,${i})" class="bg-gray-50 w-24 text-right border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block px-2.5 py-1" placeholder="0" required />
                </div>
            </td>
        </tr>
        `});
        tabBody.innerHTML += `
        <tr class="bg-white border-t">
            <td class="px-6 py-4"></td>
            <td class="px-6 py-4"></td>
            <td class="px-6 py-4 font-semibold text-gray-900 ">
                TOTAL
            </td>
            <td id="total" class="px-6 py-4 font-semibold text-gray-900 ">
                ${moneda(total())}
            </td>
            <td class="px-6 py-4"></td>
        </tr>
        `;
}

function total() {
    let total = 0;
    for (const p of carrito) {
        total += (p.precio*p.orden) - p.descuento;
    }
    return total;
}


// LISTAR CLIENTES
function listarClientes() {
    selectCli.innerHTML = '';
    clientes.forEach(c => {
        selectCli.innerHTML += `
            <option value="${c.identificacion}">${c.nombre}  ${c.celular}</option>
        `;
    })
}

// REALIZAR VENTA

const tipoVenta = document.getElementById('tipoVenta');

 function enviarVenta() {
    let venta = {
      identificacion: selectCli.value,
      tipoPago: tipoVenta.value,
      totalPagar: total(),
      totalPagado: 20000,
      carrito: carrito
    }

    axios.post('/registra_venta', venta)
    .then(msg => {
        console.log(msg.data);
    })
    .catch(err => {
        console.log(err);
    });
 }