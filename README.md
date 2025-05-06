---
title: AI Agents Course - GAIA Benchmark Agent
emoji: 🤖
colorFrom: gray
colorTo: blue
sdk: static
pinned: false
---

# AI Agents Course - Final Project

This repository contains an AI agent designed to answer questions from the GAIA benchmark for the Hugging Face AI Agents Course final project.

## Project Overview

The goal is to create an agent that can score at least 30% on the benchmark, which consists of 20 questions extracted from the GAIA validation set.

## Setup Instructions

### Prerequisites
- Python 3.8+
- OpenAI API key
- Optional: Langfuse account for tracing (optional)

### Installation

1. Clone this repository
2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Configure your environment:
   - Your OpenAI API key is already in the `.env` file
   - Update your username and code link in `config.json`

## Usage

### Running a Single Question

To evaluate the agent on a single random question:

```bash
python run_evaluation.py --single
```

To evaluate on a specific question by task ID:

```bash
python run_evaluation.py --task-id <TASK_ID>
```

### Running the Full Evaluation

To evaluate all 20 questions:

```bash
python run_evaluation.py
```

### Submitting Results

To submit your results to the leaderboard:

```bash
python run_evaluation.py --submit
```

or to run and immediately submit:

```bash
python run_evaluation.py --submit
```

## Project Structure

- `agent.py` - AI agent implementation using LangChain
- `api_client.py` - Client for the benchmark evaluation API
- `run_evaluation.py` - Script to run evaluations and submit results
- `config.json` - Configuration file for the agent and API
- `requirements.txt` - Project dependencies

## API Endpoints

- `GET /questions`: Get all evaluation questions
- `GET /random-question`: Get a random question
- `GET /files/{task_id}`: Download a file for a specific task
- `POST /submit`: Submit answers for scoring
