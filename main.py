__author__ = 'denis_iosu_jeroni_pablo'
import numpy as np
import pandas as pd

def main():
    # TODO:
    # 0. FIND AND LOAD DATA
    #       -a. We have csv-s of first and second division of spain from 1996/97 til now. And lot of information else.
    #
    #
    #                                http://www.football-data.co.uk/spainm.php
    #
    #
    #       a. Here we have history of 'quinielas': http://www.resultados-futbol.com/quiniela/historico/18
    #       b. Here we have the statistics of the 2014-15: http://www.lfp.es/estadisticas/liga-bbva/goles/
    #       c. Here we can get everything!!: http://www.marca.com/estadisticas/futbol/primera/2010_11/
    # Load data
    filename_red = 'Data/Example2013-14.csv'

    data_2013_2014 = pd.io.parsers.read_csv(filename_red, ';')
    print data_2013_2014
    #   1. FILTER DATA
    #   2. RETRIEVE
    #   3. REUSE
    #   4. REVISE
    #   5. RETAIN

if __name__ == '__main__':
    main()
