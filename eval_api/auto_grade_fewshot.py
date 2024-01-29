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

def evaluate_fluency(model: OpenAIModel, response_obj, sample_time = 3):
    item = response_obj['item']
    if isinstance(response_obj['uses'], str):
        uses = response_obj['uses']
    elif isinstance(response_obj['uses'], list):
        uses = '\n'.join(response_obj['uses'])
    else:
        raise ValueError("Invalid format for 'uses'")
    prompt = f"""
You are a helpful assistant and a critical thinker. Participants were asked to list as many uses of an item as possible. Your task is to identify and count the number of unique, relevant responses. Explain your reasoning for considering each response unique and relevant.

It is important to state the total amount of unique, relevant, and practical responses in the specific format of '(X)' at the end of your response.
Example:
The item is 'Bottle'. The responses are: 'water container, flower vase, message holder, decorative object, DIY bird feeder, makeshift funnel'. Unique and Relevant Responses: 6. Justification: Each use is distinct and practical in its own way, demonstrating a variety of applications for a bottle.
\n
Now, it's your turn:
The item is {item}. The responses are: {uses}
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
            "responses": sample_responses,
            "average_score": average_item_score
        }
    return output_format

def evaluate_flexibility(model: OpenAIModel, response_obj, sample_time = 3):
    item = response_obj['item']
    if isinstance(response_obj['uses'], str):
        uses = response_obj['uses']
    elif isinstance(response_obj['uses'], list):
        uses = '\n'.join(response_obj['uses'])
    else:
        raise ValueError("Invalid format for 'uses'")
    prompt = f"""
You are a helpful assistant and a critical thinker. Participants were asked to list as many uses for an item as possible. Your task is to evaluate the flexibility of the relevant responses. Flexibility refers to the variety of distinct categories or perspectives represented in the responses.

Define and count the number of unique categories or perspectives present, and provide a brief explanation for how you determined these categories. It is important to present the total number of categories or perspectives in the specific format of '(X)' at the end of your response.

Example:
The item is 'Spoon'. The responses are: 'eating utensil, measuring tool, gardening tool for small plants, musical instrument when hit against surfaces, art object in metalwork sculptures'. Unique Categories: (5). Justification: The responses represent distinct categories - culinary use, measurement, gardening, music, and art, showcasing a wide range of flexibility in the uses of a spoon.
\n
Now, it's your turn:
The item is {item}. The responses are: {uses}
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
            "responses": sample_responses,
            "average_score": average_item_score
        }
    return output_format

def evaluate_originality(model: OpenAIModel, response_obj, sample_time = 3):
    item = response_obj['item']
    if isinstance(response_obj['uses'], str):
        uses = response_obj['uses']
    elif isinstance(response_obj['uses'], list):
        uses = '\n'.join(response_obj['uses'])
    else:
        raise ValueError("Invalid format for 'uses'")
    prompt = f"""
You are a helpful assistant and a critical thinker. Your task is to evaluate the overall originality of the collective responses to a divergent thinking task. Participants were asked to list as many uses for a given item as possible. Assess the uniqueness or novelty of the ideas as a whole, considering factors like unexpectedness and rarity across all responses.

Rate the overall originality of the set of responses on a scale from 1 to 5, with 5 indicating the highest level of originality. Provide a brief justification for your overall score. It is important to indicate the collective originality score in the specific format of '(X)' at the end of your response.

Example 1:
The item is 'Brick'. The responses are: 'building material, doorstop, paperweight, makeshift weapon, garden ornament'. Originality Score: (3). Justification: Most uses are common, but using a brick as a garden ornament is somewhat novel.

Example 2:
The item is 'Paperclip'. The responses are: 'holding papers, makeshift lockpick, zipper pull, sculpture material, reset tool for electronics'. Originality Score: (4). Justification: The ideas show a good range of common and unexpected uses, like sculpture material and reset tool for electronics, indicating higher originality. \n

Now, it's your turn:
The item is {item}. The responses are: {uses}
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
            "responses": sample_responses,
            "average_score": average_item_score
        }
    return output_format

def evaluate_elaboration(model: OpenAIModel, response_obj, sample_time = 3):
    item = response_obj['item']
    if isinstance(response_obj['uses'], str):
        uses = response_obj['uses']
    elif isinstance(response_obj['uses'], list):
        uses = '\n'.join(response_obj['uses'])
    else:
        raise ValueError("Invalid format for 'uses'")
    prompt = f"""
You are a helpful assistant and a critical thinker. Participants were asked to list as many uses for an item as possible. Your task is to evaluate the overall level of elaboration in the set of responses. Elaboration should be judged based on the collective detail and development of the ideas across all responses.

Rate the level of elaboration on a scale of 1 to 5, with 5 being the highest. Provide a brief justification for your overall evaluation. It is important to indicate the overall elaboration score in the specific format of '(X)' at the end of your response.

Example 1:
The item is 'Brick'. The responses are: 'building material - used in construction for durability, doorstop - to keep doors open, paperweight - to hold down papers, makeshift weapon - in self-defense, garden ornament - painted and decorated for aesthetic appeal'. Elaboration Score: (4). Justification: The responses not only list uses but also include details on how and why each use is applicable, showing a high level of elaboration.

Example 2:
The item is 'Paperclip'. The responses are: 'holding papers together, used as a makeshift lockpick, can serve as a zipper pull, can be bent into various shapes for art projects'. Elaboration Score: (3). Justification: While the uses are varied, the details are somewhat basic and could be further developed for higher elaboration. \n

Now, it's your turn:
The item is {item}. The responses are: {uses}
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
        # fluency_results = evaluate_fluency(model, response_obj, args.sample)
        # flexibility_results = evaluate_flexibility(model, response_obj, args.sample)
        originality_results = evaluate_originality(model, response_obj, args.sample)
        elaboration_results = evaluate_elaboration(model, response_obj, args.sample)
        item_results = {
            "item": response_obj['item'],
            "response": response_obj['uses'],
            # "fluency": fluency_results,
            # "flexibility": flexibility_results,
            "originality": originality_results,
            "elaboration": elaboration_results
        }
        total_responses.append(item_results)

    output_file_path = os.path.join(Path(__file__).parent, 'result', f"evaluation_{args.input_file}_{args.version}_fewshot.json")
    
    with open(output_file_path, "w") as outfile:
        json.dump(total_responses, outfile, indent=4)

    model.save_cache()
    
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    main()

# python3 auto_grade.py --version 3 --input_file test_response_2 --sample 3