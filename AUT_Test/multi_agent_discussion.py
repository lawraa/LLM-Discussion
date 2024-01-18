import json
import time
import random
from openai import OpenAI
import datetime

client = OpenAI()
# openai.api_key = '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'

agents = 2  # Number of agents
rounds = 10  # Number of rounds

dataset_filename = "dataset_aut_test.json"
current_date = datetime.date.today().strftime("%m-%d_")
current_time = datetime.datetime.now()
formatted_time = current_time.strftime("%H:%M:%S")
output_filename = f"multiagent_discussion_{agents}_{rounds}_{current_date}{formatted_time}.json"

def construct_message(agents, question, idx, is_last_round):
    prefix_string = "These are the solutions to the problem from other agents:\n"

    for agent in agents:
        agent_response = agent[idx]["content"]
        response = "One agent solution: ```{}```\n".format(agent_response)
        prefix_string += response

    if is_last_round:
        prefix_string += "This is the last round of the discussion, please only present the final answers. \n\n"
    else:
        prefix_string += "In the discussion, you should persuade each other that your answers are creative by\
        giving reasonable explanations, justify your own answers or integrate with others replies,\
        coming up with ideas inspired by others, and ask questions for further understandings.\n\n"

    prefix_string += question
    return {"role": "user", "content": prefix_string}


def construct_assistant_message(completion):
    content = completion.choices[0].message.content
    return {"role": "assistant", "content": content}

def generate_answer(answer_context):
    try:
        completion = client.chat.completions.create(model="gpt-3.5-turbo-1106",
        messages=answer_context,
        n=1)
    except Exception as e:
        print("Error:", e)
        time.sleep(10)
        return generate_answer(answer_context)

    return completion

if __name__ == "__main__":
    with open(dataset_filename, "r") as file:
        data = json.load(file)

    response_dict = {}

    for example in data["examples"]:
        object = example["input"]
        question = f"what are some creative use for {object}? The goal is to come up with creative ideas,\
which are ideas that strike people as clever, unusual, interesting, uncommon, humaorous, innovative, or different.\
List the most 10 creative uses for {object}."
        answer = example["target"]
        initial_prompt = "Initiate a discussion with others to collectively complete the following task: " + question
        agent_contexts = [[{"role": "user", "content": initial_prompt}] for _ in range(agents)]

        for round in range(rounds):
            print("-----------------------------------------Round", round)
            is_last_round = (round == rounds - 1)
            for i, agent_context in enumerate(agent_contexts):
                if round != 0:
                    agent_contexts_other = agent_contexts[:i] + agent_contexts[i+1:]
                    message = construct_message(agent_contexts_other, question, 2 * round - 1, is_last_round)
                    agent_context.append(message)

                completion = generate_answer(agent_context)
                assistant_message = construct_assistant_message(completion)
                agent_context.append(assistant_message)
                print("Agent", i, "Response in Round", round, f"=\n", assistant_message)

        response_dict[question] = (agent_contexts, answer)

    
    with open(output_filename, "w") as outfile:
        json.dump(response_dict, outfile, indent=4)
