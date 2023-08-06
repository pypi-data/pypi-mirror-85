# -*- coding: utf-8 -*-
"""
Utility for brian2 simulator.
"""

__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2019-, Dilawar Singh"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"

from brian2 import *
import pandas as pd

def spikeMonitor2DataFrame(sm):
    df = pd.DataFrame()
    trains = sm.spike_trains()
    df = pd.DataFrame({k: pd.Series(v) for k, v in trains.items()})
    return df

def stateMonitorToDataFrame(sm):
    df = pd.DataFrame()
    df['t'] = np.array(sm.t/second)
    for x in sm.record_variables:
        vals = getattr(sm, x)
        for i, v in enumerate(vals):
            vname = f'{x}[{i}]'
            df[vname] = v
    return df

def test():
    N = 100
    taum = 10*ms
    taupre = 20*ms
    taupost = taupre
    Ee = 0*mV
    vt = -54*mV
    vr = -60*mV
    El = -74*mV
    taue = 5*ms
    F = 15*Hz
    gmax = .01
    dApre = .01
    dApost = -dApre * taupre / taupost * 1.05
    dApost *= gmax
    dApre *= gmax

    eqs_neurons = '''
    dv/dt = (ge * (Ee-vr) + El - v) / taum : volt
    dge/dt = -ge / taue : 1
    '''

    input = PoissonGroup(N, rates=F)
    neurons = NeuronGroup(1, eqs_neurons, threshold='v>vt', reset='v = vr',
                          method='linear')
    S = Synapses(input, neurons,
                 '''w : 1
                    dApre/dt = -Apre / taupre : 1 (event-driven)
                    dApost/dt = -Apost / taupost : 1 (event-driven)''',
                 on_pre='''ge += w
                        Apre += dApre
                        w = clip(w + Apost, 0, gmax)''',
                 on_post='''Apost += dApost
                         w = clip(w + Apre, 0, gmax)''',
                 )
    S.connect()
    S.w = 'rand() * gmax'
    mon = StateMonitor(S, 'w', record=[0, 1])
    s_mon = SpikeMonitor(input)
    run(10*second, report='text')
    df1 = spikeMonitor2DataFrame(s_mon)
    df2 = stateMonitorToDataFrame(mon)
    ax1 = plt.subplot(211)
    df1.plot(ax=ax1)
    ax2 = plt.subplot(212)
    df2.plot(x='t', ax=ax2)
    tight_layout()
    savefig(f'{__file__}.png')

def main():
    test()

if __name__ == '__main__':
    main()
