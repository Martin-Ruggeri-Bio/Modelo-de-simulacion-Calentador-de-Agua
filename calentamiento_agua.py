import matplotlib.pyplot as plt

def calcular_tiempo_calentamiento(masa_agua, calor_especifico, calor_por_segundo, temp_inicial, temp_final):
    tiempo_total = int((temp_final - temp_inicial) * masa_agua * calor_especifico / calor_por_segundo) + 1
    segundos = list(range(tiempo_total))
    return segundos


def calcular_temperatura_segundo_a_segundo(masa_agua, calor_especifico, calor_por_segundo, temp_inicial, segundos):
    # Lista para almacenar las temperaturas y los segundos
    temperaturas = []
    for segundo in segundos:
        temperatura = temp_inicial + (segundo * calor_por_segundo) / (masa_agua * calor_especifico)
        temperaturas.append(temperatura)
    return temperaturas


def calcular_calor_perdida_lista(temp_internas, espesor):
    k = 0.04  # Conductividad del poliestireno en W/(m·K)
    A = 0.0213  # Área del calentador en m²
    T_ext = 25  # Temperatura externa en °C
    T_ext_kelvin = T_ext + 273.15 # Convertir temperatura externa a kelvin
    calores_perdida = [] # Lista para almacenar los valores de calor de pérdida
    for temp_interna in temp_internas:
        T_int_kelvin = temp_interna + 273.15 # Convertir temperatura interna a kelvin
        Q = (k * A * (T_ext_kelvin - T_int_kelvin)) / espesor # Calcular la cantidad de calor de pérdida (negativa)
        calores_perdida.append(Q)
    return calores_perdida

def calcular_temperaturas_negativas(calores_perdida, masa_agua, calor_especifico):
    temperaturas_negativas = []
    for calor_perdida in calores_perdida:
        temperatura_negativa = calor_perdida / (masa_agua * calor_especifico)
        temperaturas_negativas.append(temperatura_negativa)
    return temperaturas_negativas


def calcular_diferencia_temperatura(temperaturas, temperaturas_negativas, segundos):    
    diferencias = []
    for segundo in segundos:
        diferencia = temperaturas[segundo] - temperaturas_negativas[segundo]
        diferencias.append(diferencia)
    return diferencias

def generar_y_guardar_graficar_temperatura(segundos, temperaturas, nombre, color):
    plt.figure(figsize=(10, 5))
    plt.plot(segundos, temperaturas, label=nombre, color=color)
    plt.xlabel('Tiempo (segundos)')
    plt.ylabel('Temperatura (°C)')
    plt.title(nombre)
    plt.savefig(nombre + '.png')
    plt.close()


def main():
    masa_agua = 1  # Masa del agua en kg
    calor_especifico = 4184  # Calor específico del agua en J/(kg·K)
    calor_por_segundo = 1000  # Calor por segundo en J/s
    temp_inicial = 20  # Temperatura inicial en °C
    temp_final = 100  # Temperatura final en °C
    segundos = calcular_tiempo_calentamiento(masa_agua, calor_especifico, calor_por_segundo, temp_inicial, temp_final)
    temperaturas = calcular_temperatura_segundo_a_segundo(masa_agua, calor_especifico, calor_por_segundo, temp_inicial, segundos)
    generar_y_guardar_graficar_temperatura(segundos, temperaturas, 'Temperatura interna sin perdida de calor', 'blue')
    for espesor in [0.001, 0.0005, 0.0003]:
        calores_perdida = calcular_calor_perdida_lista(temperaturas, espesor)
        temperaturas_negativas = calcular_temperaturas_negativas(calores_perdida, masa_agua, calor_especifico)
        diferencias = calcular_diferencia_temperatura(temperaturas, temperaturas_negativas, segundos)
        generar_y_guardar_graficar_temperatura(segundos, temperaturas_negativas, f'Descenso de la Temperatura por Calor de pérdida con espesor: {espesor}', 'red')
        generar_y_guardar_graficar_temperatura(segundos, diferencias, f'Temperatura interna con perdida de calor con espesor {espesor}', 'green')

if __name__ == '__main__':
    main()
