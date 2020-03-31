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
| 2020-03-31     | 66754      | 94391      |
| 2020-04-01     | 68754      | 99677      |
| 2020-04-02     | 70055      | 104345     |
| 2020-04-03     | 70709      | 108412     |
| **2020-04-04** | **70786**  | **111920** |
| 2020-04-05     | 70366      | 114923     |
| 2020-04-06     | 69530      | 117478     |
| 2020-04-07     | 68354      | 119644     |
| 2020-04-08     | 66908      | 121477     |
| 2020-04-09     | 65254      | 123026     |

### Optimized SIR parameters

```
N = 133090.46896526567
beta = 0.28572994333788726
gamma = 0.04803540389938131
delay = 13
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
