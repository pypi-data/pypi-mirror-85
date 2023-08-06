# -*- coding: utf-8 -*-
"""Pathable class file."""

import requests


class Pathable(object):
    """Example class."""

    def __init__(self, api_key):
        """Initialize an Example class instance."""
        self.base_url = "https://api.pathable.co/v1"
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-API-KEY": api_key,
        }

    def get(self, path, params={}):
        """Return a response to a get request."""
        url = f"{self.base_url}/{path}"
        response = requests.get(url, headers=self.headers, params=params).json()
        results = response["data"]
        total = response.get("total")
        while len(results) < total:
            params["skip"] = len(results)
            response = requests.get(url, headers=self.headers, params=params).json()
            results.extend(response["data"])
        return results

    def get_meetings(self):
        """Return a list of meetings."""
        path = "meetings"
        params = {}
        return self.get(path, params=params)

    # people
    def create_person(self, data):
        """Create a person in Pathable API."""
        path = "people"
        url = f"{self.base_url}/{path}"
        response = requests.post(url, headers=self.headers, data=data)
        response.raise_for_status()
        return response.json()

    def get_people(self, searchBy=None):
        """Return a list of people."""
        path = "people"
        params = {
            "searchBy": searchBy,
        }
        return self.get(path, params=params)

    def get_people_dict(self, key="_id", searchBy=None):
        """Return a dict of people."""
        people = {}
        for person in self.get_people():
            k = person[key]
            people[k] = person
        return people

    def get_person_by_email(self, email):
        """Return a person by their email address."""
        path = "people"
        params = {
            "_email": email,
        }
        results = self.get(path, params=params)
        if results:
            return results[0]

    def get_profiles(self):
        """Return a list of profiles."""
        path = "people/profiles"
        params = {}
        return self.get(path, params=params)
