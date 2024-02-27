import json
import time
import datetime
import re
import argparse

# Assuming OpenAI and other necessary libraries are installed
from openai import OpenAI
import google.generativeai as genai
import os
import logging
import subprocess



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

class Agent:
    def generate_answer(self, answer_context):
        raise NotImplementedError("This method should be implemented by subclasses.")
    def construct_assistant_message(self, prompt):
        raise NotImplementedError("This method should be implemented by subclasses.")
    def construct_user_message(self, prompt):
        raise NotImplementedError("This method should be implemented by subclasses.")

class OpenAIAgent(Agent):
    def __init__(self, model_name):
        self.model_name = model_name
        self.client = OpenAI()

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
    def __init__(self, model_name):
        self.model_name = model_name
        genai.configure(api_key=os.environ["GEMINI_API_KEY"]) # ~/.bashrc save : export GEMINI_API_KEY="YOUR_API" 
        self.model = genai.GenerativeModel(self.model_name)

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

    def construct_assistant_message(self, content):
        response = {"role": "assistant", "parts": [content]}
        return response
    
    def construct_user_message(self, content):
        response = {"role": "user", "parts": [content]}
        return response
        
class Llama2Agent(Agent):
    def __init__(self, ckpt_dir, tokenizer_path):
        self.ckpt_dir = ckpt_dir
        self.tokenizer_path = tokenizer_path

    def generate_answer(self, answer_context, temperature=0.6, top_p=0.9, max_seq_len=2048, max_batch_size=4): # return pure text
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

class Discussion:
    def __init__(self, agents_config, dataset_file, rounds):
        self.agents = self.initialize_agents(agents_config)
        self.dataset_file = dataset_file
        self.rounds = rounds
        self.chat_history = {agent: [] for agent in self.agents}

    def initialize_agents(self, agents_config):
        agents = []
        for config in agents_config:
            if config['type'] == 'openai':
                agents.append(OpenAIAgent(model_name=config['model_name']))
            elif config['type'] == 'gemini':
                agents.append(GeminiAgent(model_name=config['model_name']))
            elif config['type'] == 'llama2':
                agents.append(Llama2Agent(ckpt_dir=config['ckpt_dir'], tokenizer_path=config['tokenizer_path']))
            else:
                raise ValueError(f"Unsupported agent type: {config['type']}")
        print(f"Initialized {len(agents)} agents.")
        print("The agents are: ", agents)
        return agents
    
    def run(self):
        with open(self.dataset_file, 'r') as f:
            dataset = json.load(f)
        
        all_responses = []
        for example in dataset['examples']:
            # --------------->>>> set the system content
            object = example['object']
            problem_template = " ".join(dataset["Task"][0]["problem"])
            question = problem_template.replace("{object}", object)
            initial_prompt = "Initiate a discussion with others to collectively complete the following task: " + question
            # ------------------------------------------

            entire_conversation = []
            most_recent_responses = []
            for round in range(self.rounds):
                is_last_round = (round == self.rounds - 1)
                round_responses = []
                print(f"Round {round + 1}: Discussion on {object}")
                for agent in self.agents:
                    if round == 0:
                        formatted_initial_prompt = agent.construct_user_message(initial_prompt)
                        self.chat_history[agent].append(formatted_initial_prompt)
                        print("formatted_initial_prompt: ", formatted_initial_prompt, "\n")
                        print(f"Agent {agent} chat history: {self.chat_history[agent]}","\n")
                        response = agent.generate_answer(self.chat_history[agent])
                    else:
                        combined_prompt = self.construct_response(question ,most_recent_responses, agent, object, is_last_round)
                        formatted_combined_prompt = agent.construct_user_message(combined_prompt)
                        self.chat_history[agent].append(formatted_combined_prompt)
                        response = agent.generate_answer(self.chat_history[agent])

                    formatted_response = agent.construct_assistant_message(response)
                    self.chat_history[agent].append(formatted_response)  # Update the agent's chat history
                    round_responses.append({"agent": agent, "response": formatted_response})
                    
                most_recent_responses = round_responses
                entire_conversation.extend(round_responses)
            all_responses.append(entire_conversation)
        self.save_conversation("conversation_log.json", all_responses)
    
    def save_conversation(self, filename, conversation_data):
        with open(filename, 'w') as file:
            json.dump(conversation_data, file, indent=4)


    def construct_response(self, question, most_recent_responses, current_agent, object, is_last_round):
        prefix_string = "These are the solutions to the problem from other agents:\n"
        for response_info in most_recent_responses:
            if response_info["agent"] != current_agent:
                if isinstance(response_info["agent"], GeminiAgent):
                    # GeminiAgent uses 'parts' for storing response content
                    response_content = "".join(response_info["response"]["parts"])
                else:
                    # Both OpenAIAgent and Llama2Agent use 'content' directly
                    response_content = response_info["response"]["content"]

                response = f"One agent solution: ```{response_content}```\n"
                prefix_string += response
        if is_last_round:
            prefix_string += f"This is the last round of the discussion, please only present a list of the most creative uses of {object} as your final answers. \n\n"
        prefix_string += question
        return prefix_string
    
    @staticmethod
    def load_config(config_path):
        with open(config_path, 'r') as f:
            return json.load(f)


def main():
    parser = argparse.ArgumentParser(description="Orchestrate a discussion with multiple AI agents.")
    parser.add_argument("-c", "--config", required=True, help="Path to the configuration file for agents.")
    parser.add_argument("-d", "--dataset", required=True, help="Path to the dataset file.")
    parser.add_argument("-r", "--rounds", type=int, default=3, help="Number of rounds in the discussion.")
    args = parser.parse_args()

    agents_config = Discussion.load_config(args.config)
    discussion_runner = Discussion(agents_config, args.dataset, args.rounds)
    discussion_runner.run()
    

if __name__ == "__main__":
    main()
