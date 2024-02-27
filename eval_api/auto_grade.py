import argparse
import json
import os
from pathlib import Path
from utils.openai_model import OpenAIModel
from eval_functions.eval_criterion import evaluate_aut, evaluate_scientific, evaluate_wkct
from eval_functions.pairwise_comparison import pairwise_judgement
import logging
import csv

def main():
    # OPENAI KEY
    api_key = os.getenv("OPENAI_API_KEY")

    # PARSERS
    parser = argparse.ArgumentParser(description="Evaluate responses based on specified criteria using OpenAI's API.")
    parser.add_argument("-v", "--version", default="3", choices=["3", "4"], help="Version of the OpenAI model to use.")
    parser.add_argument("-i", "--input_file", required=True, help="Name of the input file located in the dataset/AUT/discussion_result directory.")
    parser.add_argument("-c", "--criterion",nargs='+', default="all", choices=["fluency", "flexibility", "originality", "elaboration", "all"] ,help="Criterion for evaluation (fluency, flexibility, originality, elaboration, or all). For Sampling, only choose 'all' or 'originality elaboration'")
    parser.add_argument("-t", "--type", default="default", choices=["default", "fewshot", "rubric", "pairwise", "sampling"], help="Variant of the evaluation.")
    parser.add_argument("-s", "--sample", default=3, type=int, help="Number of times to sample the evaluation.")
    parser.add_argument("-d", "--task", default="aut", choices = ["aut", "scientific", "wkct"], help="Task for the evaluation. Default is AUT.")
    args = parser.parse_args()
    
    # GPT VERSION
    version = "gpt-4-1106-preview" if args.version == "4" else "gpt-3.5-turbo-0125"
    print(f"Using GPT Version {version}, Input: {args.version}")

    # SETUP CACHE AND MODEL
    cache_file_name = f"cache_{args.version}.pickle"
    model = OpenAIModel(cache_file_name, version, api_key)

    #INPUT FILE
    input_file_path = os.path.join(Path(__file__).parent, '..', 'dataset', 'AUT','discussion_result', f"{args.input_file}.json")
    with open(input_file_path, "r") as file:
        responses = json.load(file)
    
    total_results = []

    # PAIRWISE EVALUATION
    if args.type == "pairwise":
        criteria = ["originality", "elaboration"]
        selected_criteria = criteria if args.criterion == ["all"] else args.criterion
        for response_obj in responses:
            item_results = {"item": response_obj['item']}
            for criterion in selected_criteria:
                result = pairwise_judgement(model, response_obj, criterion, 5)
                item_results["results"] = {
                    "criteria": criterion,
                    "pairwise_judgement": result
                }
            total_results.append(item_results)
            model.save_cache()
        
        output_file_path = os.path.join(Path(__file__).parent, 'result', f"evaluation_{args.input_file}_{args.type}_{args.version}.json")
    
    # SAMPLING EVALUATION
    elif args.type == "sampling":
        sampling_criteria = ["originality", "elaboration"]
        evaluation_criteria = ["fluency", "flexibility"]

        if args.criterion == ["all"]:
            selected_criteria = sampling_criteria + evaluation_criteria
        else:
            selected_criteria = args.criterion

        for response_obj in responses:
            item = response_obj['item'] 
            uses = response_obj.get('uses', [])  # Use get to avoid KeyError and provide an empty list as default
            item_results = {"item": item}
            if not uses:  # Check if 'uses' is empty
                for criterion in selected_criteria:
                    # Set score to 0 if 'uses' is empty
                    responses = [{"response": "No uses provided", "score": 0}]
                    item_results[criterion] = responses
                    log_score = {f"average_{criterion}": 0}
                    item_results[criterion].append(log_score)
            else:
                if args.criterion == ["all"]:
                    for criterion in evaluation_criteria:
                        # Evaluate fluency and flexibility for the item
                        result = evaluate_aut(model, response_obj, criterion, args.type, args.sample)
                        item_results[criterion] = [result]
                    for criterion in sampling_criteria:
                        # Evaluate originality and elaboration for each use
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
                    
                else:
                    for criterion in selected_criteria:
                        total = []
                        for use in uses:
                            result = evaluate_aut(model, {"item": item, "uses": [use]}, criterion, args.type, 1)
                            total.append(result)
                            print(f"Item: {item}, Use: {use}, {criterion.capitalize()} Score: {result['average_score']}")
                        item_results[criterion] = total
                        model.save_cache()

                for criterion in sampling_criteria:
                        avg_score = sum(res['average_score'] for res in item_results[criterion]) / len(item_results[criterion])
                        log_score = {f"average_{criterion}": avg_score}
                        item_results[criterion].append(log_score)
                
            total_results.append(item_results)

        output_file_path = os.path.join(Path(__file__).parent, 'result', f"evaluation_{args.input_file}_{args.type}_{args.version}_sample.json")

    # 4 CRITERION EVALUATION (Fluency, Flexibility, Originality, Elaboration)
    else:
        criteria = ["fluency", "flexibility", "originality", "elaboration"]
        selected_criteria = criteria if args.criterion == ["all"] else args.criterion

        for response_obj in responses:
            item_results = {"item": response_obj['item'], "uses": response_obj['uses']}
            for criterion in selected_criteria:
                item_results[criterion] = evaluate_aut(model, response_obj, criterion, args.type, args.sample)
            total_results.append(item_results)
            model.save_cache()
        
        output_file_path = os.path.join(Path(__file__).parent, 'result', f"evaluation_{args.input_file}_{args.type}_{args.version}.json")

    
    with open(output_file_path, "w") as outfile:
        json.dump(total_results, outfile, indent=4)
    print(f"Results saved to {output_file_path}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    main()




