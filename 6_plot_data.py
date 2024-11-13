import os
import subprocess
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def run_dp_dos_commands(folder):
    # Mudar para a pasta correspondente
    os.chdir(folder)

    # Executar os comandos dp_dos
    subprocess.run(["/opt/ohpc/pub/apps/dftb+/dftbplus-23.1_xtb_mpi/dftbplus-23.1/tools/dptools/bin/dp_dos", "band.out", "dos.dat"])
    subprocess.run(["/opt/ohpc/pub/apps/dftb+/dftbplus-23.1_xtb_mpi/dftbplus-23.1/tools/dptools/bin/dp_dos", "-w", "pdos.C.1.out", "pdos.C.1.dat"])
    subprocess.run(["/opt/ohpc/pub/apps/dftb+/dftbplus-23.1_xtb_mpi/dftbplus-23.1/tools/dptools/bin/dp_dos", "-w", "pdos.C.2.out", "pdos.C.2.dat"])
    subprocess.run(["/opt/ohpc/pub/apps/dftb+/dftbplus-23.1_xtb_mpi/dftbplus-23.1/tools/dptools/bin/dp_dos", "-w", "pdos.H.1.out", "pdos.H.1.dat"])
    subprocess.run(["/opt/ohpc/pub/apps/dftb+/dftbplus-23.1_xtb_mpi/dftbplus-23.1/tools/dptools/bin/dp_dos", "-w", "pdos.O.1.out", "pdos.O.1.dat"])
    subprocess.run(["/opt/ohpc/pub/apps/dftb+/dftbplus-23.1_xtb_mpi/dftbplus-23.1/tools/dptools/bin/dp_dos", "-w", "pdos.O.2.out", "pdos.O.2.dat"])

    # Voltar para o diretório original
    os.chdir("..")

def plot_dos_files(folders):
    sns.set(style="whitegrid")

    for folder in folders:
        # Ler os dados dos arquivos dos.dat e pdos*.dat
        dos_data = pd.read_csv(os.path.join(folder, "dos.dat"), delim_whitespace=True, comment="#", names=["Energy", "Density"])
        pdos_C1_data = pd.read_csv(os.path.join(folder, "pdos.C.1.dat"), delim_whitespace=True, comment="#", names=["Energy", "PDOS"])
        pdos_C2_data = pd.read_csv(os.path.join(folder, "pdos.C.2.dat"), delim_whitespace=True, comment="#", names=["Energy", "PDOS"])
        pdos_H1_data = pd.read_csv(os.path.join(folder, "pdos.H.1.dat"), delim_whitespace=True, comment="#", names=["Energy", "PDOS"])
        pdos_O1_data = pd.read_csv(os.path.join(folder, "pdos.O.1.dat"), delim_whitespace=True, comment="#", names=["Energy", "PDOS"])
        pdos_O2_data = pd.read_csv(os.path.join(folder, "pdos.O.2.dat"), delim_whitespace=True, comment="#", names=["Energy", "PDOS"])

        fermi_energy = read_fermi_level(folder)

        # Plotar os resultados
        plt.figure(figsize=(12, 6))

        plt.plot(dos_data["Energy"] - fermi_energy, dos_data["Density"], label="DOS / PDOS (arb. units)", linewidth=2)
        plt.plot(pdos_C1_data["Energy"] - fermi_energy, pdos_C1_data["PDOS"], label="C s PDOS")
        plt.plot(pdos_C2_data["Energy"] - fermi_energy, pdos_C2_data["PDOS"], label="C p PDOS")
        plt.plot(pdos_H1_data["Energy"] - fermi_energy, pdos_H1_data["PDOS"], label="H s PDOS")
        plt.plot(pdos_O1_data["Energy"] - fermi_energy, pdos_O1_data["PDOS"], label="O s PDOS")
        plt.plot(pdos_O2_data["Energy"] - fermi_energy, pdos_O2_data["PDOS"], label="O p PDOS")

        plt.title(f'Density of States and Projected DOS for {folder}')
        plt.xlabel('E - $E_f$ (eV)')
        plt.ylabel('DOS / PDOS (arb. units)')
        plt.xlim(-8, 8)
        plt.legend()

        # Salvar o gráfico em PDF e PNG
        plt.savefig(os.path.join(folder, "dos_plot.pdf"), format='pdf', dpi=600)
        plt.savefig(os.path.join(folder, "dos_plot.png"), format='png', dpi=600)
        plt.show()

def read_fermi_level(folder):
    # Ler o valor do nível de Fermi do arquivo detailed.out
    detailed_out_path = os.path.join(folder, "detailed.out")
    with open(detailed_out_path, 'r') as file:
        for line in file:
            if "Fermi level:" in line:
                fermi_energy = float(line.split()[-2])  # Pegar o penúltimo elemento da linha
                return fermi_energy

def main():
    # Pastas principais a serem acessadas
    main_folders = [str(i) for i in range(0, 65, 5)]

    for main_folder in main_folders:
        # Subpastas dentro de cada pasta principal
        sub_folders = [os.path.join(main_folder, str(i)) for i in range(1, 6)]

        # Executar comandos e plotar gráficos para cada subpasta
        for folder in sub_folders:
            run_dp_dos_commands(folder)
            plot_dos_files([folder])  # Passar uma lista com um único elemento

if __name__ == "__main__":
    main()
