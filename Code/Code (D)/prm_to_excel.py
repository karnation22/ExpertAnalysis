import pandas as pd
import os,json, sys
def main():
    ext = '//Code//Code (D)//prm_to_excel.data'
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
    outp_arr = ['prm_to_excel_fl']

    '''with open('chaperone_param_question_to_weight.txt', 'r') as f_chap:
        f_chap_l = f_chap.readlines()
        chp_dct = {}
        for itm in f_chap_l:
            prm = itm[:itm.index(":")]
            vl = float(itm[itm.index(":")+1:].strip())
            chp_dct[prm] = [vl] 
    with open('judge_param_question_to_weight.txt', 'r') as f_jdg:
        f_jdg_l = f_jdg.readlines()
        jdg_dct = {}
        for itm in f_jdg_l:
            prm = itm[:itm.index(":")]
            vl = float(itm[itm.index(":")+1:].strip())
            jdg_dct[prm] = [vl] 
    print(chp_dct)
    print(jdg_dct)
    chp_pd, jdg_pd = pd.DataFrame(data=chp_dct), pd.DataFrame(data=jdg_dct)
    chp_pd.to_csv('chaperone_parameters_to_values.csv')
    jdg_pd.to_csv('judge_parameters_to_values.csv')'''

    PATH_WRT_BCK = os.getcwd()+'pop_pg.data' #after the change...
    with open(PATH_WRT_BCK,'w+') as f_path_w:
        f_path_w.write(json.dumps(outp_arr))

main()