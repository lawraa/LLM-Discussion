import google.generativeai as genai
from openai import OpenAI
import logging
import time
import os
from typing import List, Optional
from llama import Llama, Dialog
import subprocess
import torch


client = OpenAI()
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-pro')

def generate_response_gemini(message, temperature=1, top_p=1, seed=0):
    try: 
        response = model.generate_content(
            message,
            generation_config=genai.types.GenerationConfig(temperature=temperature),
            safety_settings=[
                {"category": "HARM_CATEGORY_HARASSMENT","threshold": "BLOCK_NONE",},
                {"category": "HARM_CATEGORY_HATE_SPEECH","threshold": "BLOCK_NONE",},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT","threshold": "BLOCK_NONE",},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT","threshold": "BLOCK_NONE",},
                ]
        )
        return response.text
    except Exception as e:
        logging.exception("Exception occurred during response generation: " + str(e))
        time.sleep(1)    


def generate_response_openai(messages, temperature=1, top_p=1, seed=0):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=temperature,
            top_p=top_p,
            seed=seed
        )
        result = response.choices[0].message.content
        return result
    except Exception as e:
        logging.exception("Exception occurred during response generation: " + str(e))
        time.sleep(1)



def generate_response_llama2_torchrun(
    message: str,
    ckpt_dir: str = "/tmp2/llama-2-7b-chat",
    tokenizer_path: str = "/home/chenlawrance/repo/LLM-Creativity/model/llama/tokenizer.model",
    temperature: float = 0.6,
    top_p: float = 0.9,
    max_seq_len: int = 2048,
    max_batch_size: int = 4):
    command = [
        "torchrun", "--nproc_per_node=1", "/home/chenlawrance/repo/LLM-Creativity/model_discuss/llama_chat_completion.py",
        "--ckpt_dir", ckpt_dir,
        "--tokenizer_path", tokenizer_path,
        "--max_seq_len", str(max_seq_len),
        "--max_batch_size", str(max_batch_size),
        "--temperature", str(temperature),
        "--top_p", str(top_p),
        "--message", message
    ]
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        output = result.stdout.strip()

        # Find the beginning of the generated response
        assistant_prefix = "> Assistant:"
        start_idx = output.find(assistant_prefix)
        if start_idx != -1:
            # Calculate the starting index of the actual response
            start_of_response = start_idx + len(assistant_prefix)
            # Extract and return the generated response part
            generated_response = output[start_of_response:].strip()
            return generated_response
        else:
            return "No response generated or unable to extract response."
    except subprocess.CalledProcessError as e:
        print(f"Error executing torchrun command: {e.stderr}")
        return "Unable to generate response due to an error."




message = "Give me some creative use of ring."

response_gemini = generate_response_gemini(message, temperature=1, top_p=1, seed=0)
print("Gemini Response ::: ", response_gemini,"\n")

response_openai = generate_response_openai([{"role": "user", "content": message}], temperature=1, top_p=1, seed=0)
print("OpenAI Response ::: ", response_openai,"\n")

response = generate_response_llama2_torchrun(message)
print("LLAMA2 Response with torchrun:::", response, "\n")
