import crawler
import calculator
import pandas

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
# 퍼지화
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

########################################
# 규칙계산 - 고객의 성향에 따라 규칙은 달라짐.
# 현재규칙 - 보수적 성향
# 규칙1
# IF 안전도가 / 낮다
# and 수익률이 / 높다
# then 비중이 / 낮다
#
# 규칙2
# IF 안전도가 / 높다
# and 수익률이 / 낮다
# then 비중이 / 보통이다
#
# 규칙3
# IF 안전도가 / 할만하다
# and 수익률이 / 높다
# then 비중이 / 높다
#########################################

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

##############################################
# COG 구할 차례
##############################################

fuzzyDf