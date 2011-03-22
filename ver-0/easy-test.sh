#!/bin/sh
python train.py ../letter-set/abdgq4train.txt knowledge.dat
python test.py knowledge.dat ../letter-each/a.txt
python test.py knowledge.dat ../letter-each/a-serif.txt
python test.py knowledge.dat ../letter-each/g-serif.txt
python test.py knowledge.dat ../letter-each/q.txt
python test.py knowledge.dat ../letter-each/q-ish.txt


