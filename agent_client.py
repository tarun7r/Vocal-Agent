from textwrap import dedent
from agno.agent import Agent
from agno.models.ollama import Ollama
from agno.tools.googlesearch import GoogleSearchTools
from agno.tools.wikipedia import WikipediaTools
from agno.tools.arxiv import ArxivTools
from agno.run.response import RunResponse

# Define the Knowledge Agent
knowledge_agent_ai = Agent(
    model=Ollama(id="llama3.1:8b"),
    tools=[
        GoogleSearchTools(),  # For performing web searches
        WikipediaTools(),  # For searching Wikipedia content
        ArxivTools(),  # For searching Arxiv publications
    ],
    instructions=dedent("""\
        You are a knowledge assistant that answers questions concisely. Use the available tools:
        - Google Search for general queries and information
        - Wikipedia for facts and history
        - Arxiv for research and papers
        
        Do not use special characters or emojis in your responses.
        Note: Provide clear conversational response in 1-2 sentences and The response should be natural and engaging, and the length depends on what you have to say"""),
    add_datetime_to_instructions=True,
    show_tool_calls=False,
    markdown=True,
    stream=False,
)



def knowledge_agent_client(prompt: str):
    try:
        response = knowledge_agent_ai.run(message=prompt, stream=False)
        if isinstance(response, RunResponse):
            return response.content  
        else:
            print("Error: Invalid response from knowledge_agent_ai.")
            return None  
    except Exception as e:
        print(f"Error while querying knowledge_agent: {str(e)}")
        return None


if __name__ == "__main__":

   # Example usage with a different query
   message = "what is an mcp server use in ai agent"
   print(f'{knowledge_agent_client(message)}')
