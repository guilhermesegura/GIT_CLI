import git
import scan
import time
from datetime import datetime, timedelta

daysInGraph = 183
weeksInGraph = 26
outOfRange = 99999
today = datetime.today()

def stats(email: str):
    commits = processRepositories(email)
    printCommitsStats(commits)

def statsDate(email: str, date: str):
    global today
    day, month, year = date.split("/")
    today = datetime(int(year), int(month), int(day))
    commits = processRepositories(email)
    printCommitsStats(commits)

def processRepositories(email: str) -> dict[int, int]:
    filepath = scan.getDotFilePath()
    repos = scan.parseFileLinesToLists(filepath)
    commits = {i: 0 for i in range(daysInGraph, -1, -1)}
    
    for path in repos:
        fillCommits(email, path, commits)

    return commits

def fillCommits(email: str, path: str, commits: dict[int, int]):
    try:
        repo = git.Repo(path)
    except:
        print("An error has occured while trying to access the commits")
    else:
        commitList = list(repo.iter_commits())
        offset = calcOffset()
        for commit in commitList:
            daysAgo = countDaysSinceDate(time.localtime
                                         (commit.committed_date)) + offset
            if commit.author.email != email:
                continue
            
            if daysAgo <= daysInGraph:
                commits[daysAgo] += 1
    

def countDaysSinceDate(date: time.struct_time) ->int:
    days = 0
    date = datetime(date.tm_year, date.tm_mon, date.tm_mday)
    today_aux = datetime(today.year, today.month, today.day)
    oneDay = timedelta(days = 1)
    if date > today: return outOfRange
    while date < today_aux:
        date += oneDay
        days +=1
        if days > daysInGraph:
            return outOfRange
    return days

def calcOffset() ->int:
    weekDay = today.weekday()
    if weekDay == 6:
        return 6
    return 5 - weekDay
   

def printCommitsStats(commits: dict[int, int]):
    keys = sortDictIntoList(commits)
    cols = buildCols(commits, keys)
    printCells(cols)

def sortDictIntoList(d: dict[int, int]) ->list[int]:
    keys = []
    for k in d:
        keys.append(k)
    keys.sort()
    return keys

def buildCols(commits: dict[int, int], keys: list[int]) ->dict[int, list[int]]:
    cols = {}
    col = []
    for k in keys:
        week = k // 7
        dayinweek = k % 7

        if dayinweek == 0:
            col = []
        
        col.append(commits[k])

        if dayinweek == 6:
            cols[week] = col
        
    return cols

def printCells(cols: dict[int, list[int]]):
    printMonths()
    for j in range(6, -1, -1):
        for i in range(weeksInGraph + 1, -1, -1):
            if i == weeksInGraph + 1:
                printDayCol(j)
            
            if cols.get(i) != None:
                col = cols[i]
                if i == 0 and j == calcOffset():
                    printCell(col[j], True)
                    continue
                else:
                    if len(col) > j:
                        printCell(col[j], False)
                        continue
            
            printCell(0, False)
        
        print()


def printMonths():
    week = today - timedelta(days = daysInGraph)
    month = week.month
    oneWeek = timedelta(days = 7)
    print("          ",end="")
    while(True):
        if week.month != month:
            print(monthToString(week.month) + " ", end="")
            month = week.month
        else:
            print("    ",end="")

        week += oneWeek
        if week > today:
            break
    print()

def monthToString(month: int)-> str:
    if month == 1:
        return "Jan"
    if month == 2:
        return "Feb"
    if month == 3:
        return "Mar"
    if month == 4:
        return "Apr"
    if month == 5:
        return "May"
    if month == 6:
        return "Jun"
    if month == 7:
        return "Jul"
    if month == 8:
        return "Aug"
    if month == 9:
        return "Sep"
    if month == 10:
        return "Oct"
    if month == 11:
        return "Nov"
    if month == 12:
        return "Dec"
        
def printDayCol(day: int):
    out = "     "
    if day == 1:
        out = " Fri "
    if day == 3:
        out = " Wed "
    if day == 5:
        out = " Mon "
    
    print(out, end="")

def printCell(val: int, istoday: bool):
    escape = "\033[0;37;30m"
    if val > 0 and val < 5:
        escape = "\033[1;30;47m"
    if val >= 5 and val < 10:
        escape = "\033[1;30;43m"
    if val >= 10:
        escape = "\033[1;30;42m"
    
    if istoday:
        escape = "\033[1;37;45m"


    if val == 0:
        print(escape + "  - " + "\033[0m", end="")
        return
    lspace = "  "
    
    if val >= 10:
        lspace = " "
    
    if val >= 100:
        lspace = ""

    print(escape + lspace + str(val) + " " +"\033[0m", end="")