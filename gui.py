import tkinter
from copy import deepcopy
from pathlib import Path

from main import CLUES, CULPRIT_ID, SUSPECTS, update_probabilities

BASE_DIR = Path(__file__).resolve().parent
SUSPECTS_GUI = deepcopy(SUSPECTS)
CLUES_GUI = deepcopy(CLUES)
USED_EVIDENCE_GROUPS = set()
CLUE_BUTTONS = {}
SUSPECTS_WIDGET = {}

SUSPECT_IMAGE_COORDS = {
    "alexey": (0, 0, 724, 724),
    "maria": (724, 0, 1448, 724),
    "viktor": (1448, 0, 2172, 724),
}

CLUE_BUTTON_TEXTS = {
    "1": "Камера",
    "2": "Отпечатки",
    "3": "Карта доступа",
    "4": "Датчик движения",
}


def accuse_suspect_gui(suspect_id):
    culprit = SUSPECTS_GUI[CULPRIT_ID]
    true_crime_person = (
        f"Настоящий преступник: {culprit['name']} — {culprit['role']}"
    )

    if suspect_id == CULPRIT_ID:
        label_suspect_text = "Вы настоящий детектив.\n" + true_crime_person
    else:
        label_suspect_text = "Вы не угадали преступника.\n" + true_crime_person

    clue_status_label.configure(text=label_suspect_text)

    for button in CLUE_BUTTONS.values():
        button.configure(state="disabled")

    for button in SUSPECTS_WIDGET.values():
        button.configure(state="disabled")


def refresh_suspect_cards():
    for suspect_id, label in SUSPECTS_WIDGET.items():
        suspect = SUSPECTS_GUI[suspect_id]
        label.configure(
            text=(
                f"{suspect['name']}: {suspect['role']} "
                f"{suspect['probability']:.1%}"
            )
        )


def examine_clue_gui(clue_id: str):
    clue = CLUES_GUI[clue_id]
    label_status_text = ""
    if clue["evidence_group"] not in USED_EVIDENCE_GROUPS:
        update_probabilities(
            SUSPECTS_GUI,
            clue["likelihoods"],
        )
        USED_EVIDENCE_GROUPS.add(clue["evidence_group"])
        refresh_suspect_cards()
        label_status_text = clue["text"]
    else:
        label_status_text = (
            f"{clue['text']}\n"
            "Вероятности повторно не изменены"
        )

    clue["examined"] = True
    CLUE_BUTTONS[clue_id].configure(state="disabled")
    clue_status_label.configure(text=label_status_text)


root = tkinter.Tk()
root.title("Музейный детектив")
root.geometry("960x540")

background_image = tkinter.PhotoImage(
    file=str(BASE_DIR / "assets" / "museum-night.png")
)

suspect_sprite_sheet = tkinter.PhotoImage(
    file=str(BASE_DIR / "assets" / "suspects.png")
)

SUSPECT_IMAGES = {}

for suspect_id, coordinates in SUSPECT_IMAGE_COORDS.items():
    SUSPECT_IMAGES[suspect_id] = suspect_sprite_sheet.copy(
        from_coords=coordinates,
        subsample=4,
    )

background_image = background_image.subsample(2, 2)


root_label = tkinter.Label(root, image=background_image)

root_label.place(relx=0.5, rely=0.5, anchor="center")

title_label = tkinter.Label(
    root,
    text="ДЕЛО №001\nПРОПАВШИЙ АРТЕФАКТ",
    font=("Menlo", 22, "bold"),
    fg="#F4D58D",
    bg="#101827",
)

title_label.place(relx=0.5, rely=0.08, anchor="center")

index = 0
for suspect_id in SUSPECTS_GUI:
    suspect_button = tkinter.Button(
        root,
        image=SUSPECT_IMAGES[suspect_id],
        compound="top",
        command=lambda suspect_id=suspect_id: accuse_suspect_gui(suspect_id),
    )
    suspect_button.place(relx=0.2 + index, rely=0.5, anchor="center")
    index += 0.3
    SUSPECTS_WIDGET[suspect_id] = suspect_button

index = 0
for clue_button_id, button_text in CLUE_BUTTON_TEXTS.items():
    clue_button = tkinter.Button(
        root,
        text=button_text,
        command=lambda clue_id=clue_button_id: examine_clue_gui(clue_id)
    )
    clue_button.place(
        relx=0.2 + index,
        rely=0.9,
        anchor="center",
    )
    index += 0.2
    CLUE_BUTTONS[clue_button_id] = clue_button

clue_status_label = tkinter.Label(
    root,
    text="",
    wraplength=700,
    fg="#F4D58D",
    bg="#101827",
)

clue_status_label.place(
    relx=0.5,
    rely=0.78,
    anchor="center",
)

refresh_suspect_cards()
root.configure(bg="#101827")
root.mainloop()
