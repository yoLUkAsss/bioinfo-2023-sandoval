import os
import random
import argparse
import time

from structures import aminoacid_data, aminos_based_on_codon, codons_based_on_amino
from nucleotidos import opposite_nucleotid, random_nucleotid_value, opposite_codon

import utils

# CONSTANTES
NUMBER_OF_OPTIONS = 2
TIMER_STEP = 1.5
TIMER_RESULTS = .5
TIMER_EXPLAINATION = 1
TIMER_REPORT = 5
TIMER_STARTING = 2
TIMER_ENDING = 2

CORRECT_POINTS = 10
INCORRECT_POINTS = 5

def show_game_step(cadena, aminoacidos, current_points, aciertos_correctos, elementos_vistos, amount_invalid_option=NUMBER_OF_OPTIONS):

    print(f"#######################################################################")
    print(f"###    Cadena a Traducir: {cadena}")
    print(f"###    Codon Actual: {cadena[0:3]} - Aminoacido asociado: {aminos_based_on_codon[cadena[0:3]]}")
    print(f"###    Polipeptido Generado: {aminoacidos}")
    print(f"#######################################################################")
    print(f"\n\n###    Puntos: {current_points}   Correctos: {aciertos_correctos}   Analisis Completo: {(100*elementos_vistos/(elementos_vistos+len(cadena))):.2f}%")
    
    print(f"\n\n## .. Se encuentran disponibles los siguientes ARNt disponibles en el citosoma: ")
    options, idx_correct = generate_arnt_options(cadena[0:3], amount_invalid_option)

    print(" ".join(f"- Option {i+1}: {elem} -" for i, elem in enumerate(options)))
    
    return options, idx_correct

def show_message(message="", end=""):
    print(f"#######################################################################")
    print(f"###   " + message + "")
    print(f"#######################################################################")
    print(end)

def generate_arnt_options(codon, amount_invalid_options=NUMBER_OF_OPTIONS):
    options = []

    # Correct option
    codon_made = ""
    for idx in range(len(codon)):
        value_idx = opposite_nucleotid(codon[idx])
        codon_made += value_idx
    options.append(codon_made)
    
    for i in range(amount_invalid_options):
        bad_option = ""
        for idx in range(len(codon)):
            value_idx = random_nucleotid_value()
            bad_option += value_idx
        options.append(bad_option)

    random.shuffle(options)
    return options, options.index(codon_made)


def screen_clear():
    # Clear the screen using ANSI escape codes
    os.system('clear')

def validate_current_option(option_pressed, correct_option):

    is_correct = option_pressed == correct_option
    if is_correct:
        show_message(f"Correcto!! Sumas {CORRECT_POINTS} puntos")
    else:
        show_message(f"Incorrecto... Pierdes {INCORRECT_POINTS} puntos la opcion correcta era: " + str(correct_option))

    time.sleep(TIMER_RESULTS)
    return is_correct

def game(initial_arn, original_protein, game_name="Welcome to <inserte nombre de juego>", difficulty=NUMBER_OF_OPTIONS):

    current_points = 0
    aciertos_correctos = 0
    elementos_vistos = 0
    aminoacidos = ""
    arn = initial_arn

    # Pantalla de bienvenida
    screen_clear()
    show_message(game_name)
    time.sleep(TIMER_STEP)

    # Pantalla de descripcion
    screen_clear()
    show_message(f"¿ Como funciona la simulacion ?", end="\n")
    print(f"  La idea es simple, se mostrara una cadena ARNm y nuestra trabajo sera simular")
    print(f"el interior del ribosoma, donde ocurrira la traduccion.")
    print(f"Ante cada codon de la cadena, deberemos identificar de una lista de ARNt posibles")
    print(f"una opcion correcta y asi formar una proteina\n")
    print(f"  Recordemos que un ARNt sera correcto siempre que el triplete de nucleotidos sean opuestos")
    print(f"uno a uno con los nucleotidos del codon actual de la cadena ARNt\n")
    print(f"  Un ARNt bien elegido sumara {CORRECT_POINTS} puntos y uno incorrecto restara {INCORRECT_POINTS} puntos")
    print(f"Al finalizar se vera un reporte de correctitud y la cadena polipeptidica generada")

    ok_pressed = input("\n\nPresione ENTER, cuando quiera comenzar...")
    while ok_pressed != "":
        ok_pressed = input("\n\nPresione ENTER, cuando quiera comenzar...")

    time.sleep(TIMER_EXPLAINATION)

    while len(arn) > 0:
        try:

            # Game Start
            screen_clear()
            options, correct_option_index = show_game_step(arn, aminoacidos, current_points, aciertos_correctos, elementos_vistos, amount_invalid_option=difficulty)

            # Read a character from standard input
            char = input("\nIngrese una opcion: (o presione 'q' para salir): ")

            # Check if the user wants to quit
            if char == 'q':
                break

            # Check if the input is a digit
            if char.isdigit():
                value_pressed = int(char)
                if (value_pressed >= 1 and value_pressed <= difficulty+1):
                    is_correct = validate_current_option(value_pressed-1, correct_option_index)
                    
                    if is_correct:
                        current_points += CORRECT_POINTS
                        aciertos_correctos += 1
                        elementos_vistos += 3
                    else:
                        current_points -= INCORRECT_POINTS

                    aminoacidos += aminos_based_on_codon[opposite_codon(options[value_pressed-1])]
                    arn = arn[3:]

            # If it's neither a digit nor a letter
            else:
                print(f"Error: {char} no es una opcion valida!!!")

        except KeyboardInterrupt:
            print("\nQuitting...")
            break

    # Pantalla de resultados
    screen_clear()
    show_message(f"Traduccion completada: puntaje: {current_points} - rate: {(100 * aciertos_correctos)/len(original_protein)}%")
    print(f"CADENA ORIGINAL     : {original_protein}")
    print(f"CADENA FORMADA      : {aminoacidos}")
    time.sleep(TIMER_REPORT)

    # Pantalla de finalizacion
    screen_clear()
    show_message(f"Adios!!!")
    time.sleep(TIMER_ENDING)


if __name__ == "__main__":

    # Creamos parser
    parser = argparse.ArgumentParser(description="simple arguments parser")
    # Agregamos argumentos
    parser.add_argument("--file", help="Filename de un archivo FASTA")
    parser.add_argument("--options", help="Dificultad del juego, establece cantidad de ARNt a evaluar por codon")
    # Parseamos los argumentos
    args = parser.parse_args()
    # Obtenemos los valores de los argumentos
    fasta_filename = args.file
    sequences = utils.parse_fasta_file(fasta_filename if fasta_filename is not None else "example.fasta")
    options = int(args.options)

    # TODO: Aca podria (en realidad deberia, para q sea mas consistente) recibir un archivo 
    # q posea la cadena traducida y no una proteina, pero reutilize cosas que ya tenia
    cadena_proteina = sequences[0].chain # Tomamos solo uno, el primero
    arn = utils.generate_possible_random_codons(cadena_proteina) # Aca retornamos una posible cadena ARN en base al archivo FASTA utilizado

    time.sleep(TIMER_STARTING)
    game(arn, cadena_proteina, "Gene Expression: Translation Simulation", difficulty=options)