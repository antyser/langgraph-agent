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

PRODUCTS_TO_EVALUATE: List[Dict[str, Any]] = [
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
    },
]
