# Modules / Dependances
from configuration import APP_CONFIG
from directory_class import Directory
from gui_class import GUI

# Variables / Constantes globles
struct = {
    "root": ["*"],
    "main": ["*", "main.py"],
    "Venv": ["*", "Venv"],
    "variable": ["*", "env_variables.txt"]
}

dir = Directory(struct)
dir_infos = dir.get_directory_info()
#dir.format_python_files()

gui_properties = APP_CONFIG.GUI_PROPERTIES
gui_properties["btn_height"] = int(gui_properties["size"][1]) / dir_infos["nb_scripts"]

# Creation gui
app = GUI()
app.init(size="x".join(gui_properties["size"]), bg=gui_properties["bg"], title=gui_properties["title"])

for index, script_name in enumerate(dir_infos["scripts_name"]):
    app.add_ctn(
        name=f"ctn_btn_{script_name}",
        width=int(gui_properties["size"][0]),
        height=gui_properties["btn_height"],
        bg="grey",
        display_border=False,
        pos=[index, 0]
    )

    app.add_btn(
        name=f"btn{index}",
        x=1, y=1,
        text=script_name,
        bg="grey",
        activebackground="red",
        border_width=int(gui_properties["space_between_btn"]),
        callback=dir_infos["scripts_callback"][index],
        ctn=app.ctns[f"ctn_btn_{script_name}"]["object"]
    )

app.mainloop()
