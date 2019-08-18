## Find the top 3 experts by minimum difference between their ratings, and ranking score
import pandas as pd
import os, json, sys
from collections import Counter
from sys import maxsize
#### For part (A), document findings, code, and output files in analysis.


def wght_sum(wghts, v_l):
    print('len(wghts): ', wghts, len(wghts))
    print('len(v_l): ', v_l, len(v_l))
    assert(len(wghts)==len(v_l))
    assert(sum(wghts)==1.0)
    return sum([wghts[i]*v_l[i] for i in range(len(wghts))])

##calculate average difference between rating score(s) and avg normalized score...
def get_counter_diff_pred(rat_cmp_exp, cmp_rnk_m_1, wghts):
    exp_avg_diff_1 = dict()
    print(rat_cmp_exp.head())
    ## just for the first dictionary ...
    for ind, row in rat_cmp_exp.iterrows():
        ## if(ind%5==0): print("ind: ", ind)
        exp_nm, stp_nm = row.expert_name, row.startup_name
        row_l_nums = row.tolist()[3:] #remove the nan, expert name, and startup name...
        if(wghts==None): avg_rat = sum(row_l_nums)/len(row_l_nums)
        else: avg_rat = wght_sum(wghts, row_l_nums)
        if exp_nm not in exp_avg_diff_1: exp_avg_diff_1[exp_nm] = []
        try: exp_avg_diff_1[exp_nm].append(abs(avg_rat-cmp_rnk_m_1[stp_nm]))
        except: continue
    for key in exp_avg_diff_1:
        v_l = exp_avg_diff_1[key]
        try: exp_avg_diff_1[key] = sum(v_l)/len(v_l) #average of list (uniform weights)
        except: exp_avg_diff_1[key] = maxsize #set value to max int if zero-division...
    cntr_exp_avg_diff = Counter(exp_avg_diff_1)
    return cntr_exp_avg_diff



## main function...
def main_tp_n(norm, n, wghts=None, st='chap', en='chap'):
    ext = '//Code//Code (A)//Chap//fnd_tp_n_chp.data'
    PATH_DATA = os.getcwd()+ext
    with open(PATH_DATA,'r') as f_path:
        json_f = f_path.read()
        twoDarr = json.loads(json_f)

    #rat_cmp_exp = pd.read_csv(norm)

    outp_arr = ['testingflt_tp...']

    ## RUN THE ANALYTICS... return top n=3 most accurate chaperones.. ##
    '''
    with open('cmp_rnk_m_1.txt', 'r') as f_cmp_rnk_1:
        cmp_rnk_m_1 = f_cmp_rnk_1.read()
        cmp_rnk_m_1 = eval(cmp_rnk_m_1[cmp_rnk_m_1.index("{"):])
    with open('cmp_rnk_m_2.txt', 'r') as f_cmp_rnk_2:
        cmp_rnk_m_2 = f_cmp_rnk_2.read()
        cmp_rnk_m_2 = eval(cmp_rnk_m_2[cmp_rnk_m_2.index("{"):])
    ## print(cmp_rnk_m_1)
    ## print(cmp_rnk_m_2)
    cntr_exp_avg_diff_1 = get_counter_diff_pred(rat_cmp_exp, cmp_rnk_m_1, wghts)
    cntr_exp_avg_diff_2 = get_counter_diff_pred(rat_cmp_exp, cmp_rnk_m_2, wghts)
    least_common_1 = dict(cntr_exp_avg_diff_1.most_common()[:-n-1:-1])
    lst_cmmn_1 = ""
    least_common_2 = dict(cntr_exp_avg_diff_2.most_common()[:-n-1:-1])
    lst_cmmn_2 = ""
    with open("{}_to_{}_top_{}_names_1.txt".format(st, en, n), 'w') as f_names_1:
        for nm, scr in sorted(least_common_1.items(), key=lambda itm: itm[1]):
            scr = round(scr, 4)
            lst_cmmn_1 += "{}: {}\n\n".format(nm, scr)
        ## lst_cmmn_1 = sorted(lst_cmmn_1, key=lambda tup: tup[1])
        f_names_1.write(lst_cmmn_1)
    with open("{}_to_{}_top_{}_names_2.txt".format(st, en, n), 'w') as f_names_2:
        for nm, scr in sorted(least_common_2.items(), key=lambda itm: itm[1]):
            scr = round(scr, 4)
            lst_cmmn_2 += "{}: {}\n\n".format(nm, scr)
        ## lst_cmmn_2 = sorted(lst_cmmn_2, key=lambda tup: tup[1])
        f_names_2.write(lst_cmmn_2)
    return'''
    ########################

    PATH_WRT_BCK = os.getcwd()+'pop_pg.data' #after the change...
    with open(PATH_WRT_BCK,'w+') as f_path_w:
        f_path_w.write(json.dumps(outp_arr))

main_tp_n('chap_norm.csv', 3)