from fastapi import FastAPI, HTTPException
from agents import search_agent, qna_agent, future_work_agent,question_answer
from database.influxdb_client import  save_multiple_papers, get_paper_data

app = FastAPI()

@app.get("/search_papers/")
async def search_papers(topic: str):
    papers = search_agent.fetch_papers(topic)
    if papers:
        try:
            # Ensure save_paper_data processes each paper correctly
            save_multiple_papers(papers, topic)
            status = "Papers saved successfully"
        except Exception as e:
            # Log or handle the exception as needed
            status = f"Error saving papers: {e}"
            return {"status": status, "papers": []}  # Return empty papers if save fails
    else:
        status = "No papers found"
    return {"status": status, "papers": papers}


@app.get("/summarize/")
async def summarize_papers(topic: str):
    papers = get_paper_data(topic)
    if not papers:
        raise HTTPException(status_code=404, detail=f"No papers found for topic: {topic}")
    summary = qna_agent.summarize(papers)
    return {"summary": summary}


@app.get("/future_directions/")
async def generate_future_directions(topic: str):
    papers = get_paper_data(topic)
    if not papers:
        raise HTTPException(status_code=404, detail="No papers found")
    future_ideas = future_work_agent.generate_ideas(papers)
    return {"future_directions": future_ideas}


@app.get("/ask_question/")
async def ask_question(topic: str, question: str):
    # Integrate with an AI model or use custom logic to answer the question based on the topic
    papers = get_paper_data(topic)
    if not papers:
        raise HTTPException(status_code=404, detail="No papers found")
    answer = question_answer.give_answer(topic,question,papers)
    return {"answer": answer}
