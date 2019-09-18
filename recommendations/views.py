from django.shortcuts import render, redirect
import requests
import time
import json
from django.http import JsonResponse
from recommendations.models import Recommendation
from itertools import combinations

# Create your views here.


TRIPPINGO_URL="http://localhost:8001"
APIKEY = 'AIzaSyAgU9a5eTrwZP9pIb0eNuNRu3iPE75tR-8'


def recommendations(request):

    print("Entered recommendations")
    recs=trippingoRecommendations(request,1)
    context = {
        "recs":recs,
        "selectedRecs":[rec for rec in recs if rec.selected],
        "pk":"123"
    }
    return render(request, 'recommendations.html', context)


def recommendations_pk(request, pk):
    print("Entered recommendations_pk")
    recs,association_recs=associationRecommendations(request,pk)
    context = {
        "recs":recs,
        "selectedRecs":[rec for rec in recs if rec.selected],
        "associatedRecs":association_recs,
        "pk":pk
    }
    #print(context['selectedRecs'])
    return render(request, 'recommendations.html', context)


def selectedAttractions(request,pk):

    print("----------Entered selectedAttractions")
    #print(request)
    selected_attractions = [int(key) for key, value in request.POST.dict().items() if value == 'on']
    #print(selected_attractions)
    saveSelectedAttractions(pk, selected_attractions)
    return redirect('../{pk}/planning'.format(pk=pk))

def planning(request, pk):
    print("Entered planning")
    return render(request, 'planning.html', {"pk":pk})


def itinerary(request,pk):

    print("Entered itinerary")
    itinerary_resp = plan_itinerary(pk)
    itinerary = dict(itinerary_resp.json())
    for dayp in itinerary["dayPlans"]:
        for j in dayp["attractionVisit"]:
            daytime = time.strptime(j["timeofDay"], "%H:%M:%S")
            j["timeofDay"] = str(daytime.tm_hour)+":"+str(daytime.tm_min)

    plan_url = TRIPPINGO_URL + "/travelPlans/{id}".format(id=pk)
    plan_info = getjson(plan_url)
    hotel = plan_info["hotelLocation"]
    #url = TRIPPINGO_URL + "/travelPlans/{pk}".format(pk)
    map_label= ["" for _ in range(len(itinerary['dayPlans']))]
    API_KEY = 'AIzaSyCZ4Q24NuUFkO3sQBdtcwNxSnO3qwZqwW8'

    attrList = [0 for _ in range(len(itinerary['dayPlans']))]

    travelPlanCoordinates = [0 for _ in range(len(itinerary['dayPlans']))]  # travelPlanCoordinates list with geometry of attractions(the jth attraction of i day)
    centerGeometry = [0 for _ in range(len(itinerary['dayPlans']))]  # #record average Geometry (centre point) of each day
    timeofDays = [0 for _ in range(len(itinerary['dayPlans']))]  ##record visit time of all attractions
    direct = [0 for _ in range(len(itinerary['dayPlans']))]
    attrLatList = [0 for _ in range(len(itinerary['dayPlans']))]
    attrLngList = [0 for _ in range(len(itinerary['dayPlans']))]
    q = 0

    for i in range(len(itinerary['dayPlans'])):  # for i in numverofDays
        lat_sum = 0  # record the sum of attractions latitude per day
        lng_sum = 0  # record the sum of attractions lagnitude per day
        q = i+1

        if hotel:
            allName = [0 for _ in range(len(itinerary['dayPlans'][i]['attractionVisit']) + 2)]
            direc_url = [0 for _ in range(len(itinerary['dayPlans'][i]['attractionVisit'])+2)]
            direct_url = [0 for _ in range(len(itinerary['dayPlans'][i]['attractionVisit']) + 2)]
            attrGeometry = [0 for _ in range(len(itinerary['dayPlans'][i]['attractionVisit'])+2)]  # record geometry of each attraction
            timeperDay = [_ for _ in range(len(itinerary['dayPlans'][i]['attractionVisit'])+2)]  # record visit time of each attraction
            attrLat = [_ for _ in range(len(itinerary['dayPlans'][i]['attractionVisit'])+2)]
            attrLng = [_ for _ in range(len(itinerary['dayPlans'][i]['attractionVisit'])+2)]
            allName[0]=hotel
            allName[len(itinerary['dayPlans'][i]['attractionVisit']) + 1] = hotel
            map_label[i]="1"
            for j in range(len(itinerary['dayPlans'][i]['attractionVisit'])):
                q=j+2
                map_label[i] = map_label[i]+str(q)
                allName[j+1] = itinerary['dayPlans'][i]['attractionVisit'][j]['attraction']['name']
            map_label[i] = map_label[i]+"1"
            print(map_label[i])
        else:
            allName = [0 for _ in range(len(itinerary['dayPlans'][i]['attractionVisit']))]
            direc_url = [0 for _ in range(len(itinerary['dayPlans'][i]['attractionVisit']))]
            direct_url = [0 for _ in range(len(itinerary['dayPlans'][i]['attractionVisit']))]
            attrGeometry = [0 for _ in range(len(itinerary['dayPlans'][i]['attractionVisit']))]  # record geometry of each attraction
            timeperDay = [_ for _ in range(len(itinerary['dayPlans'][i]['attractionVisit']))]  # record visit time of each attraction
            attrLat = [_ for _ in range(len(itinerary['dayPlans'][i]['attractionVisit']))]
            attrLng = [_ for _ in range(len(itinerary['dayPlans'][i]['attractionVisit']))]
            for j in range(len(itinerary['dayPlans'][i]['attractionVisit'])):
                map_label[i] = map_label[i]+str(j+1)
                allName[j] = itinerary['dayPlans'][i]['attractionVisit'][j]['attraction']['name']
            print(map_label[i])

        for j in range(len(allName)):  # for j in numverofAttracttions per day
            if hotel=='' and j == 0:
                lastAttr = ''
            elif j==0:
                lastAttr = hotel
            else:
                lastAttr = allName[j-1]

            API_ENDPOINT = f"https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={allName[j]}&inputtype=textquery&fields=geometry&key={API_KEY}"
            attrlocation = getjson(API_ENDPOINT)
            attrGeometry[j] = attrlocation['candidates'][0]['geometry']['location']
            attrLat[j] = attrGeometry[j]['lat']
            attrLng[j] = attrGeometry[j]['lng']
            lat_sum = lat_sum + attrGeometry[j]['lat']
            lng_sum = lng_sum + attrGeometry[j]['lng']
            if hotel:
                if j>0 and j< (len(allName)-1):
                    timeperDay[j] = itinerary['dayPlans'][i]['attractionVisit'][j-1]['timeofDay']
            else:
                timeperDay[j] = itinerary['dayPlans'][i]['attractionVisit'][j]['timeofDay']

            direc_url[j] = f"https://www.google.com/maps/dir/?api=1&origin={lastAttr}&destination={allName[j]} Singapore&travelmode=transit"
            direct_url[j] = direc_url[j].replace(" ","")

        travelPlanCoordinates[i] = attrGeometry
        attrList[i] = allName
        attrLatList[i] = attrLat
        attrLngList[i] = attrLng
        centerGeometry[i] = [lat_sum / len(allName),
                             lng_sum / len(allName)]
        print(centerGeometry[i])
        timeofDays[i] = timeperDay
        direct[i] = direct_url

    context = {
        "dayPlans": itinerary["dayPlans"],
        "pk": pk,
        "travelPlanCoordinates":travelPlanCoordinates,
        "attrLatList":attrLatList,
        "attrLngList":attrLngList,
        "timeofDays":timeofDays,
        "centerGeometry":centerGeometry,
        "direct":direct,
        "attrList":attrList,
        "map_label":map_label
    }
    return render(request, 'itinerary.html', context)





def trippingoRecommendations(req,pk):
    keywords = 'Landmark'
    travellerType = 'Family'
    url = TRIPPINGO_URL + "/travelPlans/{id}/recommendations?count=10".format(id=pk);
    print(url)
    api_response = getjson(url)
    recommendations = [mapToModel(rec) for rec in api_response]

    return recommendations

def associationRecommendations(req,pk):
    recommendations = trippingoRecommendations(req,pk)
    rec_list = []
    association_recs = []
    allcom_list = []
    duplicate_check = []
    # getting names of recommended attractions
    for rec in recommendations:
        rec_list.append(rec.name)
    # getting all possible combinations of recommended attractions
    for i in range(len(rec_list)):
        temp = []
        for j in combinations(rec_list,i):
            temp.append(j)
        allcom_list.extend(temp)
    for arec in allcom_list:
        if len(association_recs)<4:
            if len(arec) == 1:
                association_url = TRIPPINGO_URL + "/travelPlans/{id}/associatedAttractions?attractions={attr_names}".format(
                    id=pk, attr_names=arec[0]);
            elif len(arec) > 1:
                association_url = TRIPPINGO_URL + "/travelPlans/{id}/associatedAttractions?attractions={attr_names}".format(
                    id=pk, attr_names=','.join(arec));
            else:
                continue
            association_api_response = getjson(association_url)
            if len(association_api_response) != 0:
                for a in association_api_response:
                    # print(a)

                    if a["name"] not in rec_list and a["name"] not in duplicate_check:
                        print(a["name"])
                        duplicate_check.append(a["name"])
                        association_recs.append(mapToModel(a))
                        print(duplicate_check)
                    # break
        else:
            return recommendations, association_recs
    print('association_recs',association_recs)
    return recommendations, association_recs



def saveSelectedAttractions(travel_plan_id, selected_attractions):
    url = TRIPPINGO_URL + "/travelPlans/{id}/selectedAttractions".format(id=travel_plan_id);
    #print(url)
    data = {"attractionIds":selected_attractions}
    #print(data)
    resp = requests.put(url, json=data)
    #print(resp.text)


def plan_itinerary(travel_plan_id):
    url = TRIPPINGO_URL + "/travelPlans/{id}/itinerary".format(id=travel_plan_id);
    print(url)
    data = {}
    resp = requests.put(url, json=data)
    #print(data)
    return resp


def mapToModel(rec):
    description = rec['description'][:150] + "..."
    name = rec['name']
    return Recommendation(rec['id'], name, description, getPhoto(name))



def getjson(url):
    resp = requests.get(url)
    return resp.json()


def getPhoto(attrname):
    try:
        API_ENDPOINT = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={attrname}&inputtype=textquery&fields=photos&key={APIKEY}".format(attrname=attrname, APIKEY=APIKEY)
        info = getjson(API_ENDPOINT)
        photo_ref = info['candidates'][0]['photos'][0]['photo_reference']
        photo_url = "https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo_ref}&key={APIKEY}".format(photo_ref=photo_ref, APIKEY=APIKEY)
    except Exception as e:
        return getPhoto('Singapore Flyer')
    return photo_url

