import openai

openai.api_base = "http://localhost:4891/v1"

openai.api_key = "not needed for a local LLM"

# Set up the prompt and other parameters for the API request
prompt = "Who is Akshay Kumar?"

#model = "gpt-3.5-turbo"
model = "Llama 3 8B Instruct"

def process_prompt(content):
    print("==========> content ", content)
    # Make the API request
    response = openai.Completion.create(
        model=model,
        prompt=f"I have found your stuff. {content}",
        max_tokens=50,
        temperature=0.28,
        top_p=0.95,
        n=1,
        echo=True,
        stream=False
    )
    return response.choices[0].text

