import re
import requests
import urllib


class MovieDatabase:
    def __init__(self, api_key):
        self.base_uri = "https://api.themoviedb.org/3/"
        self.api_key = api_key

    @classmethod
    def get_api_key(cls):
        return cls(input("api_key from TMDB: "))

    def search(self):
        query = input("Enter name of the series: ")
        payload = {"api_key": self.api_key, "query": query, "include_adult": True}
        params = urllib.parse.urlencode(payload, quote_via=urllib.parse.quote)
        r = requests.get(self.base_uri + "search/tv/", params=params)
        self.choose_series(r.json())

    def choose_series(self, series):
        counter = series["total_results"]
        series_list = series["results"]

        if counter:
            for i in range(20 if counter > 20 else counter):
                print(
                    str(i) + ".",
                    series_list[i]["first_air_date"],
                    "-",
                    series_list[i]["original_name"],
                )
            series_choice = int(input("Enter number matching prefered TV show: "))
            series_id = series_list[series_choice]["id"]
            self.list_episodes(series_id)
        else:
            print("Can't find anything for your query.")
            self.search()

    def replace_illegal(self, s):
        illegal = ["\\", "/", ":", "*", '"', "<", ">", "|", "?"]
        for i in illegal:
            s = s.replace(i, "")
        return s

    def list_episodes(self, series_id):
        season = int(input("Enter season number: "))
        params = urllib.parse.urlencode({"api_key": self.api_key})
        r_json = requests.get(
            self.base_uri + "tv/" + str(series_id) + "/season/" + str(season),
            params=params,
        ).json()
        episodes_list_raw = r_json["episodes"]
        self.episodes = [
            "{0}. {1}".format(
                episodes_list_raw[i]["episode_number"],
                self.replace_illegal(episodes_list_raw[i]["name"]),
            )
            for i in range(0, len(episodes_list_raw))
        ]
