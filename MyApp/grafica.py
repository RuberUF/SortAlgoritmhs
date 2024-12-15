import matplotlib.pyplot as plt
import io
import base64
from django.http import JsonResponse

def obtener_complejidad(algoritmo):
    complejidades = {
        'Bubble Sort': ('O(n^2)', 'O(n)', 'O(n^2)'),
        'Quick Sort': ('O(n log n)', 'O(n log n)', 'O(n^2)'),
        'Insertion Sort': ('O(n^2)', 'O(n)', 'O(n^2)'),
        'Merge Sort': ('O(n log n)', 'O(n log n)', 'O(n log n)'),
        'Heap Sort': ('O(n log n)', 'O(n log n)', 'O(n log n)')
    }
    return complejidades.get(algoritmo, ('Desconocido', 'Desconocido', 'Desconocido'))

def generar_grafica(algoritmos, tiempos):
    plt.figure(figsize=(10, 6))
    
    for algoritmo, tiempo in zip(algoritmos, tiempos):
        n = range(1, len(tiempo) + 1)
        mejor_caso, caso_promedio, peor_caso = obtener_complejidad(algoritmo)
        plt.plot(n, tiempo, label=f'{algoritmo} - Mejor: {mejor_caso}, Promedio: {caso_promedio}, Peor: {peor_caso}')
    
    plt.xlabel('Número de Datos')
    plt.ylabel('Tiempo (ms)')
    plt.title('Complejidad Temporal de los Algoritmos de Ordenamiento')
    plt.legend()
    plt.grid(True)

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    image_base64 = base64.b64encode(image_png).decode('utf-8')
    
    return image_base64


def grafica_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        algoritmos = data.get('algoritmos')
        tiempos = data.get('tiempos')

        image_base64 = generar_grafica(algoritmos, tiempos)
        
        return JsonResponse({'image_base64': image_base64})
    return JsonResponse({'error': 'Método de solicitud no válido'}, status=400)
