from django.shortcuts import render, redirect
import requests
from django.http import JsonResponse
from recommendations.models import Recommendation

# Create your views here.


TRIPPINGO_URL="http://localhost:8001"
APIKEY = 'AIzaSyAgU9a5eTrwZP9pIb0eNuNRu3iPE75tR-8'


def recommendations(request):

	print("Entered recommendations")
	recs=trippingoRecommendations(request)
	context = {
		"recs":recs,
		"selectedRecs":[rec for rec in recs if rec.selected],
		"pk":"123"
	}
	return render(request, 'recommendations.html', context)


def recommendations_pk(request, pk):
	print("Entered recommendations_pk")
	recs=trippingoRecommendations(request)
	context = {
		"recs":recs,
		"selectedRecs":[rec for rec in recs if rec.selected],
		"pk":pk
	}
	return render(request, 'recommendations.html', context)


def selectedAttractions(request,pk):

	print("Entered selectedAttractions")
	selected_attractions = [int(key) for key, value in request.POST.dict().items() if value == 'on']
	print(selected_attractions)
	saveSelectedAttractions(1, selected_attractions)
	return redirect('../{pk}/planning'.format(pk=pk))

def planning(request, pk):
	print("Entered planning")
	return render(request, 'planning.html', {"pk":pk})


def itinerary(request,pk):
	print("Entered itinerary")
	itinerary_resp = plan_itinerary(pk)
	return JsonResponse(dict(itinerary_resp.json()))


def trippingoRecommendations(req):
	keywords = 'Landmark'
	travellerType = 'Family'
	url = TRIPPINGO_URL + "/recommendations?keywords={keywords}&travellerType={travellerType}&count=3".format(
	    keywords=keywords, travellerType=travellerType);
	print(url)
	api_response = getjson(url)
	recommendations = [mapToModel(rec) for rec in api_response]
	return recommendations


def saveSelectedAttractions(travel_plan_id, selected_attractions):
	url = TRIPPINGO_URL + "/travelPlans/{id}/selectedAttractions".format(id=travel_plan_id);
	print(url)
	data = {"attractionIds":selected_attractions}
	print(data)
	resp = requests.put(url, json=data)
	print(resp.text)


def plan_itinerary(travel_plan_id):
	url = TRIPPINGO_URL + "/travelPlans/{id}/itinerary".format(id=travel_plan_id);
	print(url)
	data = {}
	resp = requests.put(url, json=data)
	print(data)
	return resp


def mapToModel(rec):
	description = rec['description'][:150] + "..."
	name = rec['name']
	return Recommendation(rec['id'], name, description, getPhoto(name))



def getjson(url):
    resp = requests.get(url)
    return resp.json()


def getPhoto(attrname):
 	API_ENDPOINT = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={attrname}&inputtype=textquery&fields=photos&key={APIKEY}".format(attrname=attrname, APIKEY=APIKEY)
 	info = getjson(API_ENDPOINT)
 	photo_ref = info['candidates'][0]['photos'][0]['photo_reference']
 	photo_url = "https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo_ref}&key={APIKEY}".format(photo_ref=photo_ref, APIKEY=APIKEY)
 	return photo_url

def associatedAttractions(request):

	print("Entered associatedAttractions")
	recs=trippingoRecommendations(request)
	context = {
		"recs":recs,
		"selectedRecs":[rec for rec in recs if rec.selected],
		"pk":"123"
	}
	return render(request, 'recommendations.html', context)