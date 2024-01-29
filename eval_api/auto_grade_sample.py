from openai import OpenAI
import os
import pickle
import json
import time
from dotenv import load_dotenv
from typing import List, Dict, Tuple
import argparse
import re
from pathlib import Path
import logging


load_dotenv()
client = OpenAI(
    api_key=os.getenv("api_key"),
)

class OpenAIModel():
    def __init__(self, cache_file, version):
        self.cache_file = cache_file
        self.cache_dict = self.load_cache()
        self.version = version

    def save_cache(self):
        for k, v in self.load_cache().items():
            self.cache_dict[k] = v

        with open(self.cache_file, "wb") as f:
            pickle.dump(self.cache_dict, f)

    def load_cache(self, allow_retry=True):
        if os.path.exists(self.cache_file):
            while True:
                try:
                    with open(self.cache_file, "rb") as f:  # rb - read binary
                        cache = pickle.load(f) #load pickle object
                    break
                except Exception:
                    if not allow_retry:
                        assert False
                    logging.error("Pickle Unpickling Error: Retry in 5sec...")
                    time.sleep(5)
        else:
            cache = {}
        return cache # return cache

    def generate_response(self, messages, temperature=1, top_p=1, seed=0):
        prompt = (messages, seed)
        prompt = str(prompt)
        if prompt in self.cache_dict:
            return self.cache_dict[prompt]
        else:
            for _ in range(3):
                try:
                    response = client.chat.completions.create(
                        model=self.version,
                        messages=messages,
                        temperature=temperature,
                        top_p=top_p,
                        seed=seed
                    )
                    result = response.choices[0].message.content
                    self.cache_dict[prompt] = result
                    return result
                except:
                    import traceback
                    traceback.print_exc()
                    logging.exception("Exception occurred")
                    time.sleep(1)

def parse_number_score(input_str):
    pattern = r'\((\d+)\)'  # This pattern matches one or more digits inside parentheses
    matches = re.findall(pattern, input_str)

    # Assuming you want the last matching number
    if matches:
        return int(matches[-1])  # Convert the matched string to an integer

    return None  # Return None or a default value if no match is found

def evaluate_fluency(model: OpenAIModel, item, uses, sample_time):
    prompt = f"""
    You are a helpful assistant and a critical thinker. Participants were asked to list the use of an item as possible. Identify and count the number of unique, relevant responses and explain why. It is important to the total amount of unique, relevant, and practical responses in the specific format of (X) at the end of your response. \n
    "The item is {item}. The response is: {uses}"
    """
    print(prompt)
    messages = [{"role": "user", "content": prompt}]
    sample_responses = []
    sample_score = 0
    seed = 0
    success_count = 0
    while success_count < sample_time:
        try:
            response = model.generate_response(messages=messages, seed=seed)
            print("RESPONSE IS = ", response)
            individual_score = parse_number_score(response)
            sample_responses.append({"response": response, "score": individual_score})
            sample_score +=  individual_score
            print("SCORE IS ===== ", sample_score)
            success_count +=1
        except:
            import traceback
            traceback.print_exc()
            time.sleep(1)
        seed += 1
    average_item_score = sample_score / sample_time
    output_format = {
            "use": uses,
            "responses": sample_responses,
            "average_score": average_item_score
        }
    return output_format

def evaluate_flexibility(model: OpenAIModel, item, uses, sample_time):
    prompt = f"""
    You are a helpful assistant and a critical thinker. Participants were asked to list the use for an item as possible. Please evaluate the flexibility of the relevant responses, where flexibility refers to the variety of distinct categories or perspectives represented in the responses. Define and count the number of unique categories or perspectives present, and provide a brief explanation for how you determined these categories. It is important to present the total number of categories or perspectives in the specific format of (X) at the end of your response. \n
    "The item is {item}. The response is: {uses}"
    """
    messages = [{"role": "user", "content": prompt}]
    sample_responses = []
    sample_score = 0
    seed = 0
    success_count = 0
    while success_count < sample_time:
        try:
            response = model.generate_response(messages=messages, seed=seed)
            print("RESPONSE IS = ", response)
            individual_score = parse_number_score(response)
            sample_responses.append({"response": response, "score": individual_score})
            sample_score +=  individual_score
            print("SCORE IS ===== ", sample_score)
            success_count +=1
        except:
            import traceback
            traceback.print_exc()
            time.sleep(1)
        seed += 1
    average_item_score = sample_score / sample_time
    output_format = {
            "use": uses,
            "responses": sample_responses,
            "average_score": average_item_score
        }
    return output_format

def evaluate_originality(model: OpenAIModel, item, uses, sample_time):
    prompt = f"""
    You are a helpful assistant and a critical thinker. Please evaluate the originality of a specific use for an item as part of a divergent thinking task. Originality should be assessed based on the uniqueness and novelty of the idea. Consider factors like unexpectedness and rarity in your evaluation. Rate the originality of this specific use on a scale from 1 to 5, with 5 indicating the highest level of originality. Provide a brief justification for your score. It is important to present the originality score in the specific format of (X) at the end of your response. \n
    "The item is {item}. The specific use is: {uses}"
    """
    messages = [{"role": "user", "content": prompt}]
    sample_responses = []
    sample_score = 0
    seed = 0
    success_count = 0
    while success_count < sample_time:
        try:
            response = model.generate_response(messages=messages, seed=seed)
            print("RESPONSE IS = ", response)
            individual_score = parse_number_score(response)
            sample_responses.append({"response": response, "score": individual_score})
            sample_score +=  individual_score
            print("SCORE IS ===== ", sample_score)
            success_count +=1
        except:
            import traceback
            traceback.print_exc()
            time.sleep(1)
        seed += 1
    average_item_score = sample_score / sample_time
    output_format = {
            "use": uses,
            "responses": sample_responses,
            "average_score": average_item_score
        }
    return output_format

def evaluate_elaboration(model: OpenAIModel, item, uses, sample_time):
    prompt = f"""
    You are a helpful assistant and a critical thinker. Please evaluate the level of elaboration for a specific use of an item. Elaboration should be judged based on the detail, development, and thoroughness of the idea presented. Rate the elaboration of this specific use on a scale from 1 to 5, with 5 being the highest level of elaboration. Provide a brief justification for your score. It is important to present the elaboration score in the specific format of (X) at the end of your response.\n
    "The item is {item}. The specific use is: {uses}"
    """
    messages = [{"role": "user", "content": prompt}]
    sample_responses = []
    sample_score = 0
    seed = 0
    success_count = 0
    while success_count < sample_time:
        try:
            response = model.generate_response(messages=messages, seed=seed)
            print("RESPONSE IS = ", response)
            individual_score = parse_number_score(response)
            sample_responses.append({"response": response, "score": individual_score})
            sample_score +=  individual_score
            print("SCORE IS ===== ", sample_score)
            success_count +=1
        except:
            import traceback
            traceback.print_exc()
            time.sleep(1)
        seed += 1
    average_item_score = sample_score / sample_time
    output_format = {
            "use": uses,
            "responses": sample_responses,
            "average_score": average_item_score
        }
    return output_format

def main():
    parser = argparse.ArgumentParser(description="This script evaluates responses based on criteria like fluency, flexibility, etc., using OpenAI's API.")
    parser.add_argument("--version", default="3", choices=["3", "4"], help="Version of the OpenAI model to use (3 or 4).")
    parser.add_argument("--input_file", required=True, help="Name of the input file without extension, located in the dataset/AUT/ directory.")
    parser.add_argument("--sample", default=3, type=int, help="Number of times you want to sample")
    args = parser.parse_args()

    if args.version == "3":
        version = "gpt-3.5-turbo-1106"
        cache_file_name = "cache_35.pickle"
    elif args.version == "4":
        version = "gpt-4-1106-preview"
        cache_file_name = "cache_4.pickle"
    #filename = Path(__file__).parent.parent / 'dataset' / 'AUT' / f"{args.input_file}.json"
    filename = os.path.join(Path(__file__).parent, '..', 'dataset', 'AUT', f"{args.input_file}.json")

    model = OpenAIModel(cache_file_name, version)
    total_responses = []

    with open(filename, "r") as file:
        responses = json.load(file)
    for response_obj in responses:
        item = response_obj['item']
        uses = response_obj['uses']
        item_results = {"item": item, "responses": []}
        for use in uses:
            use_results = {}
            #fluency_result = evaluate_fluency(model, item, use, args.sample)
            #flexibility_result = evaluate_flexibility(model, item, use, args.sample)
            originality_result = evaluate_originality(model, item, use, args.sample)
            elaboration_result = evaluate_elaboration(model, item, use, args.sample)
            #print(f"Item: {item}, Use: {use}, Fluency Score: {fluency_result['average_score']}")
            #print(f"Item: {item}, Use: {use}, Flexibility Score: {flexibility_result['average_score']}")
            print(f"Item: {item}, Use: {use}, Originality Score: {originality_result['average_score']}")
            print(f"Item: {item}, Use: {use}, Elaboration Score: {elaboration_result['average_score']}")
            # use_results['fluency'] = fluency_result
            # use_results['flexibility'] = flexibility_result
            use_results['originality'] = originality_result
            use_results['elaboration'] = elaboration_result

            item_results["responses"].append(use_results)
        
        # average_fluency = sum(r['fluency']['average_score'] for r in item_results['responses'] if 'fluency' in r) / len(item_results['responses'])
        # average_flexibility = sum(r['flexibility']['average_score'] for r in item_results['responses'] if 'flexibility' in r) / len(item_results['responses'])
        average_originality = sum(r['originality']['average_score'] for r in item_results['responses'] if 'originality' in r) / len(item_results['responses'])
        average_elaboration = sum(r['elaboration']['average_score'] for r in item_results['responses'] if 'elaboration' in r) / len(item_results['responses'])

        # item_results['average_fluency'] = average_fluency
        # item_results['average_flexibility'] = average_flexibility
        item_results['average_originality'] = average_originality
        item_results['average_elaboration'] = average_elaboration
        
        total_responses.append(item_results)

    output_file_path = os.path.join(Path(__file__).parent, 'result_sample', f"evaluation_{args.input_file}_{args.version}_sample.json")
    
    with open(output_file_path, "w") as outfile:
        json.dump(total_responses, outfile, indent=4)

    model.save_cache()
    
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    main()

# python3 auto_grade.py --version 3 --input_file test_response_2 --sample 3