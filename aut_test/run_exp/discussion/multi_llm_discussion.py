import json
import time
import random
from openai import OpenAI
import datetime
import re
import argparse

client = OpenAI()
# openai.api_key = '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'

agents = 0  # Number of agents
rounds = 0  # Number of rounds

dataset_filename = "../../datasets/dataset_aut_test.json"
current_date = datetime.date.today().strftime("%m-%d_")
current_time = datetime.datetime.now()
formatted_time = current_time.strftime("%H:%M:%S")

# system_content =  "You are an active and helpful member in this discussion. \
# You should persuade each other that your answers are creative by giving reasonable explanations, be critical to verify each answer to see if it is creative enough,\
# justify your own answers, integrate with others replies, coming up with ideas inspired by others, \
# remove answers that is not creative enough, merge similar ideas, and ask questions for further understandings.\n\n"

# shot_prompt =f"For example, you can analyze if the usage is really suitable for the object by asking what could be adjusted, or if which two are too similar, etc."

system_content = ""
shot_prompt = ""
last_round_prompt = " last prompt "

#dealing with parsing arguements
def parsing_arg():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-a', '--agents', type=int, default=2, help='Number of agents')
    parser.add_argument('-r', '--rounds', type=int, default=2, help='Number of rounds')
    parser.add_argument('-m', '--models', nargs='+', help='List of class names to append to alphabet', required=True)
    args = parser.parse_args()
    return args


# construct the model list according to input `-m`
def create_model_list(models):
    llm_models = []
    for model in models:
        if model in model_map:
            llm_models.append(model_map[model]())
        else:
             raise ValueError(f"Model {model} is not recognized.")  # Raising an error
    return llm_models

def construct_prompt(idx, other_agents_contexts, question, is_last_round):
    prefix_string = "These are the solutions to the problem from other agents:\n"
    for other_agent_context in other_agents_contexts:
        other_agent_response = other_agent_context['output_list'][-1]
        response = "One agent solution: ```{}```\n".format(other_agent_response)
        prefix_string += response

    if is_last_round:
        prefix_string += last_round_prompt

    prefix_string += question

    return prefix_string

    return full_prompt

# LLM Class
class OpenAIModel:
    def __init__(self):
        self.agent_idx = 0
        print("initialize an OpenAI model")

    def generate_response(self, prompt, idx, history_record):  # Added 'self'
        response = idx
        print(f"response = {response}")
        print("generate_response")
        return response


    def construct_history(self, agent_idx, agents_contexts):  # Added 'self'
        # Construct history_record
        history_record
        '''
        for instance, GPT model should construct a history record like this:
        [
            {
                "role": "system",
                "content": "system_content"
            },
            {
                "role": "user",
                "content": agents_contexts[agent_idx]['input_list'][n]
            },
            {
                "role": "assistant",
                "content": agents_contexts[agent_idx]['output_list'][n]
            }
        ]
        '''

        print("construct_history")
        return history_record


# mapping arguements --> LLM Classes
model_map = {
    'OpenAI': OpenAIModel,
    # 'Llama2': Llama2,
    # 'Gemini': Gemini
}

if __name__ == "__main__":
    args = parsing_arg()
    # agents = args.agents
    rounds = args.rounds
    models = args.models
    agents = len(args.models)

    # output_filename = f"../../results/discussion/llm_debate_result/history/discussion_{current_date}{formatted_time}_{agents}_{rounds}.json"
    # final_ans_filename = f"../../results/discussion/llm_debate_result/final_ans/discussion_final_results_{current_date}{formatted_time}_{agents}_{rounds}.json"
    # init_ans_filename = f"../../results/discussion/llm_debate_result/init_ans/discussion_init_results_{current_date}{formatted_time}_{agents}_{rounds}.json"

    with open(dataset_filename, "r") as file:
        data = json.load(file)


    for example in data["examples"]:
        object = example["object"]
        problem_template = " ".join(data["Task"][0]["problem"])
        # question = problem_template.replace("{object}", object)
        question = "question"
        # initial_prompt = "initial prompt " + question
        initial_prompt = "initial prompt"
        # construct the LLMs list
        llm_models = create_model_list(models)
        agents_contexts = [{'input_list': [], 'output_list': [], 'agent_idx': -1} for _ in range(agents)]
        #for each agent, it has 1. all input prompts, 2. all output responses
        #agents_contexts['input_list'] =  all the history prompts(string) into certain agent
        #agents_contexts['output_list'] =  all the history responses(string) from certain agent
        for round in range(rounds):
            print("-----------------------------------------Round", round)
            is_last_round = (round == rounds - 1)
            is_first_round = (round == 0)

            for i in range(agents):

                other_agents_contexts = agents_contexts[:i] + agents_contexts[i+1:]

                if is_first_round:
                    prompt = initial_prompt
                    # prompt = i
                else:
                    prompt = construct_prompt(i,  other_agents_contexts, question, is_last_round)
                agent = llm_models[i] #agent = certain LLM Class
                agents_contexts[i]['agent_idx'] = i
                history_record = agent.construct_history(i, agents_contexts)
                response = agent.generate_response(prompt, i, history_record)
                agents_contexts[i]['input_list'].append(prompt)
                agents_contexts[i]['output_list'].append(response)

    print(f"agents_contexts = {agents_contexts}")

        

    
    # with open(output_filename, "w") as outfile:
    #     json.dump(response_dict, outfile, indent=4)

    # with open(init_ans_filename, "w") as outfile:
    #     json.dump(init_results, outfile, indent=4)

    # with open(final_ans_filename, "w") as outfile:
    #     json.dump(final_results, outfile, indent=4)
