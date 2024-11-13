import os
import numpy as np
from ase.io import read, write
from ase.optimize import BFGS
##from ase.optimize import FIRE 
from ase.constraints import ExpCellFilter
from mace.calculators import mace_off
from mpi4py import MPI
from ase.optimize.precon import PreconLBFGS

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

def run_ml_calculation(folder, sub_folder):
    os.chdir(os.path.join(folder, sub_folder))  # Mudar para a subpasta correspondente

    # macemp = mace_mp(model="large", device='cuda', default_dtype='float64', dispersion=True)
    maceoff = mace_off(model="medium", device='cpu', default_dtype='float32', dispersion=True)

    atoms = read('go.vasp', index='-1')  # Ler a estrutura do arquivo go.vasp usando ASE
    atoms.center(axis=2)  # Centralizar na direção do eixo z

    atoms.calc = maceoff # Configurar mace como calculadora para este objeto de átomos

    ucf = ExpCellFilter(atoms, hydrostatic_strain=True)  # Configurar filtro de célula unitária para relaxar apenas nas direções xx, yy, zz

    dyn = PreconLBFGS(ucf, trajectory='go.traj',   precon='Exp')  ###  BFGS     # Configurar otimizador para relaxamento da estrutura
    dyn.run(fmax=0.01)  # Executar relaxamento até que a força máxima seja menor que 10 meV/Ang

    dyn.atoms.atoms.write('go.vasp')  # Escrever geometria relaxada no arquivo

    os.chdir('../../..')  # Voltar ao diretório original

def main():
    parent_folders = [str(i) for i in range(20, 36, 5)]  # Lista com as pastas pai
    sub_folders = [f"{j}" for j in range(1, 11)]  # Lista das subpastas

    tasks = [(folder, sub_folder) for folder in parent_folders for sub_folder in sub_folders]

    # Distribuir tarefas entre os processos MPI
    for i in range(rank, len(tasks), size):
        folder, sub_folder = tasks[i]
        run_ml_calculation(folder, sub_folder)

if __name__ == "__main__":
    main()
