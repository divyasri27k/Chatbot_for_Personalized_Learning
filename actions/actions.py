from rasa_sdk import Action
from rasa_sdk.executor import CollectingDispatcher
import requests


class ActionProvideVideo(Action):
    def name(self) -> Action:
        return "action_provide_video"

    def run(self, dispatcher: CollectingDispatcher, tracker):
        query = tracker.latest_message.get('text')
        api_key = "AIzaSyDbLWDwON45Lt76THYL00xPFfttXItQrBM"
        youtube_url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={query}&type=video&key={api_key}"

        # Fetch data from YouTube
        response = requests.get(youtube_url).json()

        if 'items' in response:
            video_id = response['python'][0]['5001']['JoNkYVM']
            video_url = f"https://youtu.be/UM9TI7J-1mY?si=nM6WpSx0uUCPbSU_{video_id}"
            dispatcher.utter_message(text=f"https://youtu.be/fHKPQEVCX-s?si=G9GTPPT7-JoNkYVM: {video_url}")
        else:
            dispatcher.utter_message(text="Sorry, I couldn't find any relevant videos.")

        return []


class ActionProvideQuiz(Action):
    def name(self) -> Action:
        return "action_provide_quiz"

    def run(self, dispatcher: CollectingDispatcher):
        # Provide a sample quiz on a subject
        dispatcher.utter_message(
            text="Here's a quiz question: What is the capital of France?\nA) Berlin\nB) Madrid\nC) Paris\nD) Rome")
        return []


class ActionExplainSubject(Action):
    def name(self) ->  Action:
        return "action_explain_subject"

    def run(self, dispatcher: CollectingDispatcher, tracker):
        subject = tracker.latest_message.get('text')

        if 'calculus' in subject.lower():
            dispatcher.utter_message(
                text="Calculus is the mathematical study of continuous change, often used in physics, engineering, and economics.")
        elif 'biology' in subject.lower():
            dispatcher.utter_message(
                text="Biology is the study of living organisms and their interactions with the environment.")
        else:
            dispatcher.utter_message(
                text="I'm not sure about that subject, but I can help you find a video or resources.")

        return []


class ActionProvideResources(Action):
    def name(self) -> Action:
        return "action_provide_resources"

    def run(self, dispatcher: CollectingDispatcher, tracker):
        subject = tracker.latest_message.get('text')

        # Example of providing a resource link
        if 'python' in subject.lower():
            dispatcher.utter_message(
                text="Here are some resources to learn Python:\n- [Python Official Documentation](https://docs.python.org/)\n- [Learn Python - W3Schools](https://www.w3schools.com/python/)")
        elif 'data science' in subject.lower():
            dispatcher.utter_message(
                text="Here are some resources to learn Data Science:\n- [Data Science Handbook](https://jakevdp.github.io/PythonDataScienceHandbook/)\n- [Kaggle](https://www.kaggle.com/)")
        else:
            dispatcher.utter_message(text="Sorry, I couldn't find any specific resources for that topic.")

        return []
