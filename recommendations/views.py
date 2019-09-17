from django.shortcuts import render, redirect
import requests
from django.http import JsonResponse
from recommendations.models import Recommendation
from itertools import combinations

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
	recs,association_recs=associationRecommendations(request,pk)
	context = {
		"recs":recs,
		"selectedRecs":[rec for rec in recs if rec.selected],
		"associatedRecs":association_recs,
		"pk":pk
	}
	print(context['selectedRecs'])
	return render(request, 'recommendations.html', context)


def selectedAttractions(request,pk):

	print("----------Entered selectedAttractions")
	print(request)
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

def associationRecommendations(req,pk):
	recommendations = trippingoRecommendations(req)
	rec_list = []
	association_recs = []
	allcom_list = []
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
				print(a)
				if a["name"] not in rec_list and mapToModel(a) not in association_recs:
					association_recs.append(mapToModel(a))
					# break
	print('association_recs',association_recs)
	return recommendations, association_recs



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




