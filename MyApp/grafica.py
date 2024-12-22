import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import io
import base64
from django.http import JsonResponse

sns.set(style="darkgrid")

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
    plt.figure(figsize=(14, 10))

    colores = sns.color_palette("husl", len(algoritmos))
    
    for idx, (algoritmo, tiempo) in enumerate(zip(algoritmos, tiempos)):
        n = np.arange(1, len(tiempo) + 1)
        mejor_caso, caso_promedio, peor_caso = obtener_complejidad(algoritmo)
        sns.lineplot(x=n, y=tiempo, marker='o', linestyle='-', markersize=6, label=f'{algoritmo}\nMejor: {mejor_caso}\nPromedio: {caso_promedio}\nPeor: {peor_caso}', color=colores[idx])

    # Configuración de los ejes
    plt.xlim(0, max(max(len(t) for t in tiempos), 10))
    plt.ylim(0, max(max(max(t) for t in tiempos), 10) + 10)
    
    # Añadir líneas y texto de referencia para O(n), O(n^2), O(n log n), etc.
    x_vals = np.linspace(0, max(len(t) for t in tiempos), 100)
    plt.plot(x_vals, x_vals, '--', label='O(n)', color='grey', alpha=0.6)
    plt.plot(x_vals, x_vals**2, '--', label='O(n^2)', color='grey', alpha=0.6)
    plt.plot(x_vals, x_vals * np.log2(x_vals + 1), '--', label='O(n log n)', color='grey', alpha=0.6)
    
    # Anotaciones para el mejor y peor caso global
    todos_tiempos = np.concatenate(tiempos)
    mejor_tiempo = min(todos_tiempos)
    peor_tiempo = max(todos_tiempos)

    plt.annotate(f'Mejor Caso: {mejor_tiempo} ms',
                 xy=(np.argmin(todos_tiempos) + 1, mejor_tiempo),
                 xytext=(np.argmin(todos_tiempos) + 1, mejor_tiempo + 10),
                 arrowprops=dict(facecolor='green', shrink=0.05),
                 fontsize=12, color='green')
    
    plt.annotate(f'Peor Caso: {peor_tiempo} ms',
                 xy=(np.argmax(todos_tiempos) + 1, peor_tiempo),
                 xytext=(np.argmax(todos_tiempos) + 1, peor_tiempo - 20),
                 arrowprops=dict(facecolor='red', shrink=0.05),
                 fontsize=12, color='red')

    plt.xlabel('Número de Datos', fontsize=14)
    plt.ylabel('Tiempo (ms)', fontsize=14)
    plt.title('Complejidad Temporal de los Algoritmos de Ordenamiento', fontsize=18, weight='bold')
    plt.legend(title="Algoritmo y Complejidad", title_fontsize='13', fontsize='11', loc='upper left', bbox_to_anchor=(1, 1))
    plt.grid(True, linestyle='--', alpha=0.7)

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
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
