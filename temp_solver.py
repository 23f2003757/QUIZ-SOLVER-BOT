json_payload = {
    "email": "your email",
    "secret": "your secret",
    "url": "https://tds-llm-analysis.s-anand.net/demo",
    "answer": "anything you want"
}

# Simply extracting the 'answer' field to print because that's the core requirement.
final_answer = json_payload['answer']
print(final_answer)