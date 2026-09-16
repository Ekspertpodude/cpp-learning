## Этапы
1. Нахождение структуры рецептора с лигандом в внеклеточной части. 
2. Подбор эпитопа связывания A2A.
3. Отбор 40 лучших фрагментов размера 3-6 нт.
4. Обучение AiDTA ; Получение 2804 аптамера длины 50-61 нт
5. Создание PDB файлов аптамеров.
6. Затем «черновой» докинг HDOCK. - **МЫ ЗДЕСЬ**
7. Отбор лучших 200 (500) и запуск «чистового» докинга HDOCK.
8. Отбор лучших 20 кандидатов и проверка через 3d_DNA.
9. Проверка с помощью HADDOCK + опционально ALphaFold3.
10. Разработка методики проверки кандидатов на связывание
11. Проверка кандидатов на афинность в лабораторных условиях.




## Используемые версии: 
    Python 3.9.25
    torch 2.8.0+cu128
    numpy 1.26.4
    pandas 2.3.1            
    scipy 1.13.1 
    RNAstructure Fold: Version 6.6 (April 2, 2026). Copyright Mathews Lab, University of Rochester.     
    Amber classic sander: Version 22.0: поля  - **leaprc.DNA.OL15**(использовали данное поле ) leaprc.DNA.OL21 leaprc.DNA.bsc1.
## HDOCK - Protein-protein and Protein-RNA/DNA Docking Huang Lab @ HUST, http://huanglab.phys.hust.edu.cn/ HDOCKlite v1.2 -- The ab initio docking engine of the HDOCK server (http://hdock.phys.hust.edu.cn/)
    Required Linux system: CentOS 6.0 or later
    This program performs the ab initio protein-protein and protein-RNA/DNA docking using
    the intrinsic scoring functions for protein-protein and protein-RNA interactions based
    on a hierarchical algorithm.
## Окружение 
    Linux Ekspert 6.18.33.2-microsoft-standard-WSL2 #1 SMP PREEMPT_DYNAMIC Thu Jun 18 21:54:43 UTC 2026 x86_64 x86_64 x86_64 GNU/Linux
    No LSB modules are available.
    Distributor ID: Ubuntu
    Description:    Ubuntu 24.04.3 LTS
    Release:        24.04
    Codename:       noble
    PRETTY_NAME="Ubuntu 24.04.3 LTS"
    NAME="Ubuntu"
    VERSION_ID="24.04"
## Мое вычислительные мощности:
        14
               total        used        free      shared  buff/cache   available
    Mem:           9.7Gi       639Mi       8.6Gi       3.5Mi       676Mi       9.1Gi
    CPU(s):                                  14
    Model name:                              AMD Ryzen 7 5800U with Radeon Graphics

## Ссылки на софт

**AiDTA** (генерация последовательностей, MCTS)

- Код: `https://github.com/Fudan-HQLab/AiDTA`
- Препринт: `https://www.biorxiv.org/content/10.1101/2025.06.01.657174`

**RNAstructure** (предсказание 2D: `Fold`, `ct2dot`, `MaxExpect`, `ProbKnot`)

- `http://rna.urmc.rochester.edu/RNAstructure.html` — страница лаборатории Mathews, оттуда и бинарники, и исходники [1](https://doaj.org/article/d226b051263c4c74bd8581cbed44aae5) [5](https://link.springer.com/article/10.1186/1471-2105-11-129)
- Статья: Reuter & Mathews, _BMC Bioinformatics_ 11:129 (2010), `https://doi.org/10.1186/1471-2105-11-129`
- Лицензия GPL v2

**3dRNA/DNA + NSP** (сборка 3D)

- `http://biophy.hust.edu.cn/new/resources/3dRNA` — раздел ресурсов, там же локальная версия и NSP [3](https://www.sciencedirect.com/science/article/abs/pii/S0022283624003516)
- Сервер: `http://biophy.hust.edu.cn/new/3dRNA`
- Статья: Zhang, Xiong, Yang, Xiao. _J Mol Biol_ 436(17):168742 (2024), `https://doi.org/10.1016/j.jmb.2024.168742`
- Метод 3dDNA: _Molecules_ 27(18):5936 (2022), `https://doi.org/10.3390/molecules27185936` [2](https://www.mdpi.com/1420-3049/27/18/5936)
- Код и данные продублированы на Zenodo — ссылка в разделе Availability статьи [3](https://www.sciencedirect.com/science/article/abs/pii/S0022283624003516)

**AmberTools** (tleap, sander/msander, ambpdb)

- `https://ambermd.org/GetAmber.php` — AmberTools бесплатен, регистрация обязательна
- Мануалы: `https://ambermd.org/Manuals.php`
- У тебя **AmberClassic** — отдельная сборка, оттуда же

**HDOCKlite** (докинг)

- `http://hdock.phys.hust.edu.cn/` — веб-сервер
- `http://huanglab.phys.hust.edu.cn/software/hdocklite/` — локальная версия, по запросу для академического использования
- Справка по формуле confidence: `http://hdock.phys.hust.edu.cn/help.php`


