# SegFormer

## Koraci

### Potrebne instalacije

**Korak 1.** Instalirajte [MMCV](https://github.com/open-mmlab/mmcv) koristeći [MIM](https://github.com/open-mmlab/mim).

```shell
pip install -U openmim
mim install mmengine
mim install "mmcv>=2.0.0"
```

**Korak 2.** Instalirajte MMSegmentation.

Ako razvijate i pokrećete mmseg direktno, MMSegmentation instalirajte sa ovog izvora:

```shell
git clone -b main https://github.com/open-mmlab/mmsegmentation.git
cd mmsegmentation
pip install -v -e .
# '-v' means verbose, or more output
# '-e' means installing a project in editable mode,
# thus any local modifications made to the code will take effect without reinstallation.
```

Ako koristite mmsegmentation kao dependency ili uključujete kao paket, MMSegmentation instalirajte pomoću pip-a:
```shell
pip install "mmsegmentation>=1.0.0"
```



### Priprema podataka

**Struktura**
Direktorij s podacima postavite u `$MMSEGMENTATION/data` tako da je Vaš mmsegmentation direktorij građen ovako:

```none
mmsegmentation
├── mmseg
├── tools
├── configs
├── data
│   ├── podaci
```

**Cityscapes**

Sa https://www.synapse.org/#!Synapse:syn3193805/files/ preuzmite skup slika i segmentacijskih maski.

Kako biste podijelili podatke u set za učenje (18 skenova) i validaciju (12 skenova) po uzoru na [TransUNet](https://arxiv.org/abs/2102.04306), pokrenite slijedeći kod:

```shell
unzip RawData.zip
cd ./RawData/Training
```
Stvorite `train.txt` i `val.txt` kako biste podijelili skup prema uputama.
Prema specifikaciji  TransUneta podatke treba podijeliti na slijedeći način:

train.txt
```none
img0005.nii.gz
img0006.nii.gz
img0007.nii.gz
img0009.nii.gz
img0010.nii.gz
img0021.nii.gz
img0023.nii.gz
img0024.nii.gz
img0026.nii.gz
img0027.nii.gz
img0028.nii.gz
img0030.nii.gz
img0031.nii.gz
img0033.nii.gz
img0034.nii.gz
img0037.nii.gz
img0039.nii.gz
img0040.nii.gz
```

val.txt
```none
img0008.nii.gz
img0022.nii.gz
img0038.nii.gz
img0036.nii.gz
img0032.nii.gz
img0002.nii.gz
img0029.nii.gz
img0003.nii.gz
img0001.nii.gz
img0004.nii.gz
img0025.nii.gz
img0035.nii.gz
```

Sadržaj Synapse skupa bi trebao izgldati ovako:

```none
├── Training
│   ├── img
│   │   ├── img0001.nii.gz
│   │   ├── img0002.nii.gz
│   │   ├── ...
│   ├── label
│   │   ├── label0001.nii.gz
│   │   ├── label0002.nii.gz
│   │   ├── ...
│   ├── train.txt
│   ├── val.txt
```

Pokrenite slijedeći kod kako biste pripremili podatke tako da odgovaraju mmsegmentation obliku.

```shell
python tools/dataset_converters/synapse.py --dataset-path /putanja/do/synapse
```none

```

### Učenje

Kako biste pokrenuli učenje modela pokrenite slijedeći kod:

```shell
python tools/train.py  ${KONFIGURACIJSKA_DATOTEKA} 
```
Za vrijeme učenja u direktoriju mmsegmentation/work_dirs stvorit će se direktorij sa datotekama sa naučenim težinama(datoteke koje završavaju sa .pth), python konfiguracijska datoteka, zadnja spremljena točka i dodatni direktorij sa izmjerenim gubitcima i metrikama u obliku JSON datoteke.

### Validacija

Kako biste validirali naučeni model pokrenite slijedeći kod:

```shell
python tools/test.py ${KONFIGURACIJSKA_DATOTEKA} ${CHECKPOINT_DATOTEKA.pth} 
```

### Konfiguracijska datoteka

**20000 iteracija, nasumično incijalizirane težine**

Korišten je Adam optimizator, a stopa učenja se kroz prvih 0.9% od ukupnog broja iteracija linearno povećava od 1e-6 do 0.00006, te se zatim do kraja treninga polinomijalno smanjuje do minimalne vrijednosti 0.0. Za prigušenje težina (eng. weight decay) postavljena je vrijednost 0.01, a kao funkcija gubitka korištena je unakrsna entropija. Koder se sastoji od 4 transformerska bloka te su veličine okna u svakom od blokova redom 7, 3, 3, 3. Pomak kod ugrađivanja okna je redom 4, 2, 2, 2, a broj kanala izlaza 32, 64, 160, 256. Broj slojeva kodera je redom 2, 2, 2, 2 u transformerskim blokovima, omjer smanjenja (eng. reduction ratio) 8, 4, 2, 1,a broj glava u slojevima samopažnje 1, 2, 5, 8. Postotak ispuštenih neurona (eng. dropout ratio) 0.1. Model se trenira kroz 20000 ieracija uz veličinu grupe 2. Težine su nasumično inicijalizirane.

Pripremljenu konfiguracijsku datoteku za učenje SegFormera na Synapse skupu prema opisanim specifikacijama možete preuzeti [odavde](https://github.com/pecra/Zavrsni/blob/main/segformer-synapse.py).

**20000 iteracija, težine inicijalizirane treniranjem na ImageNetu**

Korišten je Adam optimizator, a stopa učenja se kroz prvih 0.9% od ukupnog broja iteracija linearno povećava od 1e-6 do 0.00006, te se zatim do kraja treninga polinomijalno smanjuje do minimalne vrijednosti 0.0. Za prigušenje težina (eng. weight decay) postavljena je vrijednost 0.01, a kao funkcija gubitka korištena je unakrsna entropija. Koder se sastoji od 4 transformerska bloka te su veličine okna u svakom od blokova redom 7, 3, 3, 3. Pomak kod ugrađivanja okna je redom 4, 2, 2, 2, a broj kanala izlaza 32, 64, 160, 256. Broj slojeva kodera je redom 2, 2, 2, 2 u transformerskim blokovima, omjer smanjenja (eng. reduction ratio) 8, 4, 2, 1,a broj glava u slojevima samopažnje 1, 2, 5, 8. Postotak ispuštenih neurona (eng. dropout ratio) 0.1. Model se trenira kroz 20000 ieracija uz veličinu grupe 2. Težine su inicijalizirane treniranjem na ImageNetu.

Pripremljenu konfiguracijsku datoteku za učenje SegFormera na Synapse skupu prema opisanim specifikacijama možete preuzeti [odavde](https://github.com/pecra/Zavrsni/blob/main/segformer-synapse1.py).

**80000 iteracija, nasumično incijalizirane težine**

Korišten je Adam optimizator, a stopa učenja se kroz prvih 0.9% od ukupnog broja iteracija linearno povećava od 1e-6 do 0.00006, te se zatim do kraja treninga polinomijalno smanjuje do minimalne vrijednosti 0.0. Za prigušenje težina (eng. weight decay) postavljena je vrijednost 0.01, a kao funkcija gubitka korištena je unakrsna entropija. Koder se sastoji od 4 transformerska bloka te su veličine okna u svakom od blokova redom 7, 3, 3, 3. Pomak kod ugrađivanja okna je redom 4, 2, 2, 2, a broj kanala izlaza 32, 64, 160, 256. Broj slojeva kodera je redom 2, 2, 2, 2 u transformerskim blokovima, omjer smanjenja (eng. reduction ratio) 8, 4, 2, 1,a broj glava u slojevima samopažnje 1, 2, 5, 8. Postotak ispuštenih neurona (eng. dropout ratio) 0.1. Model se trenira kroz 80000 ieracija uz veličinu grupe 4. Težine su inicijalizirane nasumično.

Pripremljenu konfiguracijsku datoteku za učenje SegFormera na Synapse skupu prema opisanim specifikacijama možete preuzeti [odavde](https://github.com/pecra/Zavrsni/blob/main/segformer-synapse2.py).

### Težine za inicijalizaciju

Težine za inicijalizaciju SegFormer-B0 dobivene treniranjem na ImageNetu od strane [autora](https://arxiv.org/abs/2105.15203) modela  mogu se preuzeti korištene u službenom [repozitoriju](https://github.com/NVlabs/SegFormer) mogu se preuzeti [odavde](https://drive.google.com/drive/folders/1b7bwrInTW4VLEm27YawHOAMSMikga2Ia). Kako biste mogli koristiti te težine potrebno je u mmsegmentation stvoriti direktorij pretrain i u njega dodati preuzetu datoteku.

### Validacija SegFormera na Cityscapes

Za validaciju SegFormera na Cityscapes skupu koji je prethodno treniran od strane [autora](https://arxiv.org/abs/2105.15203) modela preuzeti težine dobivene nakon učenja [odavde](https://download.openmmlab.com/mmsegmentation/v0.5/segformer/segformer_mit-b0_8x1_1024x1024_160k_cityscapes/segformer_mit-b0_8x1_1024x1024_160k_cityscapes_20211208_101857-e7f88502.pth) i pokrenuti validaciju kao što je opisano iznad.

### Pregled rezultata

**Vizualizacija maske predviđanja i stvarne maske**

Za vizualizaciju maske predviđanja i stvarne segmentacijske maske u _base_/schedules/schedule_20k.py (kod treninga kroz 80000 iteracija _base_/schedules/schedule_80k.py) konfiguracijskoj datoteci postaviti:

```shell
default_hooks = dict(
    timer=dict(type='IterTimerHook'),
    logger=dict(type='LoggerHook', interval=50, log_metric_by_epoch=False),
    param_scheduler=dict(type='ParamSchedulerHook'),
    checkpoint=dict(type='CheckpointHook', by_epoch=False, interval=2000),
    sampler_seed=dict(type='DistSamplerSeedHook'),
    visualization=dict(type='SegVisualizationHook', draw=True, interval=1))

```
i pokrenuti validaciju. Prilikom validacije će se stvoriti vis_image direktorij unutar $WORK_DIRS/vis_data u kojem će biti pohranjene segmentacijske maske.

**Graf dice vrijednosti kroz trening**

Nakon završenog učenja pokrenuti slijedeći kod tako da log.json bude putanja do datoteke sa gubitcima i metrikama mjerenih za vrijeme treninga koji se nalazi u work_dirs:

```shell
python tools/analysis_tools/analyze_logs.py ${log.json} --keys mDice --legend mDice

```
Naredba iscrtava graf koji prikazuje vrijednosti dice koeficijenta od početka do kraja treninga.

**Mjerenje brzine obrade slike**

Za mjerenje brzine obrade ulaznih podataka u fps(broj slika / sekunda) pokrenuti naredbu:

```shell
python tools/benchmark.py ${PUTANJA_DO_KONFIGURACIJSKE_DATOTEKE} ${PUTANJA_DO_TEZINA_MODELA_NAKON_UCENJA}

```
