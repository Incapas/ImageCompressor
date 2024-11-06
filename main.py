import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from pathlib import Path

import customtkinter as ctk
from PIL import Image

# Configuration de la fenêtre principale de l'application.
app = ctk.CTk()
app.title("")
app.geometry(f"800x130+0+0")
app.resizable(width=False, height=False)
 
# Déclaration de la variable qui va contenir l'ensemble des images et de leurs données.
data = {}

# Déclaration de la variable de contrôle dynamique.
images_counter = tk.IntVar()


def select_images_to_reduce_their_size() -> None:
    """
    Fonction qui permet à l'utilisateur d'ouvrir son explorateur de fichiers.
    L'utilisateur pourra ensuite sélectionner une ou plusieurs images ('jpg', 'jpeg').
    La fonction analyse les différents fichiers.
    Si l'un des fichiers sélectionnés n'a pas une extension autorisée, l'utilisateur est alertée par une fenêtre Tkinter.
    Si toutes les extensions sont acceptées, les données sont ajoutées au dictionnaire 'data' dans l'espace global.

    Returns:
        None:
    """
    files = filedialog.askopenfilenames()
    extensions = [file.split(".")[-1] for file in files]
    if not all([True if extension in ["jpg", "jpeg"] else False for extension in extensions]):
        messagebox.showwarning(message="Attention, seuls les fichiers 'JPG' et 'JPEG' sont autorisés !")
    else:
        for idx, file in enumerate(files):
            image = Image.open(file)
            data[idx] = {
                "image_extension": image.filename.split(".")[-1],
                "image_name": image.filename.split("/")[-1].split(".")[0],
                "image_path_before_reduction": image.filename,
                }
    images_counter.set(len(data))
    return None


def reduce_the_size_of_selected_images() -> None:
    """
    Fonction qui permet à l'utilisateur d'ouvrir son explorateur de fichiers.
    L'utilisateur pourra ensuite sélectionner un dossier pour y exporter les images importées précédemment.
    L'utilisateur pourra également décider de conserver les images à compresser.
    Dans ce cas, le suffixe '-copie' sera ajouté au nom du fichier si le dossier de destination contient déjà un fichier avec un nom similaire.
    Si le dossier de destination n'est pas le même, le nom d'origine est conservé.
    Si l'utilisateur décide de ne pas conserver les images à compresser, le nom d'origine est gardé et les fichiers importés sont supprimés.

    Returns:
        None:
    """
    remove_images_choice = remove_images_to_reduce()
    if len(data) < 1:
        messagebox.showwarning(message="Atttention, aucune image n'a été importée !")
    else:
        directory = filedialog.askdirectory() 
        try:
            for i in range(len(data)):
                image = Image.open(data[i]["image_path_before_reduction"])
                data[i]["image_path_after_reduction"] = f"{directory}/{data[i]["image_name"]}.{data[i]["image_extension"]}"
                duplicate_check = Path(data[i]["image_path_after_reduction"])
                if duplicate_check.exists() and remove_images.get() == 1:
                    data[i]["image_name"] = f"{data[i]["image_name"]}-copie"
                    data[i]["image_path_after_reduction"] = f"{directory}/{data[i]["image_name"]}.{data[i]["image_extension"]}"
                    image.save(data[i]["image_path_after_reduction"], quality=50)
                else:
                    image.save(data[i]["image_path_after_reduction"], quality=50)
            data.clear()
            images_counter.set(len(data))
        except:
            pass
        return None


def cancel_selection() -> None:
    """
    Fonction qui permet de vider le dictionnaire 'data' dans l'espace global.

    Returns:
        None:
    """
    data.clear()
    images_counter.set(len(data))
    return None


def remove_images_to_reduce() -> int:
    """
    Fonction qui permet de retourner la valeur du widget 'remove_images'.
    La fonction retourne un entier faisant référence à un booléen : 1/True ou 0/False.

    Returns:
        int: 1 si le widget est coché / 0 si le widget est décoché.
    """
    return remove_images.get()


# frame haute et ses widgets
top_container = ctk.CTkFrame(master=app)
top_container.pack(ipady=10)

counter_label = ctk.CTkLabel(master=top_container, text="Nombre d'images sélectionnées : ", width=500, anchor="e")
counter_label.grid(column=0, row=0, columnspan=2)

counter= ctk.CTkLabel(master=top_container, textvariable=images_counter, width=300, anchor="w")
counter.grid(column=3, row=0)

# frame centrale et ses widgets
center_container = ctk.CTkFrame(master=app)
center_container.pack(ipady=10)

remove_images = ctk.CTkCheckBox(master=center_container, command=remove_images_to_reduce, text="Conserver les images importées", width=800)
remove_images.grid(column=0, row=0, padx=280)

# frame basse et ses widgets
bottom_container = ctk.CTkFrame(master=app, width=800)
bottom_container.pack(ipady=10, fill="x")

cancel = ctk.CTkButton(master=bottom_container, command=cancel_selection, text="Annuler", fg_color="#D91604", hover_color="#970F02")
cancel.grid(column=0, row=0, padx=90)

select = ctk.CTkButton(master=bottom_container, command=select_images_to_reduce_their_size, text="Importer", fg_color="#46788C", hover_color="#315462")
select.grid(column=2, row=0)

reduce = ctk.CTkButton(master=bottom_container, command=reduce_the_size_of_selected_images, text="Exporter", fg_color="#088C7F", hover_color="#056258")
reduce.grid(column=4, row=0, padx=90)


# affichage de la fenêtre de l'application
if __name__ == "__main__":
    app.mainloop()
