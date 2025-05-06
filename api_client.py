import os
import requests
import json
from typing import List, Dict, Any, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class GaiaAPIClient:
    """Client for the GAIA benchmark API."""
    
    def __init__(self, base_url: str = "https://agents-course-unit4-scoring.hf.space"):
        self.base_url = base_url
        logger.info(f"API client initialized with base URL: {base_url}")
        
    def get_all_questions(self) -> List[Dict[str, Any]]:
        """Grab all the questions from the benchmark."""
        response = requests.get(f"{self.base_url}/questions")
        if response.status_code == 200:
            questions = response.json()
            logger.info(f"Retrieved {len(questions)} questions")
            return questions
        else:
            logger.error(f"Failed to get questions: {response.status_code} - {response.text}")
            raise Exception(f"Failed to get questions: {response.status_code}")
            
    def get_random_question(self) -> Dict[str, Any]:
        """Pick a random question to try."""
        response = requests.get(f"{self.base_url}/random-question")
        if response.status_code == 200:
            question = response.json()
            logger.info(f"Retrieved random question: {question.get('task_id')}")
            return question
        else:
            logger.error(f"Failed to get random question: {response.status_code} - {response.text}")
            raise Exception(f"Failed to get random question: {response.status_code}")
    
    def get_file(self, task_id: str) -> bytes:
        """Download any files attached to a question."""
        response = requests.get(f"{self.base_url}/files/{task_id}")
        if response.status_code == 200:
            logger.info(f"Downloaded file for task: {task_id}")
            return response.content
        else:
            logger.error(f"Failed to download file for task {task_id}: {response.status_code} - {response.text}")
            raise Exception(f"Failed to download file for task {task_id}: {response.status_code}")
    
    def submit_answers(self, username: str, code_link: str, answers: List[Dict[str, str]]) -> Dict[str, Any]:
        """Send our answers to the leaderboard."""
        payload = {
            "username": username,
            "agent_code": code_link,
            "answers": answers
        }
        logger.info(f"Submitting answers for {username}: {len(answers)} responses")
        
        response = requests.post(f"{self.base_url}/submit", json=payload)
        if response.status_code == 200:
            result = response.json()
            logger.info(f"Submission successful. Score: {result.get('score', 'N/A')}")
            return result
        else:
            logger.error(f"Submission failed: {response.status_code} - {response.text}")
            raise Exception(f"Submission failed: {response.status_code} - {response.text}")
