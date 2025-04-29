from typing import Text, Dict, Any, List
import requests
import random

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

class NetworkAction(Action):

    def name(self) -> Text:
        return "send_network_request"

    def run(self,
           dispatcher: CollectingDispatcher,
           tracker: Tracker,
           domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        user_message = tracker.latest_message['text']
        ITM_url = "https://69eb-35-247-167-103.ngrok-free.app/ask"
        payload = {"question": f"{user_message}"}
        policyresponse = requests.post(ITM_url, json=payload)
        policy = policyresponse.text.strip('"')

        opa_check_url = "http://fyp-opa-1:8181/v1/polices/" + str(random.randint(1000, 9999))
        response = requests.put(url=opa_check_url, data=policy, timeout=5)

        if response.status_code == 200:
            opa_result = response.json()
            allowed = opa_result.get("result", {}).get("allow", False)

            if allowed:
                dispatcher.utter_message(text=f"Rule validation successful: ")
            else:
                dispatcher.utter_message(text=f"Rule validation failed: ")
        else:
            dispatcher.utter_message(text=f"Failed with response code: {response.status_code} and message: {response.json()}")
        return []

class ActionSayHello(Action):
    def name(self) -> str:
        return "action_say_hello"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: dict) -> list:
        dispatcher.utter_message(text="Hello! How can I help you?")
        return []

class ActionGetPolicies(Action):
   def name(self) -> Text:
      return "action_get_policies"

   def run(self,
           dispatcher: CollectingDispatcher,
           tracker: Tracker,
           domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        opa_check_url = "http://fyp-opa-1:8181/v1/policies/"

        response = requests.get(opa_check_url)
        id_value = response.json().get("result", [{}])[0].get("id", "ID not found")
        id_list = [policy.get("id", "ID not found") for policy in response.json().get("result", [])]
        print(id_list)  # Outputs: ['testPolicy', 'testPolicy2']

        dispatcher.utter_message(id_value)
        return []