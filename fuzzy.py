import crawler
import calculator
import pandas

def RuleCalc(propensity):
    ########################################
    # Rule evaluation - The rules are different according to user's propensity
    # propensity 1 - conservative propensity
    # rule1
    # IF safety / low
    # and returns / high
    # then importance / low
    #
    # rule2
    # IF safety / high
    # and returns / low
    # then importance / high
    #
    # rule3
    # IF safety / middle
    # and returns / high
    # then importance / middle
    #########################################
    if propensity=='conservative':
        setHigh=[]
        for index, x in fuzzyDf.iterrows():
            setHigh.append(x['SafetyHigh']*x['returnLow'])
        fuzzyDf['setHigh']=setHigh

        setMid=[]
        for index, x in fuzzyDf.iterrows():
            setMid.append(x['SafetyMid']*x['returnHigh'])
        fuzzyDf['setMid']=setMid

        setLow=[]
        for index, x in fuzzyDf.iterrows():
            setLow.append(x['SafetyLow']*x['returnHigh'])
        fuzzyDf['setLow']=setLow
        return fuzzyDf['setHigh'],fuzzyDf['setMid'],fuzzyDf['setLow']
    ########################################
    # propensity 2 - moderate propensity
    # rule1
    # IF safety / low
    # and returns / high
    # then importance / middle
    #
    # rule2
    # IF safety / high
    # and returns / low
    # then importance / low
    #
    # rule3
    # IF safety / middle
    # and returns / high
    # then importance / high
    #########################################
    elif propensity=='moderate':
        setHigh=[]
        for index, x in fuzzyDf.iterrows():
            setHigh.append(x['SafetyMid']*x['returnHigh'])
        fuzzyDf['setHigh']=setHigh

        setMid=[]
        for index, x in fuzzyDf.iterrows():
            setMid.append(x['SafetyHigh']*x['returnLow'])
        fuzzyDf['setMid']=setMid

        setLow=[]
        for index, x in fuzzyDf.iterrows():
            setLow.append(x['SafetyLow']*x['returnHigh'])
        fuzzyDf['setLow']=setLow
        return fuzzyDf['setHigh'],fuzzyDf['setMid'],fuzzyDf['setLow']
    
    ########################################
    # propensity 3 - aggresive propensity
    # rule1
    # IF safety / low
    # and returns / high
    # then importance / high
    #
    # rule2
    # IF safety / high
    # and returns / low
    # then importance / low
    #
    # rule3
    # IF safety / middle
    # and returns / high
    # then importance / middle
    #########################################
    elif propensity=='aggresive':
        setHigh=[]
        for index, x in fuzzyDf.iterrows():
            setHigh.append(x['SafetyLow']*x['returnHigh'])
        fuzzyDf['setHigh']=setHigh

        setMid=[]
        for index, x in fuzzyDf.iterrows():
            setMid.append(x['SafetyMid']*x['returnHigh'])
        fuzzyDf['setMid']=setMid

        setLow=[]
        for index, x in fuzzyDf.iterrows():
            setLow.append(x['SafetyHigh']*x['returnLow'])
        fuzzyDf['setLow']=setLow
        return fuzzyDf['setHigh'],fuzzyDf['setMid'],fuzzyDf['setLow']

domesticDf=crawler.GetDf('http://info.finance.naver.com/fund/fundTypeEarningRate.nhn?ivstAreaWorldYn=N')
overseasDf=crawler.GetDf('http://info.finance.naver.com/fund/fundTypeEarningRate.nhn?ivstAreaWorldYn=Y')

earningRateDf = domesticDf.append(overseasDf, ignore_index=True)
earningRateDf = calculator.GetCalc(earningRateDf)

domesticDf=calculator.GetCalc(domesticDf)
overseasDf=calculator.GetCalc(overseasDf)

domesticStockDf = domesticDf[domesticDf['대유형'].str.contains("주식")].reset_index(drop=True)
domesticBondDf= domesticDf[domesticDf['대유형'].str.contains("채권")].reset_index(drop=True)

overseaStockDf = overseasDf[overseasDf['대유형'].str.contains("주식")].reset_index(drop=True)
overseaBondDf = overseasDf[overseasDf['대유형'].str.contains("채권")].reset_index(drop=True)

realestateDf =  earningRateDf[earningRateDf['대유형'].str.contains("부동산")].reset_index(drop=True)
cashDf =  earningRateDf[earningRateDf['대유형'].str.contains("MMF")].reset_index(drop=True)

resultDf = pandas.DataFrame(columns=earningRateDf.columns)
dfList = [domesticStockDf,domesticBondDf,overseaStockDf,overseaBondDf,realestateDf,cashDf]

for x in dfList:
    if x.empty==False:
        resultDf = resultDf.append(x.iloc[0])

fuzzyDf=pandas.DataFrame()
fuzzyDf['대유형']=resultDf['대유형']

###############################################
# Fuzzyfication
# x를 계산하는 함수는 설문조사 혹은 인공지능에 따라 함수 변경 가능
# x/15-(16/3)같은 부분을 함수화 시켜 차후 DB와 연동.
##############################################
safetyHigh=[]
for x in resultDf.Safety:
    if x>80 and x<95:
        safetyHigh.append(x/15-(16/3))
    elif x>=95:
        safetyHigh.append(1)
    else:
        safetyHigh.append(0)
fuzzyDf['SafetyHigh']=safetyHigh

safetyMid=[]
for x in resultDf.Safety:
    if x>50 and x<=75:
        safetyMid.append(x/25-2) 
    elif x>75:
        safetyMid.append(-(x/25)+4)
    else:
        safetyMid.append(0)
fuzzyDf['SafetyMid']=safetyMid

safetyLow=[]
for x in resultDf.Safety:
    if x>=20 and x<=(160/3):
        safetyLow.append(-(x*3/100)+(8/5)) 
    elif x<20:
        safetyLow.append(1)
    else:
        safetyLow.append(0)
fuzzyDf['SafetyLow']=safetyLow

returnHigh=[]
for x in resultDf['기대수익률']:
    if x>=2 and x<8:
        returnHigh.append(x/6-(1/3)) 
    elif x>=8:
        returnHigh.append(1)
    else:
        returnHigh.append(0)
fuzzyDf['returnHigh']=returnHigh

returnLow=[]
for x in resultDf['기대수익률']:
    if x>=2 and x<4:
        returnLow.append(-(x/4)+1) 
    elif x<2:
        returnLow.append(1)
    else:
        returnLow.append(0)
fuzzyDf['returnLow']=returnLow

propensity = 'moderate'
fuzzyDf['setHigh'],fuzzyDf['setMid'],fuzzyDf['setLow'] = RuleCalc(propensity)

##############################################
# Defuzzification uses COG
##############################################
fuzzyDf['COG']=\
fuzzyDf['setLow']*(10+20)+fuzzyDf[['setMid','setLow']].max(axis=1)*(30+40)\
+fuzzyDf['setMid']*50+fuzzyDf[['setHigh','setMid']].max(axis=1)*(60+70)+fuzzyDf['setHigh']*(80+90+100)

resultDf['percentage']=(fuzzyDf['COG']/fuzzyDf['COG'].sum()).round(2)
resultReturn = resultDf['기대수익률']*resultDf['percentage']
print (pandas.DataFrame(resultDf[['소유형','기대수익률','percentage']]))

print (propensity, 'expected return:',resultReturn.sum()) # expected return