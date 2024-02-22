from openai import OpenAI
import os
import pickle
import time
import logging

class OpenAIModel:
    def __init__(self, cache_file, version, api_key):
        self.cache_file = cache_file
        self.cache_dict = self.load_cache()
        self.version = version
        self.client = OpenAI(api_key=api_key) 

    def save_cache(self):
        with open(self.cache_file, "wb") as f:
            pickle.dump(self.cache_dict, f)

    def load_cache(self, allow_retry=True):
        if os.path.exists(self.cache_file):
            while True:
                try:
                    with open(self.cache_file, "rb") as f:
                        return pickle.load(f)
                except Exception as e:
                    if not allow_retry:
                        raise e
                    logging.error("Pickle Unpickling Error: Retry in 5sec...")
                    time.sleep(5)
        return {}

    def generate_response(self, messages, temperature=1, top_p=1, seed=0):
        prompt = str((messages, seed))
        if prompt in self.cache_dict:
            return self.cache_dict[prompt]
        else:
            try:
                response = self.client.chat.completions.create(
                    model=self.version,
                    messages=messages,
                    temperature=temperature,
                    top_p=top_p,
                    seed=seed
                )
                result = response.choices[0].message.content
                self.cache_dict[prompt] = result
                return result
            except Exception as e:
                logging.exception("Exception occurred during response generation: " + str(e))
                time.sleep(1)
    
    def compare_pair(self, item, result_a, result_b, init_prompt, seed=0):
        item_prompt = f"Give me a creative use of {item}"
        prompt = f"""{init_prompt}\n
            [Task]
            {item_prompt}
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