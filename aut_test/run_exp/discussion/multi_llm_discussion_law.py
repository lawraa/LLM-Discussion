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
import datetime

current_date = datetime.date.today().strftime("%m-%d_")
current_time = datetime.datetime.now()
formatted_time = current_time.strftime("%H:%M:%S")



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
    def __init__(self, model_name, agent_name):
        self.model_name = model_name
        self.client = OpenAI()
        self.agent_name = agent_name

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
    def __init__(self, model_name, agent_name):
        self.model_name = model_name
        genai.configure(api_key=os.environ["GEMINI_API_KEY"]) # ~/.bashrc save : export GEMINI_API_KEY="YOUR_API" 
        self.model = genai.GenerativeModel(self.model_name)
        self.agent_name = agent_name

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
        response = {"role": "assistant", "parts": [content]}
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

class Discussion:
    def __init__(self, agents_config, dataset_file, rounds):
        self.agents = self.initialize_agents(agents_config)
        self.dataset_file = dataset_file
        self.rounds = rounds

    def initialize_agents(self, agents_config):
        agents = []
        for config in agents_config:
            if config['type'] == 'openai':
                agents.append(OpenAIAgent(model_name=config['model_name'], agent_name = config['agent_name']))
            elif config['type'] == 'gemini':
                agents.append(GeminiAgent(model_name=config['model_name'], agent_name = config['agent_name']))
            elif config['type'] == 'llama2':
                agents.append(Llama2Agent(ckpt_dir=config['ckpt_dir'], tokenizer_path=config['tokenizer_path'], agent_name = config['agent_name']))
            else:
                raise ValueError(f"Unsupported agent type: {config['type']}")
        print(f"Initialized {len(agents)} agents.")
        print("The agents are: ", agents)
        return agents
    
    def extract_uses(self, content):
        lines = content.split('\n')
        uses = [line.strip() for line in lines if line.strip() and re.match(r"^\d+\.", line)]
        uses = [use[use.find('.') + 2:] for use in uses]
        return uses
    
    def run(self):
        with open(self.dataset_file, 'r') as f:
            dataset = json.load(f)
        all_responses = {}
        init_results = []
        final_results = []
        for example in dataset['examples']:
            chat_history = {agent.agent_name: [] for agent in self.agents}
            print("initial chat_history: ", chat_history, "\n")
            # --------------->>>> set the system content
            object = example['object']
            problem_template = " ".join(dataset["Task"][0]["problem"])
            question = problem_template.replace("{object}", object)
            initial_prompt = "Initiate a discussion with others to collectively complete the following task: " + question
            # ------------------------------------------
            most_recent_responses = {}
            for round in range(self.rounds):
                is_last_round = (round == self.rounds - 1)
                is_first_round = (round == 0)
                round_responses = {agent.agent_name: [] for agent in self.agents}
                print(f"Round {round + 1}: Discussion on {object}")
                for agent in self.agents:
                    if is_first_round:
                        formatted_initial_prompt = agent.construct_user_message(initial_prompt)
                        chat_history[agent.agent_name].append(formatted_initial_prompt)
                        print("formatted_initial_prompt: ", formatted_initial_prompt, "\n")
                        print(f"Agent {agent.agent_name} chat history: {chat_history[agent.agent_name]}","\n")
                        response = agent.generate_answer(chat_history[agent.agent_name])

                        # Save the initial response for the agent
                        uses_list = self.extract_uses(response)
                        print(f"uses_list = {uses_list}")
                        init_result = {"item": object, "uses": uses_list, "Agent": agent.agent_name}
                        init_results.append(init_result)
                    else:
                        print("most_recent_responses: ", most_recent_responses)
                        combined_prompt = self.construct_response(question, most_recent_responses, agent, object, is_last_round)
                        formatted_combined_prompt = agent.construct_user_message(combined_prompt)
                        chat_history[agent.agent_name].append(formatted_combined_prompt)
                        print("INPUT TO GENERATE: ", chat_history[agent.agent_name], "\n")
                        response = agent.generate_answer(chat_history[agent.agent_name])
                        print("OUTPUT FROM GENERATE: ", response, "\n")
                        if is_last_round:
                            uses_list = self.extract_uses(response)
                            print(f"uses_list = {uses_list}")
                            final_result = {"item": object, "uses": uses_list, "Agent": agent.agent_name}
                            final_results.append(final_result)

                    formatted_response = agent.construct_assistant_message(response)
                    chat_history[agent.agent_name].append(formatted_response)  # Update the agent's chat history
                    round_responses[agent.agent_name].append(formatted_response)
                most_recent_responses = round_responses
            all_responses[question] = chat_history
        output_filename = f"../../results/discussion/llm_debate_result/history/discussion_{current_date}{formatted_time}_{len(self.agents)}_{self.rounds}.json"
        final_ans_filename = f"../../results/discussion/llm_debate_result/final_ans/discussion_final_{current_date}{formatted_time}_{len(self.agents)}_{self.rounds}.json"
        init_ans_filename = f"../../results/discussion/llm_debate_result/init_ans/discussion_init_{current_date}{formatted_time}_{len(self.agents)}_{self.rounds}.json"
        self.save_conversation(output_filename, all_responses)

        self.save_conversation(final_ans_filename, final_results)
        self.save_conversation(init_ans_filename, init_results)
    
    def save_conversation(self, filename, conversation_data):
        with open(filename, 'w') as file:
            json.dump(conversation_data, file, indent=4)
        print(f"Saved data to {filename}")

    def construct_response(self, question, most_recent_responses, current_agent, object, is_last_round):
        prefix_string = "These are the solutions to the problem from other agents:\n"
        for agent_name, responses in most_recent_responses.items():
            if agent_name == current_agent.agent_name:
                continue
            print("-----------------------------------------")
            print(agent_name)
            print(responses)
            if responses and 'parts' in responses[-1]:
                print("IN GEMINI")
                response_content = responses[-1]['parts'][0]
            else:
                print("IN GPT")
                response_content = responses[-1]['content']

            other_agent_response = f"One agent solution: ```{response_content}```\n"
            prefix_string += other_agent_response

        if is_last_round:
            prefix_string += f"This is the last round of the discussion, please only present a list of the most creative uses of {object} as your final answers. \n\n"
        else:
            discussion_prompt =  "You are an active and helpful member in this discussion. \
You should persuade each other that your answers are creative by giving reasonable explanations, be critical to verify each answer to see if it is creative enough,\
justify your own answers, integrate with others replies, coming up with ideas inspired by others, \
remove answers that is not creative enough, merge similar ideas, and ask questions for further understandings.\n\n"
            prefix_string += discussion_prompt
        prefix_string += question
        print("Constructed Response", prefix_string)
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
