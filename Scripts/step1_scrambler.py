import random


def scramble_sequence(seq):
    arr = []
    arr = list(seq)
    random.shuffle(arr)
    return "".join(arr)
def calculate_identity(seq1, seq2):
    matches = 0
    if (len(seq1) != len(seq2)):
        print('Length of sequances isnt equal', f'len of seq1 = {len(seq1)} , len of seq2 = {len(seq2)}')
        return -1
    for i in range(len(seq1)):
        if (seq1[i] == seq2[i]):
            matches+=1
    return matches/(len(seq1))* 100
def generate_scrambled_pool(aptamer_seq, n_samples=1000, max_identity=80.0):
    decoi_set = set()
    while (len(decoi_set) < n_samples):
        decoi = scramble_sequence(aptamer_seq)
        if (calculate_identity(aptamer_seq,decoi)  < max_identity):
            decoi_set.add(decoi)
    return decoi_set


