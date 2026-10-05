# AI Agent API Demo

A lightweight AI agent service built with FastAPI, LangGraph, Gemini, Pydantic and Docker.

## Architecture

```text
Client / Swagger
       ↓
FastAPI
       ↓
Pydantic validation
       ↓
LangGraph
       ↓
Conditional router
   ↙           ↘
Tool           LLM
   \           /
    Final response
```
## What this project demonstrates

- Building a REST API with FastAPI.
- Request validation with Pydantic.
- LLM integration using the Gemini API.
- Stateful agent workflows with LangGraph.
- Conditional routing based on application state.
- Integration of a custom Python tool within an agent workflow.
- Environment-based API key management.
- Containerization with Docker.

## Run locally

Clone the repository:

```bash
git clone https://github.com/majjuarez1992-art/ai-agent-api-demo.git
cd ai-agent-api-demo
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment on Windows:

```bash
.venv\Scripts\activate
```

Install the project dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file in the project root and add your Gemini API key:

```env
GEMINI_API_KEY=your_api_key_here
```

Start the FastAPI application:

```bash
uvicorn main:app --reload
```

Open the interactive Swagger documentation in your browser:

```text
http://127.0.0.1:8000/docs
```

You can then test the agent through the `POST /agent/query` endpoint using a request such as:

```json
{
  "question": "What is the status of component 25?"
}
```

Example response:

```json
{
  "question": "What is the status of component 25?",
  "component_id": 25,
  "component_status": {
    "component_id": 25,
    "status": "warning",
    "quality": 72
  },
  "answer": "The component is currently in warning status with a quality value of 72."
}
```

## Run with Docker

Build the Docker image:

```bash
docker build -t ai-agent-api-demo .
```

Run the container and provide the environment variables from your local `.env` file:

```bash
docker run --rm \
  --name ai-agent-api-demo \
  -p 8000:8000 \
  --env-file .env \
  ai-agent-api-demo
```

On Windows PowerShell, the same command can be written in one line:

```powershell
docker run --rm --name ai-agent-api-demo -p 8000:8000 --env-file .env ai-agent-api-demo
```

Open the Swagger documentation:

```text
http://localhost:8000/docs
```

The Docker workflow is:

```text
Source code
    ↓
Dockerfile
    ↓
docker build
    ↓
Docker image
    ↓
docker run
    ↓
Running container
    ↓
FastAPI + LangGraph + Gemini
```

The `.env` file is not copied into the Docker image. It is passed to the container at runtime using `--env-file`.