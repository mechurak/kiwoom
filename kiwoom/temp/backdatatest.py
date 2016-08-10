import pandas as pd
import pandas.io.data as web
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.finance import candlestick_ohlc
from matplotlib.dates import date2num

market = 1
# from pandas import DataFrame
fw = open('summary.txt', 'w')
fwr = open('summary_rank.txt', 'w')

#fw = open('summary2.txt', 'w')
#fwr = open('summary_rank2.txt', 'w')

rank = []
drawing = 0

# add columns needed
def Download_Lastest_Data(name, start, Baseline, Crossline):
	end = datetime.now()
	if market == 1:
		DB = web.DataReader(name + str('.KS'), "yahoo", start, end)
	else:
		DB = web.DataReader(name + str('.KQ'), "yahoo", start, end)
	if (Baseline != 'Adj Close'):
		DB[Baseline] = pd.stats.moments.rolling_mean(DB['Adj Close'], int(Baseline[2:]) )

	# MA
	# Crossline : the target MA
	DB[Crossline] = pd.stats.moments.rolling_mean(DB['Adj Close'], int(Crossline[2:]) )
	DB['MA15'] = pd.stats.moments.rolling_mean(DB['Adj Close'], 15 )
	DB['MA20'] = pd.stats.moments.rolling_mean(DB['Adj Close'], 20 )
	DB['MA60'] = pd.stats.moments.rolling_mean(DB['Adj Close'], 60 )
	DB['MA120'] = pd.stats.moments.rolling_mean(DB['Adj Close'], 120 )
	DB['MA200'] = pd.stats.moments.rolling_mean(DB['Adj Close'], 200 )
	DB['MA240'] = pd.stats.moments.rolling_mean(DB['Adj Close'], 240 )
	DB['DIFF'] = (DB[Baseline] - DB[Crossline])  # 'Adj Close' 'MA30'
	# BollingerBand
	DB['BBUP'] = DB['MA20'] + pd.stats.moments.rolling_std(DB['Adj Close'], 20 )*2 # bollinger band, BBUP = upper, BBCT = center, BBLW = lower
	DB['BBCT'] = DB['MA20']
	DB['BBLW'] = DB['MA20'] - pd.stats.moments.rolling_std(DB['Adj Close'], 20 )*2
	# Envelope
	DB['ENUP'] = DB['MA20'] * 1.2 # bollinger band, BBUP = upper, BBCT = center, BBLW = lower
	DB['ENCT'] = DB['MA20']
	DB['ENLW'] = DB['MA20'] * 0.8


	# plt.plot(DB.index, DB['Adj Close'], 'r')
	# plt.plot(DB.index, DB['MA240'], 'b')
	# plt.plot(DB.index, DB['D240'], 'g')
	# plt.axhline(y=0.0, xmin=0, xmax=1, hold=None)
	# plt.show()
	DB.to_csv(name + str('.csv'))



def Calculate_Profit(name):
	DB = pd.read_csv(name)
	#print(DB)

	# Golden Cross

	# BB : MA20 += 2*moving_std

	# envelope : MA20 +- 20%

	# result would be as following orders:
	# MA15, MA20, MA60, MA120, MA200, MA240, BB, EN
	# number, gain for each item
	# rank 1~8

	init_deposit = 100000000.0
	final_deposit = init_deposit #initial setting
	number = 0 # how many transactions happen?
	buy = 0.0
	sell = 0.0
	STOCKS = 0 # number of stocks
	isOpenPosition = False

	# for testing
	for index, row in DB.iterrows():
		#print("index and row", index, row)
		price = DB['Adj Close']
		ma15 = DB['MA15']
		#ma20 = DB['MA20']
		#ma60 = DB['MA60']
		#ma120 = DB['MA120']
		#ma200 = DB['MA200']
		#ma240 = DB['MA240']
		#bbup = DB['BBUP']
		#bbct = DB['BBCT']
		#bblw = DB['BBLW']
		#enup = DB['ENUP']
		#enct = DB['ENCT']
		#enlw = DB['ENLW']

		if price[index] >= ma15[index] and isOpenPosition == False:
			print("Golden Cross")
			number += 1
			buy = price[index]
			STOCKS = (int)(final_deposit/buy)
			isOpenPosition = True
		elif price[index]  < ma15[index]  and isOpenPosition == True:
			print("Dead Cross")
			number += 1
			sell = price[index]
			final_deposit = STOCKS * price
			STOCKS = 0
			isOpenPosition = False
		elif price[index]  < ma15[index]  and isOpenPosition == True:
			continue


	print(name, final_deposit)





def Read_CVS_Files(name, Baseline, Crossline):
	DB = pd.read_csv(name)

	oldValue = 0.0
	Initial_Account_Value = 10000000.0  #
	Total_Value = Initial_Account_Value
	Quantity = 0  # number of stock purchased
	Change = 0.0
	BUY = 0.0
	SELL = 0.0
	BUY_Date = ""
	SELL_Date = ""
	BUY_Index = 0
	SELL_Index = 0
	isOpenPosition = False
	Trade_Index = 0
	ohlc = []
	DateIndex = []
	for index, row in DB.iterrows():
		Date = row['Date']
		Price = row[Baseline]  # 'Adj Close' 'MA30'
		MA240 = row[Crossline]
		Value = row['DIFF']
		if (oldValue < 0.0 and Value >= 0.0):  # BUY ( minus(-) to plus(+) )
			isOpenPosition = True
			BUY = Price
			BUY_Date = Date
			BUY_Index = index
			Quantity = int(Total_Value / Price)
		# print("%4d, Date:%s Price:%8.2f, MA240:%8.2f, %8.2f %8.2f BUY@ %8.2f" % (index, Date, Price, MA240,  oldValue, Value, Price))
		elif (oldValue >= 0.0 and Value < 0.0 and isOpenPosition == True):
			SELL = Price
			SELL_Date = Date
			SELL_Index = index
			GainLoss = (SELL - BUY) * float(Quantity)
			Change = ((SELL - BUY) / BUY) * 100.0
			Total_Value += GainLoss
			Trade_Index += 1
			Hold_Period = (SELL_Index - BUY_Index)
			isOpenPosition = False
			#print("[%2d] Total Value: %15.2f,  Gain/Loss:%12.2f   Qty:%4d  Chg:%7.2f%%  Hold Period:%4d (BUY %s @%9.2f => SELL %s @%9.2f)" % (
			#	Trade_Index, Total_Value, GainLoss, Quantity, Change, Hold_Period, BUY_Date, BUY, SELL_Date, SELL))
		# print("%4d, Date:%s Price:%8.2f, MA240:%8.2f, %8.2f %8.2f             SELL@ %8.2f" % (index, Date, Price, MA240,  oldValue, Value, Price))
		# else:
		# print("%4d, Date:%s Price:%8.2f, MA240:%8.2f, %8.2f %8.2f" % (index, Date, Price, MA240,  oldValue, Value))
		oldValue = Value
		#append_me = date2num(datetime.strptime(Date,"%Y-%m-%d")), row['Open'], row['High'], row['Low'], row['Close'], row['Volume']
		#ohlc.append(append_me)
		DateIndex.append(date2num(datetime.strptime(row['Date'],"%Y-%m-%d")))

	# Calculate any open position into Account
	if (isOpenPosition == True):
		SELL = Price
		SELL_Date = Date
		SELL_Index = index
		GainLoss = (SELL - BUY) * float(Quantity)
		Change = ((SELL - BUY) / BUY) * 100.0
		Total_Value += GainLoss
		Trade_Index += 1
		Hold_Period = (SELL_Index - BUY_Index)
		#print("[%2d] Total Value:%15.2f,  Gain/Loss:%12.2f   Qty:%4d  Chg:%7.2f%%  Hold Period:%4d (BUY %s @%9.2f => SELL %s @%9.2f)" % (
		#	Trade_Index, Total_Value, GainLoss, Quantity, Change, Hold_Period, BUY_Date, BUY, SELL_Date, SELL))

	Investment = '{:,.0f}'.format(Initial_Account_Value)
	Current_Value = '{:,.0f}'.format(Total_Value)
	Net_Profit = '{:,.0f}'.format(Total_Value - Initial_Account_Value)

	#fw = open(KOSPI+str('.txt'), 'w')

	#fw.write("adj %s & ma240 %s " % (row[Baseline], row[Crossline]))

	# sweet or not sweet is not working properly. why?
	if ((row[Baseline] >= 5000) and (row[Baseline] > row[Crossline])):# Baseline : adj con & Crossline : MA240 - standard line
		fw.write("Sweet ")
		fwr.write("%s %s\n" % (KOSPI, (row[Baseline] - row[Crossline]) / row[Baseline]))
	else:
		fw.write("Not_Sweet ")

#	print("SUMMARY: Investment= ₩%s, Current Value= ₩%s  Net Profit= ₩%s  ROI= %.2f" % (
#	Investment, Current_Value, Net_Profit, (Total_Value / Initial_Account_Value)))

	#fw.write("%s SUMMARY: Investment=₩%s, Current_Value=₩%s  Net_Profit=₩%s  ROI= %.2f" % (KOSPI,
	#Investment, Current_Value, Net_Profit, (Total_Value / Initial_Account_Value)))
	fw.write("%s %s %s %s %s\n" % (KOSPI, row[Baseline], row[Crossline], row[Baseline]-row[Crossline], (row[Baseline]-row[Crossline])/row[Baseline])) # code, difference, roi

	#DB['DateIdx'] = datetime.strptime(DB['Date'],"%Y-%m-%d")

	# Display Chart
	if drawing == 1:
		if ((row[Baseline] >= 5000) and (row[Baseline] > row[Crossline])):
			scale = 1.5
			fig = plt.figure(figsize=(6 * scale, 4 * scale))
			# fig.set_size_inches(20,10)
			chart = plt.subplot(1, 1, 1)
			# chart.plot_date(DB['Date'], DB[Baseline], 'r', label='Close') #'Adj Close' 'MA30
			chart.plot_date(DateIndex, DB[Baseline], 'r', label=Baseline)  # 'Adj Close' 'MA30
			chart.plot_date(DateIndex, DB[Crossline], 'b', label=Crossline)
			chart.plot_date(DateIndex, DB['DIFF'], 'g', label='Difference')
			#candlestick_ohlc(chart, ohlc, width=0.4, colorup='#77d879', colordown='#db3f3f')

			plt.axhline(y=0.0, xmin=0, xmax=1, hold=None)
			plt.title(name[:-4]+" "+Crossline+'-based trading back test')
			plt.xlabel('Date')
			plt.ylabel('Price')
			plt.legend()
			plt.grid(True)
			#plt.xticks(rotation=70)
			plt.subplots_adjust(left=0.05, bottom=0.05, right=0.96, top=0.96, wspace=0.2, hspace=0)

			#plt.show()
			fig.savefig(KOSPI+str('.png'), dpi=600)

# hot codes


# report
def summaryrank():
	fs = open('summary_rank.txt')
	slist = fs.readlines()

	summary = {}

	for item in slist:
		item = item.split()
		summary[item[0]] = item[1]
	print(summary)

if __name__ == "__main__":

	if market == 1:
		f = open("YAHOO_KOSPI.txt")
	else:
		f = open("YAHOO_KOSDAQ.txt")

	#f = open("kospi_1.txt")
	#f = open("kospi_2.txt")
	lists = f.readlines()

	#print(len(lists))
	test = 1

	if test == 1:
		tmp = 0

	for item in lists:
		if test == 1:
			tmp += 1
			if tmp == 10:
				break
		code = item.split('\n')[0]

		KOSPI 		= code #'003490'  # 003490, 005930
		Baseline 	= 'Adj Close'  # 'Adj Close', 'MA5', 'MA10', 'MA30', 'MA60' Don't change it
		Crossline 	= 'MA240'
		Start_Date 	= datetime(2010,1,1)

		try:
			Download_Lastest_Data(KOSPI, Start_Date, Baseline, Crossline)
			#Read_CVS_Files(KOSPI+'.csv', Baseline, Crossline)
			Calculate_Profit(KOSPI+'.csv')
		except:
			print("Error :", code)

	# rank
	summaryrank()