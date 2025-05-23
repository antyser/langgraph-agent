"""Evaluation data for the product summary graph."""

from typing import Any, Dict, List

# General evaluation rubrics applied to all products
GENERAL_EVALUATION_RUBRICS = [
    "Every subsection title is formatted in bold text.",
    'All content is in bullet-point "keyword + description" style, and any unavoidable jargon is briefly defined.',
    'The insight includes category-specific sections that match the product type (e.g., "Care Tips" for skincare, "Installation" for appliances).',
    "Each subsection addresses one distinct topic only (no multi-topic sections).",
    "No fact, opinion, or phrase is repeated across different sections.",
    "Within each list or section, the highest-impact, most frequently mentioned point is listed first.",
    "Pros and Cons are presented in two clearly labeled, separate lists.",
    'Conflicting opinions are grouped under a labeled "Mixed Reviews" list (separate from Pros and Cons).',
    "Every Pro, Con, or Mixed item is materially meaningful to user decisions—not a trivial attribute such as color or size unless that trait is a known deal-breaker.",
    'The insight explicitly states "Who it\'s for" and "Who it\'s not for," tying each to use-case, age, lifestyle, or budget personas.',
    "The insight compares the product with at least one close alternative, highlighting differentiators.",
]

GENERAL_EVALUATION_RUBRICS_V2: List[str] = [
    "Top-level subsections (Pros & Cons, Who it's for / not for, Usage or care tips, Specific Use Case Considerations, Insights about comparing similar products etc) are all bold and on their own line. In-body labels inside bullets are ignored.",
    "Under each top-level subsection, every point must be written as a bullet point. Each bullet point must strictly follow a 'Keyword + Description' format. This means a concise keyword or short phrase, immediately followed by a colon (':'), and then a detailed description. The keyword is bold.",
    "Start the analysis with a one sentence intro, for example: \"Here's an analysis of [product title] based on the information available:",
    "For both top-level subsections and inline points within them, prioritize content that is high-impact for decision-making, is frequently highlighted in expert or user reviews, or serves as a key product differentiator or deal-breaker.",
    'Distinct Categorization: All positive points are listed exclusively under "Pros", all negative points exclusively under "Cons", and any points containing conflicting opinions or both positive and negative aspects are grouped solely under "Mixed Reviews" (if applicable).',
    "Clear Separation: Each of these categories (Pros, Cons, Mixed Reviews) is presented as a clearly labeled, independent list, ensuring no overlap or ambiguity in their presentation.",
    "For both top-level subsections and inline points within them, item is materially meaningful to user decisions—not a trivial attribute such as color or size unless that trait is a known deal-breaker.",
    "Include specifies user profiles (Who it's for / not for) based on use case, age, lifestyle, budget, etc",
    "Include comparing similar products: The content effectively highlights the product's key differentiators and unique selling propositions (its specialties) in direct comparison to similar competing products, explicitly detailing the specific products or product types being compared.",
]

COVERAGE_TO_EVALUATE: List[Dict[str, Any]] = [
    {
        "url": "https://www.amazon.com/dp/B08MLG2SG4",
        "name": "Amara Smoothie Melts - Mango Carrot",
        "questions": [
            # Ingredients & Allergens
            "1. Ingredients List: Does the summary list the main ingredients?",
            "2. Added Sugars: Does the summary state if there are added sugars?",
            "3. Artificial Additives: Does the summary state if there are artificial ingredients or preservatives?",
            "4. Allergens: Does the summary list common allergens (dairy, soy, nuts, gluten) present or state their absence?",
            # Texture & Safety
            "5. Dissolvability: Does the summary mention how quickly/easily the melts dissolve?",
            "6. Choking Risk Info: Does the summary address choking risk (e.g., via dissolvability or texture description)?",
            "7. Texture Description: Does the summary describe the texture?",
            "8. Age Appropriateness: Does the summary indicate the recommended age range?",
            # Usage
            "9. Serving Size: Does the summary state the recommended serving size?",
            "10. Serving Frequency: Does the summary suggest a recommended frequency of consumption?",
            # Nutrition & Taste
            "11. Key Nutrients: Does the summary mention key vitamins or nutrients provided?",
            "12. Taste Feedback: Does the summary reference user reviews regarding taste/palatability?",
            # Packaging & Storage
            "13. Packaging Features: Does the summary mention ease of opening or resealing the package?",
            "14. Quantity per Package: Does the summary state the number of melts per package?",
            "15. Shelf Life: Does the summary mention the product's shelf life?",
            "16. Storage Instructions: Does the summary provide storage instructions (especially after opening)?",
            # Comparison
            "17. Competitor Comparison: Does the summary compare this product to competitors (e.g., Gerber Melts) on aspects like ingredients, nutrition, or price?",
        ],
        "true_statements": [
            '**100% Organic, No Added Sugar:** Made with only four organic ingredients – mango, coconut milk, carrot, and lemon juice – and contains **no added sugars, preservatives, or fillers**. Certified USDA Organic and non-GMO, it\'s a **plant-based** "yogurt melt" snack that is dairy-free (uses coconut milk) and gluten-free.',
            "**Toddler-Friendly Melts:** These bite-sized pieces **melt in the mouth**, making them safe for little ones learning to self-feed. They're perfectly sized to help babies practice their pincer grip and hand-eye coordination while enjoying a fun, mess-free snack.",
            "**Convenient & Resealable:** Packaged in a set of **six 1-oz resealable pouches**, the lightweight bags don't require refrigeration – great for on-the-go, lunchboxes, or travel. The snacks are shelf-stable and the resealable design keeps leftovers fresh.",
            "**Nutrient-Rich and Clean Label:** Delivers real fruit and veggie nutrition from **mango and carrot** in each serving. Free of any artificial colors, flavors, or preservatives, and even the vibrant color comes naturally from the produce (no added dyes). The **Mango Carrot** flavor is also dairy-free, unlike some other flavors in the line.",
            '**Small Business Ethos:** **Amara** is a small business brand focused on wholesome baby foods. They emphasize that "from boob to spoon," parents shouldn\'t have to choose between nutrition and convenience. The Smoothie Melts are an innovative first-of-its-kind no-sugar-added melt snack to keep toddlers satisfied without a sugar crash.',
        ],
    },
    {
        "url": "https://www.amazon.com/Samsonite-Freeform-Hardside-Spinner-Black/dp/B01M0A3BKH/",
        "name": "Samsonite Freeform Hardside Carry-On",
        "questions": [
            # Durability & Material
            "1. Material Type: Does the summary identify the hardshell material (e.g., polypropylene)?",
            "2. Crack Resistance: Does the summary mention resistance to cracking?",
            "3. Scuff/Scratch Resistance: Does the summary mention resistance to scuffs or scratches?",
            # Wheels
            "4. Wheel Type: Does the summary specify the type of wheels (e.g., 360-degree spinner)?",
            "5. Wheel Performance: Does the summary describe the smoothness or quietness of the wheels on different surfaces?",
            "6. Wheel Durability: Does the summary comment on the durability of the wheels?",
            # Compliance & Dimensions
            "7. Carry-On Compliance: Does the summary state whether it meets major airline carry-on size restrictions?",
            "8. Exact Dimensions: Does the summary provide the exact dimensions (including wheels/handles)?",
            # Weight & Capacity
            "9. Weight Specification: Does the summary state the weight of the luggage?",
            "10. Lightweight Comparison: Does the summary compare its weight to similar carry-ons?",
            "11. Interior Organization: Does the summary describe interior features (dividers, straps, pockets)?",
            # Features
            "12. Handle Type: Does the summary describe the handle (e.g., telescoping)?",
            "13. Handle Quality: Does the summary comment on the sturdiness or comfort of the handle?",
            "14. TSA Lock: Does the summary state if it includes a built-in TSA-approved lock?",
            "15. Lock Reliability: Does the summary mention the reliability or ease of use of the lock?",
            # Aesthetics & Warranty
            "16. Finish Properties: Does the summary mention if the finish resists fingerprints or scratches easily?",
            "17. Warranty Information: Does the summary state the warranty period?",
            "18. Customer Service Reputation: Does the summary mention feedback on Samsonite's customer service for claims?",
        ],
        "true_statements": [
            "**Carry-On Dimensions & Light Weight:** Measures approximately **21.25″ x 15.25″ x 10″ including wheels**, fitting most airlines' cabin size restrictions. Despite its durable hardshell, it weighs only ~**6.5 lbs**, making it easy to lift into overhead bins.",
            "**Durable Polypropylene Shell:** Constructed from a **hard-sided polypropylene** shell that is impact-resistant and scratch-resistant. This lightweight yet sturdy material protects contents and is backed by Samsonite's **10-year limited warranty**, after rigorous quality testing.",
            "**Smooth Rolling & Maneuverable:** Equipped with four oversized **dual spinner wheels** that rotate 360°, allowing effortless gliding in any direction. The spinner wheels and telescopic handle make navigating busy airports and tight spaces easy, with great stability even on rough surfaces.",
            "**TSA-Approved Lock:** Features a built-in **TSA combination lock** integrated into the suitcase. Set your own 3-digit combo – it secures the zippers in place for peace of mind, yet allows TSA agents to open for inspection without damage. No keys needed, and your belongings stay safe throughout your journey.",
            "**Spacious & Organized Interior:** The 21″ Freeform maximizes packing space with a deep main compartment (~19.5″ x 14.5″ interior). Inside you'll find **elastic cross-straps** to hold clothes in place, a full-length zippered divider panel, and a zippered pouch – all helping to neatly separate and secure your items. The case is also **expandable**, giving you a little extra room when needed for souvenirs.",
        ],
    },
    {
        "url": "https://www.amazon.com/dp/B0CHN9X9S2",
        "name": "Sports Research Fish Oil Mini-Softgels",
        "questions": [
            # Benefits & Use
            "1. Marketed Benefits: Does the summary list the specific health benefits the product is marketed for (heart, brain, joint, etc.)?",
            # Ingredients & Form
            "2. EPA Amount: Does the summary state the exact amount of EPA per serving/softgel?",
            "3. DHA Amount: Does the summary state the exact amount of DHA per serving/softgel?",
            "4. Oil Form: Does the summary specify if the oil is in triglyceride form?",
            # Quality & Purity
            "5. Third-Party Testing: Does the summary state if it's third-party tested for purity and potency?",
            "6. Specific Purity Tests: Does the summary mention testing for heavy metals (mercury), PCBs, or dioxins?",
            "7. Test Result Accessibility: Does the summary indicate if test results (e.g., IFOS report) are accessible?",
            # Source & Sustainability
            "8. Fish Source: Does the summary identify the type of fish used (e.g., anchovy, sardine)?",
            "9. Catch Method: Does the summary state if the fish are wild-caught?",
            "10. Sustainability Certification: Does the summary mention any sustainability certifications (e.g., Friend of the Sea)?",
            # Side Effects & Usability
            "11. Fishy Burps/Aftertaste: Does the summary mention user feedback regarding fishy burps or aftertaste?",
            "12. Digestive Upset: Does the summary mention user feedback regarding digestive upset?",
            "13. Capsule Size Description: Does the summary describe the size of the 'mini-softgels'?",
            "14. Ease of Swallowing: Does the summary comment on how easy they are to swallow?",
            # Brand & Value
            "15. Oxidation Protection: Does the summary mention how the oil is protected from oxidation?",
            "16. Brand Reputation: Does the summary comment on the reputation of the Sports Research brand?",
            "17. Price Comparison: Does the summary compare its price/value to other fish oil brands based on EPA/DHA content?",
        ],
        "true_statements": [
            "**High-Potency Omega-3 (Burp-Free):** Delivers **520 mg of Omega-3 fatty acids** (EPA + DHA) per serving from wild-caught Alaska pollock, in easy-to-swallow mini softgels. Produced using a 10-step refinement (including molecular distillation and deodorization) to **eliminate fishy odor and aftertaste**, so you get the benefits of fish oil **without fish burps**.",
            "**Sustainably Sourced & Certified Pure:** Sourced from wild Alaskan pollock and certified sustainable by the **Marine Stewardship Council (MSC)**. It's also **IFOS 5-star rated**, confirming the oil's purity, potency, and freshness. Every batch is third-party tested to be free of heavy metals and contaminants.",
            "**Triglyceride Form Omega-3s:** Each new mini softgel (smaller size) contains **625 mg of fish oil concentrate**, providing 520 mg Omega-3s in the natural triglyceride form for optimal absorption. This includes the essential EPA and DHA fatty acids known to support heart, brain, and eye health.",
            '**Easy to Swallow & Digest:** The **mini softgel size** is roughly 1/2 the size of standard fish oil pills, making it much easier for kids or adults who struggle with large capsules. The formula is designed for digestion comfort – no reflux or "fishy burp" issues thanks to the advanced purification and enteric-friendly design.',
            "**Quality Ingredients – No Junk:** Manufactured in a cGMP facility in the USA and held to strict quality standards. It's **pescatarian-friendly** (gelatin from fish), and contains **no GMOs, no soy, no gluten**, and no hexane or harsh solvents used in extraction. The softgels are also free of artificial colors or flavors, with a natural lemon scent added to further prevent any fishy smell.",
        ],
    },
    {
        "url": "https://www.amazon.com/dp/B003BHZ71G",
        "name": "NOW Supplements, Sunflower Lecithin",
        "questions": [
            # Benefits & Use
            "1. Reported Uses: Does the summary list the main reasons people take sunflower lecithin (brain, liver, cholesterol, etc.)?",
            "2. Scientific Support: Does the summary mention scientific support for any claimed benefits?",
            # Source & Comparison
            "3. Advantage vs. Soy: Does the summary explain the advantages of sunflower lecithin compared to soy lecithin?",
            "4. GMO Status: Does the summary explicitly state if it's non-GMO?",
            # Dosage & Form
            "5. Product Form: Does the summary specify the form (softgel, powder, granule)?",
            "6. Lecithin per Serving: Does the summary state the amount of lecithin per serving?",
            "7. Typical Dosage: Does the summary suggest a typical daily dosage?",
            "8. Phosphatidylcholine Content: Does the summary specify the phosphatidylcholine content?",
            # Side Effects & Quality
            "9. Potential Side Effects: Does the summary mention potential side effects (e.g., digestive issues)?",
            "10. Brand Reputation: Does the summary comment on NOW Supplements' reputation for quality?",
            "11. Quality Testing/GMP: Does the summary mention purity testing or GMP certification?",
            # Usability & Certifications
            "12. Taste/Mixability (if powder/granule): If applicable, does the summary describe the taste or mixability?",
            "13. Organic Certification: Does the summary state if it's certified organic?",
        ],
        "true_statements": [
            "**Nervous System Support:** Each softgel provides **1,200 mg of sunflower lecithin**, which naturally abounds in phospholipids crucial for brain and nerve health. It's rich in **phosphatidyl inositol and phosphatidyl ethanolamine**, as well as essential fatty acids that help support healthy cell membranes and neurotransmitter function.",
            "**Soy-Free Source of Choline:** Derived from non-GMO sunflower seeds (not soy), it supplies **phosphatidyl choline**, the most abundant phospholipid in cell membranes that plays a key role in cellular signaling and cognitive function. This makes it an excellent choline source for those avoiding soy-based lecithin.",
            "**Quality Assured & Pure:** **Soy-free, Non-GMO, and allergen-friendly** – made without gluten, corn, dairy, eggs, or peanuts. It's also **certified Kosher**. NOW's manufacturing is **GMP Certified (NPA A-rated)**, meaning every aspect from sourcing to testing has been rigorously reviewed for quality and potency.",
            "**Healthy Fat Emulsifier:** Lecithin is an emulsifying lipid – it helps disperse fats and cholesterol in water. This makes it supportive of **liver health and fat metabolism**, and it's commonly taken to promote normal cholesterol levels and healthy bile flow (as part of a balanced diet).",
            "**Family Owned Since 1968:** Packaged in the USA by NOW Foods, a family-owned company known for quality supplements for decades. The formula is free of unnecessary additives; just pure sunflower lecithin in a convenient softgel form that can be taken 1–3 times daily with meals as needed.",
        ],
    },
    {
        "url": "https://www.amazon.com/Aquasana-3-Stage-Filter-System-Chrome/dp/B06XGY3G28/",
        "name": "Aquasana 3-Stage Water Filter",
        "questions": [
            # Contaminant Removal
            "1. Reduced Contaminants: Does the summary list specific contaminants reduced (chlorine, lead, PFOA/PFOS, etc.)?",
            "2. NSF/ANSI Certification: Does the summary state which NSF/ANSI standards (42, 53, 401) it is certified for?",
            "3. Mineral Retention: Does the summary mention if beneficial minerals are retained?",
            # Water Quality & Filters
            "4. Taste/Odor Improvement: Does the summary report user feedback on improved water taste or odor?",
            "5. Filter Lifespan (Gallons/Months): Does the summary specify the typical lifespan of the filters?",
            "6. Replacement Filter Cost: Does the summary indicate the ongoing cost of replacement filters?",
            # Installation & Maintenance
            "7. Installation Ease: Does the summary comment on the ease of under-sink installation for DIYers?",
            "8. Filter Replacement Ease: Does the summary describe the ease of replacing filters?",
            "9. Tools Required for Replacement: Does the summary mention if tools are needed for filter changes?",
            # Performance & Build
            "10. Flow Rate Impact: Does the summary mention if the filter affects the water flow rate?",
            "11. Faucet Quality: Does the summary comment on the quality of the included faucet?",
            "12. Leak Reports: Does the summary mention user reports regarding leaks?",
            "13. System Dimensions: Does the summary provide the dimensions of the filter unit?",
            "14. Required Under-Sink Space: Does the summary indicate the amount of under-sink space needed?",
            # Support
            "15. Warranty Details: Does the summary state the warranty offered by Aquasana?",
            "16. Customer Support Feedback: Does the summary mention user feedback on customer support?",
        ],
        "true_statements": [
            "**Removes 99% of 78 Contaminants:** This under-sink system uses **Claryum® 3-Stage Max Flow filtration** to target a broad array of contaminants. It's **NSF/ANSI certified (42, 53 including P473, 401)** to reduce up to **99% of lead, PFAS (PFOA/PFOS), chlorine, chloramines, pesticides, microplastics, pharmaceuticals, mercury, asbestos, cysts**, and more. In total it removes **15× more contaminants** than a standard water pitcher filter, while **retaining healthy minerals** like calcium, potassium, and magnesium in your water.",
            "**Three-Stage Filtration + Pre-Filter:** Combines a sediment **pre-filter (20 micron)** to catch rust, sediment, and silt, followed by activated carbon and catalytic carbon filters, and an ion-exchange filter media. This multi-stage system tackles different contaminant types (particulates, chemical contaminants, heavy metals) ensuring comprehensive filtration and extending the life of the main filters.",
            "**Fast Flow Rate, High Capacity:** The **\"Max Flow\" design delivers up to 0.72 gallons per minute** flow rate – that's about 44% faster than Aquasana's standard 3-stage system. Each set of filters treats **800 gallons** (approx. 6 months for an average family) before needing replacement. An integrated **filter change indicator** on the unit will alert you when it's time to swap filters, taking the guesswork out of maintenance.",
            "**Easy Install & Use:** Attaches to your cold water line and comes with a dedicated **metal faucet** (available in nickel, chrome, or bronze finishes) for dispensing the filtered water. DIY installation is straightforward with push-to-connect fittings and twist-off filter replacements – **no special tools or plumber needed**. The system fits under most sinks (compact dimensions ~12″ Wx 12.8″ H x 4.25″ D).",
            "**Trusted Quality & Warranty:** Aquasana's filtration technology is **independently tested** and the unit is backed by a **1-year warranty**. All plastic components are BPA-free. Using this system provides clean, great-tasting water at only **~10¢ per gallon**, reducing reliance on bottled water and supporting environmental sustainability.",
        ],
    },
    {
        "url": "https://www.amazon.com/CRZ-YOGA-Butterluxe-Racerback-Longline/dp/B0BKQ6HRLQ",
        "name": "CRZ YOGA Butterluxe Racerback",
        "questions": [
            # Support & Fabric
            "1. Recommended Impact Level: Does the summary specify the suitable activity impact level (low, medium, high)?",
            "2. Built-in Bra: Does the summary state if it has a built-in bra?",
            "3. Fabric Softness: Does the summary describe the softness of the 'Butterluxe' fabric?",
            "4. Fabric Stretch/Comfort: Does the summary comment on the stretch and comfort of the fabric?",
            "5. Fabric Comparison (Lululemon): Does the summary compare the fabric to Lululemon Align fabric?",
            "6. Breathability: Does the summary mention the fabric's breathability?",
            "7. Moisture-Wicking: Does the summary state if the fabric is moisture-wicking?",
            # Fit & Durability
            "8. Sizing Accuracy: Does the summary provide guidance on whether it runs true to size?",
            "9. Fit Description: Does the summary describe the fit (compressive, relaxed)?",
            "10. Length Description: Does the summary confirm if it's 'longline' and comment on coverage?",
            "11. Durability After Washing: Does the summary mention how the fabric holds up after washing?",
            "12. Pilling Issues: Does the summary mention user feedback regarding pilling?",
            # Features & Value
            "13. Removable Pads: If there's a built-in bra, does the summary state if the pads are removable?",
            "14. Pad Quality/Shape: Does the summary comment on the quality or shape of the pads?",
            "15. Color Accuracy: Does the summary mention if the colors match the product images?",
            "16. Value Comparison: Does the summary compare its price/value to similar tops from other brands?",
        ],
        "true_statements": [
            '**"Butterluxe" Ultra-Soft Fabric:** Made from CRZ Yoga\'s signature Butterluxe fabric, a **luxuriously soft and ultra-stretchy** material engineered for comfort. It has a **brushed, buttery feel** against the skin and high Lycra® content ("Lycra Black" fibers) that give it excellent shape retention and a gentle, lightweight compression fit. The moisture-wicking, quick-dry properties keep you cool and dry during workouts.',
            "**Built-in Bra Support:** This racerback workout tank features an integrated **built-in shelf bra** with removable pads, providing light support and coverage for low-impact activities like yoga, Pilates, or weight training. An inner elastic band keeps the bra cups securely in place during movement. (Removable pads allow for easy washing and personal adjustment of coverage.)",
            "**Ergonomic Racerback Design:** Designed with a **crew neck and Y-back racerback** cut, allowing full range of motion in the shoulders and arms. The racerback style not only offers freedom of movement but also highlights your back. The straps and armholes are constructed to prevent chafing or digging in, even during stretches or floor exercises.",
            '**Slim, Waist-Length Fit:** The Butterluxe tank has a **slim fit and short length** – it sits around the waist (slightly crop-length) for a modern look. It pairs perfectly with high-waisted leggings. Despite the lighter weight fabric, it offers a gentle "held in" feel thanks to the fine gauge knitting and high spandex content.',
            "**Low-Impact, Everyday Versatility:** **Designed for yoga and low-impact workouts**, this tank's second-skin comfort also makes it ideal for everyday wear or athleisure layering. It is **tag-free** and has flatlock seams, preventing irritation. The Butterluxe collection is all about combining **luxurious comfort with performance**, and this racerback top exemplifies that balance – providing stretch, softness, and style in and out of the gym.",
        ],
    },
    {
        "url": "https://www.amazon.com/Nest-T3007ES-Thermostat-Temperature-Generation/dp/B0131RG6VK",
        "name": "Nest Learning Thermostat",
        "questions": [
            # Installation & Compatibility
            "1. Installation Difficulty: Does the summary comment on the ease/difficulty of installation for homeowners?",
            "2. C-Wire Requirement: Does the summary clarify if a C-wire is required or if alternatives exist?",
            "3. HVAC Compatibility Check: Does the summary explain how to check compatibility with HVAC systems?",
            "4. Compatible Systems: Does the summary list types of compatible systems (multi-stage, heat pump, etc.)?",
            # Learning & Savings
            "5. Learning Feature Effectiveness: Does the summary provide insight into how well the learning feature adapts?",
            "6. Energy/Cost Savings: Does the summary mention user feedback or claims about energy/cost savings?",
            "7. Initial User Input: Does the summary indicate how much initial 'teaching' is needed?",
            # App & Control
            "8. App Usability: Does the summary comment on the intuitiveness or reliability of the Nest/Google Home app?",
            "9. Remote Control Functionality: Does the summary confirm reliable remote control via the app?",
            "10. Energy Monitoring via App: Does the summary mention energy monitoring features in the app?",
            "11. Smart Home Integration: Does the summary list compatible smart home ecosystems (Alexa, Google Assistant)?",
            "12. Manual Interface Usability: Does the summary comment on the ease of using the thermostat's physical controls?",
            "13. Display Quality: Does the summary describe the clarity or responsiveness of the display?",
            # Reliability & Fees
            "14. Wi-Fi Connectivity Issues: Does the summary mention common issues with Wi-Fi connectivity?",
            "15. General Reliability Issues: Does the summary mention other common reliability problems?",
            "16. Subscription Fees: Does the summary explicitly state if core features require a subscription?",
        ],
        "true_statements": [
            "**Learns Your Schedule Automatically:** The Nest Learning Thermostat **programs itself** by observing your temperature adjustments and daily routine. After a few days of use, it creates an optimized heating/cooling schedule tailored to you – no complex programming required. It then continually adapts (e.g., turning itself down at night or when you're away) to save energy while keeping you comfortable.",
            "**Auto-Away & Smart Sensing:** Built-in motion and ambient light sensors plus phone location integration enable **Auto-Away mode**, which **turns the temperature down when no one's home** to avoid heating or cooling an empty house. When you return, Nest kicks back in to re-comfort your home. Many users see significant energy savings – Nest is the first thermostat to earn ENERGY STAR® certification, saving up to ~12% on heating and 15% on cooling bills on average.",
            "**Remote Control via App:** Connects to Wi‑Fi, allowing full control from the **Nest smartphone app** or web. You can check or change the temperature, set schedules, or override away mode **from anywhere**. It also provides detailed **Energy History** and monthly reports, so you can see how much energy you use and why. (Works with Google Assistant, Alexa, etc., for voice control as well.)",
            "**Elegant Design with Farsight:** The thermostat's iconic circular design features a sharp, large display that **lights up when it senses you across the room** (Farsight) to show you the set temp or time. The display is a high-res color LCD and the outer ring rotates for intuitive manual control. Available in multiple finishes (stainless steel, black, copper, etc.) to complement your home.",
            "**HVAC Compatibility & Safety:** The 3rd Gen Nest works with **95% of low-voltage HVAC systems**, supporting up to 3 heating and 2 cooling stages, plus forced-air, radiant, heat pump, and boiler systems. It also has furnace monitoring and will alert you if it detects unusual patterns (which could indicate an HVAC issue). Additionally, it can integrate with Nest Protect – if high CO levels are detected, Nest can shut off the furnace as a precaution. Installation is DIY-friendly (usually ~30 min) with labeled wiring, and *C*-wire is not required for most systems due to Nest's built-in battery.",
        ],
    },
    {
        "url": "https://www.amazon.com/Company-Conscious-Plant-Based-Hypoallergenic-Dermatologist/dp/B07SH6HN2X/",
        "name": "Honest Baby Wipes",
        "questions": [
            # Ingredients & Sensitivity
            "1. Irritant Checklist: Does the summary confirm the absence of alcohol, parabens, phthalates, or fragrances?",
            "2. Plant-Based Claim: Does the summary state they are plant-based?",
            "3. Suitability for Sensitive Skin: Does the summary mention user feedback on suitability for sensitive skin/eczema?",
            # Physical Properties
            "4. Softness: Does the summary describe the softness of the wipes?",
            "5. Durability/Strength: Does the summary comment on the durability or resistance to tearing?",
            "6. Thickness: Does the summary provide information on the thickness of the wipes?",
            "7. Wetness Level: Does the summary describe the moisture level (not too dry/wet)?",
            "8. Drying Out Issue: Does the summary mention if they tend to dry out quickly after opening?",
            # Usability & Eco Claims
            "9. Dispensing Performance: Does the summary comment on whether they dispense one at a time easily?",
            "10. Scent Description: Does the summary confirm they are unscented or describe any smell?",
            "11. Biodegradability Claim: Does the summary mention any claims about biodegradability?",
            "12. Substantiation of Eco Claims: Does the summary indicate if eco claims are substantiated (e.g., certifications)?",
            # Value
            "13. Cost Per Wipe Comparison: Does the summary compare the cost per wipe to other brands?",
            "14. Available Package Sizes: Does the summary mention the different package sizes available?",
        ],
        "true_statements": [
            "**99%+ Water & Gentle Ingredients:** Honest Clean Conscious Wipes are made with **over 99% water** and just a few carefully selected ingredients (only 7 total). They contain **no alcohol, parabens, chlorine, fragrances, or dyes** – nothing to irritate sensitive skin. The formula is as simple and mild as possible, making these wipes safe for newborns and those with eczema-prone or sensitive skin.",
            "**Plant-Based & Compostable:** The wipes material is a **plant-based viscose** derived from sustainably managed forests, and they are **completely compostable**, breaking down in about 8 weeks. They provide a durable, cloth-like feel but without plastic fibers. By using these, you're reducing the environmental impact compared to conventional plastic wipes.",
            "**Dermatologist-Tested & EWG Verified:** Honest wipes are **dermatologist tested** and have received the **National Eczema Association's Seal of Acceptance** for use on sensitive, eczema-prone skin. They are also **EWG Verified**, meaning the Environmental Working Group has confirmed they meet strict criteria for health and transparency. Parents can trust that these wipes are extremely gentle and non-toxic.",
            "**Thick, Durable & Multi-Purpose:** These wipes are **extra thick and strong** – they hold up to big messes. The texture and moisture level make them effective not just for diaper changes, but also for sticky hands and faces, cleaning surfaces or toys on-the-go, and even wiping pet paws. Yet they're soft and absorbent, leaving no residue. The convenient **flip-top pack** keeps wipes moist and allows easy one-handed dispensing.",
            "**Hypoallergenic & Cruelty-Free:** Honest Co.'s formulation is hypoallergenic and pH-balanced for baby's skin. It's made without common allergens and irritants. The wipes are **not tested on animals** and contain no animal by-products (they are vegan-friendly). Each wipe is infused with a touch of aloe and cucumber extract to soothe and hydrate the skin during cleanups.",
        ],
    },
    {
        "url": "https://www.amazon.com/Millie-Moon-Diapers-COUCHES-22lbs-33lbs/dp/B0CHV6QYRV/",
        "name": "Millie Moon Diapers",
        "questions": [
            # Sensitivity & Materials
            "1. Suitability for Sensitive Skin: Does the summary mention user feedback on tolerance by babies with sensitive skin?",
            "2. Absence of Irritants: Does the summary confirm the absence of fragrance, latex, or chlorine bleaching?",
            # Performance
            "3. Leak Protection Effectiveness: Does the summary comment on effectiveness against leaks (daytime/overnight)?",
            "4. Leg Cuff/Waistband Fit: Does the summary describe the fit and effectiveness of leg cuffs/waistband?",
            "5. Softness (Inside/Outside): Does the summary describe the softness of the diaper's materials?",
            "6. Flexibility/Comfort: Does the summary comment on the flexibility and comfort of the fit?",
            "7. Absorption Speed/Capacity: Does the summary describe how well they absorb moisture?",
            "8. Skin Dryness: Does the summary mention if they keep the baby's skin feeling dry?",
            "9. Odor Control: Does the summary comment on how well odors are contained?",
            # Features & Fit
            "10. Wetness Indicator: Does the summary state if there is a wetness indicator?",
            "11. Wetness Indicator Reliability: Does the summary comment on the reliability of the wetness indicator?",
            "12. Sizing Accuracy: Does the summary provide guidance on whether the sizing is accurate based on weight?",
            # Value
            "13. Price Comparison: Does the summary compare the price to premium brands (Pampers/Huggies)?",
            "14. Availability: Does the summary mention where they are typically sold or if availability is limited?",
        ],
        "true_statements": [
            '**Ultra-Soft "CloudTouch" Comfort:** Millie Moon diapers are known for their **plush, silk-soft inner layer (CloudTouch)** that is gentle on delicate skin. The diaper\'s quilted liner provides a cushiony feel and wicks moisture away quickly, helping to prevent irritation and diaper rash. Parents often compare the softness to high-end cloth or premium brand diapers.',
            "**12-Hour Leak Protection:** These diapers feature an **ultra-absorbent core** that can hold a large volume, plus **double leak-guard barriers** along the leg cuffs, providing up to **12 hours of leak protection**. They're great for overnight use or long stretches, keeping babies dry through the night. Wetness indicators on the outside turn color to let you know when it's time for a change.",
            "**Gentle for Sensitive Skin:** **Dermatologically tested** and designed to be hypoallergenic for babies. Millie Moon diapers are **free from lotions, fragrances, latex, and elemental chlorine** (no chlorine bleaching) that can irritate skin. They are also **pH balanced** and use chlorine-free wood pulp, making them safe for babies with eczema or easily irritated skin.",
            "**High GSM Topsheet for Quick Absorption:** The top layer of the diaper is a **high GSM (grams per square meter) non-woven** fabric which means it's thicker and more absorbent than standard topsheets. This allows it to **instantly absorb moisture**, keeping liquid away from the skin to reduce the likelihood of diaper rash or chafing.",
            "**Thoughtful Design & Fit:** Millie Moon diapers have strong yet refastenable **secure tabs** that stay put even on active babies, and a **snug, high-rise waistband** at the back to help prevent blowouts up the back. The fit is generous and comfy, with stretchy side panels that move with your child. They come in stylish, gender-neutral prints – and despite the luxe features, they're often more affordable than other premium diaper brands.",
        ],
    },
    {
        "url": "https://www.amazon.com/Keurig-K-Elite-Temperature-Capability-Programmable/dp/B078NN17K3",
        "name": "Keurig K-Elite Coffee Maker",
        "questions": [
            # Cleaning & Maintenance
            "1. Ease of Regular Cleaning: Does the summary describe the ease of cleaning the needle and K-Cup holder?",
            "2. Descaling Frequency: Does the summary mention how often descaling is typically required?",
            "3. Descaling Process Ease: Does the summary comment on the simplicity of the descaling process?",
            # Reliability & Lifespan
            "4. General Reliability Feedback: Does the summary mention user feedback on overall reliability?",
            "5. Expected Lifespan: Does the summary provide insights into the expected lifespan based on reviews?",
            "6. Common Failure Points: Does the summary mention any common points of failure?",
            # Coffee Quality & Performance
            "7. Taste Consistency: Does the summary comment on the consistency of the brewed coffee taste?",
            "8. Water Temperature: Does the summary mention if the water gets hot enough for a good brew?",
            "9. 'Strong Brew' Effectiveness: Does the summary describe how well the 'Strong Brew' function works?",
            "10. Brew Speed: Does the summary state how quickly it brews a cup?",
            "11. Noise Level: Does the summary describe the noise level during heating or brewing?",
            # Features & Usability
            "12. Water Reservoir Capacity: Does the summary state the reservoir capacity?",
            "13. Water Reservoir Ease of Use: Does the summary comment on filling/cleaning the reservoir?",
            "14. Control Intuitiveness: Does the summary describe the ease of using the controls?",
            "15. Feature Performance: Does the summary comment on features like temperature control or iced coffee setting?",
            "16. K-Cup Compatibility (All types): Does the summary confirm compatibility with non-Keurig K-Cups and reusable pods?",
            "17. Physical Dimensions: Does the summary provide the machine's dimensions or footprint?",
        ],
        "true_statements": [
            '**Versatile Brewing Options:** The K-Elite can brew **5 different cup sizes** (4, 6, 8, 10, or 12 oz) at the touch of a button. It also has a **Strong Brew** feature for a bolder cup – simply press the "Strong" button to increase coffee strength and intensity. Additionally, the dedicated **"Iced" setting** brews hot coffee over ice at a lower temperature, yielding full-flavored iced coffee that isn\'t watered down.',
            "**Large 75 oz Reservoir:** The removable water reservoir holds **75 ounces** (around 9 cups) of water. This means you can brew cup after cup without frequent refills – great for offices or busy mornings. The reservoir is easy to detach and has a broad opening, making refills and cleaning straightforward.",
            "**Fast, Hot Brewing:** Thanks to Keurig's upgraded heating system, the K-Elite **brews a fresh cup in under a minute**. You can also program the **Brew Temperature** (187–192°F range) to customize how hot you like your coffee. Coffee comes out piping hot but the machine's **Quiet Brew Technology** minimizes noise during operation.",
            "**Convenient Programmable Features:** The K-Elite offers an **Auto-On** scheduler – you can set it to turn on and preheat at a specific time each morning, so it's ready to brew when you wake up. It also has an adjustable **auto-off** timer to conserve energy (e.g., turn off 2 hours after last brew). A digital display and simple button controls make it easy to navigate settings.",
            "**Modern Design & Easy Maintenance:** The sleek brewer features a premium finish and a **high-altitude mode** for optimal brewing above 5,000 ft elevation. It accommodates travel mugs up to 7.2″ tall by removing the drip tray. The drip tray can hold a full cup's worth of overflow for easy cleanup. It includes a **maintenance reminder** that alerts when it's time to descale the machine, helping keep your coffee tasting its best. All removable parts (reservoir, drip tray) are top-rack dishwasher safe, and the unit is compatible with the My K-Cup reusable filter for ground coffee.",
        ],
    },
    {
        "url": "https://www.amazon.com/Insta360-Standard-Bundle-Waterproof-Stabilization/dp/B0DBQBMQH2/",
        "name": "Insta360 Ace Pro",
        "questions": [
            # Video & Image Quality
            "1. Video Quality (Daylight): Does the summary describe video quality in good lighting?",
            "2. Video Quality (Low Light): Does the summary describe video quality in low light?",
            "3. Stabilization Effectiveness: Does the summary comment on the effectiveness of FlowState stabilization?",
            "4. Photo Quality: Does the summary describe the quality of still photos?",
            # Battery & Charging
            "5. Battery Duration: Does the summary state typical battery life during recording (and at what settings)?",
            "6. Charging Time: Does the summary state how long it takes to fully charge the battery?",
            # Workflow & App
            "7. Footage Transfer Speed/Ease: Does the summary comment on transferring footage to phone/computer?",
            "8. App Intuitiveness: Does the summary describe the Insta360 app as intuitive?",
            "9. App Editing Features: Does the summary mention the richness of editing features in the app?",
            "10. App Stability: Does the summary comment on the stability of the companion app?",
            # Durability & Hardware
            "11. Ruggedness: Does the summary comment on its suitability for action sports/ruggedness?",
            "12. Waterproofing Reliability: Does the summary mention the reliability of waterproofing without a case?",
            "13. Lens Scratch Resistance: Does the summary mention if the lens is prone to scratching?",
            "14. Built-in Audio Quality: Does the summary describe the quality of the internal microphones?",
            "15. Wind Noise Handling: Does the summary comment on how well it handles wind noise?",
            "16. Overheating Issues: Does the summary mention if the camera tends to overheat during long recordings?",
            "17. Flip Screen Quality/Usability: Does the summary comment on the flip screen's quality and usability?",
            "18. Menu Navigation Ease: Does the summary mention the ease of navigating the camera menus?",
            # Comparison & Value
            "19. Comparison vs. GoPro/DJI: Does the summary compare it to GoPro HERO or DJI Osmo Action cameras?",
            "20. Value for Money: Does the summary provide an assessment of its value proposition compared to competitors?",
        ],
        "true_statements": [
            '**Leica-Co Engineered Optics & 1/1.3" Sensor:** The Ace Pro is a flagship action cam developed with **Leica**, featuring a large **1/1.3-inch CMOS sensor** (48 MP) paired with a Leica Summarit lens. This big sensor + premium glass combo captures stunning detail, wide dynamic range (~13.5 stops), and excellent low-light performance with an effective 2.4 μm pixel size after pixel-binning. Expect sharper, more vibrant footage, especially in challenging lighting, compared to typical action cams.',
            '**4K120 Video & FlowState Stabilization:** Shoots up to **4K at 120 fps** for super slow motion, and 8K timelapses. The camera uses Insta360\'s renowned **FlowState stabilization** and horizon leveling algorithms to keep video **butter-smooth and horizon-stable**, even during intense motion. Active HDR mode is also available (called "Active HDR"), which stabilizes while preserving highlights and shadows for more color-rich footage without ghosting.',
            "**Dual Screens & Easy Controls:** Designed for vloggers, it has a flip-up **2.4″ color touchscreen** on the back that can articulate for front-facing framing, plus a small 0.7″ front status screen for recording info – perfect for selfies or blogging. The interface offers **gesture control** (start/stop with a hand motion) and improved **voice control** so you can command the camera hands-free, even in noisy environments or with the camera mounted out of reach.",
            "**Rugged & Waterproof:** The Ace Pro is built tough – its body is **waterproof down to 33 ft (10 m)** out of the box (IPX8 rated). The lens has a protective glass cover and the camera includes a high-density wind noise reduction mic cover for clear audio. The device is rated for a wide temperature range and high shock resistance, ready for surfing, mountain biking, skiing, and more. (For deeper dives beyond 10 m, an optional dive housing is available.)",
            '**Advanced Features & Expandability:** Packed with pro-grade capabilities like **Clarity Zoom** (lossless 2× digital zoom via sensor crop), **Loop Recording** (dash-cam mode), **Pre-Recording** (captures 15–30 s before hitting record so you never miss a moment), and **Timed Capture** (schedule recordings in advance). It captures **48 MP still photos** and even new **"spatial audio" 360° audio** for immersive clips. The Ace Pro has a standard 1/4"-"20 mount for accessories and is USB-C equipped for fast file transfers. It comes with a removable 1650 mAh battery, adhesive mounting buckle, and is compatible with Insta360\'s mobile app for **AI editing, auto horizon leveling, and the "Invisible Selfie Stick" effect**.',
        ],
    },
    {
        "url": "https://www.amazon.com/Murad-Retinol-Youth-Renewal-Serum/dp/B01K629LDI/",
        "name": "Murad Retinol Youth Renewal Serum",
        "questions": [
            # Target Concerns & Skin Types
            "1. Targeted Aging Signs: Does the summary list the specific signs of aging targeted (lines, wrinkles, texture, firmness, dark spots)?",
            "2. Suitability for Sensitive Skin: Does the summary indicate if it's suitable for sensitive skin based on reviews or claims?",
            # Results & Effects
            "3. Time to See Results: Does the summary provide an expected timeframe for seeing noticeable results?",
            "4. Reported Positive Effects: Does the summary list commonly reported benefits (smoother skin, reduced lines, etc.)?",
            # Formula & Irritation
            "5. Retinol Type/Technology: Does the summary specify the type of retinol used (e.g., Retinol Tri-Active Technology)?",
            "6. Likelihood of Irritation: Does the summary mention the potential for initial irritation (redness, peeling)?",
            "7. Irritation Mitigation: Does the summary suggest the formula helps mitigate irritation?",
            # Texture, Absorption & Scent
            "8. Serum Texture: Does the summary describe the texture (light, creamy, etc.)?",
            "9. Absorption Feel: Does the summary comment on how well it absorbs (non-greasy, non-sticky)?",
            "10. Scent: Does the summary mention if the product has a noticeable scent?",
            # Packaging & Usage
            "11. Packaging Effectiveness: Does the summary comment on the effectiveness of the pump bottle (dispensing, protection)?",
            "12. Recommended Frequency: Does the summary suggest how often to use the serum?",
            "13. Layering Information: Does the summary indicate if it layers well with other skincare products?",
            # Value
            "14. Value for Money Assessment: Does the summary provide an assessment of its value considering the price and results?",
        ],
        "true_statements": [
            "**Tri-Active Retinol Technology:** This fast-acting serum combines **3 forms of retinol** in one: a fast-release retinoid, a time-released encapsulated retinol, and a retinol booster ingredient. Murad's patented **Retinol Tri-Active Technology** delivers rapid wrinkle-smoothing results equivalent to high-strength retinol while being **gentle enough for nightly use**. It visibly minimizes fine lines and **deep wrinkles**, improves skin texture, and boosts radiance – in Murad's clinical studies, **92% saw smoother skin** and almost all users found it gentle on skin after 8 weeks.",
            '**Diminishes Signs of Aging:** In just 2 weeks, users reported seeing a noticeable reduction in key signs of aging – fewer wrinkles, firmer-looking skin, improved elasticity, and more even tone. By 4 weeks, it\'s **clinically proven** to visibly improve the **5 key signs of aging** (lines, wrinkles, firmness, texture, tone, glow). Many testers also saw a "boosted glow," as the formula encourages cell turnover for brighter, renewed skin.',
            "**Hydrating & Gentle Formula:** Unlike many retinol products, this serum is formulated to minimize irritation. It's infused with **hyaluronic acid** and swertia flower extract to attract moisture and plump skin, helping to **prevent dryness** and flaking often associated with retinol use. The result is potent youth-renewing benefits *without* the redness or peeling – **99% of users said it was gentle enough for nightly use** in trials.",
            "**Clean, Skin-Friendly Ingredients:** Murad's serum is free of parabens, sulfates, phthalates, gluten, and mineral oil. It's also **cruelty-free**. The formula includes antioxidants (like tocopheryl acetate) and amino acids to support skin's resilience. It's dermatologically tested and suited for all skin types – from oily to dry – that want an effective anti-aging regimen step.",
            "**Easy Integration & Usage:** The serum has a lightweight, silky texture that absorbs quickly without tackiness. It comes in an airless pump bottle to protect the retinol's potency. Use it at **night** after cleansing – just one or two pumps for full face and neck. (Murad advises reducing frequency if any sensitivity occurs, and using sunscreen during the day, as with any retinol.) Over time, skin looks more youthful, supple, and radiant thanks to this powerhouse treatment.",
        ],
    },
    {
        "url": "https://www.amazon.com/Ninja-Capacity-Dehydrate-Technology-AF141/dp/B0CSZ7WBYW/",
        "name": "Ninja Air Fryer",
        "questions": [
            # Capacity & Size
            "1. Practical Capacity: Does the summary give examples of how much food the 5.5 qt basket holds (e.g., lbs of wings)?",
            "2. Suitability for Household Size: Does the summary indicate if the size is practical for families/individuals?",
            "3. Counter Space/Dimensions: Does the summary provide the physical dimensions?",
            # Cooking Performance
            "4. Air Fry Performance: Does the summary comment on how well it air fries (crispiness, evenness)?",
            "5. Roast Performance: Does the summary comment on roasting performance?",
            "6. Bake Performance: Does the summary comment on baking performance?",
            "7. Reheat Performance: Does the summary comment on reheating performance?",
            "8. Dehydrate Performance: Does the summary comment on dehydrating performance?",
            "9. Cooking Evenness: Does the summary address whether it cooks food evenly?",
            # Ease of Use & Cleaning
            "10. Control Intuitiveness: Does the summary state if the controls are intuitive/easy?",
            "11. Preset Usefulness: Does the summary comment on the usefulness of presets?",
            "12. Cleaning Ease (Basket/Plate): Does the summary describe the ease of cleaning the basket and crisper plate?",
            "13. Dishwasher Safety: Does the summary confirm if the basket/plate are dishwasher safe?",
            "14. Dishwasher Durability: Does the summary mention how well parts hold up after dishwashing?",
            # Operation & Build
            "15. Noise Level: Does the summary describe the noise level during operation?",
            "16. Preheating Requirement/Time: Does the summary state if preheating is needed and how long it takes?",
            "17. Plastic Smell Reports: Does the summary mention user reports of plastic smell (especially initial uses)?",
            "18. Build Quality: Does the summary comment on the overall build quality and sturdiness?",
        ],
        "true_statements": [
            '**4 Cooking Functions in One:** The Ninja AF141 is a **4-in-1 appliance** – it can **Air Fry, Roast, Reheat, and Dehydrate** foods all in a single machine. Air frying lets you achieve crispy "fried" results with up to **75% less fat** than traditional deep frying (tested versus deep-fried French fries). Roast function works like a mini oven for meats or veggies, Reheat revives leftovers to crispy perfection, and Dehydrate slowly dries fruits, herbs, or jerky at low temps.',
            "**AirCrisp™ Technology:** Ninja's **Air Crisp Technology** rapidly circulates superheated air **up to 400°F** around your food for even browning and crunch with little to no added oil. Foods cook quickly and come out golden on the outside and tender inside. It's great for fries, wings, nuggets – delivering deep-fry taste and texture with a fraction of the calories.",
            "**Family-Sized 5 QT Capacity:** The nonstick basket holds **5 quarts** (4.7 L), which fits approximately **4 lbs of French fries or 5 lbs of chicken wings** in one batch. It's large enough for family meals but still compact on the counter. The basket and accompanying crisper plate are both **PTFE/PFOA-free nonstick** and **dishwasher-safe**, making cleanup a breeze.",
            "**Fast, Frozen-to-Crispy Cooking:** The Ninja can go from frozen chicken nuggets or fries to hot & crispy in minutes, **no thawing required**. Its powerful heating element and fan ensure quick preheat and even heat distribution. Users love that it significantly cuts down cook times – for example, frozen french fries can be done in about 8–10 minutes.",
            "**Modern Design & Easy Use:** Features a digital touchscreen control panel with intuitive time and temperature adjustment. The **FlowState™ spinning knob** (updated design) helps fine-tune settings precisely. It also has an **updated slim profile** – Ninja's latest H2.0 design – which **saves counter space** without compromising capacity. Cool-touch housing and an ergonomic handle ensure safe handling. (Included in the box: 5-qt fryer base, nonstick cook basket, crisper tray, and a 20-recipe inspiration guide.)",
        ],
    },
    {
        "url": "https://www.amazon.com/FIFINE-Microphone-Voice-Over-Windscreen-Amplitank-K688/dp/B0B8SNVK5K/",
        "name": "FIFINE USB/XLR Microphone K688",
        "questions": [
            # Sound Quality
            "1. USB Sound Quality for Voice: Does the summary describe the sound quality via USB for voice applications?",
            "2. XLR Sound Quality for Voice: Does the summary describe the sound quality via XLR for voice applications?",
            "3. Sound Quality Comparison: Does the summary compare its sound quality to other mics in its price range?",
            # Usability & Setup
            "4. USB Plug-and-Play Ease: Does the summary confirm easy plug-and-play setup via USB (Windows/Mac)?",
            "5. Driver Requirement: Does the summary state if special drivers are needed for USB connection?",
            # Performance
            "6. Background Noise Rejection: Does the summary comment on how well it rejects background noise/echo?",
            "7. XLR Gain Requirement: Does the summary indicate if significant gain is needed when using XLR?",
            "8. Sensitivity Level: Does the summary comment on the microphone's sensitivity for voice pickup?",
            # Build & Features
            "9. Build Material/Durability: Does the summary describe the build quality or materials used?",
            "10. Accessory Quality: Does the summary comment on the quality of included accessories (windscreen, mount)?",
            "11. Mute Button Functionality: Does the summary comment on the reliability/feel of the mute button?",
            "12. Gain Knob Functionality: Does the summary comment on the reliability/feel of the gain knob?",
            "13. Headphone Jack Monitoring: Does the summary confirm zero-latency monitoring via the headphone jack?",
            # Value
            "14. Value Proposition: Does the summary assess its value considering dual connectivity and sound quality for the price?",
        ],
        "true_statements": [
            '**Dual USB & XLR Connectivity:** The FIFINE K688 is a **hybrid dynamic microphone** that works as a plug-and-play USB mic or as a pro-grade XLR mic. Via USB, you can connect directly to a PC or Mac (great for beginners or remote work). The **XLR output** allows you to later plug into professional audio interfaces or mixers, giving you room to "level up" your setup without buying a new mic.',
            "**Dynamic Broadcast Sound:** As a **cardioid dynamic microphone**, the K688 focuses on your voice and rejects background noise, ideal for podcasting, streaming, or recording in untreated rooms. It has a **bright, clear tone** with full mids and an easy-to-drive output level – meaning you get that rich, broadcast-style sound without needing extreme gain. (It's often compared to far more expensive broadcast mics in terms of audio character.)",
            "**Built-In Controls & Monitoring (USB Mode):** The mic features convenient on-board controls: a **capacitive touch mute** button on top (for silent muting with a quick tap) and dedicated **knobs for mic gain and headphone volume** on the back. There's also a **3.5mm headphone jack** for zero-latency monitoring of your voice in real time. These make it very user-friendly during live sessions – you can quickly adjust levels or mute yourself without software.",
            '**Quality Build with Shock Mount & Pop Filter:** The K688 comes with a metal **shock mount** in the box, which isolates the mic from desk vibrations or stand movement – reducing thumps from bumps. It also includes a **high-density foam windscreen** (pop filter) that fits over the capsule to minimize plosives ("P" and "B" sounds) and wind noise. The mic\'s body is all-metal with a sleek matte finish, and the yoke mounting makes it easy to angle precisely on a boom arm or stand.',
            "**Plug & Play + Wide Compatibility:** The USB connection is driver-free and works instantly with Windows or Mac computers for Zoom calls, gaming, voice-overs, etc. (It's recognized as a standard USB audio device.) The XLR output can connect to any mixer or recorder that provides at least +48 V phantom power – although the K688 **does NOT require phantom power** to operate (it's dynamic). It's a versatile mic for anyone from beginners (using USB) to advanced creators integrating it into a professional audio chain.",
        ],
    },
    {
        "url": "https://www.amazon.com/Apple-iPhone-16-Version-128GB/dp/B0DHJH2GZL/",
        "name": "Apple iPhone 16",
        "questions": [
            # AI Features
            "1. AI Feature Usefulness: Does the summary provide insights into the practical usefulness of Apple Intelligence features?",
            "2. AI Enhancement to Experience: Does the summary suggest AI features significantly enhance the user experience?",
            # Upgrades vs. iPhone 15
            "3. Camera Improvements vs. 15: Does the summary detail noticeable camera performance improvements over the iPhone 15?",
            "4. Battery Life Improvements vs. 15: Does the summary quantify real-world battery life gains over the iPhone 15?",
            "5. Speed Improvements vs. 15: Does the summary highlight noticeable processing speed improvements over the iPhone 15?",
            "6. Display Improvements vs. 15: Does the summary describe tangible display quality improvements over the iPhone 15?",
            "7. New Button Utility: Does the summary comment on the practical utility of the new Action/Capture button?",
            # Comparison vs. iPhone 16 Pro
            "8. Key Functional Differences vs. Pro: Does the summary list the main functional differences compared to the 16 Pro?",
            "9. Missing Pro Features: Does the summary identify key Pro features absent in the standard 16 (camera, display, etc.)?",
            # Performance & Design
            "10. Low Light Camera Performance: Does the summary specifically comment on low-light photo/video quality?",
            "11. Design/Ergonomics Changes: Does the summary mention changes in physical design, weight, or feel compared to the 15?",
            "12. Thermal Performance: Does the summary indicate how well the phone manages heat during intensive tasks?",
        ],
        "true_statements": [
            '**A18 Chip & "Apple Intelligence":** The iPhone 16 is powered by Apple\'s new **A18 chip**, which features a 6‑core CPU (2 high-performance + 4 efficiency cores) and a 16‑core Neural Engine. It\'s built for next-level on-device AI – Apple\'s **personal "Apple Intelligence" system** – enabling advanced features like intelligent text completion, image recognition, and Siri improvements entirely on your device (with privacy protection). The A18 delivers a significant performance boost and improved power efficiency, translating to **smoother graphics (5‑core GPU) and longer battery life** even while handling demanding tasks or AAA mobile games.',
            '**Advanced Dual Camera with "Camera Control":** Equipped with a new **48 MP Main camera** (f/1.6 aperture) that uses Apple\'s "Fusion" technology to bin pixels for super-detailed **24 MP photos** by default, or full 48 MP ProRAW shots. It offers a **2× Telephoto option** using the center 12 MP of the sensor (essentially giving two optical-equivalent focal lengths in one lens). There\'s also a **12 MP Ultra Wide** (f/2.2) that enables **macro photography** for close-ups. A new **Camera Control** interface lets you quickly adjust depth, focus, or switch lenses with a tap – making capturing the perfect shot more intuitive. The camera system offers improved Night mode, Smart HDR 5, Photographic Styles, and can even capture **spatial photos/videos** for immersive viewing on Vision Pro.',
            "**Action Button & Dynamic Island:** Inherited from the 15 Pro, iPhone 16 features the **Action Button** on the side in place of the mute switch. This customizable button can still toggle silent mode by default, but can also be assigned to launch the camera, turn on the flashlight, start a voice memo, run shortcuts, and more – providing quick hardware access to your favorite feature. The front display incorporates the **Dynamic Island** (no more notch), which fluidly expands for alerts, background activities, and Live Activities (music, timers, calls, etc.). It's the same delightful interactive notification area introduced in the 14 Pro, now standard on the 16 family.",
            '**6.1" or 6.7" Super Retina XDR Display:** Available in two sizes – the iPhone 16 (6.1‑inch) and iPhone 16 Plus (6.7‑inch) – both with a brilliant **OLED Super Retina XDR** display. They support **HDR10 and Dolby Vision**, with up to **1600 nits HDR brightness** and **2000 nits peak outdoor brightness** for easy viewing even in sunlight. The displays are protected by Ceramic Shield glass, have up to 120 Hz adaptive refresh (ProMotion on Pro models; base 16 has standard 60 Hz), **True Tone** color adjustment, and an always-on option (on Pro). The design retains flat edges and an aerospace-grade aluminum (or surgical steel on Pro) frame, and is **IP68 water-resistant** (tested to 6 m for 30 min) for durability.',
            "**Bigger Battery & Bold Colors:** Thanks to efficiency gains and a slightly larger battery, iPhone 16 provides a notable **boost in battery life** – up to 22 hours video playback on the standard model (roughly 2 hours more than iPhone 15) and 28+ hours on the Plus. It supports 5G, MagSafe wireless charging and accessories, and all the latest iOS features like StandBy and NameDrop. The iPhone 16 comes in **five new colors**: midnight black, starlight white, a fresh light pink, a cool teal-green, and a vibrant ultramarine blue. Base storage starts at 128 GB. Apple continues its environmental strides – the 16 lineup uses more recycled materials (like 100% recycled aluminum in the chassis) and includes Apple's first **carbon-neutral** models (certain configurations paired with renewable energy and new packaging).",
        ],
    },
    {
        "url": "https://www.amazon.com/Apple-iPhone-MagSafe-Camera-Control/dp/B0DGHH9WMX/",
        "name": "Apple iPhone 16 FineWoven Case",
        "questions": [
            # Durability & Wear
            "1. Scratch/Scuff Resistance: Does the summary comment on the FineWoven material's resistance to scratches or scuffs?",
            "2. Staining Resistance: Does the summary mention if the material stains easily?",
            "3. Fraying Issues: Does the summary mention user reports of the material fraying?",
            "4. Patina Development: Does the summary comment on how the material wears or develops a patina over time?",
            # Feel & Grip
            "5. Texture Description: Does the summary describe the feel of the material (soft, textured)?",
            "6. Grip Level: Does the summary comment on whether the case provides good grip or is slippery?",
            # Protection & Fit
            "7. Drop Protection Level: Does the summary provide an assessment of the drop protection offered?",
            "8. Screen Lip Protection: Does the summary confirm a raised lip for screen protection?",
            "9. Camera Lip Protection: Does the summary confirm a raised lip for camera protection?",
            "10. Bulkiness: Does the summary comment on how much bulk the case adds?",
            # Cleanliness & MagSafe
            "11. Dust/Lint Attraction: Does the summary mention if the material attracts dust or lint?",
            "12. Ease of Cleaning: Does the summary describe how easy the case is to clean?",
            "13. MagSafe Connection Strength: Does the summary comment on the strength of the MagSafe connection?",
            "14. MagSafe Charging Interference: Does the summary mention any interference with MagSafe charging?",
            # Buttons & Aesthetics
            "15. Button Tactility: Does the summary describe the feel and responsiveness of the button covers?",
            "16. Cutout Precision: Does the summary comment on the precision of the cutouts?",
            "17. Color Accuracy/Fading: Does the summary mention if colors match marketing or if they fade?",
            # Value
            "18. Value Assessment: Does the summary assess if the case is worth the cost compared to alternatives?",
        ],
        "true_statements": [
            "**FineWoven Microtwill Material:** Crafted from Apple's premium **FineWoven fabric**, a durable microtwill made with **68% post-consumer recycled polyester**. It has a **soft, suede-like feel** with a subtle sheen, offering a luxurious hand-feel while being more eco-friendly than leather. This material is also slim and lightweight, adding minimal bulk to your iPhone 16.",
            "**MagSafe Integrated:** Built-in **MagSafe magnets** align perfectly with the iPhone 16's magnet array. The case **snaps on securely** and supports all MagSafe accessories – you can attach chargers for fast wireless charging (up to 15 W), or snap on MagSafe wallets, stands, etc., and **they stay firmly in place**. (The magnetic alignment also ensures chargers won't slip, and Apple does note that MagSafe use may leave slight imprints on the FineWoven over time, similar to how leather can develop a patina.)",
            "**Precision Fit & Protection:** This Apple-designed case precisely follows the contours of iPhone 16. It wraps around the edges to protect against scratches and minor drops, with a raised lip around the camera and screen for added defense. Inside, a **soft microfiber lining** cushions your phone. Despite the elegant fabric exterior, it's engineered for durability – lab-tested for everyday wear and tear.",
            "**Machined Metal Buttons:** The case features **anodized aluminum buttons** on the sides (color-matched to the case) that **click just like the iPhone's own buttons**, preserving a satisfying, tactile response. Cutouts for the Action button, speakers, and charging port are precise and do not impede functionality.",
            "**Environmentally Conscious & Stylish:** FineWoven cases were introduced as a sustainable alternative to leather. The material is **carbon-neutral** (when paired with Apple's renewable energy investments) and significantly reduces carbon footprint. It comes in a range of sophisticated colors – for example, charcoal black, deep blue, taupe, pacific blue, and mulberry – designed to complement the iPhone 16 finishes. The fabric resists fading and staining (it's water-resistant to small spills), though Apple recommends occasional gentle wiping to keep it looking its best. Overall, the FineWoven Case offers a blend of refined style, MagSafe convenience, and mindful craftsmanship for your iPhone 16.",
        ],
    },
    {
        "url": "https://www.amazon.com/dp/B0BJ62BW91",
        "name": "Gravol Kids Liquid",
        "questions": [
            # Effectiveness
            "1. Speed of Relief: Does the summary indicate how quickly it provides relief?",
            "2. Effectiveness for Motion Sickness: Does the summary comment on its effectiveness for motion sickness?",
            "3. Effectiveness for Stomach Bugs: Does the summary comment on its effectiveness for stomach bugs?",
            "4. Duration of Effects: Does the summary state how long the effects typically last?",
            # Side Effects
            "5. Drowsiness Level: Does the summary describe the significance of drowsiness as a side effect?",
            "6. Other Common Side Effects: Does the summary list other common side effects (dizziness, dry mouth)?",
            # Usability & Formula
            "7. Taste/Palatability for Kids: Does the summary comment on whether kids generally accept the taste?",
            "8. Dosing Tool Ease of Use: Does the summary describe the ease of using the included dosing tool?",
            "9. Dosing Tool Accuracy: Does the summary comment on the accuracy of the dosing tool?",
            "10. Active Ingredient Stated: Does the summary clearly state the active ingredient (Dimenhydrinate)?",
            "11. Concentration Stated: Does the summary state the concentration of the active ingredient?",
            "12. Recommended Minimum Age: Does the summary specify the minimum age for use?",
            "13. Dye-Free Status: Does the summary state if the formula is dye-free?",
            "14. Sugar/Sweetener Content: Does the summary provide info on sugar or artificial sweetener content?",
            # Comparison
            "15. Comparison to Alternatives: Does the summary compare it to other children's anti-nausea options?",
        ],
        "true_statements": [
            "**Child-Friendly Motion Sickness Relief:** Gravol Kids Liquid is an **anti-nausea syrup formulated for children aged 2–12**. Each 5 mL teaspoon contains **15 mg of Dimenhydrinate** (the same antiemetic agent as adult Gravol/Dramamine) which effectively **prevents and treats nausea, vomiting, and dizziness** due to motion sickness. It's ideal for car rides, flights, or boat trips to stop queasiness before it starts.",
            '**Fast-Acting & Effective:** When taken about **30–60 minutes before travel**, it helps **prevent motion sickness symptoms** so kids can enjoy the journey symptom-free. If nausea or vomiting have already begun, Gravol will help **calm the queasy feeling fairly quickly**. Parents consistently report that this syrup "works like a charm" for carsick-prone kiddos, allowing for smoother family trips with no mid-ride messes.',
            "**Dye-Free, Kid-Approved Taste:** The liquid is **free from alcohol and artificial dyes** and has a **gentle fruit flavor** (sweet grape/berry mix) that's much easier for children to take than a pill. The flavoring and sweetness (sorbitol and sucrose) mask the medicinal taste well, so there's less fuss – most kids take it willingly. It's also **gluten-free** and allergen-free.",
            "**Precise Dosing for Safety:** The product comes with a marked dosing cup (or oral syringe) for accurate measurement. Recommended dose is typically **5 mL (one teaspoon) for children 2–6 years**, and **10 mL for ages 6–12**, up to every 6–8 hours as needed. It should not be used in children under 2 unless directed by a doctor. Parents appreciate having a liquid option to tailor smaller doses by weight if needed.",
            "**Trusted Canadian Brand:** **Gravol** (by Church & Dwight Canada) has been a go-to motion sickness remedy for decades. The Kids Liquid formula is **doctor- and pharmacist-recommended** for pediatric use. It's made in Canada and **listed with Health Canada** for OTC use. As always, it's important to use as directed and be aware it may cause drowsiness (which can be a bonus on long trips). But overall, Gravol Kids Liquid is a travel essential for many families – reliably preventing car sickness meltdowns so you and your little ones can travel more comfortably.",
        ],
    },
    {
        "url": "https://www.amazon.com/Orgain-Organic-Protein-Powder-Strawberries/dp/B09SJ4WJNV/",
        "name": "Orgain Organic Protein Powder",
        "questions": [
            # Digestibility
            "1. Ease of Digestion: Does the summary comment on how easily digestible it is?",
            "2. Bloating/Gas Reports: Does the summary mention user feedback regarding bloating or gas?",
            # Taste & Texture (Strawberries & Cream)
            "3. Taste Description: Does the summary describe the taste of the Strawberries & Cream flavor?",
            "4. Sweetness Level: Does the summary comment on the sweetness level?",
            "5. Artificial Taste: Does the summary mention if it tastes artificial?",
            "6. Texture Description (Gritty/Chalky): Does the summary describe the texture (gritty, chalky, smooth)?",
            "7. Mixability: Does the summary describe how well it mixes with liquids?",
            "8. Clumping Issues: Does the summary mention issues with clumping?",
            # Ingredients & Allergens
            "9. Allergen Info (Beyond Protein): Does the summary list other potential allergens (e.g., soy)?",
            "10. Sweetener Type: Does the summary identify the type of sweetener used (erythritol, stevia)?",
            "11. Protein Sources: Does the summary list the blend of plant proteins used?",
            "12. Amino Acid Profile Info: Does the summary mention if info on the amino acid profile is available?",
            # Quality & Certifications
            "13. USDA Organic Certification: Does the summary confirm USDA Organic certification?",
            "14. Non-GMO Verification: Does the summary confirm Non-GMO Project verification?",
            "15. Heavy Metal Testing Info: Does the summary mention if Orgain provides info on heavy metal testing?",
            # Effectiveness & Value
            "16. Effectiveness for Goals: Does the summary mention user feedback on effectiveness for fitness/supplementation goals?",
            "17. Cost per Serving: Does the summary provide the cost per serving?",
            "18. Cost per Gram of Protein: Does the summary provide the cost per gram of protein?",
            "19. Value Comparison: Does the summary compare its value to other organic plant protein powders?",
        ],
        "true_statements": [
            "**Plant-Based Protein Blend (21 g):** Each serving provides **21 grams of organic plant protein** from a blend of **pea protein, brown rice protein, and chia seed**. This complete protein profile offers all essential amino acids to support muscle recovery and growth. It's a great option for vegans, vegetarians, or anyone looking to add high-quality protein to their diet without dairy.",
            "**Organic, Clean Ingredients:** Orgain's formula is **USDA Organic, non-GMO, and free of artificial sweeteners or colors**. It's naturally sweetened – the **Strawberries & Cream flavor** uses organic stevia and monk fruit (no added sugar, only 1 g sugar per serving) and natural flavors to create a smooth, not overly sweet taste reminiscent of a strawberry milkshake. There are **150 calories** per 2-scoop serving, along with 5 g of fiber and only 15 g of net carbs, making it friendly for low-carb and weight-management plans.",
            "**Allergen-Friendly & Vegan:** This powder is formulated without many common allergens – it's **dairy-free, lactose-free, gluten-free, soy-free**, and also **Kosher**. Orgain uses organic ingredients and avoids any lactose or whey, so it's easy on the stomach and suitable for those with milk or soy sensitivities. It mixes well with almond milk or oat milk for a fully vegan protein shake that's creamy and lump-free.",
            "**Great for Shakes & Baking:** The Strawberries & Cream Orgain powder blends easily into liquids – just scoop into a shaker cup or blender with water or milk for a quick smoothie. It has a **pleasant strawberry flavor** with a creamy finish that reviewers love, without the chalkiness found in some plant proteins. You can also add it to smoothies with fresh fruit, or use it in recipes (oatmeal, protein pancakes, baked goods) to boost protein intake.",
            "**Added Benefits:** Orgain's protein blend includes **naturally occurring iron and calcium** from plant sources, and chia seeds contribute omega-3 fatty acids and fiber. The product has **no erythritol** and no sugar alcohols that can cause digestive upset. It's manufactured in a cGMP-certified facility and each batch is tested for heavy metals to ensure purity. Orgain was developed by a physician and cancer survivor to **deliver clean nutrition**, and this organic protein powder is one of their best-selling, best-reviewed products – a convenient way to fuel workouts or support daily protein needs with trustworthy ingredients.",
        ],
    },
    {
        "url": "https://www.amazon.com/Quencher-Cupholder-Compatible-Insulated-Stainless/dp/B0DCDQ1RFV/",
        "name": "Stanley Quencher H2.0 FlowState Tumbler",
        "questions": [
            # Performance
            "1. Cold Retention Time: Does the summary state how long it keeps drinks cold (with ice)?",
            "2. Hot Retention Time: Does the summary state how long it keeps drinks hot?",
            "3. Meets Advertised Times: Does the summary indicate if it meets the advertised insulation times?",
            "4. Lid Leak Resistance (Straw Area): Does the summary comment on leak resistance around the straw opening?",
            "5. Lid Leak Resistance (Closed): Does the summary comment on leak resistance when the lid is closed?",
            "6. Suitability for Bag Transport: Does the summary advise if it's safe to carry in a bag without spilling?",
            "7. Taste Imparted (Metallic/Plastic): Does the summary mention user feedback on any imparted taste?",
            # Cleaning & Durability
            "8. Ease of Cleaning (Tumbler): Does the summary comment on the ease of cleaning the main tumbler body?",
            "9. Ease of Cleaning (Lid): Does the summary comment on the ease/difficulty of cleaning the FlowState lid mechanism?",
            "10. Dishwasher Safety: Does the summary confirm if all parts are dishwasher safe?",
            "11. Finish Durability (Scratches): Does the summary comment on the powder coat's resistance to scratching?",
            "12. Dent Resistance: Does the summary mention susceptibility to denting upon drops?",
            # Design & Ergonomics
            "13. Cupholder Compatibility: Does the summary confirm it fits in standard car/stroller cupholders?",
            "14. Handle Comfort: Does the summary comment on the comfort of the handle?",
            "15. Handle Security: Does the summary comment on how securely the handle is attached?",
            "16. Lid Mechanism Durability: Does the summary mention the long-term durability of the FlowState lid mechanism?",
            "17. Straw Durability: Does the summary comment on the durability of the included straw?",
        ],
        "true_statements": [
            "**Huge Hydration with Insulation:** The Stanley Quencher H2.0 is a **40 oz (1.18 L) insulated tumbler** famous for keeping drinks cold or hot for hours. Thanks to its double-wall **vacuum insulation**, it keeps water **cold for up to 9 hours, iced for ~40 hours**, and hot drinks warm for about 5–7 hours. So whether it's ice water at your desk or iced coffee on a road trip, your beverage stays at the perfect temperature all day.",
            '**"FlowState" Leak-Resistant Lid:** The upgraded **FlowState lid** features a rotating cover with three positions – one for the reusable straw, one for an open drink spout, and one fully closed. In the fully closed mode, it\'s **splash-resistant** (great for on-the-go or if tipped over briefly). The straw has a silicone stopper that keeps it in place and prevents splashes when driving or walking. This design makes it easy to sip your way (and you can remove the straw and drink from the spout as desired).',
            '**Travel-Friendly Design:** Despite its large capacity, the Quencher is designed to **fit in most car cup holders** (base diameter ~3""). It also has a sturdy **built-in handle** on the side, so carrying a full 40 oz bottle is comfortable and secure. The tapered shape and handle make it a perfect companion for commutes, workouts, or errands. *Fun fact:* this tumbler has a huge fan following because it encourages you to drink more water throughout the day.',
            "**High-Quality & Safe Materials:** Made from **18/8 stainless steel** that is highly durable and rust-proof. The interior is electropolished, so it **won't retain or impart flavors**. All plastic parts (lid, straw) are **BPA-free**. The Quencher H2.0 is also **dishwasher safe** for easy cleaning (both the steel tumbler and the lid/straw are top-rack safe). The exterior has a sweat-free powder coat finish on colored models – it won't condensate or slip.",
            '**Trendy Colors & Stanley Lifetime Warranty:** The H2.0 Quencher comes in a wide range of colors/finishes – from neutral matte charcoal or cream to fun hues like Lilac, Citron, or the popular soft matte "Eucalyptus". Stanley has been an iconic drinkware brand since 1913, and they back their products with a **lifetime warranty**. The Quencher\'s popularity on social media (often dubbed the "Stanley cup") is due to its blend of **style, quality, and functionality** – it\'s a splurge-worthy tumbler that genuinely delivers on keeping you hydrated and your drinks perfectly cold (or hot).',
        ],
    },
    {
        "url": "https://www.amazon.com/SENSARTE-Nonstick-Frying-Pan-Skillet/dp/B086PHS2V8/",
        "name": "SENSARTE Nonstick Frying Pan",
        "questions": [
            # Nonstick Performance & Durability
            "1. Initial Nonstick Effectiveness: Does the summary describe how well the nonstick works initially (e.g., with eggs)?",
            "2. Nonstick Lifespan: Does the summary provide an estimate or user feedback on how long the nonstick lasts?",
            "3. Care Instructions Adherence: Does the summary mention the importance of following care instructions for longevity?",
            # Coating Safety & Material
            "4. PFOA/PFAS Free Claim: Does the summary explicitly state it's free from PFOA/PFAS?",
            "5. Lead/Cadmium Free Claim: Does the summary explicitly state it's free from lead and cadmium?",
            "6. Coating Material Type: Does the summary identify the type of nonstick coating (e.g., granite)?",
            # Cooking Performance
            "7. Heat Distribution Evenness: Does the summary comment on how evenly the pan heats?",
            "8. Induction Compatibility: Does the summary confirm if it's suitable for induction cooktops?",
            "9. Warping Resistance: Does the summary mention resistance to warping?",
            # Cleaning & Handling
            "10. Ease of Hand Cleaning: Does the summary describe the ease of cleaning by hand?",
            "11. Dishwasher Performance (if applicable): If dishwasher use is mentioned, does the summary comment on how the pan holds up?",
            "12. Handle Comfort: Does the summary comment on the comfort of the handle grip?",
            "13. Handle Heat Resistance: Does the summary state if the handle stays cool on the stovetop?",
            "14. Oven Safety Temperature: Does the summary specify the maximum oven-safe temperature?",
            # Build & Value
            "15. Pan Body Material: Does the summary identify the material of the pan body (e.g., cast aluminum)?",
            "16. Sturdiness/Weight Balance: Does the summary comment on the pan's sturdiness or weight balance?",
            "17. Scratch Resistance (Utensils): Does the summary mention resistance to scratches from utensils?",
            "18. Value for Price: Does the summary assess the pan's value for its price?",
            "19. Available Sizes: Does the summary mention if other sizes are available?",
        ],
        "true_statements": [
            "**Swiss ILAG Granite Nonstick Coating:** Features a premium **Switzerland ILAG non-stick coating** that provides exceptional food release and durability. It's a PFOA-free, **lead and cadmium-free** formulation, approved by SGS for safety. The \"granite\" refers to its stone-like textured finish – it's ultra-smooth and scratch-resistant, allowing you to cook with minimal oil for healthier meals (and making cleanup as easy as a quick wipe).",
            "**Fast & Even Heating:** Constructed from high-grade **cast aluminum**, the pan heats up quickly and evenly without hot spots. It has a thick bottom for stability and a thinner sidewall for responsive heat – this means you get the even cooking of cast iron or stainless steel, but at a fraction of the weight. Perfect for everything from searing proteins to simmering sauces or frying eggs without scorching.",
            "**All-Stove Compatible (Induction Ready):** The base of the SENSARTE skillet incorporates a **high-magnetic stainless steel plate**, making it **suitable for all stovetops** – gas, electric, ceramic, **and induction** cooktops. The bottom is flat and smooth for optimal contact on glass tops. Users report it works great on induction, heating up fast and maintaining steady temperature thanks to the magnetic steel layer.",
            "**Ergonomic Cool-Touch Handle:** Attached is a comfortable **bakelite handle with a woodgrain finish** (looks like wood but much more durable). It's designed to stay **cool on the stovetop**, so you can maneuver the pan without oven mitts. The handle is securely riveted and has a convenient hanging hole for storage. (Note: because of the handle, the pan is **oven-safe only up to ~300°F** for warming, not high-temp baking or broiling.)",
            "**User-Friendly & Easy Clean:** Lightweight (compared to cast iron or steel pans) and **dishwasher safe** (though hand washing is recommended to prolong the nonstick). Cleaning is a breeze – usually just a soft sponge rinse will do, as food slides right off the coating. The pan's interior depth and gently sloped sides make it versatile for different cooking tasks (sautéing, stir-frying, flipping pancakes). SENSARTE even includes a soft sponged scrubber in some packages. Overall, it's a **chef-worthy skillet with home-kitchen convenience**, offering great value for a granite-coated pan in this price range.",
        ],
    },
]
