let historial = [];


function showAlert(message) {
    const alertModal = new bootstrap.Modal(document.getElementById('alertModal'));
    document.getElementById('alertModalBody').innerText = message;
    alertModal.show();
    
}document.getElementById('sortButton').addEventListener('click', function () {
    const dataInputText = document.getElementById('dataInputText').value;
    const fileInput = document.getElementById('dataInputFile');
    const file = fileInput.files[0];

    let data = [];

    if (file) {
        const reader = new FileReader();
        reader.onload = function (e) {
            const csvContent = e.target.result;
            data = csvContent.split('\n').map(line => parseFloat(line.trim())).filter(item => !isNaN(item));

            processData(data);
        };
        reader.readAsText(file);
    } else if (dataInputText) {
        data = dataInputText.split(',').map(item => parseFloat(item.trim())).filter(item => !isNaN(item));
        processData(data);
    } else {
        showAlert('Por favor, ingresa algunos datos o selecciona un archivo CSV para ordenar.');
    }

    // Limpiar los campos de entrada de datos después de procesar
    fileInput.value = '';  // Limpia el archivo cargado
    document.getElementById('dataInputText').value = '';  // Limpia el texto de entrada
});

function processData(data) {
    if (data.length === 0) {
        showAlert('Por favor, ingresa datos válidos separados por comas o selecciona un archivo CSV con datos válidos.');
        return;
    }

    const orderType = document.getElementById('orderType').value;
    const selectedAlgorithms = Array.from(document.querySelectorAll('input[type="checkbox"]:checked:not(#selectAll)')).map(cb => cb.value);

    if (selectedAlgorithms.length === 0) {
        showAlert('Por favor, selecciona al menos un algoritmo de ordenamiento.');
        return;
    }

    const resultsContainer = document.getElementById('resultsContainer');
    resultsContainer.innerHTML = '';

    let tempResults = [];
    let completedRequests = 0;
    const progressBar = document.getElementById('progressBar');
    const loadingModal = new bootstrap.Modal(document.getElementById('loadingModal'));
    const loadingPercentage = document.getElementById('loadingPercentage');
    const loadingMessage = document.getElementById('loadingMessage');

    loadingModal.show();

    const timesData = [];

    selectedAlgorithms.forEach((algorithm, index) => {
        fetch('/sort-data/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({algorithm, data, orderType})
        })
        .then(response => response.json())
        .then(result => {
            const currentDate = new Date().toLocaleString();
            historial.push({
                algorithm: algorithm,
                dataCount: data.length,
                sorted_data: result.sorted_data,
                elapsedTime: result.elapsed_time,
                date: currentDate
            });

            tempResults.push({algorithm, result, index});
            tempResults.sort((a, b) => a.index - b.index);
            timesData.push({
                label: algorithm,
                time: result.elapsed_time
            });

            resultsContainer.innerHTML = '';
            let rowDiv = null;
            tempResults.forEach((tempResult, idx) => {
                if (idx % 2 === 0) {
                    rowDiv = document.createElement('div');
                    rowDiv.className = 'row mb-4';
                    resultsContainer.appendChild(rowDiv);
                }

                const colClass = (idx % 2 === 0 && selectedAlgorithms.length === idx + 1) ? 'col-12' : 'col-md-6';
                const colDiv = document.createElement('div');
                colDiv.className = `${colClass} mb-4`;
                colDiv.innerHTML = `
                    <div class="accordion accordion-custom" id="accordion-${tempResult.algorithm.replace(/\s+/g, '')}-${idx}">
                        <div class="accordion-item">
                            <h2 class="accordion-header" id="heading-${tempResult.algorithm.replace(/\s+/g, '')}-${idx}">
                                <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapse-${tempResult.algorithm.replace(/\s+/g, '')}-${idx}" aria-expanded="false" aria-controls="collapse-${tempResult.algorithm.replace(/\s+/g, '')}-${idx}">
                                    ${tempResult.algorithm}
                                </button>
                            </h2>
                            <div id="collapse-${tempResult.algorithm.replace(/\s+/g, '')}-${idx}" class="accordion-collapse collapse" aria-labelledby="heading-${tempResult.algorithm.replace(/\s+/g, '')}-${idx}" data-bs-parent="#accordion-${tempResult.algorithm.replace(/\s+/g, '')}-${idx}">
                                <div class="accordion-body">
                                    <table class="table table-dark table-hover">
                                        <thead>
                                            <tr>
                                                <th>#</th>
                                                <th>Dato Original</th>
                                                <th>Dato Ordenado</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            ${tempResult.result.sorted_data.map((item, i) => `
                                                <tr>
                                                    <td>${i + 1}</td>
                                                    <td>${data[i]}</td>
                                                    <td>${item}</td>
                                                </tr>
                                            `).join('')}
                                        </tbody>
                                    </table>
                                    <p class="text-center text-white">Tiempo de ${tempResult.algorithm}: <span>${tempResult.result.elapsed_time} ms</span></p>
                                    <p class="text-center text-white">Número de Datos: ${data.length}</p>
                                    <button class="btn btn-success mt-3" onclick="downloadCSV('${algorithm}', ${JSON.stringify(result.sorted_data)})">Descargar CSV</button>
                                </div>
                            </div>
                        </div>
                    </div>
                `;
                rowDiv.appendChild(colDiv);
            });

            completedRequests++;
            const progressPercentage = (completedRequests / selectedAlgorithms.length) * 100;
            progressBar.style.width = `${progressPercentage}%`;
            loadingPercentage.textContent = `${progressPercentage.toFixed(1)}% completado`;

            if (completedRequests === selectedAlgorithms.length) {
                loadingPercentage.textContent = 'Proceso finalizado con éxito';
                setTimeout(() => loadingModal.hide(), 2000);
                renderChart(timesData);
            }
        });

    });
}

function renderChart(timesData) {
    const ctx = document.getElementById('sortingChart').getContext('2d');

    const chart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: timesData.map(item => item.label),
            datasets: [{
                label: 'Tiempo de ejecución (ms)',
                data: timesData.map(item => item.time),
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

function downloadCSV(algorithm, sortedData) {
    const csvContent = "data:text/csv;charset=utf-8," + sortedData.join('\n');
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement('a');
    link.setAttribute('href', encodedUri);
    link.setAttribute('download', `${algorithm}_ordenado.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}
document.getElementById('descargarBtn').addEventListener('click', function () {
    const resultados = document.querySelectorAll('.accordion-body tbody tr');
    if (resultados.length === 0) {
        showAlert('No hay datos ordenados para descargar.');
        return;
    }

    let csvContent = '';
    let currentAlgorithm = '';

    resultados.forEach(row => {
        const cells = row.querySelectorAll('td');
        const algoritmo = row.closest('.accordion-item').querySelector('.accordion-button').textContent.trim();
        
        if (algoritmo !== currentAlgorithm) {
            csvContent += `\n${algoritmo}\n`;
            csvContent += 'Dato Original,Dato Ordenado\n';
            currentAlgorithm = algoritmo;
        }

        const datoOriginal = cells[1].textContent;
        const datoOrdenado = cells[2].textContent;
        csvContent += `${datoOriginal},${datoOrdenado}\n`;
    });

    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const downloadLink = document.createElement('a');
    downloadLink.href = url;
    downloadLink.download = `resultados_ordenados_${new Date().toLocaleDateString()}.csv`;

    document.body.appendChild(downloadLink);
    downloadLink.click();
    document.body.removeChild(downloadLink);
});


function showAlert(message) {
    const alertModal = new bootstrap.Modal(document.getElementById('alertModal'));
    document.getElementById('alertModalBody').innerText = message;
    alertModal.show();
}


function applyFilter(filter) {
    const dataInputText = document.getElementById('dataInputText').value.trim();
    if (!dataInputText) {
        showAlert('Por favor, ingresa datos para filtrar.');
        return;
    }

    let data = dataInputText.split(',').map(item => parseFloat(item.trim())).filter(item => !isNaN(item));

    switch (filter) {
        case 'prime':
            data = data.filter(isPrime);
            break;
        case 'fibonacci':
            data = data.filter(isFibonacci);
            break;
        case 'factorial':
            data = data.filter(isFactorial);
            break;
        // Añade más filtros aquí según sea necesario
    }

    if (data.length === 0) {
        showAlert('No se encontraron datos que cumplan con el filtro seleccionado.');
    }

    document.getElementById('dataInputText').value = data.join(', '); // Actualiza el input con los datos filtrados
}

function isPrime(num) {
    if (num <= 1) return false;
    for (let i = 2; i <= Math.sqrt(num); i++) {
        if (num % i === 0) return false;
    }
    return true;
}

function isFibonacci(num) {
    const isPerfectSquare = (x) => {
        const s = Math.sqrt(x);
        return Math.floor(s) * Math.floor(s) === x;
    };
    return isPerfectSquare(5 * num * num + 4) || isPerfectSquare(5 * num * num - 4);
}

function isFactorial(num) {
    if (num < 1 || !Number.isInteger(num)) return false;
    let i = 1;
    while (true) {
        if (num % i !== 0) return false;
        num /= i;
        if (num === 1) return true;
        i++;
    }
}document.getElementById('searchButton').addEventListener('click', function () {
    const searchQuery = document.getElementById('searchInput').value.trim();
    const searchType = document.getElementById('searchType').value;

    if (!searchQuery) {
        showAlert('Por favor, ingresa un dato para buscar.');
        return;
    }

    if (searchType === 'Tipo de Busqueda') {
        showAlert('Por favor, selecciona un tipo de búsqueda.');
        return;
    }

    const resultsContainer = document.getElementById('searchResults');
    resultsContainer.innerHTML = '';

    const datos = historial.flatMap(entry => entry.sorted_data);

    fetch('/buscar-datos/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({algoritmo: searchType, buscar: searchQuery, datos: datos})
    })
    .then(response => response.json())
    .then(result => {
        if (result.error) {
            showAlert(result.error);
            return;
        }

        // Asignar los resultados de búsqueda y el algoritmo de ordenamiento usado
        let searchResults = result.resultados.map(idx => {
            const entryIndex = Math.floor(idx / historial[0].sorted_data.length);
            return {
                entryIndex: entryIndex,
                itemIndex: idx % historial[0].sorted_data.length,
                data: datos[idx],
                algorithm: historial[entryIndex].algorithm, // Algoritmo usado para ordenar
                date: historial[entryIndex].date
            };
        });

        if (searchResults.length === 0) {
            showAlert('Dato no encontrado.');
            return;
        }

        searchResults.forEach((result, index) => {
            const resultRow = document.createElement('tr');
            resultRow.innerHTML = `
                <td>${index + 1}</td>
                <td>${result.itemIndex + 1}</td>
                <td>${result.data}</td>
                <td>${result.algorithm}</td> <!-- Algoritmo de ordenamiento -->
                <td>${result.date}</td>
            `;
            resultRow.addEventListener('click', function () {
                const targetAccordion = document.getElementById(`collapse-${result.algorithm.replace(/\s+/g, '')}-${result.entryIndex}`);
                if (targetAccordion) {
                    const accordionParent = new bootstrap.Collapse(targetAccordion, {
                        toggle: true
                    });
                    targetAccordion.scrollIntoView({ behavior: 'smooth' });

                    const tableRows = targetAccordion.querySelectorAll('tbody tr');
                    tableRows.forEach(row => {
                        row.classList.remove('highlight');
                    });
                    tableRows[result.itemIndex].classList.add('highlight');
                }
            });
            resultsContainer.appendChild(resultRow);
        });
    })
    .catch(error => {
        console.error('Error:', error);
        showAlert('Ocurrió un error durante la búsqueda.');
    });
});

function showAlert(message) {
    const alertModal = new bootstrap.Modal(document.getElementById('alertModal'));
    document.getElementById('alertModalBody').innerText = message;
    alertModal.show();
}



const style = document.createElement('style');
style.innerHTML = `
    .highlight {
        background-color: yellow;
    }
`;
document.head.appendChild(style);


        document.getElementById('historialModal').addEventListener('show.bs.modal', function () {
            const historialResumen = document.getElementById('historialResumen');
        
            historialResumen.innerHTML = '';
        
            const resumen = {};
            historial.forEach(entry => {
                if (!resumen[entry.algorithm]) {
                    resumen[entry.algorithm] = { count: 0, dataCount: 0 };
                }
                resumen[entry.algorithm].count += 1;
                resumen[entry.algorithm].dataCount += entry.dataCount;
            });
        
            for (const [algorithm, data] of Object.entries(resumen)) {
                historialResumen.innerHTML += `
                    <tr>
                        <td>${algorithm}</td>
                        <td>${data.count}</td>
                        <td>${data.dataCount}</td>
                    </tr>
                `;
            }
        });
        
        document.getElementById('detallesModal').addEventListener('show.bs.modal', function () {
            const historialDetalles = document.getElementById('historialDetalles');
        
            historialDetalles.innerHTML = '';
        
            historial.forEach((entry, index) => {
                historialDetalles.innerHTML += `
                    <tr>
                        <td>${index + 1}</td>
                        <td>${entry.algorithm}</td>
                        <td>${entry.dataCount}</td>
                        <td>${entry.elapsedTime}</td>
                        <td>${entry.date}</td>
                    </tr>
                `;
            });
        });
        
        document.getElementById('randomData').addEventListener('change', function () {
            const dataCountInput = document.getElementById('dataCount');
            dataCountInput.disabled = !this.checked;
        });
        
        document.getElementById('generateRandomData').addEventListener('click', function () {
            const startRange = parseInt(document.getElementById('startRange').value);
            const endRange = parseInt(document.getElementById('endRange').value);
            const isRandom = document.getElementById('randomData').checked;
            const dataCount = parseInt(document.getElementById('dataCount').value);
        
            if (isNaN(startRange) || isNaN(endRange)) {
                showAlert('Por favor, ingresa valores válidos para el rango inicial y final.');
                return;
            
                        
                fetch('/generate-random-data/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrftoken
                    },
                    body: JSON.stringify({ startRange, endRange, dataCount })
                })
                .then(response => response.json())
                .then(result => {
                    document.getElementById('dataInputText').value = result.data.join(', ');
                })
                .catch(error => console.error('Error:', error));
            } else {
                // Generar datos ordenados localmente
                if (startRange > endRange) {
                    showAlert('El rango inicial no puede ser mayor que el rango final.');
                    return;
                }
        
                let orderedData = [];
                for (let i = startRange; i <= endRange; i++) {
                    orderedData.push(i);
                }
        
                document.getElementById('dataInputText').value = orderedData.join(', ');
            }
        });
        

        
        document.getElementById('dataInputFile').addEventListener('change', function (event) {
            const file = event.target.files[0];
            if (!file) return;
        
            const formData = new FormData();
            formData.append('file', file);
        
            fetch('/read-data/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken
                },
                body: formData
            })
            .then(response => response.json())
            .then(result => {
                document.getElementById('dataInputText').value = result.data.join(', ');
            })
            .catch(error => console.error('Error:', error));
        });
        
        document.getElementById('selectAll').addEventListener('change', function () {
            const checkboxContainer = document.querySelector('.checkbox-container');
            const checkboxes = checkboxContainer.querySelectorAll('input[type="checkbox"]:not(#selectAll)');
            checkboxes.forEach(cb => cb.checked = this.checked);
        });
        
        
        document.getElementById('clearButton').addEventListener('click', function () { 
            document.getElementById('dataInputText').value = '';
        });
        
        
        document.getElementById('verGraficaBtn').addEventListener('click', function () {
            const selectedAlgorithms = Array.from(document.querySelectorAll('input[type="checkbox"]:checked:not(#selectAll)')).map(cb => cb.value);
            
            if (selectedAlgorithms.length === 0) {
                showAlert('Por favor, selecciona al menos un algoritmo de ordenamiento.');
                return;
            }
            
        
            const tiempos = selectedAlgorithms.map(algorithm => {
                return historial.filter(entry => entry.algorithm === algorithm).map(entry => entry.elapsedTime);
            });
        
            fetch('/grafica/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken
                },
                body: JSON.stringify({algoritmos: selectedAlgorithms, tiempos: tiempos})
            })
            .then(response => response.json())
            .then(data => {
                const image = new Image();
                image.src = `data:image/png;base64,${data.image_base64}`;
                document.getElementById('graficaContainer').innerHTML = '';
                document.getElementById('graficaContainer').appendChild(image);
            })
            .catch(error => console.error('Error:', error));
        });

document.getElementById('saveChangesBtn').addEventListener('click', function () {
    showAlert('Cambios guardados exitosamente.', 'success');


    const modal = bootstrap.Modal.getInstance(document.getElementById('filtersModal'));
    modal.hide();
});


document.getElementById('descargarBtn').addEventListener('click', function () {
    const tempResults = Array.from(document.querySelectorAll('.accordion .accordion-item')).map(item => {
        const algorithm = item.querySelector('.accordion-button').textContent.trim();
        const rows = item.querySelectorAll('tbody tr');
        const data = Array.from(rows).map(row => {
            const columns = row.querySelectorAll('td');
            return columns.length > 0 ? columns[2].innerText : null;
        }).filter(item => item !== null);

        return { algorithm, data };
    });

    const datosOrdenadosPorAlgoritmo = {};
    tempResults.forEach(result => {
        const tiempo = document.querySelector(`#collapse-${result.algorithm.replace(/\s+/g, '')} .accordion-body p span`).textContent.trim();
        datosOrdenadosPorAlgoritmo[result.algorithm] = { datos: result.data, tiempo: tiempo };
    });

    fetch('/descargar/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({ datos_ordenados_por_algoritmo: datosOrdenadosPorAlgoritmo })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.blob();
    })
    .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        a.download = 'datos_ordenados.pdf';
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
    })
    .catch(error => console.error('Error:', error));
});
document.addEventListener('DOMContentLoaded', function () {
    const radioButtons = document.querySelectorAll('input[name="sortFilter"]');
    let lastSelected = null;

    radioButtons.forEach(radio => {
        radio.addEventListener('click', function () {
            if (lastSelected === this) {
                this.checked = false;
                lastSelected = null;
            } else {
                lastSelected = this;
            }
        });
    });
}); 

