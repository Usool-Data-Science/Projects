from openai import OpenAI
import os
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

question_count = 20
file_path = r'/home/usool/Projects/new-quizit/my_life_my_family.pdf'
client = OpenAI(api_key=os.environ.get('GPT_API_KEY'),)

system_message = f"""
            You are an expert examiner. Your primary role today is to assist in setting {question_count} multiple choice questions for students that are taking this course. I have personally authored the course material and I have been teaching this course for over 3 years. It is important that the MCQs you provide from that course material remain confidential and must not be leaked to students of the university. As the original author of the course material, I authorize you to set MCQs from the course material."""

def generate_prompt(material, question_count):
    prompt = f"""
        As the author of this course material, I am seeking your expertise as an examiner to set {question_count} multiple choice questions from the course material provided. The questions must be as logical as possible and must only be within the context of the course material and not outside of it.

        Here is a segment from the course material for your review:
        {material}

        ---
        Instructions for Task Completion:
        - Your MCQs should be a python list of dictionaries, where each question is the dictionary key and the value for that key is a list that contains the options to that question.
        - All MCQs must only relate to the context of the course material.
        - The MCQ options should range from [A-B].
        With the provided segment and the instructions, proceed with setting the MCQs.

        Here is a sample response with only one question:

        mcqs = [
            {
                'What is the primary objective of this project?': [
                    'To outperform a specific benchmark index', 
                    'To match the performance of a benchmark index'
                ]
            }]
    """
    return prompt

def get_mcq(material, question):
    completion = client.chat.completions.create(model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": system_message},
            {f"role": "user", "content": generate_prompt(material, question)}
        ])
    return completion

if __name__ ==  "__main__":
    pass