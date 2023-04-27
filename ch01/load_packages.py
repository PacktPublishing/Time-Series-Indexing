#!/usr/bin/env python3

import pandas as pd
import argparse
import stumpy
import numpy as np
import scipy
import matplotlib

def main():
	print("scipy version:", scipy.__version__)
	print("numpy version:", np.__version__)
	print("stumpy version:", stumpy.__version__)
	print("matplotlib version:", matplotlib.__version__)
	print("argparse version:", argparse.__version__)
	print("pandas version:", pd.__version__)

if __name__ == '__main__':
	main()
