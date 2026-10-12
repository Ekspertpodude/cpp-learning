import random
import subprocess
import tempfile
import os
import numpy as np
import multiprocessing as mp
import pandas as pd
import csv
from concurrent.futures import ProcessPoolExecutor, as_completed
import sys
import time
import re


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
    ss_chars = []
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        return 0.0, 0 , ''
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
            if len(part) >= 5:
                try:
                    # Пытаемся перевести в числа
                    my_idx = int(part[0])
                    pair_idx = int(part[4])
                except ValueError:
                    # Если там текст (например, слово 'seq'), просто пропускаем строку!
                    continue


                if pair_idx == 0:

                    num_of_dots += 1
                    ss_chars.append('.')
                elif my_idx < pair_idx:

                    ss_chars.append('(')
                else:

                    ss_chars.append(')')


        ss_string = "".join(ss_chars)

        if index_energy is None or index_energy >= len(heading):
            return 0.0, num_of_dots, ss_string
        else:
            return float(heading[index_energy]), num_of_dots, ss_string

def run_rnastructure (seq):
    with tempfile.TemporaryDirectory(dir='/dev/shm') as tmpdir:
        fasta_file = os.path.join(tmpdir, "seq.fasta")
        ct_file = os.path.join(tmpdir, "out.ct")
        with open(fasta_file , 'w') as f:
            f.write(f">seq\n{seq}\n")
        try:

            subprocess.run(['Fold', fasta_file, ct_file ,'-d',],
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE,
                           text=True,
                           timeout=5)
        except subprocess.TimeoutExpired:
            pass
        energy, dots, ss_string = parser_ct(ct_file)
    return energy, dots , ss_string

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


def get_processed_ids(output_file):
    Id = set()
    if os.path.exists(output_file):
        with open(output_file) as f:
            lines = f.readlines()
            for line in lines:
                part = line[0]
                Id.add(part)
    return Id

def read_input(input_path , output_path):
    results_list = []
    df_input = pd.read_csv(input_path)
    all_database_seqs = df_input["seq"].tolist()
    for index, row in df_input.iterrows():
        apt_id = row["id"]
        apt_seq = row["seq"]
        apt_len = row["L"]
        try:
            decoys = make_decoi_list(
            apt_seq, all_database_seqs, base_seed=12345 + index)

        except Exception as e:
            print(f"Error on index  {index} (ID: {apt_id}): {e}")
            decoys = []
        row_data = {
            "id": apt_id,
            "apt_seq": apt_seq,
            "length": apt_len,
            "decoy_1": decoys[0] if len(decoys) > 0 else None,
            "decoy_2": decoys[1] if len(decoys) > 1 else None,
            "decoy_3": decoys[2] if len(decoys) > 2 else None,
        }
        results_list.append(row_data)
        if (index + 1) % 50 == 0:
            temp_df = pd.DataFrame(results_list)
            temp_df.to_csv(output_path, index=False)
    final_df = pd.DataFrame(results_list)
    final_df.to_csv(output_path, index=False)
    return results_list


def prepare_3d_tasks(input_csv_path):
    df = pd.read_csv(input_csv_path)
    tasks = []
    for index, row in df.iterrows():
        id = row['id']
        apt_name = row['apt_seq']
        length = row['length']
        decoi_1 = row["decoy_1"]
        decoi_2 = row["decoy_2"]
        decoi_3 = row["decoy_3"]
        molecula = [(id , apt_name) , (id + '_dec1',decoi_1) , (id + '_dec2',decoi_2) , (id + '_dec3',decoi_3)]
        for dna in molecula:
            struct = run_rnastructure(dna[1])
            ss =struct[2]
            tasks.append((dna[0] , dna[1] , ss , length))
    return tasks


OUT_ROOT = os.path.expanduser("~/3D_DNA/apt_3d_models")
INPUT_CSV = os.path.expanduser("~/Scripts/test_scrambling.csv")
RESULTS_CSV = os.path.join(OUT_ROOT, "apt3d_results.csv")
RUN_SH = "/home/ekspert/3D_DNA/run_3dRNA_DNA/test_run_3dRNA/3dRNA/run_ss.sh"

MAX_WORKERS = 14  # Использовать 12 ядер CPU
TIMEOUT = 1800  # Таймаут 30 минут на 1 структуру (убивает висячие процессы)

JOB_PAR = """_jobid {name}
_version 2.0.0
_lib_version 3dRNA-Lib1
name {name}
seq {seq}
ss {ss}
num 1
_minimize yes
_pred_ss no
loop_building partial_bires
_mol_type dna
_rna_type linear
_routine Default
"""

def build_apt(task):
    name, seq, ss, L = task
    workdir = os.path.join(OUT_ROOT, name)
    os.makedirs(workdir, exist_ok=True)

    # Записываем конфиг job.par
    with open(os.path.join(workdir, "job.par"), "w") as f:
        f.write(JOB_PAR.format(name=name, seq=seq, ss=ss))

    cmd = f"source ~/nsp_env.sh && bash {RUN_SH} job.par > {name}.run.log 2>&1"
    t0 = time.time()

    try:
        # start_new_session=True убивает весь дерево процессов при таймауте
        p = subprocess.run(
            ["bash", "-c", cmd],
            cwd=workdir,
            timeout=TIMEOUT,
            start_new_session=True,
        )
    except subprocess.TimeoutExpired:
        subprocess.run(
            ["bash", "-c", f'pkill -9 -f "{name}.pred" 2>/dev/null; true'],
            timeout=10,
        )
        return {
            "name": name,
            "ok": False,
            "reason": f"timeout(>{TIMEOUT}s)",
            "seconds": TIMEOUT,
        }

    sec = round(time.time() - t0, 1)
    min_pdb = os.path.join(workdir, f"{name}.pred1.min.pdb")

    if not os.path.exists(min_pdb):
        return {
            "name": name,
            "ok": False,
            "reason": "no min.pdb",
            "ret": p.returncode,
            "seconds": sec,
        }

    # Проверка количества атомов
    with open(min_pdb) as f:
        atoms = sum(1 for l in f if l.startswith("ATOM"))

    if atoms < 50:
        return {
            "name": name,
            "ok": False,
            "reason": f"мало атомов: {atoms}",
            "ret": p.returncode,
            "seconds": sec,
        }

    # Проверка заряда в leap.log
    charge = None
    leap_log = os.path.join(workdir, f"{name}.pred1", "leap.log")
    if os.path.exists(leap_log):
        with open(leap_log, errors="replace") as f:
            for line in f:
                m = re.search(
                    r"unperturbed charge of the unit \((-?\d+\.?\d*)\)", line
                ) or re.search(r"[Uu]nperturbed charge[:\s]+(-?\d+\.?\d*)", line)
                if m:
                    charge = float(m.group(1))

    expected = -(L - 1)  # Одиночная цепь ДНК: -(L-1)
    ok = charge is not None and abs(charge - expected) < 1e-6

    # 🧹 ОЧИСТКА МУСОРА: Удаляем тяжелый 50 МБ файл траектории после успеха
    if ok:
        traj = os.path.join(workdir, f"{name}.traj.p1.pdb")
        try:
            if os.path.exists(traj):
                os.remove(traj)
        except OSError:
            pass

    return {
        "name": name,
        "ok": ok,
        "L": L,
        "atoms": atoms,
        "charge": charge,
        "expected": expected,
        "ret": p.returncode,
        "seconds": sec,
        "min_pdb": min_pdb if ok else "",
        "reason": "" if ok else f"заряд {charge} != {expected}",
    }
def worker(task):
    try:
        return build_apt(task)
    except Exception as e:
        return {"name": task[0], "ok": False, "reason": f"exception: {e!r}"}
def main():
    os.makedirs(OUT_ROOT, exist_ok=True)

    if not os.path.exists(INPUT_CSV):
        print(f"❌ НЕТ файла {INPUT_CSV} — сначала запусти генератор декоев!")
        sys.exit(1)

    # 1. Формируем список всех 3D-задач
    tasks = prepare_3d_tasks(INPUT_CSV)

    # Опциональный лимит для быстрой калибровки/теста
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else None
    if limit:
        tasks = tasks[:limit]
        print(f"⚠️ ВКЛЮЧЕН ЛИМИТ: берем первые {limit} задач для теста!")

    # 2. ЧЕКПОИНТ: Проверяем, что уже сделано ранее
    done = set()
    if os.path.exists(RESULTS_CSV):
        with open(RESULTS_CSV) as f:
            for row in csv.DictReader(f):
                if row.get("ok") == "True":
                    done.add(row["name"])

    todo = [t for t in tasks if t[0] not in done]
    print(f"📊 ВСЕГО задач: {len(tasks)} | Готово: {len(done)} | Осталось: {len(todo)}")

    if not todo:
        print("🎉 ВСЕ 3D-МОДЕЛИ УЖЕ ПОСТРОЕНЫ!")
        return

    new_file = (
        not os.path.exists(RESULTS_CSV) or os.path.getsize(RESULTS_CSV) == 0
    )

    # 3. МНОГОПОТОЧНЫЙ ЗАПУСК СБОРОК (12 рабочих)
    with open(RESULTS_CSV, "a", newline="") as out:
        w = csv.writer(out)
        if new_file:
            w.writerow(
                [
                    "name",
                    "ok",
                    "L",
                    "atoms",
                    "charge",
                    "expected",
                    "ret",
                    "reason",
                    "seconds",
                    "min_pdb",
                ]
            )
            out.flush()

        t0 = time.time()
        n_ok = n_bad = 0

        with ProcessPoolExecutor(max_workers=MAX_WORKERS) as ex:
            futs = {ex.submit(worker, t): t for t in todo}
            for i, fut in enumerate(as_completed(futs), 1):
                r = fut.result()
                if r.get("ok"):
                    n_ok += 1
                else:
                    n_bad += 1
                    print(
                        f"⚠️ ПРОБЛЕМА: {r.get('name')} | {r.get('reason')}",
                        flush=True,
                    )

                w.writerow(
                    [
                        r.get("name"),
                        r.get("ok"),
                        r.get("L", ""),
                        r.get("atoms", ""),
                        r.get("charge", ""),
                        r.get("expected", ""),
                        r.get("ret", ""),
                        r.get("reason", ""),
                        r.get("seconds", ""),
                        r.get("min_pdb", ""),
                    ]
                )
                out.flush()

                if i % 10 == 0 or i == len(todo):
                    sec = time.time() - t0
                    eta = sec / i * (len(todo) - i)
                    print(
                        f"[{i}/{len(todo)}] ok={n_ok} bad={n_bad} | Время: {sec/60:.1f} мин | ETA: {eta/3600:.2f} ч",
                        flush=True,
                    )

    print(
        f"\n🎉 3D-МОДЕЛИРОВАНИЕ ЗАВЕРШЕНО: {n_ok} успешно, {n_bad} с проблемами.",
        flush=True,
    )


if __name__ == "__main__":
    main()
