import os
import json
import logging
from openai import OpenAI
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

class QuizAgent:
    def __init__(self, api_key: Optional[str] = None):
        self.client = OpenAI(
            
            api_key=api_key or os.environ.get("OPENAI_API_KEY"),
            base_url=os.environ.get("OPENAI_BASE_URL")
        )
        self.model = os.environ.get("OPENAI_MODEL", "gpt-4o")

    def analyze_task(self, question: str, html_content: str, current_url: str = "") -> Dict[str, Any]:
        """
        Analyzes the question and HTML content to decide on a plan.
        Returns a JSON object with the plan.
        """
        system_prompt = """
        You are an expert data analyst and web automation bot.
        Your goal is to solve a quiz question found on a webpage.
        
        You will be provided with:
        1. The question text.
        2. A snippet of the HTML content of the page (or a description of it).
        3. The URL of the page you are currently on.
        
        You need to decide what steps to take.
        Your available tools are:
        - `python_exec`: Execute Python code to scrape, download, parse, and analyze data.
        
        Output a JSON object with the following structure:
        {
            "thought": "Explanation of your reasoning",
            "code": "Python code to execute"
        }
        
        - Be complete and runnable.
        - MUST end with `print(final_answer)` to output the result.
        - Use libraries like `requests`, `pandas`, `bs4`, `lxml` as needed.
        - If downloading files, save them to the current directory.
        - CRITICAL: DO NOT submit the answer to the server. DO NOT use `requests.post` to submit the solution.
        - The system handles submission. You ONLY calculate the answer value.
        - IMPORTANT: If you need to scrape or download data, use the provided `Current URL` as the base. Do NOT guess `example.com`.
        - OUTPUT FORMAT: Print ONLY the raw answer value (e.g., `1234` or `my_secret_code`). DO NOT print a JSON object, dictionary, or the submission payload.
        - DEFENSIVE CODING: Always check if `soup.find(...)` returns an element before accessing `.text`. If not found, print "Element not found" to avoid crashing.
        """
        
        user_prompt = f"""
        Current URL: {current_url}
        Question: {question}
        
        HTML Context (truncated):
        {html_content[:4000]}
        
        Generate the Python code to solve this.
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                response_format={"type": "json_object"}
            )
            
            content = response.choices[0].message.content
            return json.loads(content)
        except Exception as e:
            logger.error(f"Error in analyze_task: {e}")
            return {"thought": "Error", "code": ""}

    def extract_answer(self, execution_output: str, question: str) -> Any:
        """
        Parses the execution output to find the final answer formatted for the quiz.
        """
        system_prompt = """
        You are a helper that extracts the final answer from a script's output.
        The user will provide the question and the output of the code that solved it.
        You need to format the answer as required by the quiz (e.g., number, string, JSON).
        
        CRITICAL: If the output contains a JSON object with keys like "correct", "reason", or "url", IGNORE IT. That is a server response, not the answer.
        Look for the calculated value printed by the script.
        
        Return ONLY the answer value in the correct format (JSON compatible).
        """
        
        user_prompt = f"""
        Question: {question}
        
        Code Output:
        {execution_output}
        
        What is the final answer?
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            )
            
            answer_str = response.choices[0].message.content.strip()
            # Try to parse as JSON if it looks like one, otherwise return string/number
            try:
                return json.loads(answer_str)
            except:
                return answer_str
        except Exception as e:
            logger.error(f"Error in extract_answer: {e}")
            return None

    def extract_submit_url_from_text(self, text: str) -> Optional[str]:
        """
        Asks the LLM to find the submission URL in the text.
        """
        system_prompt = "You are a helper that extracts the submission URL from text. Return ONLY the URL."
        user_prompt = f"Find the URL to POST the answer to in this text:\n\n{text[:4000]}"
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"Error in extract_submit_url_from_text: {e}")
            return None
