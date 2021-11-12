#!/bin/bash

# for nb in 100000 500000 1000000 2000000; do
# 	for nq in 10000 50000 100000 500000; do
# 		for d in 128 256 512 1024 2048; do
# 		  drop_caches
# 		  python FaissTest.py --d $d --topk 1 --nb $nb --nq $nq
# 		  echo "------------------------------------"
# 		done
# 	done
# done


for nb in 1000000; do
	for nq in 50000; do
		for d in 2048; do
		  drop_caches
		  python FaissTest.py --d $d --topk 1 --nb $nb --nq $nq
		  echo "------------------------------------"
		done
	done
done

for nb in 2000000; do
	for nq in 10000 50000 100000 500000; do
		for d in 128 256 512 1024 2048; do
		  drop_caches
		  python FaissTest.py --d $d --topk 1 --nb $nb --nq $nq
		  echo "------------------------------------"
		done
	done
done