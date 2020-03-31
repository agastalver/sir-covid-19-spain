# COVID-19 SIR mathematical model

SIR mathematical model for infectious diseases optimized for COVID-19 using Spanish Ministry of Health public available data.

-----

![sir-cases](https://github.com/agastalver/sir-covid-19-spain/raw/master/images/generated-sir-cases.png "SIR Model Cases")

![sir](https://github.com/agastalver/sir-covid-19-spain/raw/master/images/generated-sir.png "SIR Model")

**Note**: `recovered` refers to people who has recovered from the virus or has died; as considered in the SIR model.

-----

## Last optimization

### Case forecasting table

| Date           | Infected   | Cases      |
|:--------------:|:----------:|:----------:|
| 2020-03-30     | 62664      | 86605      |
| 2020-03-31     | 64980      | 91968      |
| 2020-04-01     | 66585      | 96715      |
| 2020-04-02     | 67522      | 100854     |
| **2020-04-03** | **67857**  | **104419** |
| 2020-04-04     | 67666      | 107463     |
| 2020-04-05     | 67032      | 110044     |
| 2020-04-06     | 66035      | 112223     |
| 2020-04-07     | 64747      | 114056     |
| 2020-04-08     | 63235      | 115597     |

### Optimized SIR parameters

```
N = 125096.04181206386
beta = 0.29118710786376023
gamma = 0.047279622947446
delay = 12
```

All results are available in the folders `images` and `data`.

-----

## Last data information

### Spanish total cases

![total](https://github.com/agastalver/sir-covid-19-spain/raw/master/images/generated-total.png "Total cases")

### Spanish cases per region

![ccaa](https://github.com/agastalver/sir-covid-19-spain/raw/master/images/generated-ccaa.png "CCAA cases")

-----

## Methodology

### Data sources

Main data source:

* Spanish government: https://www.mscbs.gob.es/profesionales/saludPublica/ccayes/alertasActual/nCov-China/situacionActual.htm
  * https://covid19.isciii.es/
  * https://covid19.isciii.es/resources/serie_historica_acumulados.csv

Additional data source (for recovered people):

* https://github.com/datadista/datasets/blob/master/COVID%2019/nacional_covid19.csv

### Epidemiology model

This is based on the SIR epidemiology model proposed by W. O. Kermack and A. G. McKendrick in:

```
Kermack, W. O.; McKendrick, A. G. (1927). "A Contribution to the Mathematical Theory of Epidemics". Proceedings of the Royal Society A: Mathematical, Physical and Engineering Sciences. 115 (772): 700. Bibcode:1927RSPSA.115..700K. doi:10.1098/rspa.1927.0118. JSTOR 94815.
```

You can find the description on wikipedia: https://en.wikipedia.org/wiki/Mathematical_modelling_of_infectious_disease#The_SIR_model

### Optimization

The parameters `N`, `beta`, and `gamma`, are unknown. Additionally, a `delay` parameter is considered; defined as a time synchronization parameter in case the available data is not adjusted to day 0.

The optimization method is Nendel-Mead, adjusting mean squares on `I(t)` and `R(t)` to the available data. `S(t)` and `N` are calculated backwards.

```
Nelder, John A.; R. Mead (1965). "A simplex method for function minimization". Computer Journal. 7 (4): 308–313. doi:10.1093/comjnl/7.4.308.
```

## Usage

Execute:

```
$ python main.py
```

## Important note

The mathematical model could not adjust to the real behaviour of the virus. Furthermore, the data can have errors, delays, or be incomplete, so the adjustment can vary in the future.
