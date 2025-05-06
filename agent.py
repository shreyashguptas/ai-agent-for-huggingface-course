import json
from langfuse import Langfuse
from langfuse.callback import CallbackHandler

class GaiaAgent:
    def __init__(self, config_path="config.json"):
        with open(config_path, "r") as f:
            config = json.load(f)
        self.langfuse = Langfuse(
            public_key=config["langfuse_public_key"],
            secret_key=config["langfuse_secret"],
            host=config["host"]
        )
        self.callback_handler = CallbackHandler(self.langfuse)

    def process_question(self, question, file_content=None):
        # Start a trace for this question
        with self.langfuse.trace(name="process_question", input=question) as trace:
            # For now, just echo the question as the answer
            answer = question["question"]
            trace.set_output(answer)
            return answer
