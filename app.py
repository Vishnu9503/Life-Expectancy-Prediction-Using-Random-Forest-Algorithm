import numpy as np
from flask import Flask, request, render_template, redirect, url_for, flash, session
from pymongo import MongoClient
import bcrypt
import pickle

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a strong, random secret key

# MongoDB connection configuration for user authentication
client_auth = MongoClient('mongodb://localhost:27017/lifeexpectancy')  # Replace with your MongoDB connection string
db_auth = client_auth['Life']  # Replace with your database name
users_collection = db_auth['lep']  # Replace with your collection name

# MongoDB connection configuration for form data
client_data = MongoClient('mongodb://localhost:27017')  # Replace with your MongoDB connection string
db_data = client_data['life_expectancy']  # Replace with your database name
collection_data = db_data['form_data']  # Replace with your collection name

# Load Pickle model
model = pickle.load(open("model.pkl", "rb"))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/home')
def home():
    return render_template('login.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users_collection.find_one({'username': username})

        if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
            session['username'] = username
            flash('Login successful', 'success')
            return redirect(url_for('predict'))
        else:
            flash('Invalid username or password', 'danger')

    return render_template('signin.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        existing_user = users_collection.find_one({'username': username})

        if existing_user:
            flash('Username already exists', 'danger')
        else:
            new_user = {
                'username': username,
                'password': hashed_password
            }
            users_collection.insert_one(new_user)
            flash('Account created successfully', 'success')
            return redirect(url_for('predict'))

    return render_template('signup.html')

@app.route('/signout')
def signout():
    session.pop('username', None)
    flash('You have been logged out', 'info')
    return redirect(url_for('index'))

@app.route('/predict', methods=["GET", "POST"])
def predict():
    if 'username' not in session:
        flash('You need to be logged in to access this page.', 'danger')
        return redirect(url_for('signin'))

    if request.method == "POST":
        username = session['username']  # Get the currently logged-in user's username
        float_features = [float(x) for x in request.form.values()]
        features = [np.array(float_features)]
        prediction = model.predict(features)

        # Store the form data in MongoDB with the associated username
        form_data = {
            'Username': username,  # Associate the form data with the logged-in user
            'Year': request.form.get('Year'),
            'AdultMortality': request.form.get('AdultMortality'),
            'InfantDeaths': request.form.get('InfantDeaths'),
            'Alcohol': request.form.get('Alcohol'),
            'PercentageExpenditure': request.form.get('PercentageExpenditure'),
            'HepatitisB': request.form.get('HepatitisB'),
            'Measles': request.form.get('Measles'),
            'BMI': request.form.get('BMI'),
            'UnderFiveDeaths': request.form.get('UnderFiveDeaths'),
            'Polio': request.form.get('Polio'),
            'TotalExpenditure': request.form.get('TotalExpenditure'),
            'Diphtheria': request.form.get('Diphtheria'),
            'HIVAIDS': request.form.get('HIVAIDS'),
            'GDP': request.form.get('GDP'),
            'Population': request.form.get('Population'),
            'Thinness1_19years': request.form.get('Thinness1_19years'),
            'Thinness5_9years': request.form.get('Thinness5_9years'),
            'IncomeComposition': request.form.get('IncomeComposition'),
            'Schooling': request.form.get('Schooling'),
            'Prediction': prediction[0]  # Store the prediction result
        }
        collection_data.insert_one(form_data)

        # Fetch data from the MongoDB collection for the logged-in user
        data_from_db = list(collection_data.find({'Username': username}))

        return render_template("result.html", prediction_text="Your Predicted Life Expectancy is: {}".format(prediction), data_from_db=data_from_db)

    return render_template("predict.html")

if __name__ == '__main__':
    app.run(debug=True)
