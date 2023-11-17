import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import pickle
from sklearn.preprocessing import LabelEncoder

#Load the csv files
life_expectancy_df = pd.read_csv(r'C:\Users\Vaishnavi S\OneDrive\Desktop\LifeExpectancy\Life_Expectancy_Data.csv')


#Data Preprocessing
life_expectancy_df=life_expectancy_df.drop(['Country'],axis=1)
life_expectancy_df.columns
life_expectancy_df.dropna(how='any',inplace=True)
life_expectancy_df.isnull().sum()
life_expectancy_df['Year'] = life_expectancy_df['Year'].astype(str)




#split dataset in features and target variable
# Correct way to access multiple columns using a list of column names
columns = ['Year', 'Adult Mortality', 'Infant Deaths', 'Alcohol', 'Percentage Expenditure', 'Hepatitis B', 'Measles', 'BMI', 'Under-Five Deaths', 'Polio', 'Total Expenditure', 'Diphtheria', 'HIV/AIDS', 'GDP', 'Population', 'Thinness  1-19 years', 'Thinness 5-9 years', 'Income Composition of Resources', 'Schooling']

X = life_expectancy_df[columns]  # Features

y = life_expectancy_df['Life Expectancy']# Target variable
X.head()

# Split dataset into training set and test set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1) # 70% training and 30% test
#Feature Scaling
sc=StandardScaler()
X_train=sc.fit_transform(X_train)
X_test=sc.transform(X_test)

#Model Building
rf = RandomForestRegressor(n_estimators = 40, random_state = 50)
#Fit the model
rf.fit(X_train, y_train)

#Make pickle file of model
pickle.dump(rf,open("model.pkl",'wb'))
