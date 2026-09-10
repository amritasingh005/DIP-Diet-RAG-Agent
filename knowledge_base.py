"""
DIP Diet RAG Agent - Knowledge Base
====================================
Curated DIP Diet knowledge used to seed the vector store.
Each entry is a document chunk with metadata.
"""

DIP_KNOWLEDGE_BASE = [
    # ─────────────────────────────────────────────
    # SECTION 1: WHAT IS DIP DIET
    # ─────────────────────────────────────────────
    {
        "id": "dip_001",
        "source": "DIP Diet Foundation Guide",
        "section": "Introduction",
        "content": """The DIP Diet stands for Disciplined Intelligent Personalized Diet. It was popularized by Dr. Biswaroop Roy Chowdhury and is based on whole, plant-based foods with a focus on natural eating patterns. The DIP Diet emphasizes eating two meals a day, eliminating refined and processed foods, and adopting a holistic lifestyle that includes sunlight, physical activity, and mindful eating. The protocol has shown promising results for managing chronic diseases including Type 2 Diabetes, hypertension, obesity, and metabolic syndrome when followed consistently."""
    },
    {
        "id": "dip_002",
        "source": "DIP Diet Foundation Guide",
        "section": "Core Principles",
        "content": """The 10 core principles of the DIP Diet are: (1) Eat only two meals per day — breakfast and lunch/dinner. (2) The morning meal should consist exclusively of raw fruits. (3) The second meal should be a balanced plate with 50% raw salad, 25% cooked vegetables, and 25% whole grains or legumes. (4) No snacking between meals. (5) No refined sugar, maida, or refined oils. (6) No animal products in the strict version (whole-food plant-based). (7) Adequate hydration between meals, not during meals. (8) 20-30 minutes of morning sunlight daily. (9) Daily physical activity — walking, yoga, or exercise. (10) Mindful eating — chew 32 times, eat in peace, express gratitude."""
    },
    {
        "id": "dip_003",
        "source": "DIP Diet Foundation Guide",
        "section": "Two Meal Protocol",
        "content": """The Two-Meal-A-Day (2MAD) protocol is central to the DIP Diet. The first meal (breakfast/brunch) should be eaten after some physical activity and morning sunlight exposure, typically between 8-10 AM. This meal should consist entirely of fresh, ripe, seasonal fruits — a variety of at least 3-5 fruits is recommended. The second meal (lunch or early dinner) should be eaten between 1-6 PM. Eating after 7 PM is discouraged. The gap between meals allows the body to digest, rest, and repair. This eating window naturally creates intermittent fasting benefits without strict calorie counting."""
    },
    {
        "id": "dip_004",
        "source": "DIP Diet Foundation Guide",
        "section": "The DIP Plate",
        "content": """The DIP Diet plate is divided into three sections: (1) 50% Raw Foods — fresh fruits or raw salad (cucumber, tomato, carrot, beetroot, sprouts, leafy greens). This provides live enzymes, fiber, vitamins, and antioxidants. (2) 25% Cooked Vegetables — lightly steamed, pressure-cooked, or water-sautéed vegetables like palak, lauki, tinda, karela, bhindi, pumpkin. Avoid heavy frying. (3) 25% Whole Grains or Legumes — whole wheat roti, brown rice, millet roti, dal, rajma, chana, moong, masoor. This provides complex carbohydrates and plant protein. No refined oils in cooking — use water sautéing or steam cooking."""
    },
    # ─────────────────────────────────────────────
    # SECTION 2: DIABETES & DISEASE REVERSAL
    # ─────────────────────────────────────────────
    {
        "id": "dip_005",
        "source": "DIP Diet & Diabetes Reversal Manual",
        "section": "Diabetes Management",
        "content": """The DIP Diet has been studied as a supportive dietary approach for Type 2 Diabetes management. A whole-food plant-based diet naturally lowers blood sugar by reducing refined carbohydrate and fat intake, improving insulin sensitivity through increased fiber and phytonutrients, reducing body weight and visceral fat, and providing anti-inflammatory compounds from fruits and vegetables. Key foods for diabetes management on DIP Diet: bitter gourd (karela), fenugreek seeds (methi), amla (Indian gooseberry), jamun, drumstick leaves (moringa), turmeric, cinnamon, and fiber-rich whole grains like oats, ragi, and barley. DISCLAIMER: Always consult your doctor before modifying diabetes medication based on dietary changes."""
    },
    {
        "id": "dip_006",
        "source": "DIP Diet & Diabetes Reversal Manual",
        "section": "Blood Sugar Management Foods",
        "content": """Foods that help manage blood sugar on the DIP Diet: LOW GLYCEMIC INDEX FOODS: Green leafy vegetables, bitter gourd, cucumber, bottle gourd, ridge gourd, cluster beans, broccoli, cauliflower. MEDIUM GI WHOLE FOODS: Brown rice, whole wheat, oats, barley, millets (ragi, jowar, bajra, foxtail millet). AVOID HIGH GI FOODS: White rice, maida, white bread, sugar, sweets, fruit juices (whole fruit preferred over juice). BENEFICIAL SPICES: Turmeric (anti-inflammatory), fenugreek seeds (lower blood sugar), cinnamon (insulin sensitizer), ginger (anti-inflammatory). DAILY RECOMMENDATIONS: Eat at least 1 serving of bitter gourd weekly, consume 1 tablespoon of soaked fenugreek seeds on an empty stomach if tolerated."""
    },
    # ─────────────────────────────────────────────
    # SECTION 3: INDIAN FOODS & SUBSTITUTIONS
    # ─────────────────────────────────────────────
    {
        "id": "dip_007",
        "source": "Indian DIP Diet Food Guide",
        "section": "Traditional Indian Foods in DIP Diet",
        "content": """Traditional Indian foods compatible with the DIP Diet: GRAINS: Whole wheat roti/chapati, brown rice, ragi (finger millet) roti, jowar roti, bajra roti, oat upma, poha (beaten rice), quinoa. LEGUMES: All dals (moong, masoor, toor, urad, chana), rajma (kidney beans), kabuli chana (chickpeas), cowpea (lobia), soya chunks, sprouts. VEGETABLES: All vegetables are encouraged — especially bitter gourd, ash gourd (petha), drumstick (sahjan), moringa leaves, spinach, amaranth (chaulai), fenugreek leaves (methi), ridge gourd, bottle gourd. FRUITS: All seasonal fruits — banana, papaya, mango, guava, amla, jamun, watermelon, pomegranate, chikoo, apple, pear, citrus fruits. FERMENTED FOODS: Idli, dosa (from whole grain batter), kanji (fermented carrot drink), homemade pickles without excess oil."""
    },
    {
        "id": "dip_008",
        "source": "Indian DIP Diet Food Guide",
        "section": "Food Substitutions",
        "content": """DIP Diet food substitutions for common Indian ingredients: INSTEAD OF refined sugar → Use dates, jaggery (in limited amounts), raisins, figs, or ripe banana as natural sweetener. INSTEAD OF maida (refined wheat flour) → Use whole wheat atta, ragi flour, besan (chickpea flour), oat flour, almond flour. INSTEAD OF white rice → Use brown rice, red rice, black rice, foxtail millet (kangni), little millet (kutki), barnyard millet (jhangora). INSTEAD OF refined cooking oil → Water sauté with vegetable broth; use minimal cold-pressed coconut oil or groundnut oil only when absolutely needed. INSTEAD OF milk (for WFPB) → Use homemade soy milk, peanut milk, oat milk, or unsweetened almond milk. INSTEAD OF ghee/butter → Use avocado spread, nut butters, or eliminate entirely. INSTEAD OF commercial biscuits/namkeen → Roasted chana, makhana (fox nuts), fresh fruit, soaked almonds/walnuts."""
    },
    {
        "id": "dip_009",
        "source": "Indian DIP Diet Food Guide",
        "section": "Indian Superfoods",
        "content": """Indian superfoods emphasized in the DIP Diet: AMLA (Indian Gooseberry): Highest vitamin C content of any food, powerful antioxidant, liver protective, supports immunity. Eat 1-2 fresh amla daily or 1 tsp amla powder. ASH GOURD (Petha/Winter Melon): Highly alkaline, excellent for gut health, reduces inflammation, 96% water content. MORINGA (Drumstick Leaves): Complete plant protein (all amino acids), 25x more iron than spinach, 17x more calcium than milk, rich in antioxidants. TULSI (Holy Basil): Adaptogenic herb, reduces cortisol, anti-inflammatory, antimicrobial. Drink as tea or chew fresh leaves. TURMERIC: Curcumin is anti-inflammatory and neuroprotective. Use with black pepper for bioavailability. FLAXSEEDS: Richest plant source of omega-3 fatty acids (ALA). 1-2 tablespoons ground flaxseeds daily."""
    },
    # ─────────────────────────────────────────────
    # SECTION 4: MEAL PLANS
    # ─────────────────────────────────────────────
    {
        "id": "dip_010",
        "source": "DIP Diet Meal Planning Guide",
        "section": "Sample Daily Meal Plan - Standard",
        "content": """SAMPLE DIP DIET DAILY PLAN (Standard): MORNING ROUTINE (6-7 AM): Wake up, drink 1-2 glasses warm water with lemon, 20 min morning walk or yoga, 15 min sunlight exposure. MEAL 1 - FRUIT BREAKFAST (8-10 AM): 2 bananas + 1 papaya (medium) + 1 guava + handful of pomegranate seeds + 10 soaked almonds + 5 walnuts. Total: Approx 400-500 calories, high in fiber, vitamins C & B6, potassium. MEAL 2 - MAIN MEAL (1-2 PM): Large salad (cucumber, tomato, carrot, beetroot, sprouts, lemon dressing) + 2 whole wheat rotis + 1 bowl dal (moong or masoor) + 1 sabzi (any cooked vegetable) + small bowl brown rice (optional). HYDRATION: 8-10 glasses of water between meals. EVENING (6-8 PM): Herbal tea (tulsi/ginger), light walk. NO SNACKING between meals."""
    },
    {
        "id": "dip_011",
        "source": "DIP Diet Meal Planning Guide",
        "section": "Sample Daily Meal Plan - Diabetes Friendly",
        "content": """DIABETES-FRIENDLY DIP DIET DAILY PLAN: MORNING (6 AM): Warm water + 1 tbsp soaked fenugreek seeds. MEAL 1 (9 AM): 1 small banana + 1 guava + 1 pear + 1 amla (fresh or powder) + 15 soaked almonds. Avoid mango, chikoo in large quantities. MEAL 2 (12-1 PM): Karela (bitter gourd) sabzi + 1 ragi roti + 1 bowl moong dal + large salad with methi leaves + cucumber raita (with plant milk yogurt). POST MEAL: Walk for 15 minutes after second meal to lower blood sugar response. AVOID: Fruit juices, white rice, maida items, sweets, fried snacks, processed foods. WATER: 10-12 glasses between meals. NOTE: Monitor blood sugar regularly. Consult physician before reducing diabetes medication."""
    },
    {
        "id": "dip_012",
        "source": "DIP Diet Meal Planning Guide",
        "section": "Weekly Meal Plan Overview",
        "content": """DIP DIET WEEKLY MEAL PLAN STRUCTURE: MONDAY: Fruit meal (banana, papaya, apple) + Lunch: Dal khichdi (brown rice + moong dal) + salad. TUESDAY: Fruit meal (seasonal fruits) + Lunch: Rajma (kidney beans) + roti + sabzi + salad. WEDNESDAY: Fruit meal (citrus fruits, guava) + Lunch: Chana masala + jowar roti + salad. THURSDAY: Fruit meal (banana, pomegranate) + Lunch: Palak dal + brown rice + salad. FRIDAY: Fruit meal (seasonal) + Lunch: Mixed vegetable stew + millet roti + salad. SATURDAY: Fruit meal + Lunch: Sprouted moong curry + ragi roti + salad. SUNDAY: Extended fruit meal (larger quantity) + Late lunch: Dal makhani (oil-free) + whole wheat roti + salad. PROTEIN ROTATION: Rotate legumes daily to get a full amino acid profile. MILLET ROTATION: Include at least 3 different millets per week."""
    },
    # ─────────────────────────────────────────────
    # SECTION 5: LIFESTYLE & DISCIPLINE
    # ─────────────────────────────────────────────
    {
        "id": "dip_013",
        "source": "DIP Diet Lifestyle Guide",
        "section": "Morning Routine",
        "content": """THE DIP DIET MORNING PROTOCOL: 5:30-6:00 AM: Wake up naturally if possible (use gentle alarm). Begin with 2 glasses warm water, optionally with half lemon juice or a pinch of black salt. 6:00-6:30 AM: Light physical activity — 20-30 minute brisk walk, yoga, pranayama, or stretching. No intense exercise on an empty stomach. 6:30-7:00 AM: Sunlight exposure — stand in direct morning sunlight for 15-20 minutes. Morning sunlight regulates circadian rhythm, increases Vitamin D production, improves mood (serotonin), and supports melatonin regulation for better sleep at night. 7:00-8:00 AM: Personal hygiene, mindfulness/meditation (5-10 minutes). 8:00-10:00 AM: Have Meal 1 (fruit meal). Eat slowly, chew well, sit down to eat without distractions."""
    },
    {
        "id": "dip_014",
        "source": "DIP Diet Lifestyle Guide",
        "section": "Sleep & Recovery",
        "content": """SLEEP OPTIMIZATION FOR DIP DIET SUCCESS: Aim for 7-8 hours of uninterrupted sleep. Ideal sleep time: 10 PM - 5:30 AM (aligns with natural circadian rhythm). TIPS FOR BETTER SLEEP: Avoid eating within 3 hours of bedtime (this is why early dinner is key in DIP Diet). Avoid screens (phone, TV, laptop) 1 hour before bed. Sleep in a dark, cool room (18-21°C is optimal). Practice 5 minutes of deep breathing or yoga nidra before sleep. Avoid caffeine after 2 PM. SLEEP & METABOLISM: Poor sleep increases ghrelin (hunger hormone) and decreases leptin (satiety hormone), leading to overeating. 7 hours of sleep improves insulin sensitivity by 20-30%. Good sleep supports cellular repair, detoxification, and metabolic health — all essential for DIP Diet results."""
    },
    {
        "id": "dip_015",
        "source": "DIP Diet Lifestyle Guide",
        "section": "Exercise & Physical Activity",
        "content": """EXERCISE RECOMMENDATIONS FOR DIP DIET: DAILY MINIMUM: 30 minutes of moderate activity — brisk walking is the most recommended. OPTIMAL PROTOCOL: Morning: 20-30 min yoga or light stretching. Daytime: 10-min walk after meals (especially after lunch — reduces post-meal blood sugar spike). Evening: 20-30 min walk in natural surroundings. STRENGTH TRAINING: 2-3 sessions per week of bodyweight exercises (pushups, squats, lunges) or light weights helps maintain muscle mass on a plant-based diet. YOGA ASANAS for metabolic health: Surya Namaskar (12 rounds), Paschimottanasana, Mandukasana (helps diabetes), Sarvangasana (thyroid support), Shavasana (stress relief). AVOID: Intense exercise in the hottest part of the day. Exercising immediately after meals. Long periods of sitting — take a 5-min movement break every hour."""
    },
    {
        "id": "dip_016",
        "source": "DIP Diet Lifestyle Guide",
        "section": "Mindful Eating",
        "content": """MINDFUL EATING PRACTICES IN DIP DIET: BEFORE EATING: Wash hands, sit down, express gratitude for the food. Take 3 deep breaths. Turn off screens and phone notifications. DURING EATING: Chew each bite 30-40 times (improves digestion, nutrient absorption). Eat slowly — take at least 20-30 minutes per meal. Focus on the taste, texture, and aroma of food. Stop when 80% full (Japanese concept of 'Hara Hachi Bu'). AFTER EATING: Sit quietly for 5-10 minutes after the meal. A short walk (15 min) helps digestion. Avoid lying down immediately after eating. SOCIAL EATING: Eating with family or community enhances the experience and encourages mindful pace. EMOTIONAL EATING: If you notice stress eating or emotional food cravings, practice 4-7-8 breathing technique and identify the underlying emotion before reaching for food."""
    },
    # ─────────────────────────────────────────────
    # SECTION 6: SPECIFIC CONDITIONS
    # ─────────────────────────────────────────────
    {
        "id": "dip_017",
        "source": "DIP Diet Health Conditions Guide",
        "section": "PCOS & Hormonal Health",
        "content": """DIP DIET FOR PCOS (Polycystic Ovary Syndrome): PCOS is strongly linked to insulin resistance and inflammation. The DIP Diet addresses both root causes. ANTI-INFLAMMATORY FOODS TO EMPHASIZE: Berries, pomegranate, amla, turmeric, ginger, flaxseeds (lignans balance hormones), green leafy vegetables. FOODS TO AVOID: Dairy (linked to increased androgen levels), refined sugar (spikes insulin), processed soy products in excess, refined flour. BENEFICIAL PRACTICES: Regular exercise improves insulin sensitivity. Sleep at consistent times (poor sleep worsens hormonal imbalance). Stress reduction (high cortisol worsens PCOS). SPECIFIC RECOMMENDATIONS: 1 tbsp ground flaxseeds daily for lignan content. Spearmint tea (anti-androgenic properties). Cinnamon in warm water in the morning. Include cruciferous vegetables (broccoli, cauliflower) for estrogen metabolism support. DISCLAIMER: Consult your gynecologist/endocrinologist for PCOS management."""
    },
    {
        "id": "dip_018",
        "source": "DIP Diet Health Conditions Guide",
        "section": "Heart Health",
        "content": """DIP DIET FOR HEART HEALTH & HYPERTENSION: A whole-food plant-based diet is the most evidence-based dietary approach for cardiovascular disease prevention and reversal. KEY HEART-HEALTHY FOODS IN DIP DIET: Oats (beta-glucan lowers LDL), flaxseeds (omega-3), walnuts (ALA omega-3), garlic (lowers blood pressure), pomegranate (reduces arterial stiffness), tomatoes (lycopene), dark leafy greens (folate, magnesium), beans and lentils (soluble fiber). REDUCE SODIUM: Avoid pickles, papads, canned foods, table salt excess. Use herbs and spices for flavor. AVOID SATURATED FAT SOURCES: Ghee, butter, coconut oil (in excess), full-fat dairy, fried foods. BLOOD PRESSURE MANAGEMENT: DASH-compliant foods overlap greatly with DIP Diet. Increase potassium (bananas, spinach, sweet potato). Magnesium from legumes, seeds, and leafy greens is a natural calcium channel blocker. DISCLAIMER: Do not modify heart medications without medical supervision."""
    },
    {
        "id": "dip_019",
        "source": "DIP Diet Health Conditions Guide",
        "section": "Weight Management",
        "content": """DIP DIET FOR WEIGHT LOSS & WEIGHT MANAGEMENT: The DIP Diet promotes sustainable, gradual weight loss without calorie counting by: (1) High fiber foods create satiety with fewer calories. (2) Two meals naturally reduce total caloric intake. (3) No snacking eliminates mindless caloric consumption. (4) Whole plant foods have lower caloric density than processed foods. EXPECTED WEIGHT LOSS: 2-4 kg per month in the first 3 months is typical and healthy. Faster loss may indicate inadequate nutrition. FOODS THAT AID FAT LOSS: All non-starchy vegetables (very low calorie density), raw salads, fruits (despite sugar, whole fruit promotes weight loss due to fiber), legumes (high protein + fiber = high satiety). FOODS TO MINIMIZE IF OVERWEIGHT: Dried fruits in excess, nuts in excess (calorie-dense), coconut milk, avocado in large quantities. IMPORTANT: Never go below 1200 kcal/day for women or 1500 kcal/day for men without medical supervision."""
    },
    # ─────────────────────────────────────────────
    # SECTION 7: NUTRITION SCIENCE
    # ─────────────────────────────────────────────
    {
        "id": "dip_020",
        "source": "DIP Diet Nutrition Science Reference",
        "section": "Plant Protein Sources",
        "content": """COMPLETE PLANT PROTEIN GUIDE FOR DIP DIET: HIGHEST PROTEIN LEGUMES (per 100g cooked): Lentils (masoor dal): 9g protein. Chickpeas (kabuli chana): 9g protein. Black beans: 9g protein. Kidney beans (rajma): 9g. Edamame/Soya: 11g protein. Tofu (firm): 8g protein. COMPLETE PROTEINS (all essential amino acids): Soy products (tofu, tempeh, edamame), quinoa, buckwheat, amaranth (rajgira). COMPLEMENTARY PROTEIN COMBINATIONS: Dal + Rice (classic Indian combination — completes amino acid profile). Roti + Dal. Hummus + whole wheat pita. DAILY PROTEIN REQUIREMENTS: 0.8g per kg bodyweight for sedentary adults. 1.2-1.6g per kg for active individuals. A 70kg person needs ~56g protein/day (sedentary) to 112g/day (very active). PROTEIN-RICH DIP DIET MEAL EXAMPLE: 1 cup cooked dal (9g) + 100g tofu (8g) + 2 rotis (4g) + salad with sprouts (4g) = ~25g protein per meal."""
    },
    {
        "id": "dip_021",
        "source": "DIP Diet Nutrition Science Reference",
        "section": "Vitamins & Minerals on Plant-Based Diet",
        "content": """KEY NUTRIENTS TO MONITOR ON DIP DIET: VITAMIN B12: NOT found in plant foods. MUST SUPPLEMENT if fully plant-based. Recommended: 500-1000 mcg cyanocobalamin or methylcobalamin weekly. Deficiency causes: nerve damage, anemia, fatigue, memory problems. VITAMIN D: Get 20+ min morning sunlight daily. Supplement 1000-2000 IU if sunlight is insufficient. IRON: Plant iron (non-heme) is less absorbable. BOOST ABSORPTION: Eat iron-rich foods (spinach, lentils, seeds) with Vitamin C (lemon, amla, guava). AVOID: Tea/coffee with meals (tannins inhibit iron absorption). CALCIUM: Sources — sesame seeds (til), finger millet (ragi), amaranth, soy products, almonds, figs. OMEGA-3: Ground flaxseeds (1-2 tbsp/day), walnuts (5-7), chia seeds provide ALA. Consider algae-based DHA/EPA supplement. ZINC: Pumpkin seeds, hemp seeds, legumes, cashews. Soaking and sprouting legumes improves zinc bioavailability. IODINE: Use iodized salt (minimal) or sea vegetables. Important for thyroid function."""
    },
    {
        "id": "dip_022",
        "source": "DIP Diet Nutrition Science Reference",
        "section": "Fiber & Gut Health",
        "content": """FIBER & GUT HEALTH IN DIP DIET: The DIP Diet is naturally very high in dietary fiber. RECOMMENDED INTAKE: 25-38g per day. Most DIP Diet followers consume 40-60g+ daily. HIGH-FIBER DIP FOODS: Rajma (25g/cup), lentils (16g/cup), black beans (15g/cup), oats (4g/cup cooked), avocado (10g each), pears (5.5g), broccoli (5g/cup). GUT MICROBIOME BENEFITS: High fiber feeds beneficial gut bacteria (prebiotics). Fermented foods (idli, dosa, kanji, homemade pickles) provide probiotics. A diverse plant-based diet increases microbial diversity — linked to better immunity, mood, metabolism, and reduced disease risk. TRANSITION TIPS: If transitioning from a low-fiber diet, increase fiber gradually over 4-6 weeks to prevent gas and bloating. Drink plenty of water. Soak and cook legumes thoroughly. Use asafoetida (hing) and ginger in dal cooking to reduce gas."""
    },
    # ─────────────────────────────────────────────
    # SECTION 8: FASTING & SPECIAL OCCASIONS
    # ─────────────────────────────────────────────
    {
        "id": "dip_023",
        "source": "Indian DIP Diet Cultural Guide",
        "section": "Religious Fasting & DIP Diet",
        "content": """DIP DIET & INDIAN RELIGIOUS FASTING: The DIP Diet's two-meal approach aligns well with traditional Indian fasting practices. EKADASHI FASTING: Eat only fruits and water on Ekadashi days — perfectly compatible with DIP Diet. This is essentially a fruit-only day which gives the digestive system rest. NAVRATRI FASTING: DIP-compatible options: sabudana khichdi (in moderation), kuttu (buckwheat) roti, singhara atta, fresh fruits, dry fruits, makhana (fox nuts). AVOID during Navratri fasting: refined grain products, excessive ghee, sugar-laden sweets. RAMADAN: DIP Diet can be adapted — have a fruit-rich sehri (pre-dawn meal) and a balanced DIP plate for iftar. Avoid deep-fried items and sweets. GENERAL FASTING BENEFITS: Fasting from sunset to sunrise naturally aligns with DIP Diet's early dinner recommendation. Fasting gives the gut rest, activates autophagy (cellular cleaning), and improves insulin sensitivity."""
    },
    {
        "id": "dip_024",
        "source": "Indian DIP Diet Cultural Guide",
        "section": "Festival Foods & Healthier Alternatives",
        "content": """FESTIVAL FOODS — HEALTHIER DIP DIET VERSIONS: DIWALI: Replace mithai (sweets) → date-nut energy balls (dates + nuts + cardamom), dry fruit barfi (no added sugar), baked mathri (whole wheat). Replace deep-fried snacks → roasted makhana, baked chakli (ragi/whole wheat). HOLI: Replace gujiya → baked whole wheat gujiya with date-nut filling. Replace bhang drinks → fresh fruit smoothies with cooling spices. CHRISTMAS: Replace plum cake → whole grain fruit cake with jaggery and dry fruits. Replace rich gravies → lentil-based stews and roasted vegetables. EID: Replace sheer khurma → oat kheer with dates, saffron, and plant milk. Replace biryani → brown rice/millet biryani with vegetables and soy chunks. GENERAL TIPS FOR FESTIVALS: Eat a large fruit meal before attending events to avoid hunger-driven poor choices. Choose dry snacks over fried when available. Enjoy a small portion of traditional sweets rather than eliminating joy from celebrations."""
    },
    # ─────────────────────────────────────────────
    # SECTION 9: FREQUENTLY ASKED QUESTIONS
    # ─────────────────────────────────────────────
    {
        "id": "dip_025",
        "source": "DIP Diet FAQ Guide",
        "section": "Common Questions",
        "content": """FREQUENTLY ASKED QUESTIONS ABOUT DIP DIET: Q: Will I get enough protein on DIP Diet? A: Yes, if you eat adequate legumes, sprouts, tofu, and whole grains daily. Protein deficiency is rare on a well-planned plant-based diet. Q: Can children follow DIP Diet? A: A modified version can work for children with pediatrician guidance. Children need more frequent meals and should not follow strict 2MAD. Q: Is DIP Diet suitable during pregnancy? A: Pregnant women should NOT follow restrictive eating windows. A nutrient-dense plant-based diet is beneficial but consult your OB/GYN. Ensure adequate B12, iron, calcium, and DHA. Q: What if I feel hungry between meals? A: Initially normal. Hunger adapts within 2-3 weeks. Drink water or herbal tea. Ensure meals are calorie-sufficient and fiber-rich. Q: Can I drink coffee or tea? A: Herbal teas are preferred. If needed, black coffee or green tea in moderation, not with meals. Avoid milk tea with sugar. Q: How quickly will I see results? A: Most people notice improved energy in 1-2 weeks, weight changes in 3-4 weeks, and significant health improvements in 3-6 months of consistent adherence."""
    },
    {
        "id": "dip_026",
        "source": "DIP Diet FAQ Guide",
        "section": "Challenges & Solutions",
        "content": """COMMON DIP DIET CHALLENGES & SOLUTIONS: CHALLENGE: Social pressure to eat non-DIP foods at gatherings. SOLUTION: Eat a fruit meal before events, politely explain your health choices, choose the best available option, don't stress about one meal. CHALLENGE: Difficulty giving up tea/coffee habit. SOLUTION: Gradually replace: first eliminate sugar, then transition to green tea, then to herbal teas (ginger-tulsi, chamomile). CHALLENGE: Family members not following DIP Diet. SOLUTION: Cook shared meals that happen to be DIP-compatible. Focus on your own journey. Lead by example. CHALLENGE: Eating out at restaurants. SOLUTION: Choose dal-based dishes, sabzi without excess oil, tandoori items, idli/dosa, salads. Request less oil. Avoid biryani, paneer in cream sauce, fried items. CHALLENGE: Traveling or busy schedule. SOLUTION: Carry whole fruits as backup. Order fruit salads. Identify DIP-friendly restaurant options in advance. CHALLENGE: Digestive issues when starting. SOLUTION: Introduce high-fiber foods gradually. Soak legumes 8+ hours. Cook thoroughly. Use digestive spices (hing, jeera, ajwain)."""
    },
    # ─────────────────────────────────────────────
    # SECTION 10: RECIPES
    # ─────────────────────────────────────────────
    {
        "id": "dip_027",
        "source": "DIP Diet Recipe Collection",
        "section": "Basic Recipes",
        "content": """DIP DIET OIL-FREE RECIPES: WATER-SAUTÉED DAL TADKA: Heat pan, add 2 tbsp water. Add cumin seeds, dried red chili, mustard seeds. Let splutter. Add chopped onion, cook stirring with water as needed. Add tomatoes, turmeric, coriander powder, salt. Cook until soft. Add to cooked dal. Finish with lemon and fresh coriander. OIL-FREE STIR-FRIED VEGETABLES: In a wok, add 2-3 tbsp vegetable broth or water. Add minced garlic and ginger. Add hard vegetables first (carrots, broccoli), then soft ones (zucchini, spinach). Season with soy sauce (low sodium), turmeric, black pepper, lemon. RAGI (FINGER MILLET) ROTI: Mix 1 cup ragi flour with warm water, pinch salt, optionally add finely chopped spinach or methi. Knead into soft dough. Roll thin (dust with ragi flour). Cook on dry tawa until spots appear. Rich in calcium (344mg/100g), iron, and fiber. SPROUT CHAAT: Mixed sprouts (moong, moth, chana) + cucumber + tomato + onion + green chili + chaat masala + lemon juice + fresh coriander. NO oil needed."""
    },
    {
        "id": "dip_028",
        "source": "DIP Diet Recipe Collection",
        "section": "Smoothies & Beverages",
        "content": """DIP DIET APPROVED BEVERAGES & SMOOTHIES: GREEN DETOX SMOOTHIE: 1 cup spinach or moringa leaves + 1 banana + 1 apple + 1/2 inch ginger + 1 glass water. Blend until smooth. Rich in iron, vitamins, and phytonutrients. AMLA IMMUNITY BOOSTER: 2 fresh amla (or 1 tsp amla powder) + 1 cup warm water + pinch of black salt + few fresh mint leaves. Drink first thing in the morning. ASH GOURD JUICE: Blend raw ash gourd (petha) with water. Strain. Drink on empty stomach. Highly alkaline, anti-inflammatory, improves gut health. TURMERIC GOLDEN MILK: 1 cup unsweetened plant milk + 1/2 tsp turmeric + 1/4 tsp ginger powder + pinch black pepper + dates for sweetness. Heat gently. GINGER-TULSI HERBAL TEA: Boil water with 5-6 tulsi leaves + 1-inch ginger (grated). Simmer 5 min. Strain, add lemon and honey (optional). AVOID: Packaged fruit juices (even 100% juice has no fiber), carbonated drinks, alcohol, milk-based commercial beverages."""
    }
]
