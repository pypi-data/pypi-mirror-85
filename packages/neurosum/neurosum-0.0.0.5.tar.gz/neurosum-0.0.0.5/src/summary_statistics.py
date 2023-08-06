#!/usr/bin/env python3
from os import path
import numpy as np
from src.mea_analyzer import mea_wrapper
import matplotlib.pyplot as plt
import sys, os, scipy.io, pickle, h5py, argparse, glob
from pathlib import Path
import importlib.util
import configparser

def run_summary():
    '''
    Takes in a data set as a commandline argument, it expects a two-dimensional array of [channels x signals]
    '''
    parser = argparse.ArgumentParser(description='Create a plot of summary statistics.')
    parser.add_argument('--file', type=str, help='Navigate to, and name data set to run', default='', required=False)
    parser.add_argument('--wells', type=int, help='Number of wells to analyze', default=12, required=False)
    parser.add_argument('--shape', type=str, help='Number of wells to analyze', default='3x4', required=False)
    parser.add_argument('--analysis', type=str, help='Which analysis to run', default='000100000', required=False)
    args = parser.parse_args()
    myFile = args.file
    # User input shape of mea plate, e.g. 4x3
    split_shape = args.shape.split('x')
    if len(split_shape) == 2:
        mea_shape = (int(split_shape[0]), int(split_shape[1]))
    else:
        print('Shape argument is malformed, must look like: 3x4')
        sys.exit()
    files_to_run = []
    if myFile == '':
        files_to_run = glob.glob(f'**/**.raw', recursive=True)
    elif os.path.isdir(myFile):
        files_to_run = glob.glob(f'{myFile}/**/**.raw', recursive=True)
        if len(files_to_run) == 0:
            print('Cannot find any raw files, exiting...')
            sys.exit()
    elif os.path.isfile(myFile):
        files_to_run.append(myFile)
    else:
        print('Cannot find any raw files, exiting...')
        sys.exit()
    # Do analysis file by file
    user_todo = [int(a) for a in args.analysis]
    for i, raw_file in enumerate(files_to_run):
        print(f'Proccessing file {i+1} of {len(files_to_run)}')
        mea_wrapper(user_todo=user_todo).raw_summary(raw_file)

    print('The summary statistics have finished computing.\nFind the "processed" folder for details.')

#            self.fooof_recordings.append(self.fooof_wells)
    # Across recording analyses
#    self.plot_fooof()
def main():
    run_summary()


