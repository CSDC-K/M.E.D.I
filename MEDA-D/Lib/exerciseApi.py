import os
import json
from datetime import datetime

from dateutil.utils import today


def getTime() -> str:
    now = datetime.now()
    today_date = now.strftime("%Y-%m-%d")
    return today_date

def controlLogs() -> bool:
    with open("Data\\Json\\todayLog.json","r", encoding="utf-8") as logFile:
        todayLog = json.load(logFile)

    todayTime = getTime()
    if todayLog["Date"] == todayTime:
        return True
    else:
        oldLog = todayLog
        print(oldLog)

        with open(f"Data\\Logs\\Daily\\{oldLog['Date']}.json","w", encoding="utf-8") as logFile:
            logFile.write(json.dumps(oldLog,ensure_ascii=False,indent=4))


        todayLog["Date"] = todayTime
        todayLog["Squat"] = 0
        todayLog["Kollar Öne"] = 0
        todayLog["Kollar Yana"] = 0
        todayLog["Topuk Kaldırma"] = 0

        with open("Data\\Json\\todayLog.json", "w", encoding="utf-8") as f:
            json.dump(todayLog, f, ensure_ascii=False, indent=4)

        return False

def getLogs(mode : str = "Biggest") -> any:
    with open("Data\\Json\\todayLog.json","r", encoding="utf-8") as logFile:
        todayLogs = json.load(logFile)
        if mode == "total":
            return (todayLogs["Squat"] +
                    todayLogs["Kollar Öne"] +
                    todayLogs["Kollar Yana"] +
                    todayLogs["Topuk Kaldırma"])

        elif mode == "Biggest":
            todayLogs = {k: int(v) for k, v in todayLogs.items() if k != "Date"}
            biggest = max(todayLogs, key=todayLogs.get)
            return biggest

        elif mode == "AllExercises":
            with open("Data\\Json\\Log.json", "r", encoding="utf-8") as logFile:
                todayLogs = json.load(logFile)
            return todayLogs["TotalExercise"]
            logFile.close()
        elif mode == "AllUser":
            with open("Data\\Json\\Log.json", "r", encoding="utf-8") as logFile:
                todayLogs = json.load(logFile)
            return todayLogs["TotalUser"]
            logFile.close()


def addLogs(Squat : int = 0,
            Kollar : int = 0,
            Yana : int = 0,
            Topuk : int = 0,
            User : int = 0,
            Username : str = None,
            CreateUserLog : bool = False) -> None:
    with open("Data\\Json\\todayLog.json","r", encoding="utf-8") as logFile:
        todayLogs = json.load(logFile)

    with open("Data\\Json\\Log.json","r", encoding="utf-8") as AlogFile:
        totalLogs = json.load(AlogFile)

    if User != 0:
        totalLogs["TotalUser"] = totalLogs["TotalUser"] + User
        return

    elif CreateUserLog:

        path = f"Data/Logs/Patients/{Username}.json"
        os.makedirs(os.path.dirname(path), exist_ok=True)
        if not os.path.exists(path):
            with open(path, "w", encoding="utf-8") as f:
                json.dump({}, f, ensure_ascii=False, indent=4)

        with open(f"Data\\Logs\\Patients\\{Username}.json", "r", encoding="utf-8") as logFile:
            userDaily = json.load(logFile)

        with open(f"Data\\Logs\\Patients\\{Username}.json","w", encoding="utf-8") as logFile:
            try:
                userDaily[getTime()] = {
                    "Squat": userDaily[getTime()]["Squat"] + Squat,
                    "Kollar Öne": userDaily[getTime()]["Kollar"] + Kollar,
                    "Kollar Yana": userDaily[getTime()]["Yana"] + Yana,
                    "Topuk Kaldırma": userDaily[getTime()]["Topuk"] + Topuk,
                }
            except KeyError:
                userDaily[getTime()] = {
                    "Squat": Squat,
                    "Kollar Öne": Kollar,
                    "Kollar Yana": Yana,
                    "Topuk Kaldırma": Topuk,
                }
            json.dump(userDaily, logFile, ensure_ascii=False, indent=4)

        return

    elif Username != None:
        with open("Data\\Profiles\\Users.json","r", encoding="utf-8") as logFile:
            userLogs = json.load(logFile)


        userLogs[Username]["Total_Exercises"] = userLogs[Username]["Total_Exercises"] + (Squat + Kollar + Yana + Topuk)
        with open("Data\\Profiles\\Users.json","w", encoding="utf-8") as logFile:
            json.dump(userLogs, logFile, ensure_ascii=False, indent=4)

        return

    todayLogs["Squat"] = todayLogs["Squat"] + Squat
    todayLogs["Kollar Öne"] = todayLogs["Kollar Öne"] + Kollar
    todayLogs["Kollar Yana"] = todayLogs["Kollar Yana"] + Yana
    todayLogs["Topuk Kaldırma"] = todayLogs["Topuk Kaldırma"] + Topuk

    with open("Data\\Json\\todayLog.json","w", encoding="utf-8") as logFile:
        json.dump(todayLogs, logFile, ensure_ascii=False, indent=4)



    totalLogs["TotalExercise"] = totalLogs["TotalExercise"] + (Squat + Kollar + Yana + Topuk)



    with open("Data\\Json\\Log.json","w", encoding="utf-8") as AAlogFile:
        json.dump(totalLogs, AAlogFile, ensure_ascii=False, indent=4)

