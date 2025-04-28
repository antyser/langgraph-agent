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
from langchain_core.messages import HumanMessage

# Configure logging - simplified to just relevant information
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Import necessary modules
from src.common.llm_models import GEMINI_2_5_FLASH_PREVIEW
from src.product_summary.graph import graph as product_summary_graph
from src.product_summary.state import InputState
from src.product_summary.graph import create_llm

# --- Product Data ---
PRODUCTS_TO_EVALUATE: List[Dict[str, Any]] = [
    {
        "url": "https://www.amazon.com/dp/B08MLG2SG4",
        "name": "Amara Smoothie Melts - Mango Carrot",
        "questions": [
            "1. 成分， 是否添加了糖或者别的非天然原料 (Ingredients, any added sugar or artificial ingredients?)",
            "2. 小朋友一天能吃多少 (How much can a child eat per day?)"
        ]
    },
    {
        "url": "https://www.amazon.com/Samsonite-Freeform-Hardside-Spinner-Black/dp/B01M0A3BKH/",
        "name": "Samsonite Freeform Hardside Carry-On",
        "questions": [
            "1. 是否耐用，表面是否容易刮花 (Is it durable? Does the surface scratch easily?)",
            "2. 轮子是否好滑 (Are the wheels smooth?)",
            "3. 是不是各个航空公司都允许登机 (Is it allowed as carry-on by most airlines?)"
        ]
    },
    {
        "url": "https://www.amazon.com/dp/B0CHN9X9S2",
        "name": "Sports Research Fish Oil Mini-Softgels",
        "questions": [
            "(需要知道怎么选鱼油) (Need to know how to choose fish oil)",
            "1. What is this for? Skin, brain?",
            "2. 有效成分是什么，相比于同类产品含量差别多少 (What are the active ingredients, how does the content compare to similar products?)",
            "3. 萃取方法 (Extraction method?)",
            "4. 鱼是否含有重金属 (Does the fish contain heavy metals?)",
            "5. 副作用？ (Side effects?)",
            "6. 牌子怎么样 (How is the brand reputation?)"
        ]
    },
    {
        "url": "https://www.amazon.com/dp/B003BHZ71G",
        "name": "NOW Supplements, Sunflower Lecithin",
        "questions": [
            "1. What is this for?",
            "2. Sources? Sunflower better than soy?",
            "3. 正常人每天应该吃多少 (How much should a normal person take daily?)",
            "4. 有没有副作用 (Are there side effects?)",
            "5. 牌子怎么样 (How is the brand reputation?)"
        ]
    },
    {
        "url": "https://www.amazon.com/Aquasana-3-Stage-Filter-System-Chrome/dp/B06XGY3G28/",
        "name": "Aquasana 3-Stage Water Filter",
        "questions": [
            "1. 滤水器到底能过滤什么有害物质 (What harmful substances does the filter remove?)",
            "2. 过滤完的水足够健康么？ (Is the filtered water healthy enough?)"
        ]
    },
    {
        "url": "https://www.amazon.com/CRZ-YOGA-Butterluxe-Racerback-Longline/dp/B0BKQ6HRLQ",
        "name": "CRZ YOGA Butterluxe Racerback",
        "questions": [
            "1. 是否适合跑步 (Is it suitable for running?)"
        ]
    },
    {
        "url": "https://www.amazon.com/Nest-T3007ES-Thermostat-Temperature-Generation/dp/B0131RG6VK",
        "name": "Nest Learning Thermostat",
        "questions": [
            "1. 如何安装 (How to install?)",
            "2. 是否需要额外收费 (Are there additional fees?)"
        ]
    },
    {
        "url": "https://www.amazon.com/Company-Conscious-Plant-Based-Hypoallergenic-Dermatologist/dp/B07SH6HN2X/",
        "name": "Honest Baby Wipes",
        "questions": [
            "1. 是否有刺激性物质 (Does it contain irritating substances?)",
            "2. 是否适合敏感肌肤小孩 (Is it suitable for children with sensitive skin?)"
        ]
    },
    {
        "url": "https://www.amazon.com/Millie-Moon-Diapers-COUCHES-22lbs-33lbs/dp/B0CHV6QYRV/",
        "name": "Millie Moon Diapers",
        "questions": [
            "1. 是否适合敏感肌肤小孩 (Is it suitable for children with sensitive skin?)",
            "2. 是否容易漏 (Does it leak easily?)"
        ]
    },
    {
        "url": "https://www.amazon.com/Keurig-K-Elite-Temperature-Capability-Programmable/dp/B078NN17K3",
        "name": "Keurig K-Elite Coffee Maker",
        "questions": [
            "1. 是否容易清洗 (Is it easy to clean?)"
        ]
    },
    {
        "url": "https://www.amazon.com/Insta360-Standard-Bundle-Waterproof-Stabilization/dp/B0DBQBMQH2/",
        "name": "Insta360 Ace Pro",
        "questions": [
            "1. 多久需要充电 (How long does the battery last/take to charge?)",
            "2. 照片导入是否方便 (Is importing photos/videos convenient?)",
            "3. 画质如何 (How is the image/video quality?)"
        ]
    },
    {
        "url": "https://www.amazon.com/Murad-Retinol-Youth-Renewal-Serum/dp/B01K629LDI/",
        "name": "Murad Retinol Youth Renewal Serum",
        "questions": [
            "1. 对什么样的皮肤有效 (What skin types is it effective for?)",
            "2. 多久才会有效 (How long does it take to see results?)",
            "3. 有什么样的效果 (What are the effects?)"
        ]
    },
    {
        "url": "https://www.amazon.com/Ninja-Capacity-Dehydrate-Technology-AF141/dp/B0CSZ7WBYW/",
        "name": "Ninja Air Fryer",
        "questions": [
            "1. 能够一次放多少东西 (How much can it hold at once?)",
            "2. 有什么样的功能 (What functions does it have?)"
        ]
    },
    {
        "url": "https://www.amazon.com/FIFINE-Microphone-Voice-Over-Windscreen-Amplitank-K688/dp/B0B8SNVK5K/",
        "name": "FIFINE USB/XLR Microphone K688",
        "questions": [
            "1. 音质是否够好 (Is the sound quality good enough?)"
        ]
    },
    {
        "url": "https://www.amazon.com/Apple-iPhone-16-Version-128GB/dp/B0DHJH2GZL/",
        "name": "Apple iPhone 16",
        "questions": [
            "1. Apple Intelligence 效果怎么样 (How well does Apple Intelligence work?)",
            "2. 和上一代比有什么不一样的 (What's different compared to the previous generation?)",
            "3. 和pro比有什么不一样 (What's different compared to the Pro model?)"
        ]
    },
    {
        "url": "https://www.amazon.com/Apple-iPhone-MagSafe-Camera-Control/dp/B0DGHH9WMX/",
        "name": "Apple iPhone 16 FineWoven Case",
        "questions": [
            "1. 厚度怎么样 (How thick is it?)",
            "2. 是否容易坏 (Does it break easily?)",
            "3. 是否容易脏 (Does it get dirty easily?)"
        ]
    },
    {
        "url": "https://www.amazon.com/dp/B0BJ62BW91",
        "name": "Gravol Kids Liquid",
        "questions": [
            "1. 效果如何 (How effective is it?)",
            "2. 有没有副作用 (Are there side effects?)"
        ]
    },
    {
        "url": "https://www.amazon.com/Orgain-Organic-Protein-Powder-Strawberries/dp/B09SJ4WJNV/",
        "name": "Orgain Organic Protein Powder",
        "questions": [
            "1. 是否会导致肠胃不适 (Does it cause gastrointestinal discomfort?)",
            "2. 有没有副作用 (Are there side effects?)"
        ]
    },
    {
        "url": "https://www.amazon.com/Quencher-Cupholder-Compatible-Insulated-Stainless/dp/B0DCDQ1RFV/",
        "name": "Stanley Quencher H2.0 FlowState Tumbler",
        "questions": [
            "1. 是否会有塑料的味道 (Does it have a plastic taste/smell?)",
            "2. 是否可以装热水 (Can it hold hot water?)",
            "3. 是否容易清洗 (Is it easy to clean?)"
        ]
    },
    {
        "url": "https://www.amazon.com/SENSARTE-Nonstick-Frying-Pan-Skillet/dp/B086PHS2V8/",
        "name": "SENSARTE Nonstick Frying Pan",
        "questions": [
            "1. 是否含有有害物质，特别是高温后或者放洗碗机后 (Does it contain harmful substances, especially after high heat or dishwasher use?)"
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
        eval_llm = create_llm(GEMINI_2_5_FLASH_PREVIEW)
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


async def evaluate_product(product_info: Dict[str, Any], graph: CompiledGraph) -> Dict[str, Any]:
    """
    Runs the product summary graph for a single product URL and captures just the 
    overall latency, summary content, and evaluation results.
    """
    url = product_info["url"]
    name = product_info.get("name", url)
    questions = product_info.get("questions", [])
    
    logger.info(f"Evaluating: {name}")
    
    # Run the graph and measure overall latency
    start_time = time.perf_counter()
    input_state = {"url": url}
    
    try:
        result = await graph.ainvoke(input_state)
        logger.info(f"Result: {result}")
        end_time = time.perf_counter()
        total_latency_ms = (end_time - start_time) * 1000
        # Extract the summary from the result
        messages = result.get("messages", [])
        if messages and hasattr(messages[-1], 'content'):
            summary = messages[-1].content
        else:
            summary = "No summary generated."
            
        # Evaluate if summary answers questions
        question_evaluations = await check_summary_answers_questions(summary, questions)
        
        # Log results
        logger.info(f"Latency: {total_latency_ms:.2f}ms")
        logger.info(f"Summary:\n{summary[:500]}..." if len(summary) > 500 else f"Summary:\n{summary}")
        
        # Log question evaluation results
        for i, (question, evaluation) in enumerate(zip(questions, question_evaluations)):
            question_short = question[:50] + "..." if len(question) > 50 else question
            logger.info(f"Q{i+1}: {question_short} - {evaluation.upper()}")
            
        return {
            "product": product_info,
            "summary": summary,
            "latency_ms": total_latency_ms,
            "question_evaluations": question_evaluations,
            "questions_answered": {
                "yes": question_evaluations.count("yes"),
                "partially": question_evaluations.count("partially"),
                "no": question_evaluations.count("no"),
                "unknown": question_evaluations.count("unknown"),
                "total": len(question_evaluations)
            }
        }
    
    except Exception as e:
        end_time = time.perf_counter()
        total_latency_ms = (end_time - start_time) * 1000
        logger.error(f"Error evaluating product {name}: {e}")
        
        return {
            "product": product_info,
            "summary": f"Error: {str(e)}",
            "latency_ms": total_latency_ms,
            "question_evaluations": ["unknown"] * len(questions),
            "questions_answered": {
                "yes": 0, "partially": 0, "no": 0, 
                "unknown": len(questions), "total": len(questions)
            },
            "error": str(e)
        }


async def main():
    """Main function to run the evaluation for all products."""
    results = []
    
    # Run evaluations sequentially
    for product in PRODUCTS_TO_EVALUATE:
        result = await evaluate_product(product, product_summary_graph)
        results.append(result)
        await asyncio.sleep(1)  # Short delay between products
    
    # Save results
    output_filename = "evaluation_results.json"
    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    # Write a simple summary log file
    summary_log_file = "evaluation_summary_log.txt"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open(summary_log_file, "a", encoding="utf-8") as f:
        f.write(f"\n\n{'=' * 50}\n")
        f.write(f"EVALUATION SUMMARY - {timestamp}\n")
        f.write(f"{'=' * 50}\n\n")
        
        for result in results:
            product_name = result["product"].get("name", "Unknown product")
            latency = result.get("latency_ms", 0)
            questions = result["product"].get("questions", [])
            yes_count = result["questions_answered"]["yes"]
            partially_count = result["questions_answered"]["partially"]
            
            f.write(f"Product: {product_name}\n")
            f.write(f"Latency: {latency:.2f}ms\n")
            f.write(f"Questions answered: {yes_count + partially_count}/{len(questions)}\n")
            f.write(f"Summary:\n{result['summary'][:500]}...\n\n")
    
    logger.info(f"Results saved to {output_filename} and {summary_log_file}")


if __name__ == "__main__":
    asyncio.run(main()) 