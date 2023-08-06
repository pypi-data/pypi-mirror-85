#!/usr/bin/python
"""Basic settings"""

import scipy as sp

__date__ = 'October 22, 2018'

# number of instances per parameter setting
NO_TRIALS = 2

# division rate of every ~7 days for lung cancers (Rew & Wilson, European Journal of Surgical Oncology 2000)
BIRTH_RATE = 0.14

# division rate of every 4 days is typical for colorectal cancers (Jones et al, PNAS 2008) and
# BIRTH_RATE = 0.25

# early PDA (Klein et al, 2002, Yachida et al, Nature 2010)
# 144 days is median doubling time of PDA PT (Furukawa et al, 2001)
# BIRTH_RATE = 1 / 2.3   # typical for PDA mets, Yachida et al, Nature 2010: 0.435

# median doubling time of stage I lung cancer is 181 days (Winer-Muram et al, Radiology 2002)
# leads to a growth rate of r = ln(2) / 181 = ~0.4% and hence d = 0.136
DEATH_RATE = 0.136

# median doubling time of stage relapsed lung cancer is 29 days (Sharouni et al, British Journal of Cancer 2003)
# leads to a growth rate of r = ln(2) / 29 = ~2% and hence d = 0.12

# typical growth rate of early colorectal cancers is ~0.5% per day
# DEATH_RATE = 0.245

# primary tumor detection size where biomarker (ctDNA) level is evaluated
PT_DETSIZE = [1e9]

# half life of cfDNA and ctDNA: Wan et al., Nature Reviews Cancer, 2017
T12_MINS = 30

# Heitzer et al, Nature Reviews Genetics, 2019
DIPLOID_GE_WEIGHT_ng = 0.0066   # average yield of a nucleated cell is 6.6 pg of DNA

# default shedding probability per dell death inferred from Chabon et al, Nature 2020 and Abbosh et al, Nature 2017
# 0.24 genome equivalents per cm^3 at the above calculated death rate of d=0.136
Q_D_LUNG = 1.4e-4

# amount of blood per human
BLOOD_AMOUNT = 5.0   # [liters]

# fraction of plasma in blood
PLASMA_FRACTION = 0.55

# 15 ml liquid biopsy sampling tube size (Cohen et al, Science 2018)
# 30 ml is possible (McDonald, STM 2019)
TUBE_SIZE = 0.015  # [liters]

# primary tumor size when a cancer becomes diagnosed due to symptoms
DIAGNOSIS_SIZE = 2.25e10   # median lung cancer detection size in SEER data

# sequencing panel size for virtual detection
CAPPSEQ_SIZE = 300000    # CAPP-Seq covers 302,620 bases according to Newman et al, Nature Biotechnology 2016
CANCERSEEK_SIZE = 2000   # CancerSeek covers 2,001 bases according to Cohen et al, Science 2018
PANEL_SIZE = CANCERSEEK_SIZE

# base sequencing error rate
# 1.1e-4 McDonald et al, STM 2019
# 1.5e-5 Newman et al, Nature Biotechnology 2016
# 2e-6 Wan et al, STM 2020
# 3e-7 Phallen et al, STM 2017
SEQUENCING_ERROR_RATE = 1.0e-5

# fraction of molecules in sample that get sequenced; perhaps as low as 50% (Chabon et al, Nature 2020)
SEQUENCING_EFFICIENCY = 0.5

# default output directory
OUTPUT_DIR_NAME = 'output'

# parameter values to mimic distribution of plasma DNA concentrations
# based on a Gamma distribution to capture overdispersion
# fitted to data of stage 1 cancers in Cohen et al, Science 2018 with fit argument floc=0
# mean 6.287e+00, median 5.203e+00 ng/mL
# mean 953 hGE per plasma mL
FIT_GAMMA_PARAMS = {
    'shape': 1.86,
    'location': 0.0,
    'scale': 3.38
}

FIT_BETA_PARAMS = {
    'alpha': 1.84,
    'beta': 1.56e10,
    'loc': 0.0,
    'scale': 5.34e10
}

# growth rate of pancreatic cancers according to Furukawa et al., 2001: 0.0048
# death rate is calculated from the given doubling time and the birth rate
# 144 days is median doubling time of PDA PT (Furukawa et al, 2001)
# 159 days is mean doubling time of PDA PT (Furukawa et al, 2001)
DT_PDA_PT = 144
# growth rate of pancreatic cancer mets according to Amikura et al, 2001: 0.0123
DT_PDA_MET = 56       # median doubling time in PDA mets (Amikura et al, 1995)

# ####### DYNAMICS MODE ########
# approximate growth of tumor after it reaches a threshold
EXACT_THRESHOLD = 1e4

# output dynamics file resolution [days]
# if biomarker changes are sufficient (at most one per day), set to None
DYN_OUTPUT_RESOLUTION = 1.0
