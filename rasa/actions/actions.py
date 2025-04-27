from typing import Text, Dict, Any, List
import requests

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

class ActionChangeRouting(Action):

    def name(self) -> Text:
        return "action_change_route"

    def run(self,
           dispatcher: CollectingDispatcher,
           tracker: Tracker,
           domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        source = tracker.get_slot("source_node")
        destination = tracker.get_slot("destination_node")

        if not source or not destination:
            dispatcher.utter_message(text="I need both source and destination nodes to check the rule. I recieved" )
            return []
        dispatcher.utter_message(TEXT = "found source and destination")

        test_input = {
            "input": {
                "action": "route_traffic",
                "source": source,
                "destination": destination
            }
        }
        
        opa_check_url = "http://fyp-opa-1:8181/v1/polices/"
        response = requests.put(url=opa_check_url, json=test_input, timeout=5)

        if response.status_code == 200:
            opa_result = response.json()
            allowed = opa_result.get("result", {}).get("allow", False)

            if allowed:
                dispatcher.utter_message(text=f"Rule validation successful: Routing from {source} to {destination} is permitted.")
            else:
                dispatcher.utter_message(text=f"Rule validation failed: Routing from {source} to {destination} is not allowed.")
        else:
            dispatcher.utter_message(text=f"Failed with response code: {response.status_code} and message: {response.reason}")
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