import json
import numpy as np # For safe averaging

# Load the data
with open("evaluation_results_scrape.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# --- Calculations for Summary --- 

total_products = len(data)
total_latency_ms = 0
total_plan_latency = 0
total_search_latency = 0
total_summary_latency = 0
total_score = 0
total_questions = 0

valid_plan_latency_count = 0
valid_search_latency_count = 0
valid_summary_latency_count = 0

score_map = {
    "yes": 1.0,
    "partially": 0.5,
    "no": 0.0,
    "unknown": 0.0
}

emoji_map = {
     "yes": "✅",
     "partially": "🤏",
     "no": "❌",
     "unknown": "❓"
}

for item in data:
    total_latency_ms += item.get("latency_ms", 0)
    
    plan_lat = item.get("plan_latency")
    if plan_lat is not None:
        total_plan_latency += plan_lat
        valid_plan_latency_count += 1
        
    search_lat = item.get("search_latency")
    if search_lat is not None:
        total_search_latency += search_lat
        valid_search_latency_count += 1
        
    summary_lat = item.get("summary_latency")
    if summary_lat is not None:
        total_summary_latency += summary_lat
        valid_summary_latency_count += 1
        
    num_q = item["questions_answered"]["total"]
    if num_q > 0:
        # Ensure all answers are valid keys before scoring
        valid_answers = [ans for ans in item["question_evaluations"] if ans in score_map]
        product_score = sum(score_map[ans] for ans in valid_answers)
        total_score += product_score
        total_questions += num_q # Count total questions even if some answers were invalid for scoring

# Calculate Averages safely
avg_latency_ms = total_latency_ms / total_products if total_products > 0 else 0
avg_plan_latency = total_plan_latency / valid_plan_latency_count if valid_plan_latency_count > 0 else 0
avg_search_latency = total_search_latency / valid_search_latency_count if valid_search_latency_count > 0 else 0
avg_summary_latency = total_summary_latency / valid_summary_latency_count if valid_summary_latency_count > 0 else 0
avg_score_percentage = (total_score / total_questions * 100) if total_questions > 0 else 0

# --- Generate Summary Table Markdown (Part 1) --- 

summary_table_md = "## Evaluation Summary\n\n"
summary_table_header = [
    "Metric", "Average Value"
]
summary_table_rows = [
    ["Avg Overall Latency", f"{avg_latency_ms:.2f} ms"],
    ["Avg Plan Node Latency", f"{avg_plan_latency:.3f} s"],
    ["Avg Search Node Latency", f"{avg_search_latency:.3f} s"],
    ["Avg Summary Node Latency", f"{avg_summary_latency:.3f} s"],
    ["Avg Question Score", f"{avg_score_percentage:.1f}% ({total_score:.1f}/{total_questions})"]
]

summary_table_md += "| " + " | ".join(summary_table_header) + " |\n"
summary_table_md += "|:---|:---|\n" # Add alignment specifiers
for row in summary_table_rows:
    # Escape pipes in cell content just in case
    cells = [str(cell).replace("|", "\\|") for cell in row]
    summary_table_md += "| " + " | ".join(cells) + " |\n"


# --- Generate Individual Results Table Markdown (Part 2) ---

individual_table_md = "\n## Individual Product Results\n\n"
# Update header for the last column
individual_header = ["URL", "Product Name", "Question Evaluations", "Latencies (Plan/Search/Summary/Total)"]
individual_table_md += "| " + " | ".join(individual_header) + " |\n"
# Add alignment specifiers
individual_table_md += "|:---|:---|:---|:---|\n"

for item in data:
    url = item["product"]["url"]
    name = item["product"]["name"]
    questions = item["product"]["questions"]
    answers = item["question_evaluations"]
    
    # Format evaluation with emojis using single <br>
    evaluation_lines = []
    for q, a in zip(questions, answers):
        emoji = emoji_map.get(a, "❓")
        # Escape markdown characters in question
        q_escaped = q.replace("|", "\\|").replace("\n", " ") # Replace newline with space
        evaluation_lines.append(f"{emoji} **{a.upper()}**: {q_escaped}")
    # Use single <br> for line breaks between questions within the cell
    evaluation_str = "<br>".join(evaluation_lines)
    
    # Format latencies into a single cell
    plan_lat_str = f"{item.get('plan_latency'):.3f}s" if item.get("plan_latency") is not None else "N/A"
    search_lat_str = f"{item.get('search_latency'):.3f}s" if item.get("search_latency") is not None else "N/A"
    summary_lat_str = f"{item.get('summary_latency'):.3f}s" if item.get("summary_latency") is not None else "N/A"
    total_lat_str = f"{item.get('latency_ms', 0):.0f}ms"
    latency_str = f"Plan: {plan_lat_str}<br>Search: {search_lat_str}<br>Summary: {summary_lat_str}<br>**Total: {total_lat_str}**"
    
    # Escape pipes in other fields
    url = url.replace("|", "\\|")
    name = name.replace("|", "\\|")
    
    # Construct the row for the individual results table
    row = [url, name, evaluation_str, latency_str]
    individual_table_md += "| " + " | ".join(row) + " |\n"

# --- Generate Individual Summaries Section (Part 3) ---

summary_section_md = "\n## Individual Product Summaries\n\n"
for i, item in enumerate(data):
    name = item["product"]["name"]
    summary = item.get("summary", "*No summary generated or error occurred.*")
    # Escape potential markdown in summary if needed, or display as is
    # For now, display as is but add separators
    summary_section_md += f"### {i+1}. {name}\n\n"
    summary_section_md += f"{summary}\n\n"
    summary_section_md += "---\n\n" # Add a horizontal rule between summaries

# --- Combine and Write Output --- 

# Combine: Summary Table + Individual Table + Individual Summaries
final_md = summary_table_md + "\n" + individual_table_md + "\n" + summary_section_md

with open("evaluation_results.md", "w", encoding="utf-8") as f:
    f.write(final_md)

print("Markdown report saved to evaluation_results.md")