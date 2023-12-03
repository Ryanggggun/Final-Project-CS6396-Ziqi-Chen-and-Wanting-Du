import openai

openai.api_key = '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'

def get_chatgpt_response(comment, product_url, model="gpt-4-1106-preview", max_tokens=60):
    prompt = f"A customer has a concern about the product: '{comment}'. Imagine that you are a competitor of that product and sell the benefits of your own product based on the claim. Don't include sorry and thank you's. Answer in a positive sunny way! don't apologize, and present the benefits of the product(For example, it's cost-effective, very good quality and looks great. Respond to reviews based on their claims). End the response with a link to the product website for additional support."
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "system", "content": prompt}],
            max_tokens=max_tokens
        )
        reply = response['choices'][0]['message']['content'].strip()
        return f"{reply}\nFor more information, please visit our website: {product_url}"
    except Exception as e:
        print(f"An error occurred: {e}")
        return ""