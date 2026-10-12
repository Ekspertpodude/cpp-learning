#!/usr/bin/env python3
# step1_scrambler_repair.py — пакет негативного контроля (scramble-декои), 3D-маршрут:
#   nsp assemble (чистый 3D_DNA, ~30 c) -> repair_one() из repair_ss.py
#   (одна цепь 1..L, tleap-мостики OL15, минимизация 2000/1000,
#    приёмка КАЖДОЙ задачи: заряд == -(L-1), стыки O3'..O5' <= 3.05 A)
# Отличия от исходного step1_scrambler.py (все помечены "# ИЗМЕНЕНО"):
#   1) сборка через assemble + repair_one вместо тяжёлого run_ss.sh
#      (приёмка по стыкам — у run_ss.sh её не было, разрывы хребта проходили мимо);
#   2) parser_ct всегда возвращает 3 значения (убегает от ValueError при пустом .ct);
#   3) prepare_3d_tasks пропускает пустые декои (раньше в fasta улетала строка "None");
#   4) main пишет apt_tasks.csv (id,seq,ss,L) — мост к dock_apt.py;
#   5) MAX_WORKERS=12 при nproc=14.
# Вход:  ~/Scripts/test_scrambling.csv (id,apt_seq,length,decoy_1..3) — ОЧИЩЕННЫЙ!
# Выход: ~/3D_DNA/apt_3d_models/<name>/… + apt_tasks.csv + apt3d_results.csv
# Запуск:  conda activate aidta            (Fold/DATAPATH нужны для 2D)
#          python3 step1_scrambler_repair.py 4     # дым: 1 аптамер + 3 его декоя
#          python3 step1_scrambler_repair.py       # вся партия
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

# ИЗМЕНЕНО (1): ремонтная приёмка из проверенного repair_ss.py — не копипастим,
# а импортируем, чтобы правила приёмки жили в одном месте.
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from repair_ss import repair_one  # noqa: E402


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
        return 0.0, 0, ""  # ИЗМЕНЕНО (2): всегда 3 значения — распаковка ниже не падает
    index_energy = None
    with open(path) as f:
        lines = f.readlines()
        heading = lines[0].split()
        num_of_dots = 0
        for i in range(len(heading)):
            if (heading[i] == '='):
                index_energy = i + 1
        # ИЗМЕНЕНО (6): .ct от Fold содержит НЕСКОЛЬКО структур подряд
        # (МФЕ + субоптимальные в энергетическом окне). Читаем ТОЛЬКО первый
        # блок из n_lin строк, иначе ss склеивается в k*L и assemble падает
        # с "length of the sequence should equal to the length of the SS".
        n_lin = int(heading[0])
        parsed = 0
        for line in lines[1:]:
            if parsed >= n_lin:
                break
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
                parsed += 1

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
            pass    # НБ: при таймауте .ct нет -> вернётся (0.0, 0, "") — без падения,
                    # но ss будет пустой; для 2D-задач это отловится пустой ss.
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
            # ИЗМЕНЕНО (3): пустая/отсутствующая последовательность пропускается,
            # а не превращается в fasta со строкой "None"
            if not isinstance(dna[1], str) or not dna[1]:
                print(f"⚠️ {dna[0]}: пустая последовательность — задача пропущена")
                continue
            struct = run_rnastructure(dna[1])
            ss =struct[2]
            if not ss:
                # ИЗМЕНЕНО (3): пустая ss (таймаут Fold) — не создаём битую задачу
                print(f"⚠️ {dna[0]}: Fold вернул пустую ss — задача пропущена")
                continue
            tasks.append((dna[0] , dna[1] , ss , length))
    return tasks


OUT_ROOT = os.path.expanduser("~/3D_DNA/apt_3d_models")
INPUT_CSV = os.path.expanduser("~/Scripts/test_scrambling.csv")
RESULTS_CSV = os.path.join(OUT_ROOT, "apt3d_results.csv")
# ИЗМЕНЕНО (4): мост к dock_apt.py — он ждёт задачи именно в таком файле
TASKS_CSV = os.path.join(OUT_ROOT, "apt_tasks.csv")
# ИЗМЕНЕНО (1): вместо RUN_SH (run_ss.sh) — прямой вызов чистого assemble
NSP_BIN = "/home/ekspert/3D_DNA/home/yiduo/3dRNA/NSP/cirRNA_and_DNA/nsp"

MAX_WORKERS = 12  # ИЗМЕНЕНО (5): nproc=14 → 12 в счёт, 2 системе/Fold
TIMEOUT_ASS = 1800  # Потолок на assemble (норма ~30 c), от зависших процессов

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

# ИЗМЕНЕНО (1): тело сборки — боевой быстрый маршрут, сигнатура результата прежняя
def build_apt(task):
    name, seq, ss, L = task
    workdir = os.path.join(OUT_ROOT, name)
    os.makedirs(workdir, exist_ok=True)

    # Записываем конфиг job.par (шаблон с обязательной пустой строкой в конце)
    with open(os.path.join(workdir, "job.par"), "w") as f:
        f.write(JOB_PAR.format(name=name, seq=seq, ss=ss))

    t0 = time.time()
    # Шаг 1: чистый assemble 3D_DNA.
    # start_new_session=True: при таймауте убивается вся группа процессов.
    try:
        p = subprocess.run(
            ["bash", "-c",
             f"source ~/nsp_env.sh && {NSP_BIN} assemble -par job.par "
             f'-ss "{ss}" -t DNA > {name}.assemble.log 2>&1'],
            cwd=workdir,
            timeout=TIMEOUT_ASS,
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
            "reason": f"timeout assemble (>{TIMEOUT_ASS}s)",
            "seconds": TIMEOUT_ASS,
        }
    if p.returncode != 0:
        return {
            "name": name,
            "ok": False,
            "reason": f"assemble rc={p.returncode} (см. {name}.assemble.log)",
            "ret": p.returncode,
        }
    pred = os.path.join(workdir, f"{name}.pred1.pdb")
    if not os.path.exists(pred):
        return {
            "name": name,
            "ok": False,
            "reason": "assemble без pred1.pdb",
            "ret": p.returncode,
        }
    ass_sec = time.time() - t0

    # Шаг 2: ремонт хребта + минимизация 2000/1000 + приёмка
    # (заряд == -(L-1) И стыки O3'..O5' <= 3.05 A) — всё внутри repair_one.
    r = repair_one(name, seq, pred, workdir)
    r["seconds"] = round(r.get("seconds", 0) + ass_sec, 1)
    r["ret"] = p.returncode
    if not r.get("ok"):
        r["min_pdb"] = ""
    return r

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

    # ИЗМЕНЕНО (4): дублируем задачи в apt_tasks.csv (id,seq,ss,L) —
    # именно в таком виде их потом подхватит dock_apt.py
    with open(TASKS_CSV, "w", newline="") as tf:
        w = csv.writer(tf)
        w.writerow(["id", "seq", "ss", "L"])
        w.writerows(tasks)

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

    # 3. МНОГОПОТОЧНЫЙ ЗАПУСК СБОРОК
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
