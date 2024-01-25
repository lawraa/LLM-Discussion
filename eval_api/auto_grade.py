from openai import OpenAI
import os
import pickle
import json
import time
from dotenv import load_dotenv
from typing import List, Dict, Tuple
import argparse
import re

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
                    print ("Pickle Error: Retry in 5sec...")
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
    You are a helpful assistant and a critical thinker. Please evaluate the overall originality of the collective responses to a divergent thinking task where participants were asked to list as many uses for an item as possible. Originality should be gauged by assessing the uniqueness or novelty of the ideas as a whole, considering factors like unexpectedness and rarity across all responses. Rate the overall originality of the set of responses on a scale from 1 to 5, with 5 indicating the highest level of originality. Provide a brief justification for your overall score. It is important to indicate the collective originality score in the specific format of (X) at the end of your response. \n
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
    You are a helpful assistant and a critical thinker. Participants were asked to list as many uses for an item as possible. Please evaluate the overall level of elaboration in the set of responses on a scale of 1 to 5, with 5 being the highest. Elaboration should be judged based on the collective detail and development of the ideas across all responses. Provide a brief justification for your overall evaluation. It is important to indicate the overall elaboration score in the specific format of (X) at the end of your response. \n
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
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", default="3", choices=["3", "4"])
    # Add a new argument for the input file name
    parser.add_argument("--input_file", required=True, help="File name in /home/chenlawrance/repo/LLM-Creativity/dataset/AUT/")
    args = parser.parse_args()

    if args.version == "3":
        version = "gpt-3.5-turbo-1106"
        cache_file_name = "cache_35.pickle"
    elif args.version == "4":
        version = "gpt-4-1106-preview"
        cache_file_name = "cache_4.pickle"
    
    model = OpenAIModel(cache_file_name, version)

    filename = f"/home/chenlawrance/repo/LLM-Creativity/dataset/AUT/{args.input_file}.json"


    # version = "gpt-4-1106-preview"  # or "gpt-3.5-turbo-1106" based on your preference
    # cache_file_name = "cache_4.pickle"  # Change according to the model version

    model = OpenAIModel(cache_file_name, version)
    total_responses = []

    with open(filename, "r") as file:
        responses = json.load(file)
    for response_obj in responses:
        fluency_results = evaluate_fluency(model, response_obj, 3)
        flexibility_results = evaluate_flexibility(model, response_obj, 3)
        originality_results = evaluate_originality(model, response_obj, 3)
        elaboration_results = evaluate_elaboration(model, response_obj, 3)
        item_results = {
            "item": response_obj['item'],
            "response": response_obj['uses'],
            "fluency": fluency_results,
            "flexibility": flexibility_results,
            "originality": originality_results,
            "elaboration": elaboration_results
        }
        total_responses.append(item_results)

    with open(f"./result/evaluation_{args.input_file}_{args.version}.json", "w") as outfile:
        json.dump(total_responses, outfile, indent=4)

    model.save_cache()
    
if __name__ == "__main__":
    main()



# python3 auto_grade --version 3 --input_file test_response