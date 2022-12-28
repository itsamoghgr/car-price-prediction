from flask import Flask, render_template, request
import jsonify
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler
app = Flask(__name__)
model = pickle.load(open('rf_CarPricePredKaggle.pkl', 'rb'))
@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')


standard_to = StandardScaler()
@app.route("/predict", methods=['POST'])
def predict():
    Fuel_Type_Diesel=0
    if request.method == 'POST':
        Year = int(request.form['Year'])
        # Present_Price=float(request.form['Present_Price'])
        Km_Driven=int(request.form['Km_Driven'])
        Km_Driven2=np.log(Km_Driven)
        Owner=request.form['Owner']
        if(Owner=='Test'):
            owner_Test=1
            owner_Second=0
            owner_Third=0
            owner_Fourth = 0
        elif(Owner == '2'):
            owner_Test=0
            owner_Second=1
            owner_Third=0
            owner_Fourth = 0
        elif(Owner == '3'):
            owner_Test=0
            owner_Second=0
            owner_Third=1
            owner_Fourth = 0
        elif(Owner == '4'):
            owner_Test=0
            owner_Second=0
            owner_Third=0
            owner_Fourth = 1
        else:
            owner_Test=0
            owner_Second=0
            owner_Third=0
            owner_Fourth = 0

        fuel=request.form['fuel']
        if(fuel=='Petrol'):
                fuel_Petrol=1
                fuel_Diesel=0
                fuel_Electric=0
                fuel_LPG=0
        elif(fuel=='Diesel'):
                fuel_Petrol=0
                fuel_Diesel=1
                fuel_Electric=0
                fuel_LPG=0
        elif(fuel=='Electric'):
                fuel_Petrol=0
                fuel_Diesel=0
                fuel_Electric=1
                fuel_LPG=0
        elif(fuel=='LPG'):
            fuel_Petrol=0
            fuel_Diesel=0
            fuel_Electric=0
            fuel_LPG=1
        else:
            fuel_Petrol=0
            fuel_Diesel=0
            fuel_Electric=0
            fuel_LPG=0

        no_years_old=2022-Year

        seller_type_Individual=request.form['seller_type_Individual']
        if(seller_type_Individual=='Individual'):
            seller_type_Individual=1
            seller_type_TrustmarkDealer = 0
        else:
            seller_type_Individual=0
            seller_type_TrustmarkDealer = 1 
        transmission_Manual=request.form['transmission_Manual']
        if(transmission_Manual=='Manual'):
            transmission_Manual=1
        else:
            transmission_Manual=0

        prediction=model.predict([[Km_Driven,no_years_old,fuel_Petrol,fuel_Diesel,fuel_Electric,fuel_LPG,seller_type_Individual,seller_type_TrustmarkDealer,transmission_Manual,owner_Test,owner_Second,owner_Third,owner_Fourth]])
        output=round(prediction[0],2)
        if output<0:
            return render_template('index.html',prediction_texts="Sorry you cannot sell this car")
        else:
            return render_template('index.html',prediction_text="You Can Sell The Car at {}".format(output))
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)





