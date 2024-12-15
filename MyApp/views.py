from django.shortcuts import render
from django.http import JsonResponse
import json
import time
from .algoritmos_Ordenamiento import read_data_from_file, generate_random_data, bubble_sort, quick_sort, insertion_sort, cocktail_sort, bucket_sort, counting_sort, merge_sort, binary_tree_sort, radix_sort, shell_sort, comb_sort, heap_sort, selection_sort, gnome_sort
from .grafica import generar_grafica
from .descargar import descargar_pdf
from .filtros import aplicar_filtro

def home(request):
    return render(request, 'MyApp/index.html')

def about(request):
    return render(request, 'MyApp/about.html')

def intereses(request):
    return render(request, 'MyApp/intereses.html')

def blog(request):
    return render(request, 'MyApp/blog.html')

def ejercicios(request):
    return render(request, 'MyApp/ejercicios.html')

def sort_data(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        algorithm = data.get('algorithm')
        data_list = data.get('data', [])
        order_type = data.get('orderType')

        start_time = time.time()

        if algorithm == 'Bubble Sort':
            sorted_data = bubble_sort(data_list, order_type)
        elif algorithm == 'Quick Sort':
            sorted_data = quick_sort(data_list, order_type)
        elif algorithm == 'Insertion Sort':
            sorted_data = insertion_sort(data_list, order_type)
        elif algorithm == 'Cocktail Sort':
            sorted_data = cocktail_sort(data_list, order_type)
        elif algorithm == 'Bucket Sort':
            sorted_data = bucket_sort(data_list, order_type)
        elif algorithm == 'Counting Sort':
            sorted_data = counting_sort(data_list, order_type)
        elif algorithm == 'Merge Sort':
            sorted_data = merge_sort(data_list, order_type)
        elif algorithm == 'Binary Tree Sort':
            sorted_data = binary_tree_sort(data_list, order_type)
        elif algorithm == 'Radix Sort':
            sorted_data = radix_sort(data_list, order_type)
        elif algorithm == 'Shell Sort':
            sorted_data = shell_sort(data_list, order_type)
        elif algorithm == 'Comb Sort':
            sorted_data = comb_sort(data_list, order_type)
        elif algorithm == 'Heap Sort':
            sorted_data = heap_sort(data_list, order_type)
        elif algorithm == 'Selection Sort':
            sorted_data = selection_sort(data_list, order_type)
        elif algorithm == 'Gnome Sort':
            sorted_data = gnome_sort(data_list, order_type)
        else:
            return JsonResponse({'error': 'Algoritmo no reconocido'}, status=400)

        end_time = time.time()
        elapsed_time = round((end_time - start_time) * 1000, 2)  # en milisegundos

        return JsonResponse({
            'sorted_data': sorted_data,
            'elapsed_time': elapsed_time
        })
    return JsonResponse({'error': 'Método de solicitud no válido'}, status=400)

def generate_random_data_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        start_range = data.get('startRange')
        end_range = data.get('endRange')
        data_count = data.get('dataCount')

        random_data = generate_random_data(start_range, end_range, data_count)
        return JsonResponse({'data': random_data})
    return JsonResponse({'error': 'Método de solicitud no válido'}, status=400)

def read_data_view(request):
    if request.method == 'POST':
        file = request.FILES['file']
        data = read_data_from_file(file)
        return JsonResponse({'data': data})
    return JsonResponse({'error': 'Método de solicitud no válido'}, status=400)

def grafica_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        algoritmos = data.get('algoritmos')
        tiempos = data.get('tiempos')

        image_base64 = generar_grafica(algoritmos, tiempos)
        
        return JsonResponse({'image_base64': image_base64})
    return JsonResponse({'error': 'Método de solicitud no válido'}, status=400)

def descargar_view(request):
    return descargar_pdf(request)

def filtros_view(request):
    return aplicar_filtro(request)

