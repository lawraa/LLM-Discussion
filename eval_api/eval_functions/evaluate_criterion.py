from eval_functions.eval_prompts import prompts
from utils.util import parse_number_score
from utils.openai_model import OpenAIModel
import traceback
import logging
import time

def evaluate_criterion(model: OpenAIModel, response_obj, criterion, eval_type, sample_time=3):
    item = response_obj['item']
    uses = '\n'.join(response_obj['uses']) if isinstance(response_obj['uses'], list) else response_obj['uses']

    # Fetch the specific prompt and append the common part
    get_prompt = prompts[criterion].get(eval_type, prompts[criterion]['default'])
    if eval_type == 'sampling':
        full_prompt = get_prompt +  f"\nThe item is {item}. The specific use is: {uses}"
    else: 
        full_prompt = get_prompt + f"\nThe item is {item}. The responses are: {uses}"
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
            print("Model Response ::: ", response)
            print("Given Seed ::: ", seed)
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
    if eval_type == "sample":
        return {
            "use": uses,
            "responses": sample_responses,
            "average_score": average_item_score
        }
    
    return {
        "responses": sample_responses,
        "average_score": average_item_score
    }
