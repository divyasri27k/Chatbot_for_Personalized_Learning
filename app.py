import streamlit as st
import requests
import json
from datetime import datetime

# Add custom CSS styles for a professional design
st.markdown("""
    <style>
        /* Global Styles */
        body {
            font-family: 'Arial', sans-serif;
            background-color: #DBADD9;
            margin: 0;
            padding: 0;
        }

        /* Header Styles */
        .header {
            font-size: 3em;
            font-weight: bold;
            text-align: center;
            color: #2c3e50;
            text-shadow: 3px 3px 5px rgba(0, 0, 0, 0.3);
            margin-top: 20px;
        }
        .subheader {
            font-size: 1.5em;
            text-align: center;
            color: #811B1B;
            font-style: italic;
            letter-spacing: 2px;
            animation: pop 1s ease-out forwards;
        }
        @keyframes pop {
            0% { transform: scale(0.8); opacity: 0; }
            100% { transform: scale(1); opacity: 1; }
        }

        /* Chatbot Styles */
        .chat-container {
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            background-color: #E6AFAF;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            border: 1px solid #ddd;
            margin-bottom: 30px;
        }
        .message {
            padding: 10px 15px;
            margin: 10px 0;
            border-radius: 10px;
        }
        .message.user {
            background-color: #B0DBE6;
            text-align: right;
        }
        .message.assistant {
            background-color: #C8B0E6;
            text-align: left;
        }

        /* Sidebar Styles */
        .sidebar {
            background-color: #651A61;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .sidebar h1 {
            font-size: 1.8em;
            font-weight: bold;
            color: #4CAF50;
        }
        .sidebar p {
            font-size: 1em;
            color: #666;
        }

        /* Button and Link Styles */
        .button {
            background-color: #4CAF50;
            color: white;
            padding: 10px 20px;
            border-radius: 5px;
            text-align: center;
            text-decoration: none;
            transition: all 0.3s ease;
        }
        .button:hover {
            background-color: #45a049;
        }
        a {
            color: #007bff;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
    </style>
""", unsafe_allow_html=True)

# Create a creative header with a bold and centered title and a popping subheading
st.markdown("""
    <div class="header">AcademiaBot</div>
    <div class="subheader">Your companion in the journey of education</div>
""", unsafe_allow_html=True)

# Initialize chat history and enrolled courses
if "messages" not in st.session_state:
    st.session_state.messages = []
if "enrolled_courses" not in st.session_state:
    st.session_state.enrolled_courses = []

# Define materials for all topics
COURSE_MATERIALS = {
    "web": {
        "name": "Web Development for Beginners",
        "materials": [
            {"name": "Beginner course for Web Development", "url": "https://youtube.com/playlist?list=PLfqMhTWNBTe3H6c9OGXb5_6wcc1Mca52n&si=EjjRsPFo6oCej3cJ"},
            {"name": "Source link(GFG)", "url": "https://www.geeksforgeeks.org/web-development/"},
            {"name": "Certificate", "url": "https://www.udemy.com/courses/development/web-development/"}
        ],
        "description": "Master the art of building stunning, responsive websites in web development",
        "learning_path": [
            "Start with HTML & CSS basics",
            "Move on to JavaScript",
            "Choose a framework (React, Vue, or Angular)"
        ]
    },
    "data": {
        "name": "Data Science for Beginners",
        "materials": [
            {"name": "Beginner course for Data Science", "url": "https://youtu.be/-ETQ97mXXF0?si=YDpBNowP1_g3FRMk"},
            {"name": "Source link(GFG)", "url": "https://www.geeksforgeeks.org/data-science/"},
            {"name": "Certificate", "url": "https://www.mygreatlearning.com/data-science/free-courses"}
        ],
        "description": "A comprehensive introduction to data science and analysis",
        "learning_path": [
            "Learn Python basics",
            "Master data analysis libraries",
            "Practice with real datasets"
        ]
    },
    "mobile": {
        "name": "Mobile App Development for Beginners",
        "materials": [
            {"name": "Beginner course for Mobile", "url": "https://youtu.be/6N5Gny4YlbU?si=SEp3DTPxKdLJjqUe"},
            {"name": "Source link(GFG)", "url": "https://www.geeksforgeeks.org/introduction-of-mobile-applications/"},
            {"name": "Certificate", "url": "https://www.simplilearn.com/free-app-development-course-skillup"}
        ],
        "description": "Learn to build mobile apps for iOS and Android",
        "learning_path": [
            "Choose your platform (iOS/Android)",
            "Learn platform basics",
            "Build your first app"
        ]
    },
    "cloud": {
        "name": "Cloud for Beginners",
        "materials": [
            {"name": "Beginner course for Cloud", "url": "https://youtube.com/playlist?list=PL9ooVrP1hQOFtZ5oAAeOgi_nH-txMcDMu&si=zzx58vd0rgPZMybF"},
            {"name": "Source link(GFG)", "url": "https://www.geeksforgeeks.org/cloud-computing/"},
            {"name": "Certificate", "url": "https://alison.com/tag/devops"}
        ],
        "description": "Learn to build mobile apps for iOS and Android",
        "learning_path": [
            "Choose your platform (Aws/Azure)",
            "Learn platform basics"
        ]
    },
    "rasa": {
        "name": "Rasa for Beginners",
        "materials": [
            {"name": "Beginner platform for Rasa", "url": "https://youtube.com/playlist?list=PLp9h3aIPyUbZyCUP4ELTaS2ajxKNWaSnU&si=mPtFFawe2q1r5nK8"},
            {"name": "Rasa doc", "url": "https://rasa.com/docs/rasa/custom-actions"}
        ],
        "description": "Learn to build rasa platform ",
        "learning_path": [
            "Choose your platform (rasa)",
            "Learn platform basics"
        ]
    },
    "ai": {
        "name": "Artificial Intelligence for Beginners",
        "materials": [
            {"name": "Beginner course for AI", "url": "https://youtu.be/0TCYAafJgRE?si=07dOrcxM5nmDqdOo"},
            {"name": "Source link(GFG)", "url": "https://www.geeksforgeeks.org/artificial-intelligence/"},
            {"name": "Certificate", "url": "https://alison.com/tag/artificial-intelligence"}
        ],
        "description": "Introduction to AI and machine learning concepts",
        "learning_path": [
            "Learn Python and mathematics basics",
            "Understand ML fundamentals",
            "Practice with AI frameworks"
        ]
    }
}

# Add feedback responses
FEEDBACK_RESPONSES = {
    "thanks": [
        "You're always welcome! 😊 Feel free to reach out anytime if you need help!",
        "Glad I could assist! 🌟 Keep exploring and learning more courses!",
        "You're welcome! 🎉 Don't hesitate to ask if you need anything else!"
    ],
    "good": [
        "Thank you for the kind words! 🌟 Anything else you'd like to explore?",
        "I'm glad to hear that! 🎉 Let me know if there's more you'd like to learn!",
        "It's great to hear that! 😊 Feel free to ask about more topics anytime!"
    ],
    "bye": [
        "Goodbye for now! 👋 Come back anytime to continue your learning journey!",
        "See you soon! 🌟 Your enrolled courses will be waiting when you return!",
        "Have a fantastic day! 😊 Keep up with your newfound knowledge!"
    ],
    "hello": [
        "Hello! 👋 Ready to dive into new learning adventures?",
        "Welcome! 🌟 What would you like to learn today? I'm here to help!",
        "Hi there! 😊 Let me know how I can help you find the perfect course!"
    ]
}

def get_feedback_response(prompt):
    import random
    if any(word in prompt for word in ["thanks", "thank you", "thx"]):
        return random.choice(FEEDBACK_RESPONSES["thanks"])
    elif any(word in prompt for word in ["good", "great", "awesome", "amazing"]):
        return random.choice(FEEDBACK_RESPONSES["good"])
    elif any(word in prompt for word in ["bye", "goodbye", "see you"]):
        return random.choice(FEEDBACK_RESPONSES["bye"])
    elif any(word in prompt for word in ["hi", "hello", "hey"]):
        return random.choice(FEEDBACK_RESPONSES["hello"])
    return None

def display_course_response(topic):
    course = COURSE_MATERIALS[topic]
    response_text = f"🎉 Welcome to {course['name']}!"

    # For AI-related topics, add a robotic emoji 🤖 to the response
    if topic == "ai":
        response_text = "👾 " + response_text

    st.markdown(response_text)
    st.write("📚 *Learning Materials:*")
    for material in course['materials']:
        st.markdown(f"• [{material['name']}]({material['url']})")

    st.write("\n📝 *Course Description:*")
    st.write(course['description'])

    st.info("💡 *Learning Path:*\n" +
            "\n".join(f"{i+1}. {step}" for i, step in enumerate(course['learning_path'])) +
            "\n\nType 'show my courses' anytime to see your enrolled courses!")

    # Add course to enrolled courses
    course_entry = {
        "name": course['name'],
        "enrolled_at": datetime.now().strftime("%Y-%m-%d"),
        "status": "In Progress",
        "materials": course['materials']
    }
    if course_entry not in st.session_state.enrolled_courses:
        st.session_state.enrolled_courses.append(course_entry)

    return response_text, course['materials']

def show_enrolled_courses():
    if st.session_state.enrolled_courses:
        response_text = "Here are your enrolled courses:\n\n"
        for course in st.session_state.enrolled_courses:
            response_text += f"📚 {course['name']}\n"
            response_text += f"Status: {course['status']}\n"
            response_text += f"Enrolled: {course['enrolled_at']}\n\n"

        st.markdown(response_text)

        # Show materials for each course
        for course in st.session_state.enrolled_courses:
            st.write(f"\n*Materials for {course['name']}:*")
            for material in course['materials']:
                st.markdown(f"• [{material['name']}]({material['url']})")
    else:
        st.markdown("You're not enrolled in any courses yet. Would you like some recommendations?")

def check_input_requirements(prompt):
    has_experience = any(word in prompt for word in ["beginner", "intermediate", "advanced"])
    has_topic = any(word in prompt for word in ["web", "data", "science", "mobile", "app", "ai", "artificial", "cloud" , "rasa"])

    if not has_experience and not has_topic:
        return "Could you please mention both your experience level (beginner, intermediate, or advanced) and your area of interest? For example: 'I'm a beginner interested in web development.'"
    elif not has_experience:
        return "Please let me know your experience level (beginner, intermediate, or advanced). For example: 'I'm a beginner.'"
    elif not has_topic:
        return "Can you specify what you'd like to learn (web development, data science, mobile apps,rasa, cloud or artificial intelligence)?"
    return None

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "materials" in message:
            st.write("📚 *Learning Materials:*")
            for material in message["materials"]:
                st.markdown(f"• [{material['name']}]({material['url']})")

# Accept user input
if prompt := st.chat_input("Type here....."):
    prompt = prompt.lower()
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        # First check for feedback/greetings
        feedback_response = get_feedback_response(prompt)
        if feedback_response:
            st.markdown(feedback_response)
            st.session_state.messages.append({
                "role": "assistant",
                "content": feedback_response
            })
        # Then check for course-related queries
        elif "show my courses" in prompt:
            show_enrolled_courses()
            st.session_state.messages.append({
                "role": "assistant",
                "content": "Showing your enrolled courses"
            })
        else:
            # Check if input meets requirements
            requirement_message = check_input_requirements(prompt)
            if requirement_message:
                st.markdown(requirement_message)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": requirement_message
                })
            else:
                # Check for topic matches
                topic = None
                if "web" in prompt:
                    topic = "web"
                elif "data" in prompt or "science" in prompt:
                    topic = "data"
                elif "mobile" in prompt or "app" in prompt:
                    topic = "mobile"
                elif "rasa" in prompt or "rasa" in prompt:
                    topic = "rasa"
                elif "cloud" in prompt or "web" in prompt:
                    topic = "cloud"
                elif "ai" in prompt or "artificial" in prompt:
                    topic = "ai"

                if topic:
                    response_text, materials = display_course_response(topic)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response_text,
                        "materials": materials
                    })

# Add sidebar with additional information
with st.sidebar:
    st.header("Welcome to AcademiaBot: Chat. Learn. Grow.")
    st.write("👩‍🎓Looking to learn new programming languages or enhance your coding skills? Browse here🎯")
    st.write("What can I help you with today? 🔍")
    st.write("Try asking about:")
    st.write("- 🌐 Web Development (Learn how to build amazing websites! 💻)")
    st.write("- 📊 Data Science (Dive into data analysis, machine learning, and more! 📈)")
    st.write("- 📱 Mobile App Development (Create your own apps for Android & iOS! 📲)")
    st.write("- ☁ cloud (Learn how to handle cloud ! 💾)")
    st.write("- 🌐 Rasa (Learn how to build platforms ! 💻)")
    st.write("- 🤖 Artificial Intelligence (Explore the world of smart machines and AI! 🧠)")
    st.write("Feel free to ask me about any topic!🤗")
