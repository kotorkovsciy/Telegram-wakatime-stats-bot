import matplotlib.pyplot as plt
from io import BytesIO
import pandas as pd
import math


class Convertation:
    @staticmethod
    def json_to_dataframe(json: dict) -> pd.DataFrame:
        """Convert json to dataframe

        Args:
            json (dict): Json

        Returns:
            pd.DataFrame: Dataframe
        """
        data = {"date": json["date"]}

        for i in json["stats"]:
            data[i["name"]] = i["total_seconds"]

        df = pd.DataFrame([data])

        return df

    @classmethod
    def list_json_to_dataframe(cls, list_json: list[dict]) -> pd.DataFrame:
        """Convert list json to dataframe

        Args:
            list_json (list[dict]): List json

        Returns:
            pd.DataFrame: Dataframe
        """
        df = pd.DataFrame()
        for json in list_json:
            df = pd.concat([df, cls.json_to_dataframe(json)], ignore_index=True)

        return df

    @staticmethod
    def num_to_percent(df: pd.DataFrame) -> pd.DataFrame:
        """Convert numbers to percent

        Args:
            df (pd.DataFrame): Dataframe

        Returns:
            pd.DataFrame: Dataframe
        """
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
    @classmethod
    def create_pie_diagram(cls, data: list[dict]) -> bytes:
        """Create pie diagram

        Args:
            data (list[dict]): Data

        Returns:
            bytes: Image
        """

        if len(data) > 15:
            data = cls.filter_data_for_pie_diagram(data, 1)

        data_names, data_val = [], []


        for i in data:
            data_val.append(i["total_seconds"])
            data_names.append(i["name"])

        total = sum(data_val)
        labels = [f"{n} ({v/total:.1%})" for n,v in zip(data_names, data_val)]

        dpi = 80
        fig = plt.figure(dpi = dpi, figsize = (1000 / dpi, 600 / dpi) )

        plt.pie(
            data_val, radius=1.1,
            explode=[0.15] + [0 for _ in range(len(data_names) - 1)] )
        plt.legend(
            bbox_to_anchor = (-0.16, 0.45, 0.25, 0.25),
            loc = 'best', labels = labels )

        buffer = BytesIO()
        fig.savefig(buffer, format="png")
        buffer.seek(0)

        img = buffer.getvalue()

        buffer.close()

        return img

    @staticmethod
    def filter_data_for_pie_diagram(data: list[dict], percent: int) -> list[dict]:
        """Filter data for pie diagram

        Args:
            data (list[dict]): Data
            percent (int): Percent

        Returns:
            list[dict]: Data
        """

        total = sum([i["total_seconds"] for i in data])
        data = [i for i in data if i["total_seconds"] / total * 100 > percent]

        return data

    def create_bar_diagram(data: list[dict]) -> bytes:
        """Create bar diagram

        Args:
            data (list[dict]): Data

        Returns:
            bytes: Image
        """
        df = Convertation.list_json_to_dataframe(data)
        df = Convertation.num_to_percent(df)
        df.plot(x="date", linestyle="-.", marker="s")

        buffer = BytesIO()
        plt.savefig(buffer, format="png")
        buffer.seek(0)

        img = buffer.getvalue()

        buffer.close()

        return img

    def create_bar_diagram_slice(
        data: list[dict], start: int = 0, end: int = 5
    ) -> bytes:
        """Create bar diagram slice

        Args:
            data (list[dict]): Data
            start (int, optional): Start. Defaults to 0.
            end (int, optional): End. Defaults to 5.

        Returns:
            bytes: Image
        """
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
