# Entry point for command line. Supply baseline and parameter multipliers in triples
# python3 shell.py large_town geometry n 0.5 health vi 0.5

from pandemic.example_parameters import BASELINES, modifier
from pandemic.conventions import DESCRIPTIONS, CATEGORIES
from pandemic.simulation import simulate
import  matplotlib.pyplot as plt
import sys

def modify_and_run(baseline, triples):
    # python3 shell.py large_town geometry n 20000 health vi 0.5
    params = BASELINES[baseline]
    descriptions = list()
    n = len(triples)
    assert n % 3 ==0, 'Expecting triples of command line parameters '
    num = int(n/3)
    print(num)
    for k in range(num):
        category = triples[3 * k].lower()
        param    = triples[3 * k+1].lower()
        assert category in CATEGORIES
        assert param in list(DESCRIPTIONS[category].keys())
        factor   = float(triples[3*k+2])
        params, desc = modifier( category=category, param=param, factor=factor, baseline=params )
        descriptions.append(desc)
    simulate(params=params, plt=plt, xlabel=','.join(descriptions))

if __name__=="__main__":
    modify_and_run(baseline=sys.argv[1],triples=sys.argv[2:])