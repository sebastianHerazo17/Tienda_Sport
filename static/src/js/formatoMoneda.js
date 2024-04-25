function moneda(valor) {
    const formato = new Intl.NumberFormat('es-CO', {
        style: 'currency',
        currency: 'COP',
        minimumFractionDigits: 0, 
    });

    return formato.format(valor);
}
function formatoMoneda(event) {
    const input = event.target;
    let cambio = input.value.replace(/[^\d]/g, ''); // Elimina caracteres no numéricos
    if (cambio === '') {
        input.value = 0; // Si está vacío, deja el campo en 0
    } else {
        const valorNumerico = parseInt(cambio, 10); // Convierte a número
        input.value = moneda(valorNumerico); // Aplica el formato de moneda
    }
}