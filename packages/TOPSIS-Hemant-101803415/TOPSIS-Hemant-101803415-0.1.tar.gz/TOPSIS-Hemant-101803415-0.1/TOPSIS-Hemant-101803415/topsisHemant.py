def topsisfun(df,wt,impact,result):
    try:
        import logging
        import sys
        import pandas as pd
        import math
        from pandas.api.types import is_string_dtype
        from pandas.api.types import is_numeric_dtype    
        df1=df.copy()
        df.drop(df.columns[0],axis=1,inplace=True)
        for i in df.columns:
            if  not (is_numeric_dtype(df[i])):
                logging.warning('column contain other than numeric value')
                return
        lt=[math.sqrt(sum(df[i]*df[i])) for i in df.columns]
        k=0
        for i in df.columns:
            df[i]=df[i]/lt[k]
            df[i]*=wt[k]
            k=k+1
        vpos=list()
        vneg=list()
        k=0
        for i in df.columns:
            if impact[k]=='+':
                vpos.append(max(df[i]))
                vneg.append(min(df[i]))
            else:
                vneg.append(max(df[i]))
                vpos.append(min(df[i]))
            k=k+1
        spos=[math.sqrt(sum((df.loc[i]-vpos)*(df.loc[i]-vpos))) for i in df.index]
        sneg=[math.sqrt(sum((df.loc[i]-vneg)*(df.loc[i]-vneg))) for i in df.index]
        #ssum=[spos[k]+sneg[k] for k in range(len(spos))]
        perf=[sneg[i]/(sneg[i]+spos[i]) for i in range(len(sneg))]
        df1['topsis_score']=perf
        df1["Rank"] = df1["topsis_score"].rank(ascending=0) 

        #print(df1)
        #print(sneg)
        df1.to_csv(result)
    except:
        logging.warning('wrong file entered')

def topsis():
    try:
        import logging
        import sys
        import pandas as pd
        import math
        from pandas.api.types import is_string_dtype
        from pandas.api.types import is_numeric_dtype
        try:
            df=pd.read_csv(sys1)
        except:
            logging.warning('File Not Found or file is not .csv')
            return
        if len(df.columns)<3:
            logging.warning('Number of columns is less than 3')
            return
        elif (2*(len(df.columns)-1)-1)!=len(sys2):
            logging.warning("number of weights are different from number of columns")
            return
        elif (2*(len(df.columns)-1)-1)!=len(sys3):
            logging.warning("number of impact are different from number of columns")
            return
        i=0
        s=sys3
        impact=[]
        weights=[]
        while i<len(s):
            if i%2==0:
                if s[i]=='+' or s[i]=='-':
                    impact.append(s[i])
                    i+=1
                    continue
                else:
                    logging.warning('impact contains other char instead of + or -')
                    return
            else:
                if s[i]==',':
                    i+=1
                    continue
                else:
                    logging.warning('impact is not separated by commas')
                    return
        s=sys2
        i=0
        while i<len(s):
            if i%2==0:
                if s[i].isnumeric():
                    weights.append(int(s[i]))
                    i+=1
                    continue
                else:
                    logging.warning('weight contain no-numeric value instead of numeric value')
                    return
            else:
                if s[i]==',':
                    i+=1
                    continue
                else:
                    logging.warning('weight is not separated by commas')
                    return
        

        #print(weights)
        result=sys4
        topsisfun(df,weights,impact,result)
    except:
        logging.warning("check your dataframe")
        
        