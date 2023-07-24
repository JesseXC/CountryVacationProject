from serpapi import GoogleSearch
import os, json
country = "United States"

def getImages(query,number):
    params = {
    "engine": "google",
    "q":f'{query}',
    "tbm": "isch",
    "ijn":0,
    "api_key": 'b3c3b18e40505a9d6a63833895869fcd35fa42ba5201015466ee7ca64a6487b6'
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

