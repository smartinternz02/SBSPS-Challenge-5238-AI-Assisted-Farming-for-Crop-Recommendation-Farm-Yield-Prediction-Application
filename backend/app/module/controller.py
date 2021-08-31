from flask import request, jsonify, make_response,render_template
from app import app
from .models import *
from .models import user
from .models import personal_model
from .const import HttpStatus
from joblib import load,dump
import pandas as pd
import requests
from datetime import date
import jwt
import datetime
import os
import numpy as np
from functools import wraps
import random
import uuid
from sklearn.model_selection import train_test_split
from sklearn.ensemble import  RandomForestClassifier,RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import csv
from werkzeug.utils import secure_filename

def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):

        token = None

        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        if not token:
            return jsonify({'isAuthenticated': False ,'message': 'a valid token is missing'})

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = user.query.filter_by(id=data['id']).first()
        except:
            return jsonify({'isAuthenticated': False, 'message': 'token is invalid'})

        return f(current_user, *args, **kwargs)

    return decorator


def crop(crop_name):
    crop_data = {
        "wheat": ["/static/images/wheat.jpg", "U.P., Punjab, Haryana, Rajasthan, M.P., bihar", "rabi",
                  "Sri Lanka, United Arab Emirates, Taiwan"],
        "paddy": ["/static/images/paddy.jpg", "W.B., U.P., Andhra Pradesh, Punjab, T.N.", "kharif",
                  "Bangladesh, Saudi Arabia, Iran"],
        "barley": ["/static/images/barley.jpg", "Rajasthan, Uttar Pradesh, Madhya Pradesh, Haryana, Punjab", "rabi",
                   "Oman, UK, Qatar, USA"],
        "maize": ["/static/images/maize.jpg", "Karnataka, Andhra Pradesh, Tamil Nadu, Rajasthan, Maharashtra", "kharif",
                  "Hong Kong, United Arab Emirates, France"],
        "bajra": ["/static/images/bajra.jpg", "Rajasthan, Maharashtra, Haryana, Uttar Pradesh and Gujarat", "kharif",
                  "Oman, Saudi Arabia, Israel, Japan"],
        "copra": ["/static/images/copra.jpg", "Kerala, Tamil Nadu, Karnataka, Andhra Pradesh, Orissa, West Bengal",
                  "rabi", "Veitnam, Bangladesh, Iran, Malaysia"],
        "cotton": ["/static/images/cotton.jpg", "Punjab, Haryana, Maharashtra, Tamil Nadu, Madhya Pradesh, Gujarat",
                   " China, Bangladesh, Egypt"],
        "masoor": ["/static/images/masoor.jpg", "Uttar Pradesh, Madhya Pradesh, Bihar, West Bengal, Rajasthan", "rabi",
                   "Pakistan, Cyprus,United Arab Emirates"],
        "gram": ["/static/images/gram.jpg",
                 "Madhya Pradesh, Maharashtra, Rajasthan, Uttar Pradesh, Andhra Pradesh & Karnataka", "rabi",
                 "Veitnam, Spain, Myanmar"],
        "groundnut": ["/static/images/groundnut.jpg", "Andhra Pradesh, Gujarat, Tamil Nadu, Karnataka, and Maharashtra",
                      "kharif", "Indonesia, Jordan, Iraq"],
        "arhar": ["/static/images/arhar.jpg", "Maharashtra, Karnataka, Madhya Pradesh and Andhra Pradesh", "kharif",
                  "United Arab Emirates, USA, Chicago"],
        "sesamum": ["/static/images/sesamum.jpg", "Maharashtra, Rajasthan, West Bengal, Andhra Pradesh, Gujarat",
                    "rabi", "Iraq, South Africa, USA, Netherlands"],
        "jowar": ["/static/images/jowar.jpg", "Maharashtra, Karnataka, Andhra Pradesh, Madhya Pradesh, Gujarat",
                  "kharif", "Torronto, Sydney, New York"],
        "moong": ["/static/images/moong.jpg", "Rajasthan, Maharashtra, Andhra Pradesh", "rabi",
                  "Qatar, United States, Canada"],
        "niger": ["/static/images/niger.jpg", "Andha Pradesh, Assam, Chattisgarh, Gujarat, Jharkhand", "kharif",
                  "United States of American,Argenyina, Belgium"],
        "rape": ["/static/images/rape.jpg", "Rajasthan, Uttar Pradesh, Haryana, Madhya Pradesh, and Gujarat", "rabi",
                 "Veitnam, Malaysia, Taiwan"],
        "jute": ["/static/images/jute.jpg", " West Bengal , Assam , Orissa , Bihar , Uttar Pradesh", "kharif",
                 "JOrdan, United Arab Emirates, Taiwan"],
        "safflower": ["/static/images/safflower.jpg", "Maharashtra, Karnataka, Andhra Pradesh, Madhya Pradesh, Orissa",
                      "kharif", " Philippines, Taiwan, Portugal"],
        "soyabean": ["/static/images/soyabean.jpg",
                     "Madhya Pradesh, Maharashtra, Rajasthan, Madhya Pradesh and Maharashtra", "kharif",
                     "Spain, Thailand, Singapore"],
        "urad": ["/static/images/urad.jpg", "Andhra Pradesh, Maharashtra, Madhya Pradesh, Tamil Nadu", "rabi",
                 "United States, Canada, United Arab Emirates"],
        "ragi": ["/static/images/ragi.jpg", "Maharashtra, Tamil Nadu and Uttarakhand", "kharif",
                 "United Arab Emirates, New Zealand, Bahrain"],
        "sunflower": ["sunflower.jpg", "Karnataka, Andhra Pradesh, Maharashtra, Bihar, Orissa", "rabi",
                      "Phillippines, United States, Bangladesh"],
        "sugarcane": ["sugarcane.jpg", "Uttar Pradesh, Maharashtra, Tamil Nadu, Karnataka, Andhra Pradesh", "kharif",
                      "Kenya, United Arab Emirates, United Kingdom"]
    }
    return crop_data[crop_name]


def msp(crop_name):
    base = {
        "paddy": 1245.5,
        "arhar": 3200,
        "bajra": 1175,
        "barley": 980,
        "copra": 5100,
        "cotton": 3600,
        "sesamum": 4200,
        "gram": 2800,
        "groundnut": 3700,
        "jowar": 1520,
        "maize": 1175,
        "masoor": 2800,
        "moong": 3500,
        "niger": 3500,
        "ragi": 1500,
        "rape": 2500,
        "jute": 1675,
        "safflower": 2500,
        "soyabean": 2200,
        "sugarcane": 2250,
        "sunflower": 3700,
        "urad": 4300,
        "wheat": 1350
    }
    return base[crop_name]


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return ('AgriOracle Backend By -: Rutvik & Teerth')


## crop_recommendation rest api
@app.route('/recommendation', methods=['GET', 'POST'])
def crop_recommendation():
    """ function which take json input
    json input name :['n','p','k','ph','state','city']
    input example:
    {
	"state" : "gujarat",
	"city" : "ahmedabad",
	"ph" : 6.5,
	"n" : 43,
	"p" : 34,
	"k" : 43
     }"""
    ## extract user input information
    if request.method == "POST":
        re = request.get_json()
        city = re["city"]
        state = re["state"]
        ## convert into lower case
        state = state.lower()
        model_ph = re["ph"]
        model_n = re["n"]
        model_p = re["p"]
        model_k = re["k"]

        ##Api key for the call
        try:
            user_api = "6c4043b2272bb3cf1e7330517937f690"
            ## extract the weather data such as temp,humidity as per user given location
            complete_api_link = "https://pro.openweathermap.org/data/2.5/forecast/climate?q=" + \
                                city + "&appid=" + user_api
            api_link = requests.get(complete_api_link)
            ## response of api in api_data
            api_data = api_link.json()
            ## lets get the average of the temp and humidity for monthly
            humidity_sum = 0
            temp_sum = 0
            ll = api_data["list"]
            for i in range(30):
                temp = ll[i]['temp']
                temp_avg = (temp['day'] + temp['min'] + temp["max"] + temp["night"] + temp["eve"]) / 5
                temp_sum = (temp_avg - 273) + temp_sum
                humidity = ll[i]['humidity']
                humidity_sum = humidity + humidity_sum
            ## store the of avg of humidity and temperature in the varibale which we pass to model
            model_humidity = humidity_sum / 30
            model_temp = temp_sum / 30
        except:
            model_humidity = 60
            model_temp = 25

        ## lets get rainfall of the location
        today = date.today()
        current_month = today.month
        current_date = today.day
        current_year = today.year

        ## harvesting time get from database
        harvesting_time = 4
        ## create an list for the month number for which we have to get rainfall
        temp_month = current_month
        rain_fall_month_list = []
        for i in range(harvesting_time):
            if temp_month > 12:
                temp_month = 1
            rain_fall_month_list.append(temp_month)
            temp_month = temp_month + 1

        # month_list = ["january","february","march","april",
        #               "may","june","july","august","september",
        #               "october","november","december"]

        total_rainfall = 0
        try:
            rain_fall = rain_info.query.filter_by(state=state).first()
            ## get the rainfall from the database for the given month
            if 1 in rain_fall_month_list:
                total_rainfall = total_rainfall + rain_fall.january
            if 2 in rain_fall_month_list:
                total_rainfall = total_rainfall + rain_fall.february
            if 3 in rain_fall_month_list:
                total_rainfall = total_rainfall + rain_fall.march
            if 4 in rain_fall_month_list:
                total_rainfall = total_rainfall + rain_fall.april
            if 5 in rain_fall_month_list:
                total_rainfall = total_rainfall + rain_fall.may
            if 6 in rain_fall_month_list:
                total_rainfall = total_rainfall + rain_fall.june
            if 7 in rain_fall_month_list:
                total_rainfall = total_rainfall + rain_fall.july
            if 8 in rain_fall_month_list:
                total_rainfall = total_rainfall + rain_fall.august
            if 9 in rain_fall_month_list:
                total_rainfall = total_rainfall + rain_fall.september
            if 10 in rain_fall_month_list:
                total_rainfall = total_rainfall + rain_fall.october
            if 11 in rain_fall_month_list:
                total_rainfall = total_rainfall + rain_fall.november
            if 12 in rain_fall_month_list:
                total_rainfall = total_rainfall + rain_fall.december
        except:
            annual_rainfall = [29, 21, 37.5, 30.7, 52.6, 150, 299, 251.7, 179.2, 70.5, 39.8, 10.9]
            for month in rain_fall_month_list:
                total_rainfall = total_rainfall + annual_rainfall[month - 1]

        total_rainfall = total_rainfall / len(rain_fall_month_list)
        ## assign the rainfall
        model_rainfall = total_rainfall
        ## get the dataset and append in list for model
        model_para = [model_n, model_p, model_k, model_temp, model_humidity, model_ph, model_rainfall]

        ## model testing and get output
        # NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
        API_KEY = "6Pe2pNaBxpPB0eN7oyIPBQgDZ6d_ujIp8h4W1ik-pyk5"
        token_response = requests.post('https://iam.cloud.ibm.com/identity/token',
                                       data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
        mltoken = token_response.json()["access_token"]

        header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

        # NOTE: manually define and pass the array(s) of values to be scored in the next line
        payload_scoring = {"input_data": [
            {"field": ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall', 'label'], "values": [model_para]}]}

        response_scoring = requests.post(
            'https://us-south.ml.cloud.ibm.com/ml/v4/deployments/91bf6a6b-7d60-4e50-b75b-bc99fd76d42a/predictions?version=2021-07-08',
            json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})

        response_score = response_scoring.json()

        ## response _score containing the info of the output

        ## created a list in which order the probablity of each crop is returned by model
        list_of_ordered_crops = ["apple", "banana", "blackgram", "chickpea", "coconut",
                                 "coffee", "cotton", "grapes", "jute", "kidneybeans",
                                 "lentil", "maize", "mango", "mothbeans", "mungbean",
                                 "muskmelon", "orange", "papaya", "pigeonpeas",
                                 "pomegranate", "rice", "watermelon"]

        ##PIE CHART
        ## gather the info of the other crops for pie chart
        predicted_prob = response_score["predictions"][0]["values"][0][1]
        new_list = list(zip(list_of_ordered_crops, predicted_prob))
        sorted_list = sorted(new_list, key=lambda l: l[1], reverse=True)
        ## create an list in which the probablity is not zero
        chart_list = []
        for i in sorted_list:
            if i[1] == 0:
                pass
            else:
                chart_list.append(i)
        ## code for top5 or possible top but less than 5
        pie_chart_labels = []
        pie_chart_values = []
        temp_values = []
        for i in range(0, 5):
            try:
                pie_chart_labels.append(chart_list[i][0])
                temp_values.append(chart_list[i][1])
            except:
                break

        ## code for the value of of 1
        for val in temp_values:
            temp = val / sum(temp_values)
            temp = round(temp, 2)
            pie_chart_values.append(temp)
        pie_chart_values = [round(item * 100, 2) for item in pie_chart_values]

        ## if by chance during round sum become > 1
        if sum(pie_chart_values) > 100:
            pie_chart_values[0] = pie_chart_values[0] - (sum(pie_chart_values) - 100)
        if sum(pie_chart_values) < 100:
            pie_chart_values[0] = pie_chart_values[0] + (100 - sum(pie_chart_values))

        ## BAR CHART
        weather_list = ["Temperature", "Humidity", "Rainfall"]
        soil_list = ["Nitroegen", "Phosphorus", "Potassium", "Ph"]
        final_list = list()
        count = 0
        for crop_name in pie_chart_labels:
            crop_name = crop_name.lower()
            actual_crop_need = crop_details.query.filter_by(crop=crop_name).first()
            image_path =  crop_name + ".jpg"
            success_chance = pie_chart_values[count]
            weather_info = [round(actual_crop_need.temperature, 2),
                            round(actual_crop_need.humidity, 2),
                            round(actual_crop_need.rainfall, 2)]
            soil_info = [round(actual_crop_need.n, 2), round(actual_crop_need.p, 2),
                         round(actual_crop_need.k, 2), round(actual_crop_need.ph, 2)]
            prodcution_data = crop_name_info.query.filter_by(recommendation_name=crop_name).first()
            prodcution_name = prodcution_data.production_name
            final_list.append(
                {
                    "cropName" : crop_name,
                    "imagePath": image_path,
                    "successChance": success_chance,
                    "weatherInfo": weather_info,
                    "soilInfo": soil_info,
                    "productionName": prodcution_name
                })
            count = count + 1

        ##User Crop weather info
        user_weather_list = [round(model_temp, 2), round(model_humidity, 2), round(model_rainfall, 2)]
        user_soil_list = [model_n, model_p, model_k, model_ph]
        static_dict = dict()
        static_dict

        ## create an response dict
        response_dict = {
            "Top5CropInfo": final_list,
            "static_info": {
                "pieChartOfSuccessPercentageLabel": pie_chart_labels,
                "pieChartOfSuccessPercentageValue": pie_chart_values,
                "weatherBarChartLabel": weather_list,
                "soilBarChartLabel": soil_list,
                "weatherBarChartUserValue": user_weather_list,
                "soilBarChartUserValue": user_soil_list
            }
        }
        return jsonify(response_dict)


## api for yield prediction
@app.route("/yield", methods=['GET', 'POST'])
def yield_prediction():
    """
    function which take json input
    yield prediction
    list of name :["state", "city","season","crop","area"]
    example input:
    {
	"state" : "gujarat",
	"city" : "amreli",
	"season" : "kharif",
	"crop" :"rice",
	"area" : 120.12
    }
    """
    ## input code here
    if request.method == "POST":
        re = request.get_json()
        city = re["city"]
        state = re["state"]
        ## convert into lower case
        state = state.lower()
        city = city.lower()
        model_crop = re["crop"]
        model_crop = model_crop.lower()
        model_season = re["season"]
        model_season = model_season.lower()
        model_area = re["area"]
        model_area = int(model_area)

        ## store name of crop for the graph
        crop = model_crop
        ## preprocesss the code

        try:
            state_le = load("static/labelencoder/state_le.joblib")
            district_le = load("static/labelencoder/district_le.joblib")
            season_le = load("static/labelencoder/season_le.joblib")
            crop_le = load("static/labelencoder/crop_le.joblib")
            model_crop = crop_le.transform([model_crop])[0]
            model_season = season_le.transform([model_season])[0]
            model_state = state_le.transform([state])[0]
            model_city = district_le.transform([city])[0]
        except:
            response_dict = {
                "status": False,
                "message": "Enter Valid Data"
            }
            return jsonify(response_dict)

        model_city = int(model_city)
        model_state = int(model_state)
        model_crop = int(model_crop)
        model_season = int(model_season)
        model_para = [model_state, model_city, model_season, model_crop, model_area]

        ## prediction code here

        import requests
        # NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
        API_KEY = "S30qFHkYTHMDO81ijSRiGSiE1jOfnlt01Vtn9UBU2KqL"
        token_response = requests.post('https://iam.cloud.ibm.com/identity/token',
                                       data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
        mltoken = token_response.json()["access_token"]

        header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

        # NOTE: manually define and pass the array(s) of values to be scored in the next line
        payload_scoring = {"input_data": [
            {"fields": ["State_Name", "District_Name", "Season", "Crop", "Area"], "values": [model_para]}]}

        response_scoring = requests.post(
            'https://us-south.ml.cloud.ibm.com/ml/v4/deployments/180fe5c1-a652-4e59-8b33-781326790706/predictions?version=2021-07-16',
            json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})

        output = response_scoring.json()

        ## retrive the output

        pred_yield = output["predictions"][0]['values'][0][0]
        pred_production = pred_yield * model_area

        ## PIE CHART
        try:
            kharif_value = kharif_yield.query.filter_by(crop_name=crop).first()
            kharif_values = kharif_value.yield_value
        except:
            kharif_values = 0
        try:
            rabi_value = rabi_yield.query.filter_by(crop_name=crop).first()
            rabi_values = rabi_value.yield_value
        except:
            rabi_values = 0

        try:
            summer_value = summer_yield.query.filter_by(crop_name=crop).first()
            summer_values = summer_value.yield_value
        except:
            summer_values = 0

        try:
            winter_value = winter_yield.query.filter_by(crop_name=crop).first()
            winter_values = winter_value.yield_value
        except:
            winter_values = 0

        try:
            autumn_value = autumn_yield.query.filter_by(crop_name=crop).first()
            autumn_values = autumn_value.yield_value
        except:
            autumn_values = 0

        try:
            whole_year_value = whole_year_yield.query.filter_by(crop_name=crop).first()
            whole_year_values = whole_year_value.yield_value
        except:
            whole_year_values = 0

        season_name = ['kharif', 'rabi', 'summer', 'winter', 'autumn', 'whole year']
        yield_list = [kharif_values, rabi_values, summer_values, winter_values, autumn_values, whole_year_values]

        season_yield_dict = dict()
        pie_list = list()
        for season, value in zip(season_name, yield_list):
            if value == 0:
                pass
            else:
                season_yield_dict[season] = round(value, 2)
                pie_list.append(round(value, 2))
        bar_graph_label = list(season_yield_dict.keys())
        pie_final_list = list()
        sum_list = sum(pie_list)
        for val in pie_list:
            suceess = val / sum_list
            suceess = round(suceess, 2)
            pie_final_list.append(suceess * 100)

        ## reponse dict here
        response_dict = {
            "predYield": pred_yield,
            "predProduction": pred_production,
            "barGraphLabel": bar_graph_label,
            "barGraphvalue": yield_list,
            "pieChartLabel": bar_graph_label,
            "pieChartValue": pie_final_list
        }
        return jsonify(response_dict)


## rest api for the price
@app.route("/individual_price", methods=['GET', 'POST'])
def priceforecast():
    if request.method == 'POST':
        """
        function which will take crop name as an input
        """
        re = request.get_json()
        crop_name = re["crop_name"]
        crop_name = str(crop_name)
        crop_name = crop_name.lower()
        crop_data = crop(crop_name)
        model_name = crop_name + ".joblib"
        model_path = "static/models/" + model_name

        ## month number and name dictionary
        month = {'1': 'Janauary',
                 '2': 'February',
                 '3': 'March',
                 '4': 'April',
                 '5': 'May',
                 '6': 'June',
                 '7': 'July',
                 '8': 'August',
                 '9': 'September',
                 '10': 'October',
                 '11': 'November',
                 '12': 'December'}

        ##get the month and year for which we have to predict the price
        today = date.today()
        current_month = today.month
        current_year = today.year
        paramter_list = list()

        for i in range(12):
            if current_month >= 12:
                current_month = 1
                current_year = current_year + 1
                paramter_list.append([current_month, current_year])
            else:
                current_month = current_month + 1
                paramter_list.append([current_month, current_year])

        ## prediction time for tweleve monthforecast
        min_index = 0
        max_index = 0
        max_value = 0
        min_value = 1000000
        iter = 0
        prediction_list = list()
        change = list()
        today1 = date.today()
        current_month1 = today1.month
        current_year1 = today1.year
        model = load(model_path)
        current_wpi = model.predict(pd.DataFrame([current_month1, current_year1]).T)
        for para in paramter_list:
            pred = model.predict(pd.DataFrame(para).T)[0]
            month_name = month[str(para[0])]
            year = para[1]
            prediction_list.append([month_name, year, pred])
            change.append((((pred - current_wpi) * 100) / current_wpi)[0])
            if pred > max_value:
                max_value = pred
                max_index = iter
            if pred < min_value:
                min_value = pred
                min_index = iter
            iter = iter + 1

        ## get the data into price
        final_list = list()

        ##here work is not done
        try:
            base_price = msp_details.query.filter_by(crop=crop_name).first()
            base2021 = base_price.year2021
            base2020 = base_price.year2020
        except:
            base2021 = msp(crop_name)
            base2020 = base2021 - 300
        for i, val in enumerate(prediction_list):
            month_year = str(val[0]) + "," + str(val[1])
            price = round((val[2] * base2021) / 100, 2)
            change_temp = round(change[i], 2)
            wpi = val[2]
            final_list.append([month_year, price, wpi, change_temp])
        forecast_x = list()
        forecast_y_price = list()
        forecast_y_wpi = list()
        change_itration = list()

        ## graph information:
        for li in final_list:
            forecast_x.append(li[0])
            forecast_y_price.append(li[1])
            forecast_y_wpi.append(li[2])
            change_itration.append((li[3]))
        forecast_y_price_range = (min(forecast_y_price) - 120, max(forecast_y_price) + 120)
        forecast_y_wpi_range = (min(forecast_y_price) - 2.0, max(forecast_y_price) + 2.0)

        maxmimum_price_data = final_list[max_index]
        minimum_price_data = final_list[min_index]

        ## tweleve motnh previous
        previous_price_list = twelvemonthprevious(model, month, crop_name)
        previous_x = list()
        previous_y_price = list()
        previous_y_wpi = list()
        for li in previous_price_list:
            previous_x.append(li[0])
            previous_y_price.append(li[1])
            previous_y_wpi.append(li[2])
        previous_y_wpi.reverse()
        previous_y_price.reverse()
        previous_x.reverse()
        previous_price_list.reverse()
        previous_y_price_range = (min(previous_y_price) - 120, max(previous_y_price) + 120)
        previous_y_wpi_range = (min(previous_y_wpi) - 2.0, max(previous_y_wpi) + 2.0)
        image = crop_name + ".jpg"
        ##response dict
        response_dict = {
            "cropName" : crop_name,
            "priceForecast": final_list,
            "previousYear": previous_price_list,
            "forGraphForecastX": forecast_x,
            "forGraphForecastYPrice": forecast_y_price,
            "forGraphForecastYWpi": forecast_y_wpi,
            "forGraphForecastYchange": change_itration,
            "forGraphForecastYPriceRange": forecast_y_price_range,
            "forGraphForecastYWpiRange": forecast_y_wpi_range,
            "forGraphPreviousX": previous_x,
            "forGraphPreviousYPrice": previous_y_price,
            "forGraphPreviousYWpi": previous_y_wpi,
            "forGraphPreviousYPriceRange": previous_y_price_range,
            "forGraphPreviousYWpiRange": previous_y_wpi_range,
            "maximumPrice": maxmimum_price_data,
            "minimumPrice": minimum_price_data,
            "imageUrl": image,
            "productionState": crop_data[1],
            "productionSeason": crop_data[2],
            "exportCountry": crop_data[3],
            "basePrice2021": base2021,
            "basePrice2020": base2020
        }
        return jsonify(response_dict)


## for twelevemonth previous price
def twelvemonthprevious(model, month, crop_name):
    from datetime import date
    today = date.today()
    current_month = today.month
    current_year = today.year
    paramter_list = list()
    prediction_list = list()
    change = list()
    final_list = list()
    for i in range(12):
        if current_month == 1:
            current_month = 12
            current_year = current_year - 1
        else:
            current_month = current_month - 1
        paramter_list.append([current_month, current_year])
    for para in paramter_list:
        pred = model.predict(pd.DataFrame(para).T)[0]
        month_name = month[str(para[0])]
        year = para[1]
        prediction_list.append([month_name, year, pred])
    try:
        base_price = msp_details.query.filter_by(crop=crop_name).first()
        base2021 = base_price.year2021
        base2020 = base_price.year2020
    except:
        base2021 = msp(crop_name)
        base2020 = base2021 - 300
    for i, val in enumerate(prediction_list):
        month_year = str(val[0]) + "," + str(val[1])
        price = round((val[2] * base2020) / 100, 2)
        wpi = val[2]
        final_list.append([month_year, price, wpi])
    return final_list


def get_change_list():
    """
    function which will return the list containing the change in demand
    :return: change_list,current_month_wpi,previous_month_wpi
    """
    today = date.today()
    current_month = today.month
    current_year = today.year
    current_month_pred = dict()
    previous_month_pred = dict()
    change = list()
    commodity_list = ["arhar", "bajra", "barley", "copra", "cotton", "sesamum", "gram", "groundnut",
                      "jowar", "maize", "masoor", "moong", "niger", "paddy", "ragi", "rape", "jute",
                      "safflower", "soyabean", "sugarcane", "sunflower", "urad", "wheat"]
    if current_month == 1:
        previous_month = 12
        previous_year = current_year - 1
    else:
        previous_month = current_month - 1
        previous_year = current_year
    for crop in commodity_list:
        model_path = "static/models/" + crop + ".joblib"
        model = load(model_path)
        current_month_wpi = model.predict(pd.DataFrame([current_month, current_year]).T)[0]
        current_month_pred[crop] = current_month_wpi
        previous_month_wpi = model.predict(pd.DataFrame([previous_month, previous_year]).T)[0]
        previous_month_pred[crop] = previous_month_wpi
        change.append((((current_month_wpi - previous_month_wpi) * 100 / previous_month_wpi), crop))
    sorted_change = change
    return sorted_change, current_month_pred, previous_month_pred


def top5list(ascending):
    """
    function which take true or false as an argument and return the top5 loosers and gainers list
    :param ascending: True or False
    :return: list
    """
    sorted_change, current_month_pred, previous_month_pred = get_change_list()
    sorted_change.sort(reverse=ascending)
    to_send = list()
    for j in range(0, 5):
        name = sorted_change[j][1]
        change_ammount = sorted_change[j][0]
        try:
            base_price = msp_details.query.filter_by(crop=name).first()
            base2021 = base_price.year2021
        except:
            base2021 = msp(name)
        current_month_price = round((current_month_pred[name] * base2021) / 100, 2)
        previous_month_price = round((previous_month_pred[name] * base2021) / 100, 2)
        to_send.append([name, current_month_price, previous_month_price, current_month_pred[name],
                        previous_month_pred[name], change_ammount])
    return to_send


## rest api for the top5 gainers and loosers:
@app.route("/top5", methods=['GET', 'POST'])
def top5winners_loosers():
    top_5_winners = top5list(True)
    top_5_loosers = top5list(False)
    ## top_5_winners has [name,current_month_price,previous_month_price,current_wpi,previous_wpi]
    ## response dict here
    response_dict = {
        "top5Winner": top_5_winners,
        "top5Loosers": top_5_loosers
    }
    return jsonify(response_dict)


    # if __name__ == '__main__':
    #     app.run(debug=True)

@app.route("/signup", methods=['POST'])
def signup():
    if request.method == 'POST':
        re = request.get_json()
        email = re['email']
        password = re['password']
        username = re['username']
    newusr = user.query.filter_by(email=email).first()
    if not newusr:
        auth_key = uuid.uuid4()
        api_key = uuid.uuid4()
        print('second step')
        newusr = user(username=username, email=email, hashed_password=password, auth_key=auth_key, api_token=api_key)
        print('adding user')
        db.session.add(newusr)
        print('commiting user')
        db.session.commit()
        response = {"details": newusr.id}
        print(type(newusr))
        return make_response(jsonify(response), 200)
    else:
        response = {"Message": "User already regstred"}
        return jsonify(response)


@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        re = request.get_json()
        email = re['email']
        hashed_password = re['password']
        loguser = user.query.filter_by(email=email, hashed_password=hashed_password).first()
        if not loguser:
            response = {"isAuthenticated": False}
            return jsonify(response)
        claims = {
            'id': loguser.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=10000)
        }
        token = jwt.encode(claims,app.config['SECRET_KEY'],algorithm="HS256")
        response = {"user": loguser.id, "token": token}
        return jsonify(response)

def model_train(crop_recommendation, yield_dataset, pass_dict):
        x = crop_recommendation.drop(['crop'], axis=1)
        y = crop_recommendation['crop']
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)
        model = RandomForestClassifier()
        model.fit(x_train, y_train)
        accuracy = model.score(x_test, y_test)
        accuracy = round(accuracy, 2) * 100
        path1 = "static/usermodel/" + pass_dict['api_key'] + "_" + pass_dict['model_name'] + "_recommendation.joblib"
        dump(model, path1)

        ##train the yield model
        x1 = yield_dataset.drop(['yield'], axis=1)
        y1 = yield_dataset['yield']
        crops = list(x1['crop'].unique())
        crops.sort()
        print(crops)
        le = LabelEncoder()
        le = le.fit(x1['crop'])
        x1['crop'] = le.transform(x1['crop'])
        path2 = "static/usermodel/" + pass_dict['api_key'] + "_" + pass_dict['model_name'] + "_labelencoder.joblib"
        dump(le, path2)
        model1 = RandomForestRegressor()
        model1.fit(x1, y1)
        path3 = "static/usermodel/" + pass_dict['api_key'] + "_" + pass_dict['model_name'] + "_yield.joblib"
        dump(model1, path3)

        ##insert into database
        pm = personal_model(api_token=pass_dict['api_key'], model_name=pass_dict['model_name'],
                            recommendation_model=path1, labelencoder_model=path2,
                            yield_model=path3, crops=crops, state=pass_dict['state_name'],
                            city=pass_dict['city_name'])
        db.session.add(pm)
        db.session.commit()
        response = {
            "result": True,
            "messgae": "model training is done !! now you can use your own model",
        }
        return response


## for training the personal model
@app.route("/personal_model", methods=['POST'])
@token_required
def readcsv(current_user):
    if request.method == 'POST':
        id = current_user.id
        user_data = user.query.filter_by(id=id).first()
        api_key = user_data.api_token
        file = request.files['csvfile']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        path = "static/" + filename
        data = pd.read_csv(path)
        print(data)
        model_name = request.form.get('model_name')
        city_name = request.form.get('city_name')
        state_name = request.form.get('state')
        pass_dict = {
            "api_key": api_key,
            "model_name": model_name,
            "city_name": city_name,
            "state_name": state_name,
        }
        print(pass_dict)
        response_dict = dict()
        model_check = personal_model.query.filter_by(api_token=api_key, model_name=model_name).count()
        if model_check != 0:
            response_dict = {
                "result": False,
                "message": "Already one model is existing !try different name"
            }
            return jsonify(response_dict)
        try:
            data = pd.read_csv(path)
        except:
            response_dict = {
                "result": False,
                "message": "Uploaded csv file is not valid or its corrupted"
            }
            return jsonify(response_dict)
        if data.isnull().sum().sum() > 0:
            response_dict = {
                "result": False,
                "message": "the file has missing values"
            }
            return jsonify(response_dict)
        if len(data.columns) != 11:
            response_dict = {
                "result": False,
                "message": "csv file must have 11 columns"
            }
            return jsonify(response_dict)
        data_columns_list = ['n', 'p', 'k', 'temperature', 'humidity', 'ph', 'rainfall', 'crop', 'season', 'area',
                             'production']
        if list(data.columns) != data_columns_list:
            response_dict = {
                "result": False,
                "message": "column name in csv file is not matching with demo csv file"
            }
            return jsonify(response_dict)
        try:
            data['n'] = data['n'].astype('float64')
            data['p'] = data['p'].astype('float64')
            data['k'] = data['k'].astype('float64')
            data['ph'] = data['ph'].astype('float64')
            data['temperature'] = data['temperature'].astype('float64')
            data['humidity'] = data['humidity'].astype('float64')
            data['crop'] = data['crop'].str.lower()
            data['crop'] = data['crop'].str.strip()
            data['season'] = data['season'].str.lower()
            data['season'] = data['season'].str.strip()
            data['seasons'] = 0
            data.loc[data.season == "kharif", "seasons"] = 1
            data.loc[data.season == "rabi", "seasons"] = 2
            data.loc[data.season == "autumn", "seasons"] = 3
            data.loc[data.season == "summer", "seasons"] = 4
            data.loc[data.season == "winter", "seasons"] = 5
            data.loc[data.season == "whole year", "seasons"] = 6
            data['area'] = data['area'].astype('float64')
            data['production'] = data['production'].astype('float64')
            data['yield'] = data['production'] / data['area']
        except:
            response_dict = {
                "result": False,
                "message": "value of the csv file is not in valid datatypes"
            }
            return jsonify(response_dict)
        recommendation_dataset = data.drop(['seasons', 'area', 'yield', 'production', 'season'], axis=1)
        yield_dataset = data.drop(['n', 'p', 'k', 'ph', 'rainfall', 'humidity', 'temperature', 'production', 'season'],
                                  axis=1)

        response = model_train(recommendation_dataset, yield_dataset, pass_dict)

    return jsonify(response)


@app.route("/user_recommendation_model", methods=['POST'])
@token_required
def personal_use(current_user):
    if request.method == "POST":
        id = current_user.id
        user_data = user.query.filter_by(id=id).first()
        api_token = user_data.api_token
        re = request.get_json()
        model_name = re["model_name"]
        ## convert into lower case
        model_ph = re["ph"]
        model_n = re["n"]
        model_p = re["p"]
        model_k = re["k"]
        model_check = personal_model.query.filter_by(api_token=api_token, model_name=model_name).first()
        response_dict = dict()
        print(model_check)
        try:
            city = model_check.city
            state = model_check.state
            re_path = model_check.recommendation_model
            crop_list = model_check.crops
            crop_list = crop_list.replace("{", "")
            crop_list = crop_list.replace("}", "")
            words = crop_list.split(',')
            list_of_ordered_crops = list()
            for word in words:
                list_of_ordered_crops.append(word)
        except:
            response_dict = {
                "result": False,
                "message": "Please Try again "
            }
            return jsonify(response_dict)
        try:
            user_api = "6c4043b2272bb3cf1e7330517937f690"
            ## extract the weather data such as temp,humidity as per user given location
            complete_api_link = "https://pro.openweathermap.org/data/2.5/forecast/climate?q=" + \
                                city + "&appid=" + user_api
            api_link = requests.get(complete_api_link)
            ## response of api in api_data
            api_data = api_link.json()
            ## lets get the average of the temp and humidity for monthly
            humidity_sum = 0
            temp_sum = 0
            ll = api_data["list"]
            for i in range(30):
                temp = ll[i]['temp']
                temp_avg = (temp['day'] + temp['min'] + temp["max"] + temp["night"] + temp["eve"]) / 5
                temp_sum = (temp_avg - 273) + temp_sum
                humidity = ll[i]['humidity']
                humidity_sum = humidity + humidity_sum
            ## store the of avg of humidity and temperature in the varibale which we pass to model

            model_humidity = humidity_sum / 30
            model_temp = temp_sum / 30
        except:
            model_humidity = 60
            model_temp = 25
        today = date.today()
        current_month = today.month
        current_date = today.day
        current_year = today.year

        ## harvesting time get from database
        harvesting_time = 4
        ## create an list for the month number for which we have to get rainfall
        temp_month = current_month
        rain_fall_month_list = []
        for i in range(harvesting_time):
            if temp_month > 12:
                temp_month = 1
            rain_fall_month_list.append(temp_month)
            temp_month = temp_month + 1
        total_rainfall = 0
        try:
            rain_fall = rain_info.query.filter_by(state=state).first()
            ## get the rainfall from the database for the given month
            if 1 in rain_fall_month_list:
                total_rainfall = total_rainfall + rain_fall.january
            if 2 in rain_fall_month_list:
                total_rainfall = total_rainfall + rain_fall.february
            if 3 in rain_fall_month_list:
                total_rainfall = total_rainfall + rain_fall.march
            if 4 in rain_fall_month_list:
                total_rainfall = total_rainfall + rain_fall.april
            if 5 in rain_fall_month_list:
                total_rainfall = total_rainfall + rain_fall.may
            if 6 in rain_fall_month_list:
                total_rainfall = total_rainfall + rain_fall.june
            if 7 in rain_fall_month_list:
                total_rainfall = total_rainfall + rain_fall.july
            if 8 in rain_fall_month_list:
                total_rainfall = total_rainfall + rain_fall.august
            if 9 in rain_fall_month_list:
                total_rainfall = total_rainfall + rain_fall.september
            if 10 in rain_fall_month_list:
                total_rainfall = total_rainfall + rain_fall.october
            if 11 in rain_fall_month_list:
                total_rainfall = total_rainfall + rain_fall.november
            if 12 in rain_fall_month_list:
                total_rainfall = total_rainfall + rain_fall.december
        except:
            annual_rainfall = [29, 21, 37.5, 30.7, 52.6, 150, 299, 251.7, 179.2, 70.5, 39.8, 10.9]
            for month in rain_fall_month_list:
                total_rainfall = total_rainfall + annual_rainfall[month - 1]

        total_rainfall = total_rainfall / len(rain_fall_month_list)
        ## assign the rainfall
        model_rainfall = total_rainfall
        ## get the dataset and append in list for model
        model_para = [model_n, model_p, model_k, model_temp, model_humidity, model_ph, model_rainfall]

        model = load(re_path)
        predicted_prob = model.predict_proba(pd.DataFrame(model_para).T)
        new_list = list(zip(list_of_ordered_crops, predicted_prob[0]))
        sorted_list = sorted(new_list, key=lambda l: l[1], reverse=True)
        ## create an list in which the probablity is not zero
        chart_list = []
        for i in sorted_list:
            if i[1] == 0:
                pass
            else:
                chart_list.append(i)
        ## code for top5 or possible top but less than 5
        pie_chart_labels = []
        pie_chart_values = []
        temp_values = []
        for i in range(0, 5):
            try:
                pie_chart_labels.append(chart_list[i][0])
                temp_values.append(chart_list[i][1])
            except:
                break

        ## code for the value of of 1
        for val in temp_values:
            temp = val / sum(temp_values)
            temp = round(temp, 2)
            pie_chart_values.append(temp)
        pie_chart_values = [round(item * 100, 2) for item in pie_chart_values]

        ## if by chance during round sum become > 1
        if sum(pie_chart_values) > 100:
            pie_chart_values[0] = pie_chart_values[0] - (sum(pie_chart_values) - 100)
        if sum(pie_chart_values) < 100:
            pie_chart_values[0] = pie_chart_values[0] + (100 - sum(pie_chart_values))

        count = 0
        final_list = list()
        for crop_name in pie_chart_labels:
            success_chance = pie_chart_values[count]
            final_list.append(
                {
                    "cropName": crop_name,
                    "successChance": success_chance,
                })
            count = count + 1

        response_dict = {
            "Top5CropInfo": final_list,
            "static_info": {
                "pieChartOfSuccessPercentageLabel": pie_chart_labels,
                "pieChartOfSuccessPercentageValue": pie_chart_values
            }
        }
        return jsonify(response_dict)

@app.route("/user_yield_model" ,methods=['POST'])
@token_required
def yield_model(current_user):
    if request.method == "POST":
        id = current_user.id
        user_data = user.query.filter_by(id=id).first()
        api_token = user_data.api_token
        re = request.get_json()
        model_name = re["model_name"]
        season = re["season"]
        season = season.lower()
        crop = re["crop"]
        model_area = re["area"]
        model_area = int(model_area)
        model_season = 1
        response_dict = dict()
        if season == "kharif":
            model_season = 1
        elif season == "rabi":
            model_season = 2
        elif season == "autumn":
            model_season = 3
        elif season == "summer":
            model_season == 4
        elif season == "winter":
            model_season =5
        else:
            model_season = 6
        model_check = personal_model.query.filter_by(api_token=api_token, model_name=model_name).first()
        try:
            city = model_check.city
            state = model_check.state
            re_path = model_check.recommendation_model
            le_path = model_check.labelencoder_model
            yield_path = model_check. yield_model
            crop_list = model_check.crops
        except:
            response_dict = {
                "result": False,
                "message": "Please Try again "
            }
            return jsonify(response_dict)
        try:
            crop_le = load(le_path)
            model_crop = crop_le.transform(crop)[0]
        except:
            model_crop= 1

        model_para = [model_crop,model_area,model_season]
        print(model_para)
        try:
            model = load(yield_path)
            predyield = model.predict(pd.DataFrame(model_para).T)[0]
            predProduction = model_area * predyield
        except:
            predyield = 22.3444
            predProduction = model_area * predyield
        print(predyield)
        response_dict = {
            "predYield" : predyield,
            "predProduction" : predProduction
        }
        return jsonify(response_dict)

@app.route("/user_models" ,methods=['GET'])
@token_required
def models(current_user):
    id = current_user.id
    user_data = user.query.filter_by(id=id).first()
    api_token = user_data.api_token
    model_check = personal_model.query.filter_by(api_token=api_token).all()
    model_list = list()
    for model in model_check:
        model_list.append(model.model_name)
    response_dict = {
        "names" : model_list
    }
    return jsonify(response_dict)

@app.route("/delete_model" ,methods=['POST'])
@token_required
def delete_model(current_user):
    re = request.get_json()
    model_name = re["model_name"]
    id = current_user.id
    user_data = user.query.filter_by(id=id).first()
    api_token = user_data.api_token
    response_dict = dict()
    if True:
        me = personal_model.query.filter_by(api_token=api_token,model_name=model_name).first()
        db.session.delete(me)
        db.session.commit()
        print(me)
        response_dict = {
            "result" : True
        }


    return jsonify(response_dict)
@app.route("/check", methods=['GET'])
@token_required
def new(current_user):
    print(current_user.id)
    id = current_user.id
    user_data = user.query.filter_by(id=id).first()
    print(user_data.api_token)
    response_dict = dict()
    response_dict = {
        "isAuthenticated": True,
        "api_token": user_data.api_token,
    }
    return jsonify(response_dict)
