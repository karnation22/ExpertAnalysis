## Provide ranking score to companies (for both columns)
## save scores in dictionary; higher score corresponds to higher ranking

import pandas as pd, os, json

def main_ranker(xlsx_sht_nm, sht_nm):
    PATH_DATA = os.getcwd()+'//'+os.path.basename(__file__)[:-3]+".data"
    with open(PATH_DATA,'r') as f_path:
        json_f = f_path.read()
        twoDarr = json.loads(json_f)
    outp_arr = ['rnk_jdg_cmp..']
    ## Main Ranker Judge ##
    '''
    cmp_rnk_pd = pd.read_excel(xlsx_sht_nm, sheet_name=sht_nm)
    cmp_rnk_1 = cmp_rnk_pd.iloc[:,1].dropna().tolist()[:-1]
    cmp_rnk_2 = cmp_rnk_pd.iloc[:,1].dropna().tolist()[:-1]
    nm_rows = len(cmp_rnk_1)
    ## print(cmp_rnk_1, len(cmp_rnk_1))
    
    cmp_rnk_1_m = dict([(comp, round((nm_rows-ind)/nm_rows, 4) ) for ind,comp in enumerate(cmp_rnk_1)])
    cmp_rnk_2_m = dict([(comp, round((nm_rows-ind)/nm_rows, 4) ) for ind,comp in enumerate(cmp_rnk_2)])
    #### sprint("cmp_df: ", cmp_df, type(cmp_df))
    print("cmp_rnk_1: ", cmp_rnk_1)
    print("cmp_rnk_2: ", cmp_rnk_2)
    print("cmp_rnk_1_m", cmp_rnk_1_m)
    print("cmp_rnk_2_m", cmp_rnk_2_m)

    with open("jdg_cmp_rnk_m_1.txt", "w") as f_cmp_rnk_1:
        for cmp_nm, cmp_sc in sorted(cmp_rnk_1_m.items(), key=lambda tup: tup[1]):
            f_cmp_rnk_1.write("{}: {}\n".format(cmp_nm, cmp_sc))

    with open("jdg_cmp_rnk_m_2.txt", "w") as f_cmp_rnk_2:
        for cmp_nm, cmp_sc in sorted(cmp_rnk_2_m.items(), key=lambda tup: tup[1]):
            f_cmp_rnk_2.write("{}: {}\n".format(cmp_nm, cmp_sc))
    ##print("nm_rows: ", nm_rows)
    ##print("nm_rows: ", nm_rows)
    ##print("cmp_rnk_pd",cmp_rnk_pd)'''
    ## Main Ranker Judge ##
    os.chdir('../../..')
    PATH_WRT_BCK = os.getcwd()+'pop_pg.data' #after the change...
    with open(PATH_WRT_BCK,'w') as f_path_w:
        f_path_w.write(json.dumps(outp_arr))

main_ranker('S5 - Startup-O Judge Evaluation Sheet-Mar 30.xlsx', 'final summary')