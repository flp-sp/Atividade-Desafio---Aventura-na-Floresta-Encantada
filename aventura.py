# Variaveis globais do jogo - CUIDADO: Nao use variaveis globais em projetos grandes!
player_name = ""
player_health = 0
inventory = []
current_location = ""

# Variáveis novas
monster_health = 0
MONSTER_DAMAGE = 0
PLAYER_DAMAGE = 0
POTION_EFFECT = 0

# Mapa do jogo
locations = {
    "Clareira Tranquila": {
        "description": "Você está em uma clareira ensolarada. Há um caminho para o Leste.",
        "east": "Caminho da Floresta",
        "items": ["poção pequena"]
    },
    "Caminho da Floresta": {
        "description": "Uma trilha estreita serpenteia pela floresta. Você pode ir para o Oeste ou Norte.",
        "west": "Clareira Tranquila",
        "north": "Caverna Sombria"
        "south": "Pântano Misterioso"
    },
    "Caverna Sombria": {
        "description": "Uma caverna escura e úmida. Há um brilho fraco no fundo. Você pode voltar para o Sul.",
        "south": "Caminho da Floresta",
        "items": ["amuleto mágico"]
    },
    "Pântano Misterioso": {
        "description": "Um pântano denso e perigoso. Você sente um arrepio. Há um caminho para o Leste.",
        "east": "Clareira Tranquila",
        "challenge": True # Novo desafio
    }
}

def display_status():
    print("\n--- Status do Jogador ---")
    print(f"Nome: {player_name}")
    print(f"Vida: {player_health}")
    print(f"Inventário: {', '.join(inventory) if inventory else 'Vazio'}")
    print("------------------------")

def main_game_loop():
    global player_name, player_health, current_location, inventory
    global monster_health, MONSTER_DAMAGE, PLAYER_DAMAGE, POTION_EFFECT # novas variáveis

    # Inicializacao do jogo
    player_name = input("Qual o seu nome, aventureiro? ")
    player_health = 100
    current_location = "Clareira Tranquila"
    inventory = []

    # inicializações novas
    monster_health = 100
    MONSTER_DAMAGE = 25
    PLAYER_DAMAGE = 30
    POTION_EFFECT= 30

    game_active = True
    while game_active:
        print(f"\nVocê está em: {current_location}")
        print(locations[current_location]["description"])

        # Opcoes de saida
        exits = []
        for direction in ["north", "south", "east", "west"]:
            if direction in locations[current_location]:
                exits.append(direction.capitalize())
        print(f"Saídas disponíveis: {', '.join(exits)}")

        # Itens no local
        if "items" in locations[current_location] and locations[current_location]["items"]:
            print(f"Itens neste local: {", ".join(locations[current_location]["items"])}")

        # Desafio movido para depois das ações

        action = input("O que você quer fazer? (andar [direção], pegar [item], usar [item], atacar, sair) ").lower().strip()

        if action.startswith("andar "):
            parts = action.split(" ")
            if len(parts) > 1:
                direction_input = parts[1]
                
                if direction_input == "norte" and "north" in locations[current_location]:
                    current_location = locations[current_location]["north"]
                elif direction_input == "sul" and "south" in locations[current_location]:
                    current_location = locations[current_location]["south"]
                elif direction_input == "leste" and "east" in locations[current_location]:
                    current_location = locations[current_location]["east"]
                elif direction_input == "oeste" and "west" in locations[current_location]:
                    current_location = locations[current_location]["west"]
                else:
                    print("Você não pode ir nessa direção.")
            else:
                print("Por favor, especifique uma direção para andar.")

        elif action.startswith("pegar "):
            item_to_pick = action.split(" ",1)[1] # slice mal feito
            if "items" in locations[current_location] and item_to_pick in locations[current_location]["items"]:
                inventory.append(item_to_pick)
                locations[current_location]["items"].remove(item_to_pick)
                print(f"Você pegou o {item_to_pick}.")
            else:
                print("Este item não está aqui.")

        elif action.startswith("usar "):
            item_to_use = action.split(" ",1)[1]
            if item_to_use in inventory:
                if item_to_use == "poção pequena":
                    player_health = min(100, player_health + POTION_EFFECT)
                    inventory.remove(item_to_use)
                    print(f"Você usou a poção e recuperou {POTION_EFFECT} de vida.")
                elif item_to_use == "amuleto mágico":
                    print("Você usou o Amuleto Mágico! PARABÉNS, você venceu o jogo!")
                    game_active = False
                else:
                    print("Você não sabe como usar este item agora.")
            else:
                print("Você não tem este item no seu inventário.")

        elif action == "atacar": # ação nova de atacar
            if "challenge" in locations[current_location] and locations[current_location]["challenge"] == True:
                monster_health -= PLAYER_DAMAGE
                if monster_health < 0: # garantir que a vida do monstro não seja menor que zero
                    monster_health = 0


        elif action == "sair":
            game_active = False
            print("Você decidiu sair da Floresta Encantada. Até a próxima!")

        else:
            print("Comando inválido.")

        # Desafio no local
        if "challenge" in locations[current_location] and locations[current_location]["challenge"] == True:
            if monster_health > 0:
                print("O monstro do pântano te ataca!")
                player_health -= MONSTER_DAMAGE
                if player_health < 0: # evitar que a vida do player seja < 0
                    player_health = 0

                print(f"Você perdeu {MONSTER_DAMAGE} de vida. Vida atual: {player_health}")
                print(f"Você acertou um golpe e tirou {PLAYER_DAMAGE} de vida do monstro. Vida atual do monstro: {monster_health}")
                display_status()
            elif monster_health <= 0:
                locations[current_location]["challenge"] = False # Desafio só acaba se o monstro morrer
                print(f"Você acertou um golpe e tirou {PLAYER_DAMAGE} de vida do monstro. O monstro foi derrotado")
                # adicionar lógica dos caminhos
                display_status()
            else:
                display_status()
                

        # Condicoes de fim de jogo
        if player_health <= 0:
            print("Sua vida chegou a zero. Fim de jogo!")
            game_active = False
        
        if current_location == "Caverna Sombria" and "amuleto mágico" in inventory and game_active:
            print("Você encontrou o Amuleto Mágico e venceu o jogo!")
            game_active = False


# Chamada principal para iniciar o jogo
main_game_loop()