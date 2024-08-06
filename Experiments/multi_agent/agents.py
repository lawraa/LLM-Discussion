import json
import os
import logging
import subprocess
import time
from openai import OpenAI
import google.generativeai as genai

def generate_response_llama2_torchrun(
    message,
    ckpt_dir: str = "/tmp2/llama-2-7b-chat",
    tokenizer_path: str = "/home/chenlawrance/repo/LLM-Creativity/model/tokenizer.model",
    temperature: float = 0.6,
    top_p: float = 0.9,
    max_seq_len: int = 2048,
    max_batch_size: int = 4):
    message_json = json.dumps(message)  # Serialize the message to a JSON string
    command = [
        "torchrun", "--nproc_per_node=1", "/home/chenlawrance/repo/LLM-Creativity/llama_model/llama_chat_completion.py",
        "--ckpt_dir", ckpt_dir,
        "--tokenizer_path", tokenizer_path,
        "--max_seq_len", str(max_seq_len),
        "--max_batch_size", str(max_batch_size),
        "--temperature", str(temperature),
        "--top_p", str(top_p),
        "--message", message_json
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

class Agent:
    def generate_answer(self, answer_context):
        raise NotImplementedError("This method should be implemented by subclasses.")
    def construct_assistant_message(self, prompt):
        raise NotImplementedError("This method should be implemented by subclasses.")
    def construct_user_message(self, prompt):
        raise NotImplementedError("This method should be implemented by subclasses.")

class OpenAIAgent(Agent):
    def __init__(self, model_name, agent_name, agent_role, agent_speciality, agent_role_prompt, speaking_rate, missing_history = []):
        self.model_name = model_name
        self.client = OpenAI()
        self.agent_name = agent_name
        self.agent_role = agent_role
        self.agent_speciality = agent_speciality
        self.agent_role_prompt = agent_role_prompt
        self.speaking_rate = speaking_rate
        self.missing_history = missing_history
        
    def generate_answer(self, answer_context, temperature=1):
        try:
            completion = self.client.chat.completions.create(
                model=self.model_name,
                messages=answer_context,
                n=1)
            result = completion.choices[0].message.content
            # for pure text -> return completion.choices[0].message.content
            return result
        except Exception as e:
            print(f"Error with model {self.model_name}: {e}")
            time.sleep(10)
            return self.generate_answer(answer_context)

    def construct_assistant_message(self, content):
        return {"role": "assistant", "content": content}
    
    def construct_user_message(self, content):
        return {"role": "user", "content": content}
    
class GeminiAgent(Agent):
    def __init__(self, model_name, agent_name, agent_role, agent_speciality, agent_role_prompt, speaking_rate):
        self.model_name = model_name
        genai.configure(api_key=os.environ["GEMINI_API_KEY"]) # ~/.bashrc save : export GEMINI_API_KEY="YOUR_API" 
        self.model = genai.GenerativeModel(self.model_name)
        self.agent_name = agent_name
        self.agent_role = agent_role
        self.agent_speciality = agent_speciality
        self.agent_role_prompt = agent_role_prompt
        self.speaking_rate = speaking_rate

    def generate_answer(self, answer_context,temperature= 1.0):
        try: 
            response = self.model.generate_content(
                answer_context,
                generation_config=genai.types.GenerationConfig(temperature=temperature),
                safety_settings=[
                    {"category": "HARM_CATEGORY_HARASSMENT","threshold": "BLOCK_NONE",},
                    {"category": "HARM_CATEGORY_HATE_SPEECH","threshold": "BLOCK_NONE",},
                    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT","threshold": "BLOCK_NONE",},
                    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT","threshold": "BLOCK_NONE",},
                    ]
            )
            # for pure text -> return response.text
            # return response.candidates[0].content
            return response.text
        except Exception as e:
            logging.exception("Exception occurred during response generation: " + str(e))
            time.sleep(1)
            return self.generate_answer(answer_context)
        
    def construct_assistant_message(self, content):
        response = {"role": "model", "parts": [content]}
        return response
    
    def construct_user_message(self, content):
        response = {"role": "user", "parts": [content]}
        return response
        
class Llama2Agent(Agent):
    def __init__(self, ckpt_dir, tokenizer_path, agent_name):
        self.ckpt_dir = ckpt_dir
        self.tokenizer_path = tokenizer_path
        self.agent_name = agent_name

    def generate_answer(self, answer_context, temperature=0.6, top_p=0.9, max_seq_len=100000, max_batch_size=4): # return pure text
        return generate_response_llama2_torchrun(
            message=answer_context,
            ckpt_dir=self.ckpt_dir,
            tokenizer_path=self.tokenizer_path,
            temperature=temperature,
            top_p=top_p,
            max_seq_len=max_seq_len,
            max_batch_size=max_batch_size
        )
    
    def construct_assistant_message(self, content):
        return {"role": "assistant", "content": content}
    
    def construct_user_message(self, content):
        return {"role": "user", "content": content}