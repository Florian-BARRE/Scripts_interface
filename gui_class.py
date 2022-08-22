# Librairies
import tkinter as tkt

class GUI(tkt.Tk):
    """
    Classe permettant la construction de l'interface graphique (GUI)
    """
    ctns = dict()
    btns = dict()

    def init(self, **properties):
        """
        Initialise tout les parametres par defaut: fond, taille, titre
        :param properties:
        :return:
        """
        self.resizable(True, True)
        for key, value in properties.items():
            if key.lower() in ["size", "geometry", "dim", "dimension"] and isinstance(value, str):
                self.geometry(value)

            elif key.lower() in ["bg", "background", "color", "bg_color", "backgroundcolor"] and isinstance(value, str):
                self.configure(bg=value)

            elif key.lower() in ["title", "titre"] and isinstance(value, str):
                self.title(value)

    def add_ctn(self, **properties):
        """
        Permet d'ajouter un container au GUI, il peut contenir du texte / btn / etc ...
        :param properties:
        :return: container
        """
        ctn = tkt.Frame(self, width=properties.get("width", 10), height=properties.get("height", 10))
        # Update params
        for key, value in properties.items():
            if key.lower() in ["display_border", "affiher_bordure"] and isinstance(value, bool):
                ctn['highlightthickness'] = value

            elif key.lower() in ["bg", "background", "color", "bg_color", "backgroundcolor"] and isinstance(value, str):
                ctn.configure(bg=value)

            elif key.lower() in ["place", "pos", "position", "coords", "coord"] and isinstance(value, list):
                ctn.grid(row=value[0], column=value[1], sticky="s")

        # Add ctn to ctn_dict
        for key, value in properties.items():
            if key.lower() in ["name", "nom", "id"] and isinstance(value, (str, int)):
                self.ctns[value] = properties
                self.ctns[value]["object"] = ctn
                break
        return ctn

    def add_btn(self, **properties):
        """
        Permet d'ajouter un bouton GUI, ce bouton doit être dans un container
        :param properties:
        :return: bouton
        """
        btn = tkt.Button(properties.get("ctn", tkt.Frame(self, width=1, height=1)))

        # Update params
        for key, value in properties.items():
            if key.lower() in ["fg", "fc", "front_color", "frontcolor"] and isinstance(value, str):
                btn['fg'] = value

            elif key.lower() in ["bg", "background", "color", "bg_color", "backgroundcolor"] and isinstance(value, str):
                btn['bg'] = value

            elif key.lower() in ["activebackground", "active_bg_color", "activebackgroundcolor", "active_color",
                                 "activecolor"] and isinstance(value, str):
                btn["activebackground"] = value

            elif key.lower() in ["relief"] and isinstance(value, str):
                btn["relief"] = value

            elif key.lower() in ["borderwidth", "border_width", "taille_bordure", "largeur_bordure", "taillebordure",
                                 "largeurbordure"] and isinstance(value, int):
                btn["borderwidth"] = value

            elif key.lower() in ["text"] and isinstance(value, str):
                btn["text"] = value

            elif key.lower() in ["fonction", "function", "callback", "def"]:
                btn["command"] = value

        # Add ctn to ctn_dict
        for key, value in properties.items():
            if key.lower() in ["name", "nom", "id"] and isinstance(value, (str, int)):
                self.btns[value] = properties
                self.btns[value]["object"] = btn
                break

        btn.place(relwidth=properties.get("x", 1), relheight=properties.get("y", 1))
        return btn
