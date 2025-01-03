from llm_helper import llm
from few_shot import FewShotPosts




def get_length_str(length):
    if length == "Short":
        return "1 to 5 lines"
    elif length == "Medium":
        return "5 to 10 lines"
    elif length == "Long":
        return "11 to 15 lines"


def get_prompt(length, language, tag):
    fs = FewShotPosts()

    length_str = get_length_str(length)

    prompt = f'''
        Generate a LinkedIn post using the below information. No preamble
        1. Topic:{tag}
        2. Length: {length_str}
        3. Language: {language}
        If language is Hinglish then it means it is a mix of Hindi and English.
        The script for the generated post should always be English.

        '''
    examples = fs.get_filtered_posts(language, length, tag)

    if len(examples) > 0:
        prompt += "4. Use the writing style as per the following examples"
        for i, post in enumerate(examples, start=1):
            post_text = post['text']

            prompt += f"\n\nExample {i}: \n\n {post_text}"

            if i == 2:
                break

    return prompt


def generate_post(length, language, tag):

    prompt = get_prompt(length, language, tag)
    response = llm.invoke(prompt)
    return response.content



if __name__ == "__main__":
    post = generate_post("Long", "English", "Career")
    print(post)