from utils.openai_model import OpenAIModel  # Adjust the import path as needed
from utils.util import parse_judgement_result  # Importing the function from utils/util.py
from eval_functions.eval_prompts import prompts

def pairwise_judgement(model, response_obj, criteria, max_attempts=5):
    pairwise_results = []
    item = response_obj['item']
    uses = response_obj['uses']
    
    print("ITEM = ", item)
    print("USE = ", uses)
    
    get_prompt = prompts[criteria]['pairwise']

    #SET SEED
    seed = 0

    for i in range(len(uses) - 1):
        for j in range(i + 1, len(uses)):
            result_a = uses[i]
            result_b = uses[j]
            attempt = 0
            result_1 = result_2 = None
            while attempt < max_attempts:
                if result_1 is None:
                    response_text_1 = model.compare_pair(item, result_a, result_b, get_prompt, seed)
                    result_1 = parse_judgement_result(response_text_1)
                    print("Seed === ", seed)
                    print("response_text_1 === ", response_text_1)
                    print("parsed 1 === ", result_1)
                if result_2 is None:
                    response_text_2 = model.compare_pair(item, result_b, result_a, get_prompt, seed)
                    result_2 = parse_judgement_result(response_text_2)
                    print("Seed === ", seed)
                    print("response_text_2 === ", response_text_2)
                    print("parsed 2 === ", result_2)
                if result_1 is not None and result_2 is not None:
                    break
                attempt += 1
                seed += 1

            if attempt == max_attempts:
                final_result = 'Error'
            elif (result_1 == 'A' and result_2 == 'B'):
                final_result = 'A'
            elif (result_1 == 'B' and result_2 == 'A'):
                final_result = 'B'
            elif (result_2 == 'C' and result_1 in ['A', 'B']):
                final_result = result_1 if result_1 in ['A', 'B'] else result_2
            elif (result_1 == 'C' and result_2 in ['A', 'B']):
                final_result = 'B' if result_2 == 'A' else 'A'
            else:
                final_result = 'C' 

            pairwise_results.append({
                'pair_A_B': (result_a, result_b),
                'winner': final_result,
                'round_1': response_text_1,
                'round_2': response_text_2
            })

    return pairwise_results



