import json

with open("evaluation_results.json", "r", encoding="utf-8") as f:
    data = json.load(f)

rows = []
for item in data:
    url = item["product"]["url"]
    name = item["product"]["name"]
    questions = item["product"]["questions"]
    answers = item["question_evaluations"]
    summary = item["summary"].replace("\n", " ")  # Remove newlines for table
    latency = item["latency_ms"]
    evaluation = "<br>".join(
        f"{q} - {a}" for q, a in zip(questions, answers)
    )
    rows.append([url, name, evaluation, summary, f"{latency:.0f}"])

# Markdown table header
header = ["url", "name", "evaluation", "summary", "latency_ms"]
md = "| " + " | ".join(header) + " |\n"
md += "|---" * len(header) + "|\n"

# Markdown table rows
for row in rows:
    # Escape pipes in summary/evaluation
    row = [str(cell).replace("|", "\\|") for cell in row]
    md += "| " + " | ".join(row) + " |\n"

with open("evaluation_results.md", "w", encoding="utf-8") as f:
    f.write(md)

print("Markdown table saved to evaluation_results.md")