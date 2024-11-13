import streamlit as st
import requests


# Injecting Font Awesome CDN for icons
st.markdown("""
    <head>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
    </head>
""", unsafe_allow_html=True)

# Custom CSS for improved design
st.markdown("""
    <style>
        body {
            background-color: #f0f4f8; /* Light background */
            font-family: 'Arial', sans-serif;
            padding: 20px;
        }
        .title {
            text-align: center;
            color: #3a5a99; /* Deep blue for title */
            font-size: 36px;
            font-weight: bold;
            margin-bottom: 40px;
        }
        .button {
            background-color: #4CAF50;
            color: white;
            border-radius: 12px;
            padding: 12px 25px;
            margin: 10px;
            text-align: center;
            width: 200px;
            font-size: 16px;
            cursor: pointer;
            transition: background-color 0.3s ease, transform 0.2s;
        }
        .button:hover {
            background-color: #45a049;
            transform: scale(1.05);
        }
        .card {
            background-color: white;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
        }
        .section-title {
            color: #3a5a99; /* Deep blue for section titles */
            font-weight: bold;
            font-size: 20px;
        }
        .abstract-text {
            color: #555555;
            font-size: 16px;
            line-height: 1.6;
        }
        .response {
            font-size: 18px;
            color: #333333;
            background-color: #f9f9f9;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .input-field {
            padding: 12px;
            width: 100%;
            border-radius: 10px;
            border: 1px solid #ccc;
            margin-bottom: 20px;
        }
        .question-section {
            margin-top: 40px;
            padding-top: 20px;
            border-top: 2px solid #e0e0e0;
        }
        .footer {
            text-align: center;
            color: #777777;
            font-size: 14px;
            margin-top: 40px;
        }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown("<h1 class='title'>Research Nexus</h1>", unsafe_allow_html=True)

# Topic input
topic = st.text_input("Enter a research topic:", key="topic", placeholder="e.g., Artificial Intelligence in Healthcare")

# Search button
if st.button("Search Papers", key="search", help="Search for research papers related to your topic"):
    response = requests.get(f"http://localhost:8000/search_papers/?topic={topic}")
    if response.status_code == 200:
        data = response.json()
        papers = data.get("papers", [])
        if papers:
            st.write(f"### Research papers on '{topic}':")
            for i, paper in enumerate(papers, 1):
                st.markdown(f"""
                    <div class="card">
                        <h3 class="section-title">{i}. {paper['title']}</h3>
                        <p class="abstract-text">{paper['abstract']}</p>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.write("No papers found for the given topic.")
    else:
        st.write("An error occurred while fetching the papers.")

# Summarize button
if st.button("Summarize", key="summarize", help="Summarize the research papers related to your topic"):
    response = requests.get(f"http://localhost:8000/summarize/?topic={topic}")
    if response.status_code == 200:
        summary = response.json().get("summary", "No summary available.")
        st.markdown(f"<div class='response'>{summary}</div>", unsafe_allow_html=True)

# Generate future directions button
if st.button("Generate Future Directions", key="directions", help="Generate potential future research directions"):
    response = requests.get(f"http://localhost:8000/future_directions/?topic={topic}")
    if response.status_code == 200:
        directions = response.json().get("future_directions", "No future directions available.")
        st.markdown(f"<div class='response'>{directions}</div>", unsafe_allow_html=True)

# Ask a question input field and button
question = st.text_input("Ask a question related to this topic:", key="question", placeholder="e.g., What are the challenges in AI healthcare?")
if st.button("Ask Question", key="ask", help="Ask a question related to the topic"):
    if question:
        response = requests.get(f"http://localhost:8000/ask_question/?topic={topic}&question={question}")
        if response.status_code == 200:
            answer = response.json().get("answer", "Sorry, I couldn't find an answer to that question.")
            st.markdown(f"<div class='response'>{answer}</div>", unsafe_allow_html=True)
        else:
            st.write("An error occurred while fetching the answer.")
    else:
        st.write("Please enter a question.")



st.markdown("""
    <style>
        .footer {
            text-align: center;
            padding: 10px;
            font-family: Arial, sans-serif;
        }
        .footer-links a {
            margin: 0 15px;
            text-decoration: none;
            color: #000;
            font-weight: bold;
        }
        .footer-links {
            display: inline-block;
            margin-bottom: 10px;
        }
        .footer p {
            margin: 5px 0;
            color: #666;
            font-size: 14px;
        }
    </style>

    <div class="footer">
        <div class="footer-links">
            <a href="https://github.com/Ravii-saini" target="_blank">GitHub</a>
            <a href="https://www.linkedin.com/in/ravi-sainii/" target="_blank">LinkedIn</a>
            <a href="mailto:ravisainijnv@example.com" class="contact-button">Contact Me</a>
        </div>
        <p>Made with ❤️ by Ravi</p>
        <p>© 2024 All Rights Reserved.</p>
    </div>
""", unsafe_allow_html=True)
