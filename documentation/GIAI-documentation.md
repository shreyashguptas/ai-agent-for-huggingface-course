## GAIA Standard for Submissions - Hugging Face AI Agents Course (Unit 4)

The GAIA standard defines how you must format and submit your final project answers for evaluation in Unit 4 of the Hugging Face AI Agents course. Below is a concise reference you can include in your documentation.

---

### **What is the GAIA Standard?**

GAIA is a benchmark designed to evaluate advanced language models (LLMs) with enhanced capabilities, such as tool use, efficient prompting, and external information access. For this course, you will use a subset of the GAIA benchmark questions to evaluate your agent’s performance. Your agent must achieve at least a 30% score on the benchmark to earn the course certificate.

---

### **Submission Format and Process**

- **Submission Format:**
  All answers must be submitted as JSON lines, where each line contains:
  - `task_id`: The unique identifier for the question.
  - `submitted_answer`: The answer produced by your agent.
  - `reasoning_trace` (optional): An explanation of how the answer was reached.

  **Example:**
  ```json
  {
    "task_id": "example_task_001",
    "submitted_answer": "42",
    "reasoning_trace": "The agent calculated the answer using the provided data."
  }
  ```
  Only `task_id` and `submitted_answer` are required; `reasoning_trace` is optional.

- **Evaluation:**
  - Answers are evaluated using an **EXACT MATCH** to the ground truth.
  - Do **not** include extra text such as “FINAL ANSWER” in your submission-just the answer itself.
  - The leaderboard will display your score as the percentage of correct answers.

- **Submission Components:**
  When submitting, you must provide:
  - **Username:** Your Hugging Face username.
  - **Code Link:** URL to your public Hugging Face Space code (for verification).
  - **Answers:** The list of your agent’s responses in the required format.

- **API Endpoints:**
  - `GET /questions`: Retrieve all evaluation questions.
  - `GET /random-question`: Fetch a random question.
  - `GET /files/{task_id}`: Download files for specific tasks.
  - `POST /submit`: Submit your answers for scoring and leaderboard update.

---

### **Key Points to Remember**

- Use the provided template as a starting point, but you are encouraged to modify and personalize it.
- Keep your Hugging Face Space public if you want your score to appear on the leaderboard.
- Submissions without a public code link may be reviewed or removed from the leaderboard.
- The leaderboard and evaluation are for educational purposes and community engagement.
