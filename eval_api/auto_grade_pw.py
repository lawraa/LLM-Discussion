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
import random

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
        rand_seed = random.randint(0, 10000)
        prompt = (messages, rand_seed)
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
                        seed=rand_seed
                    )
                    result = response.choices[0].message.content
                    self.cache_dict[prompt] = result
                    return result
                except:
                    import traceback
                    traceback.print_exc()
                    logging.exception("Exception occurred")
                    time.sleep(1)

    def compare_pair(self, item, result_a, result_b, criteria, seed=0):
        itme_prompt = f"Give me a creative use of {item}"
        if criteria == "originality":
            prompt = f"""
            Please act as an impartial judge and evaluate the originality of the responses provided by two different people to the given task. Compare the responses in terms of their uniqueness, novelty, and creativity. Originality should be assessed based on how unique and innovative each response is, without being influenced by the order in which they are presented, or the length of the responses. Your evaluation should be objective, focusing solely on the originality of the ideas presented in each response. After your comparison, conclude with a clear verdict using this format: '[[A]]' if Result A's response is more original, '[[B]]' if Result B's response is more original, or '[[C]]' for equal originality.
            [User Question]
            {itme_prompt}
            [The Start of Result A]
            {result_a}
            [The End of Result A]
            [The Start of Result B]
            {result_b}
            [The End of Result B]
            """
        messages = [{"role": "user", "content": prompt}]
        response = self.generate_response(messages=messages, seed=seed)
        return response


def parse_judgment_result(response_text):
    pattern = r"\[\[\'?([ABC])\'?\]\]"  # Regex pattern to find [[A]], [[B]], or [[C]]
    matches = re.findall(pattern, response_text)

    if matches:
        return matches[0]  # Return the first match (A, B, or C)
    else:
        return None  # Return None if no match is found

def pairwise_judgment(model, response_obj, criteria, max_attempts=5):
    pairwise_results = []
    item = response_obj['item']
    uses = response_obj['uses']
    print("THE ITEM IS ::::::::::: ", item)
    print("THE USES ARE ----------- ", uses)

    for i in range(len(uses) - 1):
        for j in range(i + 1, len(uses)):
            result_a = uses[i]
            result_b = uses[j]

            attempt = 0
            result_1 = result_2 = None
            while attempt < max_attempts:
                if result_1 is None:
                    response_text_1 = model.compare_pair(item, result_a, result_b, criteria)
                    result_1 = parse_judgment_result(response_text_1)
                    print("response_text_1 ====== ", response_text_1)
                    print("parsed 1 ====== ", result_1)
                if result_2 is None:
                    response_text_2 = model.compare_pair(item, result_b, result_a, criteria)
                    result_2 = parse_judgment_result(response_text_2)
                    print("response_text_2 ====== ", response_text_2)
                    print("parsed 2 ====== ", result_2)
                if result_1 is not None and result_2 is not None:
                    break
                attempt += 1

            if attempt == max_attempts:
                final_result = 'Error'
            elif (result_1 == 'A' and result_2 == 'B'):
                final_result = 'A'
            elif (result_1 == 'B' and result_2 == 'A'):
                final_result = 'B'
            else:
                final_result = 'C' 

            pairwise_results.append({
                'pair': (result_a, result_b),
                'result': final_result,
                'explanation_1': response_text_1,
                'explanation_2': response_text_2
            })

    return pairwise_results

def parse_number_score(input_str):
    pattern = r'\((\d+)\)'  # This pattern matches one or more digits inside parentheses
    matches = re.findall(pattern, input_str)

    # Assuming you want the last matching number
    if matches:
        return int(matches[-1])  # Convert the matched string to an integer

    return None  # Return None or a default value if no match is found


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
    parser = argparse.ArgumentParser(description="This script evaluates responses based on criteria, using OpenAI's API.")
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
    total_pairwise_results = []

    with open(filename, "r") as file:
        responses = json.load(file)

    for response_obj in responses:
        pairwise_results = pairwise_judgment(model, response_obj, "originality", args.sample)
        item_results = {
            "item": response_obj['item'],
            "pairwise_judgment": pairwise_results
        }
        total_pairwise_results.append(item_results)

    output_file_path = os.path.join(Path(__file__).parent, 'result', f"pairwise_evaluation_{args.input_file}_{args.version}.json")
    
    with open(output_file_path, "w") as outfile:
        json.dump(total_pairwise_results, outfile, indent=4)

    model.save_cache()
    
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    main()

# python3 auto_grade.py --version 3 --input_file test_response_2 --sample 3