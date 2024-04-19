import ast
import json
import os
import pprint
import urllib
from typing import Dict, List, Any

import geopy
import requests
from geopy.extra.rate_limiter import RateLimiter
from geopy.geocoders import Nominatim
from langchain.tools import BaseTool

RADIUS = 100000
FSQ_PLACE_SEARCH_URL = "https://api.foursquare.com/v3/places/search"
FSQ_PLACE_INFO_URL = "https://api.foursquare.com/v3/places/{}/tips"

ROUTE_URL = "http://dev.virtualearth.net/REST/V1/Routes/{}?"


class PlacesOfInterestTool(BaseTool):
    """
    Tool for discovering places of interest near any given location. This tool retrieves details about attractions,
    restaurants, and more based on the specified area. Only one area should be provided at a time.

    Attributes:
        name (str): The name of the tool.
        description (str): The description of the tool.
    """
    name = "Places Of Interest Retriever"
    description = "Discover places of interest near any location (city, town or locality) with this tool. " \
                  "Important: Use it to get places of interest in the specified area, do not use it for fetching " \
                  "information of that area (for example history of that area or its religious/spiritual " \
                  "importance etc). Provide only one area at a time. The location has to be granular " \
                  "like city or town or locality and not as broad as a district or country. The tool takes a single " \
                  "input parameter, 'location', which is a string representing the name or address of " \
                  "the area to search for places of interest. The string must not contain anything else " \
                  "but the location."

    def _run(self, location: str) -> Dict[str, str]:
        """Synchronously runs the tool with the given location.

        Args:
            location (str): location provided by the agent

        Returns:
            output (dict): Places of interest around the given location and their descriptions
        """
        location_data = get_location_data(location)
        places_of_interest = get_places_of_interests(location_data.latitude, location_data.longitude, RADIUS)
        output = {"output": places_of_interest}
        return output

    def _arun(self, location: str):
        """Asynchronous method is not implemented.

        Args:
            location (str): location provided by the agent
        """
        raise NotImplementedError("This tool does not support async")


def get_places_of_interests(latitude: float, longitude: float, radius: int) -> str:
    """Retrieves places of interest in the vicinity of the specified latitude and longitude.

    Args:
        latitude (float): latitude of the given location
        longitude (float): longitude of the given location
        radius (int): radius of search

    Returns:
        places_description (list(str)): list of strings describing each of the places of interest
    """
    try:
        fsq_api_key = os.environ.get('FSQ_API_KEY', None)
        if fsq_api_key is None:
            raise ValueError("API KEY for FSQ must be set")

        url = FSQ_PLACE_SEARCH_URL
        headers = {
            "accept": "application/json",
            "Authorization": fsq_api_key
        }
        params = {"ll": f"{latitude},{longitude}",
                  "radius": radius,
                  "sort": "RELEVANCE",
                  "limit": 10
                  }
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            raise Exception("Failed to fetch places of interest.")
        places = response.json()['results']
        places_description = '\n'.join(get_fsq_info_of_location(place['name'], place['fsq_id']) for place in places)
        return places_description
    except Exception as e:
        print(f"An error occurred: {e}")


def get_location_data(location: str) -> geopy.location.Location:
    """Geocodes the location using Nominatim service.

    Args:
        location (str): location given by the agent

    Returns: location_details (geopy.location.Location): location details like latitude, longitude etc., provided by
    geopy geocode
    """
    if location.startswith("location="):
        location = location[len("location="):]
        location = location.strip()
    geolocator = Nominatim(user_agent="places_of_interest_finder")
    geocoding_rate_limiter = RateLimiter(geolocator.geocode, min_delay_seconds=1)

    try:
        location_details = geocoding_rate_limiter(location)
        if location_details:
            return location_details
        else:
            raise Exception("Location not found. Please refine your query.")
    except Exception as exc:
        print(f"An error occurred while fetching location data: {exc}")
        raise


def get_fsq_info_of_location(name: str, fsq_id: str) -> str:
    """Fetches additional information for a location identified by Foursquare ID.

    Args:
        name (str): Name of the place of interest
        fsq_id (str): FSQ ID of the location

    Returns:
        description (str): short descriptions of the location
    """
    try:
        url = FSQ_PLACE_INFO_URL.format(fsq_id)
        fsq_api_key = os.environ.get('FSQ_API_KEY', None)
        if fsq_api_key is None:
            raise ValueError("API KEY for FSQ must be set")
        headers = {
            "accept": "application/json",
            "Authorization": fsq_api_key
        }
        params = {"sort": "POPULAR", "limit": 2}
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            raise Exception("Failed to fetch location's additional info.")
        tips = response.json()
        description = name + ': ' + ' '.join(tip['text'] for tip in tips)
        return description
    except Exception as e:
        print(f"An error occurred: {e}")


class RouteRetriever(BaseTool):
    name = "Route Retriever"
    description = (
        "use this tool routes for given locations and mode of transport. The tool takes one input parameter, "
        "'input_data', which is a dictionary and must contain two keys 'locations' and 'transport_mode'"
        " the value 'locations' is a list of strings each representing the name or address of the location, "
        "indicating starting point, intermediate stops and endpoint of the travel, "
        "and value of 'transportation_mode' is a string that indicates the mode of transport "
        "(can be cycle, walking, transit or car). "
        "Example: {'locations': ['Mumbai', 'Pune', 'Nagpur'], 'transportation_mode': 'cycle'}"
        "The response is instructions through different waypoints, do not change the response."
    )

    def _run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        if isinstance(input_data, str):
            input_data = ast.literal_eval(input_data)
        mode = self.detect_transportation_mode(input_data.get('transportation_mode', 'car'))
        locations = input_data.get('locations', [''])
        route = get_route(locations, mode)
        return route

    def _arun(self, locations: List[str], transportation_mode: str) -> None:
        raise NotImplementedError("This tool does not support asynchronous operations.")

    @staticmethod
    def detect_transportation_mode(transportation_mode: str) -> str:
        transportation_mode = transportation_mode.lower()
        transportation_mode.strip()
        if 'foot' in transportation_mode or 'walk' in transportation_mode:
            return 'Walking'
        if 'cycle' in transportation_mode:
            return 'bicycle'
        if 'public' in transportation_mode or 'bus' in transportation_mode or 'train' in transportation_mode or \
                'transit' in transportation_mode:
            return 'Transit'
        return 'Driving'


def get_route(locations: List[str], mode: str) -> Dict[str, Any]:
    bing_maps_key = os.getenv('BING_API_KEY')
    if not bing_maps_key:
        raise ValueError("Bing API key must be set in environment variables.")
    route_url = ROUTE_URL
    route_url = route_url.format(mode)
    for i, loc in enumerate(locations):
        encoded_location = urllib.parse.quote(loc, safe='')
        if i == 0:
            route_url += f"wp.{i}=" + encoded_location
        else:
            route_url += f"&wp.{i}=" + encoded_location

    route_url += "&key=" + bing_maps_key
    print(route_url)
    try:
        request = urllib.request.Request(route_url)
        response = urllib.request.urlopen(request)

        r = response.read().decode(encoding="utf-8")
        print(r)
        result = json.loads(r)
        itinerary_items = result["resourceSets"][0]["resources"][0]["routeLegs"][0]["itineraryItems"]
        directions = []
        geocode_points = []
        pprint.pprint(itinerary_items)
        for item in itinerary_items:
            directions.append('- '+item["instruction"]["text"])
            geocode_points.append(item["maneuverPoint"]["coordinates"])
        route = {"output": '\n'.join(directions), 'geocode_points': geocode_points}
        return route
    except Exception as e:
        raise ConnectionError(f"An issue occurred while retrieving the route: {e}")
