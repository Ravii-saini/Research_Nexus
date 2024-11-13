import google.generativeai as genai

# Configure the Gemini model with your API key
genai.configure(api_key="AIzaSyA8VwFWNfx_j759DpP_L6sIBOwC2PtAcE8")  # Replace with your actual API key

# Define the function to get an answer based on the topic, question, and related research papers' abstracts
def give_answer(topic, question, papers):
    # Combine the abstracts of the papers into a single string
    combined_abstracts = " ".join([paper['abstract'] for paper in papers])

    # Prepare the prompt with both the topic, question, and the combined abstracts
    prompt = f"""
    Given the research topic '{topic}' and the following abstracts of recent research papers: {combined_abstracts},
    please provide a concise and relevant answer to the question: '{question}'. 

    - Ensure that the answer is clear and focused, avoiding overly long explanations.
    also provide refrence of the title of page from which u understand and which paper is base for your answer from all paper u have 
    - Whenever possible, base the answer directly on the information provided in the research papers.
    - If the answer is not explicitly found in the papers, make sure to mention that and offer a general perspective based on the available content.
    """


    # Initialize the Gemini model
    model = genai.GenerativeModel("gemini-1.5-flash")

    try:
        # Generate the answer using Gemini
        response = model.generate_content(prompt)
        
        # Extract and return the answer
        answer = response.text.strip()
        return answer

    except Exception as e:
        # Handle any errors that occur during the API request
        print(f"Error during question answering: {e}")
        return "Error generating answer."
