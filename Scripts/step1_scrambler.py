import random
import subprocess
import tempfile
import os
import numpy as np
import multiprocessing as mp
import pandas as pd
def scramble_sequence(seq):

    arr = []
    arr = list(seq)
    random.shuffle(arr)
    return "".join(arr)
def calculate_identity(seq1, seq2):
    matches = 0
    if (len(seq1) != len(seq2)):
        return -1
    for i in range(len(seq1)):
        if (seq1[i] == seq2[i]):
            matches+=1
    return matches/(len(seq1))* 100
def generate_scrambled_pool(aptamer_seq, n_samples=1000, max_identity=80.0 , Seed = 12345):
    random.seed(Seed)
    decoi_set = set()
    while (len(decoi_set) < n_samples):
        decoi = scramble_sequence(aptamer_seq)
        if (calculate_identity(aptamer_seq,decoi)  < max_identity):
            decoi_set.add(decoi)
    return decoi_set





def parser_ct (path):
    index_energy = None
    with open(path ) as f:
        lines = f.readlines()
        heading = lines[0].split()
        num_of_dots = 0
        for i in range(len(heading)):
            if (heading[i] == '='):
                index_energy = i + 1
        for line in lines[1:]:
            part = line.split()
            if len(part) >= 5 and part[4] == "0":
                num_of_dots += 1
    if (index_energy == None):
        return (0.0 , num_of_dots)
    else:
        return (float(heading[index_energy]), num_of_dots)

def run_rnastructure (seq):

    with tempfile.TemporaryDirectory() as tmpdir:
        fasta_file = os.path.join(tmpdir, "seq.fasta")
        ct_file = os.path.join(tmpdir, "out.ct")
        with open(fasta_file , 'w') as f:
            f.write(f">seq\n{seq}\n")
        subprocess.run(['Fold', fasta_file,ct_file], stdout=subprocess.PIPE,
                   stderr=subprocess.PIPE,
                   text=True)
        energy, dots = parser_ct(ct_file)
    return energy, dots

def calculate_z_scores(apt_seq, Seed=12345):
    num_cores = mp.cpu_count()
    Energy_apt = run_rnastructure(apt_seq)[0]
    decoi_list = np.array(list(generate_scrambled_pool(apt_seq, Seed=Seed)))
    with mp.Pool(processes=num_cores) as pool:
        results = pool.map(run_rnastructure , decoi_list)
    results = np.array(results)
    energy_list = np.array(results[:,0])
    dots_list = np.array(results[: , 1])
    mean_energy = np.mean(energy_list)
    std_energy = np.std(energy_list)
    z_score_apt = (Energy_apt - mean_energy) / std_energy
    z_score_decoi = (energy_list - mean_energy) / std_energy

    return  z_score_apt, z_score_decoi, decoi_list, dots_list

def similarity_with_aptamers (seq1 , apt_list):
    for i in range(len(apt_list)):
        ident = calculate_identity(seq1, apt_list[i])
        if (ident == -1):
            continue
        if ( (ident != -1 )and (ident > 70) ):
            return False

    return True



def make_decoi_list (apt_seq , apt_list, Attempt = 1, base_seed=12345):
    decoi = calculate_z_scores(apt_seq , base_seed)
    decoi_sort = []
    for i in range(len(decoi[2])):
        if (decoi[1][i] < -1):
            if (decoi[3][i] > 11):
                if (similarity_with_aptamers(decoi[2][i] ,apt_list)):
                    this_decoi = decoi[2][i]
                    decoi_sort.append((this_decoi , calculate_identity(apt_seq ,this_decoi)))
    if (len(decoi_sort) >= 3):
        decoi_sort.sort(key=lambda decoi: decoi[1])
        decoi_result = []
        decoi_result.append(decoi_sort[0][0])
        for i in range(len(decoi_sort)):
            if (( similarity_with_aptamers(decoi_sort[i][0] , decoi_result) ) and  (len(decoi_result) < 3)):
                decoi_result.append(decoi_sort[i][0])
        return decoi_result
    elif (Attempt < 3) :
        return make_decoi_list(
            apt_seq, apt_list, Attempt=Attempt + 1, base_seed=base_seed + 1
        )
    else:
        decoi_sort.sort(key=lambda x: x[1])
        return [x[0] for x in decoi_sort]



