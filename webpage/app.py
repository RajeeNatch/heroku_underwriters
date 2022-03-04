# Import dependecies
from multiprocessing.sharedctypes import Array
from flask import Flask, render_template, request
import datetime
from datetime import date
import numpy as np
import pickle
from sklearn.preprocessing import StandardScaler
import pandas as pd

# Create an instance of Flask
app = Flask(__name__)

# Create a route to the home page
@app.route("/")
def home():
    return render_template("index.html")

# Load the ML Model
clf = pd.read_pickle('./Credit_Risk_Evaluator_Model.zip', compression='zip')

# Load the ML Scaler
filename2 = './scaler.sav'
scaler = pickle.load(open(filename2, 'rb'))

# Create a route to run the Machine Learning model and make the prediction

@app.route("/pred", methods=['POST'])
def pred():
    if request.method == 'POST':

        date_of_birth = datetime.datetime.strptime(
            request.form['DAYS_BIRTH'], '%Y-%m-%d')
        dob_day_diff = date_of_birth-datetime.datetime.today()
        cell1 = dob_day_diff.days

        cell2 = request.form['AMT_CREDIT']

        cell3 = request.form['AMT_INCOME_TOTAL']

        date_of_registration = datetime.datetime.strptime(
            request.form['DAYS_REGISTRATION'], '%Y-%m-%d')
        dor_day_diff = date_of_registration-datetime.datetime.today()
        cell4 = dor_day_diff.days

        date_of_employement = datetime.datetime.strptime(
            request.form['DAYS_EMPLOYED'], '%Y-%m-%d')
        doe_day_diff = date_of_employement-datetime.datetime.today()
        cell5 = doe_day_diff.days

        date_of_publish = datetime.datetime.strptime(
            request.form['DAYS_ID_PUBLISH'], '%Y-%m-%d')
        dop_day_diff = date_of_publish-datetime.datetime.today()
        cell6 = dop_day_diff.days

        cell7 = request.form['REGION_POPULATION_RELATIVE']

        hour_approval = datetime.datetime.strptime(
            request.form['HOUR_APPR_PROCESS_START'], '%H:%M:%S')
        cell8 = hour_approval.time().hour

        cell9 = request.form['NAME_CONTRACT_TYPE']
        if (cell9 == 'Cash loans'):
            cell9 = 1
            cell10 = 0
        else:
            cell9 = 0
            cell10 = 1

        cell11 = request.form['CNT_CHILDREN']

        cell12 = request.form['FLAG_PHONE']
        if (cell12 == ''):
            cell12 = 0
        else:
            cell12 = 1

        cell13 = request.form['FLAG_WORK_PHONE']
        if (cell13 == ''):
            cell13 = 0
        else:
            cell13 = 1

        cell14 = request.form['NAME_EDUCATION_TYPE_Secondary / secondary special']
        if (cell14 == 'Secondary / secondary special'):
            cell14 = 1
            cell19 = 0
        elif (cell14 == 'Higher education'):
            cell14 = 0
            cell19 = 1
        else:
            cell14 = 0
            cell19 = 0

        cell15 = request.form['NAME_FAMILY_STATUS_Married']
        if (cell15 == 'Married'):
            cell15 = 1
        else:
            cell15 = 0

        cell16 = request.form['ORGANIZATION_TYPE_Business Entity Type 3']
        if (cell16 == 'Business Entity'):
            cell16 = 1
            cell22 = 0
        elif (cell16 == 'Self-employed'):
            cell16 = 0
            cell22 = 1
        else:
            cell16 = 0
            cell22 = 0

        cell17 = request.form['REGION_RATING_CLIENT']
        if (cell17 == '1'):
            cell17 = 1
        elif (cell17 == '2'):
            cell17 = 2
        else:
            cell17 = 3

        cell18 = request.form['REGION_RATING_CLIENT_W_CITY']
        if (cell8 == '1'):
            cell8 = 1
        elif (cell18 == '2'):
            cell18 = 2
        else:
            cell18 = 3

        cell20 = request.form['REG_CITY_NOT_WORK_CITY']
        if (cell20 == 'Yes'):
            cell20 = 0
        else:
            cell20 = 1

        cell21 = request.form['WEEKDAY_APPR_PROCESS_START_THURSDAY']
        if (cell21 == 'Thursday'):
            cell21 = 1
        else:
            cell21 = 0

        # array = np.array([[cell1, cell2, cell3, cell4, cell5, cell6, cell7, cell8, cell9, cell10, cell11, cell12,
        #                    cell13, cell14, cell15, cell16, cell17, cell18, cell19, cell20, cell21, cell22]])
        
        array = np.array([[cell11, cell3, cell2, cell7, cell1, cell5, cell4, cell6, cell13, cell12,
                           cell17, cell18, cell8, cell20, cell9, cell10, cell19, cell14, cell15, cell21, cell16, cell22]])
        print(array)

        scaled = scaler.transform(array)
        pred = clf.predict(scaled)
        print(scaled)
        print(pred)
        
        if pred == 1:
            return render_template('index.html', prediction="Bad news! You are most likely not to get approved for a loan.")
        else:
            return render_template('index.html', prediction="Good news! You are most likely to get approved for a loan.")
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
