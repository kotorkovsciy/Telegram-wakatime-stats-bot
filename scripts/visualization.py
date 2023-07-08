import matplotlib.pyplot as plt
from io import BytesIO


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
