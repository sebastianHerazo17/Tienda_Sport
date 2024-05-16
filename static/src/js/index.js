// fecha actual
let fechaActual = new Date();

// //Colocar el valor de el primer día del mes
let primerDiaMes = new Date(fechaActual.getFullYear(), fechaActual.getMonth(), 1).toISOString().split('T')[0];
const fechaInicio = document.getElementById('fechaInicio');
fechaInicio.value = primerDiaMes;

// Fecha actual para el input de fecha final
let today = fechaActual.toISOString().split('T')[0];
const fechaFin = document.getElementById('fechaFin');
const vistaGraf = document.getElementById('vistaGraf');
fechaInicio.setAttribute('max', today);
fechaFin.setAttribute('min', fechaInicio.value);
fechaFin.setAttribute('max', today);
console.log(today);
fechaFin.value = today;
const contGanancias = document.getElementById("contGanancias");
const etiquetaG = document.getElementById("etiquetaG");

function finanzas(fi, ff, group) {
    axios.get(`/finanzas/${fi}/${ff}/${group}`)
    .then(resp => {
        f = resp.data;
        console.log(f);
        document.getElementById("ingresos").innerText = moneda(f.ingresos);
        document.getElementById("egresos").innerText = moneda(f.egresos);
        if(f.ganancias<0){
            contGanancias.classList.add('bg-red-50');
            contGanancias.classList.add('text-red-500');
            etiquetaG.innerText = "Perdidas";
        } else {
            contGanancias.classList.remove('bg-red-50');
            contGanancias.classList.remove('text-red-500');
            etiquetaG.innerText = "Ganancias";
        }
        document.getElementById("ganancias").innerText = moneda(f.ganancias);
        fechaFin.setAttribute('min', fechaInicio.value);
        graficaInforme(f.informePagos);
        graficaConteo(f.informeConteo);
    })
    .catch(err => {
        console.log(err);
        alert('Ocurrio error: '+err)
    })
}

finanzas(fechaInicio.value, fechaFin.value, vistaGraf.value);

fechaInicio.addEventListener('input', () => { finanzas(fechaInicio.value, fechaFin.value, vistaGraf.value) });
fechaFin.addEventListener('input', () => { finanzas(fechaInicio.value, fechaFin.value, vistaGraf.value) });
vistaGraf.addEventListener('change', () => { finanzas(fechaInicio.value, fechaFin.value, vistaGraf.value) });

const textDate = document.getElementById('textDate');
setInterval(() => {
    fechaActual = new Date();
    textDate.innerText = 'Fecha y hora: '+ fechaActual.toLocaleString();
}, 1000);


// CÓDIGO PARA GRÁFICA
const graph = document.querySelector("#grafica");
const graphC = document.querySelector('#graficaCont')
var Grafico;
var GraficoCont;
function graficaInforme(informe) {
    let labels = informe.map(item => item.fecha);
    let totales = informe.map(item => item.total);
    const dataset = [{
        label: "Ingresos",
        data: totales,
        backgroundColor: 'rgba(69, 248, 84, 0.8)',
        fill: false
    }];
    const data = {
        labels: labels,
        datasets: dataset
    }; 
    const config = {
        type: 'bar',
        data: data,
    };
    if(Grafico) Grafico.destroy();
    Grafico = new Chart(graph, config);
}

function graficaConteo(informe) {
    let labels = informe.map(item => item.fecha);
    let totales = informe.map(item => item.total);
    const dataset = [{
        label: "Ventas totales",
        data: totales,
        backgroundColor: '#90e0ef',
        fill: false
    }];
    const data = {
        labels: labels,
        datasets: dataset
    }; 
    const config = {
        type: 'bar',
        data: data,
    };
    if(GraficoCont) GraficoCont.destroy();
    GraficoCont = new Chart(graphC, config);
}


