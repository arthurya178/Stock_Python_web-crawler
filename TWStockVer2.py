import matplotlib.pyplot as plt
import matplotlib.font_manager
import requests
from bs4 import BeautifulSoup

url = "https://goodinfo.tw/StockInfo/StockBzPerformance.asp?STOCK_ID=2377&RPT_CAT=M%5FYEAR"

soup = ""
req = ""
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"}
dataTitle = ['年度', '股本(億)', '財報評分', '年度股價(元) 收盤', '年度股價(元) 平均', '年度股價(元) 漲跌', '年度股價(元) 漲跌(%)', '獲利金額(億) 營業收入',
             '獲利金額(億) 營業毛利', '獲利金額(億) 營業利益', '獲利金額(億) 業外損益', '獲利金額(億) 稅後淨利', '獲利率(%) 營業毛利',
             '獲利率(%) 營業利益', '獲利率(%) 業外損益', '獲利率(%) 稅後淨利', '獲利率(%) 營業毛利', '獲利率(%) 營業毛利', 'ROE(%)',
             'ROA(%)', 'EPS(元) 稅後EPS', 'EPS(元) 年增(元)', 'BPS(元)']
pyplotARGS = ['k--', 'g--', 'r--', 'b--']
selectList = []
plotColor = 0
dataList = [[]]


def createSlot(numberOfAddon):
    for i in range(numberOfAddon):
        dataList.append([])


def saveData(list_GrapData):
    for index in range(len(list_GrapData)):
        if index == 0:
            classification(list_GrapData[index], index)
        else:
            classification(list_GrapData[index], index, "a")


def classification(data, index, parseType=""):
    if parseType != "":
        try:
            dataList[index].append(data.find(parseType).string)
        except:
            dataList[index].append(0)

    else:
        dataList[index].append(data.string)


def changeListType(changedList):
    for i in range(len(changedList)):
        if isinstance(changedList[i], str):
            changedList[i] = float(changedList[i].replace(",", ""))


def loadPage():
    global req
    req = requests.get(url, headers=header)
    req.encoding = 'utf-8'


def transToSoup():
    global soup
    soup = BeautifulSoup(req.text, 'lxml')


def grabData():
    div_FinDetail = soup.find(id='txtFinDetailData')
    div_yearData = div_FinDetail.find_all("tr", align='center')
    createSlot(21)
    for yearData in div_yearData:
        yearDetail = yearData.find_all("nobr")
        saveData(yearDetail)


def addPlot(select, base=0):
    global plotColor
    changeListType(dataList[select])
    plt.plot(base, dataList[select], pyplotARGS[plotColor], label=dataTitle[select])
    plotColor+=1


def graphPicture():
    plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
    plt.rcParams['axes.unicode_minus'] = False

    lineColor = 0
    for i in selectList:
    plt.xticks(rotation=-45)
    plt.show()


def findStockTitle():
    find_table = soup.find("table", class_="b1 p4_2 r10").find("table", class_="b0")
    find_a = find_table.find("a", class_="link_blue")
    return find_a.text


def Selection():
    while True:
        print("選擇顯示項目")
        for i in range(1, len(dataTitle)):
            print("{0}:{1}".format(i, dataTitle[i]))
        print("輸入111 顯示圖表")
        try:
            userSelect = int(input("輸入-1即可離開:"))
            if userSelect == -1:
                break
            if 0 < userSelect < len(dataTitle):
                graphPicture(userSelect)
            else:
                print("Selection Failed!!")
        except :

            print("Input Error!!")


def selectNumber():
    stockID = int(input("請輸入股票號碼"))
    global url
    url = "https://goodinfo.tw/StockInfo/StockBzPerformance.asp?STOCK_ID={0}&RPT_CAT=M%5FYEAR".format(stockID)


def main():
    selectNumber()
    loadPage()
    transToSoup()
    print(findStockTitle())
    grabData()
    Selection()

if __name__ == '__main__':
    selectList = [3,5,7]
    graphPicture()
