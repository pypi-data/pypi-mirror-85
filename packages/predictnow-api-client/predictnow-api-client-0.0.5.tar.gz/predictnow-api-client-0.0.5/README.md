A library python project that encapsulate Rest Client features (Http Client). Hiding those (complexity) http request details like to consume PredictNow RestfulApi. By simply giving high-level facade, i.e. pdApi.Train(), pdApiPredict().

By doing so, client no need to set up http client boilerplate codes to access PredictNow Api.


Contains features:

- Setting API key used to hit rest api

- Methods train() & predict() to hit the restapi accordingly

- Save Output

 

**usage** 

```from predictnow.pdapi import PredictNowClient

# Setup client along with its api key
api_key = "<YOUR_API_KEY>" # omitted for now
api_host = "http://localhost:5000"
client = PredictNowClient(api_host, api_key)

# Train demo
file_path = 'example_input_train.csv'
train_params = {
    "username": "jon_snow",
    "email": "jon.snow@targaryenwasastark.ai",
    "label": "futreturn",
    "timeseries": "yes",
    "type": "classification",
    "feature_selection": "shap",
    "analysis": "small",
    "boost": "gbdt",
    "mode": "train",
    "testsize": "0.2",
    "weights": "no",
    "prob_calib": "no",
    "suffix": "myfirstsuffix",
    "eda": "no",
}

response = client.train(file_path, train_params)
print(response)
print(response.feature_importance) 

# Predict demo
file_path = 'example_input_live.csv'
predict_params = {
    "username": "jon_snow",
    "model_name": "saved_model_myfirstsuffix.pkl",  
    "eda": "no",
}
response = client.predict(file_path, params=predict_params)
print(response)

# Save Result demo
output_path = "C:/Users/<your_machine_name>/Documents" # if not defined, it will be on project root
response = client.save_to_output({"username": "jon_snow"}, output_path)
print(response)```

