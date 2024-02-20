import json
import time
import random
from openai import OpenAI
import datetime
import re
import argparse

client = OpenAI()

#init
agent_num = 0  # Number of agents
round_num = 0  # Number of rounds

system_prompt =  "You are an active and helpful member in this discussion. \
You should persuade each other that your answers are creative by giving reasonable explanations, be critical to verify each answer to see if it is creative enough,\
justify your own answers, integrate with others replies, coming up with ideas inspired by others, \
remove answers that is not creative enough, merge similar ideas, and ask questions for further understandings.\n\n"
shot_prompt =f"For example, you can analyze if the usage is really suitable for the object by asking what could be adjusted, or if which two are too similar, etc."

dataset_filename = "../../datasets/dataset_aut_test.json"
current_date = datetime.date.today().strftime("%m-%d_")
current_time = datetime.datetime.now()
formatted_time = current_time.strftime("%H:%M:%S")

def parsing_arg():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-a', '--agent_num', type=int, default=2, help='Number of agents')
    parser.add_argument('-r', '--round_num', type=int, default=2, help='Number of rounds')
    args = parser.parse_args()
    return args


def construct_message(agent_idx, agent_contexts, question, content_idx, is_first_round, is_last_round, object):
    prefix_string = "These are the responses to the problem from other agents:\n"

    if not is_first_round:
        for agent in range(agent_idx + 1, agent_num):
            agent_response = agent_contexts[agent][content_idx]["content"]
            response = "One agent response: ```{}```\n".format(agent_response)
            prefix_string += response

    for agent in range(0, agent_idx):
        agent_response = agent_contexts[agent][content_idx]["content"]
        response = "One agent response: ```{}```\n".format(agent_response)
        prefix_string += response

    if is_last_round:
        prefix_string += f"This is the last round of the discussion, please only present a list of the most creative uses of {object} as your final answers. \n\n"

    prefix_string += question
    return prefix_string


def construct_assistant_message(completion):
    content = completion.choices[0].message.content
    return content

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
    agent_num = args.agent_num
    round_num = args.round_num

    output_filename = f"../results/discussion/conv_result/history/conv_discussion_{current_date}{formatted_time}_{agent_num}_{round_num}.json"
    final_ans_filename = f"../results/discussion/conv_result/final_ans/conv_discussion_final_{current_date}{formatted_time}_{agent_num}_{round_num}.json"
    init_ans_filename = f"../results/discussion/conv_result/init_ans/conv_discussion_init_{current_date}{formatted_time}_{agent_num}_{round_num}.json"

    response_dict = {}
    init_results = []
    final_results = []

    with open(dataset_filename, "r") as file:
        data = json.load(file)

    for example in data["examples"]:
        object = example["object"]
        problem_template = " ".join(data["Task"][0]["problem"])
        question = problem_template.replace("{object}", object)
        answer = example["object"]
        initial_prompt = "Initiate a discussion with others to collectively complete the following task: " + question
        agent_contexts = [[{"role": "system", "content": system_prompt}] for _ in range(agent_num)]

        for round in range (round_num):
            print(f"----------------------- ROUND {round} -----------------------")
            if round == 0:
                is_first_round = True
            else:
                is_first_round = False

            if round == (round_num - 1):
                is_last_round = True
            else:
                is_last_round = False

            for agent, agent_context in enumerate(agent_contexts):
                if round == 0 and agent == 0:
                    prompt_msg = initial_prompt
                elif round == 0 :
                    prompt_msg = construct_message(agent, agent_contexts, question, -1 , is_first_round, is_last_round, object) + shot_prompt
                else:
                    prompt_msg = construct_message(agent, agent_contexts, question, -1 , is_first_round, is_last_round, object)
                
                agent_context.append({"role": "user", "content": prompt_msg})
                completion = generate_answer(agent_context)
                assistant_message = construct_assistant_message(completion)

                agent_context.append({"role": "assistant", "content": assistant_message})

                if is_first_round:
                    uses_list = extract_uses(assistant_message)
                    print(f"uses_list = {uses_list}")
                    init_result = {"item": object, "uses": uses_list, "Agent": agent}
                    init_results.append(init_result)
                elif is_last_round:
                    uses_list = extract_uses(assistant_message)
                    final_result = {"item": object, "uses": uses_list, "Agent": agent}
                    final_results.append(final_result)
    
        response_dict[question] = (agent_contexts)
    
    with open(output_filename, "w") as outfile:
        json.dump(response_dict, outfile, indent=4)

    with open(init_ans_filename, "w") as outfile:
        json.dump(init_results, outfile, indent=4)

    with open(final_ans_filename, "w") as outfile:
        json.dump(final_results, outfile, indent=4)
