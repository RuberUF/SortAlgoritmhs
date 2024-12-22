def busqueda_lineal(arr, x):
    x = int(x)
    arr = list(map(int, arr)) 
    resultados = []
    for i, item in enumerate(arr):
        if item == x:
            resultados.append(i)
    return resultados

def busqueda_binaria(arr, x):
    x = int(x)
    arr = list(map(int, arr))
    arr.sort()
    resultados = []
    izquierda, derecha = 0, len(arr) - 1
    while izquierda <= derecha:
        medio = (izquierda + derecha) // 2
        if arr[medio] == x:
            i = medio
            while i >= 0 and arr[i] == x:
                resultados.append(i)
                i -= 1
            i = medio + 1
            while i < len(arr) and arr[i] == x:
                resultados.append(i)
                i += 1
            break
        elif arr[medio] < x:
            izquierda = medio + 1
        else:
            derecha = medio - 1
    return resultados

def busqueda_exponencial(arr, x):
    x = int(x)
    arr = list(map(int, arr))  
    if arr[0] == x:
        return [0]
    i = 1
    while i < len(arr) and arr[i] <= x:
        i *= 2
    return busqueda_binaria(arr[:min(i, len(arr))], x)

def busqueda_fibonacci(arr, x):
    x = int(x)
    arr = list(map(int, arr)) 
    arr.sort()
    n = len(arr)
    fibMMm2 = 0
    fibMMm1 = 1
    fibM = fibMMm2 + fibMMm1
    while fibM < n:
        fibMMm2 = fibMMm1
        fibMMm1 = fibM
        fibM = fibMMm2 + fibMMm1
    offset = -1
    resultados = []
    while fibM > 1:
        i = min(offset + fibMMm2, n - 1)
        if arr[i] < x:
            fibM = fibMMm1
            fibMMm1 = fibMMm2
            fibMMm2 = fibM - fibMMm1
            offset = i
        elif arr[i] > x:
            fibM = fibMMm2
            fibMMm1 = fibMMm1 - fibMMm2
            fibMMm2 = fibM - fibMMm1
        else:
            while i >= 0 and arr[i] == x:
                resultados.append(i)
                i -= 1
            i = i + 2
            while i < len(arr) and arr[i] == x:
                resultados.append(i)
                i += 1
            return resultados
    if fibMMm1 and arr[offset + 1] == x:
        resultados.append(offset + 1)
    return resultados

def busqueda_interpolacion(arr, x):
    x = int(x)
    arr = list(map(int, arr)) 
    arr.sort()
    n = len(arr)
    low = 0
    high = n - 1
    resultados = []
    while low <= high and x >= arr[low] and x <= arr[high]:
        if low == high:
            if arr[low] == x:
                resultados.append(low)
            return resultados
        pos = low + ((high - low) * (x - arr[low]) // (arr[high] - arr[low]))
        pos = int(pos)
        if arr[pos] == x:
            i = pos
            while i >= 0 and arr[i] == x:
                resultados.append(i)
                i -= 1
            i = pos + 1
            while i < len(arr) and arr[i] == x:
                resultados.append(i)
                i += 1
            return resultados
        if arr[pos] < x:
            low = pos + 1
        else:
            high = pos - 1
    return resultados

def ejecutar_busqueda(algoritmo, arr, x):
    if algoritmo == 'Lineal':
        return busqueda_lineal(arr, x)
    elif algoritmo == 'Binaria':
        return busqueda_binaria(arr, x)
    elif algoritmo == 'Exponencial':
        return busqueda_exponencial(arr, x)
    elif algoritmo == 'Fibonacci':
        return busqueda_fibonacci(arr, x)
    elif algoritmo == 'Interpolación':
        return busqueda_interpolacion(arr, x)
    else:
        raise ValueError("Algoritmo de búsqueda no reconocido")
