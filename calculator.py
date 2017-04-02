import crawler
import pandas

def __init__(self):
    df
    
def GetCalc(df):
    ###########################################################
    # drop 조건
    # 1. 설정액이 1000억이하 섹터 drop.
    # 2. 한번이라도 수익률이 마이너스를 기록했던 섹터 drop.
    # 3. 국내채권,국내주식,해외채권,해외주식,부동산,현금으로 나누고 이 6개의 비중을 퍼지이론으로 조절하는 방식.
    ###########################################################
    
    df = df.drop(df[(df['설정액']<1000)].index) # 1번 조건 drop.
    
    df['MoMofQoQ'] = ((((100+df['3개월'])/100)**(1/3))-1)*100
    df['MoMofYoY'] = ((((100+df['1년'])/100)**(1/12))-1)*100    
    df = df.drop(df[(df.MoMofYoY<0)|(df.MoMofQoQ<0)|(df['1개월']<0)].index) # 2번 조건 drop.
    
    dfStd = df[['1개월','MoMofYoY','MoMofQoQ']].std(axis=1)
    df['Safety'] = (100-((dfStd - dfStd.min())/(dfStd.max()-dfStd.min()))*100)
    
    ReturnAdjValue = 1 # 수익성향보정치
    SafetyAdjValue = 1 # 안전성향보정치
    
    # 기대수익률 = (1개월, MoMofYoY, MoMofQoQ의 평균 수익률 * 수익성향보정치) * (안전도*안전성향보정치)
    df['기대수익률'] = (((df[['1개월','MoMofYoY','MoMofQoQ']].mean(axis=1)*ReturnAdjValue) * (df['Safety']*SafetyAdjValue) / 10000 + 1)**12-1)*100
    df = df.drop(['3개월','1년'],axis=1)
    
    df = df.sort_values(by=['기대수익률'], ascending=False)
    #df.reset_index(inplace=True, drop=True)
    return df