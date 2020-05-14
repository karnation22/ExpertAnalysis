## Find the top 3 experts by minimum difference between their ratings, and ranking score
import pandas as pd
import os, json, sys
from collections import Counter
from sys import maxsize
#### For part (A), document findings, code, and output files in analysis.

mn_wghts = [.3, .4, .1, .2]
sub_wghts = [[.15, .3, .15, .15, .25], [.1, .2, .1, .15, .1, .1, .25], [.15, .3, .15, .2, .2], [.2, .1, .3, .1, .3]]

def lrn_wghts():
    wghts = []
    assert(len(mn_wghts)==len(sub_wghts))
    for m_i in range(len(mn_wghts)):
        mn_wght = mn_wghts[m_i]
        sub_wght = sub_wghts[m_i]
        for s_wght in sub_wght:
            wghts.append(s_wght*mn_wght) 
    return wghts

def wght_sum(wghts, v_l):
    ## print('len(wghts): ', wghts, len(wghts))
    ## print('len(v_l): ', v_l, len(v_l))
    assert(len(wghts)==len(v_l))
    assert(round(sum(wghts), 2)==1.0)
    return sum([wghts[i]*v_l[i] for i in range(len(wghts))])

##calculate average difference between rating score(s) and avg normalized score...
def get_counter_diff_pred(rat_cmp_exp, cmp_rnk_m_1, wghts):
    exp_avg_diff_1 = dict()
    ## print(rat_cmp_exp.head())
    ## just for the first dictionary ...
    for ind, row in rat_cmp_exp.iterrows():
        ## if(ind%5==0): print("ind: ", ind)
        exp_nm, stp_nm = row[1], row[2]
        row_l_nums = row.tolist()[3:] #remove the nan, expert name, and startup name...
        if(wghts==None): avg_rat = sum(row_l_nums)/len(row_l_nums)
        else: avg_rat = wght_sum(wghts, row_l_nums)
        if exp_nm not in exp_avg_diff_1: exp_avg_diff_1[exp_nm] = []
        try: exp_avg_diff_1[exp_nm].append(abs(avg_rat-cmp_rnk_m_1[stp_nm]))
        except: continue
    for key in exp_avg_diff_1:
        v_l = exp_avg_diff_1[key]
        try: exp_avg_diff_1[key] = sum(v_l)/len(v_l) #average of list for each expert (uniform weights)
        except: exp_avg_diff_1[key] = maxsize #set value to max int if zero-division...
    cntr_exp_avg_diff = Counter(exp_avg_diff_1)
    return cntr_exp_avg_diff



## main function...
def main_tp_n(norm, n, wghts=None, st='chap', en='chap'):
    ext = '//Code//Code (A)//Chap//fnd_tp_n_jdg.data'
    PATH_DATA = os.getcwd()+ext
    with open(PATH_DATA,'r') as f_path:
        json_f = f_path.read()
        twoDarr = json.loads(json_f)
    inp_df = pd.DataFrame()
    for item in twoDarr:
        for item2 in item:
            inp_d = {}
            for item3 in item2:
                inp_d['company_name'] = item3[0]
                inp_d['startup_name'] = item3[2]
                if(not(item3[4]==None)): inp_d[item3[3]] = item3[4]
                else: inp_d[item3[3]] = item3[5]
                #print(inp_d)
                inp_df=inp_df.append(inp_d,ignore_index=True)
        print(inp_df)
    #rat_cmp_exp = pd.read_csv(norm)
    outp_arr = ['testingfnd_tp_n_jdg..']
    ## Run the analytics... find top n=3 experts in judge round... 
    '''
    with open('jdg_cmp_rnk_m_1.txt', 'r') as f_cmp_rnk_1:
        cmp_rnk_m_1_p = f_cmp_rnk_1.readlines()
        cmp_rnk_m_1 = {}
        for itm in cmp_rnk_m_1_p:
            cmp_nm = itm[:itm.index(":")]
            vl = float(itm[itm.index(":")+1:].strip())
            cmp_rnk_m_1[cmp_nm] = vl
    with open('jdg_cmp_rnk_m_1.txt', 'r') as f_cmp_rnk_1:
        cmp_rnk_m_2_p = f_cmp_rnk_1.readlines()
        cmp_rnk_m_2 = {}
        for itm in cmp_rnk_m_2_p:
            cmp_nm = itm[:itm.index(":")]
            vl = float(itm[itm.index(":")+1:].strip())
            cmp_rnk_m_2[cmp_nm] = vl
    cntr_exp_avg_diff_1 = get_counter_diff_pred(rat_cmp_exp, cmp_rnk_m_1, wghts)
    cntr_exp_avg_diff_2 = get_counter_diff_pred(rat_cmp_exp, cmp_rnk_m_2, wghts)
    least_common_1 = dict(cntr_exp_avg_diff_1.most_common()[:-n-1:-1])
    lst_cmmn_1 = ""
    least_common_2 = dict(cntr_exp_avg_diff_2.most_common()[:-n-1:-1])
    lst_cmmn_2 = ""
    with open("{}_top_{}_names_1.txt".format(st, n), 'w') as f_names_1:
        for nm, scr in sorted(least_common_1.items(), key=lambda itm: itm[1]):
            scr = round(scr, 4)
            lst_cmmn_1 += "{}: {}\n\n".format(nm, scr)
        ## lst_cmmn_1 = sorted(lst_cmmn_1, key=lambda tup: tup[1])
        f_names_1.write(lst_cmmn_1)
    with open("{}_top_{}_names_2.txt".format(st, n), 'w') as f_names_2:
        for nm, scr in sorted(least_common_2.items(), key=lambda itm: itm[1]):
            scr = round(scr, 4)
            lst_cmmn_2 += "{}: {}\n\n".format(nm, scr)
        ## lst_cmmn_2 = sorted(lst_cmmn_2, key=lambda tup: tup[1])
        f_names_2.write(lst_cmmn_2)
    return'''

    PATH_WRT_BCK = os.getcwd()+'pop_pg.data' #after the change...
    with open(PATH_WRT_BCK,'w+') as f_path_w:
        f_path_w.write(json.dumps(outp_arr))



## m_wghts = lrn_wghts()
## print('m_wghts: ', m_wghts)
## main_tp_n('jud_nrm.csv', n=3, wghts=m_wghts, st='jdg')