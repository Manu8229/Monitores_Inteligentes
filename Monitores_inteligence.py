import random
import time
import csv
import matplotlib.pyplot as plt
from itertools import count

def gerar_leituras(num_leituras):
    """ Gera leituras fictícias de sensores """
    leituras = []
    for i in range(num_leituras):
        id_maquina = f"MAQ{i+1}"
        temperatura = round(random.uniform(50, 100), 2)
        vibracao = round(random.uniform(5, 15), 2)
        leitura = {
            "ID da máquina": id_maquina,
            "Temperatura (°C)": temperatura,
            "Vibração (mm/s)": vibracao
        }
        leituras.append(leitura)
    return leituras

def verificar_anomalias(leituras):
    """ Verifica anomalias nas leituras dos sensores """
    alertas = []
    for leitura in leituras:
        if leitura["Temperatura (°C)"] > 80:
            alertas.append((leitura["ID da máquina"], "Temperatura", leitura["Temperatura (°C)"]))
        if leitura["Vibração (mm/s)"] > 10:
            alertas.append((leitura["ID da máquina"], "Vibração", leitura["Vibração (mm/s)"]))
    return alertas

def gerar_relatorio(leituras, alertas):
    """ Gera um relatório resumido com estatísticas das leituras """
    total_leituras = len(leituras)
    total_alertas = len(alertas)
    
    temperatura_media = sum(leitura["Temperatura (°C)"] for leitura in leituras) / total_leituras
    vibracao_media = sum(leitura["Vibração (mm/s)"] for leitura in leituras) / total_leituras
    
    print("\n--- Relatório Resumido ---")
    print(f"Temperatura média: {temperatura_media:.2f} °C")
    print(f"Vibração média: {vibracao_media:.2f} mm/s")
    print(f"Total de alertas gerados: {total_alertas}")

def salvar_dados_csv(leituras, timestamp):
    """ Salva os dados em um arquivo CSV """
    try:
        with open("dados_sensores.csv", mode="a+", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["Timestamp", "ID da máquina", "Temperatura (°C)", "Vibração (mm/s)"])
            if file.tell() == 0:
                writer.writeheader()
            for leitura in leituras:
                writer.writerow({"Timestamp": timestamp, **leitura})
        print("\nDados salvos no arquivo 'dados_sensores.csv'.")
    except PermissionError:
        print("Erro: O arquivo 'dados_sensores.csv' está aberto em outro programa. Feche-o e tente novamente.")

def exibir_dashboard(leituras):
    """ Exibe gráficos de temperatura e vibração com alertas destacados """
    ids = [leitura["ID da máquina"] for leitura in leituras]
    temperaturas = [leitura["Temperatura (°C)"] for leitura in leituras]
    vibracoes = [leitura["Vibração (mm/s)"] for leitura in leituras]
    
    cores_temp = ['red' if temp > 80 else 'blue' for temp in temperaturas]
    cores_vib = ['red' if vib > 10 else 'green' for vib in vibracoes]

    plt.clf()
    fig, ax = plt.subplots(2, 1, figsize=(10, 8))
    
    ax[0].bar(ids, temperaturas, color=cores_temp)
    ax[0].axhline(y=80, color='red', linestyle='--', label='Limite de Temperatura')
    ax[0].set_title('Temperatura das Máquinas')
    ax[0].set_ylabel('Temperatura (°C)')
    ax[0].legend()
    
    ax[1].bar(ids, vibracoes, color=cores_vib)
    ax[1].axhline(y=10, color='red', linestyle='--', label='Limite de Vibração')
    ax[1].set_title('Vibração das Máquinas')
    ax[1].set_ylabel('Vibração (mm/s)')
    ax[1].legend()
    
    plt.tight_layout()
    plt.pause(1)

def main():
    """ Loop principal para simulação contínua a cada 1 minuto """
    plt.ion()  # Modo interativo do Matplotlib
    contador = count(start=1)
    
    while True:
        timestamp = f"Leitura {next(contador)}"
        print(f"\n{timestamp}: Gerando novas leituras...")
        
        leituras_sensores = gerar_leituras(10)
        alertas = verificar_anomalias(leituras_sensores)
        
        print("\nAlertas de anomalias:")
        for alerta in alertas:
            print(f"ALERTA: Máquina {alerta[0]} com {alerta[1]} crítica de {alerta[2]}")
        
        gerar_relatorio(leituras_sensores, alertas)
        salvar_dados_csv(leituras_sensores, timestamp)
        exibir_dashboard(leituras_sensores)
        
        time.sleep(60)  # Aguarda 1 minuto antes de gerar novas leituras

if __name__ == "__main__":
    main()
