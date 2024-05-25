import os
import re
import json
import argparse
from openai import OpenAI
import datetime
import sys
from pathlib import Path
from types import SimpleNamespace


client = OpenAI()
model = "gpt-3.5-turbo-0125"
prompt = " Please finalize and present a list of creative answers. Please list the final response in 1. ... 2. ... 3. ... and so on.\n\n"
current_time = datetime.datetime.now()
current_date = datetime.date.today().strftime("%Y-%m-%d")
formatted_time = current_time.strftime("%H-%M-%S")

def generate_response(prompt):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error in API call: {e}")
        return None

def extract_response(content):
        lines = content.split('\n')
        uses = [line.strip() for line in lines if line.strip() and re.match(r"^\d+\.", line)]
        uses = [use[use.find('.') + 2:] for use in uses]
        return uses

def save_conversation(filename, conversation_data):
        with open(filename, 'w') as file:
            json.dump(conversation_data, file, indent=4)
        print(f"Saved Conversation Data to {filename}")

def main(args):
    if args.role is not None:
        role_data_path = "Thinking_role_config.json"
        with open(role_data_path, "r") as f:
            role_data = json.load(f)
        agent_role = role_data[args.role-1]["agent_role"]
        agent_speciality = role_data[args.role-1]["agent_speciality"]
        agent_role_prompt = role_data[args.role-1]["agent_role_prompt"]
        print("Agent Role: ", agent_role, "Agent Speciality: ", agent_speciality, "Agent Role Prompt: ", agent_role_prompt)
        role_prompt = f"You are a {agent_role} whose specialty is {agent_speciality}. {agent_role_prompt} Remember to claim your role in the beginning of your response. "
    else: 
        role_prompt = ""

    with open(args.input, "r") as f:
        dataset = json.load(f)
    final_results = []
    count = 0
    
    if args.type == "AUT":
        amount_of_data = len(dataset['Examples'])
        for example in dataset['Examples']:
            count += 1
            print("Example", count, "\nObject: ", example['object'])
            object = example['object']
            problem_template = " ".join(dataset["Task"][0]["Problem"])
            question = problem_template.replace("{object}", object)
            question += prompt
            print("Input Question: ", question)
            response = generate_response(role_prompt + question)
            response_list = extract_response(response)
            final_result = {"item": object, "uses": response_list}
            final_results.append(final_result)
    elif args.type == "Scientific":
        amount_of_data = 0
        for task in dataset['Task']:
            amount_of_data += len(task['Example'])
            for example in task['Example']:
                count += 1
                print("Example", count, "\nQuestion: ", example)
                question_with_prompt = example + prompt
                print("Input Question: ", question_with_prompt)
                response = generate_response(role_prompt+question_with_prompt)
                response_list = extract_response(response)
                final_result = {"question": example, "answer": response_list}
                final_results.append(final_result)
    elif args.type == "Similarities" or args.type == "Instances":
        amount_of_data = len(dataset['Examples'])
        for example in dataset['Examples']:
            count += 1
            print("Example", count, "\nQuestion: ", example)
            question_with_prompt = example + prompt
            print("Input Question: ", question_with_prompt)
            response = generate_response(role_prompt+question_with_prompt)
            response_list = extract_response(response)
            final_result = {"question": example, "answer": response_list}
            final_results.append(final_result)
    
    if args.role is not None:
        output_role_name = agent_role.replace(" ", "")
        subtask = "roleplay"
    else:
        output_role_name = "None"
        subtask = "baseline"
    
    model_name = model.replace(".", "-")
    output_file_name = f"../../../Results/{args.type}/Output/single_agent/{args.type}_single_single_{subtask}_1_1_{model_name}_{output_role_name}_final_{current_date}-{formatted_time}_{amount_of_data}.json"
    save_conversation(output_file_name, final_results)

    return f"{args.type}_single_single_{subtask}_1_1_{model_name}_{output_role_name}_final_{current_date}-{formatted_time}_{amount_of_data}.json"
    # final_results will look something like this:
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run a single agent response.")
    parser.add_argument("-i", "--input", required=True, help="absolute input file path")
    parser.add_argument("-t", "--type", required=True, choices= ["AUT", "Scientific","Similarities", "Instances"], help="type of task")
    parser.add_argument("-e", "--eval_mode", action="store_true", default=False, help="Run in evaluation mode.")
    parser.add_argument("-r", "--role", type=int, choices=range(1, 11), default=None, help="Role of the agent (1-10).")
    args = parser.parse_args()
    discussion_output = main(args)
    if args.eval_mode:
        project_root = Path(__file__).resolve().parents[3]
        evaluation_path = project_root / 'Evaluation'
        sys.path.append(str(evaluation_path))
        # Now you can import auto_grade directly
        import json
        import os
        import csv
        import numpy as np
        from utils.openai_model import OpenAIModel
        from eval_functions.eval_criterion import evaluate_aut, evaluate_scientific, evaluate_wkct
        from eval_functions.pairwise_comparison import pairwise_judgement
        from automation_csv import calculate_mean_std, write_results_to_csv
        import logging
        from auto_grade_final import auto_grade

        #Call Evaluation
        input_file_name = discussion_output.split('.')[0]
        args = SimpleNamespace(
            version="3", 
            input_file=input_file_name, 
            type="sampling", 
            sample=3, 
            task=args.type, 
            output="y"
        )
        auto_grade(args)
