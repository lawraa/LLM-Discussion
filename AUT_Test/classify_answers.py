from openai import OpenAI

client = OpenAI()
import json
import datetime

agent = 1
input_file_name = "dataset_aut_test.json"
current_date = datetime.date.today().strftime("%m-%d_")
current_time = datetime.datetime.now()
formatted_time = current_time.strftime("%H:%M:%S")
output_file_name = f"classify_answers_{agent}_{current_date}{formatted_time}.json"

def call_openai_api(prompt):
    try:
        response = client.chat.completions.create(model="gpt-3.5-turbo-1106",
        messages=[{"role": "user", "content": prompt}])
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error in API call: {e}")
        return None

def extract_purposes(response):
    # Assuming each purpose is on a new line and starts with a number and a dot '1.', '2.', etc.
    lines = response.split('\n')
    purposes = []

    for line in lines:
        # Check if the line starts with a number and a dot, indicating it's one of the items
        if line.strip() and line[0].isdigit() and line[1] == '.':
            # Extract everything after 'number.' and strip whitespaces
            purpose = line.split('.', 1)[1].strip()
            purposes.append(purpose)
    return purposes


if __name__ == "__main__":
    with open(input_file_name, "r") as file:
        data = json.load(file)

    results = []
    for example in data["examples"]:
        #round_1
        object = example["input"]
        question = f"What are some creative uses for {object}? The goal is to come up with creative ideas, which are ideas that strike people as clever, unusual, interesting, uncommon, humorous, innovative, or different.List as many as creative uses for {object}."
        input_prompt = question
        # print("INPUT: ", input_prompt)
        response = call_openai_api(input_prompt)
        print(f"RESPONSE: \n", response)
        purposes = extract_purposes(response)


        #round_2
        classify_prompt = f"Q: Here are the usages of {object}: {response}. Classify them into several categories by usages, and give the explanation of your classification."
        classification = call_openai_api(classify_prompt)
        print(f"CLASSIFICATION: \n", classification)

        #round_3
        extract_prompt = f"Q: Based on your classification of the usages of{object}: {classification}, choose only one the most creative answer from each category and give the explanation why it is the most creative one."
        # print("INPUT: ", advantage_prompt)
        extracted = call_openai_api(extract_prompt)
        print(f"EXTRACTED: \n",extracted)

        # #round_4
        re_think_prompt = f"Here are some creative categories of the uses of {object}. Please come up with more creative ideas, which are ideas that strike people as clever, unusual, interesting, uncommon, humorous, innovative, or different.List as many as creative uses for {object} other than these categories, and give the explanations."
        print("INPUT: ", re_think_prompt)
        final_answer = call_openai_api(re_think_prompt)
        print("FINAL ANSWER: ",final_answer)
        print("------------------------------------------")


            #print
        results.append({"init": input_prompt, "model_response_1": response, "input_2":classify_prompt, "classification": classification, "input_3": extract_prompt, "extracted": extracted, "input_4": re_think_prompt, "final answer": final_answer})
            # print({"input": input_prompt, "model_response": response, "target": example["target"]})
    
    with open(output_file_name, "w") as outfile:
        json.dump(results, outfile, indent=4)
