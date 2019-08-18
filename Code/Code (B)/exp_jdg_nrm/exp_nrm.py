import pandas as pd 

def preprocdf(exp_pd_df): 
    exp_pd_df.drop(exp_pd_df.index[:3], inplace=True)
    exp_pd_df.columns = exp_pd_df.iloc[0]
    exp_pd_df.drop(exp_pd_df.index[0], inplace=True)
    exp_pd_df.drop('Score', inplace=True, axis=1)
    print(exp_pd_df.head())
    return exp_pd_df

def f_nrmd_exp_pd_df(exp_pd_df):
    nrmd_exp_pd_df = pd.DataFrame()
    for c_i, c_c in enumerate(exp_pd_df):
        print("c_c: ", c_c)
        if(c_i>2):
            col_l = exp_pd_df[c_c].tolist()
            col_l = [col_v/max(col_l) for col_v in col_l]
            nrmd_exp_pd_df[c_c] = col_l
        elif(c_i>0): nrmd_exp_pd_df[c_c] = exp_pd_df[c_c]
    return nrmd_exp_pd_df


def main():
    exp_pd_df = pd.read_excel('Startup-O Expert Evaluation Sheet-Season 5 Round 2 - 1 Mar 18.xlsx', sheet_name='Scoring')
    exp_pd_df = preprocdf(exp_pd_df)
    nrmd_exp_pd_df = f_nrmd_exp_pd_df(exp_pd_df)
    nrmd_exp_pd_df.to_csv('exp_nrmd.csv')
main()