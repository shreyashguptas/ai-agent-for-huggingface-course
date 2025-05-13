[<img src="hf-logo.svg" alt="Hugging Face" width="80" style="vertical-align:middle;">](https://huggingface.co)

# AI Agent for GAIA Benchmark (Hugging Face Project)

## Project Overview

This project was completed as part of a Hugging Face challenge, where I built an AI agent capable of answering a diverse set of questions using a variety of tools and data sources. I successfully passed the challenge and received a certificate for my work.

- **Platform:** Hugging Face
- **Model Provider:** OpenAI (GPT-4.1)
- **Score Achieved:** **35%** (number of questions answered correctly out of the total evaluated)
- **Agent Notebook:** See `agent.ipynb` for the full implementation, logic, and tool usage.

### Types of Questions Answered
- Factual and encyclopedic queries
- Web search and current events
- Audio transcription (e.g., extracting information from voice memos)
- Image analysis (e.g., chessboard positions)
- Excel/CSV data analysis (e.g., sales totals)
- Mathematical and logic puzzles

### Tools Used by the Agent
- **OpenAI GPT-4.1** (for planning, synthesis, and vision tasks)
- **Wikipedia Search** (via `wikipedia` Python package)
- **SerpAPI Web Search** (Google/Bing search)
- **Excel/CSV File Parser** (using `pandas`)
- **Image Analysis** (OpenAI Vision API)
- **Audio Transcription** (OpenAI Whisper)

### Supported File Types
- `.mp3`, `.wav`, `.m4a`, `.flac`, `.ogg` (audio)
- `.png`, `.jpg`, `.jpeg` (images)
- `.xlsx`, `.xls`, `.csv` (spreadsheets)

---

## How to Reproduce or Run This Notebook

### 1. Clone the Repository

```
git clone <this-repo-url>
cd ai_agents_course
```

### 2. Create the `config.json` File

At the top of `agent.ipynb`, you will find a code block like this:

```json
{
    "openai_api_key": "",
    "host": "https://us.cloud.langfuse.com",
    "langfuse_secret": "",
    "langfuse_public_key": "",
    "HF_TOKEN": "",
    "SERPAPI_API_KEY": ""
}
```

- Copy this block into a new file called `config.json` in the project root.
- Fill in your own API keys:
  - `openai_api_key`: Your OpenAI API key
  - `langfuse_secret` and `langfuse_public_key`: Your Langfuse credentials
  - `HF_TOKEN`: Your Hugging Face token (optional, only needed for Hugging Face integration)
  - `SERPAPI_API_KEY`: Your SerpAPI key

> **Note:** If you are not using Hugging Face, you can ignore or remove the Hugging Face-specific code (see later steps in `agent.ipynb`).

### 3. Install Dependencies

This project uses **Python 3.12.9**. Install the required packages by running the following in a notebook cell or your terminal:

```python
# Uncomment and run this in your notebook or terminal
!pip install -q langfuse wikipedia openai google-search-results pandas openai-whisper ffmpeg-python openpyxl
```

### 4. Prepare the Questions

- Create a folder called `all-json` in the project root.
- Place your questions in a file named `all_questions.json` inside `all-json/`.
- The format should be a list of question objects, for example:

```json
[
  {
    "task_id": "2d83110e-a098-4ebb-9987-066c06fa42d0",
    "question": ".rewsna eht sa \"tfel\" drow eht fo etisoppo eht etirw ,ecnetnes siht dnatsrednu uoy fI",
    "Level": "1",
    "file_name": ""
  },
  ...
]
```

### 5. Run the Notebook

- Open `agent.ipynb` in Jupyter or VSCode.
- Run all cells in order. The agent will process the questions, use the appropriate tools, and output the results.
- Final answers and validation results will be saved in the `all-json` folder.

---

## Notes
- The agent is modular and can be extended with new tools or data sources.
- For best results, ensure all API keys are valid and you have internet access for web/API calls.
- The Hugging Face integration is optional and can be removed if not needed.
