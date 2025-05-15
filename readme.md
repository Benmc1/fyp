# Project Startup Guide

This guide walks you through starting the inference notebook and integrating it with Rasa and OPA components.

## Prerequisites

- Access to the Colab notebook for inference
- Model stored on Google Drive
- Docker installed on your system
- Ngrok account (optional but recommended for stable URLs)

---

## 🚀 Startup Instructions

### 1. Launch the Inference Notebook

- Open the Colab notebook provided for inference.
- Run all necessary cells to initialize the environment.
- The notebook is currently set up to **load the model from Google Drive**.

### 2. Configure Ngrok URL

- When the notebook starts, it will generate an Ngrok URL.
- Copy the URL (e.g., `https://abc123.ngrok.io`).

- Open the file `rasa/actions/actions.py`.
- Locate the `ITM_URL` variable and replace its value with the Ngrok URL.

  ```python
  ITM_URL = "https://abc123.ngrok.io/ask"
  ```
- Make sure to save the file after updating the URL

### 3. Start Rasa and OPA Containers

Launch the Docker containers that run the Rasa and OPA components:
- docker-compose up

### 4. Interact with Rasa

To send a message to Rasa, make a POST request to:
- "http://localhost:5005/webhooks/rest/webhook"

Example Request (JSON):
```json
{
  "sender": "default",
  "message": "Write a Rego rule to deny tcp access to 100.0.0.1"
}
```
## Data repos
These are the repos where most of the examples came from. Each rego was taken broken into labeled question:answer pairs and stroed in jsonl for training
- https://github.com/CptOfEvilMinions/fleet
- https://github.com/DominusKelvin/fleet
- https://github.com/KarlatIwoca/fleets
- https://github.com/open-policy-agent/opa
- https://www.openpolicyagent.org/docs/latest/policy-language/
- https://github.com/fugue/fregot/
