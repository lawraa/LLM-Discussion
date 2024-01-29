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
    You are a helpful assistant and a critical thinker. Participants were asked to list as many uses of an item as possible. Identify and count the number of unique, relevant responses and explain why. It is important to the total amount of unique, relevant, and practical responses in the specific format of (X) at the end of your response. \n
    "The item is {item}. The responses are: {uses}"
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
    You are a helpful assistant and a critical thinker. Participants were asked to list as many uses for an item as possible. Please evaluate the flexibility of the relevant responses, where flexibility refers to the variety of distinct categories or perspectives represented in the responses. Define and count the number of unique categories or perspectives present, and provide a brief explanation for how you determined these categories. It is important to present the total number of categories or perspectives in the specific format of (X) at the end of your response. \n
    "The item is {item}. The responses are: {uses}"
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
    You are a helpful assistant and a critical thinker. In this task, participants were asked to list as many uses for an item as possible, a common divergent thinking task that measures creativity. Please evaluate the overall originality of the collective responses based on their uniqueness and novelty. Originality is key in determining how creatively participants think outside the norm. Rate the overall originality on a scale from 1 to 5, considering:

    - 1 point: Very Common - The ideas are mundane and frequently mentioned in everyday contexts. There's a notable lack of novelty, with responses being the most typical or expected uses.
    - 2 points: Somewhat Common - The ideas are somewhat ordinary but show slight variations from typical uses, indicating a basic level of creativity.
    - 3 points: Moderately Original - The ideas display a fair amount of creativity and novelty. They are not the usual thoughts but aren't highly rare or unexpected.
    - 4 points: Very Original - The ideas are significantly unique, demonstrating a high level of creativity and innovation. They are unexpected and not commonly considered.
    - 5 points: Extremely Original - The ideas are extraordinarily unique and rare, displaying a high degree of novelty, creativity, and unexpectedness. These ideas are seldom thought of in typical contexts.

    After reviewing the responses, assign an overall originality score based on these criteria. Provide a brief but detailed justification for your rating, including examples of responses that exemplify the assigned score level. It is important to conclude your response by stating the collective originality score in the format: (X) \n

    "The item is {item}. The responses are: {uses}"
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
    You are a helpful assistant and a critical thinker. Participants were asked to list as many uses for an item as possible. Please evaluate the overall level of elaboration in the set of responses on a scale of 1 to 5, where 1 is the least elaborated and 5 is the most elaborated. Elaboration should be judged based on the collective detail and development of the ideas across all responses. Consider the following criteria for each rating point:

    1 point: Very Basic - The responses are extremely basic with minimal detail or explanation. Ideas are presented in a very simple or cursory manner.
    2 points: Somewhat Basic - The responses show a slight degree of detail, but remain on a basic level. Ideas are somewhat developed but lack depth.
    3 points: Moderately Elaborated - The responses offer a moderate level of detail and development. Ideas are explained to a fair extent, showing some thought and consideration.
    4 points: Highly Elaborated - The responses are well-developed and detailed. Ideas are thoroughly explained and exhibit a high level of thought and complexity.
    5 points: Exceptionally Elaborated - The responses demonstrate exceptional elaboration. Ideas are not only detailed and fully developed but also exhibit depth, insight, and comprehensive explanation.

    After reviewing the responses, assign an overall elaboration score based on these criteria. Provide a brief justification for your rating. It is important to conclude your response by stating the overall elaboration score in the format (X). \n

    "The item is {item}. The responses are: {uses}"
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

    output_file_path = os.path.join(Path(__file__).parent, 'result_sample', f"evaluation_{args.input_file}_{args.version}_criteria.json")
    
    with open(output_file_path, "w") as outfile:
        json.dump(total_responses, outfile, indent=4)

    model.save_cache()
    
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    main()

# python3 auto_grade.py --version 3 --input_file test_response_2 --sample 3