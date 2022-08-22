# Librairie(s)
import glob
import os
from functools import partial
from pathlib import Path

# Modules / Dependances
from configuration import APP_CONFIG


class Directory:
    _execution_path = APP_CONFIG.BASE_DIR
    _scripts_path = os.path.join(_execution_path, '..')

    # Template path: root & main & Venv
    _root_template_path = _scripts_path
    _main_template_path = _scripts_path
    _Venv_template_path = _scripts_path
    _env_variables_template_path = _scripts_path

    # List of root path & main.py & Venv path
    _paths_roots = list()
    _paths_scripts = list()
    _paths_Venvs = list()
    _paths_python_files = list()

    # List of environnement variable
    _env_variables = list()

    # Directory informations dictonnary
    _directory_infos = dict()

    def __init__(self, project_structure):
        # Get root template path and the list of all root path
        for folder in project_structure["root"]:
            self._root_template_path = os.path.join(self._root_template_path, folder)
        self._get_list_of_root_path()

        # Get main template path and the list of all main.py path
        for folder in project_structure["main"]:
            self._main_template_path = os.path.join(self._main_template_path, folder)
        self._get_list_of_main_path()

        # Get Venv template path and the list of all Venv path
        for folder in project_structure["Venv"]:
            self._Venv_template_path = os.path.join(self._Venv_template_path, folder)
        self._get_list_of_Venv_path()

        # Get environnement variables template path and the list of all variables path
        for folder in project_structure["variable"]:
            self._env_variables_template_path = os.path.join(self._env_variables_template_path, folder)
        self._get_list_of_env_variables()

        self._get_list_of_python_files_path()

    def exec_script(self, name, root_path, main_path, Venv_path, env_variables):
        # Creation des lignes de commandes pour l'execution du projet
        #   desactivation du Venv par defaut
        #   cd dans le dossier du projet
        #   activation du Venv du projet

        # Variables d environnement
        cmd_env_variables = "".join(
            f"set {variable}={value}{APP_CONFIG.GLOBAL['cmds']['add cmd']}" for variable, value in env_variables.items()
        )

        commands = f'{os.path.join(self._execution_path, "Venv", "Scripts", "deactivate")} {APP_CONFIG.GLOBAL["cmds"]["add cmd"]} ' \
                   f'cd {root_path} {APP_CONFIG.GLOBAL["cmds"]["add cmd"]} ' \
                   f'{os.path.join(Venv_path, "Scripts", "activate")} {APP_CONFIG.GLOBAL["cmds"]["add cmd"]} ' \
                   f'{cmd_env_variables}' \
                   f'{APP_CONFIG.GLOBAL["cmds"]["print"]} Start projet: {name} {APP_CONFIG.GLOBAL["cmds"]["add cmd"]} ' \
                   f'python {main_path}'

        # f'clear & ' et cls pour windows TODO: clear terminal

        commands_save_path = os.path.join(self._execution_path, 'run_scripts', name)

        # Pour Win -> on cree un fichier .bat
        if APP_CONFIG.GLOBAL["os"] == "win":
            with open(f"{commands_save_path}.bat", "w", encoding='utf-8') as file:
                file.write(commands)
            # On lance le projet
            os.system(f"{APP_CONFIG.GLOBAL['cmds']['open new terminal and pass cmds']} {commands_save_path}")

        # Pour Linux -> on cree un fichier .sh
        elif APP_CONFIG.GLOBAL["os"] == "linux":
            with open(f"{commands_save_path}.sh", "w", encoding='utf-8') as file:
                file.write(commands)
            # On lance le projet
            os.system(f"{APP_CONFIG.GLOBAL['cmds']['open new terminal and pass cmds']} 'bash {commands_save_path}; '")

        else:
            print("OS non reconnu")

    def _get_list_of_root_path(self):
        for root_path in glob.glob(self._root_template_path, recursive=True):
            # On trie les chemins racines dirigeant vers un simple fichier car ils sont incomplets
            if os.path.isdir(root_path):
                self._paths_roots.append(root_path)

    def _get_list_of_main_path(self):
        for main_path in glob.glob(self._main_template_path, recursive=True):
            self._paths_scripts.append(main_path)

    def _get_list_of_Venv_path(self):
        for Venv_path in glob.glob(self._Venv_template_path, recursive=True):
            self._paths_Venvs.append(Venv_path)

    def _get_list_of_env_variables(self):
        for variables_path in glob.glob(self._env_variables_template_path, recursive=True):
            if os.path.isfile(variables_path):
                variables = dict()

                with open(variables_path, "r", encoding='utf-8') as file:
                    variables_str = file.read()

                variables_lignes = variables_str.split("\n")
                for ligne in variables_lignes:
                    if ligne != "":
                        variable, value = ligne.split("=")[0], ligne.split("=")[1]
                        variables[variable] = value

                self._env_variables.append(variables)

    def _get_list_of_python_files_path(self):
        list_of_no_count_python_files = [
            "Venv",
            "__pycache__",
            ".idea"
        ]

        for root, dirs, files in os.walk(".", topdown=False):
            for name in files:
                file_path_parts = Path(root).parts
                # Si aucune parties alors fichier a la racine
                if (len(file_path_parts) == 0 or \
                    (len(file_path_parts) > 0 and file_path_parts[0] not in list_of_no_count_python_files)) and \
                        os.path.splitext(name)[1] == ".py":
                    self._paths_python_files.append(
                        os.path.join(
                            os.path.abspath(root),
                            name
                        )
                    )

    def format_python_files(self):
        for file_path in self._paths_python_files:
            try:
                if file_path != os.path.realpath(__file__):
                    with open(file_path, 'r', encoding="UTF-8") as f:
                        file = f.read()

                    with open(file_path, 'w', encoding="UTF-8") as f:
                        f.write(file.replace("é", "e").replace("è", "e").replace("ô", "o").replace("à", "a"))
            except:
                pass

    def get_directory_info(self):
        self._directory_infos["root template path"] = os.path.dirname(self._root_template_path)
        self._directory_infos["main template path"] = os.path.dirname(self._main_template_path)
        self._directory_infos["Venv template path"] = os.path.dirname(self._Venv_template_path)

        self._directory_infos["nb_scripts"] = len(self._paths_scripts)

        self._directory_infos["roots_path"] = self._paths_roots
        self._directory_infos["scripts_path"] = self._paths_scripts
        self._directory_infos["Venvs_path"] = self._paths_Venvs

        self._directory_infos["env_variables"] = self._env_variables

        self._directory_infos["scripts_name"] = [
            os.path.basename(os.path.dirname(path_script)) for path_script in self._paths_scripts
        ]

        self._directory_infos["python_files_path"] = self._paths_python_files

        self._directory_infos["scripts_callback"] = list()
        for script_index in range(self._directory_infos["nb_scripts"]):
            self._directory_infos["scripts_callback"].append(
                partial(
                    self.exec_script,
                    self._directory_infos["scripts_name"][script_index],
                    self._directory_infos["roots_path"][script_index],
                    self._directory_infos["scripts_path"][script_index],
                    self._directory_infos["Venvs_path"][script_index],
                    self._directory_infos["env_variables"][script_index],
                )
            )

        return self._directory_infos
