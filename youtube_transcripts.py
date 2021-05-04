import os
import re
from youtubesearchpython import VideosSearch
from youtube_transcript_api import YouTubeTranscriptApi

PATH = os.getcwd() + "\\collection"
#returns a list dict w/ 1 key that holds a list of dictionaries for each entry

def format_results(result, addon = "", parent = None):
    num_results = len(result.result()["result"])
    res = result.result()["result"]
    results = {}
    for i in range(num_results):
        title = res[i]["title"].lower()
        title = re.sub('[^A-Za-z0-9]+','_',title)
        results[title] = {}
        results[title]["author"] = res[i]["channel"]["name"]
        results[title]["id"] = res[i]["id"]
        results[title]["link"] = res[i]["link"]
    return results

def create_transcripts(results, parent = None):
    titles = list(results.keys())
    total = 0
    for i in range(len(titles)):
        try:
            trans = YouTubeTranscriptApi.get_transcript(results[titles[i]]["id"])
            file = open(f"{PATH}\\{titles[i]}.txt","w")
            for j in range(len(trans)):
                file.write(f"{trans[j]['text']}\n")
            file.close()
            if parent:
                parent.update_console(f"Aquired Transcript for: {titles[i]}")
            total += 1
        except:
            print(i)
            if parent:
                parent.update_console(f"Could not get video transcript for: {titles[i]}", color = "red")
    return total
