## Provide ranking score to companies (for both columns)
## save scores in dictionary; higher score corresponds to higher ranking

import pandas as pd, os, json

def main_ranker(xlsx_sht_nm, sht_nm):
    PATH_DATA = os.getcwd()+'//'+os.path.basename(__file__)[:-3]+".data"
    with open(PATH_DATA,'r') as f_path:
        json_f = f_path.read()
        twoDarr = json.loads(json_f)
    outp_arr = ['rnk_chp_cmp..']
    ### Rank chaperone...##
    '''
    cmp_rnk_pd = pd.read_excel(xlsx_sht_nm, sheet_name=sht_nm)
    cmp_rnk_pd.columns = cmp_rnk_pd.iloc[0]
    cmp_rnk_pd = cmp_rnk_pd.drop(cmp_rnk_pd.index[0],axis=0)
    nm_rows = len(cmp_rnk_pd)
    cmp_df = cmp_rnk_pd['Company']
    cmp_rnk_1, cmp_rnk_2 = cmp_df.iloc[:,0].tolist(), cmp_df.iloc[:,1].tolist()
    cmp_rnk_1_m = dict([(comp, round((nm_rows-ind)/nm_rows, 4) ) for ind,comp in enumerate(cmp_rnk_1)])
    cmp_rnk_2_m = dict([(comp, round((nm_rows-ind)/nm_rows, 4) ) for ind,comp in enumerate(cmp_rnk_2)])
    print("cmp_df: ", cmp_df, type(cmp_df))
    print("cmp_rnk_1: ", cmp_rnk_1)
    print("cmp_rnk_2: ", cmp_rnk_2)
    print("cmp_rnk_1_m: ", cmp_rnk_1_m)
    print("cmp_rnk_2_m: ", cmp_rnk_2_m)

    with open("chp_cmp_rnk_m_1.txt", "w") as f_cmp_rnk_1:
        for cmp_nm, cmp_sc in sorted(cmp_rnk_1_m.items(), key=lambda tup: tup[1]):
            f_cmp_rnk_1.write("{}: {}\n".format(cmp_nm, cmp_sc))

    with open("chp_cmp_rnk_m_2.txt", "w") as f_cmp_rnk_2:
        for cmp_nm, cmp_sc in sorted(cmp_rnk_2_m.items(), key=lambda tup: tup[1]):
            f_cmp_rnk_2.write("{}: {}\n".format(cmp_nm, cmp_sc))
    ##print("nm_rows: ", nm_rows)
    ##print("cmp_rnk_pd",cmp_rnk_pd)'''
    ## Main ranker Chaperone ##
    os.chdir('../../..')
    PATH_WRT_BCK = os.getcwd()+'pop_pg.data' #after the change...
    with open(PATH_WRT_BCK,'w') as f_path_w:
        f_path_w.write(json.dumps(outp_arr))

main_ranker('Startup-O Chaperone Evaluation Sheet- 1 MAR 2018.xlsx', 'Ranking test')