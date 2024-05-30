#!/usr/bin/env python3

from subprocess import run, PIPE
import os, sys

# Change working dir to the script path
os.chdir(os.path.dirname(os.path.abspath(__file__)))

models = [os.path.splitext(m)[0] for m in os.listdir() if '.mcrl2' in m]

lps = 'tmp.lps'
open(lps, 'a').close()
for model in models:
    print(f'============= {model} ==============')
    r = run(['mcrl22lps', f'{model}.mcrl2'], stdout=PIPE, check=True)
    r = run(['lpsconstelm'], input=r.stdout, stdout=PIPE, check=True)
    _ = run(['lpsparelm', '-', lps], input=r.stdout, check=True)

    for mcf in os.listdir('properties/'):
        if '.mcf' in mcf:
            prop, _ = os.path.splitext(mcf)

            print(f'property {prop}:\t', end='')
            sys.stdout.flush()

            r = run(['lps2pbes',  '-f', f'properties/{mcf}', lps], stdout=PIPE, check=True)
            r = run(['pbessolve', ], input=r.stdout, check=True)

os.remove(lps)
