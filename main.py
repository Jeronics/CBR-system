__author__ = 'denis_iosu_jeroni_pablo'
import numpy as np
import pandas as pd
import PreprocessMatches as ppm
import Match as read
import utils as ut

def main():

    # Load data
    dataset = "Data/Example2013-14.csv"

    # READ DATASET
    matches_data = read.read_match_dataset(dataset)

    # PREPROCESS DATASET
    matches_preprocessdata = ppm.main(matches_data)


    for match in matches_preprocessdata:
        # print match.local
        print ut.int_to_weekday(ut.date_to_day_of_week(match.data))


if __name__ == '__main__':
    main()
