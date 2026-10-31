import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
df = pd.read_csv("train.csv") #titanis dataset
df.head()
df.shape
df.columns
df.describe()
age = df["Age"].dropna()
population_mean=age.mean()
population_std=age.std()
print(population_mean)
print(population_std)
sample_size = 30
no_of_samples=1000
sample_means=[]
for i in range(no_of_samples):
    sample = np.random.choice(age,sample_size)
    sample_mean=np.mean(sample)
    sample_means.append(sample_mean)

mean_of_sample_means=np.mean(sample_means)
standard_error = np.std(sample_means)
print(mean_of_sample_means)
print(standard_error)

#hist
plt.hist(sample_means,bins = 20)
plt.xlabel("Sample mean of age")
plt.ylabel("Frequency")
plt.title("")
plt.show()
