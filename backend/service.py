# python -m flask --debug --app service run (works also in PowerShell)

import datetime
import os
import pickle
from pathlib import Path

import pandas as pd
from azure.storage.blob import BlobServiceClient
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS

# init app, load model from storage
print("*** Init and load model ***")
if 'AZURE_STORAGE_CONNECTION_STRING' in os.environ:
    azureStorageConnectionString = os.environ['AZURE_STORAGE_CONNECTION_STRING']
    blob_service_client = BlobServiceClient.from_connection_string(azureStorageConnectionString)

    print("fetching blob containers...")
    containers = blob_service_client.list_containers(include_metadata=True)
    for container in containers:
        existingContainerName = container['name']
        print("checking container " + existingContainerName)
        if existingContainerName.startswith("mj-stats-model"):
            parts = existingContainerName.split("-")
            print(parts)
            suffix = 1
            if (len(parts) == 4):
                newSuffix = int(parts[-1])
                if (newSuffix > suffix):
                    suffix = newSuffix

    container_client = blob_service_client.get_container_client("mj-stats-model-" + str(suffix))
    blob_list = container_client.list_blobs()
    for blob in blob_list:
        print("\t" + blob.name)

    # Download the blob to a local file
    Path("../model").mkdir(parents=True, exist_ok=True)
    download_file_path = os.path.join("../model", "basketball_game_outcome_predictor.pkl")
    print("\nDownloading blob to \n\t" + download_file_path)

    with open(file=download_file_path, mode="wb") as download_file:
         download_file.write(container_client.download_blob(blob.name).readall())

else:
    print("CANNOT ACCESS AZURE BLOB STORAGE - Please set connection string as env variable")
    print(os.environ)
    print("AZURE_STORAGE_CONNECTION_STRING not set")    

file_path = Path(".", "../model/", "basketball_game_outcome_predictor.pkl")
with open(file_path, 'rb') as fid:
    model = pickle.load(fid)


print("*** Init Flask App ***")
app = Flask(__name__, static_url_path='/', static_folder='../frontend/dist')
cors = CORS(app)

@app.route("/")
def indexPage():
     return send_file("../frontend/dist/index.html")

@app.route("/api/predict")
def predict():
    mj_career_game = request.args.get('mj_career_game', default = 0, type = int)
    team_game_this_season = request.args.get('team_game_this_season', default = 0, type = int)
    minutes_played = request.args.get('minutes_played', default = 0, type = int)
    field_goal_made = request.args.get('field_goal_made', default = 0, type = int)
    three_pointers = request.args.get('three_pointers_made', default = 0, type = int)
    free_throws = request.args.get('free_throws_made', default = 0, type = int)
    total_rebounds = request.args.get('total_rebounds', default = 0, type = int)
    assists = request.args.get('assists', default = 0, type = int)
    steals = request.args.get('steals', default = 0, type = int)
    blocks = request.args.get('blocks', default = 0, type = int)
    personal_fouls = request.args.get('personal_fouls', default = 0, type = int)
    points = request.args.get('points', default = 0, type = int)

    demoinput = [[mj_career_game, team_game_this_season, minutes_played, field_goal_made, three_pointers, free_throws,
                  total_rebounds, assists, steals, blocks, personal_fouls, points]]
    demodf = pd.DataFrame(columns=['MJ career game', 'Team game this season', 'Minutes played', 'Field goal made', '3-Pointers made',
                                   'Free throws made', 'Total rebounds', 'Assists', 'Steals', 'Blocks', 'Personal fouls', 'Points'], data=demoinput)
    print("demodf:" + str(demodf))
    demooutput = model.predict(demodf)
    print("demooutput:" + str(demooutput[0]))
    outcome = demooutput[0]

    return jsonify({
        'prediction': str(outcome)
        })