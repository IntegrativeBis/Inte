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
    





/*
    document.getElementById('buscador').addEventListener('input', function() {
        const query = this.value.trim().toLowerCase();  // Obtener el valor del input
        const resultadosDiv = document.getElementById('resultados');  // Contenedor donde mostrar los resultados
    
        // Limpiar los resultados anteriores
        resultadosDiv.innerHTML = '';
    
        if (query) {
            fetch(`/buscar_productos?q=${query}`)
                .then(response => response.json())
                .then(data => {
                    if (data.length > 0) {
                        data.forEach(producto => {
                            // Crear contenedor para cada producto
                            const item = document.createElement('div');
                            item.classList.add('producto');
    
                            // Crear un elemento <img> para la imagen del producto
                            const img = document.createElement('img');
                            img.src = producto.imagen;  // URL de la imagen
                            img.alt = producto.descripcion;  // Texto alternativo
                            img.style.width = '100px';  // Ajustar el tamaño según tus necesidades
                            img.style.height = '100px';
    
                            // Crear un elemento <p> para la descripción del producto
                            const descripcion = document.createElement('p');
                            descripcion.textContent = producto.descripcion;
    
                            // Crear un elemento <p> para el precio
                            const precio = document.createElement('p');
                            precio.textContent = `$${producto.precio || 'N/A'}`;
    
                            // Añadir la imagen, descripción y precio al contenedor del producto
                            item.appendChild(img);
                            item.appendChild(descripcion);
                            item.appendChild(precio);
    
                            // Añadir el contenedor del producto a los resultados
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
            // Si no hay texto en el campo de búsqueda, limpiar los resultados
            resultadosDiv.innerHTML = '';
        }
    });
    */