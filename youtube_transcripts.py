import os
from youtubesearchpython import VideosSearch
from youtube_transcript_api import YouTubeTranscriptApi

PATH = os.getcwd() + "\\collection"

#returns a list dict w/ 1 key that holds a list of dictionaries for each entry

def format_results(result, addon = ""):
    num_results = len(result.result()["result"])
    res = result.result()["result"]
    results = {}
    for i in range(num_results):
        # title = res[i]["title"].lower()
        # title = title.replace(" ", "_")
        # title = title.replace("!", "")
        # title = title.replace("*", "")
        # title = title.replace("?", "")
        title = addon+str(i)
        results[title] = {}
        #results[title]["author"] = res[i]["channel"]["name"]
        results[title]["id"] = res[i]["id"]
        #results[title]["link"] = res[i]["link"]   
    return results



    



def create_transcripts(results):
    titles = list(results.keys())
    for i in range(len(titles)):
        try:
            trans = YouTubeTranscriptApi.get_transcript(results[titles[i]]["id"])
            file = open(f"{PATH}\\{titles[i]}.txt","w")
            for i in range(len(trans)):
                file.write(trans[i]["text"])
            file.close()
        except:
            print("couldn't get video transcript")


query = "transformers prime"
vs = VideosSearch(query,10)
res = format_results(vs,query)
create_transcripts(res)

