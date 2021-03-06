import os
import requests

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from scipy import optimize
from scipy.integrate import odeint

if not os.path.exists("data"):
    os.makedirs("data")

if not os.path.exists("images"):
    os.makedirs("images")

# download file

url = "https://covid19.isciii.es/resources/serie_historica_acumulados.csv"
s = requests.get(url).text

url2 = "https://raw.githubusercontent.com/datadista/datasets/master/COVID%2019/nacional_covid19.csv"
s2 = requests.get(url2).text

# save file

fn = os.path.join("data","serie_historica_acumulados.csv")
with open(fn, "w") as f:
    f.write(s)

fn2 = os.path.join("data","nacional_covid19.csv")
with open(fn2, "w") as f2:
    f2.write(s2)

# read file

df = pd.read_csv(fn, encoding="latin1")
df2 = pd.read_csv(fn2)

# prepare

df = df[:-8]
df = df.fillna(0)
df.columns = ["ccaa", "date", "cases", "pcr", "ac", "hospitalized", "uci", "dead", "recovered"]
df["date"] = pd.to_datetime(df["date"], format="%d/%m/%Y", infer_datetime_format=True)

df2.columns = ["date", "cases", "pcr", "ac", "recovered", "dead", "uci", "hospitalized"]
df2["date"] = pd.to_datetime(df2["date"], format="%Y-%m-%d")
df2 = df2.set_index("date").resample("D").interpolate().fillna(0)

#dft = df[["date", "cases", "pcr", "ac", "hospitalized", "uci", "dead", "recovered"]].groupby("date").sum()
dft = df2
dft = dft.fillna(0)

dfto = dft.copy()

#dft = dft.fillna(0)
#dft["cases"] = dft["cases"] + dft["pcr"] + dft["ac"]
dfpct = 100*dft["dead"]/dft["cases"]
dft["recovered"] = dft["recovered"] + dft["dead"] # as SIR model defines
dft["infected"] = dft["cases"] - dft["recovered"]

# optimization SIR

inf0 = dft["infected"].values[0]
rec0 = dft["recovered"].values[0]
days = len(dft)

def sir(N, beta, gamma, days):
    I0 = inf0
    R0 = rec0
    S0 = N - I0 - R0

    def deriv(y, t, N, beta, gamma):
        S, I, R = y
        dSdt = -beta * S * I / N
        dIdt = beta * S * I / N - gamma * I
        dRdt = gamma * I
        return dSdt, dIdt, dRdt
    
    t = np.linspace(0, days, days)
    y0 = S0, I0, R0
    ret = odeint(deriv, y0, t, args=(N, beta, gamma))
    S, I, R = ret.T

    return S, I, R

def sir_lockdown(N, beta, gamma, days, delta, epsilons, lckday1, lckday2s, lckday3):
    I0 = inf0
    R0 = rec0
    S0 = N - I0 - R0

    def deriv(y, t, N, beta, gamma, delta):
        S, I, R = y
        dSdt = -beta * delta * S * I / N
        dIdt = beta * delta * S * I / N - gamma * I
        dRdt = gamma * I
        return dSdt, dIdt, dRdt
    
    t = np.linspace(0, days, days)

    y0 = S0, I0, R0
    t0 = t[:min(lckday1+1, days)]
    ret = odeint(deriv, y0, t0, args=(N, beta, gamma, 1))
    S, I, R = ret.T

    if lckday1 < days:
        y1 = S[-1], I[-1], R[-1]
        t1 = t[lckday1:min(lckday2s[0]+1, days)]
        ret = odeint(deriv, y1, t1, args=(N, beta, gamma, delta))
        S1, I1, R1 = ret.T
        S, I, R = np.concatenate((S, S1[1:])), np.concatenate((I, I1[1:])), np.concatenate((R, R1[1:]))

    for idx, lckday2 in enumerate(lckday2s):
        if lckday2 < days:
            y2 = S[-1], I[-1], R[-1]
            lckday2e = lckday3 if idx == (len(lckday2s)-1) else lckday2s[idx+1]
            t2 = t[lckday2:min(lckday2e+1, days)]
            ret = odeint(deriv, y2, t2, args=(N, beta, gamma, epsilons[idx]))
            S2, I2, R2 = ret.T
            S, I, R = np.concatenate((S, S2[1:])), np.concatenate((I, I2[1:])), np.concatenate((R, R2[1:]))

    if lckday3 < days:
        y3 = S2[-1], I2[-1], R2[-1]
        t3 = t[lckday3:]
        ret = odeint(deriv, y3, t3, args=(N, beta, gamma, 1))
        S3, I3, R3 = ret.T
        S, I, R = np.concatenate((S, S3[1:])), np.concatenate((I, I3[1:])), np.concatenate((R, R3[1:]))

    return S, I, R

def fdelay(delay):
    def f(x):
        N = x[0]
        beta = x[1]
        gamma = x[2]
        days = len(dft)
        S, I, R = sir(N, beta, gamma, days + delay)
        S, I, R = S[delay:delay+days], I[delay:delay+days], R[delay:delay+days]
        Io, Ro = dft["infected"].values, dft["recovered"].values
        #So = N - Io
        #loss = ((S - So)**2).sum()/days + ((I - Io)**2).sum()/days + ((R - Ro)**2).sum()/days
        loss = ((I - Io)**2).sum()/days + ((R - Ro)**2).sum()/days
        return loss

    result = optimize.minimize(f, [100000, 0.5, 0.05], method="Nelder-Mead")

    return result

def fdelay_lockdown(delay, lckday, nlckchgdays, nlckdays):
    def f(x):
        N = x[0]
        beta = x[1]
        gamma = x[2]
        delta = x[3]
        epsilons = x[4:]
        days = len(dft)
        S, I, R = sir_lockdown(N, beta, gamma, days + delay, delta, epsilons, lckday + delay, lckday + nlckchgdays + delay, lckday + nlckdays + delay)
        S, I, R = S[delay:delay+days], I[delay:delay+days], R[delay:delay+days]
        Io, Ro = dft["infected"].values, dft["recovered"].values
        So = N - Io - Ro
        loss = ((S - So)**2).sum()/days + ((I - Io)**2).sum()/days + ((R - Ro)**2).sum()/days
        #loss = ((I - Io)**2).sum()/days + ((R - Ro)**2).sum()/days
        return loss

    result = optimize.minimize(f, [100000, 0.5, 0.05, 0.5] + [0.5]*len(nlckchgdays), method="Nelder-Mead")

    return result

lckday = dft.index.get_loc(pd.to_datetime("2020-03-15"))
nlckchgdays = np.array([33,49,55]) # days to first significant change in lockdown
nlckdays = 69 # days

delay = 0 # days back
result = fdelay_lockdown(delay, lckday, nlckchgdays, nlckdays)
for d in range(5):
    #res = fdelay(d)
    res = fdelay_lockdown(d, lckday, nlckchgdays, nlckdays)
    print("delay: {}, fun: {}".format(d, res.fun))
    if res.fun < result.fun:
        delay = d
        result = res

N = result.x[0]
beta = result.x[1]
gamma = result.x[2]
delta = result.x[3]
epsilons = result.x[4:]

print("optimal: N = {}, beta = {}, gamma = {}, delta = {}, epsilons = {}, delay = {}".format(N, beta, gamma, delta, epsilons, delay))
print("error: {}".format(result.fun))

#S, I, R = sir(N, beta, gamma, days + delay)
S, I, R = sir_lockdown(N, beta, gamma, days + delay, delta, epsilons, lckday + delay, lckday + nlckchgdays + delay, lckday + nlckdays + delay)
S, I, R = S[delay:delay+days], I[delay:delay+days], R[delay:delay+days]

dft["S"] = S
dft["I"] = I
dft["R"] = R

dft["susceptible"] = N - dft["infected"] - dft["recovered"]

# forecasting

far = 60 # days

#S, I, R =  sir(N, beta, gamma, days + far + delay)
S, I, R = sir_lockdown(N, beta, gamma, days + far + delay, delta, epsilons, lckday + delay, lckday + nlckchgdays + delay, lckday + nlckdays + delay)
S, I, R = S[delay:delay+days+far], I[delay:delay+days+far], R[delay:delay+days+far]
d = {
    "S": S,
    "I": I,
    "R": R,
    "susceptible": list(dft["susceptible"].values) + [np.nan]*far,
    "infected": list(dft["infected"].values) + [np.nan]*far,
    "recovered": list(dft["recovered"].values) + [np.nan]*far,
}
dff = pd.DataFrame(d)
dff["date"] = pd.date_range(dft.index[0],periods=days+far,freq="D")
dff = dff.set_index("date")

dff["cases"] = dff["recovered"] + dff["infected"]
dff["forecast"] = dff["R"] + dff["I"]
dff[["forecast", "cases"]].to_csv(os.path.join("data", "generated-cases.csv"))

# graph

metadata = {'Creator': None, 'Producer': None, 'CreationDate': None}

fig, ax = plt.subplots(figsize=(8,6))
dfto[["cases", "pcr", "ac", "hospitalized", "uci", "dead", "recovered"]].plot(ax=ax)
ax.set_title("Totals in Spain")
ax.set_xlabel("")
ax.set_ylabel("# of occurences")
ax.grid(True, which="both")
dfto[["cases", "pcr", "ac",  "hospitalized", "uci", "dead", "recovered"]].to_csv(os.path.join("data", "generated-total.csv"))
plt.savefig(os.path.join("images", "generated-total.png"), format="png", dpi=300)
plt.savefig(os.path.join("images", "generated-total.pdf"), format="pdf", dpi=300, metadata=metadata)

fig, ax = plt.subplots(figsize=(8,6))
dfpct.plot(ax=ax)
ax.set_title("Percentage of dead")
ax.set_xlabel("")
ax.set_ylabel("%")
ax.grid(True, which="both")
plt.savefig(os.path.join("images", "generated-deadpct.png"), format="png", dpi=300)
plt.savefig(os.path.join("images", "generated-deadpct.pdf"), format="pdf", dpi=300, metadata=metadata)

fig, ax = plt.subplots(figsize=(8,6))
dff[["susceptible"]].plot(ax=ax, alpha=0.5)
dff[["infected", "recovered"]].plot(ax=ax)
dff[["S", "I", "R"]].plot(ax=ax, linestyle=":")
ax.axvspan(dff.index[lckday], dff.index[lckday+nlckdays], alpha=0.1, color='red', label="_lockdown")
plt.text(dff.index[lckday+nlckdays-3], N*0.89, 'lockdown', color='red', alpha=0.5, rotation=90)
ax.set_title("SIR model")
ax.set_xlabel("")
ax.set_ylabel("# of people")
ax.grid(True, which="both")
dff.to_csv(os.path.join("data", "generated-sir.csv"))
plt.savefig(os.path.join("images", "generated-sir.png"), format="png", dpi=300)
plt.savefig(os.path.join("images", "generated-sir.pdf"), format="pdf", dpi=300, metadata=metadata)

fig, ax = plt.subplots(figsize=(8,6))
dff[["cases"]].plot(ax=ax)
dff[["forecast"]].plot(ax=ax, linestyle=":")
ax.axvspan(dff.index[lckday], dff.index[lckday+nlckdays], alpha=0.1, color='red', label="_lockdown")
plt.text(dff.index[lckday+1], N*0.89, 'lockdown', color='red', alpha=0.5, rotation=90)
ax.set_title("Cases forecasting")
ax.set_xlabel("")
ax.set_ylabel("# of occurences")
ax.grid(True, which="both")
plt.savefig(os.path.join("images", "generated-sir-cases.png"), format="png", dpi=300)
plt.savefig(os.path.join("images", "generated-sir-cases.pdf"), format="pdf", dpi=300, metadata=metadata)

# update
with open("README.md") as f:
    lines = f.readlines()

data = dff.reset_index().loc[len(dft):len(dft)+9,["date","I","forecast"]].to_dict(orient="split")["data"]
lines[24:34] = ["| {} | {:.0f} | {:.0f} |\n".format(d[0].date(), d[1], d[2]) for d in data]
lines[38] = "N = {}\n".format(N)
lines[39] = "beta = {}\n".format(beta)
lines[40] = "gamma = {}\n".format(gamma)
lines[41] = "delta = {}\n".format(delta)
lines[42] = "epsilons = {}\n".format(epsilons)
lines[43] = "delay = {}\n".format(delay)

with open("README.md", "w") as f:
    f.write("".join(lines))
