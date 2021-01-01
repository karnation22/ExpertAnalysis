# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from openpyxl.utils.cell import get_column_letter as g_c_l
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer as SIA
from math import isnan as isn
import pathlib
import pandas as pd, numpy as np
import os, sys
import json

## Input Chaperone 'results' data into dataframe
## Output the same Chaperone data as a series of floating point numbers

NUMER_DATA = ['D','E','F','G','AA','AB','AF','AR','AS']
CAT_ORD_DATA = ['H','I','O','AC','AD','AT','AU','AV','AW','AX','AY','AZ']
BIN_POS = ['J','K','L','M','R','S','T','U','AI']
BIN_PRES = ['W','X']
COMM_DATA = ['AE','BA']
ROLES = ['mentor', 'expert', 'tech', 'judge']
NLO,NHI=1,4
wlo,wmed,whi='low','med','high'
chp_sheet = 'Startup-O Chaperone Evaluation Sheet- 1 MAR 2018.csv'
res,rnk = 'results','Ranking test'
sia_ana = SIA()

qs =  [
    'Does the management believe in building a strong in-house tech team ?', 
    'Relevant Industry/market background of team', 
        'How well can team execute their presented plans ?', 
        'What isthe level of understanding and clarity of the financial projections by the team ?', 
        'Additional Comments', 
        'Potential Execution Risks', 
        'Are the hiring plans relevant to the roadmap and business growth ?', 
        'Does he understand the business space clearly or is he just a techie ?', 
        'Go to market plan strength', 
        'What is the level of uniqueness in the proposition for the venture?', 
        'Is it built using a relevant tech stack ? Are they using relevant technologies to build the product ?', 
        'Do the tech team (and biz team) understand and follow a form of agile / lean SDLC ?', 
        'How high is the business momentum and pipeline of business ?', 
        'Is the team sufficiently staffed ?', 
        'Please rank from high to low the risks to your revenue in next 24 months ?', 
        'How feasible do you think is the Go To Market plan in next 12-18 month timeframe ?', 
        'Addressable Market Size', 
        'How high is the competitive index given direct competition & available alternatives for the proposed offering by the venture ?', 
        'How strong is the team composition in terms of its complementary skills and completeness of critical functions ?', 
        'Does the lead have capability to hire and scale team effectively ?', 
        'Technology Barrier', 
        'Product Uniqueness', 
        'What is the level of competition in terms of alternatives available ?', 
        'Does the product work reliably ? What technical issues are the team facing in servicing their customers?', 
        'Do they do automated testing, TDD, BDD etc to deliver reliable software ?', 
        'How high are the chances for the business to extend beyond its currently served geographies ?', 
        'How high is trend momentum for the domain that startup is active in with its offerings ?', 
        'What would you say is your Unfair Advantage that would add competitive advantage vs anyone who could start the same venture ?', 
        'How large is the absolute market opportunity for the venture ?', 
        "Is the company filing for any relevant patents that are critical to the business's success?", 
        'Does the Tech leader have a vision for the product & company ?', 
        'How high is the defensibility of the solution from technology or any operating leverage point of view ?', 
        'How do you think is the ability of the teamto manage risks with Plan B ?', 
        'What functions are missing or outsourced?', 
        'Are the tech lead and team adequately incentivised (stocks, salary, etc.) to stay on for the long run ?', 
        'Revenue Stage', 
        'Revenue Risks', 
        'What is the overall feasibility of the business going forward ?', 
        'How did you find the overall presentation quality in terms of clarity and impact through communication ?', 
        'Are thebusiness milestones for the next 24 months exciting?', 
        'How high is the competitive advantage for this business ?', 
        'Potential Team Weakness', 
        'How high is the clarity and understanding of the team re: different customer personas ?', 
        'Adequate knowledge of marketing analytics and growth hacking tools', 
        'What is the strength of thecompetitive advantage in the business model?', 
        'Are they building the right capabilities for business growth ?', 
        'How high arethe defensible technology barriers in the business? (High being 4)', 
        'How would you rate the quality of presentation deck in terms of clarity, scope, visual impact u0026 simplicity ?', 
        'Will the tech lead be able to help the management with strategic decision making ?', 
        'How high did you sense was the passion of the founder/founding team ?', 
        'What is the quantum of tech gap between the company and the competition ?', 
        'How impressive is the early stage traction and adoption of the product in the market ?', 
        'Is the lead able to articulate business priorities, plan and execute effectively with the team along with founder/CEO ?', 
        'Overall Assessment', 
        'How well is the problem identified and defined?', 
        'How would you rate the likability u0026 connect with the Founder and his authenticity?', 
        'Does the tech leadership have a roadmap and plan?', 
        'Are the business metrics clearly defined', 
        'To what degree will the core technology be a differentiator ? ', 
        'What are the critical success factors for your venture type / category to succeed ?', 
        'How relevant do the metrics and milestones of of this business model appear ?', 
        'What is the geographic scope of operations in 2-3 years?', 
        'How high are the chances for the business to extend beyond its currently served markets ?', 
        'Does the lead have industry network, reputation and experience to get help on problems that are not his areas of expertise ?', 
        'What is the level of sustainability of the competitive advantage in the next 24 months?', 
        'Does the business team (Founder & CTO) understand the technological capabilities required ?', 
        'Does the lead code or is he a "tech manager" ?', 
        'What is the expected burn rate and does that correlate with roadmap and hiring plans ?', 
        'What is the level of pain area felt / perceived by the target customers / consumers?', 
        'How would you quantify the traction of the venture?', 
        'How unique & differentiated is the value proposition ?', 
        'Is it just a demo product or is it in the hands of customers ? Are there real customers apart from friends and family ?', 
        'Competitive Advantage', 
        'How high is the strength of revenue projection in the business model ?', 
        'Is the architecture robust and scalable ? Is it modular ?', 
        'Is the company developing any IP ?', 
        'Does the team do CI / CD? Adequate knowledge of infra, PaaS and SaaS tools', 
        'Does the team have relevant skill sets & work experience ?', 
        'Does the business model has high level of operating leverage u0026 scalability potential ?', 
        'What is the weakest link inthe teamcomposition? What would help solving them?', 
        'Is the business tech driven or is tech an enabler ?', 
        'How lucrative does the exit potential for this business appears with either of the possible ways viz: potential trade sales or M&A with big Cos or IPO etc. ?']


def au_map(rating):
    rating = rating.lower()
    if('highly' in rating): return 2
    elif('general' in rating): return 1
    else: return 0
def aw_map(rating):
    rating = rating.lower()
    if('unique' in rating): return 2
    elif('differentiated' in rating): return 1
    else: return 0 
def ax_map(rating):
    rating = rating.lower()
    if('successful' in rating): return 2
    elif('logical' in rating): return 1
    else: return 0
def ay_map(rating):
    rating = rating.lower()
    if('steady' in rating): return 2
    elif('imminent' in rating): return 1
    else: return 0
def az_map(rating):
    rating = rating.lower()
    if('strong' in rating): return 2
    elif('unique' in rating): return 1
    else: return 0
def oth_map(rating):
    rating = rating.lower()
    if('high' in rating): return 2
    elif('med' in rating): return 1
    else: return 0

## Normalize numerical ordinal data;
def feed_numer_data(chp_rst_pd_dt,col,outp_df):
    try: col_ser = chp_rst_pd_dt[col]
    except: return outp_df
    col_ser = col_ser / col_ser.max()
    outp_df[col] = col_ser
    return outp_df

## Replace categorical ordinal data with numerical equivalent; then normalize;
def feed_cat_ord_data(chp_rst_pd_dt,col,col_let,outp_df):
    try: col_ser = chp_rst_pd_dt[col]
    except: return outp_df
    col_ser_l = col_ser.tolist()
    ## print("col_ser_l: ", col_ser_l)
    ## print("col: ", col)
    if(col_let=='AU'): col_ser = list(map(au_map, col_ser_l))
    elif(col_let=='AW'): col_ser = list(map(aw_map, col_ser_l))
    elif(col_let=='AX'): col_ser = list(map(ax_map, col_ser_l))
    elif(col_let=='AY'): col_ser = list(map(ay_map, col_ser_l))
    elif(col_let=='AZ'): col_ser = list(map(az_map, col_ser_l))
    else: col_ser = list(map(oth_map, col_ser_l))
    ## print("col_ser: ", col_ser)
    col_ser = [elem/max(col_ser) for elem in col_ser]
    outp_df[col] = col_ser
    ## print(outp_df)
    return outp_df


## Replace present columns with 1's, empty/nan columns with 0's;
def feed_bin_pos(chp_rst_pd_dt,col,outp_df):
    try: col_ser = chp_rst_pd_dt[col]
    except: return outp_df
    def bin_pos_map(inp):
        return int(inp==inp)
    col_ser_l = col_ser.tolist()
    col_ser = list(map(bin_pos_map, col_ser_l))
    outp_df[col] = col_ser
    return outp_df 

## Replace 'yes's' with 1's, and 'no's' with 0's; 
def feed_bin_pres(chp_rst_pd_dt,col,outp_df):
    try: col_ser = chp_rst_pd_dt[col]
    except: return outp_df
    col_ser_l = col_ser.tolist()
    def bin_pres_map(inp):
        return int((inp==1) or (inp=='1') or (inp=='Yes'))
    col_ser = list(map(bin_pres_map, col_ser_l))
    outp_df[col] = col_ser
    return outp_df

## Apply VADER Analysis on text; feed composite score to outp_df
def feed_comm_data(chp_rst_pd_dt,col,outp_df):
    try: col_ser = chp_rst_pd_dt[col]
    except: return outp_df
    col_ser_l = col_ser.tolist()
    def comm_map(item):
        if(type(item)==float and isn(item)): return 0.5
        scores = sia_ana.polarity_scores(item)
        return (scores['compound']+1)/2
    col_ser = list(map(comm_map, col_ser_l))
    outp_df[col] = col_ser
    return outp_df

## preprocess data, and feed into empty dataframe
def pre_proc_data(chp_rst_pd_dt):
    outp_df = pd.DataFrame()
    for ind, col in enumerate(chp_rst_pd_dt):
        if(ind>0): #skip the first column (nan)
            col_let = g_c_l(ind+1)  
            if(col_let=='B' or col_let=='C'): outp_df[col] = chp_rst_pd_dt[col]
            elif(col_let in NUMER_DATA): outp_df = feed_numer_data(chp_rst_pd_dt,col,outp_df)
            elif(col_let in CAT_ORD_DATA): outp_df = feed_cat_ord_data(chp_rst_pd_dt,col,col_let,outp_df)
            ## elif(col_let in BIN_POS): outp_df = feed_bin_pos(chp_rst_pd_dt,col,outp_df)
            elif(col_let in BIN_PRES): outp_df = feed_bin_pres(chp_rst_pd_dt,col,outp_df)
            elif(col_let in COMM_DATA): outp_df = feed_comm_data(chp_rst_pd_dt,col,outp_df)
            else: continue

    return outp_df



## Read data into pandas dataframe 
def main():
    ext = '//Code//Code (A)//Chap//flt_s0_chp_ev.data'
    PATH_DATA = os.getcwd()+ext
    print("PATH_DATA: ",PATH_DATA)
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
        
    outp_arr = ['testingflt_chp_ev...'] ## THE ACTUAL OUTPUT.

    ###### THE ACTUAL ANALYTICS PROCESS ###### - normalize chaperone data 1-4 --> 0.25-1.0
    chp_rst_pd_dt = pd.read_excel(chp_sheet, sheet_name=res)
    chp_rnk_pd_dt = pd.read_excel(chp_sheet, sheet_name=rnk)
    rnk_col_len = len(chp_rnk_pd_dt.columns)
    chp_rnk_pd_dt1,chp_rnk_pd_dt2=chp_rnk_pd_dt.iloc[:,range(2)],chp_rnk_pd_dt.iloc[:,range(rnk_col_len-2,rnk_col_len)]
    chp_rnk_pd_dt1.columns, chp_rnk_pd_dt2.columns = chp_rnk_pd_dt1.iloc[0,], chp_rnk_pd_dt2.iloc[0,]
    chp_rnk_pd_dt1, chp_rnk_pd_dt2 = chp_rnk_pd_dt1.iloc[1:,], chp_rnk_pd_dt2.iloc[1:,]
    ## print(chp_rnk_pd_dt)
    ## print(chp_rnk_pd_dt1)
    ## print(chp_rnk_pd_dt2)
    
    chp_rst_pd_dt.columns = chp_rst_pd_dt.iloc[0]
    chp_rst_pd_dt = chp_rst_pd_dt.drop(chp_rst_pd_dt.index[0],axis=0)
    ## print(chp_rst_pd_dt.columns[1])
    ## print(chp_rst_pd_dt)
    ## print(chp_rst_pd_dt.columns, len(chp_rst_pd_dt.columns))
    
    outp_df = pre_proc_data(chp_rst_pd_dt).dropna()
    print('outp_df: ', outp_df)
    outp_df.to_csv('chap_norm.csv')
    ##########################################

    PATH_WRT_BCK = os.path.join(os.getcwd(),'pop_pg.data') #after the change...
    print("PATH_WRT_BCK: ",PATH_WRT_BCK)
    with open(PATH_WRT_BCK,'w+') as f_path_w:
        f_path_w.write(json.dumps(outp_arr))

    print(chp_rst_pd_dt)
    print("g_c_l(1): ", g_c_l(1))
    

main()
