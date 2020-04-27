from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from typing import Text, Dict, Any, List
import requests

WIKI_API="https://photoshop.fandom.com/api/v1"
def query(intent, key_word):
    url = "{}/Search/List?query={}&limit=25&minArticleQuality=10&batch=1&namespaces=0%2C14".format(WIKI_API, key_word)
    res = requests.get(url)
    if res.status_code != 200:
        return "Failed to search keyword '{}'".format(key_word)
    result = res.json()
    if result['total'] == 0:
        return "Empty result with keyword '{}'".format(key_word)
    first_result = result['items'][0]
    if first_result['title'].lower().find('key_word') == -1:
        return "Not found"
    article_id = first_result['id']

    url = "{}/Articles/AsSimpleJson?id={}".format(WIKI_API, article_id)
    res = requests.get(url)
    if res.status_code != 200:
        return "Failed to get article '{}'".format(article_id)
    result = res.json()
    return result['sections'][0]['content'][0]['text']

class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_ask_object"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text=query("AAA", tracker.get_slot("object_1")))
        dispatcher.utter_message(text="{}".format(tracker.get_slot("object_1")))

        return []
