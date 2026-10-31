
# Linear Least Squares Regression using Iris Dataset

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.api as sm
from sklearn.metrics import mean_squared_error, r2_score

# Load Iris dataset
iris = sns.load_dataset('iris')

# Independent and dependent variables
X = iris[['sepal_length']]
y = iris['petal_length']

# Add constant for intercept
X = sm.add_constant(X)

# Fit Linear Regression Model
model = sm.OLS(y, X).fit()

# Predict values
y_pred = model.predict(X)

# Display model summary
print("Regression Results:")
print(model.summary())

# Evaluate model
mse = mean_squared_error(y, y_pred)
r2 = r2_score(y, y_pred)

print("\nModel Evaluation")
print("Mean Squared Error:", mse)
print("R-Squared:", r2)

# Plot regression line
plt.figure(figsize=(8, 5))

plt.scatter(iris['sepal_length'], y,
            color='blue', label='Actual Data')

plt.plot(iris['sepal_length'], y_pred,
         color='red', label='Regression Line')

plt.xlabel('Sepal Length (cm)')
plt.ylabel('Petal Length (cm)')
plt.title('Linear Least Squares Regression')
plt.legend()
plt.grid()
plt.show()
