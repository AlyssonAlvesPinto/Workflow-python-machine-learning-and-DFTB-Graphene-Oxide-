#!/bin/bash
#SBATCH --partition=short
#SBATCH --job-name=multi_GO
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=80
#SBATCH --ntasks=80
##SBATCH --exclusive
export OMP_NUM_THREADS=$NP
#SBATCH -o %x.o%j
#SBATCH -e %x.e%j
module load dftbplus/23.1_xtb
ulimit -s unlimited

# Definir as pastas principais e subpastas
main_folders=(20) # 5 10  20 25 30
subfolders_range=$(seq 1 10)

# Função para executar o DFTB+ em cada subpasta
run_dftb_in_subfolder() {
    local folder=$1
    local subfolder=$2
    local job_name="${folder}_${subfolder}"

    # Entrar no diretório da subpasta e rodar o DFTB+
    cd ${folder}/${subfolder}
    echo "Executando DFTB+ para a pasta ${folder}/${subfolder}..."

    # Executar o DFTB+
    dftb+ | tee output

    # Voltar para o diretório anterior
    cd - > /dev/null
}

# Loop para percorrer as pastas e subpastas e rodar os jobs sequencialmente
for folder in "${main_folders[@]}"; do
    for subfolder in $subfolders_range; do
        # Executar o job no diretório correto
        run_dftb_in_subfolder $folder $subfolder
    done
done
