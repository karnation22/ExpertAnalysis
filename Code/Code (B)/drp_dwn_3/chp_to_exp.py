import pandas as pd 
from rnk_exp_cmp import main_ranker
from fnd_tp_n_exp import main_tp_n, get_counter_diff_pred

chp_wghts = [(1/35)]*35 #uniform weights for chap.

def main():
    main_ranker('Startup-O Expert Evaluation Sheet-Season 5 Round 2 - 1 Mar 18.xlsx', 'Ranked')
    main_tp_n('chap_norm.csv', 3, None, 'chap', 'exp')
    

main()