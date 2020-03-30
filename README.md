# COVID-19 SIR mathematical model

Modelo matemático SIR optimizado con los datos de COVID-19 del Ministerio de Salud en España.

-----

## Última optimización (2020-03-30)

Los resultados están disponibles en las carpetas `images` y `data`.

### Gráfica de casos

![total](https://github.com/agastalver/sir-covid-19-spain/raw/master/images/generated-total.png "Total cases")

### Gráfica de predicción

![sir model](https://github.com/agastalver/sir-covid-19-spain/raw/master/images/generated-sir.png "SIR Model")

### Optimización

```
N = 226135.58759394957
beta = 0.301632016967233
gamma = 0.09679570331035678
delay = +9
```

## Información del método

### Datos

Disponibles en https://covid19.isciii.es/

O desde el enlace directo: https://covid19.isciii.es/resources/serie_historica_acumulados.csv

### Modelo SIR

Basado en el modelo propuesto por W. O. Kermack y A. G. McKendrick:

```
Kermack, W. O.; McKendrick, A. G. (1927). "A Contribution to the Mathematical Theory of Epidemics". Proceedings of the Royal Society A: Mathematical, Physical and Engineering Sciences. 115 (772): 700. Bibcode:1927RSPSA.115..700K. doi:10.1098/rspa.1927.0118. JSTOR 94815.
```

Descrito también en wikipedia: https://en.wikipedia.org/wiki/Mathematical_modelling_of_infectious_disease#The_SIR_model

### Optimización

Se supone como desconocido los parámetros N, beta, gamma. Adicionalmente se supone que el modelo puede comenzar en un día anterior o posterior a los datos disponibles.

El método de optimización es Nendel-Mead, ajustando mínimos cuadrados con respecto a los datos disponibles:

```
Nelder, John A.; R. Mead (1965). "A simplex method for function minimization". Computer Journal. 7 (4): 308–313. doi:10.1093/comjnl/7.4.308.
```

## Ejecución

Ejecutar el archivo main.py con python.

```
$ python main.py
```

## Aviso

Se trata de un modelo matemático que podría no ajustarse al comportamiento real del virus. Además, dado que los datos pueden sufrir errores o retrasos en la información, es posible que el ajuste cambie en el futuro.
