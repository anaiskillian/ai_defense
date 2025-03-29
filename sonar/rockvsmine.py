# %%
# Import required librries 
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
# %%
df = pd.read_csv('./sonar/sonar.csv',header=None)

# %%
df.head()

# %%
df.describe()

# %%
# One-hot encoding
def convertion(text):
    if 'R' in text:
      return 0
    elif 'M' in text:
      return 1

df[60]= df[60].apply(convertion)

# %%
# Separating Data and Labels
X = df.drop(columns=60, axis=1) # Independent data
Y = df[60] # dependent data

# %%
# Libraries for feature importances and also fit the dependent and independent data
from sklearn.ensemble import ExtraTreesRegressor
model = ExtraTreesRegressor()
model.fit(X,Y)

# %%
X.head()

# %% [markdown]
# Correlation states how the features are related to each other or the target variable.
# 
# We can use a heatmap to identify which features are most related to the target variable.

# %%
corrmat = df.corr()

# %%
top_corr_features = corrmat.index
plt.figure(figsize=(20,20))
# Plot
g = sns.heatmap(df[top_corr_features].corr(),annot=True,cmap='RdYlGn')

# %%
# Cross-Validation
from sklearn.model_selection import train_test_split
X_train, X_test, Y_train, Y_test = train_test_split(X,Y,test_size=0.3, random_state=1)

# %%
def models(X_train,Y_train):
    
    # Logistic Regression
    from sklearn.linear_model import LogisticRegression
    log = LogisticRegression(random_state=0)
    log.fit(X_train,Y_train)
    
    #K Neighbors
    from sklearn.neighbors import KNeighborsClassifier
    knn =  KNeighborsClassifier(n_neighbors = 5 , metric = 'minkowski',p =2)
    knn.fit(X_train,Y_train)

    # Radial basis functions (RBFs) in ML are used for function approximation, interpolation, and pattern recognition.
    # They transform input data into higher-dimensional spaces, capturing complex, non-linear relationships.
    from sklearn.svm import SVC
    svc_rbf = SVC(kernel='rbf',random_state= 0)
    svc_rbf.fit(X_train,Y_train)

    # Decision Tree Algorithm
    from sklearn.tree import DecisionTreeClassifier
    tree = DecisionTreeClassifier(criterion='entropy',random_state = 0)
    tree.fit(X_train,Y_train)
    
    # Random Forest Model
    from sklearn.ensemble import RandomForestClassifier
    forest = RandomForestClassifier(n_estimators =10, criterion='entropy',random_state = 0)
    forest.fit(X_train,Y_train)

    print("Logistic Regression Accuracy:" ,log.score(X_train,Y_train))
    print("")
    print("K N N  Accuracy:" ,knn.score(X_train,Y_train))
    print("")
    print("Support Vector Machine Accuracy:" ,svc_rbf.score(X_train,Y_train))
    
    # Save the SVM model
    import joblib
    joblib.dump(svc_rbf, 'sonar/svm_model.pkl')
    print("\nSaved SVM model to sonar/svm_model.pkl")
    
    return log,knn,svc_rbf

# %%
model = models(X_train,Y_train)
