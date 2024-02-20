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

    output_filename = f"../../results/discussion/llm_debate_result/history/discussion_{current_date}{formatted_time}_{agents}_{rounds}.json"
    final_ans_filename = f"../../results/discussion/llm_debate_result/final_ans/discussion_final_results_{current_date}{formatted_time}_{agents}_{rounds}.json"
    init_ans_filename = f"../../results/discussion/llm_debate_result/init_ans/discussion_init_results_{current_date}{formatted_time}_{agents}_{rounds}.json"

    with open(dataset_filename, "r") as file:
        data = json.load(file)

    response_dict = {}
    init_results = []
    final_results = []
    for example in data["examples"]:
        object = example["object"]
        problem_template = " ".join(data["Task"][0]["problem"])
        question = problem_template.replace("{object}", object)
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
                    print(f"uses_list = {uses_list}")
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
    print(f"output file at: {output_filename}")
