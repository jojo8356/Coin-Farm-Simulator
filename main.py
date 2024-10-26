# Fonctions de conversion
def convert_gold_to_pieces(gold):
    return gold / 1.2


def convert_pieces_to_gold(pieces):
    return pieces * 1.2


def convert_gold_to_euro(gold):
    return gold / 431 * 0.04


def convert_eggs_to_pieces(eggs):
    return eggs / 100


def convert_pieces_to_euros(pieces):
    gold = convert_pieces_to_gold(pieces)
    return convert_gold_to_euro(gold)


def convert_eggs_to_euros(eggs):
    pieces = convert_eggs_to_pieces(eggs)
    return convert_pieces_to_euros(pieces)


def calculate_monthly_income(inventory, bird_types):
    """Calcule le revenu mensuel total en pièces d'or basé sur l'inventaire actuel."""
    total_gold_per_month = sum(
        inventory[bird] * bird_types[bird]["yield_per_hour"] * 24 * 30
        for bird in inventory
    )
    return total_gold_per_month


def buy_birds(pieces, inventory, bird_types):
    """Achète le maximum d'oiseaux possible selon les pièces disponibles et met à jour l'inventaire."""
    for bird in sorted(
        bird_types.keys(), key=lambda x: bird_types[x]["yield_per_hour"], reverse=True
    ):
        bird_price = bird_types[bird]["price"]
        birds = 0
        while pieces >= bird_price:
            inventory.setdefault(bird, 0)
            inventory[bird] += 1
            birds += 1
            pieces -= bird_price
        if birds:
            print(f"achat de {birds} {bird}")
    return pieces


def get_all_price(bird_types):
    all_prices = [(bird, data["price"]) for bird, data in bird_types.items()]
    return all_prices


def can_buy(pieces, bird_types):
    prices = get_all_price(bird_types)
    return pieces > min(prices)[1]


def print_inventory(bird_inventory, bird_types):
    print("Inventaire des oiseaux :")
    print("------------------------")
    for bird, quantity in bird_inventory.items():
        price = bird_types[bird]["price"]
        yield_per_hour = bird_types[bird]["yield_per_hour"]
        print(
            f"{bird}: {quantity} possédé(s), Prix: {price} pièces, Rendement: {yield_per_hour} œufs/heure"
        )


# Données des types d'oiseaux
bird_types = {
    "Beige": {"yield_per_hour": 1, "price": 35},
    "Vert": {"yield_per_hour": 5, "price": 150},
    "Jaune": {"yield_per_hour": 55, "price": 1500},
    "Brun": {"yield_per_hour": 277, "price": 7500},
    "Bleu": {"yield_per_hour": 1430, "price": 37500},
    "Rouge": {"yield_per_hour": 7230, "price": 150000},
    "Royal": {"yield_per_hour": 21925, "price": 375000},
}

# Variables de départ
pieces = 250  # Pièces initiales
goal = 1500  # Objectif de 1500 euros par mois
inventory = {}  # Inventaire des oiseaux
euros = convert_pieces_to_euros(pieces)

# Simulation mensuelle
months = 0
while euros < goal:
    months += 1
    print(f"\n--- Mois {months} ---")
    print(pieces)

    if can_buy(pieces, bird_types):
        buy_birds(pieces, inventory, bird_types)

    print_inventory(inventory, bird_types)
    eggs = calculate_monthly_income(inventory, bird_types)
    pieces = convert_eggs_to_pieces(eggs)
    euros = convert_pieces_to_euros(pieces)
    print(f"\neuros: {euros}, pieces: {pieces}, eggs/heure: {eggs//(24*30)}")
