import pandas as pd 
from collections import defaultdict 
import os, json, sys
LP = 0

def create_pd_df(exp_comp_d_d):
    ## exp_comp_pd_df = pd.DataFrame(columns=cols_q)
    exp_l = []
    for name in exp_comp_d_d:
        ser_v = pd.Series(exp_comp_d_d[name]) #dictionary input..
        nm_ser = pd.Series(index=['name'], data=[name])
        ser_v = nm_ser.append(ser_v)
        ## exp_comp_pd_df.append(ser_v)
        exp_l.append(ser_v)
    exp_comp_pd_df = pd.DataFrame(exp_l)
    print('\n\n')
    print('exp_comp_pd_df: ')
    print('\t',exp_comp_pd_df)
    return exp_comp_pd_df

def pre_proc_exp_cmp_pd_df(exp_comp_d_d):
    for nm in exp_comp_d_d:
        for col in exp_comp_d_d[nm]:
            assert(type(exp_comp_d_d[nm][col])==list)
            exp_comp_d_d[nm][col] = sum(exp_comp_d_d[nm][col])/len(exp_comp_d_d[nm][col])
    return exp_comp_d_d

def populate_weight_dictionary(scr_sht_exp_cmp_nm):
    cols = scr_sht_exp_cmp_nm.columns.tolist()
    ## print("cols_q: ", cols_q)
    exp_comp_d_d = defaultdict(dict)
    for ind, row in scr_sht_exp_cmp_nm.iterrows():
        if(ind%5==0): print("ind: ", ind)
        ## print(type(row))
        row_l = row.tolist()
        exp_nm, stp_nm = row_l[1], row_l[2]
        ## print("exp_nm: ", exp_nm)
        ## print("stp_nm: ", stp_nm)
        ## print(row_l, len(row_l))
        ## print(cols, len(cols))
        assert(len(row_l)==len(cols))
        for c_ind, rat in enumerate(row_l): #rat is main rating for c_ind>2...
            if(c_ind>2 and c_ind<(len(row_l)-1)): #skip nan, exp_nm, and stp_nm...
                col_v = cols[c_ind]
                ## print("col_v: ", col_v)
                cum_sum, cum_cnt = 0,0
                for _, row2 in scr_sht_exp_cmp_nm.iterrows():
                    if(stp_nm==row2.tolist()[2]): #same startup...
                        ## print("row2: ", row2)
                        cum_sum += row2[col_v] + LP
                        cum_cnt += 1
                avg_scr = (cum_sum/cum_cnt)
                ## print('avg_scr: ', avg_scr)
                try: exp_comp_d_d[exp_nm][col_v].append(round(avg_scr/(rat+LP), 4)) 
                except:
                    exp_comp_d_d[exp_nm][col_v] = []
                    exp_comp_d_d[exp_nm][col_v].append(round(avg_scr/(rat+LP), 4)) 
                #+1 to remove division by zero error...            
    print('exp_comp_d_d:\n\n', exp_comp_d_d)
    print('\n\n')
    exp_comp_d_d = pre_proc_exp_cmp_pd_df(exp_comp_d_d)
    exp_comp_pd_df = create_pd_df(exp_comp_d_d)
    return exp_comp_pd_df

def preproc_scr_sht_exp_cmp_nm(scr_sht_exp_cmp_nm):
    print('scr_sht_exp_cmp_nm', scr_sht_exp_cmp_nm)
    scr_sht_exp_cmp_nm.drop(scr_sht_exp_cmp_nm.index[:3], inplace=True)
    ## print('2 scr_sht_exp_cmp_nm', scr_sht_exp_cmp_nm)
    hdr_row = scr_sht_exp_cmp_nm.iloc[0]
    scr_sht_exp_cmp_nm.columns = hdr_row
    scr_sht_exp_cmp_nm.drop(scr_sht_exp_cmp_nm.index[0], inplace=True)
    return

def main():
    ext = '//Code//Code (C)//gen_wght_mtrx.data'
    PATH_DATA = os.getcwd()+ext
    with open(PATH_DATA,'r') as f_path:
        json_f = f_path.read()
        twoDarr = json.loads(json_f)
    outp_arr = ['gen_wght_mtrx_outp']
    ## FIND RELATIVE ACCURACY OF EACH EXPERT ###
    scr_sht_exp_cmp_nm = pd.read_csv('jdg_nrm.csv')
    ## scr_sht_exp_cmp_nm = preproc_scr_sht_exp_cmp_nm(scr_sht_exp_cmp_nm)
    print('columns: ', scr_sht_exp_cmp_nm.columns)
    print('\n\n')
    print(scr_sht_exp_cmp_nm.head())
    
    exp_comp_pd_df = populate_weight_dictionary(scr_sht_exp_cmp_nm)#.set_index('name')
    print(exp_comp_pd_df.head())
    exp_comp_pd_df.to_csv('jdg_wght_tble_exp_qs.csv')
    return
    #############################################

    PATH_WRT_BCK = os.getcwd()+'pop_pg.data' #after the change...
    with open(PATH_WRT_BCK,'w+') as f_path_w:
        f_path_w.write(json.dumps(outp_arr))

main()
