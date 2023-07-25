from serpapi import GoogleSearch
import os, json
country = "United States"

def getImages(query,number):
    params = {
    "engine": "google",
    "q":f'{query}',
    "tbm": "isch",
    "ijn":0,
    "api_key": 'e6eb1309e3554bf989498272bdb3ccdcb3bd0c613d93608c447c0323217d4025'
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

