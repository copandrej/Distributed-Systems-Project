import os
import subprocess
from dotenv import load_dotenv

# ai agentic stuff
from crewai import Agent, Task, Crew
from crewai.tools import BaseTool

# environment, copy .env.example to .env and adjust before running
load_dotenv()


class KubectlTool(BaseTool):
    name: str = "kubectl"
    description: str = (
        "Executes kubectl commands and returns the actual output. "
        "IMPORTANT: Always use this tool to run commands - never just describe what would happen. "
        "Input format: the command without 'kubectl' prefix. "
        "Examples: 'get nodes', 'get pods -A', 'describe node <name>'"
    )
    
    def _run(self, command: str) -> str:
        try:
            result = subprocess.run(
                f"kubectl {command}", shell=True, capture_output=True, text=True, timeout=30
            )
            return result.stdout if result.returncode == 0 else result.stderr
        except Exception as e:
            return f"Error: {str(e)}"


def main():
    # Setup LLM
    llm_provider = os.getenv("LLM_PROVIDER")
    if llm_provider == "ollama":
        os.environ["OLLAMA_API_BASE"] = os.getenv("OLLAMA_BASE_URL")
        llm = f"ollama/{os.getenv('OLLAMA_MODEL')}"
    elif llm_provider == "openrouter":
        os.environ["OPENROUTER_API_KEY"] = os.getenv("OPENROUTER_API_KEY")
        llm = f"openrouter/{os.getenv('OPENROUTER_MODEL')}"
    else:
        raise NotImplementedError()
    
    # Create agent
    agent = Agent(
        role="Kubernetes assistant",
        goal="Execute kubectl commands and return actual results",
        backstory=(
            "You are a Kubernetes expert. When asked about clusters, you MUST use the kubectl tool "
            "to get real data. Never describe what a command does - always execute it and show the output."
        ),
        tools=[KubectlTool()],
        llm=llm,
        verbose=True
    )
    
    print("Kubernetes Assistant (type 'exit' to quit)\n")
    
    while True:
        query = input("You: ").strip()
        if query.lower() in ['exit', 'quit']:
            break
        
        task = Task(
            description=f"Use the kubectl tool to: {query}. You MUST execute the command and return the actual output.",
            expected_output="The actual command output from kubectl",
            agent=agent
        )
        
        result = Crew(agents=[agent], tasks=[task], verbose=True).kickoff()
        print(f"\nAgent: {result}\n")


if __name__ == "__main__":
    main()
