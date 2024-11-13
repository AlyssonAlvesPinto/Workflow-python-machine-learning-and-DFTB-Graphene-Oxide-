import os
from pymatgen.analysis.graphs import StructureGraph
from pymatgen.analysis.local_env import JmolNN
from pymatgen.core import Structure

def process_subfolders(parent_folder):
    parent_folder = os.path.abspath(parent_folder)  # Caminho absoluto para a pasta pai

    for folder_number in range(0, 61, 5):  # Loop sobre as pastas pai
        parent_path = os.path.join(parent_folder, str(folder_number))

        for subfolder_number in range(1, 6):  # Loop sobre as subpastas
            subfolder_path = os.path.join(parent_path, f"{subfolder_number}")

            if not os.path.exists(subfolder_path):  # Verifica se a subpasta existe
                print(f"Erro: Subpasta {subfolder_path} não encontrada.")
                continue

            # Muda para a subpasta atual
            os.chdir(subfolder_path)

            for k in range(2):
                if k == 0:
                    ion1 = 'O'
                    ion2 = 'C'
                elif k == 1:
                    ion1 = 'H'
                    ion2 = 'O'

                # Verifica se o arquivo VASP existe na subpasta
                file_path = os.path.join(subfolder_path, 'go.vasp')
                if not os.path.exists(file_path):
                    print(f"Erro: Arquivo go.vasp não encontrado em {subfolder_path}.")
                    continue

                # Carrega a estrutura VASP
                structure = Structure.from_file(file_path)

                # Filtra os átomos de oxigênio na estrutura
                ion_indices = [i for i, site in enumerate(structure) if site.specie.name == ion1]

                # Cria o grafo da estrutura com base na estratégia JmolNN
                sg = StructureGraph.with_local_env_strategy(structure, JmolNN())

                # Lista para armazenar os índices dos sítios de oxigênio a serem removidos
                indices_to_remove = []

                # Loop sobre os índices dos átomos de oxigênio na estrutura
                for i in ion_indices:
                    # Obtém a coordenação do sítio
                    coordination = len(sg.get_connected_sites(i))

                    # Verifica a coordenação do sítio
                    if coordination == 0:
                        indices_to_remove.append(i)

                    elif coordination == 1:
                        # Verifica se o sítio está conectado a um átomo de carbono
                        connected_sites = sg.get_connected_sites(i)
                        connected_elements = [connected_site.site.specie.name for connected_site in connected_sites]
                        if ion2 not in connected_elements:
                            indices_to_remove.append(i)

                    elif coordination == 2:
                        connected_sites = sg.get_connected_sites(i)
                        connected_elements = [connected_site.site.specie.name for connected_site in connected_sites]
                        if ion2 not in connected_elements:
                            indices_to_remove.append(i)

                structure.remove_sites(indices_to_remove)

                # Salva a estrutura final no formato VASP
                structure.to(filename="go.vasp", fmt="poscar")

                # Volta para a pasta principal
                os.chdir(parent_folder)

def main():
    process_subfolders("./")  # Chama a função principal com o diretório atual como pasta pai

if __name__ == "__main__":
    main()
