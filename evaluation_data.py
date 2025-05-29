"""Evaluation data for the product summary graph."""

from typing import Any, Dict, List

GENERAL_EVALUATION_RUBRICS_V2: List[str] = [
    # ── A. HEADER FORMAT ────────────────────────────────────────────
    "A1. Every required top-level section header (Pros, Cons, Mixed Reviews, Who it’s for, Who it’s not for, Usage/Care Tips, Specific Use-Case, Insights vs. Similar Products) is present.",
    "A2. Every top-level header is bold (wrapped in **).",
    "A3. Every top-level header appears alone on its own line, with no text or bullet on the same line.",
    
    # ── B. BULLET FORMAT ────────────────────────────────────────────
    "B1. Under every top-level header, *all* content is written as bullet points (no paragraphs or numbered lists).",
    "B2. Each bullet begins with a bold keyword (≤ 4 words) that ends with a single colon ‘:’.",
    "B3. After the colon, the description follows on the *same* line and is ≤ 25 words.",
    
    # ── C. INTRO SENTENCE ───────────────────────────────────────────
    "C1. The analysis opens with exactly one sentence in the form: \"Here's an analysis of [PRODUCT TITLE] based on the information available:\"",

    # ── D. CONTENT QUALITY & RELEVANCE ──────────────────────────────
    "D1. Bullet points focus on high-impact, decision-making factors repeatedly cited by experts or users (no trivial colour/size notes unless they are deal-breakers).",
    
    # ── E. CATEGORY PLACEMENT ───────────────────────────────────────
    "E1. *Pros* list contains only positive points (no negatives, no mixed).",
    "E2. *Cons* list contains only negative points (no positives, no mixed).",
    "E3. *Mixed Reviews* list contains only points that have BOTH positive and negative aspects, and such points do **not** appear in Pros or Cons.",
    "E4. Pros, Cons, and Mixed Reviews are three independent, clearly labelled lists (no sub-bullets that mix categories).",
    
    # ── F. USER PROFILE COVERAGE ────────────────────────────────────
    "F1. The *Who it’s for* bullets reference at least one age group **or** life stage (e.g., seniors, toddlers, college students).",
    "F2. The *Who it’s for* bullets mention at least one lifestyle/situation (e.g., frequent travellers, apartment dwellers, budget-conscious shoppers).",
    "F3. The *Who it’s for* OR *Who it’s not for* bullets mention budget level (e.g., premium price, budget-friendly).",
    
    # ── G. COMPARISON WITH COMPETITORS ──────────────────────────────
    "G1. *Insights vs. Similar Products* names at least one specific competing brand or model.",
    "G2. For each competitor named, the bullet states a clear differentiator (better, worse, unique feature, or price gap).",
    
    # ── H. WORD COUNT ───────────────────────────────────────────────
    "H1. Total word count of the output is between 500 and 700 words, inclusive.",
]

COVERAGE_TO_EVALUATE: List[Dict[str, Any]] =[
    {
        "url": "https://www.amazon.com/dp/B08MLG2SG4",
        "name": "Amara Smoothie Melts – Mango Carrot",
        "questions": [
            "1. Clean ingredients & no added sugar?",
            "2. Allergen transparency (dairy / soy / nut / gluten)?",
            "3. Dissolvability & choking-risk explanation?",
            "4. Recommended age range stated?",
            "5. Parent/kid taste feedback included?",
            "6. Value versus other toddler melt or pouch snacks?"
        ],
    },
    {
        "url": "https://www.amazon.com/Samsonite-Freeform-Hardside-Spinner-Black/dp/B01M0A3BKH/",
        "name": "Samsonite Freeform Hardside Carry-On",
        "questions": [
            "1. Polypropylene shell & crack/scuff resistance covered?",
            "2. Exact weight and carry-on dimensions listed?",
            "3. Dual-spinner wheel quality & maneuverability described?",
            "4. Telescopic-handle sturdiness and TSA lock noted?",
            "5. Interior dividers/straps detailed?",
            "6. Value compared with similar hard-side carry-ons?"
        ],
    },
    {
        "url": "https://www.amazon.com/dp/B0CHN9X9S2",
        "name": "Sports Research Fish Oil Mini-Softgels",
        "questions": [
            "1. EPA+DHA milligrams per serving stated?",
            "2. Natural triglyceride form specified?",
            "3. Purity & sustainability certifications (e.g., IFOS, MSC) cited?",
            "4. Wild-caught source identified?",
            "5. Burp-free / digestion comfort mentioned?",
            "6. Cost per gram omega-3 benchmarked against other mass-market brands?"
        ],
    },
    {
        "url": "https://www.amazon.com/dp/B003BHZ71G",
        "name": "NOW Sunflower Lecithin 1 200 mg",
        "questions": [
            "1. Lecithin & phosphatidylcholine mg per serving listed?",
            "2. Soy-free, non-GMO advantage explained?",
            "3. Product form and typical daily dosage guidance provided?",
            "4. GMP / purity testing or allergen-free status noted?",
            "5. Potential digestive side-effect mention?",
            "6. Value comparison versus soy-based lecithin?"
        ],
    },
    {
        "url": "https://www.amazon.com/Aquasana-3-Stage-Filter-System-Chrome/dp/B06XGY3G28/",
        "name": "Aquasana Claryum 3-Stage Max-Flow",
        "questions": [
            "1. NSF-certified contaminant reduction (lead, PFAS, etc.) specified?",
            "2. Filter lifespan & replacement-cartridge cost stated?",
            "3. 0.72 GPM flow-rate advantage quantified?",
            "4. DIY install & tool-free filter-swap ease described?",
            "5. Annual operating cost versus other under-sink systems?",
            "6. Warranty period clearly stated?"
        ],
    },
    {
        "url": "https://www.amazon.com/CRZ-YOGA-Butterluxe-Racerback-Longline/dp/B0BKQ6HRLQ",
        "name": "CRZ YOGA Butterluxe Racerback Tank",
        "questions": [
            "1. Butterluxe softness & comparison to Lululemon Align covered?",
            "2. Support level and removable-pad built-in bra noted?",
            "3. Fit and sizing guidance provided?",
            "4. Durability / pilling feedback included?",
            "5. Breathability & moisture-wicking stated?",
            "6. Price/value compared with premium workout tops?"
        ],
    },
    {
        "url": "https://www.amazon.com/dp/B0131RG6VK",
        "name": "Nest Learning Thermostat (3rd Gen)",
        "questions": [
            "1. DIY installation difficulty & C-wire requirement explained?",
            "2. HVAC compatibility range listed?",
            "3. Learning auto-schedule & typical energy-savings percent cited?",
            "4. App usability and remote-control reliability covered?",
            "5. Subscription-fee disclosure (core functions free) included?",
            "6. Common reliability or Wi-Fi issues mentioned?"
        ],
    },
    {
        "url": "https://www.amazon.com/Company-Conscious-Plant-Based-Hypoallergenic-Dermatologist/dp/B07SH6HN2X/",
        "name": "Honest Clean Conscious Baby Wipes",
        "questions": [
            "1. No alcohol, parabens, fragrances, etc. confirmed?",
            "2. Compostable plant-based material and eco certifications noted?",
            "3. Thickness, strength, and moisture retention described?",
            "4. Suitability for sensitive/eczema-prone skin addressed?",
            "5. One-hand single-wipe dispensing performance covered?",
            "6. Cost per wipe compared with other premium baby wipes?"
        ],
    },
    {
        "url": "https://www.amazon.com/Millie-Moon-Diapers-COUCHES-22lbs-33lbs/dp/B0CHV6QYRV/",
        "name": "Millie Moon Diapers",
        "questions": [
            "1. Overnight leak-protection performance validated?",
            "2. Cloud-soft, hypoallergenic materials (no chlorine/fragrance) noted?",
            "3. Wetness-indicator accuracy discussed?",
            "4. Fit & sizing guidance for different body types provided?",
            "5. Absorption speed / skin-dryness effectiveness explained?",
            "6. Price compared with other premium diaper brands?"
        ],
    },
    {
        "url": "https://www.amazon.com/Keurig-K-Elite-Temperature-Capability-Programmable/dp/B078NN17K3",
        "name": "Keurig K-Elite Coffee Maker",
        "questions": [
            "1. Brew-temperature range & Strong/Iced mode impact covered?",
            "2. 75 oz reservoir capacity and cleaning ease noted?",
            "3. Descaling frequency prompts explained?",
            "4. Reliability and expected lifespan discussed?",
            "5. Noise level and sub-1-minute brew speed described?",
            "6. Compatibility with reusable or third-party pods confirmed?"
        ],
    },
    {
        "url": "https://www.amazon.com/Insta360-Standard-Bundle-Waterproof-Stabilization/dp/B0DBQBMQH2/",
        "name": "Insta360 Ace Pro Action Cam",
        "questions": [
            "1. Daylight and low-light 4 K video quality (1/1.3″ sensor) detailed?",
            "2. FlowState stabilization & horizon leveling effectiveness described?",
            "3. Battery life at 4 K 60 fps stated?",
            "4. Ruggedness & 33 ft waterproof rating covered?",
            "5. App workflow and AI editing ease discussed?",
            "6. Overheating behaviour or limits mentioned?"
        ],
    },
    {
        "url": "https://www.amazon.com/Murad-Retinol-Youth-Renewal-Serum/dp/B01K629LDI/",
        "name": "Murad Retinol Youth Renewal Serum",
        "questions": [
            "1. Tri-Active retinol technology explained?",
            "2. Timeframe for visible results given?",
            "3. Irritation-mitigation ingredients & nightly-use suitability covered?",
            "4. Lightweight texture & fast absorption described?",
            "5. Airless-pump packaging benefit noted?",
            "6. Price/value versus other OTC retinol serums discussed?"
        ],
    },
    {
        "url": "https://www.amazon.com/Ninja-Capacity-Dehydrate-Technology-AF141/dp/B0CSZ7WBYW/",
        "name": "Ninja AF141 5-Qt Air Fryer",
        "questions": [
            "1. Air-fry performance and even crisping results detailed?",
            "2. Real-world capacity expressed in pounds of food?",
            "3. Cleanup ease & dishwasher-safe parts mentioned?",
            "4. Preheat time and overall cook-speed compared to oven/competitors?",
            "5. Noise level and initial plastic-smell reports addressed?",
            "6. Control-panel intuitiveness described?"
        ],
    },
    {
        "url": "https://www.amazon.com/FIFINE-Microphone-Voice-Over-Windscreen-Amplitank-K688/dp/B0B8SNVK5K/",
        "name": "FIFINE K688 USB/XLR Microphone",
        "questions": [
            "1. Voice sound quality via USB and XLR detailed?",
            "2. Cardioid dynamic background-noise rejection explained?",
            "3. On-board mute/gain and zero-latency monitoring covered?",
            "4. Metal build and included shock-mount/pop filter described?",
            "5. Self-noise or gain-requirement info provided?",
            "6. Price/performance versus similar broadcast-style mics discussed?"
        ],
    },
    {
        "url": "https://www.amazon.com/Apple-iPhone-16-Version-128GB/dp/B0DHJH2GZL/",
        "name": "Apple iPhone 16",
        "questions": [
            "1. A18 chip & Apple-Intelligence benefits illustrated?",
            "2. Camera improvements over iPhone 15 detailed?",
            "3. Battery-life increase over iPhone 15 quantified?",
            "4. Action-button practical utility explained?",
            "5. Key missing features versus iPhone 16 Pro listed?",
            "6. Launch-price change versus prior model highlighted?"
        ],
    },
    {
        "url": "https://www.amazon.com/Apple-iPhone-MagSafe-Camera-Control/dp/B0DGHH9WMX/",
        "name": "Apple iPhone 16 FineWoven Case",
        "questions": [
            "1. Scratch, stain, and fray durability described?",
            "2. MagSafe strength and possible imprinting noted?",
            "3. Grip feel & added bulk assessed?",
            "4. Raised lip protection for screen and camera confirmed?",
            "5. Cleaning method and ease provided?",
            "6. Value versus leather or silicone cases discussed?"
        ],
    },
    {
        "url": "https://www.amazon.com/dp/B0BJ62BW91",
        "name": "Gravol Kids Liquid",
        "questions": [
            "1. Dimenhydrinate mg per dose & minimum age stated?",
            "2. Prevention window (30–60 min) & duration of effect explained?",
            "3. Drowsiness side-effect likelihood described?",
            "4. Kid-friendly taste feedback included?",
            "5. Dosing tool accuracy/ease mentioned?",
            "6. Storage requirements (room temp vs refrigeration) specified?"
        ],
    },
    {
        "url": "https://www.amazon.com/Orgain-Organic-Protein-Powder-Strawberries/dp/B09SJ4WJNV/",
        "name": "Orgain Organic Protein Powder – Strawberries & Cream",
        "questions": [
            "1. 21 g plant-protein blend (pea/rice/chia) listed?",
            "2. Taste, sweetness level, and mixability described?",
            "3. USDA Organic & Non-GMO certifications noted?",
            "4. Digestive comfort (gas/bloat) feedback covered?",
            "5. Cost per serving compared with other organic plant proteins?",
            "6. Total servings per container stated?"
        ],
    },
    {
        "url": "https://www.amazon.com/Quencher-Cupholder-Compatible-Insulated-Stainless/dp/B0DCDQ1RFV/",
        "name": "Stanley Quencher H2.0 FlowState (40 oz)",
        "questions": [
            "1. Cold/iced and hot retention times verified?",
            "2. Leak resistance in straw and fully-closed modes described?",
            "3. Cup-holder fit and handle comfort covered?",
            "4. Dishwasher safety and cleaning ease noted?",
            "5. Powder-coat scratch/dent resistance discussed?",
            "6. Filled weight and portability addressed?"
        ],
    },
    {
        "url": "https://www.amazon.com/SENSARTE-Nonstick-Frying-Pan-Skillet/dp/B086PHS2V8/",
        "name": "SENSARTE ILAG Granite Nonstick Frying Pan",
        "questions": [
            "1. Initial nonstick performance & PFOA-free safety covered?",
            "2. Expected nonstick lifespan and care-instruction tips given?",
            "3. Even heating and induction compatibility described?",
            "4. Cool-touch handle & oven-safe temperature limit noted?",
            "5. Scratch resistance with everyday utensils mentioned?",
            "6. Warranty length or overall value versus competing pans discussed?"
        ],
    },
]