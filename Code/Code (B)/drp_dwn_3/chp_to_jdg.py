import pandas as pd 
from rnk_jdg_cmp import main_ranker
from fnd_tp_n_exp import main_tp_n, get_counter_diff_pred

chp_wghts = [(1/35)]*35 #uniform weights for chap.

def main():
    main_ranker('S5 - Startup-O Judge Evaluation Sheet-Mar 30.xlsx', 'final summary')
    main_tp_n('chap_norm.csv', 3, None, 'chap', 'jdg')

main()