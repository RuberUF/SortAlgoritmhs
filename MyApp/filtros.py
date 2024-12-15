from django.http import JsonResponse
import json

def es_primo(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def es_fibonacci(n):
    def is_perfect_square(x):
        s = int(x**0.5)
        return s * s == x

    return is_perfect_square(5 * n * n + 4) or is_perfect_square(5 * n * n - 4)

def es_factorial(n):
    if n == 0 or n == 1:
        return True
    fact = 1
    i = 1
    while fact < n:
        i += 1
        fact *= i
    return fact == n

def filtrar_datos(data, filtro):
    if filtro == 'prime':
        return [x for x in data if es_primo(x)]
    elif filtro == 'fibonacci':
        return [x for x in data if es_fibonacci(x)]
    elif filtro == 'factorial':
        return [x for x in data if es_factorial(x)]
    return data

def aplicar_filtro(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        original_data = data.get('original_data', [])
        filtro = data.get('filtro', '')

        if not original_data or not filtro:
            return JsonResponse({'error': 'Datos o filtro no proporcionados'}, status=400)

        filtered_data = filtrar_datos(original_data, filtro)
        return JsonResponse({'filtered_data': filtered_data})
    return JsonResponse({'error': 'Método de solicitud no válido'}, status=400)
