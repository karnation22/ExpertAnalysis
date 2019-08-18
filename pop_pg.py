import psycopg2 as pg2 
import names
import pandas as pd
import os, sys, pathlib
import pickle
import json
import Crypto.Random.OSRNG
import argparse
from random import choice, randint
from configparser import ConfigParser as CP 

TOT_DATA_PTS = 1000
SHOW_TABS = "\dt"
TAB_QUERY = "SELECT TABLE_NAME, TABLE_TYPE, TABLE_SCHEMA FROM information_schema.tables"
COL_QUERY = "SELECT COLUMN_NAME, DATA_TYPE FROM information_schema.columns"
OVERALL_QUERY = "SELECT TABLE_NAME, TABLE_SCHEMA, COLUMN_NAME, DATA_TYPE FROM information_schema.columns"
INSRT_ASSMT_CLS = "INSERT INTO assessments (question, a_number, evaluation_id, typeform_id, a_text, a_bool, a_type, a_options) VALUES "
RECIEVE_ASSMT_CLS = "SELECT startups.season_id,startups.name,evaluations.role,users.name,assessments.question,assessments.a_number,assessments.a_text\
     FROM assessments,evaluations,startups,users WHERE startups.id=evaluations.startup_id and assessments.evaluation_id=evaluations.id and evaluations.user_id=users.id;"
INSERT_ANALYTICS_TABLE = "INSERT INTO analytics VALUES ({} {} {} {} {} {} {} {} {})"
INSRT_EVL_CLS = "INSERT INTO evaluations (role) VALUES  "
INSRT_STUP_CLS = "INSERT INTO startups (name) VALUES " #just the name for now...
DEL_CONT = "TRUNCATE assesments, evaluations, startups;"
CODE_PATH_STR = "//Code//Code ({})"
ANA_L = ['A','B','C','D']
SUB_DIR = [['//Chap','//Judge'],['//drp_dwn_3','//exp_jdg_nrm','//rnk_cmp'],[''],['']]
PY_FILES =[ [['//flt_s0_chp_ev.py','//fnd_tp_n_chp.py'],['//fnd_tp_n_jud.py']], \
    [['//chp_to_exp.py','//chp_to_jud.py','//exp_to_jud.py'],['//exp_nrm.py','//jdg_nrm.py'],\
    ['//rnk_chp_cmp.py','//rnk_exp_cmp.py','//rnk_jdg_cmp.py']],[['//gen_wght_mtrx.py']],\
    [['//det_wght_ech_q.py','//prm_to_excel.py']]  ]
rel_tabs = ['assessments', 'evaluations', 'startups']
ROLES = ['mentor', 'expert', 'tech', 'judge']


CHAP_Q = [
    "'How well is the problem identified and defined? '", 
    "'What is the level of pain area felt / perceived by the target customers / consumers?'",
	"'What is the level of uniqueness in the proposition for the venture?'",
    "'How high are the defensible technology barriers in the business? (High being 4)'",
    "'What is the strength of the competitive advantage in the business model?'",	
    "'What is the level of competition in terms of alternatives available ?'"	
    "'Low Price'","'Superior Quality'",	"'Distribution Leverage'", "'Geographic Presence'",	"'Other'",	
    "'What is the level of sustainability of the competitive advantage in the next 24 months?'",
    "'What is the geographic scope of operations in 2-3 years?'",
    "'No Traction yet'", "'Some Free Customers'", 
    "'Lots of Free Customers'",	"'Some Paid Customers'", "'Growing Fast'",	"'Other'",	
    "'Are the business milestones for the next 24 months exciting?'",	
    "'Are the business metrics clearly defined'",	"'Other'",	"'Please rank from high to low the risks to your revenue in next 24 months ?'",
    "'How feasible do you think is the Go To Market plan in next 12-18 month timeframe ?'",	
    "'What is the level of understanding and clarity of the financial projections by the team ?'",	
    "'Does the business model has high level of operating leverage & scalability potential ?'",	
    "'How do you think is the ability of the team to manage risks with Plan B ?'",	
    "'What would you say is your ‘Unfair Advantage’ that would add competitive advantage vs anyone who could start the same venture ?'",	
    "'How would you rate the likability & connect with the Founder and his authenticity?'",
    "'Lack of complementary Co-Founder'",	"'No Tech Leadership'",	"'Quality of Developers'", "'Business Dev'", "'Marketing'",	"'Other'",
    "'Tech'", "'Marketing'","'Biz Dev'", "'Fund Raise'", "'Other'",	
    "'How did you find the overall presentation quality in terms of clarity and impact through communication ?'",	
    "'How would you rate the quality of presentation deck in terms of clarity, scope, visual impact & simplicity ?'",
    "'What is the overall feasibility of the business going forward ?'",
    "'Relevant Industry/market background of team'",	"'Addressable Market Size'", "'Technology Barrier'", "'Go to market plan strength'", 
    "'Revenue Stage'", "'Product Uniqueness'", "'Additional Comments'"
]
EXP_Q = [
    "'How high is the clarity and understanding of the team re: different customer personas ?'",
    "'How unique & differentiated is the value proposition ?'",
    "'How large is the absolute market opportunity for the venture ?'",
    "'How impressive is the early stage traction and adoption of the product in the market ?'",
    "'How high is the competitive index given direct competition & available alternatives for the proposed offering by the venture ?'",
    "'How high is the strength of revenue projection in the business model ?'",
    "'How lucrative does the exit potential for this business appears with either of the possible ways viz: potential trade sales or M&A with big Cos or IPO etc. ?'",
    "'How high is trend momentum for the domain that startup is active in with its offerings ?'",
    "'How relevant do the metrics and milestones of of this business model appear ?'",
    "'How high is the defensibility of the solution from technology or any operating leverage point of view ?'",
    "'How high is the business momentum and pipeline of business ?'",
    "'How high are the chances for the business to extend beyond its currently served markets ?'",
    "'How high is the competitive advantage for this business ?'",
    "'How high are the chances for the business to extend beyond its currently served geographies ?'",
    "'Overall Assessment'"
]

JUD_Q = [
    "'Value Propostion'",	"'Market Size & Growth rate'", "'Operating leverage'",	"'Margin structure'",	"'Revenue'",	"'Clarity of vision'", "'Knowledge of customer'", "'Team dynamics'",
    "'Key man risk'",	"'Humility / arrogance of founders'",	"'Cultural values'", "'Learnability of management team'",	"'Founder Reserve & Life-cycle'",	"'Funding Pipeline'",	"'Time Commitment'",	"'% net worth invested'",
    "'Motivation'",	"'Potential vendor possibility with Corporates'",	"'Potential trade/ strategic sales to corporates'",	"'Attractive valuation for new investors'",	"'News momentum to catch investor attention'",	
    "'Network'",	"'Founder orientation'",	"'Cash generating potential'",	"'Skin in the game'",	"'Staying power'", "'Corporate interest'",	"'Team longevity and quality'",	"'Customer understanding'",	"'VC proposition'",
    "'Overall Investibility'", "'Overall Assessment Comments'"

]

def generate_random_data():
    nm_l = []
    role_l = []
    for _ in range(TOT_DATA_PTS):
        nm_l.append("'" + names.get_first_name()+"'")
        role_i = choice(ROLES)
        role_d = {}
        role_q = []
        role_r = []
        if(role_i=='expert'):
            role_q = EXP_Q
            for exp_q in CHAP_Q:
                role_r.append(randint(1,4))
        elif(role_i=='judge'):
            role_q = JUD_Q
            for jdg_q in JUD_Q:
                role_r.append(randint(1,4))
        elif(role_i=='tech'):
            role_q = CHAP_Q
            for chp_q in CHAP_Q:
                role_r.append(randint(1,4))
        else: continue
        role_d[role_i] = zip(role_q, role_r)
        role_l.append(role_d)
    return nm_l, role_l

def config(file_params='database.ini', section='postgresql'):
    parser = CP()
    parser.read(file_params)
    db_prms={}
    if parser.has_section(section):
        params = parser.items(section)
        for key,val in params:
            db_prms[key] = val
    return db_prms

def f1_substr_val(role_d_role_i):
    val_substr = ""
    for q, rat in role_d_role_i:
        val_substr += "({}, {}, {}, {}, {}, {}, {}, {}),".format(q, rat, "-1", "_", "_", "_", "false", "_", "{}")
    return val_substr[:-1]+";"

def f2_substr_val(role_d):
    val_substr = ""
    for role_i in role_d:
        val_substr += "({}),".format(role_i)
    return val_substr[:-1]+";"

def f3_substr_val(names_l):
    val_substr = ""
    for nm in names_l:
        val_substr += "({}),".format(nm)
    return val_substr[:-1]+";"

## 1) connect to the database and show basics
## 2) randomly insert 1000 (TOTAL_DATA_PTS) into tables...
def connect_and_load(bool_del):
    params = config()
    print("Connecting to PostrgreSQL database...") 
    conn = pg2.connect(**params)
    cursor = conn.cursor()
    print("PostgreSQL Version: ")
    cursor.execute("SELECT version()")
    db_ver = cursor.fetchone()
    print(db_ver)
    cursor.execute(OVERALL_QUERY)
    all_items = cursor.fetchall()
    print("All tables: ")
    names_l, roles_l = generate_random_data()
    for table_name, table_schema, col_name, data_type in all_items:
        if(table_name in rel_tabs):
            print("tb_nm: {}, tb_sch: {}, cl_nm: {}, dt_tp: {}".format(table_name, table_schema, col_name, data_type))
    for table_name in rel_tabs:
        if(table_name=="assessments"):
            for role_d in roles_l:
                for role_i in role_d:
                    # print(INSRT_ASSMT_CLS.format("question", "a_number", q, rat))
                    val_substr = f1_substr_val(role_d[role_i])
                    cursor.execute(INSRT_ASSMT_CLS+val_substr)
        if(table_name=="evaluations"):
            for role_d in roles_l:
                val_substr = f2_substr_val(role_d)
                cursor.execute(INSRT_EVL_CLS+val_substr)
        if(table_name=="startups"):
            val_substr = f3_substr_val(names_l)
            cursor.execute(INSRT_STUP_CLS+val_substr)
    if(bool_del): cursor.execute(DEL_CONT)
    ##cursor.commit()
    ##conn.commit()
    
    conn.close()
    return


def parse_input_params():
    parser = argparse.ArgumentParser(description='--Boolean flags for each analytics request...')
    parser.add_argument('--A',type=bool,default=False,help='Expert Curation')
    parser.add_argument('--B',type=bool,default=False,help='S4 to S1 funnel')
    parser.add_argument('--C',type=bool,default=False,help='Bias Weights Each Expert')
    parser.add_argument('--D',type=bool,default=False,help='Question Predictive Power')
    parser.add_argument('--season_id',type=int,default=-1,help='season_id for analytics request(s)')
    parser.add_argument('--bool_del',type=bool,default=False,help='delete database contents...')
    return vars(parser.parse_args())


## 1) Do analytics - write to analytics table...
def analytics(LET):
    CODE_PATH = CODE_PATH_STR.format(LET)
    prms = config()
    conn = pg2.connect(**prms)
    cursor = conn.cursor()
    ind = ANA_L.index(LET)
    for sub_dir,py_files in zip(SUB_DIR[ind],PY_FILES[ind]):
        for py_file in py_files:
            PATH_DATA = os.getcwd()+CODE_PATH+sub_dir+py_file[:-3]+".data" ##folder to store 'pickle'...
            
            PATH = os.getcwd()+CODE_PATH+sub_dir+py_file
            cursor.execute(RECIEVE_ASSMT_CLS.format(TOT_DATA_PTS))
            all_items_pre = cursor.fetchall()
            rounds = set(map(lambda x: x[2], all_items_pre))
            eval_ids = set(map(lambda x: x[3], all_items_pre))
            qs = list(set(map(lambda x: x[4], all_items_pre)))
            all_items = [[ [ list(item_tup[1:]) for item_tup in all_items_pre if item_tup[3]==eval_id \
                and (item_tup[2]==rnd)] for rnd in rounds] for eval_id in eval_ids]
            s_id = all_items_pre[0][0]
            #print('all_items_pre: ',all_items_pre)
            print('s_id: ',s_id)
            
            all_items = list(map(lambda itm: list(filter(lambda itm2: not(itm2==[]), itm )), all_items))
            ##print("all items: ", str(all_items))
            for items in all_items:
                print(items)
            with open(PATH_DATA,'w') as f:
                f.write(json.dumps(all_items)) ## dump data
            print("PATH: ",PATH)
            owd = os.getcwd()
            exec(open(PATH).read()) ##execute the actual file...
            return
            OUTP_DATA = os.getcwd()+py_file[:-3]+".data" # read back
            with open(OUTP_DATA,'w') as f_outp:
                f_outp_data = f_outp.read()
                OUTP_DATA = json.loads(f_outp_data)
            print("OUTP_DATA",OUTP_DATA)
            if(LET=="A"): cursor.execute(INSERT_ANALYTICS_TABLE.format(s_id,json.dumps(OUTP_DATA),True,None,None,None,None,None,None))
            elif(LET=="B"): cursor.execute(INSERT_ANALYTICS_TABLE.format(s_id,None,None,json.dumps(OUTP_DATA),True,None,None,None,None))
            elif(LET=="C"): cursor.execute(INSERT_ANALYTICS_TABLE.format(s_id,None,None,None,None,json.dumps(OUTP_DATA),True,None,None))
            else: cursor.execute(INSERT_ANALYTICS_TABLE.format(s_id,None,None,None,None,None,None,json.dumps(OUTP_DATA),True))
            return

            #for item_group in all_items:
            #    for item in item_group:
            #        print("item: ",item)
            #    print('\n')
    
    cursor.commit()        
    conn.commit()            


    print('\n\n')

def main():
    args = parse_input_params()
    print(args,type(args))
    #connect_and_load(args['bool_del'])
    for ANA in ANA_L:
        ## Skip analytics B request for now... ##
        print(ANA)
        if(not(ANA=='B') and args[ANA]): analytics(ANA)


main()

    




