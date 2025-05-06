import os
import argparse
import json
from typing import List, Dict, Any, Optional
import logging
import sys

from api_client import GaiaAPIClient
from agent import GaiaAgent

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def evaluate_all_questions(
    api_client: GaiaAPIClient,
    agent: GaiaAgent,
    save_path: str = "evaluation_results.json"
) -> List[Dict[str, str]]:
    """Run through all questions and get answers from the agent.
    
    Saves progress as we go in case we need to resume later.
    """
    # Get all questions
    questions = api_client.get_all_questions()
    logger.info(f"Starting evaluation on {len(questions)} questions")
    
    answers = []
    
    # Process each question
    for i, question in enumerate(questions):
        task_id = question.get("task_id")
        question_text = question.get("question")
        
        logger.info(f"[{i+1}/{len(questions)}] Processing question {task_id}")
        
        # Check if the question has an associated file
        file_content = None
        if question.get("has_file", False):
            try:
                file_content = api_client.get_file(task_id)
                logger.info(f"Downloaded file for task {task_id}")
            except Exception as e:
                logger.error(f"Error downloading file for task {task_id}: {e}")
        
        # Process the question
        try:
            answer = agent.process_question(question, file_content)
            answers.append({
                "task_id": task_id,
                "question": question_text,
                "submitted_answer": answer
            })
            
            logger.info(f"Answer for task {task_id}: {answer}")
            
            # Save intermediate results
            with open(save_path, "w") as f:
                json.dump(answers, f, indent=2)
                logger.info(f"Saved intermediate results to {save_path}")
        except Exception as e:
            logger.error(f"Error processing question {task_id}: {e}")
    
    return answers

def evaluate_single_question(
    api_client: GaiaAPIClient,
    agent: GaiaAgent,
    task_id: Optional[str] = None
) -> Dict[str, str]:
    """Try out the agent on one question, either random or specified by ID."""
    # Get the question
    if task_id:
        questions = api_client.get_all_questions()
        question = next((q for q in questions if q.get("task_id") == task_id), None)
        if not question:
            raise ValueError(f"Question with task_id {task_id} not found")
    else:
        question = api_client.get_random_question()
        task_id = question.get("task_id")
    
    logger.info(f"Evaluating single question: {task_id}")
    
    # Check if the question has an associated file
    file_content = None
    if question.get("has_file", False):
        try:
            file_content = api_client.get_file(task_id)
            logger.info(f"Downloaded file for task {task_id}")
        except Exception as e:
            logger.error(f"Error downloading file for task {task_id}: {e}")
    
    # Process the question
    answer = agent.process_question(question, file_content)
    result = {
        "task_id": task_id,
        "question": question.get("question"),
        "submitted_answer": answer
    }
    logger.info(f"Answer for task {task_id}: {answer}")
    
    return result

def main():
    parser = argparse.ArgumentParser(description='Run GAIA benchmark evaluation')
    parser.add_argument('--config', type=str, default='config.json', help='Path to config file')
    parser.add_argument('--single', action='store_true', help='Evaluate a single random question')
    parser.add_argument('--task-id', type=str, help='Evaluate a specific question by task ID')
    parser.add_argument('--submit', action='store_true', help='Submit results to leaderboard')
    parser.add_argument('--results', type=str, default='evaluation_results.json', help='Path to results file')
    args = parser.parse_args()
    
    # Load config
    try:
        with open(args.config, 'r') as f:
            config = json.load(f)
    except Exception as e:
        logger.error(f"Error loading config: {e}")
        config = {}
    
    # Initialize API client
    api_client = GaiaAPIClient(
        base_url=config.get('api_base_url', 'https://agents-course-unit4-scoring.hf.space')
    )
    
    # Initialize the agent
    agent = GaiaAgent()
    
    results = None
    
    # Run evaluation
    if args.single or args.task_id:
        # Evaluate a single question
        result = evaluate_single_question(api_client, agent, args.task_id)
        print(f"\nResult for task {result['task_id']}:\n{result['submitted_answer']}")
    else:
        # Check if results file exists and ask to continue
        if os.path.exists(args.results):
            try:
                with open(args.results, 'r') as f:
                    results = json.load(f)
                    logger.info(f"Loaded {len(results)} existing results from {args.results}")
                choice = input(f"Found existing results with {len(results)} answers. Continue evaluation? (y/n): ")
                if choice.lower() != 'y':
                    results = None
            except Exception as e:
                logger.error(f"Error loading existing results: {e}")
        
        # Run full evaluation if needed
        if results is None:
            results = evaluate_all_questions(api_client, agent, args.results)
        
        print(f"\nEvaluation completed with {len(results)} answers")
    
    # Submit results if requested
    if args.submit and results:
        username = config.get('username')
        code_link = config.get('code_link')
        
        if not username:
            username = input("Enter your Hugging Face username: ")
        
        if not code_link:
            code_link = input("Enter the URL to your code (your HF Space tree/main URL): ")
        
        try:
            submission_result = api_client.submit_answers(username, code_link, results)
            score = submission_result.get('score', 'N/A')
            logger.info(f"Submission successful. Score: {score}")
            print(f"\nSubmission successful! Your score: {score}")
            
            # Print additional information if available
            if 'details' in submission_result:
                print("\nDetailed results:")
                for detail in submission_result['details']:
                    print(f"Task {detail.get('task_id')}: {'✓' if detail.get('is_correct') else '✗'}")
        except Exception as e:
            logger.error(f"Error submitting results: {e}")
            print(f"Error submitting results: {str(e)}")

if __name__ == "__main__":
    main()
