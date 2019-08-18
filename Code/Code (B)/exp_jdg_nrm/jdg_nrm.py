import pandas as pd 

def preprec_j(jud_pd_df):
    jud_pd_df.columns = jud_pd_df.iloc[0]
    col_l = jud_pd_df.columns.tolist()
    lst_id = col_l.index('Network')+1
    print(jud_pd_df.columns)
    jud_pd_df.drop(jud_pd_df.index[0], inplace=True)
    jud_pd_df.drop(jud_pd_df.index[:3], inplace=True)
    jud_pd_df.drop(columns=col_l[lst_id:],inplace=True)

    print(jud_pd_df.head(), jud_pd_df.columns)
    return jud_pd_df

def f_nrmd_jud_pd_df(jud_pd_df):
    nrmd_jud_pd_df = pd.DataFrame()
    for c_i, c_c in enumerate(jud_pd_df):
        ## print("c_c: ", c_c)
        if(c_i>=2):
            col_l = jud_pd_df[c_c].tolist()
            col_l = [col_v/max(col_l) for col_v in col_l]
            nrmd_jud_pd_df[c_c] = col_l
        else: nrmd_jud_pd_df[c_c] = jud_pd_df[c_c]
    return nrmd_jud_pd_df

def main():
    jud_pd_df = pd.read_excel('S5 - Startup-O Judge Evaluation Sheet-Mar 30.xlsx', sheet_name='algo')
    jud_pd_df = preprec_j(jud_pd_df)
    nrmd_jud_pd_df = f_nrmd_jud_pd_df(jud_pd_df)
    nrmd_jud_pd_df.to_csv('jud_nrm.csv')
    print(nrmd_jud_pd_df.head())

main()