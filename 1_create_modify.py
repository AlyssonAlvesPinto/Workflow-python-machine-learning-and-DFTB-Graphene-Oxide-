import os
import shutil
import subprocess

def create_folders():
    parent_folders = [i for i in range(1, 31, 5)]  # Lista com as pastas pai
    for folder in parent_folders:
        folder_path = f"{folder}"
        os.makedirs(folder_path, exist_ok=True)
        for j in range(1, 11):  # Cria 11 subpastas dentro de cada pasta pai
            sub_folder = os.path.join(folder_path, f"{j}")
            os.makedirs(sub_folder, exist_ok=True)
            # Copia os arquivos para cada subpasta
            shutil.copy("GOBruno.py", sub_folder)
            shutil.copy("dftb_in.hsd", sub_folder)
            shutil.copy("job", sub_folder)

def execute_GOBruno(folder):
    sub_folders = [f"{j}" for j in range(1, 11)]  # Lista das subpastas
    for sub_folder in sub_folders:
        sub_folder_path = os.path.join(folder, sub_folder)
        # Modifica o arquivo GOBruno.py
        script_file = os.path.join(sub_folder_path, "GOBruno.py")
        with open(script_file, "r") as f:
            script_content = f.read()
        script_content = script_content.replace("12.5", str(os.path.basename(folder)))
        with open(script_file, "w") as f:
            f.write(script_content)

        # Modifica o arquivo job
        job_file = os.path.join(sub_folder_path, "job")
        with open(job_file, "r") as f:
            job_content = f.read()
        job_content = job_content.replace("DFTB+", str(os.path.basename(folder)) + "_GO")
        with open(job_file, "w") as f:
            f.write(job_content)

        # Executa o GOBruno.py na subpasta
        os.chdir(sub_folder_path)  # Muda para a subpasta
        subprocess.run(["python3", "GOBruno.py"])
        os.chdir("../..")  # Retorna para a pasta pai

def main():
    create_folders()

    parent_folders = [str(i) for i in range(1, 31, 5)]  # Lista com as pastas pai
    for folder in parent_folders:
        execute_GOBruno(folder)

if __name__ == "__main__":
    main()
