from fastapi import FastAPI
import json
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import city_data
from fastapi.responses import FileResponse

import requests
import uvicorn

import os
import openai
from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
# run python "$python main.py" & "$node index.js" at the same time for results








    
def main():
    cities_to_desc = {}
    flights = []

    url = 'https://ef75-144-9-80-252.ngrok.io/flights?date=2020-01-01'
    print("Hello World!")
    # data = requests.request("GET", url)
    # print(data.text)

    def user_pref_matcher(user_pref,city_data):
        # loops through the data of possible cities and creates a list of possible cities the customer may like, then iterates through that list deleting entries as they stop matching
        poss_cities = {}
        for key in user_pref:
            for city in city_data:
                if user_pref[key] == bool:
                    if user_pref[key] == city[key]:
                        poss_cities += city
                # elif user_pref[key] == list:
                #     if user_pref[key] == city[key]
            for city in poss_cities:
                    if user_pref[key] != poss_cities[key]:
                        del poss_cities[city]

            


    def city_image(city):
        # generates an image for front end use using openAI
        response = openai.Image.create(
        prompt= f"Provide a scenic image of {city} that can be advertised for airlines.",
        n=1,
        size="1024x1024" 
        )
        return response



    def city_description(City,User_pref):
        # generates a tailored description of the city to visit using the user's preferences and openAI to generate the description

        completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are acting as a travel assitant, skilled in selling a destination to a customer."},
            {"role": "user", "content": f"Provide a description of {City} based on {User_pref}. Only output a short 3 sentence pitch, selling the customer the destination, referencing some of their preferneces in the pitch."}
        ]
        )


        return completion.choices[0].message
    
    # print(city_description("dallas", {"hot": True,"cold": True,"humid": False,"dry": True,"best_time_of_year_to_visit": [False, True, False, False],"Dairy": True,"Gluten": True,"Shellfish": True,"Nuts": False,"halaal": False,"Walkable": True,"region": [False, False, False, False, False, False, False],"kid friendly": True,"nightlife": True,}))

    def trip_planner(city,user_pref):
# plans the user a trip using the data available to openAI, using the preferences of the user as a basis for the suggestions.
        completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are acting as a travel assitant, looking to utilize user preferenecs to come up with a trip that matches them."},
            {"role": "user", "content": f"Provide a 3 event itenerary of things to do in {City} based on {User_pref}. Give up to 5 things for the customer to do and make sure they fit the preferences."}
        ]
        )


        return completion.choices[0].message

    


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_root():
    return {"Hello": "World"}

class Data(BaseModel):
    data: dict

@app.post("/test")
async def read_item(data:Data):
    user = 'test'
    # user = data.user
    # make reques
    f = open(user + ".txt", "w")
    f.write(json.dumps(data.data))
    f.close()
    return data



if __name__ == '__main__':
    print(city_description("dallas", {"hot": True,"cold": True,"humid": False,"dry": True,"best_time_of_year_to_visit": [False, True, False, False],"Dairy": True,"Gluten": True,"Shellfish": True,"Nuts": False,"halaal": False,"Walkable": True,"region": [False, False, False, False, False, False, False],"kid friendly": True,"nightlife": True,}))
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)