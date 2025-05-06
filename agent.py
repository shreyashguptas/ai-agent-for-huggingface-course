import os
import json
import time
from typing import Dict, Any, List, Optional
import logging
import tempfile

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.tools import BaseTool, StructuredTool, Tool
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.callbacks.manager import CallbackManager
from langchain_core.messages import HumanMessage, AIMessage
from langchain.callbacks.tracers import LangChainTracer
from langchain_core.tools import tool
from langchain.chains import LLMChain
from langchain.agents import Agent

# Optional: Configure Langfuse for tracing
try:
    from langfuse.callback import CallbackHandler
    LANGFUSE_AVAILABLE = True
except ImportError:
    LANGFUSE_AVAILABLE = False

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class GaiaAgent:
    """Agent for answering GAIA benchmark questions."""
    
    def __init__(self, api_key: str, model_name: str = "gpt-4o-mini"):
        """Set up the agent with API key and model."""
        self.max_iterations = 2  # Reduce from 3 to 2 to prevent loops
        self.llm = ChatOpenAI(
            model=model_name,
            temperature=0,
            openai_api_key=api_key,
            max_tokens=150  # Limit response length
        )
        self.tools = self._setup_tools()
        self.agent = self._setup_agent()
        logger.info(f"Agent initialized with model {model_name}")
        
    def _setup_tools(self):
        """Set up the tools the agent can use."""
        def search_web(query: str, search_type: str = "general") -> str:
            """Search for info online. Supports general, wiki, academic, and news searches."""
            if search_type == "wikipedia":
                return "I don't know. The information is not available in Wikipedia."
            elif search_type == "academic":
                return "I don't know. The information is not available in academic databases."
            elif search_type == "news":
                return "I don't know. The information is not available in news sources."
            else:
                return "I don't know. The information is not available."

        def analyze_media(media_url: str, media_type: str) -> str:
            """Look at video or audio content."""
            if media_type == "video":
                return "I cannot analyze video content. Please provide a text description of what you need to know."
            elif media_type == "audio":
                return "I cannot analyze audio content. Please provide a transcript or text description."
            return "I cannot analyze this type of media. Please provide a text description."

        def analyze_file(file_path: str, file_type: str) -> str:
            """Check out different file types like excel, python, or text files."""
            if file_type == "excel":
                return "I cannot directly analyze Excel files. Please provide the data in text format."
            elif file_type == "python":
                return "I cannot directly analyze Python files. Please provide the code or output in text format."
            elif file_type == "text":
                return "I cannot directly analyze text files. Please provide the content in the question."
            return "I cannot analyze this type of file. Please provide the content in text format."

        def analyze_table(table_data: str, analysis_type: str) -> str:
            """Look at math tables and check properties like commutativity."""
            try:
                # Parse the table data
                rows = [row.split('|') for row in table_data.strip().split('\n')]
                if len(rows) < 2:
                    return "Invalid table format"
                
                # Extract elements and operation results
                elements = [e.strip() for e in rows[0][1:-1]]
                results = {}
                for row in rows[1:]:
                    if len(row) < 3:
                        continue
                    a = row[0].strip()
                    for i, b in enumerate(row[1:-1]):
                        if i < len(elements):
                            results[(a, elements[i])] = b.strip()
                
                if analysis_type == "commutative":
                    # Find non-commutative pairs
                    non_commutative = []
                    for a in elements:
                        for b in elements:
                            if a != b and (a, b) in results and (b, a) in results:
                                if results[(a, b)] != results[(b, a)]:
                                    non_commutative.extend([a, b])
                    return ",".join(sorted(set(non_commutative)))
                
                return "Analysis not implemented for this type"
            except Exception as e:
                return f"Error analyzing table: {str(e)}"

        def calculator(expression: str) -> str:
            """Do basic math calculations."""
            try:
                # Remove any whitespace
                expression = expression.replace(" ", "")
                # Evaluate the expression
                result = eval(expression)
                return str(result)
            except Exception as e:
                return f"Error evaluating expression: {str(e)}"

        return [
            Tool(
                name="search_web",
                func=lambda query, search_type="general": search_web(query, search_type),
                description="Search for info online. Good for facts, history, news. Use search_type: general, wikipedia, academic, or news."
            ),
            Tool(
                name="analyze_media",
                func=lambda media_url, media_type: analyze_media(media_url, media_type),
                description="Check out video or audio content. Use media_type: video or audio."
            ),
            Tool(
                name="analyze_file",
                func=lambda file_path, file_type: analyze_file(file_path, file_type),
                description="Look at files. Use file_type: excel, python, or text."
            ),
            Tool(
                name="analyze_table",
                func=lambda table_data, analysis_type: analyze_table(table_data, analysis_type),
                description="Check math tables. Use analysis_type: commutative or associative."
            ),
            Tool(
                name="calculator",
                func=calculator,
                description="Do math calculations."
            )
        ]
        
    def _setup_agent(self):
        """Set up the agent with tools and prompt."""
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You're an AI assistant tackling the GAIA benchmark. Keep answers concise and accurate.

Key points:
- Use available tools efficiently
- Break down complex questions
- Be direct and factual
- Admit when you can't answer

Tools:
- search_web: For general knowledge and facts
- analyze_media: For video/audio content
- analyze_file: For file analysis
- analyze_table: For math tables
- calculator: For calculations

Limits:
- No direct internet access
- No media analysis
- No external DB access
- No complex calculations
- No image/video analysis

Process:
1. Understand the question
2. Pick the right tool
3. Get the answer
4. Keep it simple"""),
            ("human", "{input}"),
            ("ai", "{agent_scratchpad}")
        ])

        agent = create_openai_functions_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=prompt
        )

        return AgentExecutor.from_agent_and_tools(
            agent=agent,
            tools=self.tools,
            verbose=True,
            max_iterations=self.max_iterations
        )
        
    def process_question(self, question: Dict[str, Any], file_content: Optional[bytes] = None) -> str:
        """Process a question and return the answer."""
        task_id = question.get("task_id", "unknown")
        question_text = question.get("question", "")
        
        # Log the full question for better visibility
        logger.info(f"Processing question {task_id}: {question_text}")
        print(f"\nQuestion: {question_text}\n")
        
        # Handle file if provided
        file_path = None
        if file_content:
            # Create a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as temp_file:
                temp_file.write(file_content)
                file_path = temp_file.name
            question_text += f"\n\nA file is associated with this question. It's available at: {file_path}"
        
        try:
            # Run the agent
            result = self.agent.invoke({"input": question_text})
            answer = result.get("output", "")
            
            # Clean up the answer to match the exact format expected
            answer = answer.strip()
            
            # Remove any explanatory text and keep only the direct answer
            if "here is" in answer.lower() or "here are" in answer.lower():
                # Split by newlines and take the last part that contains the actual answer
                parts = answer.split("\n")
                for part in reversed(parts):
                    if part.strip() and not any(phrase in part.lower() for phrase in ["here is", "here are", "the answer is", "the result is"]):
                        answer = part.strip()
                        break
            
            # Remove any quotes around the answer
            answer = answer.strip('"')
            
            # For list-type answers, ensure they're comma-separated without any additional text
            if "list" in question_text.lower() or "alphabetize" in question_text.lower():
                # Extract just the comma-separated items
                items = [item.strip() for item in answer.split(",")]
                answer = ", ".join(items)
            
            logger.info(f"Generated answer for task {task_id}: {answer}")
            
            return answer
        finally:
            # Clean up temporary file if created
            if file_path and os.path.exists(file_path):
                os.remove(file_path)
