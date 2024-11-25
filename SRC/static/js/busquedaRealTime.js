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
                            item.classList.add('producto');      //Aplicar estilos desde CSS
                            item.textContent = `${producto.descripcion}`;
                            item.dataset.id = producto.id_producto; // Guardar el ID del producto en un atributo data-id

                                // Agregar evento de clic para redireccionar al detalle del producto
                            item.addEventListener('click', function () {
                                const id_producto = this.dataset.id;
                                window.location.href = `/producto/${id_producto}`; // Redirigir con el ID del producto
                            });

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
    
