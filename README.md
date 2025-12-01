# Distributed Systems Project

Agentic system for managing Kubernetes clusters through natural language interactions.

Single AI agent that can monitor and manage distributed Kubernetes infrastructure using LLMs.

Agent can execute kubectl commands, monitor cluster health (graphana, prometheus), and manage services (replication, configs) through a terminal-based chat interface.

## Architecture

- **Agent Framework**: CrewAI for agent orchestration
- **LLM Provider**: Configurable probably openrouter with some free model
- **Kubernetes**: Local cluster using Kind + kubectl command execution
- **Interface**: Terminal-based chatbot for user interaction
- **Implementation**: Simple Python app, uv for dependencies, modular.

- Python 3.12+
- Docker
- kubectl CLI
- Kind (Kubernetes in Docker)
- uv (Python package manager)


## Example interactions:
```
You: Check the health of all pods in the cluster
Agent: Running health check... Found 5 pods, 4 running, 1 pending...

You: Deploy a nginx service with 3 replicas
Agent: Creating deployment... Deployment successful!

You: What's consuming the most CPU?
Agent: Analyzing resource usage... Top consumer: api-server (65% CPU)
```

## Installation

### uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Local Kubernetes

```bash
kind create cluster --name agent-cluster
```

### Set Up Ollama (Local LLM) if needed or connect to OpenRouter

```bash
# Run Ollama in Docker
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
docker exec -it ollama ollama pull qwn
```

### 4. Install Project Dependencies

```bash
uv sync
```

## TODO
- Define a more complex cluster with some configs
- Add pod monitoring and health check functions (prometheus, grafana)
- Implement service deployment capabilities (yaml conigs, kubectl apply)
- Test with Kind local cluster

## References

- [CrewAI Documentation](https://docs.crewai.com/)
- [Ollama](https://ollama.ai/)
- [Kind Documentation](https://kind.sigs.k8s.io/)
- [uv Package Manager](https://github.com/astral-sh/uv)