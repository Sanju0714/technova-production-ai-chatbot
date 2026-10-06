# TechNova Customer Support Chatbot

A production-oriented customer support chatbot built using LangChain, LangGraph, NVIDIA-hosted LLMs, and LangSmith.

## Project Overview

TechNova is an electronics store that sells laptops, phones, and accessories.

The chatbot can help customers with:

- Order status
- Returns
- Warranty
- Shipping
- Conversation follow-up questions

The project demonstrates stateful conversations, tool calling, conversation memory, LangSmith observability, latency monitoring, token usage analysis, cost estimation, fault handling, and model evaluation.

## Features

- Stateful chatbot using LangGraph
- Conversation memory using MemorySaver
- Order status lookup
- Return, warranty, and shipping policy lookup
- Tool calling
- LangSmith tracing
- Custom traced helper function
- Run metadata and tags
- Latency benchmarking
- P50 and P95 latency analysis
- Time-to-first-token measurement
- Token usage tracking
- Cost estimation
- Token optimization
- Fault injection and error handling
- LangSmith evaluation dataset
- LLM-as-judge evaluation
- Human feedback
- Model comparison

## Technology Stack

- Python 3.12
- LangChain
- LangGraph
- LangChain OpenAI integration
- NVIDIA NIM API
- LangSmith
- Pandas
- python-dotenv

## Project Structure

technova/
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
├── README.md
│
├── app/
│   ├── tools.py
│   └── graph.py
│
├── experiments/
│   ├── latency.py
│   ├── tokens.py
│   ├── part_e_error_rate.py
│   ├── evaluate_models.py
│   └── add_feedback.py
│
└── results/
    └── summary.csv

## Setup

### 1. Create Virtual Environment

python -m venv venv

### 2. Activate Virtual Environment

Windows:

venv\Scripts\activate

### 3. Install Dependencies

pip install -r requirements.txt

## Environment Variables

Create a .env file in the project root.

Add the following:

NVIDIA_API_KEY=your_nvidia_api_key
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=your_langsmith_api_key
LANGSMITH_PROJECT=technova-bot-sanjana

Never commit the .env file to GitHub.

The .env.example file contains placeholder values.

## Running the Chatbot

Run:

python -m app.graph

Example:

TechNova Support Chatbot
Type 'exit' to stop.

You: What is the status of order TN1001?

Assistant: Order TN1001: Item: Laptop Pro 14, Status: Shipped, ETA: 2 days

You: What was the item in that order?

Assistant: The item in order TN1001 was Laptop Pro 14.

The second question demonstrates conversation memory using LangGraph.

Type exit to stop the application.

## Mock Data

The chatbot uses the following TechNova mock orders:

| Order ID | Item | Status | ETA |
|---|---|---|---|
| TN1001 | Laptop Pro 14 | Shipped | 2 days |
| TN1002 | Noise-cancel Earbuds | Processing | 5 days |
| TN1003 | Phone X | Delivered | - |

### Policies

Returns:

Returns are accepted within 30 days in the original packaging.

Warranty:

Electronics come with a 1-year manufacturer warranty.

Shipping:

Free shipping is available for orders above Rs.999. Standard delivery takes 3-5 days.

## Tools

### get_order_status

Retrieves the status, item name, and estimated delivery time for a TechNova order.

### get_policy

Retrieves TechNova policies for:

- Returns
- Warranty
- Shipping

## LangGraph Workflow

The chatbot uses a LangGraph state graph consisting of:

- Agent node
- Tools node
- Tool routing
- Conversation state
- MemorySaver checkpointing

The workflow is:

START → Agent → Tools → Agent → END

If the agent determines that a tool is required, LangGraph routes the request to the appropriate tool. The tool result is then returned to the agent to generate the final response.

## Conversation Memory

Conversation memory is implemented using LangGraph's MemorySaver.

A thread ID is used to maintain conversation state.

Example:

You: What is the status of TN1001?

Assistant: Order TN1001 is shipped. The item is Laptop Pro 14 and the ETA is 2 days.

You: What was the item?

Assistant: The item was Laptop Pro 14.

## LangSmith Observability

LangSmith is used to trace and monitor the chatbot.

The project tracks:

- LangGraph execution
- Agent execution
- LLM calls
- Tool calls
- Latency
- Token usage
- Tags
- Metadata
- Session information
- Thread information
- Custom traced functions

The custom clean_user_input helper is instrumented using the LangSmith @traceable decorator.

Metadata includes:

- model_name
- user_id
- app_version
- session_id
- thread_id

LangSmith project:

technova-bot-sanjana

## Model Configuration

Primary model:

nvidia/nemotron-3.5-lightning-30b-a3b

The application uses NVIDIA's OpenAI-compatible endpoint through ChatOpenAI.

Endpoint:

https://integrate.api.nvidia.com/v1

This compatibility approach was used because the required NVIDIA model ID was not available through the installed ChatNVIDIA model catalog.

Model configuration:

- Temperature: 0
- Maximum output tokens: 256
- Thinking: Disabled

## Part C - Latency Monitoring

### Baseline Results

| Metric | Result |
|---|---:|
| Average latency | 9.34 s |
| P50 latency | 4.70 s |
| P95 latency | 42.47 s |
| Maximum latency | 55.91 s |

### Optimized Results

| Metric | Result |
|---|---:|
| Average latency | 5.33 s |
| P50 latency | 2.65 s |
| P95 latency | 18.48 s |
| Maximum latency | 28.27 s |

### Improvement

| Metric | Improvement |
|---|---:|
| Average latency | 42.9% |
| P50 latency | 43.6% |
| P95 latency | 56.5% |
| Maximum latency | 49.4% |

The optimization used a reduced maximum output token limit and disabled unnecessary model thinking.

## Model Comparison

30B Model:

nvidia/nemotron-3.5-lightning-30b-a3b

120B Model:

nvidia/nemotron-3-super-120b-a12b

| Metric | 30B | 120B |
|---|---:|---:|
| Average latency | 6.71 s | 1.30 s |
| P50 latency | 3.20 s | 1.14 s |
| P95 latency | 16.94 s | 2.29 s |
| Maximum latency | 18.53 s | 2.82 s |
| Evaluation accuracy | 100% | 100% |

## Time to First Token

Representative streaming measurements:

| Model | TTFT |
|---|---:|
| 30B | 0.554 s |
| 120B | 0.356 s |

## Part D - Token Usage and Cost

A 10-turn conversation was analyzed to measure token growth.

### Token Usage

| Metric | Tokens |
|---|---:|
| Input tokens | 8,178 |
| Output tokens | 1,722 |
| Total tokens | 9,900 |

### Token Optimization

| Metric | Reduction |
|---|---:|
| Input tokens | 77.1% |
| Total tokens | 62.6% |

The optimization reduced the amount of conversation history sent to the model while maintaining answer quality.

### 10-Turn Cost

| Model | Cost |
|---|---:|
| 30B | $0.001980 |
| 120B | $0.008910 |

### 20-Question Benchmark Cost

| Model | Cost |
|---|---:|
| 30B | $0.004103 |
| 120B | $0.018238 |

### Estimated Cost at 10,000 Conversations per Day

| Model | Daily Cost | Monthly Cost |
|---|---:|---:|
| 30B | $19.80 | $594 |
| 120B | $89.10 | $2,673 |

These are exercise estimates based on the hypothetical rate card provided in the assignment and are not actual NVIDIA billing prices.

## Part E - Error Handling and Resilience

Five fault scenarios were tested:

1. Invalid model
2. Invalid or missing API key
3. Timeout
4. Tool failure
5. Bad user input

### Invalid Model

A non-existent model was intentionally configured.

The application falls back to the backup model.

### Invalid API Key

A deliberately invalid API key was used.

The application fails fast and returns a friendly user-facing message instead of repeatedly retrying the authentication failure.

### Timeout

A timeout condition was intentionally simulated.

The application retries the request with backoff and returns a graceful message if the retries fail.

### Tool Failure

The order-status tool was intentionally made to fail during testing.

The chatbot handles the tool failure and returns a user-friendly response instead of exposing an internal stack trace.

### Bad User Input

Invalid input was tested.

The application provides guidance instead of exposing internal errors.

## Fault-Injection Benchmark

A 20-request fault-injection benchmark was performed.

| Metric | Result |
|---|---:|
| Total requests | 20 |
| Successful requests | 12 |
| Failed requests | 8 |
| Error rate | 40% |

The 40% error rate represents a deliberate fault-injection benchmark and should not be interpreted as the normal production error rate.

## Part F - Evaluation and Feedback

A LangSmith evaluation dataset containing 10 customer-support questions and reference answers was created.

The evaluation used an LLM-as-judge approach to score answer correctness.

### Evaluation Results

| Model | Correctness |
|---|---:|
| 30B | 100% |
| 120B | 100% |

Both models achieved 100% correctness on the 10-example evaluation dataset.

### Human Feedback

Five positive user feedback ratings were attached to LangSmith runs using the user_rating feedback key.

Positive human feedback:

5 runs

## Key Findings

The 30B model achieved the same evaluation accuracy as the 120B model in the 10-example evaluation while having a substantially lower estimated cost.

The 120B model showed lower measured latency in the model comparison benchmark.

The 30B model provides a better cost-quality trade-off for a cost-sensitive customer-support deployment, while the 120B model may be considered when lower latency is prioritized and the additional cost is acceptable.

## Security

The following sensitive information must never be committed to GitHub:

- NVIDIA API key
- LangSmith API key
- .env file

The .gitignore file excludes .env, the virtual environment, Python cache files, and notebook checkpoints.

## Results

Benchmark results are stored in:

results/summary.csv

The results include:

- Latency metrics
- Token usage
- Token optimization
- Cost estimates
- Fault-injection results
- Model evaluation results
- Human feedback count

## Running Experiments

Latency experiments are stored in the experiments directory.

Token and cost experiments are stored in the experiments directory.

Run the Part E fault-injection benchmark using:

python -m experiments.part_e_error_rate

Run the model evaluation using:

python -m experiments.evaluate_models

Add LangSmith human feedback using:

python -m experiments.add_feedback

## Final Recommendation

Based on the measured results, the 30B model is recommended for the initial TechNova deployment because:

- It achieved 100% correctness in the evaluation dataset.
- It has a substantially lower estimated cost.
- It provides sufficient performance for the customer-support use case.
- Token optimization further reduces operational cost.

The 120B model can be considered when lower latency is prioritized and the additional inference cost is acceptable.

## Production Risks to Monitor

### 1. Latency

Monitor P95 latency continuously.

Recommended alert:

P95 latency above 8 seconds for 5 consecutive minutes.

### 2. Error Rate

Monitor application and tool failures.

Recommended alert:

Error rate above 5% over a rolling production window.

### 3. Token and Cost Growth

Monitor input-token growth caused by long conversations.

Recommended alert:

Average token usage increases by more than 25% compared with the established baseline.

## Conclusion

The TechNova chatbot demonstrates a production-oriented LangGraph architecture with tool calling, conversation memory, LangSmith observability, model benchmarking, token optimization, cost estimation, resilience testing, and automated evaluation.

The experiments show that careful monitoring and token optimization can significantly improve latency and operational efficiency while maintaining answer quality.