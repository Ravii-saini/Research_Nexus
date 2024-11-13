import google.generativeai as genai

# Configure the Gemini model with your API key
genai.configure(api_key="AIzaSyA8VwFWNfx_j759DpP_L6sIBOwC2PtAcE8")  # Replace with your actual API key

def generate_ideas(papers):
    # Combine the abstracts of the papers into one string
    combined_abstracts = " ".join([paper['abstract'] for paper in papers])

    # Prepare the prompt to suggest future research directions based on the combined abstracts
    prompt = f"""
    Based on the following abstracts of recent research papers, suggest new and relevant research directions in the field of AI. Please ensure that the research ideas are specific, feasible, and innovative, but not too broad. The total response should be between 300 to 500 words.

    Here are the abstracts of the papers:

    {combined_abstracts}

    Research ideas:
    """

    # Initialize the Gemini model
    model = genai.GenerativeModel("gemini-1.5-flash")

    try:
        # Generate the research ideas using Gemini
        response = model.generate_content(prompt)
        
        # Extract the generated text (research ideas) and clean it
        research_ideas = response.text.strip()
        return research_ideas
    except Exception as e:
        # Handle any errors that occur during the API request
        print(f"Error during idea generation: {e}")
        return "Error generating research ideas."
