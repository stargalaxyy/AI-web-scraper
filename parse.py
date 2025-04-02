# "Ollama" allows you to run opensource LLMs locally on your computer
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

template = (
    "You are tasked with extracting specific information from the following text content: {dom_content}. "
    "Please follow these instructions carefully: \n\n"
    "1. **Extract Information:** Only extract the information that directly matches the provided description: {parse_description}. "
    "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
    "3. **Empty Response:** If no information matches the description, return an empty string ('')."
    "4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text."
)


model = OllamaLLM(model="deepseek-r1")

# we need to give the prompt more detail
def parse_with_ollama(dom_chunks, parse_description):
    # Creating a prompt templare
    prompt = ChatPromptTemplate.from_template(template)
    # using the prompt template for our specified model
    chain = prompt | model
    
    parsed_results = []

    # passing the different chunks to our LLM and store them
    # start=1 means that we are counting from 1 not 0
    for i, chunk in enumerate(dom_chunks,start=1):
        response = chain.invoke(
            {'dom_content':chunk,'parse_description': parse_description}
            )
        print(f'Parsed batch {i} of {len(dom_chunks)}')
        parsed_results.append(response)
    
    return "\n".join(parsed_results)

# The faster the computer is the faster the code will execute
# This is a very simple example
# There are ways to parallelize this --> asyncronous code