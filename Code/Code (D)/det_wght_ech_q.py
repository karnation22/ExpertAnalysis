## 1) Extract average 'Borda Score' from the company rankings
## 2) Multiply each 'normalized' rating by respective weights determined earlier
## ##  
## 3) Train perceptron model w/ weights (|W| = number of question parameters) and bias.
## 4) Determine relative strengths of each w_i parameter
import pandas as pd
import numpy as np
import pickle
import os, json, sys
from sklearn.linear_model import LinearRegression as LR
from collections import Counter
## MX_SCR = 5  normalizing score
## OFFST = 1 # offset value (avoids zero ratings)
SIM = 0.90 # 90% similarity for now
TOP_PERC = 0.90 #want to find top k params to maintiain .90

def get_avg_brda_scrs(cmp_rnk_d_1, cmp_rnk_d_2):
    avg_cmp_rnk = {}
    print(cmp_rnk_d_1, cmp_rnk_d_2)
    for cmp_nm in cmp_rnk_d_1:
        print(cmp_rnk_d_1[cmp_nm], cmp_rnk_d_2[cmp_nm])
        avg_cmp_rnk[cmp_nm] = (cmp_rnk_d_1[cmp_nm]+cmp_rnk_d_2[cmp_nm])/2
    return avg_cmp_rnk

#preprocess the dataframe
def preproc(exp_evl_pd_df):
    exp_evl_pd_df = exp_evl_pd_df.drop(exp_evl_pd_df.index[0:3])
    exp_evl_pd_df.columns = exp_evl_pd_df.iloc[0]
    exp_evl_pd_df.drop(exp_evl_pd_df.index[0], inplace=True)
    ## print(exp_evl_pd_df.columns)
    exp_evl_pd_df.drop(['Score'], axis=1, inplace=True)
    print(exp_evl_pd_df.head())
    return exp_evl_pd_df

def find_val(stp_nm, brd_scrs):
    for nm in brd_scrs:
        match = 0
        m_ln = min(len(nm), len(stp_nm))
        avg_ln = (len(nm)+len(stp_nm))/2
        for i in range(m_ln):
            if(nm[i]==stp_nm[i]): match+=1
        if(float(match)/avg_ln >= SIM): 
            #print(nm, stp_nm)
            return brd_scrs[nm] 
    return -1

def nrmlze_exp_evl(exp_evl_pd_df, nm_chp_wght_tbl, brd_scrs):
    ## print('brd_scrs: ', brd_scrs)
    nrm_exp_evl_X, nrm_exp_evl_Y = pd.DataFrame(), []
    cl_vls = exp_evl_pd_df.columns.tolist()
    print(cl_vls)
    for _, row in exp_evl_pd_df.iterrows():
        exp_nm, stp_nm = row[1], row[2]
        wght_rw = nm_chp_wght_tbl.loc[nm_chp_wght_tbl['name']==exp_nm]
        ## print(wght_rw.columns)
        row_l = row.tolist()
        ## print('row_l: ', row_l)
        row_o = []
        for r_i, r_c in enumerate(row_l):
            if(r_i>2): #skip nan, exp_nm, stp_nm
                cl_nm = cl_vls[r_i]
                ## print('cl_nm: ', cl_nm, type(cl_nm))
                try: wght_cf = wght_rw.loc[:,cl_nm].values[0]
                except: wght_cf = 1.0
                ## print("wght_cf", wght_cf, type(wght_cf))
                r_c = wght_cf * r_c
                ## print("r_c", r_c, type(r_c))
                row_o.append((cl_nm, r_c))
        d_row_o = dict(row_o)
        ## print(d_row_o)
        ## print("sr_d_row_o", sr_d_row_o)
        vl_stp_nam = find_val(stp_nm, brd_scrs)
        ## print("ans_d_row_o", ans_d_row_o)
        nrm_exp_evl_X = nrm_exp_evl_X.append(d_row_o, ignore_index=True)  
        nrm_exp_evl_Y.append(vl_stp_nam)
    return np.asarray(nrm_exp_evl_X), np.asarray(nrm_exp_evl_Y), nrm_exp_evl_X.columns.tolist()

def train_per(nrm_exp_evl_np_X, nrm_exp_evl_np_Y):
    skl_per = LR()
    skl_per_ft = skl_per.fit(nrm_exp_evl_np_X, nrm_exp_evl_np_Y)
    with open('jdg_skl_per.pkl', 'wb') as f_skl_per:
        pickle.dump(skl_per_ft, f_skl_per)
    return skl_per_ft

def find_top_k_params(model_params_v_s, col_vals, s_m_p):
    tot = []
    col_vls_k = []
    for (ind, vl) in model_params_v_s:
        print("ind, v: ", ind, vl)
        tot.append(vl)
        col_vls_k.append(col_vals[ind])
        if(sum(tot)/s_m_p >= TOP_PERC): 
            col_tot_d = {}
            with open('jdg_prm_to_wght_k.txt', 'w') as f_k_jdg_prm_t_wght:
                for i in range(len(tot)):
                    f_k_jdg_prm_t_wght.write("{}: {}\n".format(col_vls_k[i], tot[i]))
                    col_tot_d[col_vls_k[i]] = [tot[i]]
            print(col_tot_d)
            pd.DataFrame.from_dict(data=col_tot_d).to_excel('jdg_prm_to_wght_k.xlsx')
            return

def main():
    ext = '//Code//Code (D)//det_wght_ech_q.data'
    PATH_DATA = os.getcwd()+ext
    with open(PATH_DATA,'r') as f_path:
        json_f = f_path.read()
        twoDarr = json.loads(json_f)
    outp_arr = ['det_wght_ech_q...']
    ## RUN LINEAR REGRESSION - FIND RELATIVE WEIGHTS OF EACH QUESTION
    '''with open('jdg_cmp_rnk_m_1.txt', 'r') as f_cmp_rnk_1:
        cmp_rnk_L_1 = f_cmp_rnk_1.read().strip().split('\n')
        print(cmp_rnk_L_1)
        cmp_rnk_d_1 = {}
        for itm in cmp_rnk_L_1:
            key = itm[:itm.index(":")]
            vl = float(itm[itm.index(":")+1:].strip())
            cmp_rnk_d_1[key] = vl
    with open('jdg_cmp_rnk_m_2.txt', 'r') as f_cmp_rnk_2:
        cmp_rnk_L_2 = f_cmp_rnk_2.read().strip().split('\n')
        print(cmp_rnk_L_2)
        cmp_rnk_d_2 = {}
        for itm in cmp_rnk_L_2:
            key = itm[:itm.index(":")]
            vl = float(itm[itm.index(":")+1:].strip())
            cmp_rnk_d_2[key] = vl
    brd_scrs = get_avg_brda_scrs(cmp_rnk_d_1, cmp_rnk_d_2)
    exp_evl_pd_df = pd.read_csv('jdg_nrm.csv')
    #### exp_evl_pd_df = preproc(exp_evl_pd_df)
    nm_chp_wght_tbl = pd.read_csv('jdg_wght_tble_exp_qs.csv')
    nrm_exp_evl_np_X, nrm_exp_evl_np_Y, col_vals = nrmlze_exp_evl(exp_evl_pd_df, nm_chp_wght_tbl, brd_scrs)
    per_model = train_per(nrm_exp_evl_np_X, nrm_exp_evl_np_Y)
    model_params = per_model.coef_
    ## model_params /= sum(model_params)
    model_params = list(enumerate(list(np.exp(model_params) / sum(np.exp(model_params)))))
    s_m_p = sum(list(map(lambda tup: tup[1], model_params))) # should be ~1.0
    model_params_v_s = sorted(model_params, key=lambda tup: tup[1], reverse=True)
    print("model_params: ", model_params )
    print("model_params_v_s; s_m_p: ", model_params_v_s, s_m_p)
    find_top_k_params(model_params_v_s, col_vals, s_m_p)
    param_to_wght = {}
    for p_i in range(len(model_params)):
        param_to_wght[col_vals[p_i]] = round(model_params[p_i][1], 4)
    ##print(param_to_wght)
    with open('judge_param_question_to_weight.txt', 'w') as f_prm_wght:
        outp_l = []
        for q_p in param_to_wght:
            outp_l.append("{}: {}\n".format(q_p, param_to_wght[q_p]))
        f_prm_wght.writelines(outp_l)'''
    ####################################################################

    PATH_WRT_BCK = os.getcwd()+'pop_pg.data' #after the change...
    with open(PATH_WRT_BCK,'w+') as f_path_w:
        f_path_w.write(json.dumps(outp_arr))


main()