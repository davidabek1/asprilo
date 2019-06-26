import os
import subprocess

os.chdir('/home/david/asprilo/')

for k in range(5, 80, 5):
    #os.popen('gen -x 15 -y 12 -r {0} -s {0} -N 5 --prs 1 --spr 1 --pus 1 --ol 1 -p 1 -P {0} -u {0} -o {0}'.format(k))
    subprocess.call('gen -x 15 -y 12 -r {0} -s {0} -N 5 --prs 1 --spr 1 --pus 1 --ol 1 -p 1 -P {0} -u {0} -o {0}'.format(k), shell=True)
