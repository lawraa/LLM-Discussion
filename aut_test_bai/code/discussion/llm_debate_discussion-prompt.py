import os
import json
import time
import random
from openai import OpenAI
from tqdm import tqdm

import datetime
import re
import argparse

client = OpenAI()
# openai.api_key = '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'

agents = 0  # Number of agents
rounds = 0  # Number of rounds

dataset_filename = "../../datasets/aut_10.json"
current_date = datetime.date.today().strftime("%m-%d_")
current_time = datetime.datetime.now()
formatted_time = current_time.strftime("%H:%M:%S")

base_output_dir = "../../results/discussion/llm_debate_result-prompt/history"
base_final_ans_dir = "../../results/discussion/llm_debate_result-prompt/final_ans"
base_init_ans_dir = "../../results/discussion/llm_debate_result-prompt/init_ans"

# system_content =  "You are an active and helpful member in this discussion. \
# You should persuade each other that your answers are creative by giving reasonable explanations, be critical to verify each answer to see if it is creative enough,\
# justify your own answers, integrate with others replies, coming up with ideas inspired by others, \
# remove answers that is not creative enough, merge similar ideas, and ask questions for further understandings.\n\n"

# shot_prompt =f"For example, you can analyze if the usage is really suitable for the object by asking what could be adjusted, or if which two are too similar, etc."

system_content = ""
shot_prompt = ""

def generate_filename(base_dir, base_filename, extension):
    filename = os.path.join(base_dir, f"{base_filename}{extension}")
    counter = 1
    while os.path.exists(filename):
        filename = os.path.join(base_dir, f"{base_filename}_{counter}{extension}")
        counter += 1
    return filename

def parsing_arg():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-a', '--agents', type=int, default=2, help='Number of agents')
    parser.add_argument('-r', '--rounds', type=int, default=2, help='Number of rounds')
    args = parser.parse_args()
    return args


def construct_message(agents, question, idx, is_last_round, object):
    prefix_string = "These are the solutions to the problem from other agents:\n"

    for agent in agents:
        agent_response = agent[idx]["content"]
        response = "One agent solution: ```{}```\n".format(agent_response)
        prefix_string += response

    if is_last_round:
        prefix_string += f"This is the last round of the discussion, please only present a list of the most creative uses of {object} as your final answers. \n\n"
    # else:
#         prefix_string += "In the discussion, you should persuade each other that your answers are creative by \
# giving reasonable explanations, justify your own answers or integrate with others replies, \
# coming up with ideas inspired by others, and ask questions for further understandings.\n\n"

    prefix_string += question
    return {"role": "user", "content": prefix_string}


def construct_assistant_message(completion):
    content = completion.choices[0].message.content
    return {"role": "assistant", "content": content}

def generate_answer(answer_context):
    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=answer_context,
            n=1)
    except Exception as e:
        print("Error:", e)
        time.sleep(10)
        return generate_answer(answer_context)

    return completion

def extract_uses(content):
    # Split the content into lines and remove the introductory sentence
    lines = content.split('\n')
    uses = [line.strip() for line in lines if line.strip() and re.match(r"^\d+\.", line)]

    # Remove the numbering from each use
    uses = [use[use.find('.') + 2:] for use in uses]
    return uses

if __name__ == "__main__":
    args = parsing_arg()
    agents = args.agents
    rounds = args.rounds

    question_idx = 5 # if u wanna change the start index

    with open(dataset_filename, "r") as file:
        data = json.load(file)

    for q in data["Task"][question_idx:]:
        problem_template = " ".join(q["problem"])
        response_dict = {}
        init_results = []
        final_results = []

        for example in tqdm(data["examples"]):
            current_date = datetime.date.today().strftime("%Y-%m-%d")
            base_filename = f"discussion_{current_date}_{agents}_{rounds}_q{question_idx+1}"
            output_filename = generate_filename(base_output_dir, base_filename, ".json")
            final_ans_filename = generate_filename(base_final_ans_dir, base_filename + "_final_results", ".json")
            init_ans_filename = generate_filename(base_init_ans_dir, base_filename + "_init_results", ".json")

            object = example["object"]
            question = problem_template.replace("{object}", object)
            print(f"Question{question_idx+1}: {question}")
            # print()

            initial_prompt = "Initiate a discussion with others to collectively complete the following task: " + question
            system_prompt = {"role": "system", "content": system_content}
            agent_contexts = [[ system_prompt, {"role": "user", "content": initial_prompt}] for _ in range(agents)]

            for round in range(rounds):
                print("-----------------------------------------Round", round)
                is_last_round = (round == rounds - 1)
                for i, agent_context in enumerate(agent_contexts):
                    if round != 0:
                        agent_contexts_other = agent_contexts[:i] + agent_contexts[i+1:]
                        # print(f"agent_contexts_other = {agent_contexts_other}")
                        message = construct_message(agent_contexts_other, question, 2 * round, is_last_round, object)
                        if round == 1:
                            message["content"] += shot_prompt
                        agent_context.append(message)

                    completion = generate_answer(agent_context)
                    assistant_message = construct_assistant_message(completion)
                    agent_context.append(assistant_message)
                    # print("Agent", i, "Response in Round", round, f"=\n", assistant_message)
                    
                    if round == 0:
                        uses_list = extract_uses(assistant_message['content'])
                        # print(f"uses_list = {uses_list}")

                        init_result = {"item": object, "uses": uses_list, "Agent": i}
                        init_results.append(init_result)
                    elif is_last_round:
                        uses_list = extract_uses(assistant_message['content'])
                        final_result = {"item": object, "uses": uses_list, "Agent": i}
                        final_results.append(final_result)

            response_dict[question] = (agent_contexts)
        
        with open(output_filename, "w") as outfile:
            json.dump(response_dict, outfile, indent=4)
        with open(init_ans_filename, "w") as outfile:
            json.dump(init_results, outfile, indent=4)
        with open(final_ans_filename, "w") as outfile:
            json.dump(final_results, outfile, indent=4)

        print("Discussion END!!!")
        print(f"output file at: {final_ans_filename}")
        question_idx += 1 # add the question index

# time python3 llm_debate_discussion-prompt.py -a 2 -r 6