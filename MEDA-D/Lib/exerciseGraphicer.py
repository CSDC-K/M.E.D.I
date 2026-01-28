import os
import json
import matplotlib.pyplot as plt
from datetime import datetime

def plot_logs(mode: str = "Hepsi"):
    plt.style.use("seaborn-v0_8-whitegrid")

    if mode == "Hepsi":
        folder = "Data\\Logs\\Daily\\"
        logs = []

        for file in os.listdir(folder):
            if file.endswith(".json"):
                with open(os.path.join(folder, file), "r", encoding="utf-8") as f:
                    logs.append(json.load(f))

        logs.sort(key=lambda x: datetime.strptime(x["Date"], "%Y-%m-%d"))
        dates = [log["Date"] for log in logs]

        data_map = {
            "Squat": [log.get("Squat", 0) for log in logs],
            "Kollar Öne": [log.get("Kollar Öne", 0) for log in logs],
            "Kollar Yana": [log.get("Kollar Yana", 0) for log in logs],
            "Topuk Kaldırma": [log.get("Topuk Kaldırma", 0) for log in logs],
        }

        plt.figure(figsize=(9, 5), dpi=200)
        for name, values in data_map.items():
            plt.plot(dates, values, marker="o", label=name)

        plt.xlabel("Tarih")
        plt.ylabel("Tekrar Sayısı")
        plt.title("Günlük Egzersiz İstatistikleri (Hepsi)")
        plt.xticks(rotation=45, ha="right")
        plt.legend()
        plt.tight_layout()
        plt.savefig("user.png", dpi=200)
        plt.close()

        return "user.png"

    else:
        path = f"Data\\Logs\\Patients\\{mode}.json"
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        dates = list(data.keys())
        exercises = list(data[dates[0]].keys())
        values = {ex: [data[d][ex] for d in dates] for ex in exercises}

        x = range(len(dates))
        width = 0.15
        fig, ax = plt.subplots(figsize=(9, 5), dpi=200)

        for i, ex in enumerate(exercises):
            ax.bar([p + i * width for p in x], values[ex], width, label=ex, alpha=0.9)

        ax.set_xticks([p + width for p in x])
        ax.set_xticklabels(dates, rotation=45, ha="right")
        ax.set_xlabel("Tarih")
        ax.set_ylabel("Tekrar Sayısı")
        ax.set_title(f"{mode} Egzersiz İstatistikleri")
        ax.legend(frameon=False)
        plt.tight_layout()
        plt.savefig("user.png", dpi=200)
        plt.close()

        return "user.png"
