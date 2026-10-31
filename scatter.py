import pandas as pd
import matplotlib.pyplot as plt
df=pd.read_csv("Study_hours_scores.csv")
df.head()
df.info()
df.describe()

#scatter
plt.figure(figsize=(8,6))
plt.scatter(
    df["Study_Hours"],
    df["Exam_Score"],
    color = "blue",
    marker="o",
    s = 80
)
plt.title("")
plt.xlabel("Study hours")
plt.ylabel("exam score")
plt.grid(True)
plt.show()
