from serpapi import GoogleSearch
import os, json
country = "United States"

def getImages(query,number):
    params = {
    "engine": "google",
    "q":f'{query}',
    "tbm": "isch",
    "ijn":0,
    "api_key": '3fe231506a5f1da132bb9c02f90787f5bba231499b81839fe8b4bef385b78efe'
    }
    search = GoogleSearch(params)
    image_results = []
    images_is_present = True
    count = 0
    while images_is_present and count < number:
        results = search.get_dict()
        if "error" not in results:
            while count < number:
                for image in results["images_results"]:
                    if count == number:
                        break
                    if image["original"] not in image_results:
                        image_results.append(image["original"])
                        count += 1
        else:
            images_is_present = False
            print(results["error"])
    return json.dumps(image_results)

