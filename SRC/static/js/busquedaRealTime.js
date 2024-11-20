    document.getElementById('buscador').addEventListener('input', function() {
        const query = this.value.trim().toLowerCase();  // Obtener el valor del input y limpiarlo de espacios adicionales
        const resultadosDiv = document.getElementById('resultados');  // Contenedor donde mostrar los resultados
        // Limpiar los resultados anteriores
        resultadosDiv.innerHTML = '';
        if (query) {
            fetch(`/buscar_productos?q=${query}`)
                .then(response => response.json())
                .then(data => {
                    if (data.length > 0) {
                        data.forEach(producto => {
                            const item = document.createElement('div');
                            item.classList.add('producto');
                            item.textContent = `${producto.descripcion} - $${producto.precio || 'N/A'}`;
                            resultadosDiv.appendChild(item);
                        });
                    } else {
                        resultadosDiv.innerHTML = 'No se encontraron productos';
                    }
                })
                .catch(error => {
                    console.error('Error al buscar productos:', error);
                });
        } else {
            // Si no hay texto en el campo de búsqueda, mostrar mensaje vacío
            resultadosDiv.innerHTML = '';
        }
    });
    
let debounceTimeout;
document.getElementById('buscador').addEventListener('input', function() {
    clearTimeout(debounceTimeout);
    debounceTimeout = setTimeout(() => {
        // Aquí va el código para la búsqueda
    }, 30); // Espera 300 ms antes de realizar la búsqueda
});
