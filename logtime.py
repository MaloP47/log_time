import datetime

def enregistrer_temps():
    print("1. Arrivée")
    print("2. Départ")
    print("3. Ajouter manuellement des heures")
    choix = input("Choisissez (1/2/3): ")

    maintenant = datetime.datetime.now()

    if choix == "1":
        action = "Arrivée"
    elif choix == "2":
        action = "Départ"
    elif choix == "3":
        heures = float(input("Combien d'heures voulez-vous ajouter? "))
        action = f"Ajouté {heures} heures"
        maintenant += datetime.timedelta(hours=heures)
    else:
        print("Choix invalide.")
        return

    avec = f"{action}, {maintenant.strftime('%Y-%m-%d %H:%M:%S')}\n"

    with open("temps_de_presence.txt", "a") as fichier:
        fichier.write(avec)

    print(f"{action} enregistré.")

def afficher_temps():
    with open("temps_de_presence.txt", "r") as fichier:
        print(fichier.read())

def jours_ouvrables_restants_mois():
    aujourdhui = datetime.datetime.today()
    dernier_jour_mois = (aujourdhui.replace(month=aujourdhui.month % 12 + 1, day=1) - datetime.timedelta(days=1)).day
    jours_restants = dernier_jour_mois - aujourdhui.day

    # Enlever les weekends
    jours_ouvrables = 0
    for i in range(aujourdhui.day, dernier_jour_mois + 1):
        if (aujourdhui + datetime.timedelta(days=i-aujourdhui.day)).weekday() < 5:
            jours_ouvrables += 1
    return jours_ouvrables

def temps_restant_pour_le_mois():
    with open("temps_de_presence.txt", "r") as fichier:
        lignes = fichier.readlines()

    total_seconds = 0
    arrivee = None

    for ligne in lignes:
        if ", " not in ligne:
            continue
        action, horaire = ligne.strip().split(", ")
        horaire = datetime.datetime.strptime(horaire, '%Y-%m-%d %H:%M:%S')

        if "Arrivée" in action:
            arrivee = horaire
        elif "Départ" in action and arrivee:
            total_seconds += (horaire - arrivee).total_seconds()
            arrivee = None
        elif "Ajouté" in action:
            heures = float(action.split(" ")[1])
            total_seconds += heures * 3600

    total_hours_worked = total_seconds / 3600

    temps_restant = 140 - total_hours_worked

    jours_restants = jours_ouvrables_restants_mois()

    if jours_restants == 0:
        print("Le mois est fini.")
        return

    moyenne_par_jour = temps_restant / jours_restants

    print(f"Temps restant pour 140h : {temps_restant:.2f} heures")
    print(f"Temps moyen à travailler par jour pour le reste du mois : {moyenne_par_jour:.2f} heures")

def calculer_temps_total():
    with open("temps_de_presence.txt", "r") as fichier:
        lignes = fichier.readlines()

    total_seconds = 0
    arrivee = None

    for ligne in lignes:
        if ", " not in ligne:
            continue
        action, horaire = ligne.strip().split(", ")
        horaire = datetime.datetime.strptime(horaire, '%Y-%m-%d %H:%M:%S')

        if "Arrivée" in action:
            arrivee = horaire
        elif "Départ" in action and arrivee:
            total_seconds += (horaire - arrivee).total_seconds()
            arrivee = None
        elif "Ajouté" in action:
            heures = float(action.split(" ")[1])
            total_seconds += heures * 3600

    total_hours_worked = total_seconds / 3600

    print(f"Temps total travaillé jusqu'à présent: {total_hours_worked:.2f} heures")
    temps_restant = 140 - total_hours_worked
    print(f"Temps restant pour atteindre 140h : {temps_restant:.2f} heures")


def menu():
    while True:
        print("\nMenu:")
        print("1. Enregistrer le temps")
        print("2. Afficher les temps")
        print("3. Calculer le temps total du mois")
        print("4. Temps moyen par jour restant")
        print("5. Quitter")
        choix = input("Choisissez (1/2/3/4/5): ")

        if choix == "1":
            enregistrer_temps()
        elif choix == "2":
            afficher_temps()
        elif choix == "3":
            calculer_temps_total()
        elif choix == "4":
            temps_restant_pour_le_mois()
        elif choix == "5":
            break
        else:
            print("Choix invalide.")

if __name__ == "__main__":
    menu()

