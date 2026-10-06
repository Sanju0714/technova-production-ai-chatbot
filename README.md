# TechNova Production-Ready AI Customer Support Chatbot

A production-oriented customer support chatbot built with **LangGraph, LangChain, NVIDIA NIM, and LangSmith**.

The chatbot supports order-status lookup, returns, warranty, and shipping questions while maintaining conversation memory, handling failures, tracing executions, evaluating response quality, and monitoring latency, token usage, and errors.

## 🚀 Features

- **LangGraph agent workflow** with tool calling
- **NVIDIA Nemotron 3 Super 120B A12B** LLM
- **Order-status lookup tool**
- **Returns, warranty, and shipping policy tool**
- **Conversation memory** using LangGraph `MemorySaver`
- **LangSmith tracing** for LLM, tools, graph nodes, latency, and tokens
- **Input guardrail** for irrelevant or unsafe requests
- **Fallback handling** for model failures
- **Timeout and retry handling**
- **Tool-failure handling**
- **Friendly API failure responses**
- **LangSmith LLM-as-a-judge evaluation**
- **Streamlit chat interface**
- **LangSmith production dashboard**
- **Error-rate alerting**
- **Token optimization experiment**

## 🏗️ Architecture

```text
                    User
                      │
                      ▼
                 ┌─────────┐
                 │Guardrail│
                 └────┬────┘
                      │
                      ▼
                 ┌─────────┐
                 │  Agent  │
                 │  LLM    │
                 └────┬────┘
                      │
                 Tool required?
                    /     \
                  No       Yes
                  │         │
                  ▼         ▼
               Answer    ┌─────────┐
                         │  Tool   │
                         └────┬────┘
                              │
                              ▼
                         ┌─────────┐
                         │  Agent  │
                         │  LLM    │
                         └────┬────┘
                              │
                              ▼
                           Answer
```

## 🧰 Tech Stack

| Technology | Purpose |
|---|---|
| Python | Application development |
| LangChain | LLM and tool integration |
| LangGraph | Stateful agent workflow |
| NVIDIA NIM | Hosted NVIDIA inference |
| Nemotron 3 Super 120B A12B | Production LLM |
| LangSmith | Tracing, evaluation and monitoring |
| Streamlit | Chat UI |
| Pandas | Benchmark analysis |

## 🔧 Available Tools

### `get_order_status`

Looks up a TechNova order using its order ID.

Example:

```text
TN1001
→ Laptop Pro 14
→ Shipped
→ ETA: 2 days
```

### `get_policy`

Retrieves TechNova policies for:

- Returns
- Warranty
- Shipping

## 🧠 Conversation Memory

The chatbot uses LangGraph `MemorySaver` with a `thread_id` to maintain conversation state.

Example:

```text
User: What is the status of TN1001?

Assistant: Order TN1001 is shipped...

User: What was the item?

Assistant: The item was Laptop Pro 14.
```

## 📊 Performance Results

### Model Comparison

The same 20-question benchmark was run against both models.

| Model | Average | P50 | P95 | Max | Quality |
|---|---:|---:|---:|---:|---:|
| Nemotron 3.5 Lightning 30B | 18.85s | 11.77s | 61.32s | 89.82s | 5/5 |
| Nemotron 3 Super 120B A12B | **1.84s** | **1.59s** | **3.65s** | **4.98s** | **5/5** |

The 120B model delivered substantially lower observed latency in this benchmark while maintaining the same evaluation quality.

> These are observed benchmark results for the NVIDIA hosted endpoint and should not be interpreted as a guarantee of model latency in every environment.

## 🪙 Token Optimization

A 10-turn conversation was tested using full conversation history.

### Full History

- Input tokens: **6,847**
- Total tokens: **8,127**

### Recent History

- Input tokens: **1,451**
- Total tokens: **2,731**

### Reduction

- **78.81% input-token reduction**
- **66.40% total-token reduction**

This demonstrates the impact of controlling conversation history in long-running sessions.

## 💰 Cost Estimation

Using the assignment's hypothetical rate of **$0.90 per 1M tokens** for the large model:

| Scenario | Estimated Cost |
|---|---:|
| 10-turn full history | $0.007506 |
| 10,000 conversations/day | $75.06/day |
| 30-day month | $2,251.80/month |
| 10-turn optimized | $0.002458 |
| 10,000 optimized conversations/day | $24.58/day |
| 30-day optimized month | $737.37/month |

These are **hypothetical assignment estimates**, not actual NVIDIA billing.

## 🛡️ Fault Tolerance

A 20-request fault-injection benchmark was performed.

| Metric | Result |
|---|---:|
| Total requests | 20 |
| Normal requests | 10 |
| Fault-injected requests | 10 |
| Successful requests | 12 |
| Failed requests | 8 |
| Fault-injection error rate | **40.00%** |

### Tested failure scenarios

- Invalid model → fallback model
- Invalid API key → friendly failure
- Timeout → retry/backoff
- Tool failure → friendly failure
- Bad input → validation response

> The 40% error rate represents the deliberately fault-injected benchmark and is **not a normal production error rate**.

## 🧪 LangSmith Evaluation

Evaluation dataset:

```text
technova-customer-support-eval
```

Dataset size:

**10 examples**

| Model | Correctness |
|---|---:|
| Nemotron 3.5 Lightning 30B | **100%** |
| Nemotron 3 Super 120B A12B | **100%** |

An LLM-as-a-judge evaluator was used to assess answer correctness.

Human feedback was also collected through LangSmith.

## 📈 Observability

LangSmith was used to monitor:

- Full LangGraph execution trees
- LLM calls
- Tool calls
- Guardrail execution
- Latency
- Token usage
- Errors
- Evaluation scores
- User feedback

A custom production dashboard was created for:

- Average latency
- Token usage
- Error rate

An error-rate alert was also configured for monitoring.

## 🖥️ Streamlit UI

The project includes a Streamlit interface with:

- Customer-support chat
- Conversation interaction
- Helpful / Not Helpful feedback buttons
- LangSmith feedback integration

Run the UI with:

```bash
streamlit run app/ui.py
```

## 📁 Project Structure

```text
technova/
│
├── app/
│   ├── graph.py
│   ├── tools.py
│   └── ui.py
│
├── experiments/
│   ├── latency.py
│   ├── part_d_tokens.py
│   ├── part_d_optimization.py
│   ├── part_e_error_rate.py
│   └── evaluate_models.py
│
├── results/
│   ├── summary.csv
│   ├── latency_nemotron35_direct.csv
│   └── latency_nemotron120b.csv
│
├── screenshots/
│
├── report.pdf
├── README.md
├── requirements.txt
├── .env.example
└── .gitignore
```

## ⚙️ Setup

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd technova
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file:

```env
NVIDIA_API_KEY=your_nvidia_api_key

LANGSMITH_TRACING=true
LANGSMITH_API_KEY=your_langsmith_api_key
LANGSMITH_PROJECT=technova-bot-your-name
```

**Never commit `.env` or API keys to GitHub.**

Use `.env.example` as the template.

### 5. Run the chatbot

```bash
python -m app.graph
```

### 6. Run the Streamlit UI

```bash
streamlit run app/ui.py
```

## 🔬 Run Experiments

Latency benchmark:

```bash
python -m experiments.latency
```

Token benchmark:

```bash
python -m experiments.part_d_tokens
```

Token optimization:

```bash
python -m experiments.part_d_optimization
```

Fault-injection benchmark:

```bash
python -m experiments.part_e_error_rate
```

LangSmith evaluation:

```bash
python -m experiments.evaluate_models
```

## 🔐 Security

The repository excludes sensitive files through `.gitignore`.

```text
.env
venv/
__pycache__/
*.pyc
.ipynb_checkpoints/
```

Before pushing to GitHub, verify that no NVIDIA or LangSmith API keys are present in tracked files.

## 📄 Project Report

The complete project report contains:

- Architecture
- LangSmith traces
- Latency analysis
- Token analysis
- Cost estimation
- Fault-tolerance testing
- Model evaluation
- Deployment recommendation
- Monitoring and alerting

See:

```text
report.pdf
```

## 🎯 Key Takeaways

This project demonstrates how to move beyond a basic LLM chatbot toward a more production-oriented AI application by combining:

**Agent orchestration + tool calling + memory + observability + evaluation + resilience + monitoring.**

## 👩‍💻 Author

**Gorli Sanjana**

B.Tech Computer Science & Engineering  
Rajiv Gandhi University of Knowledge Technologies (RGUKT)

---

⭐ If you find this project useful, consider giving the repository a star.
