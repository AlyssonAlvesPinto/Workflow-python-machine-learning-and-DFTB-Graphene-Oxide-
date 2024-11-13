import os
import subprocess
import time
import multiprocessing

def executar_calculo(pasta_principal, subpasta):
    pasta_completa = os.path.join(pasta_principal, subpasta)
    os.chdir(pasta_completa)
    subprocess.run(["sbatch", "job"])
    os.chdir("../..")  # Voltar dois níveis acima (para a pasta principal)
    print(f"Cálculo submetido para {pasta_completa}")

def main():
    pastas_principais = [str(i) for i in range(5, 10, 5)]
    subpastas = [str(i) for i in range(1, 6)]

    with multiprocessing.Pool(processes=3) as pool:  # Limite de 5 processos paralelos
        for pasta_principal in pastas_principais:
            for subpasta in subpastas:
                pool.apply_async(executar_calculo, args=(pasta_principal, subpasta))

        pool.close()
        pool.join()

    print("Todos os cálculos foram submetidos.")

if __name__ == "__main__":
    main()
