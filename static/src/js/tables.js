function buscar(tabla, search){
    // Obtener la tabla y el campo de búsqueda
    const table = document.getElementById(tabla);
    const searchInput = document.getElementById(search);
    const searchText = searchInput.value.toLowerCase();

    for (let i = 1; i < table.rows.length; i++) {
        // Obtener el texto de la fila actual y convertirlo a minúsculas
        const rowText = table.rows[i].innerText.toLowerCase();

        // Mostrar u ocultar la fila según si coincide con el texto de búsqueda
        if (rowText.includes(searchText)) {
            table.rows[i].style.display = '';
        } else {
            table.rows[i].style.display = 'none';
        }
    }
    
}