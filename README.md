# Distributed Systems Project Report: Agentic Kubernetes Management

Agentic system for managing Kubernetes clusters through natural language interactions.

Single AI agent that can monitor and manage distributed Kubernetes infrastructure using LLMs.

Agent can execute kubectl commands, monitor cluster health, and manage services (replication, configs) through a terminal-based chat interface.

## Architecture

- **Agent Framework**: CrewAI for agent orchestration
- **LLM Provider**: Configurable, Probably openrouter with some free model or Ollama for local LLM
- **Kubernetes**: Local cluster using Kind + kubectl command execution
- **Interface**: Terminal-based chatbot for user interaction
- **Implementation**: Simple Python app, uv for dependencies, modular, easy to extend as we will need for the master's thesis project later

- Python 3.12
- Docker
- kubectl CLI
- Kind (Kubernetes in Docker), or any Kubernetes cluster with kubectl access
- uv (Python package manager), or pip


## Example interactions:
```
You: Check the health of all pods in the cluster
Agent: Running health check... Found 5 pods, 4 running, 1 pending...

You: Deploy an example hello world nginx service
Agent: Creating deployment... Deployment successful!

You: Increase the replicas of the nginx service to 3
Agent: Scaling deployment... Now 3 replicas running.
```

## Installation

### uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

If you dont want to use uv, you can install dependencies with pip from pyproject.toml


### Local Kubernetes

To allow localhost access to NodePort services, create the cluster with the provided config:

```bash
kind create cluster --name agent-cluster --config kind-config.yaml
```

### Set Up Ollama (Local LLM) if needed or connect to OpenRouter (see .env.example)

```bash
# Run Ollama in Docker
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
docker exec -it ollama ollama pull qwen3:8b
```

# copy .env.example to .env and set your API keys and model preferences

```bash
cp .env.example .env
```

### 4. Install Project Dependencies, or use pip

```bash
uv sync
```

## Echo Service (Test Workload)

A simple FastAPI service is included in `echo_service/` to test the agent's deployment capabilities.

### Build and Deploy

1. **Build the Docker image:**
   ```bash
   docker build -t echo-service:latest ./echo_service
   ```

2. **Load image into Kind cluster:**
   ```bash
   kind load docker-image echo-service:latest --name agent-cluster
   ```

3. **Deploy to Kubernetes:**
   ```bash
   kubectl apply -f echo_service/deployment.yaml
   ```

4. **Verify deployment:**
   ```bash
   kubectl get pods -l app=echo-service
   ```

5. **Access the service (Localhost):**
   The service is exposed via `NodePort` 30080, which is mapped to localhost by the Kind config.
   
   ```bash
   curl -X POST "http://localhost:30080/echo" -d '{"test": "data"}'
   ```
6. **Load testing**

   A load testing script is provided to evaluate the echo service's performance.

   ```bash
   python load_test.py --url http://localhost:30080/echo --concurrency 5 --requests 20 --output latency_results.json
   ```

Tell the agent to increase the number of replicas of the echo service and run the load test again to see the performance improvement.

## Repository Structure

- `main.py`: The entry point for the AI agent. It initializes the CrewAI agent and handles the chat loop.
- `load_test.py`: An asynchronous script to stress-test deployed services and measure latency.
- `echo_service/`: Contains the source code for a test workload (FastAPI app) that simulates computational work.
  - `main.py`: The application code performing matrix multiplication.
  - `Dockerfile`: Instructions to containerize the service.
  - `deployment.yaml`: Kubernetes manifests for deploying the service.
- `kind-config.yaml`: Configuration for the local Kind cluster to map ports to localhost.
- `pyproject.toml`: Defines project dependencies and python version.


## References and technologies used

- [CrewAI Documentation](https://docs.crewai.com/)
- [Ollama](https://ollama.ai/)
- [Kind Documentation](https://kind.sigs.k8s.io/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [uvicorn](https://www.uvicorn.org/)
