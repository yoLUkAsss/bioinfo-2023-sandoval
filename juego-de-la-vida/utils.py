import random
from structures import codons_based_on_amino

class FastaUnit:

    def __init__(self, name, chain) -> None:
        self.name = name
        self.chain = chain


def generate_possible_random_codons(amino_acid_string):

    # TODO: Utilizar matriz PAM para mejorar la generacion

    return "".join([random.choice(codons_based_on_amino[amino_acid]) for amino_acid in amino_acid_string])


def print_type_of(variable):
    print(f"Variable: {variable} is of type: {type(variable)}")


def parse_fasta_file(file_path):
    sequences = []
    current_sequence_name = ""
    current_sequence = []

    with open(file_path, "r") as fasta_file:
        for line in fasta_file:
            line = line.strip()  # Remove leading/trailing whitespace

            if line.startswith(">"):
                # This line contains the sequence name
                if current_sequence_name:
                    # If we have already started a sequence, store it
                    sequences[current_sequence_name] = "".join(current_sequence)
                    current_sequence = []

                current_sequence_name = line[1:]  # Remove ">" from the name
            else:
                # This line contains sequence data
                current_sequence.append(line)

        # Store the last sequence
        if current_sequence_name:
            sequences.append(
                FastaUnit(current_sequence_name, "".join(current_sequence))
            )

    return sequences