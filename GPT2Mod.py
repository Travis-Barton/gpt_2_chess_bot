#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 13:54:34 2020

@author: tbarton
"""
# make sure you have tensorflow 1.15
import gpt_2_simple as gpt2
sess = gpt2.start_tf_sess()
gpt2.load_gpt2(sess, run_name='new_run_large')
gpt2.download_gpt2()


sess = gpt2.start_tf_sess()
gpt2.load_gpt2(sess, run_name='new_run_large')
gpt2.finetune(sess,
              dataset='big_chess_set.txt',
              run_name='lets_play_chess',
              print_every=1,
              multi_gpu=True,
              save_every=2,
              combine=100,
              steps=10)   # steps is max number of training steps

sess.close()
