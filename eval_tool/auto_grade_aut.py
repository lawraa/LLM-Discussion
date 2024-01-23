from openai import OpenAI
import time
import json
from typing import List, Dict, Tuple
from dotenv import load_dotenv
import os
import pickle
import argparse

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

    
    def generate_response(self, messages, tools, tool_choice, temperature = 1, top_p = 1, seed = 0):
        prompt = (messages, tools, tool_choice, seed)

        prompt = str(prompt)
        #print("MESSAGE IS : ", messages)
        if prompt in self.cache_dict:
            return self.cache_dict[prompt]
        else:
            for _ in range(3):
                try:
                    response = client.chat.completions.create(
                        model=self.version, # gpt-4-1106-preview, gpt-3.5-turbo-1106
                        messages=messages,
                        temperature=temperature, # adjust temperature
                        top_p=top_p,
                        tools=tools,
                        tool_choice=tool_choice,
                        seed=seed
                    )
                    result = response.choices[0].message.tool_calls[0].function.arguments
                    result = json.loads(result)
                    self.cache_dict[prompt] = result
                    return result
                except:
                    import traceback
                    traceback.print_exc()
                    time.sleep(1)
    

def evaluate_fluency(model: OpenAIModel, responses_file_path: str, sample_time = 3):
    with open(responses_file_path, "r") as file:
        responses = json.load(file)
    tools = [
        {
            "type": "function",
            "function": {
                "name": "fluency_evaluator",
                "description": "This tool evaluates counts the number of unique, relevant(practical) responses, lists them out, and provides the total fluency score. It also includes an explanation of the criteria used to determine the relevance of each response and the counting process.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "results": {
                            "type": "object",
                            "description": "The output of the evaluation, including the listed responses and total number of relevant(practical) response.",
                            "properties": {
                                "number_of_responses": {
                                    "type": "number",
                                    "description": "This will output the total number of unique, relevant ideas."
                                },
                                "listed_responses": {
                                    "type": "string",
                                    "description": "Numbered list of unique, relevant responses."
                                },
                                "evaluation_explanation": {
                                    "type": "string",
                                    "description": "A brief explanation of how relevance of response was determined and counted."
                                }
                            }
                        }
                    }
                }
            }
        }
    ]

    tool_choice = {"type": "function", "function": {"name": "fluency_evaluator"}}
    #format or process "responses" further

    total_score = 0
    total_responses = []

    for response_obj in responses:
        item = response_obj['item']
        uses = '\n'.join(response_obj['uses'])
        prompt = f"The item is {item}. The responses are: {uses}"

        messages = [{"role": "user", "content": prompt}]
        sample_responses = []
        sample_score = 0
        seed = 0
        success_count = 0
        while success_count < sample_time:
            try:
                response = model.generate_response(messages=messages, tools=tools, tool_choice=tool_choice, seed=seed)
                print(response)
                sample_responses.append(response)
                sample_score += response['results']['number_of_responses']
                success_count += 1
            except:
                import traceback
                traceback.print_exc()
                time.sleep(1)
            seed += 1
        average_item_score = sample_score / sample_time
        total_score += average_item_score

        # Add the responses for this item to the total responses
        total_responses.append({
            "item": item,
            "result": uses,
            "responses": sample_responses,
            "average_score": average_item_score
        })

    return total_responses


def evaluate_flexibility(model: OpenAIModel, responses_file_path: str, sample_time = 3):
    with open(responses_file_path, "r") as file:
        responses = json.load(file)
    tools = [
        {
            "type": "function",
            "function": {
                "name": "flexibility_evaluator",
                "description": "This tool evaluates the flexibility of responses to a divergent thinking task where participants were asked to list as many use of an item as possible. Flexibility refers to the variety of categories or perspectives in the responses. This tool calculates the number of different categories or approaches used in the answer.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "results": {
                            "type": "object",
                            "description": "The output of the evaluation, including the flexibility rating and explanation.",
                            "properties": {
                                "listed_categories": {
                                    "type": "string",
                                    "description": "List of categories and approaches appeared in the response."
                                },
                                "total_flexibility_score": {
                                    "type": "number",
                                    "description": "The total flexibility score based on the total number of categories or perspectives in the responses."
                                },
                                "evaluation_explanation": {
                                    "type": "string",
                                    "description": "A brief explanation of how flexibility of response was determined and counted."
                                }
                            }
                        }
                    }
                }
            }
        }
    ]
    tool_choice = {"type": "function", "function": {"name": "flexibility_evaluator"}}
    total_score = 0
    total_responses = []

    for response_obj in responses:
        item = response_obj['item']
        uses = response_obj['uses']
        prompt = f"The item is {item}. The responses are: {uses}"

        messages = [{"role": "user", "content": prompt}]
        sample_responses = []
        sample_score = 0
        seed = 0
        success_count = 0
        while success_count < sample_time:
            try:
                response = model.generate_response(messages=messages, tools=tools, tool_choice=tool_choice, seed=seed)
                print(response)
                sample_responses.append(response)
                sample_score += response['results']['total_flexibility_score']
                success_count += 1
            except:
                import traceback
                traceback.print_exc()
                time.sleep(1)
            seed += 1
        average_item_score = sample_score / sample_time
        total_score += average_item_score
        total_responses.append({
            "item": item,
            "result": uses,
            "responses": sample_responses,
            "average_score": average_item_score
        })
    return total_responses


def evaluate_originality(model: OpenAIModel, responses_file_path: str, sample_time = 3):
    with open(responses_file_path, "r") as file:
        responses = json.load(file)
    tools = [
        {
            "type": "function",
            "function": {
                "name": "originality_evaluator",
                  "description": "This tool evaluates the originality of responses to a divergent thinking task where participants were asked to list as many use of an item as possible. Originality is gauged by the uniqueness or novelty of the ideas. This tool gives one overall score to the entire list of ideas and provides an explanation of the assessment.",
                  "parameters": {
                    "type": "object",
                    "properties": {
                        "results": {
                            "type": "object",
                            "description": "The output of the evaluation, including the overall originality rating and explanation.",
                            "properties": {
                                "originality_rating": {
                                    "type": "number",
                                    "description": """
                                    The overall originality rating on a scale from 1 to 5, with 1 being the lowest. 
                                    """  
                                },
                                "evaluation_explanation": {
                                    "type": "string",
                                    "description": "A brief explanation of how the originality was assessed."
                                }
                            }
                        }
                    }
                }
            }
        }
    ]
    tool_choice = {"type": "function", "function": {"name": "originality_evaluator"}}
    total_score = 0
    total_responses = []

    for response_obj in responses:
        item = response_obj['item']
        uses = response_obj['uses']
        prompt = f"The item is {item}. The responses are: {uses}"

        messages = [{"role": "user", "content": prompt}]
        sample_responses = []
        sample_score = 0
        seed = 0
        success_count = 0
        while success_count < sample_time:
            try:
                response = model.generate_response(messages=messages, tools=tools, tool_choice=tool_choice, seed=seed)
                print(response)
                sample_responses.append(response)
                sample_score += response['results']['originality_rating']
                success_count += 1
            except:
                import traceback
                traceback.print_exc()
                time.sleep(1)
            seed += 1
        average_item_score = sample_score / sample_time
        total_score += average_item_score

        # Add the responses for this item to the total responses
        total_responses.append({
            "item": item,
            "result": uses,
            "responses": sample_responses,
            "average_score": average_item_score
        })
    return total_responses


def evaluate_elaboration(model: OpenAIModel, responses_file_path: str, sample_time: int = 3):
    with open(responses_file_path, "r") as file:
        responses = json.load(file)
    tools = [
        {
            "type": "function",
            "function": {
                "name": "elaboration_evaluator",
                "description": "This tool evaluates the level of elaboration in responses to a divergent thinking task where participants were asked to list as many use of an item as possible. Elaboration involves the detail and development in the ideas or responses. This tool gives one score for the detail and development of the entire list of ideas and provides an explanation of the assessment.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "results": {
                            "type": "object",
                            "description": "The output of the evaluation, including the overall elaboration rating and explanation.",
                            "properties": {
                                "elaboration_rating": {
                                    "type": "number",
                                    "description": """
                                    The overall elaboration rating on a scale from 1 to 5, with 1 being the lowest.
                                    Give the score according to the following guidance:
                                    - 5 points: The response demonstrates exceptional detail and development in ideas. It goes beyond the surface level, offering in-depth explanations or unique expansions of the concept. The ideas are richly fleshed out and thoroughly considered, showing a high level of thoughtfulness and complexity.
                                    - 4 points: The response shows a high level of detail and development. It provides more than just a basic explanation, including additional layers or aspects of the idea. The response is well-thought-out and shows clear signs of extended thinking, but may lack the highest level of complexity or depth seen in 5-point responses.
                                    - 3 points: The response demonstrates a moderate level of detail and development. It goes beyond a basic description, offering some additional insights or extensions of the idea, but these are not deeply explored. The response shows some level of thoughtfulness but remains somewhat on the surface.
                                    - 2 points: The response shows limited detail and development. It provides a basic, surface-level description or idea, with minimal additional insights or expansion. The response is simple and straightforward, lacking depth or thorough exploration.
                                    - 1 point: The response demonstrates very little to no elaboration. It provides a minimal, cursory description or idea, with no additional detail or development. The response lacks depth and complexity, offering the most basic and conventional explanation.
                                    """
                                },
                                "evaluation_explanation": {
                                    "type": "string",
                                    "description": "A brief explanation of how the elaboration was assessed."
                                }
                            }
                        }
                    }
                }
            }
        }
    ]
    tool_choice = {"type": "function", "function": {"name": "elaboration_evaluator"}}
    total_score = 0
    total_responses = []

    for response_obj in responses:
        item = response_obj['item']
        uses = response_obj['uses']
        prompt = f"The item is {item}. The responses are: {uses}"

        messages = [{"role": "user", "content": prompt}]
        sample_responses = []
        sample_score = 0
        seed = 0
        success_count = 0
        while success_count < sample_time:
            try:
                response = model.generate_response(messages=messages, tools=tools, tool_choice=tool_choice, seed=seed)
                print(response)
                sample_responses.append(response)
                sample_score += response['results']['elaboration_rating']
                success_count += 1
            except:
                import traceback
                traceback.print_exc()
                time.sleep(1)
            seed += 1
        average_item_score = sample_score / sample_time
        total_score += average_item_score

        # Add the responses for this item to the total responses
        total_responses.append({
            "item": item,
            "result": uses,
            "responses": sample_responses,
            "average_score": average_item_score
        })

    return total_responses

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

    # Use the input file argument
    filename = f"/home/chenlawrance/repo/LLM-Creativity/dataset/AUT/{args.input_file}.json"
    
    fluency_results = evaluate_fluency(model, filename)
    flexibility_results = evaluate_flexibility(model, filename)
    originality_results = evaluate_originality(model, filename)
    elaboration_results = evaluate_elaboration(model, filename)

    evaluation_details = {
        "fluency": fluency_results,
        "flexibility": flexibility_results,
        "originality": originality_results,
        "elaboration": elaboration_results
    }

    with open(f"./result/evaluation_{args.input_file}_{args.version}.json", "w") as outfile:
        json.dump(evaluation_details, outfile, indent=4)

    model.save_cache()

if __name__ == "__main__":
    main()


#python your_script.py --version 3 --input_file phober_response