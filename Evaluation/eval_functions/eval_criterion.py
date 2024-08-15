from eval_functions.eval_prompts import aut_prompts, scientific_prompts, wkct_prompts
from utils.util import parse_number_score
from utils.openai_model import OpenAIModel
import traceback
import logging
import time

def evaluate_aut(model: OpenAIModel, response_obj, criterion, eval_type, sample_time=3):
    item = response_obj['item']
    detect_empty_list = response_obj.get('uses', []) 
    uses = '\n'.join(response_obj['uses']) if isinstance(response_obj['uses'], list) else response_obj['uses']
    if not detect_empty_list:  # Check if 'uses' is not provided
        if eval_type == "sampling":
            return {
                "use": "Empty List",
                "responses": [{"response": "No uses provided", "score": 0}],
                "average_score": 0
            }
        else: 
            return {
                "responses": [{"response": "No uses provided", "score": 0}],
                "average_score": 0
            }

    # if there is eval type, get aut_prompts[criterion][eval_type], else get aut_prompts[criterion]['default']
    get_prompt = aut_prompts[criterion].get(eval_type, aut_prompts[criterion]['default'])
    
    if eval_type == 'sampling':
        full_prompt = get_prompt + f"\nThe item is {item}\nThe response is: {uses}"
    print("FULL PROMPT ::: ", full_prompt)
    messages = [{"role": "user", "content": full_prompt}]
    sample_responses = []
    sample_score = 0

    #SET SEED
    seed = 0
    
    success_count = 0

    while success_count < sample_time:
        try:
            response = model.generate_response(messages=messages, seed=seed)
            print("Given Seed ::: ", seed)
            print("Model Response ::: ", response)
            individual_score = parse_number_score(response)
            sample_responses.append({"response": response, "score": individual_score})
            sample_score += individual_score
            print("Score ::: ", sample_score)
            success_count += 1
        except Exception as e:
            traceback.print_exc()
            logging.exception(f"Exception occurred: {e}")
            time.sleep(1)
        seed += 1

    average_item_score = sample_score / sample_time
    if eval_type == "sampling":
        return {
            "task result": response_obj['uses'],
            "responses": sample_responses,
            "average_score": average_item_score
        }
        
    
    return {
        "responses": sample_responses,
        "average_score": average_item_score
    }

def evaluate_scientific(model: OpenAIModel, response_obj, criterion, eval_type, sample_time=3):
    # When fluency and flexibility are evaluated, the response_obj is a list of responses
    # When originality and elaboration are evaluated, the response_obj is a single response
    # eval_type is set to 'sampling'
    question = response_obj['question']
    answer = '\n'.join(response_obj['answer']) if isinstance(response_obj['answer'], list) else response_obj['answer']
    #task_response
    get_prompt = scientific_prompts[criterion].get(eval_type, scientific_prompts[criterion]['default'])
    
    if eval_type == 'sampling':
        full_prompt = get_prompt + f"\nThe task is: {question}\nThe response is: {answer}"
    print("Input Prompt ::: ", full_prompt)
    messages = [{"role": "user", "content": full_prompt}]
    sample_responses = []
    sample_score = 0

    #SET SEED
    seed = 0
    
    success_count = 0

    while success_count < sample_time:
        try:
            response = model.generate_response(messages=messages, seed=seed)
            print("Given Seed ::: ", seed)
            print("Model Response ::: ", response)
            individual_score = parse_number_score(response)
            sample_responses.append({"response": response, "score": individual_score})
            sample_score += individual_score
            print("Score ::: ", sample_score)
            success_count += 1
        except Exception as e:
            traceback.print_exc()
            logging.exception(f"Exception occurred: {e}")
            time.sleep(1)
        seed += 1

    average_item_score = sample_score / sample_time
    if eval_type == "sampling":
        return {
            "answer": answer,
            "responses": sample_responses,
            "average_score": average_item_score
        }
    return {
        "responses": sample_responses,
        "average_score": average_item_score
    }


def evaluate_wkct(model: OpenAIModel, response_obj, criterion, eval_type, sample_time=3):
    # When fluency and flexibility are evaluated, the response_obj is a list of responses
    # When originality and elaboration are evaluated, the response_obj is a single response
    # eval_type is set to 'sampling'
    question = response_obj['question']
    answer = '\n'.join(response_obj['answer']) if isinstance(response_obj['answer'], list) else response_obj['answer']
    #task_response
    get_prompt = wkct_prompts[criterion].get(eval_type, aut_prompts[criterion]['default'])
    
    if eval_type == 'sampling':
        full_prompt = get_prompt + f"\nThe task is: {question}\nThe response is: {answer}"
    print("Input Prompt ::: ", full_prompt)
    messages = [{"role": "user", "content": full_prompt}]
    sample_responses = []
    sample_score = 0

    #SET SEED
    seed = 0
    
    success_count = 0

    while success_count < sample_time:
        try:
            response = model.generate_response(messages=messages, seed=seed)
            print("Given Seed ::: ", seed)
            print("Model Response ::: ", response)
            individual_score = parse_number_score(response)
            sample_responses.append({"response": response, "score": individual_score})
            sample_score += individual_score
            print("Score ::: ", sample_score)
            success_count += 1
        except Exception as e:
            traceback.print_exc()
            logging.exception(f"Exception occurred: {e}")
            time.sleep(1)
        seed += 1

    average_item_score = sample_score / sample_time
    if eval_type == "sampling":
        return {
            "answer": answer,
            "responses": sample_responses,
            "average_score": average_item_score
        }
    return {
        "responses": sample_responses,
        "average_score": average_item_score
    }