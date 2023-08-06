# MHCLovac

MHC class I binding and epitope prediction based on modeled physicochemical properties of peptides.

### Disclaimer
MHCLovac is a result of my personal interests and some free time. 
It is **not** a result of thorough scientific research. 
That said, MHCLovac is not too bad in terms of predictions it makes and I plan to improve it further if possible.

### What's new?
* **version 3.0**
  * epitope prediction.
  * ic50 predictions are replaced with binding score. The higher the score the stronger the binding.
  * single prediction algorithm replaced with collection of algorithms, prediction consensus.

### About
MHCLovac is a command line tool used for MHC Class I binding and epitope prediction. 
It uses modeled physicochemical properites of target peptides to predict binding and epitope scores. 
The modeling is accomplished using [proteinko](https://pypi.org/project/proteinko/) python package (also my work). 
MHCLovac is not constrained by the length of target peptide sequence and is capable of making predictions for peptides of any length. 
Prediction is carried out by a collection of regression and classification algorithms.
Algos are trained on data obtained from two sources: 
dataset used for retraining the IEDB class I binding prediction tools [http://tools.iedb.org/static/main/binding_data_2013.zip](http://tools.iedb.org/static/main/binding_data_2013.zip) 
and IEDB database ([www.iedb.org](www.iedb.org)). 

Training results and a list of supported MHC alleles is available in [training/results](training/results) folder.

Trained models are benchmarked using ROC-AUC method. 
Benchmarking method is explained in [benchmark](benchmark) folder.

![roc/auc](https://gitlab.com/stojanovicbg/mhclovac/-/raw/master/benchmark/results/ROC.png)

### Installation

```
pip install mhclovac
```

### Example usage
```
mhclovac -f example.fasta -m HLA-B*44:02 -l 11
```

### Example output
```
 sequence          mhc  peptide_length           sequence_name  binding_score  epitope_score  combined_score
 MEIFIEVFSHF  HLA-B*44:02              11  MEIFIEVFSHF HLA-B44:02       0.523205       0.965484        1.488688
 EIFIEVFSHFL  HLA-B*44:02              11  MEIFIEVFSHF HLA-B44:02       0.087188       0.512132        0.599320
 IFIEVFSHFLL  HLA-B*44:02              11  MEIFIEVFSHF HLA-B44:02       0.039142       0.159362        0.198503
 FIEVFSHFLLQ  HLA-B*44:02              11  MEIFIEVFSHF HLA-B44:02       0.114877       0.264553        0.379430
 IEVFSHFLLQL  HLA-B*44:02              11  MEIFIEVFSHF HLA-B44:02       0.317922       0.964168        1.282090
```

Columns:
1. `sequence` 
2. `sequence_name` - Fasta sequence name or name provided by `-n` argument
3. `peptide_length`
4. `mhc` - MHC allele
5. `binding_score` - Higher score means better binding
6. `epitope_score` - Higher score means a better epitope
7. `combined_score` - Sum of binding and epitope scores if both are available

### Donate to support my work
This work is done on my own budget so if you like you can support me by donating Bitcoin. 
Any amount donated will be appreciated. 
Thank you! 

BTC: bc1qrg7wku5g35kn0qyay4uwzugfmfqwnvz95g54pj
