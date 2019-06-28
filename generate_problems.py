import os
import subprocess

os.chdir('/home/david/asprilo/')

batch_size = 5
for k in range(5, 80, batch_size):
    #os.popen('gen -x 15 -y 12 -r {0} -s {0} -N 5 --prs 1 --spr 1 --pus 1 --ol 1 -p 1 -P {0} -u {0} -o {0}'.format(k))
    subprocess.call('gen -x 15 -y 12 -r {0} -s {0} -N {1} --prs 1 --spr 1 --pus 1 --ol 1 -p 1 -P {0} -u {0} -o {0}'.format(k, batch_size), shell=True)
    for i in range(0,batch_size):
        subprocess.call('python ./fix_asprilo_assignment.py generatedInstances/x15_y12_n180_r{0}_s{0}_ps1_pr{0}_u{0}_o{0}_l{0}_N{1:03d}.lp'.format(k,i+1), shell=True)
