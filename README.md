# Storage System AI Diagnostic Agent

An AI-powered diagnostic assistant that helps users identify, analyze, and troubleshoot latency issues in storage systems by intelligently inspecting metrics, logs, and configurations. Designed for modern, complex storage infrastructures, this agent integrates large language models (LLMs), retrieval-augmented generation (RAG), and interactive visualizations to accelerate issue resolution.

## Features

- **LLM-Powered Diagnosis**: Uses the Groq LLM API to intelligently process user queries and orchestrate tool invocations for gathering relevant diagnostic data.
- **Tool-Based Analysis**: Leverages specialized tool wrappers to fetch and process system metrics, logs, and configuration details relevant to the suspected issue.
- **RAG Integration**: Integrates support documentation (PDF/text) to supplement AI-generated recommendations with reference content from manuals, KB articles, and internal documentation.
- **Interactive Visualizations**: Displays key diagnostic metrics via interactive charts and dashboards for clear, real-time insights.
- **Conversational Context Tracking**: Maintains context of the diagnostic session across multiple user queries to support deep-dive, follow-up, and comparative analysis.

## Supported Latency Issue Types

The AI agent currently supports diagnosis of three primary latency fault categories in storage systems:

1. **High Capacity Usage Issues**
   - Detects when elevated storage capacity consumption leads to degraded I/O latency.
   - Monitors capacity thresholds, volume sizes, and historical usage patterns.

2. **High Throughput Saturation Issues**
   - Identifies scenarios where storage arrays or servers become saturated with I/O requests, causing queueing delays.
   - Analyzes IOPS, bandwidth utilization, queue depths, and average response times.

3. **Replication Link Issues**
   - Diagnoses problems in replication networks that might cause delayed writes, asynchronous lag, or inconsistent states.
   - Tracks replication link health, transfer rates, and lag metrics.

## Setup Instructions

### Prerequisites

- Python 3.8+
- Groq API Key 
- Streamlit (for interactive web UI)

### Installation

1. Clone this repository:

   ```bash
   git clone <repository-url>
   cd storage-ai-agent
   ```

2. Install Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Set environment variables:

   Create a `.env` file in the project root directory and add:

   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ```

4. Provide support documentation:

   Place your storage system's technical documentation or operational guides in the project root directory as either:

   - `support_documentation.pdf`
   - `support_documentation.txt`

## Running the Agent

To start the Streamlit web application, run:

```bash
streamlit run ai_agent.py
```

Once the app launches, open your browser and navigate to:

[http://localhost:8501](http://localhost:8501)

## Usage Instructions

1. **Select a Storage System**  
   Use the storage subsystem UI to create systems and export/unexport volumes.

2. **Enter a Query**  
   In the text input area, type a natural language query about system performance or a specific latency event.  
   _Example:_  
   `"Why was my latency unusually high in system 5003?`

3. **Review the AI’s Analysis**  
   The agent will:
   - Fetch relevant metrics and logs.
   - Perform AI-based analysis.
   - Summarize possible causes, issue classifications, and offer documentation snippets for reference.

5. **Ask Follow-up Questions**  
   Continue the session by typing new, related queries to dive deeper into metrics or request targeted suggestions.  
   _Example:_  
   `"Show replication lag trend over the past 24 hours"`

## Metrics Files Reference

The AI agent reads from these key data sources:

| File Name                  | Description                                              |
|:--------------------------|:---------------------------------------------------------|
| `system_metrics.json`      | System-wide metrics like capacity, throughput, and saturation |
| `io_metrics.json`          | Detailed I/O performance metrics by storage volume and host |
| `replication_metrics.json` | Replication-specific metrics including link health, lag, and transfer rates |
| Log Files (`logs/*.log`)   | System events, error logs, warnings, and informational messages |

## Visualizations

Streamlit-powered interactive dashboards visualize:

- Line and bar charts for capacity, latency, IOPS, and throughput over time.

## Development & Extensibility

**To extend diagnostic capabilities:**

1. **Add New Tool Functions**  
   Create additional data retrieval and analysis functions in `ai_tools.py`.

2. **Update Documentation Corpus**  
   Add new PDFs or text files containing operational manuals, KB articles, or troubleshooting guides into the project root.

3. **Enhance Visualizations**  
   Update the Streamlit app (`ai_agent.py`) to visualize new metrics or analysis results.


## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.


## Example `.env` File

```env
GROQ_API_KEY=your_groq_api_key_here
```

## Example `requirements.txt`

```
streamlit
python-dotenv
groq-sdk
pandas
matplotlib
seaborn
numpy
pdfplumber
```
