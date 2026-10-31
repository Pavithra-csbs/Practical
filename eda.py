import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
df = pd.read_csv("heart_cleveland_upload.csv")
df.head()
df.shape
df.info()
df.isnull().sum()
df.describe()
#histogram
plt.figure(figsize=(6,4))
plt.hist(df["age"],bins=15,color = "skyblue",edgecolor="black")
plt.title("Age distribution")
plt.xlabel("Age")
plt.ylabel("Frequency")
plt.show()
#countplot
plt.figure(figsize=(5,4))
sns.countplot(x="condition",data = df)
plt.title("Heart Disease Distribution")
plt.show()
#pie chart
gender = df["sex"].value_counts()
plt.figure(figsize=(5,5))
plt.pie(gender,
        labels=["Male","Female"],
        autopct = "%1.1f%%",
        startangle=90)
plt.title("Gender Distribution")
plt.show()

#heatmap
plt.figure(figsize=(10,8))
sns.heatmap(df.corr(),annot=True,cmap = "coolwarm")
plt.title("Correlation heatmap")
plt.show()

#boxplot
plt.figure(fisize=(6,4))
sns.boxplot(x=df["age"])
plt.title("Box plot of age")
plt.show()

