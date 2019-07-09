import os
import subprocess

#os.chdir('/home/david/asprilo/')
#os.chdir('/home/zeged/mygits/asprilo/')

batch_size = 5
for k in range(5, 80, batch_size):
    #usage: gen.py [X] [Y] [Robots/Shelves] [max rooms] [min room] [max room] [batchs size]
    #os.popen('gen -x 15 -y 12 -r {0} -s {0} -N 5 --prs 1 --spr 1 --pus 1 --ol 1 -p 1 -P {0} -u {0} -o {0}'.format(k))
    subprocess.call(f'python ./adapter.py 16 16 {k} 15 5 10 3', shell=True)

