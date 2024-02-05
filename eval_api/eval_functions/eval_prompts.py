aut_prompts = {
    'fluency': {
        'default': f"""
            You are a helpful assistant and a critical thinker. Participants were asked to list as many uses of an item as possible. Identify and count the number of unique, relevant responses and explain why. It is important to the total amount of unique, relevant, and practical responses in the specific format of (X) at the end of your response.
        """,
        'fewshot': f"""
            You are a helpful assistant and a critical thinker. Participants were asked to list as many uses of an item as possible. Your task is to identify and count the number of unique, relevant responses. Explain your reasoning for considering each response unique and relevant.
            It is important to state the total amount of unique, relevant, and practical responses in the specific format of '(X)' at the end of your response.
            Example:
            The item is 'Bottle'. The responses are: 'water container, flower vase, message holder, decorative object, DIY bird feeder, makeshift funnel'. Unique and Relevant Responses: (6). Justification: Each use is distinct and practical in its own way, demonstrating a variety of applications for a bottle.
            \n
            Now, it's your turn:
        """,
        'rubric': f"""
            You are a helpful assistant and a critical thinker. Participants were asked to list as many uses of an item as possible. Identify and count the number of unique, relevant responses and explain why. It is important to the total amount of unique, relevant, and practical responses in the specific format of (X) at the end of your response.
        """
    },
    'flexibility': {
        'default': f"""
            You are a helpful assistant and a critical thinker. Participants were asked to list as many uses for an item as possible. Please evaluate the flexibility of the relevant responses, where flexibility refers to the variety of distinct categories or perspectives represented in the responses. Define and count the number of unique categories or perspectives present, and provide a brief explanation for how you determined these categories. It is important to present the total number of categories or perspectives in the specific format of (X) at the end of your response. 
        """,
        'fewshot': f"""
            You are a helpful assistant and a critical thinker. Participants were asked to list as many uses for an item as possible. Your task is to evaluate the flexibility of the relevant responses. Flexibility refers to the variety of distinct categories or perspectives represented in the responses.
            Define and count the number of unique categories or perspectives present, and provide a brief explanation for how you determined these categories. It is important to present the total number of categories or perspectives in the specific format of '(X)' at the end of your response.

            Example:
            The item is 'Spoon'. The responses are: 'eating utensil, measuring tool, gardening tool for small plants, musical instrument when hit against surfaces, art object in metalwork sculptures'. Unique Categories: (5). Justification: The responses represent distinct categories - culinary use, measurement, gardening, music, and art, showcasing a wide range of flexibility in the uses of a spoon.
            \n
            Now, it's your turn:
        """,
        'rubric': f"""
            You are a helpful assistant and a critical thinker. Participants were asked to list as many uses for an item as possible. Please evaluate the flexibility of the relevant responses, where flexibility refers to the variety of distinct categories or perspectives represented in the responses. Define and count the number of unique categories or perspectives present, and provide a brief explanation for how you determined these categories. It is important to present the total number of categories or perspectives in the specific format of (X) at the end of your response.
        """
    },
    'originality': {
        'default': f"""
            You are a helpful assistant and a critical thinker. Please evaluate the overall originality of the collective responses to a divergent thinking task where participants were asked to list as many uses for an item as possible. Originality should be gauged by assessing the uniqueness or novelty of the ideas as a whole, considering factors like unexpectedness and rarity across all responses. Rate the overall originality of the set of responses on a scale from 1 to 5, with 5 indicating the highest level of originality. Provide a brief justification for your overall score. It is important to indicate the collective originality score in the specific format of (X) at the end of your response. 
        """,
        'fewshot': f"""
            You are a helpful assistant and a critical thinker. Your task is to evaluate the overall originality of the collective responses to a divergent thinking task. Participants were asked to list as many uses for a given item as possible. Assess the uniqueness or novelty of the ideas as a whole, considering factors like unexpectedness and rarity across all responses.
            Rate the overall originality of the set of responses on a scale from 1 to 5, with 5 indicating the highest level of originality. Provide a brief justification for your overall score. It is important to indicate the collective originality score in the specific format of '(X)' at the end of your response.
            Example 1:
            The item is 'Brick'. The responses are: 'building material, doorstop, paperweight, makeshift weapon, garden ornament'. Originality Score: (3). Justification: Most uses are common, but using a brick as a garden ornament is somewhat novel.
            Example 2:
            The item is 'Paperclip'. The responses are: 'holding papers, makeshift lockpick, zipper pull, sculpture material, reset tool for electronics'. Originality Score: (4). Justification: The ideas show a good range of common and unexpected uses, like sculpture material and reset tool for electronics, indicating higher originality. \n
            Now, it's your turn:

        """,
        'rubric': f"""
            You are a helpful assistant and a critical thinker. In this task, participants were asked to list as many uses for an item as possible, a common divergent thinking task that measures creativity. Please evaluate the overall originality of the collective responses based on their uniqueness and novelty. Originality is key in determining how creatively participants think outside the norm. Rate the overall originality on a scale from 1 to 5, considering:

            - 1 point: Very Common - The ideas are mundane and frequently mentioned in everyday contexts. There's a notable lack of novelty, with responses being the most typical or expected uses.
            - 2 points: Somewhat Common - The ideas are somewhat ordinary but show slight variations from typical uses, indicating a basic level of creativity.
            - 3 points: Moderately Original - The ideas display a fair amount of creativity and novelty. They are not the usual thoughts but aren't highly rare or unexpected.
            - 4 points: Very Original - The ideas are significantly unique, demonstrating a high level of creativity and innovation. They are unexpected and not commonly considered.
            - 5 points: Extremely Original - The ideas are extraordinarily unique and rare, displaying a high degree of novelty, creativity, and unexpectedness. These ideas are seldom thought of in typical contexts.

            After reviewing the responses, assign an overall originality score based on these criteria. Provide a brief but detailed justification for your rating, including examples of responses that exemplify the assigned score level. It is important to conclude your response by stating the collective originality score in the format: (X) 
        """,
        'sampling': f"""
            You are a helpful assistant and a critical thinker. Please evaluate the originality of a specific use for an item as part of a divergent thinking task. Originality should be assessed based on the uniqueness and novelty of the idea. Consider factors like unexpectedness and rarity in your evaluation. Rate the originality of this specific use on a scale from 1 to 5, with 5 indicating the highest level of originality. Provide a brief justification for your score. It is important to present the originality score in the specific format of (X) at the end of your response.
        """,
        'pairwise': "Please act as an impartial judge and evaluate the originality of the responses provided by two different people to the given task. Compare the responses in terms of their uniqueness, novelty, and creativity. Originality should be assessed based on how unique and innovative each response is, without being influenced by the order in which they are presented or the length of the responses. Your evaluation should be objective, focusing solely on the originality of the ideas presented in each response. After your comparison, conclude with a clear verdict using this format: '[[A]]' if Result A's response is more original, '[[B]]' if Result B's response is more original, or '[[C]]' for equal originality."
    },
    'elaboration': {
        'default': f"""
            You are a helpful assistant and a critical thinker. Participants were asked to list as many uses for an item as possible. Please evaluate the overall level of elaboration in the set of responses on a scale of 1 to 5, with 5 being the highest. Elaboration should be judged based on the collective detail and development of the ideas across all responses. Provide a brief justification for your overall evaluation. It is important to indicate the overall elaboration score in the specific format of (X) at the end of your response. 
        """,
        'fewshot': f"""
            You are a helpful assistant and a critical thinker. Participants were asked to list as many uses for an item as possible. Your task is to evaluate the overall level of elaboration in the set of responses. Elaboration should be judged based on the collective detail and development of the ideas across all responses.

            Rate the level of elaboration on a scale of 1 to 5, with 5 being the highest. Provide a brief justification for your overall evaluation. It is important to indicate the overall elaboration score in the specific format of '(X)' at the end of your response.

            Example 1:
            The item is 'Brick'. The responses are: 'building material - used in construction for durability, doorstop - to keep doors open, paperweight - to hold down papers, makeshift weapon - in self-defense, garden ornament - painted and decorated for aesthetic appeal'. Elaboration Score: (4). Justification: The responses not only list uses but also include details on how and why each use is applicable, showing a high level of elaboration.

            Example 2:
            The item is 'Paperclip'. The responses are: 'holding papers together, used as a makeshift lockpick, can serve as a zipper pull, can be bent into various shapes for art projects'. Elaboration Score: (3). Justification: While the uses are varied, the details are somewhat basic and could be further developed for higher elaboration. \n

            Now, it's your turn:
        """,
        'rubric': f"""
            You are a helpful assistant and a critical thinker. Participants were asked to list as many uses for an item as possible. Please evaluate the overall level of elaboration in the set of responses on a scale of 1 to 5, where 1 is the least elaborated and 5 is the most elaborated. Elaboration should be judged based on the collective detail and development of the ideas across all responses. Consider the following criteria for each rating point:

            1 point: Very Basic - The responses are extremely basic with minimal detail or explanation. Ideas are presented in a very simple or cursory manner.
            2 points: Somewhat Basic - The responses show a slight degree of detail, but remain on a basic level. Ideas are somewhat developed but lack depth.
            3 points: Moderately Elaborated - The responses offer a moderate level of detail and development. Ideas are explained to a fair extent, showing some thought and consideration.
            4 points: Highly Elaborated - The responses are well-developed and detailed. Ideas are thoroughly explained and exhibit a high level of thought and complexity.
            5 points: Exceptionally Elaborated - The responses demonstrate exceptional elaboration. Ideas are not only detailed and fully developed but also exhibit depth, insight, and comprehensive explanation.

            After reviewing the responses, assign an overall elaboration score based on these criteria. Provide a brief justification for your rating. It is important to conclude your response by stating the overall elaboration score in the format (X).
        """,
        'sampling': f"""
            You are a helpful assistant and a critical thinker. Please evaluate the level of elaboration for a specific use of an item. Elaboration should be judged based on the detail, development, and thoroughness of the idea presented. Rate the elaboration of this specific use on a scale from 1 to 5, with 5 being the highest level of elaboration. Provide a brief justification for your score. It is important to present the elaboration score in the specific format of (X) at the end of your response.
        """,
        'pairwise': "Please act as an impartial judge and evaluate the level of elaboration in the responses provided by two different people to the given task. Compare the responses in terms of their detail, development, and thoroughness. Elaboration should be assessed based on how well-developed and comprehensive each response is, considering the depth and complexity of the ideas presented, without being influenced by the order in which they are presented or the length of the responses. Your evaluation should be objective, focusing solely on the level of elaboration evident in each response. After your comparison, conclude with a clear verdict using this format: '[[A]]' if Result A's response is more elaborated, '[[B]]' if Result B's response is more elaborated, or '[[C]]' for equal levels of elaboration."
        }    
}


scientific_prompts = {
        "fluency": {
            "default": """
                You are a thoughtful assistant with a focus on scientific creativity. Participants were asked to list as many scientific uses or inquiries as possible for a given scenario or object. Your task is to identify and count the number of unique, scientifically relevant responses. Explain why each response is relevant and scientifically sound. It is important to state the total amount of unique, scientifically relevant responses in the specific format of (X) at the end of your response.
            """,
            "rubric": """
                Rate responses based on the quantity and uniqueness of scientific uses or inquiries mentioned. Consider:
                - 1 point: Very few (1-2) relevant scientific uses or inquiries.
                - 2 points: A small range (3-4) of relevant scientific uses or inquiries.
                - 3 points: A moderate variety (5-6) of relevant scientific uses or inquiries, showing some unique ideas.
                - 4 points: A broad range (7-8) of relevant and unique scientific uses or inquiries.
                - 5 points: An extensive range (9+) of highly relevant and unique scientific uses or inquiries, demonstrating exceptional scientific fluency.
                Provide a total count of unique, relevant scientific uses or inquiries in the format (X).
            """
        },
        "flexibility": {
            "default": """
                Assess the diversity of scientific disciplines and approaches represented in the responses. Flexibility in scientific creativity refers to the ability to apply concepts across different branches of science and to think about a scenario or object from multiple scientific perspectives. Count and categorize the responses based on distinct scientific disciplines or methodologies they represent. Conclude with the total number of unique scientific perspectives in the format (X).
            """,
            "rubric": """
                Evaluate the diversity of scientific disciplines and approaches in the responses. Consider:
                - 1 point: Responses are limited to a single scientific discipline or approach.
                - 2 points: Responses include a limited range (2) of scientific disciplines or approaches.
                - 3 points: Responses show a moderate variety (3-4) of scientific disciplines or approaches.
                - 4 points: Responses demonstrate a broad range (5-6) of distinct scientific disciplines or approaches.
                - 5 points: Responses encompass a wide range (7+) of distinct and innovative scientific disciplines or approaches.
                Conclude with the total number of unique scientific perspectives in the format (X).
            """
        },
        "originality": {
            "default": """
                Focus on the originality and innovation of the proposed solutions or uses. Evaluate the responses for their novelty, especially solutions that demonstrate a significant departure from common knowledge or conventional approaches. Rate the overall novelty of the set of responses on a scale from 1 to 5, with 5 being the most novel. Justify your rating with examples from the responses and conclude with the novelty score in the format (X).
            """,
            "sampling": """
                Evaluate the originality of a specific proposed solution or use. Consider its uniqueness and potential for innovation. Rate the originality on a scale from 1 to 5, with 5 being the most novel, and provide your reasoning in the format (X).
            """,
            "pairwise": """
                Compare the originality of solutions or uses proposed by two different responses. Assess which response offers more novel or innovative ideas. Determine the more original set: '[[A]]' for the first response, '[[B]]' for the second, or '[[C]]' if they are equally original.
            """,
            "rubric": """
                Rate the novelty and innovation of the proposed solutions or uses. Consider:
                - 1 point: Solutions are common with little to no novelty.
                - 2 points: Solutions show slight novelty or a new twist on common ideas.
                - 3 points: Solutions are moderately novel, offering some unexpected uses or ideas.
                - 4 points: Solutions are highly novel and innovative, showing unique and uncommon uses or ideas.
                - 5 points: Solutions are exceptionally novel and innovative, presenting groundbreaking and rare ideas.
                Provide an overall novelty score in the format (X).
            """
        },
        "practical_application": {
            "default": """
                Evaluate the practicality and potential impact of the responses on real-world scientific problems or questions. Consider how these ideas could be implemented and the feasibility of their application. Rate the practicality of the responses on a scale from 1 to 5, providing justification for your assessment and concluding with the score in the format (X).
            """,
            "sampling": """
                Assess the feasibility and practical impact of a specific proposed application. Rate its practicality on a scale from 1 to 5, with 5 being the most practical, and justify your assessment in the format (X).
            """,
            "pairwise": """
                Compare the practicality of two different proposed applications. Evaluate which response suggests more feasible and impactful ideas. Conclude with '[[A]]' if the first is more practical, '[[B]]' for the second, or '[[C]]' for equal practicality.
            """,
            "rubric": """
                Evaluate the feasibility and practical impact of the responses. Consider:
                - 1 point: Solutions are impractical or infeasible with little to no real-world application.
                - 2 points: Solutions have limited practicality or feasibility in real-world scenarios.
                - 3 points: Solutions are moderately practical, with a fair potential for real-world application.
                - 4 points: Solutions are highly practical and feasible, with strong potential for impactful real-world application.
                - 5 points: Solutions are exceptionally practical and feasible, with clear, detailed plans for impactful real-world application.
                Rate the practicality of the responses on a scale from 1 to 5 in the format (X).
            """
        },
        "scientific_inquiry_methodology": {
            "default": """
                Assess the methodological soundness of the approaches suggested for scientific inquiry or experimentation. Consider the use of scientific principles, the clarity of the proposed methods, and the ability to generate testable hypotheses. Provide a brief evaluation of the methodological rigor demonstrated in the responses and conclude with an overall methodology score in the format (X).
            """,
            "sampling": """
                Evaluate the methodological rigor of a single proposed scientific inquiry or experiment. Consider its scientific soundness and potential for generating meaningful results. Rate the methodology on a scale from 1 to 5, with 5 being the most rigorous, and explain your rating in the format (X).
            """,
            "pairwise": """
                Compare the scientific inquiry methodologies proposed in two responses. Determine which response demonstrates a more methodologically sound approach to addressing a scientific question. Conclude with '[[A]]' for the first methodology, '[[B]]' for the second, or '[[C]]' for equal rigor.
            """,
            "rubric": """
                Assess the methodological soundness and scientific rigor of the proposed inquiries. Consider:
                - 1 point: Methods are unsound or lack scientific basis.
                - 2 points: Methods show limited scientific soundness or are poorly explained.
                - 3 points: Methods are moderately sound, with some scientific basis and explanation.
                - 4 points: Methods are highly sound and well-explained, with a clear scientific basis.
                - 5 points: Methods are exceptionally sound and rigorously designed, with comprehensive scientific explanations.
                Conclude with an overall methodology score in the format (X).
            """
        },
        "elaboration": {
            "default": """
                Evaluate the overall level of elaboration in the set of responses. Rate the elaboration on a scale of 1 to 5, with 5 being the highest level of detail and development. Provide a brief justification for your overall evaluation. Indicate the overall elaboration score in the specific format of (X).
            """,
            "rubric": """
                Assess the level of detail and development in the responses:
                - 1 point: Very Basic - Minimal detail, ideas are barely developed.
                - 2 points: Somewhat Basic - Some details present, but development is lacking.
                - 3 points: Moderately Elaborated - A fair amount of detail, ideas are reasonably developed.
                - 4 points: Highly Elaborated - Detailed and well-developed ideas, showing depth.
                - 5 points: Exceptionally Elaborated - Comprehensive detail, ideas are fully fleshed out and insightful.
                Justify your rating and conclude with the elaboration score in the format (X).
            """,
            "sampling": """
                Evaluate the level of elaboration for a specific proposed use or idea. Rate the detail and development on a scale from 1 to 5, with 5 indicating the highest level of elaboration, and provide a brief justification for your score. Present the elaboration score in the specific format of (X).
            """,
            "pairwise": """
                Compare the level of elaboration in responses by two different participants. Determine which response is more detailed and well-developed. Conclude with '[[A]]' if the first response shows more elaboration, '[[B]]' if the second is more elaborated, or '[[C]]' for equal levels of elaboration.
            """
        }
}
