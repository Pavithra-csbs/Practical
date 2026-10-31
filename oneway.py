
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import f_oneway

# Load Iris dataset
iris = sns.load_dataset('iris')

# Display dataset
print(iris.head())

# Separate data based on species
setosa = iris[iris['species'] == 'setosa']['sepal_length']
versicolor = iris[iris['species'] == 'versicolor']['sepal_length']
virginica = iris[iris['species'] == 'virginica']['sepal_length']

# Perform One-Way ANOVA
f_value, p_value = f_oneway(setosa, versicolor, virginica)

print("\nOne-Way ANOVA Results")
print("F-Statistic:", f_value)
print("P-Value:", p_value)

# Hypothesis testing
if p_value < 0.05:
    print("Reject Null Hypothesis")
    print("There is a significant difference between group means.")
else:
    print("Accept Null Hypothesis")
    print("There is no significant difference between group means.")

# Draw Boxplot
plt.figure(figsize=(8, 5))

sns.boxplot(x='species', y='sepal_length', data=iris)

plt.title('Boxplot of Sepal Length for Iris Species')
plt.xlabel('Iris Species')
plt.ylabel('Sepal Length (cm)')
plt.show()
