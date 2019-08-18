import pandas as pd
from rnk_jdg_cmp import main_ranker
from fnd_tp_n_exp import main_tp_n, get_counter_diff_pred

exp_wghts_p = [5,5,5,5,5,5,5,5,5,2.5,2.5,2.5,2.5,10,2.5,5,2.5,25] 
exp_wghts = [exp_wght/100 for exp_wght in exp_wghts_p]  #uniform weights for chap.


def main():
    main_ranker('S5 - Startup-O Judge Evaluation Sheet-Mar 30.xlsx', 'final summary')
    main_tp_n('exp_nrmd.csv', 3, exp_wghts, 'exp', 'jdg')

main()