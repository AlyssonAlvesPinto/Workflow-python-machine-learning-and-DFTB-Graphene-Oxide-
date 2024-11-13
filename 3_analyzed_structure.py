import os
from pymatgen.analysis.graphs import StructureGraph
from pymatgen.analysis.local_env import JmolNN
from pymatgen.core import Structure

def process_subfolders(parent_folder):
    parent_folder = os.path.abspath(parent_folder)  # Caminho absoluto para a pasta pai

    for folder_number in range(20, 21, 5):  # Loop sobre as pastas pai
        parent_path = os.path.join(parent_folder, str(folder_number))

        for subfolder_number in range(10, 11):  # Loop sobre as subpastas
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

                # Cria o grafo da estrutura com base na estratégia JmolNN
                sg = StructureGraph.with_local_env_strategy(structure, JmolNN())

                # Lista para armazenar os índices dos sítios de íons a serem removidos
                indices_to_remove = []

                for i, site in enumerate(structure):
                    if site.specie.name == ion1:
                        # Obtém os sites conectados
                        connected_sites = sg.get_connected_sites(i)

                        # Se não houver sites conectados, o átomo está isolado
                        if len(connected_sites) == 0:
                            indices_to_remove.append(i)
                        else:
                            # Verifica se o átomo está conectado a pelo menos um átomo esperado (ion2)
                            connected_elements = [connected_site.site.specie.name for connected_site in connected_sites]
                            if ion2 not in connected_elements:
                                indices_to_remove.append(i)

                # Remove os átomos desconectados da estrutura
                if indices_to_remove:
                    structure.remove_sites(indices_to_remove)
                    print(f"{len(indices_to_remove)} átomos de {ion1} removidos da subpasta {subfolder_path}.")
                else:
                    print(f"Nenhum átomo de {ion1} removido da subpasta {subfolder_path}.")

                # Salva a estrutura final no formato VASP
                structure.to(fmt="poscar", filename="go_cleaned.vasp")

            # Volta para o diretório pai
            os.chdir(parent_folder)

def main():
    process_subfolders("./")  # Chama a função principal com o diretório atual como pasta pai

if __name__ == "__main__":
    main()
