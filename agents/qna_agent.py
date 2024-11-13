import google.generativeai as genai

# Configure the Gemini model with your API key
genai.configure(api_key="AIzaSyA8VwFWNfx_j759DpP_L6sIBOwC2PtAcE8")  # Replace with your actual API key

# Define the function to summarize research papers
def summarize(papers):
    # Combine all the abstracts into one string
    combined_abstracts = " ".join([paper['abstract'] for paper in papers])

    # Prepare the prompt to summarize all papers in 100 words
    prompt = f"""
    Please summarize the following research papers as a unified overview. Focus on the key findings, contributions, and main points from all the abstracts, highlighting the most important aspects of the research. Keep the summary brief, clear, and to the point, encapsulating the essence of the collective work.

    Here are the abstracts of the papers:

    {combined_abstracts}

    Summary:
    """



    # Initialize the Gemini model
    model = genai.GenerativeModel("gemini-1.5-flash")

    try:
        # Generate the summary using Gemini
        response = model.generate_content(prompt)
        
        # Get the summary and trim it to 100 words
        summary = response.text.strip()
        # words = summary.split()
        
        # # Limit the summary to the first 100 words
        # summary_100_words = " ".join(words[:100])
        return summary
    except Exception as e:
        # Handle any errors that occur during the API request
        print(f"Error during summarization: {e}")
        return "Error generating summary."
