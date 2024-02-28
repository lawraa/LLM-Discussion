import os
import json
import datetime
from tqdm import tqdm
from openai import OpenAI

client = OpenAI()

agent = 1
input_file_name = "../../datasets/aut_100.json"
# current_date = datetime.date.today().strftime("%m-%d ")
# current_time = datetime.datetime.now()
# formatted_time = current_time.strftime("%H:%M:%S")
# output_file_name = f"../../results/single_agent/AUT_single_result_{agent}_{current_date}.json"


def write_output_file(results):
    folder_path = f"../../results/single_agent/"
    base_file_name = 'AUT_single_result'
    file_extension = '.json'

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    counter = 0
    file_name = f"{base_file_name}-{counter}{file_extension}"
    full_file_path = os.path.join(folder_path, file_name)

    while os.path.exists(full_file_path):
        counter += 1
        file_name = f"{base_file_name}-{counter}{file_extension}"
        full_file_path = os.path.join(folder_path, file_name)
    
    with open(full_file_path, "w") as outfile:
        json.dump(results, outfile, indent=4)
        print(f"output file save at: {full_file_path}")


def call_openai_api(prompt):
    try:
        response = client.chat.completions.create(model="gpt-3.5-turbo-1106",
        messages=[{"role": "user", "content": prompt}])
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error in API call: {e}")
        return None


if __name__ == "__main__":
    with open(input_file_name, "r") as file:
        data = json.load(file)

    results = []
    for example in tqdm(data["Examples"]):
        #round_1
        object = example["object"]
        # question = f"what are some creative use for {object}? The goal is to come up with creative ideas,\
        # which are ideas that strike people as clever, unusual, interesting, uncommon, humorous, innovative, or different.\
        # List the most 10 creative uses for {object}."

        problem_template = " ".join(data["Task"][0]["Problem"])
        question = problem_template.replace("{object}", object)

        input_prompt = question + " Provide the explanations of your answers."
        print("INPUT: ", input_prompt)
        response = call_openai_api(input_prompt)
        print("RESPONSE: ", response)

        #round_2
        round2_prompt = "Here is your Previous answers: ```{}```\n".format(response)
        round2_prompt += "Please categorize answers of a similar type into the same category, and give the explanation of your classification basis. From each category, choose the most creative answer and add some new categories as your revised answers to the following problem:"
        round2_prompt += (question + " Provide the explanations of your answers.")
        print("INPUT_2: ", round2_prompt)
        response2 = call_openai_api(round2_prompt)
        print("RESPONSE2: ", response2)

        #print
        results.append({"input_1": input_prompt, "model_response_1": response, "input_2": round2_prompt, "model_response_2": response2 })
        print({"input": input_prompt, "model_response": response})
        print('================= NEXT OBJECT =================')
    
    write_output_file(results)
    # with open(output_file_name, "w") as outfile:
    #     json.dump(results, outfile, indent=4)
