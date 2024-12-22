import csv
from django.http import HttpResponse

def generar_csv(datos_originales, datos_ordenados, algoritmo):
    """
    Genera y descarga un archivo CSV con los datos originales, ordenados y el algoritmo usado.

    Args:
        datos_originales (list): Lista de datos originales.
        datos_ordenados (list): Lista de datos ordenados.
        algoritmo (str): Nombre del algoritmo de ordenamiento usado.

    Returns:
        HttpResponse: Respuesta HTTP con el archivo CSV.
    """

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{algoritmo}_resultado.csv"'

    writer = csv.writer(response)
    writer.writerow(['Algoritmo', 'Datos Originales', 'Datos Ordenados'])
    writer.writerow([algoritmo, ', '.join(map(str, datos_originales)), ', '.join(map(str, datos_ordenados))])

    return response
