import matplotlib.pyplot as plt
from io import BytesIO
import pandas as pd
import math


class Convertation:
    @staticmethod
    def json_to_dataframe(json):
        data = {"date": json["date"]}

        for i in json["stats"]:
            data[i["name"]] = i["total_seconds"]

        df = pd.DataFrame([data])

        return df

    @classmethod
    def list_json_to_dataframe(cls, list_json):
        df = pd.DataFrame()
        for json in list_json:
            df = pd.concat([df, cls.json_to_dataframe(json)], ignore_index=True)

        return df

    @staticmethod
    def num_to_percent(df):
        new_df = pd.DataFrame()

        for index, row in df.iterrows():
            data = {}
            sum = 0
            for i in row.items():
                if i[0] != "date":
                    if not math.isnan(i[1]):
                        sum += float(i[1])
                    else:
                        sum += 0

            for i in row.items():
                if i[0] != "date":
                    if not math.isnan(i[1]):
                        data[i[0]] = float(i[1]) / sum * 100
                    else:
                        data[i[0]] = 0
                else:
                    data[i[0]] = i[1]

            new_df = pd.concat([new_df, pd.DataFrame([data])], ignore_index=True)

        return new_df


class Visualization:
    @staticmethod
    def create_pie_diagram(data):
        stats, times = [], []
        times.append(0)
        stats.append("Other")

        for i in data:
            if i["total_seconds"] > 8000:
                if i["name"] != "Other":
                    times.append(i["total_seconds"])
                    stats.append(i["name"])
                else:
                    times[0] += i["total_seconds"]
            else:
                times[0] += i["total_seconds"]

        if times[0] == 0:
            del times[0]
            del stats[0]

        fig, ax = plt.subplots()
        ax.pie(times, labels=stats, shadow=True)
        ax.axis("equal")

        buffer = BytesIO()
        plt.savefig(buffer, format="png")
        buffer.seek(0)

        img = buffer.getvalue()

        buffer.close()

        return img

    def create_bar_diagram(data):
        df = Convertation.list_json_to_dataframe(data)
        df = Convertation.num_to_percent(df)
        df.plot(x="date", linestyle="-.", marker="s")

        buffer = BytesIO()
        plt.savefig(buffer, format="png")
        buffer.seek(0)

        img = buffer.getvalue()

        buffer.close()

        return img

    def create_bar_diagram_slice(data, start=0, end=5):
        df = Convertation.list_json_to_dataframe(data)
        df = Convertation.num_to_percent(df)

        df2 = pd.DataFrame(df.mean(numeric_only=True)[start:end])
        df.plot(x="date", y=df2.index, linestyle="-.", marker="s")

        buffer = BytesIO()
        plt.savefig(buffer, format="png")
        buffer.seek(0)

        img = buffer.getvalue()

        buffer.close()

        return img
