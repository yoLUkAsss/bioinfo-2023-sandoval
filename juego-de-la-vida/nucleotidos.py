import random

NUCLEOTIDS_VALUES = "ACGU"
NUCLEOTIDS_OPPOSITE_VALUES = "UGCA"

def random_nucleotid_value():
    random_idx = random.randint(0, len(NUCLEOTIDS_VALUES) - 1)
    return NUCLEOTIDS_VALUES[random_idx]

def opposite_nucleotid(nucleotid):
    return NUCLEOTIDS_OPPOSITE_VALUES[NUCLEOTIDS_VALUES.index(nucleotid)]

def opposite_codon(codon):
    return "".join(NUCLEOTIDS_OPPOSITE_VALUES[NUCLEOTIDS_VALUES.index(nucleotid)] for nucleotid in codon)