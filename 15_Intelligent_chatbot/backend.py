import openai

# NOTE: DON'T WANT TO GIVE MY PHONE NUMBER TO GET AN API KEY
# NOTE: SO, IT DOESN'T WORK !

class ChatBot():
    def __init__(self):
        openai.api_key = ""

    def get_response(self, user_input):
        """Send prompt to model and return response
        """
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=user_input,
            max_tokens=3000,
            temperature=0.5
        ).choices[0].text
        return response