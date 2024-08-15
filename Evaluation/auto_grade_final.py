import argparse
import json
import os
from pathlib import Path
from utils.openai_model import OpenAIModel
from eval_functions.eval_criterion import evaluate_aut, evaluate_scientific, evaluate_wkct
import logging
from automation_csv import calculate_mean_std, write_results_to_csv

TASK_PATHS = {
    "AUT": "Results/AUT/Output",
    "Scientific": "Results/Scientific/Output",
    "Instances": "Results/Instances/Output",
    "Similarities": "Results/Similarities/Output",
}

def ensure_folder_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Created directory: {path}")

def auto_grade(args):
    print("AUTO GRADE STARTED, Input_file: ", args.input_file)

    # OPENAI KEY
    api_key = os.getenv("OPENAI_API_KEY")
    version = "gpt-4-0125-preview" if args.version == "4" else "gpt-3.5-turbo-0125"
    print(f"Using GPT Version {version}, Input: {args.version}")

    # SETUP CACHE AND MODEL
    cache_file_name = f"cache_{args.version}.pickle"
    model = OpenAIModel(cache_file_name, version, api_key)

    # This is for assign the input folder
    print(f"{args.input_file.split('_')[1]}_agent")

    task_folder = TASK_PATHS[args.task]
    input_file_path = os.path.join(Path(__file__).parent, '..', task_folder, f"{args.input_file.split('_')[1]}_agent", f"{args.input_file}.json")
    
    ensure_folder_exists(os.path.dirname(input_file_path))

    with open(input_file_path, "r") as file:
        responses = json.load(file)
    
    total_results = []
    sampling_criteria = ["originality", "elaboration"]
    evaluation_criteria = ["fluency", "flexibility"]
    selected_criteria = evaluation_criteria + sampling_criteria 

    if args.task == "AUT":
        for response_obj in responses:
            item = response_obj['item']
            uses = response_obj.get('uses', [])
            item_results = {"item": item}
            if not uses:  # Check if 'uses' is empty
                for criterion in selected_criteria:
                    responses = [{"response": "No uses provided", "score": 0}]
                    item_results[criterion] = responses
                    log_score = {f"average_{criterion}": 0}
                    item_results[criterion].append(log_score)
            else:
                for criterion in evaluation_criteria:
                    result = evaluate_aut(model, response_obj, criterion, args.type, args.sample)
                    item_results[criterion] = [result]
                    model.save_cache()
                for criterion in sampling_criteria:
                    total = []
                    for use in uses:
                        result = evaluate_aut(model, {"item": item, "uses": [use]}, criterion, args.type, 1)
                        total.append(result)
                        print(f"Item: {item}, Use: {use}, {criterion.capitalize()} Score: {result['average_score']}")
                    item_results[criterion] = total
                    model.save_cache()
                for criterion in evaluation_criteria:
                    avg_score = sum(res['average_score'] for res in item_results[criterion]) / len(item_results[criterion])
                    log_score = {f"average_{criterion}": avg_score}
                    item_results[criterion].append(log_score)
                for criterion in sampling_criteria:
                    avg_score = sum(res['average_score'] for res in item_results[criterion]) / len(item_results[criterion])
                    log_score = {f"average_{criterion}": avg_score}
                    item_results[criterion].append(log_score)
            total_results.append(item_results)      

    elif args.task == "Scientific":
        print("Scientific Task")
        for response_obj in responses:
            question = response_obj['question']
            answer = response_obj.get('answer',[])
            question_results = {"question": question}
            if not answer:  # Check if 'answer' is empty
                for criterion in selected_criteria:
                    responses = [{"answer": "No responses provided", "score": 0}]
                    question_results[criterion] = responses
                    log_score = {f"average_{criterion}": 0}
                    question_results[criterion].append(log_score)
            else:
                for criterion in evaluation_criteria:
                    result = evaluate_scientific(model, response_obj, criterion, args.type, args.sample)
                    question_results[criterion] = [result]
                    model.save_cache()
                for criterion in sampling_criteria:
                    total = []
                    for ans in answer:
                        result = evaluate_scientific(model, {"question": question, "answer": [ans]}, criterion, args.type, 1)
                        total.append(result)
                        print(f"Question: {question}, Answer: {ans}, {criterion.capitalize()} Score: {result['average_score']}")
                    question_results[criterion] = total
                    model.save_cache()
                for criterion in evaluation_criteria:
                    avg_score = sum(res['average_score'] for res in question_results[criterion]) / len(question_results[criterion])
                    log_score = {f"average_{criterion}": avg_score}
                    question_results[criterion].append(log_score)
                for criterion in sampling_criteria:
                    avg_score = sum(res['average_score'] for res in question_results[criterion]) / len(question_results[criterion])
                    log_score = {f"average_{criterion}": avg_score}
                    question_results[criterion].append(log_score)
            total_results.append(question_results)

    elif args.task == "Instances" or args.task == "Similarities":
        print("WKCT Task")
        for response_obj in responses:
            question = response_obj['question']
            answer = response_obj.get('answer',[])
            question_results = {"question": question}
            if not answer:  # Check if 'answer' is empty
                for criterion in selected_criteria:
                    responses = [{"answer": "No responses provided", "score": 0}]
                    question_results[criterion] = responses
                    log_score = {f"average_{criterion}": 0}
                    question_results[criterion].append(log_score)
            else:
                for criterion in evaluation_criteria:
                    result = evaluate_wkct(model, response_obj, criterion, args.type, args.sample)
                    question_results[criterion] = [result]
                    model.save_cache()
                for criterion in sampling_criteria:
                    total = []
                    for ans in answer:
                        result = evaluate_wkct(model, {"question": question, "answer": [ans]}, criterion, args.type, 1)
                        total.append(result)
                        print(f"Question: {question}, Answer: {ans}, {criterion.capitalize()} Score: {result['average_score']}")
                    question_results[criterion] = total
                    model.save_cache()
                for criterion in evaluation_criteria:
                    avg_score = sum(res['average_score'] for res in question_results[criterion]) / len(question_results[criterion])
                    log_score = {f"average_{criterion}": avg_score}
                    question_results[criterion].append(log_score)
                for criterion in sampling_criteria:
                    avg_score = sum(res['average_score'] for res in question_results[criterion]) / len(question_results[criterion])
                    log_score = {f"average_{criterion}": avg_score}
                    question_results[criterion].append(log_score)

            total_results.append(question_results)

    output_folder = task_folder.replace('Output', 'Eval_Result')
    output_file_path = os.path.join(Path(__file__).parent, '..', output_folder, f"{args.input_file.split('_')[1]}_agent", f"evaluation_{args.input_file}_{args.type}_{args.version}.json")

    ensure_folder_exists(os.path.dirname(output_file_path))

    with open(output_file_path, "w") as outfile:
        json.dump(total_results, outfile, indent=4)
    print(f"Results saved to {output_file_path}")
    
    if args.output == 'y':
        mean_std_results = calculate_mean_std(total_results)
        output_csv_path = os.path.join(Path(__file__).parent, '..', 'Results', 'LeaderBoard', f'LeaderBoard-{args.task}.csv')
        ensure_folder_exists(os.path.dirname(output_csv_path))
        write_results_to_csv(args.input_file, mean_std_results, output_csv_path, args.version)
    else:
        print('Output will not be saved in Leader Board!')


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    # PARSERS
    parser = argparse.ArgumentParser(description="Evaluate responses based on specified criteria using OpenAI's API.")
    parser.add_argument("-v", "--version", default="3", choices=["3", "4"], help="Version of the OpenAI model to use.")
    parser.add_argument("-i", "--input_file", required=True, help="Name of the input file located in the Results directory.")
    parser.add_argument("-t", "--type", default="sampling", choices=["default", "sampling"], help="Variant of the evaluation.")
    parser.add_argument("-s", "--sample", default=3, type=int, help="Number of times to sample the evaluation.")
    parser.add_argument("-d", "--task", default="AUT", choices = ["AUT", "Scientific", "Instances", "Similarities"], help="Task for the evaluation. Default is AUT.")
    parser.add_argument("-o", "--output", default="n", choices=["y", "n"], help="Output into LeaderBoard or not")
    args = parser.parse_args()
    auto_grade(args)

