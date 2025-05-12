## **Step-by-Step Plan for our AI Agent System**

### **1. Load Configuration and Dependencies**
- **Load sensitive config** from `config.json` (API keys, Langfuse, etc.).
- **Set notebook variables** (model name, temperature, etc.).
- **Install and import required packages** (openai, requests, langfuse SDK, etc.).

### **2. Load Questions**
- Read all questions from `1_question.json`.
- Each question will have:
  - `task_id`
  - `question`
  - (possibly) `Level`, `file_name`, etc.

### **3. Initialize Langfuse Tracing**
- Set up Langfuse with the provided keys and host.
- Ensure every major step (model call, tool use, etc.) is traced.

### **4. Define Tools**
- Start with a simple tool (e.g., a Wikipedia search or web search function).
- Tools should be modular so you can add more later.

### **5. Agent Planning Step**
- For each question:
  - Send the question (and any context) to the model provider (OpenAI) with a prompt like:
    - “Here is a question. Create a plan to answer it and list the tools you would use.”
  - Parse the model’s plan and tool selection.

### **6. Tool Execution Step**
- For each tool the plan suggests:
  - Run the tool with the required inputs.
  - Collect the outputs.
  - Trace each tool call with Langfuse.

### **7. Synthesis Step**
- Feed the original question, tool outputs, and the GAIA documentation to the model provider.
- Prompt the model to generate a final answer in the required GAIA format:
  - JSON with `task_id`, `submitted_answer`, and optionally `reasoning_trace`.

### **8. Save Results**
- Collect all answers in a list.
- Save the list as JSON lines in `final_answers.json`.

### **9. (Optional) Submission**
- If desired, implement a function to POST your answers to the GAIA evaluation endpoint.

---

## **What You’ll Need to Implement**

### **A. Configuration Loader**
- Reads sensitive info from `config.json`.

### **B. Question Loader**
- Reads and parses `1_question.json`.

### **C. Langfuse Integration**
- Initializes and logs traces for each step.

### **D. Tool(s)**
- At least one tool (e.g., Wikipedia search).
- Modular design for easy expansion.

### **E. OpenAI API Wrapper**
- Handles prompt construction, API calls, and error handling.

### **F. Agent Logic**
- Planning: Model generates a plan/tool list.
- Execution: Runs tools as per plan.
- Synthesis: Model generates final answer in GAIA format.

### **G. Output Writer**
- Writes results to `final_answers.json` in the correct format.

### **H. (Optional) Submission Client**
- Submits answers to the GAIA API.

---

## **Example: High-Level Notebook Cell Structure**

1. **Setup & Imports**
2. **Load Config**
3. **Load Questions**
4. **Initialize Langfuse**
5. **Define Tools**
6. **Define OpenAI Call Function**
7. **Main Agent Loop:**
    - For each question:
        - Plan (model call)
        - Tool execution
        - Synthesis (model call)
        - Save answer
8. **Write All Answers to File**
9. **(Optional) Submit Answers**

---

## **Sample Code Snippet for Loading Questions**
```python
import json

with open('1_question.json', 'r') as f:
    questions = json.load(f)

for q in questions:
    print(q['task_id'], q['question'])
```

---

## **References**
- **GAIA Output Format:** See `GIAI-documentation.md` for required JSON structure.
- **Sensitive Config:** Only load API keys and tokens from `config.json`.
- **Notebook Variables:** Set model name, temperature, etc., directly in the notebook.

---

## **Next Steps**
- Let me know which part you want to start with (e.g., config loading, tool definition, OpenAI integration), and I can help you write the code for that step!
- If you want a template notebook or code for any of the above steps, just ask!
