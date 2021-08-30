from flask import request, jsonify
from app import app
from .models import *
from .const import HttpStatus
from joblib import load
import pandas as pd
import requests
from datetime import date
import os
import numpy as np

def crop(crop_name):
    crop_data = {
    "wheat":["/static/images/wheat.jpg", "U.P., Punjab, Haryana, Rajasthan, M.P., bihar", "rabi","Sri Lanka, United Arab Emirates, Taiwan"],
    "paddy":["/static/images/paddy.jpg", "W.B., U.P., Andhra Pradesh, Punjab, T.N.", "kharif","Bangladesh, Saudi Arabia, Iran"],
    "barley":["/static/images/barley.jpg", "Rajasthan, Uttar Pradesh, Madhya Pradesh, Haryana, Punjab", "rabi","Oman, UK, Qatar, USA"],
    "maize":["/static/images/maize.jpg", "Karnataka, Andhra Pradesh, Tamil Nadu, Rajasthan, Maharashtra", "kharif", "Hong Kong, United Arab Emirates, France"],
    "bajra":["/static/images/bajra.jpg", "Rajasthan, Maharashtra, Haryana, Uttar Pradesh and Gujarat", "kharif", "Oman, Saudi Arabia, Israel, Japan"],
    "copra":["/static/images/copra.jpg", "Kerala, Tamil Nadu, Karnataka, Andhra Pradesh, Orissa, West Bengal","rabi", "Veitnam, Bangladesh, Iran, Malaysia"],
    "cotton":["/static/images/cotton.jpg", "Punjab, Haryana, Maharashtra, Tamil Nadu, Madhya Pradesh, Gujarat", " China, Bangladesh, Egypt"],
    "masoor":["/static/images/masoor.jpg", "Uttar Pradesh, Madhya Pradesh, Bihar, West Bengal, Rajasthan", "rabi", "Pakistan, Cyprus,United Arab Emirates"],
    "gram":["/static/images/gram.jpg", "Madhya Pradesh, Maharashtra, Rajasthan, Uttar Pradesh, Andhra Pradesh & Karnataka", "rabi", "Veitnam, Spain, Myanmar"],
    "groundnut":["/static/images/groundnut.jpg", "Andhra Pradesh, Gujarat, Tamil Nadu, Karnataka, and Maharashtra", "kharif", "Indonesia, Jordan, Iraq"],
    "arhar":["/static/images/arhar.jpg", "Maharashtra, Karnataka, Madhya Pradesh and Andhra Pradesh", "kharif", "United Arab Emirates, USA, Chicago"],
    "sesamum":["/static/images/sesamum.jpg", "Maharashtra, Rajasthan, West Bengal, Andhra Pradesh, Gujarat", "rabi", "Iraq, South Africa, USA, Netherlands"],
    "jowar":["/static/images/jowar.jpg", "Maharashtra, Karnataka, Andhra Pradesh, Madhya Pradesh, Gujarat", "kharif", "Torronto, Sydney, New York"],
    "moong":["/static/images/moong.jpg", "Rajasthan, Maharashtra, Andhra Pradesh", "rabi", "Qatar, United States, Canada"],
    "niger":["/static/images/niger.jpg", "Andha Pradesh, Assam, Chattisgarh, Gujarat, Jharkhand", "kharif", "United States of American,Argenyina, Belgium"],
    "rape":["/static/images/rape.jpg", "Rajasthan, Uttar Pradesh, Haryana, Madhya Pradesh, and Gujarat", "rabi", "Veitnam, Malaysia, Taiwan"],
    "jute":["/static/images/jute.jpg", " West Bengal , Assam , Orissa , Bihar , Uttar Pradesh", "kharif", "JOrdan, United Arab Emirates, Taiwan"],
    "safflower":["/static/images/safflower.jpg",  "Maharashtra, Karnataka, Andhra Pradesh, Madhya Pradesh, Orissa", "kharif", " Philippines, Taiwan, Portugal"],
    "soyabean":["/static/images/soyabean.jpg",  "Madhya Pradesh, Maharashtra, Rajasthan, Madhya Pradesh and Maharashtra", "kharif", "Spain, Thailand, Singapore"],
    "urad":["/static/images/urad.jpg",  "Andhra Pradesh, Maharashtra, Madhya Pradesh, Tamil Nadu", "rabi", "United States, Canada, United Arab Emirates"],
    "ragi":["/static/images/ragi.jpg",  "Maharashtra, Tamil Nadu and Uttarakhand", "kharif", "United Arab Emirates, New Zealand, Bahrain"],
    "sunflower":["sunflower.jpg",  "Karnataka, Andhra Pradesh, Maharashtra, Bihar, Orissa", "rabi", "Phillippines, United States, Bangladesh"],
    "sugarcane":["sugarcane.jpg","Uttar Pradesh, Maharashtra, Tamil Nadu, Karnataka, Andhra Pradesh" , "kharif", "Kenya, United Arab Emirates, United Kingdom"]
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
        return "<h1>Welcome to Crop Recommendation</h1><p>Created By: Teerth Sankesara</p>"
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
    if request.method =="POST":
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
                total_rainfall = total_rainfall + annual_rainfall[month-1]

        total_rainfall = total_rainfall/len(rain_fall_month_list)

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

        ## extract the predicted crop from the response of model adn convert into lower case
        predicted_crop = response_score["predictions"][0]["values"][0][0]
        predicted_crop = predicted_crop.lower()


        ## get the image path of the crop
        image_path = "static/image/"+predicted_crop+".jpg"
        ##get the need of the crop from the database
        actual_crop_need = crop_details.query.filter_by(crop=predicted_crop).first()

        para_list =["n","p","k","temperature","humidity","ph","rainfall"]
        value_list = [actual_crop_need.n,actual_crop_need.p,actual_crop_need.k,
                      actual_crop_need.temperature,actual_crop_need.humidity,
                      actual_crop_need.ph,actual_crop_need.rainfall]
        ## by default bar chart
        predicted_crop_soil_value = [round(actual_crop_need.n,2), round(actual_crop_need.p,2),
                                    round(actual_crop_need.k,2), round(actual_crop_need.ph,2)]
        predicted_crop_weather_value = [round(actual_crop_need.temperature,2),
                                       round(actual_crop_need.humidity,2),
                                       round(actual_crop_need.rainfall,2)]

        ## make list of combine info
        actual_crop_info = list(zip(para_list,value_list))

        ## get the index at which the probability is there for the best crop
        predicted_crop_index = list_of_ordered_crops.index(predicted_crop)

        ## success chances of predicted crop
        predicted_crop_success_chances = response_score["predictions"][0]["values"][0][1][predicted_crop_index]

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


        ## BAR CHART
        weather_list = ["Temperature", "Humidity", "Rainfall"]
        weather_info_list = list()
        soil_list = ["Nitroegen","Phosphorus","Potassium","Ph"]
        soil_info_list = list()
        final_dict= dict()
        final_list = list()
        count =0
        for crop_name in pie_chart_labels:
            crop_name = crop_name.lower()
            actual_crop_need = crop_details.query.filter_by(crop=crop_name).first()
            image_path ="static/image/"+crop_name+".jpg"
            success_chance = pie_chart_values[count]
            weather_info = [round(actual_crop_need.temperature,2),
                            round(actual_crop_need.humidity,2),
                            round(actual_crop_need.rainfall,2)]
            soil_info = [round(actual_crop_need.n,2), round(actual_crop_need.p,2),
                         round(actual_crop_need.k,2), round(actual_crop_need.ph,2)]

            final_list.append({crop_name:
                                   {
                                       "imagePath" : image_path,
                                       "successChance" : success_chance,
                                       "weatherInfo" : weather_info,
                                       "soilInfo" : soil_info
                                   }})
            count = count + 1
            ## create a weather list inside weather dict with crop_name_key
            # weather_info_list.append({crop_name:[round(actual_crop_need.temperature,2),
            #                            round(actual_crop_need.humidity,2),
            #                            round(actual_crop_need.rainfall,2)]})
            #
            # ## create a soil list inside soil dict with crop_name key
            # soil_info_list.append({crop_name:[round(actual_crop_need.n,2), round(actual_crop_need.p,2),
            #                         round(actual_crop_need.k,2), round(actual_crop_need.ph,2)]})
        # final_list.append(final_dict)



        ## make a list of what actually user having
        user_crop_info_list = [model_n,model_p,model_k,model_temp,model_humidity,model_ph,model_rainfall]
        user_crop_info = list(zip(para_list, user_crop_info_list))

        ##User Crop weather info
        user_weather_list = [round(model_temp,2),round(model_humidity,2),round(model_rainfall,2)]
        user_soil_list = [model_n,model_p,model_k,model_ph]

        ## create an response dict
        response_dict = {
            
            # "chnacesOfSuccessOfPredictedCrop": predicted_crop_success_chances,
            # "otherCropProbForPieChart": chart_list,
            # "pieChartOfSuccessPercentageLabel" : pie_chart_labels,
            # "pieChartOfSuccessPercentageValue" : pie_chart_values,
            # "weatherBarChartLabel" : weather_list,
            # "weatherBarChartCropValue" : weather_info_list,
            # "soilBarChartLabel" : soil_list,
            # "soilBarChartCropValue": soil_info_list,
            # "weatherBarChartUserValue" : user_weather_list,
            # "soilBarChartUserValue" : user_soil_list,
            "Top5CropInfo" : final_list,
            "chatbot" : 45
            # "byDefaultWeatherBarChartValue" : predicted_crop_weather_value,
            # "byDefaultSoilChartValue" : predicted_crop_soil_value,
            # "actualCropInfo" : actual_crop_info,
            # "userCropInfo" : user_crop_info,

        }
        return response_dict


## api for yield prediction
@app.route("/yield" , methods=['GET','POST'])
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
    if request.method =="POST":
        re = request.get_json()
        city = re["city"]
        state = re["state"]
        ## convert into lower case

        state = state.lower()
        city = city.lower()

        model_crop = re["crop"]
        model_season = re["season"]
        model_area = re["area"]

    ## preprocesss the code

        state_le = load("static/labelencoder/state_le.joblib")
        district_le = load("static/labelencoder/district_le.joblib")
        season_le = load("static/labelencoder/season_le.joblib")
        crop_le = load("static/labelencoder/crop_le.joblib")

        model_crop = crop_le.transform([model_crop])[0]
        model_season = season_le.transform([model_season])[0]
        model_state = state_le.transform([state])[0]
        model_city = district_le.transform([city])[0]
        model_city = int(model_city)
        model_state = int(model_state)
        model_crop = int(model_crop)
        model_season = int(model_season)
        model_para = [model_state,model_city,model_season,model_crop,model_area]

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

    ## reponse dict here

        response_dict = {
            "predYield" : pred_yield,
            "predProduction" : pred_production
        }
        return response_dict



## rest api for the price
@app.route("/individual_price" ,methods=['GET','POST'])
def priceforecast():
    if request.method == 'POST':
        """
        function which will take crop name as an input
        """
        re = request.get_json()
        crop_name =  re["crop_name"]
        crop_name = str(crop_name)
        crop_name = crop_name.lower()
        crop_data = crop(crop_name)
        model_name = crop_name + ".joblib"
        model_path =  "static/models/"+ model_name


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
        current_wpi = model.predict(pd.DataFrame([current_month1,current_year1]).T)
        for para in paramter_list:
            pred = model.predict(pd.DataFrame(para).T)[0]
            month_name = month[str(para[0])]
            year = para[1]
            prediction_list.append([month_name,year,pred])
            change.append((((pred-current_wpi)*100)/current_wpi)[0])
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
            final_list.append([month_year,price,wpi,change_temp])
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
        previous_price_list =twelvemonthprevious(model,month,crop_name)
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
        previous_y_price_range = (min(previous_y_price)-120,max(previous_y_price)+120)
        previous_y_wpi_range = (min(previous_y_wpi)-2.0,max(previous_y_wpi)+2.0)


        ##response dict
        response_dict = {
            "priceForecast" : final_list,
            "previousYear": previous_price_list,
            "forGraphForecastX" : forecast_x,
            "forGraphForecastYPrice" : forecast_y_price,
            "forGraphForecastYWpi" : forecast_y_wpi,
            "forGraphForecastYchange" : change_itration,
            "forGraphForecastYPriceRange" :forecast_y_price_range,
            "forGraphForecastYWpiRange" : forecast_y_wpi_range,
            "forGraphPreviousX" : previous_x,
            "forGraphPreviousYPrice": previous_y_price,
            "forGraphPreviousYWpi" : previous_y_wpi,
            "forGraphPreviousYPriceRange":previous_y_price_range,
            "forGraphPreviousYWpiRange" : previous_y_wpi_range,
            "maximumPrice" : maxmimum_price_data,
            "minimumPrice" : minimum_price_data,
            "imageUrl" : crop_data[0],
            "productionState" : crop_data[1],
            "productionSeason": crop_data[2],
            "exportCountry" : crop_data[3],
            "basePrice2021" : base2021,
            "basePrice2020" : base2020
        }
        return response_dict

## for twelevemonth previous price
def twelvemonthprevious(model,month,crop_name):
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
    return sorted_change,current_month_pred,previous_month_pred

def top5list(ascending):
    """
    function which take true or false as an argument and return the top5 loosers and gainers list
    :param ascending: True or False
    :return: list
    """
    sorted_change,current_month_pred,previous_month_pred = get_change_list()
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
                        previous_month_pred[name],change_ammount])
    return to_send

## rest api for the top5 gainers and loosers:
@app.route("/top5", methods=['GET','POST'])
def top5winners_loosers():
    top_5_winners = top5list(True)
    top_5_loosers = top5list(False)
    ## top_5_winners has [name,current_month_price,previous_month_price,current_wpi,previous_wpi]
    ## response dict here
    response_dict={
        "top5Winner" : top_5_winners,
        "top5Loosers":top_5_loosers
    }
    return  response_dict


if __name__ == '__main__':
    app.run(debug=True)