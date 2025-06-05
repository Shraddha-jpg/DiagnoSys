import os
import json
import re
import importlib.util
from typing import Any, Dict, List
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, END
from pydantic import BaseModel
from typing import TypedDict

# === Load Configuration ===
CONFIG_PATH = "config.json"
if not os.path.exists(CONFIG_PATH):
    raise FileNotFoundError(f"Configuration file not found at {CONFIG_PATH}")
with open(CONFIG_PATH, 'r') as f:
    config = json.load(f)
PROBLEM_SPACE = config.get("problem_space", "storage_system")
PROBLEM_SPACE_DIR = f"problem_spaces/{PROBLEM_SPACE}"
DATA_MODEL_PATH = f"{PROBLEM_SPACE_DIR}/data_model.json"
TOOLS_CONFIG_PATH = f"{PROBLEM_SPACE_DIR}/tools.json"
RAG_PATH = f"{PROBLEM_SPACE_DIR}/rag.txt"

# Validate problem space files
for path in [DATA_MODEL_PATH, TOOLS_CONFIG_PATH, RAG_PATH]:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Required file not found at {path}")

# Load data model
with open(DATA_MODEL_PATH, 'r') as f:
    DATA_MODEL = json.load(f)

# Load tools
with open(TOOLS_CONFIG_PATH, 'r') as f:
    TOOLS_CONFIG = json.load(f)

TOOLS = {}
for tool in TOOLS_CONFIG:
    tool_path = f"{PROBLEM_SPACE_DIR}/tools/{tool['file']}"
    if not os.path.exists(tool_path):
        raise FileNotFoundError(f"Tool file not found at {tool_path}")
    spec = importlib.util.spec_from_file_location(tool['name'], tool_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if not hasattr(module, 'run'):
        raise AttributeError(f"Tool {tool['name']} missing 'run' function")
    TOOLS[tool['name']] = {
        'run': module.run,
        'description': tool['description'],
        'parameters': tool['parameters'],
        'required': tool['required']
    }

# === CONFIG ===
GROQ_API_KEY = ""
GROQ_MODEL = "llama-3.3-70b-versatile"

# === Initialize LLM ===
llm = ChatOpenAI(
    model=GROQ_MODEL,
    openai_api_base="https://api.groq.com/openai/v1",
    openai_api_key=GROQ_API_KEY,
    temperature=0
)

# === Load and Chunk RAG Document ===
print("🔍 Loading and splitting RAG document...")
loader = TextLoader(RAG_PATH)
docs = loader.load()
if not docs:
    raise ValueError("No content loaded from the RAG file")
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
chunks = splitter.split_documents(docs)

# === Embeddings and Vector Store ===
print("📡 Embedding and indexing...")
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectorstore = FAISS.from_documents(chunks, embeddings)
retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 7})

# === State Definition for LangGraph ===
class AgentState(TypedDict):
    query: str
    port: int
    system_name: str
    context: str
    fault_analysis: Dict[str, Any]
    formatted_report: str
    system_data: Dict[str, Any]
    system_metrics: Dict[str, Any]

# === Agent 1: Data Extraction Agent ===
def extract_relevant_data(state: AgentState) -> AgentState:
    """Extract relevant files and context for the given port and query."""
    query = state["query"]
    port_match = re.search(r'(?:system|port)\s+(\d+)', query.lower())
    port = int(port_match.group(1)) if port_match else 5000

    # Load system data
    data_dir = f"data_instance_{port}"
    system_data = {}
    system_metrics = {}
    context_parts = []

    if not os.path.exists(data_dir):
        context_parts.append(f"⚠️ Warning: Data directory {data_dir} not found")
        state["context"] = "\n\n".join(context_parts)
        state["port"] = port
        state["system_name"] = f"System_{port}"
        state["system_data"] = system_data
        state["system_metrics"] = system_metrics
        return state

    # System info
    system_file = f"{data_dir}/system.json"
    if os.path.exists(system_file):
        try:
            with open(system_file, 'r') as f:
                system_data_raw = json.load(f)
            if isinstance(system_data_raw, list) and len(system_data_raw) > 0:
                system_data = system_data_raw[0]
            else:
                system_data = system_data_raw
            system_name = system_data.get("name", f"System_{port}")
            context_parts.append(f"System Information:\n{json.dumps(system_data, indent=2)}")
        except Exception as e:
            context_parts.append(f"⚠️ Error loading system.json: {str(e)}")
            system_name = f"System_{port}"

    # Latest metrics
    metrics_file = f"{data_dir}/system_metrics.json"
    if os.path.exists(metrics_file):
        try:
            with open(metrics_file, 'r') as f:
                metrics_data = json.load(f)
            if metrics_data and isinstance(metrics_data, list) and len(metrics_data) > 0:
                system_metrics = metrics_data[-1]
                context_parts.append(f"Latest Metrics:\n{json.dumps(system_metrics, indent=2)}")
            else:
                context_parts.append(f"⚠️ Warning: system_metrics.json is empty or invalid")
        except Exception as e:
            context_parts.append(f"⚠️ Error loading system_metrics.json: {str(e)}")
    else:
        context_parts.append(f"⚠️ Warning: system_metrics.json not found")

    # Volumes info
    volumes_file = f"{data_dir}/volume.json"
    if os.path.exists(volumes_file):
        try:
            with open(volumes_file, 'r') as f:
                volumes_data = json.load(f)
            context_parts.append(f"Volumes Information:\n{json.dumps(volumes_data, indent=2)}")
        except Exception as e:
            context_parts.append(f"⚠️ Error loading volume.json: {str(e)}")

    # IO metrics
    io_metrics_file = f"{data_dir}/io_metrics.json"
    if os.path.exists(io_metrics_file):
        try:
            with open(io_metrics_file, 'r') as f:
                io_metrics_data = json.load(f)
            context_parts.append(f"IO Metrics:\n{json.dumps(io_metrics_data, indent=2)}")
        except Exception as e:
            context_parts.append(f"⚠️ Error loading io_metrics.json: {str(e)}")

    # Replication metrics
    replication_file = f"{data_dir}/replication_metrics.json"
    if os.path.exists(replication_file):
        try:
            with open(replication_file, 'r') as f:
                replication_data = json.load(f)
            context_parts.append(f"Replication Metrics:\n{json.dumps(replication_data, indent=2)}")
        except Exception as e:
            context_parts.append(f"⚠️ Error loading replication_metrics.json: {str(e)}")

    # Snapshots info
    snapshots_file = f"{data_dir}/snapshots.json"
    if os.path.exists(snapshots_file):
        try:
            with open(snapshots_file, 'r') as f:
                snapshots_data = json.load(f)
            context_parts.append(f"Snapshots Information:\n{json.dumps(snapshots_data, indent=2)}")
        except Exception as e:
            context_parts.append(f"⚠️ Error loading snapshots.json: {str(e)}")

    # Logs
    logs_file = f"{data_dir}/logs_{port}.txt"
    if os.path.exists(logs_file):
        try:
            with open(logs_file, 'r') as f:
                logs_content = f.read()[:1000]
            context_parts.append(f"System Logs:\n{logs_content}")
        except Exception as e:
            context_parts.append(f"⚠️ Error loading logs_{port}.txt: {str(e)}")

    state["context"] = "\n\n".join(context_parts)
    state["port"] = port
    state["system_name"] = system_name
    state["system_data"] = system_data
    state["system_metrics"] = system_metrics
    return state

# === Agent 2: Fault Analysis Agent ===
def analyze_fault(state: AgentState) -> AgentState:
    """Analyze the fault using the problem space's RAG logic and system data."""
    query = state["query"]
    context = state["context"]
    system_data = state["system_data"]
    system_metrics = state["system_metrics"]
    
    print("\n=== Analyze Fault Inputs ===")
    print(f"Query: {query}")
    print(f"System Data: {json.dumps(system_data, indent=2)}")
    print(f"System Metrics: {json.dumps(system_metrics, indent=2)}")

    # Flatten context for analysis
    def flatten_json(obj, prefix=""):
        lines = []
        if isinstance(obj, dict):
            for k, v in sorted(obj.items()):
                full_key = f"{prefix}.{k}" if prefix else k
                if isinstance(v, (dict, list)):
                    lines.extend(flatten_json(v, prefix=full_key))
                else:
                    lines.append(f"{full_key} = {v}")
        elif isinstance(obj, list):
            for idx, item in enumerate(obj):
                full_key = f"{prefix}[{idx}]"
                if isinstance(item, (dict, list)):
                    lines.extend(flatten_json(item, prefix=full_key))
                else:
                    lines.append(f"{full_key} = {item}")
        elif isinstance(obj, str):
            sections = obj.split("\n\n")
            for section in sections:
                if section.strip():
                    section_lines = section.strip().split('\n')
                    section_title = section_lines[0].strip()
                    section_content = section.strip()
                    lines.append(f"{prefix}.{section_title} = {section_content}")
        return lines

    flattened = flatten_json(context) if context else []
    formatted_input = "\n".join(flattened)

    # Construct analysis prompt
    analysis_prompt = ChatPromptTemplate.from_messages([
        SystemMessage(content=(
            f"You are an RCA assistant for the {PROBLEM_SPACE} domain. Based on the structured system data, system metrics, and RCA logic from the RAG document, diagnose the root cause of the issue described in the query. "
            "Steps:\n"
            "1. Apply the fault diagnosis rules from the RAG document to determine the fault type.\n"
            "2. Use system_metrics to infer key metrics where available.\n"
            "3. If system_metrics is empty, estimate metrics from volume.json or io_metrics.json.\n"
            "4. Calculate percentages as specified in the data model.\n"
            "5. Choose the tool based on the fault type and available metrics.\n"
            "6. Return only the highest causing fault or no fault if the thresholds are not matched.\n"
            "7. Include relevant details as per the data model.\n"
            "8. If replication metrics are available, check for replication issues as per the RAG document.\n"
            "9. Ensure the response is based solely on RAG logic, system_data, and system_metrics, without assuming hardcoded thresholds.\n"
            "10. Return a JSON object with the following structure:\n"
            "   - fault_analysis: Matches the data model structure.\n"
            "    - tool: {name: '<tool_name>', parameters: {'fault_analysis': <fault_analysis>, 'system_data': <system_data>}} .\n"
            "11. Available tools:\n" +
            "\n".join([f"- {t['name']}: {t['description']} (Parameters: {', '.join(t['parameters'])})" for t in TOOLS_CONFIG]) +
            "\n12. Do not include Python expressions or additional text in the JSON, include the details of all the volumes in the JSON.\n"
            "13. Perform proper reasoning based on the provided data and RAG logic; do not make assumptions.\n"
            "Return only the JSON object with the tool section filled compulsarily ."
        )),
        HumanMessage(content=(
            f"Query: {query}\n\n"
            f"Extracted system data:\n{formatted_input}\n\n"
            f"Expected fault_analysis structure:\n{json.dumps(DATA_MODEL, indent=2)}"
        ))
    ])

    # Retrieve relevant RAG chunks
    relevant_docs = retriever.invoke(query)
    context_with_rca = "\n".join([doc.page_content for doc in relevant_docs])
    
    # Update the system message with RAG context
    system_message = analysis_prompt.messages[0].content + f"\nRAG Logic:\n{context_with_rca}"
    
    # Create the final messages list
    messages = [
        SystemMessage(content=system_message),
        HumanMessage(content=analysis_prompt.messages[1].content)
    ]
    
    # Invoke the LLM with the messages
    print("\n=== Invoking LLM for Fault Analysis ===")
    response = llm.invoke(messages)
    print(f"Raw LLM Response: {response.content}")
    
    # Try to parse the JSON
    fault_analysis = None
    tool_spec = None
    raw_response = response.content
    try:
        response_json = json.loads(raw_response)
        fault_analysis = response_json.get("fault_analysis", {})
        tool_spec = response_json.get("tool")
    except json.JSONDecodeError:
        print("Error: Failed to parse LLM response as JSON, attempting to extract JSON")
        json_match = re.search(r'```json\n([\s\S]*?)\n```', raw_response)
        if json_match:
            json_str = json_match.group(1)
            json_str = re.sub(r'\((\d+)\s*/\s*(\d+)\)\s*\*\s*100', lambda m: str(int(m.group(1)) / int(m.group(2)) * 100), json_str)
            try:
                response_json = json.loads(json_str)
                fault_analysis = response_json.get("fault_analysis", {})
                tool_spec = response_json.get("tool")
            except json.JSONDecodeError as e:
                print(f"Error: Failed to parse extracted JSON: {e}")
                fault_analysis = {"error": "Invalid analysis output", "raw_result": raw_response}
        else:
            fault_analysis = {"error": "Invalid analysis output", "raw_result": raw_response}

    # Apply tool if specified
    if fault_analysis and not fault_analysis.get("error") and tool_spec:
        tool_name = tool_spec.get("name")
        parameters = tool_spec.get("parameters", {})
        if tool_name not in TOOLS:
            print(f"Error: Unknown tool '{tool_name}' specified by LLM")
            fault_analysis["error"] = f"Unknown tool: {tool_name}"
        else:
            tool = TOOLS[tool_name]
            # Validate required parameters
            missing_params = [p for p in tool['required'] if p not in parameters]
            if missing_params:
                print(f"Error: Missing required parameters for tool '{tool_name}': {missing_params}")
                fault_analysis["error"] = f"Missing parameters: {missing_params}"
            else:
                try:
                    # Prepare parameters
                    tool_params = {}
                    for param in tool['parameters']:
                        if param in parameters:
                            tool_params[param] = parameters[param]
                        elif param in state:
                            tool_params[param] = state[param]
                    fault_analysis = tool['run'](**tool_params)
                    print("\n=== Fault Analysis with Tool Contributions ===")
                    print(json.dumps(fault_analysis, indent=2))
                except Exception as e:
                    print(f"Error in tool execution: {e}")
                    fault_analysis["error"] = f"Tool execution failed: {str(e)}"

    state["fault_analysis"] = fault_analysis
    return state

# === Agent 3: Response Formatting Agent ===
def format_response(state: AgentState) -> AgentState:
    """Format the fault analysis into a human-readable report."""
    fault_analysis = state["fault_analysis"]
    system_name = state["system_name"]
    port = state["port"]

    formatting_prompt = ChatPromptTemplate.from_messages([
        SystemMessage(content=(
            f"Format the following JSON fault analysis into a concise, human-readable report for system {system_name} (Port: {port}) in the {PROBLEM_SPACE} domain. "
            "Include the fault type, key details, and relevant component information as per the data model. Use bullet points for components, issues, and contributions. "
            "Keep it clear, structured, and under 300 words. Avoid raw JSON or code-like formatting. "
            "Only include the highest causing fault and ensure the report is actionable. "
            "Use the contributions field from the JSON for consistent reporting. "
            "If contributions are empty or missing, indicate that contribution data is unavailable and suggest checking system configuration. "
            "Use the fault_analysis numbers only, don't make assumptions about the calculations.\n"
            "If there is no fault, skip the bully component section.\n"
            "Example format:\n"
            f"Fault Report for {system_name} (Port: {port})\n"
            "Fault Type: <type>\n"
            "Key Details: <metrics>\n"
            "Component Information: <details>\n"
            "Issues: <details>\n"
            "Contributions:\n"
            "- <component_name> (<component_id>): contribution: <percentage>%\n"
            "Bully Component: <component and contribution for the applicable fault>\n"
            "Next Actions: <detailed actions to be taken for the fault>\n"
        )),
        HumanMessage(content=f"JSON Analysis:\n{json.dumps(fault_analysis, indent=2)}")
    ])

    messages = [
        SystemMessage(content=formatting_prompt.messages[0].content),
        HumanMessage(content=formatting_prompt.messages[1].content)
    ]
    
    formatted_report = llm.invoke(messages).content
    state["formatted_report"] = formatted_report
    return state

# === LangGraph Workflow ===
workflow = StateGraph(AgentState)

workflow.add_node("extract_data", extract_relevant_data)
workflow.add_node("analyze_fault", analyze_fault)
workflow.add_node("format_response", format_response)

workflow.add_edge("extract_data", "analyze_fault")
workflow.add_edge("analyze_fault", "format_response")
workflow.add_edge("format_response", END)

workflow.set_entry_point("extract_data")

app = workflow.compile()

# === Main Loop ===
def main():
    print(f"\n✅ LangGraph Agentic Fault Detection System ({PROBLEM_SPACE})")
    print("Example queries:")
    print("- Why is system 5000 experiencing high latency?")
    print("- Check replication issues in system 5001")
    print("- Analyze snapshot capacity in system 5000")
    print("- Show faults across all systems")
    print("Type 'exit' to quit\n")

    while True:
        query = input("🔎 Enter your query: ").strip()
        if query.lower() in ("exit", "quit"):
            print("👋 Exiting. Take care!")
            break

        try:
            state = {"query": query, "port": 0, "system_name": "", "context": "", "fault_analysis": {}, "formatted_report": "", "system_data": {}, "system_metrics": {}}
            result = app.invoke(state)
            print("\n" + "="*50)
            print(result["formatted_report"])
            print("="*50 + "\n")
        except Exception as e:
            print(f"❌ Error during analysis: {e}")

if __name__ == "__main__":
    main()
