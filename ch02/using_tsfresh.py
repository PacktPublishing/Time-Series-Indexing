#!/usr/bin/env python3

import sys
import pandas as pd
import tsfresh

def main():
    if len(sys.argv) != 2:
        print("TS")
        sys.exit()

    TS1 = sys.argv[1]
    ts1Temp = pd.read_csv(TS1, compression='gzip')
    ta = ts1Temp.to_numpy()
    ta = ta.reshape(len(ta))

    # Mean value
    meanValue = tsfresh.feature_extraction.feature_calculators.mean(ta)
    print("Mean value:\t\t", meanValue)

    # Standard deviation
    stdDev = tsfresh.feature_extraction.feature_calculators.standard_deviation(ta)
    print("Standard deviation:\t", stdDev)

    # Skewness
    skewness = tsfresh.feature_extraction.feature_calculators.skewness(ta)
    print("Skewness:\t\t", skewness)

    # Kurtosis
    kurtosis = tsfresh.feature_extraction.feature_calculators.kurtosis(ta)
    print("Kurtosis:\t\t", kurtosis)

if __name__ == '__main__':
	main()
