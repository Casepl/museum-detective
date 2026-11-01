CULPRIT_ID = "maria"

SUSPECTS = {
    "alexey": {
        "name": "Алексей",
        "role": "охранник",
        "description": "Имел доступ ко всем помещениям, но утверждает, что всю ночь был на посту.",
        "probability": 0.35
    },
    "maria": {
        "name": "Мария",
        "role": "реставратор",
        "description": "Работала с артефактом и знала, где он хранится",
        "probability": 0.40
    },
    "viktor": {
        "name": "Виктор",
        "role": "коллекционер",
        "description": "Интересовался артефактом и предлагал музею его продать",
        "probability": 0.25
    }
}

CAMERA_LIKELIHOODS = {
    "alexey": 0.80,
    "maria": 0.45,
    "viktor": 0.25
}

FINGERPRINT_LIKELIHOODS = {
    "alexey": 0.25,
    "maria": 0.85,
    "viktor": 0.15
}

KEYCARD_LIKELIHOODS = {
    "alexey": 0.90,
    "maria": 0.65,
    "viktor": 0.10,
}


CLUES = {
    "1": {
        "text": "Камера наблюдения зафиксировала движение ночью.",
        "likelihoods": CAMERA_LIKELIHOODS,
        "evidence_group": "corridor_presence",
        "examined": False,
    },
    "2": {
        "text": "На витрине обнаружены отпечатки пальцев.",
        "likelihoods": FINGERPRINT_LIKELIHOODS,
        "evidence_group": "fingerprints",
        "examined": False,
    },
    "3": {
        "text": "Система доступа зарегистрировала открытие двери.",
        "likelihoods": KEYCARD_LIKELIHOODS,
        "evidence_group": "door_access",
        "examined": False,
    },
    "4": {
        "text": "Датчик движения подтвердил присутствие в коридоре.",
        "likelihoods": CAMERA_LIKELIHOODS,
        "evidence_group": "corridor_presence",
        "examined": False,
    },
}

def show_suspects(suspects):
    for suspect in suspects.values():
        print(f"{suspect['name']} — {suspect['role']}")
        print(suspect["description"])
        print(f"Вероятность: {suspect['probability']:.1%}")

def show_probabilities(suspects):
    print("Текущие вероятности:")

    for suspect in suspects.values():
        print(f"{suspect['name']}: {suspect['probability']:.1%}")

def update_probabilities(suspects, likelihoods):
    weights = {}

    for suspect_id, suspect in suspects.items():
        weights[suspect_id] = (
            suspect["probability"] * likelihoods[suspect_id]
        )
    total_weight = sum(weights.values())

    if total_weight == 0:
        raise ValueError("Сумма весов не может быть равна нулю")

    for suspect_id, weight in weights.items():
        suspects[suspect_id]["probability"] = weight / total_weight

def accuse_suspect(suspects, culprit_id):
    print("Кого вы обвиняете?")

    for suspect_id, suspect in suspects.items():
        print(f"{suspect_id} — {suspect['name']}")

    accused_id = input("Ваш выбор: ")

    if accused_id not in suspects:
        print("Неизвестный подозреваемый.")
        return False

    if culprit_id == accused_id:
        print("Вы настоящий детектив.")
    else:
        print("Вы не угадали преступника.")

    culprit = suspects[culprit_id]
    print(
        f"Настоящий преступник: "
        f"{culprit['name']} — {culprit['role']}."
    )

    return True

def examine_clue(clues, suspects, used_evidence_groups):
    print("Доступные улики:")

    for clue_id, clue in clues.items():
        print(f"{clue_id} - {clue['text']}")

    clue_id = input("Выберите улику: ")
    clue = clues.get(clue_id)

    if clue is None:
        print("Неизвестная улика.")
        return

    if clue["examined"]:
        print("Эта улика уже изучена.")
        return

    evidence_group = clue["evidence_group"]
    print(clue['text'])

    if evidence_group in used_evidence_groups:
        print("Эта улика подтверждает уже учтённое свидетельство.")
        print("Вероятности повторно не изменены.")
        clue["examined"] = True
        return

    update_probabilities(suspects, clue['likelihoods'])
    used_evidence_groups.add(evidence_group)
    clue["examined"] = True

    print("Вероятности обновлены.")

def run_game():
    used_evidence_groups = set()

    while True:
        print("1 — Посмотреть подозреваемых")
        print("2 — Изучить улику")
        print("3 — Посмотреть вероятности")
        print("4 — Назвать преступника")
        print("0 — Выйти")
        choice = input("Ваш выбор: ")

        if choice == "1":
            show_suspects(SUSPECTS)
        elif choice == "2":
            examine_clue(CLUES, SUSPECTS, used_evidence_groups)
        elif choice == "3":
            show_probabilities(SUSPECTS)
        elif choice == "4":
            accusation_finished = accuse_suspect(SUSPECTS, CULPRIT_ID)

            if accusation_finished:
                show_probabilities(SUSPECTS)
                print(
                    "Высокая вероятность — это обоснованное предположение, "
                    "а не доказательство вины."
                )
                print("Расследование завершено.")
                break
        elif choice == "0":
            print("Расследование завершено.")
            break
        else:
            print("Неизвестная команда")


if __name__ == "__main__":
    run_game()
