# COVID-19 SIR mathematical model

SIR mathematical model for infectious diseases optimized for COVID-19 using Spanish Ministry of Health public available data.

-----

## Last optimization (2020-03-30)

![sir](https://github.com/agastalver/sir-covid-19-spain/raw/master/images/generated-sir.png "SIR Model")

**Note**: `recovered` refers to people who has recovered from the virus or has died; as considered in the SIR model.

### Case forecasting

![sir-cases](https://github.com/agastalver/sir-covid-19-spain/raw/master/images/generated-sir-cases.png "SIR Model Cases")

### Case forecasting table

| Date           | Cases      | Infected   |
|:--------------:|:----------:|:----------:|
| 2020-03-30     |  94534     | 55249      |
| 2020-03-31     | 104310     | 59423      |
| 2020-04-01     | 113954     | 63082      |
| 2020-04-02     | 123300     | 66116      |
| 2020-04-03     | 132207     | 68448      |
| 2020-04-04     | 140569     | 70044      |
| 2020-04-05     | 148316     | 70904      |
| **2020-04-06** | **155409** | **71062**  |
| 2020-04-07     | 161841     | 70574      |
| 2020-04-08     | 167626     | 69517      |

### Optimized SIR parameters

```
N = 226135.58759394957
beta = 0.301632016967233
gamma = 0.09679570331035678
delay = +9
```

All results are available in the folders `images` and `data`.

## Last data information

### Spanish total cases

![total](https://github.com/agastalver/sir-covid-19-spain/raw/master/images/generated-total.png "Total cases")

### Spanish cases per region

![ccaa](https://github.com/agastalver/sir-covid-19-spain/raw/master/images/generated-ccaa.png "CCAA cases")

## Methodology

### Data

Disponibles en https://covid19.isciii.es/

O desde el enlace directo: https://covid19.isciii.es/resources/serie_historica_acumulados.csv

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
