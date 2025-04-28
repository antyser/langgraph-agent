"""Script to evaluate the product summary agent graph with a list of products."""

import asyncio
import json
import logging
import os
import time
from datetime import datetime
from typing import Any, Dict, List, Optional, Literal
from typing_extensions import Annotated, TypedDict

from dotenv import load_dotenv
from langgraph.graph.graph import CompiledGraph
from langchain_core.messages import HumanMessage, BaseMessage

# Configure logging - simplified to just relevant information
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Import necessary modules
from src.common.llm_models import GEMINI_2_5_FLASH_PREVIEW, create_gemini
from src.product_summary.plan_graph import graph as plan_graph
from src.product_summary.graph import graph as scrape_graph
from src.common.callbacks import NodeLatencyCallback

# --- Product Data ---
PRODUCTS_TO_EVALUATE: List[Dict[str, Any]] = [
{
"url": "https://www.amazon.com/dp/B08MLG2SG4",
"name": "Amara Smoothie Melts - Mango Carrot",
"questions": [
"1. Ingredients & Allergens: Are there any added sugars, artificial ingredients, preservatives, or common allergens (like dairy, soy, nuts)?",
"2. Texture & Safety: Do they dissolve quickly and easily in a baby's/toddler's mouth to minimize choking risk?",
"3. Portion Size: What is a typical serving size, and how often is it recommended for toddlers?"
]
},
{
"url": "https://www.amazon.com/Samsonite-Freeform-Hardside-Spinner-Black/dp/B01M0A3BKH/",
"name": "Samsonite Freeform Hardside Carry-On",
"questions": [
"1. Durability: How well does the hardshell material hold up against cracking and scuffs during typical travel? Is scratching a common issue?",
"2. Wheels: Are the spinner wheels smooth and durable on various surfaces (airport floors, sidewalks)? Do they handle well when the bag is full?",
"3. Carry-On Compliance: Does this consistently meet the carry-on size restrictions for major US domestic and international airlines?",
"4. Weight & Capacity: Is it lightweight compared to similar hardside carry-ons? Does the interior offer practical packing space?"
]
},
{
"url": "https://www.amazon.com/dp/B0CHN9X9S2",
"name": "Sports Research Fish Oil Mini-Softgels",
"questions": [
"(Context: How to choose a good fish oil supplement?)",
"1. Benefits & Target Use: What specific health benefits is this fish oil primarily marketed for (e.g., heart health, brain function, joint support, general wellness)?",
"2. Active Ingredients (EPA/DHA) & Form: What are the exact amounts of EPA and DHA per serving? Is the oil in the more bioavailable triglyceride form? How does the concentration compare to other popular fish oil brands?",
"3. Purity & Quality Testing: Is it third-party tested for purity, specifically checking for heavy metals (mercury), PCBs, and dioxins? Are test results accessible?",
"4. Source & Sustainability: Where are the fish sourced from? Are they wild-caught and from sustainable sources?",
"5. Side Effects: Are fishy burps or digestive upset common side effects reported by users?",
"6. Brand Reputation: Is Sports Research considered a reputable brand known for quality supplements?"
]
},
{
"url": "https://www.amazon.com/dp/B003BHZ71G",
"name": "NOW Supplements, Sunflower Lecithin",
"questions": [
"1. Primary Uses/Benefits: What are the main reasons people take sunflower lecithin (e.g., brain health, liver support, improving cholesterol levels, emulsifier in cooking, breastfeeding support)?",
"2. Source Comparison: What are the perceived advantages of sunflower lecithin over soy lecithin (e.g., non-GMO, allergen concerns)?",
"3. Dosage: What is a typical daily dosage for general health support? Does it vary depending on the reason for taking it?",
"4. Potential Side Effects: Are there any common side effects associated with taking sunflower lecithin (e.g., digestive issues)?",
"5. Brand Reputation: Is NOW Supplements a well-regarded brand for quality and purity?"
]
},
{
"url": "https://www.amazon.com/Aquasana-3-Stage-Filter-System-Chrome/dp/B06XGY3G28/",
"name": "Aquasana 3-Stage Water Filter",
"questions": [
"1. Contaminant Removal: What specific contaminants does this filter system effectively reduce or remove (e.g., chlorine, lead, cysts, PFOA/PFOS, pharmaceuticals)? Does it retain beneficial minerals?",
"2. Filtered Water Quality: Does the filtered water taste noticeably better? Is it considered safe and healthy for drinking according to independent certifications (like NSF)?",
"3. Filter Lifespan & Cost: How long do the filters typically last, and what is the ongoing cost of replacement filters?",
"4. Installation & Maintenance: Is it reasonably easy to install for someone with basic DIY skills? Is filter replacement straightforward?"
]
},
{
"url": "https://www.amazon.com/CRZ-YOGA-Butterluxe-Racerback-Longline/dp/B0BKQ6HRLQ",
"name": "CRZ YOGA Butterluxe Racerback",
"questions": [
"1. Support Level: Is this top suitable for high-impact activities like running, or is it better suited for low-to-medium impact (yoga, weightlifting, casual wear)?",
"2. Fabric & Comfort: Is the 'Butterluxe' fabric genuinely soft, comfortable, and non-restrictive? Is it breathable and moisture-wicking during workouts?",
"3. Fit & Sizing: Does it generally run true to size? How is the fit in terms of coverage and length (is it truly longline)?",
"4. Durability: Does the fabric hold up well after multiple washes (e.g., no pilling, stretching, or fading)?"
]
},
{
"url": "https://www.amazon.com/Nest-T3007ES-Thermostat-Temperature-Generation/dp/B0131RG6VK",
"name": "Nest Learning Thermostat",
"questions": [
"1. Installation: How difficult is the installation process for an average homeowner? Does it require specific wiring (like a C-wire) for full functionality?",
"2. Compatibility: How can I check if it's compatible with my existing HVAC system (heating/cooling)?",
"3. Learning & Savings: Does the 'learning' feature actually adapt well to schedules and save energy/money as claimed? How much user input is needed initially?",
"4. Additional Fees: Are there any required subscription fees for basic remote control, scheduling, or learning features? (Note: Some advanced features might integrate with optional Nest Aware subscriptions for other Nest products)."
]
},
{
"url": "https://www.amazon.com/Company-Conscious-Plant-Based-Hypoallergenic-Dermatologist/dp/B07SH6HN2X/",
"name": "Honest Baby Wipes",
"questions": [
"1. Ingredients & Irritants: Does the ingredients list contain common irritants like alcohol, parabens, phthalates, or strong fragrances?",
"2. Sensitivity: Are they genuinely suitable for babies with sensitive skin or eczema, according to user reviews?",
"3. Texture & Wetness: Are the wipes thick and durable enough? Do they have the right amount of moisture (not too dry, not too wet)?",
"4. Dispensing: Do they dispense easily one at a time from the package?"
]
},
{
"url": "https://www.amazon.com/Millie-Moon-Diapers-COUCHES-22lbs-33lbs/dp/B0CHV6QYRV/",
"name": "Millie Moon Diapers",
"questions": [
"1. Sensitivity: Are these diapers generally well-tolerated by babies with sensitive skin? Do they contain potential irritants like fragrance or chlorine?",
"2. Leak Protection: How effective are they at preventing leaks, especially overnight or for active babies?",
"3. Softness & Fit: Are they noticeably soft inside and out? How is the fit and flexibility around the waist and legs?",
"4. Absorption: Do they absorb well and keep the baby feeling dry?"
]
},
{
"url": "https://www.amazon.com/Keurig-K-Elite-Temperature-Capability-Programmable/dp/B078NN17K3",
"name": "Keurig K-Elite Coffee Maker",
"questions": [
"1. Cleaning & Maintenance: How easy is it to clean the machine regularly? Does it require frequent descaling, and is that process simple?",
"2. Reliability & Lifespan: What is the general reliability and expected lifespan of this model based on user experiences?",
"3. Coffee Quality: Does it brew a consistently good-tasting cup of coffee? How does the 'Strong Brew' function perform?",
"4. Noise Level: Is the machine noisy during operation?"
]
},
{
"url": "https://www.amazon.com/Insta360-Standard-Bundle-Waterproof-Stabilization/dp/B0DBQBMQH2/",
"name": "Insta360 Ace Pro",
"questions": [
"1. Battery Life & Charging: How long does the battery typically last during continuous recording? How long does it take to fully charge?",
"2. Workflow & App Experience: How easy and fast is it to transfer footage (photos/videos) to a phone or computer? Is the companion app intuitive and feature-rich for editing?",
"3. Image & Video Quality: How good is the video quality in various lighting conditions (daylight, low light)? How effective is the stabilization (FlowState)? Is the image quality comparable to other top action cameras?",
"4. Durability & Waterproofing: Is it rugged enough for action sports? How reliable is the waterproofing without an extra case?"
]
},
{
"url": "https://www.amazon.com/Murad-Retinol-Youth-Renewal-Serum/dp/B01K629LDI/",
"name": "Murad Retinol Youth Renewal Serum",
"questions": [
"1. Target Skin Concerns & Types: What specific signs of aging does this serum target most effectively (e.g., fine lines, wrinkles, uneven texture, firmness)? Is it suitable for sensitive skin, or primarily for normal/tolerant skin types?",
"2. Time to See Results: Realistically, how long does it typically take users to see noticeable improvements in their skin?",
"3. Key Effects & Benefits: What are the most commonly reported positive effects (e.g., smoother skin, reduced lines, improved radiance)?",
"4. Potential Irritation: Given it contains retinol, how likely is it to cause initial irritation, redness, or peeling? Does the formula mitigate this effectively?",
"5. Value: Considering the price, do users feel it delivers results justifying the cost compared to other retinol serums?"
]
},
{
"url": "https://www.amazon.com/Ninja-Capacity-Dehydrate-Technology-AF141/dp/B0CSZ7WBYW/",
"name": "Ninja Air Fryer",
"questions": [
"1. Actual Capacity: How much food can it comfortably cook at once (e.g., how many chicken wings, servings of fries)? Is the 5.5 qt capacity practical?",
"2. Cooking Performance: How well does it perform its main functions (Air Fry, Roast, Bake, Reheat, Dehydrate)? Does it cook food evenly and make it crispy?",
"3. Ease of Use & Cleaning: Are the controls intuitive? Is the basket/crisper plate non-stick and easy to clean (dishwasher safe)?",
"4. Noise & Footprint: Is it loud during operation? What are its dimensions (how much counter space does it need)?"
]
},
{
"url": "https://www.amazon.com/FIFINE-Microphone-Voice-Over-Windscreen-Amplitank-K688/dp/B0B8SNVK5K/",
"name": "FIFINE USB/XLR Microphone K688",
"questions": [
"1. Sound Quality: How does the sound quality compare to other popular USB/XLR microphones in its price range? Is it suitable for podcasting, streaming, voice-overs, or music recording?",
"2. Ease of Use (USB): How simple is the plug-and-play setup using USB? Does it require special drivers?",
"3. Background Noise Rejection: How well does its cardioid pattern reject background noise and room echo?",
"4. Build Quality & Features: Is the microphone well-built? Do the onboard controls (mute, gain, headphone jack) work well?",
"5. XLR Performance: For users considering XLR, does it perform well when connected to an audio interface?"
]
},
{
"url": "https://www.amazon.com/Apple-iPhone-16-Version-128GB/dp/B0DHJH2GZL/",
"name": "Apple iPhone 16",
"questions": [
"1. Apple Intelligence: How useful and practical are the new AI features in real-world daily use? Do they significantly enhance the user experience?",
"2. Key Upgrades vs. iPhone 15: What are the most impactful improvements over the iPhone 15 (e.g., camera performance, battery life, processing speed, display quality, new hardware features like the Action/Capture button)?",
"3. Comparison vs. iPhone 16 Pro: What are the main functional differences compared to the iPhone 16 Pro? What key features are missing that might justify upgrading to the Pro (e.g., camera system, ProMotion display, processor)?",
"4. Battery Life: Is there a noticeable real-world improvement in battery life compared to the iPhone 15?",
"5. Camera Performance: How significant are the camera upgrades in terms of photo and video quality in various lighting conditions?"
]
},
{
"url": "https://www.amazon.com/Apple-iPhone-MagSafe-Camera-Control/dp/B0DGHH9WMX/",
"name": "Apple iPhone 16 FineWoven Case",
"questions": [
"1. Durability & Wear: How well does the FineWoven material hold up to daily use? Is it prone to scratches, scuffs, staining, or fraying easily?",
"2. Feel & Grip: How does the material feel in hand? Does it provide adequate grip, or is it slippery?",
"3. Thickness & Protection: Does the case add significant bulk to the phone? Does it offer reasonable drop protection for the screen and camera lenses?",
"4. Cleanliness: Does the material attract dust, lint, or get dirty easily? How easy is it to clean?"
]
},
{
"url": "https://www.amazon.com/dp/B0BJ62BW91",
"name": "Gravol Kids Liquid",
"questions": [
"1. Effectiveness: How quickly and effectively does it relieve nausea and vomiting in children (e.g., for motion sickness or stomach bugs)? How long do the effects last?",
"2. Side Effects: What are the most common side effects in children (e.g., drowsiness, dizziness, dry mouth)? Is it non-drowsy?",
"3. Taste & Acceptance: How palatable is the liquid for kids? Do children generally take it without fuss?",
"4. Dosage Accuracy: Is the included dosing tool easy and accurate to use?"
]
},
{
"url": "https://www.amazon.com/Orgain-Organic-Protein-Powder-Strawberries/dp/B09SJ4WJNV/",
"name": "Orgain Organic Protein Powder",
"questions": [
"1. Digestibility: Is this protein powder generally easy to digest? Do users commonly report bloating, gas, or other gastrointestinal discomfort?",
"2. Taste & Mixability: How is the taste and texture (especially the Strawberries & Cream flavor)? Does it mix well with liquids (water, milk) without clumping?",
"3. Ingredients & Allergens: Does it contain common allergens or ingredients some users might avoid (e.g., erythritol, stevia, gums)?",
"4. Effectiveness: Do users find it effective for its intended purpose (e.g., post-workout recovery, meal replacement, supplementing protein intake)?"
]
},
{
"url": "https://www.amazon.com/Quencher-Cupholder-Compatible-Insulated-Stainless/dp/B0DCDQ1RFV/",
"name": "Stanley Quencher H2.0 FlowState Tumbler",
"questions": [
"1. Taste/Smell: Does the tumbler or lid impart any plastic or metallic taste/smell to beverages?",
"2. Insulation Performance: How long does it actually keep drinks cold or hot in real-world conditions?",
"3. Leak Resistance: How leak-resistant is the FlowState lid in different positions? Is it safe to carry in a bag?",
"4. Ease of Cleaning: Is it easy to clean thoroughly, especially the lid mechanism? Is it dishwasher safe?",
"5. Durability: How well does the finish and overall construction hold up to regular use and potential drops?"
]
},
{
"url": "https://www.amazon.com/SENSARTE-Nonstick-Frying-Pan-Skillet/dp/B086PHS2V8/",
"name": "SENSARTE Nonstick Frying Pan",
"questions": [
"1. Nonstick Coating Safety: Is the nonstick coating made without PFOA, PFAS, lead, and cadmium? Is it safe at high cooking temperatures and after dishwasher use?",
"2. Nonstick Performance & Durability: How effective is the nonstick surface initially? How long does the nonstick property typically last with regular use and proper care?",
"3. Cooking Performance: Does the pan heat evenly? Is it suitable for various cooktops (induction compatible?)?",
"4. Ease of Cleaning: Is it genuinely easy to clean by hand? How does the nonstick surface hold up in the dishwasher (if recommended)?"
]
}
]

# Define TypedDict for structured outputs
class QuestionEvaluation(TypedDict):
    """Evaluation of whether a product summary answers specific questions."""
    evaluations: Annotated[List[Literal["yes", "no", "partially", "unknown"]], ..., 
                          "List of evaluations, one for each question. Must be one of: yes, no, partially, unknown"]


async def check_summary_answers_questions(summary: str, questions: List[str]) -> List[str]:
    """
    Evaluates whether the product summary adequately answers each question.
    
    Args:
        summary: The product summary text generated by the agent.
        questions: List of questions to check against the summary.
        
    Returns:
        List of statuses ("yes", "no", "partially", "unknown") corresponding to each question.
    """
    if not summary or summary == "No summary generated.":
        return ["unknown"] * len(questions)
        
    try:
        # Create LLM and configure for structured output
        eval_llm = create_gemini()
        structured_llm = eval_llm.with_structured_output(QuestionEvaluation)
        
        # Prepare a concise prompt
        prompt = f"""Evaluate if this product summary answers these questions:

Summary:
---
{summary}
---

Questions:
{chr(10).join([f"{i+1}. {q}" for i, q in enumerate(questions)])}

Return evaluations as: yes (clearly answers), no (doesn't address), partially (touches on it), or unknown (can't determine).
"""
        
        # Call the evaluation LLM with structured output
        result = await structured_llm.ainvoke([HumanMessage(content=prompt)])
        evaluations = result["evaluations"]
        return evaluations
    except Exception as e:
        logger.error(f"Evaluation error: {e}")
        return ["unknown"] * len(questions)


async def evaluate_product(
    product_info: Dict[str, Any],
    graph_to_run: CompiledGraph, # Pass the actual graph object
    latency_callback: NodeLatencyCallback
) -> Dict[str, Any]:
    """
    Runs a specific product summary graph for a single product, captures summary,
    evaluates questions, and records latencies using the callback handler.
    """
    name = product_info.get("name", product_info["url"])
    url = product_info["url"]
    questions = product_info.get("questions", [])
    # Attempt to get a meaningful name for logging/reporting
    graph_name = getattr(graph_to_run, 'name', None) or getattr(graph_to_run, '__name__', 'unknown_graph')

    logger.info(f"Evaluating [{graph_name}]: {name}")

    # Reset callback for this run
    latency_callback.reset()

    # Determine input based on graph type by inspecting the input schema
    input_keys = list(graph_to_run.input_schema.schema().get('properties', {}).keys())
    if "product" in input_keys:
        input_state = {"product": name}
        graph_type = "plan"
    elif "url" in input_keys:
        input_state = {"url": url}
        graph_type = "scrape"
    else:
        logger.error(f"Cannot determine input schema for graph {graph_name}. Skipping.")
        return { # Return a minimal error structure
            "graph_type": "unknown",
            "product": product_info,
            "summary": "Error: Unknown graph input schema",
            "latency_ms": 0,
            "plan_latency": None,
            "search_latency": None,
            "summary_latency": None,
            "question_evaluations": ["unknown"] * len(questions),
            "questions_answered": {"yes": 0, "partially": 0, "no": 0, "unknown": len(questions), "total": len(questions)},
            "error": "Unknown graph input schema"
        }

    # Overall timing still useful for total execution including setup/teardown
    start_time = time.perf_counter()
    node_latencies: Dict[str, float] = {}
    summary = "No summary generated."
    error_str: Optional[str] = None
    result: Optional[Dict[str, Any]] = None

    try:
        # Run the graph with the latency callback
        result = await graph_to_run.ainvoke(
            input_state,
            config={"callbacks": [latency_callback]}
        )
        # logger.info(f"Result: {result}") # Can be verbose

        # Get latencies recorded by the callback (only plan_graph populates these)
        node_latencies = latency_callback.get_last_run_report()
        if node_latencies:
            latency_callback.print_last_run_report() # Log the node latencies if any

        # Extract the summary based on graph type
        if graph_type == "plan":
             summary = result.get("summary", "No summary generated.")
        elif graph_type == "scrape":
             # Assuming scrape_graph returns state with 'messages' list
             messages: List[BaseMessage] = result.get("messages", [])
             if messages and hasattr(messages[-1], 'content'):
                 summary = messages[-1].content
             else:
                 summary = "Summary not found in messages."
        else:
             summary = "Error: Could not determine summary extraction method."

    except Exception as e:
        logger.error(f"Error invoking {graph_name} for product {name}: {e}", exc_info=True)
        error_str = str(e)
        # Still print any partial latencies captured before the error
        if latency_callback.get_last_run_report():
             latency_callback.print_last_run_report()
        node_latencies = latency_callback.get_last_run_report()

    finally:
        end_time = time.perf_counter()
        total_latency_ms = (end_time - start_time) * 1000
        logger.info(f"Total invoke latency for [{graph_name}] {name}: {total_latency_ms:.2f}ms")

    # Evaluate if summary answers questions (even if there was an error)
    question_evaluations = await check_summary_answers_questions(summary, questions)

    # Log summary and question evaluation results
    logger.info(f"Summary ({graph_name}):\n{summary[:500]}..." if len(summary) > 500 else f"Summary ({graph_name}):\n{summary}")
    for i, (question, evaluation) in enumerate(zip(questions, question_evaluations)):
        question_short = question[:50] + "..." if len(question) > 50 else question
        logger.info(f"Q{i+1} ({graph_name}): {question_short} - {evaluation.upper()}")

    # Prepare final result dict
    eval_result = {
        "graph_type": graph_type,
        "product": product_info,
        "summary": summary,
        "latency_ms": total_latency_ms, # Overall invoke time
        # Node latencies will only be present for plan_graph
        "plan_latency": node_latencies.get("plan"),
        "search_latency": node_latencies.get("search"),
        "summary_latency": node_latencies.get("summarize"),
        "question_evaluations": question_evaluations,
        "questions_answered": {
            "yes": question_evaluations.count("yes"),
            "partially": question_evaluations.count("partially"),
            "no": question_evaluations.count("no"),
            "unknown": question_evaluations.count("unknown"),
            "total": len(question_evaluations)
        }
    }
    if error_str:
        eval_result["error"] = error_str

    return eval_result


async def main():
    """Main function to run the evaluation for all products across multiple graphs."""
    
    graphs_to_evaluate = {
        "scrape": scrape_graph
    }
    all_results: Dict[str, List[Dict[str, Any]]] = {name: [] for name in graphs_to_evaluate}
    
    # Instantiate the callback handler once
    latency_callback = NodeLatencyCallback()
    
    # Loop through each graph type
    for graph_key, graph_obj in graphs_to_evaluate.items():
        logger.info(f"\n{'='*20} Starting Evaluation for Graph: {graph_key.upper()} {'='*20}\n")
        current_graph_results = []
        # Run evaluations sequentially for each product for the current graph
        for product in PRODUCTS_TO_EVALUATE:
            # Pass the callback instance and the current graph object
            result = await evaluate_product(product, graph_obj, latency_callback)
            current_graph_results.append(result)
            # await asyncio.sleep(0.1) # Small delay if needed for API limits/logging
        
        all_results[graph_key] = current_graph_results
        
        # --- Save results for the current graph ---
        output_filename = f"evaluation_results_{graph_key}.json"
        try:
            with open(output_filename, "w", encoding="utf-8") as f:
                json.dump(current_graph_results, f, indent=2, ensure_ascii=False)
            logger.info(f"Results for graph '{graph_key}' saved to {output_filename}")
        except IOError as e:
            logger.error(f"Failed to save JSON results for graph '{graph_key}': {e}")

    # --- Write combined summary log file ---
    summary_log_file = "evaluation_summary_log.txt"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    try:
        with open(summary_log_file, "a", encoding="utf-8") as f:
            f.write(f"\n\n{'=' * 60}\n")
            f.write(f"COMBINED EVALUATION SUMMARY - {timestamp}\n")
            f.write(f"{'=' * 60}\n")

            for graph_key, results in all_results.items():
                f.write(f"\n\n--- SUMMARY FOR GRAPH: {graph_key.upper()} ---\n")
                if not results:
                    f.write("No results found for this graph.\n")
                    continue

                total_overall_latency = 0
                total_plan_latency = 0
                total_search_latency = 0
                total_summary_latency = 0
                num_products = len(results)
                valid_plan_latency_count = 0
                valid_search_latency_count = 0
                valid_summary_latency_count = 0
                
                for result in results:
                    latency = result.get("latency_ms", 0)
                    plan_latency = result.get("plan_latency")
                    search_latency = result.get("search_latency")
                    summary_latency = result.get("summary_latency")
                    
                    total_overall_latency += latency
                    if plan_latency is not None: 
                        total_plan_latency += plan_latency
                        valid_plan_latency_count += 1
                    if search_latency is not None: 
                        total_search_latency += search_latency
                        valid_search_latency_count += 1
                    if summary_latency is not None: 
                        total_summary_latency += summary_latency
                        valid_summary_latency_count += 1
                
                # Write overall averages for this graph
                f.write(f"Average Overall Latency: {total_overall_latency / num_products:.2f}ms\n")
                if valid_plan_latency_count > 0:
                     f.write(f"Average Plan Node Latency: {total_plan_latency / valid_plan_latency_count:.3f}s\n")
                if valid_search_latency_count > 0:
                     f.write(f"Average Search Node Latency: {total_search_latency / valid_search_latency_count:.3f}s\n")
                if valid_summary_latency_count > 0:
                     f.write(f"Average Summary Node Latency: {total_summary_latency / valid_summary_latency_count:.3f}s\n")
                
                f.write("\n--- Individual Product Details ---\n")
                for i, result in enumerate(results):
                    product_name = result["product"].get("name", "Unknown product")
                    latency = result.get("latency_ms", 0)
                    questions = result["product"].get("questions", [])
                    yes_count = result["questions_answered"]["yes"]
                    partially_count = result["questions_answered"]["partially"]
                    
                    f.write(f"\n{i+1}. Product: {product_name}\n")
                    f.write(f"   Overall Latency: {latency:.2f}ms\n")
                    # Log individual node latencies if available
                    plan_lat = result.get("plan_latency")
                    search_lat = result.get("search_latency")
                    summary_lat = result.get("summary_latency")
                    if plan_lat is not None or search_lat is not None or summary_lat is not None:
                         f.write(f"   Node Latencies (P/S/Sum): "
                                 f"{f'{plan_lat:.3f}s' if plan_lat else 'N/A'} / "
                                 f"{f'{search_lat:.3f}s' if search_lat else 'N/A'} / "
                                 f"{f'{summary_lat:.3f}s' if summary_lat else 'N/A'}\n")
                                 
                    f.write(f"   Questions answered: {yes_count + partially_count}/{len(questions)}\n")
                    f.write(f"   Summary Snippet:\n     {result['summary'][:150].replace('\n', ' ')}...\n")
                    if "error" in result:
                        f.write(f"   ERROR: {result['error']}\n")
            
            f.write(f"\n{'=' * 60}\n")

        logger.info(f"Combined summary log saved to {summary_log_file}")

    except IOError as e:
        logger.error(f"Failed to write to summary log file {summary_log_file}: {e}")


if __name__ == "__main__":
    asyncio.run(main()) 