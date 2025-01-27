# Chatbot for Personalized Learning

Infosys Learning Project (Demo)

# Requirements
To run the chatbot, you need the following:

Python 3.8 or later
Rasa Open Source
Streamlit
Additional libraries as specified in requirements.txt

# Installation

# Prerequisites
   Python 3.10 or later
   Rasa Open Source
   Virtual environment (recommended)
   
# Setup Instructions

1)Clone the Repository:

    git clone https://github.com/divyasri27k/Chatbot_for_Personalized_Learning.git
    
2)Navigate to the Project Directory

3)Create and Activate a Virtual Environment

4)Install Dependencies

     pip install -r requirements.txt
     
5)Train the model

    rasa train
    
6)Run the Chatbot Interactively

    rasa shell
    
7)Run the Chatbot as a Server

    rasa run

# Start the Rasa Action Server:

   rasa run actions
   
  
   Start the Rasa Shell:
   

   rasa run -m models --enable-api --cors "*" --debug
   
   
   Launch the Streamlit UI:
   

   streamlit run app.py
   


