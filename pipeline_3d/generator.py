import os
import json
import random
import re
import urllib.request

CURATED_3D_POOL = [
    {
        "title": "What Happens If You Swallow Chewing Gum?",
        "voice": "am_michael",
        "speed": 1.02,
        "lead": 0.35,
        "outro": 1.0,
        "gap": 0.26,
        "music": "tension",
        "sources": [
            "Mayo Clinic, 'Is swallowing gum harmful?' (gum base is indigestible but passes naturally)",
            "American Academy of Pediatrics (foreign body ingestion)"
        ],
        "lines": [
            { "text": "You've probably heard that swallowing gum takes seven years to digest.", "caps": "Swallowing *gum | takes *7 years | to *digest?" },
            { "text": "Well, that is completely false.", "caps": "Well, that is | *completely *false" },
            { "text": "When you swallow gum, it slides down your esophagus into your stomach.", "caps": "Slides down | your *esophagus | into your *stomach" },
            { "text": "Your powerful stomach acids break down the sweeteners and flavorings,", "caps": "Stomach *acids | break down *sweeteners | and *flavors" },
            { "text": "but your body cannot dissolve the rubbery gum base.", "caps": "Cannot *dissolve | the rubbery *gum base" },
            { "text": "Instead of staying stuck for seven years,", "caps": "Instead of *staying stuck | for *7 years" },
            { "text": "your digestive muscles keep contracting,", "caps": "Digestive *muscles | keep *contracting" },
            { "text": "pushing it through your intestines just like normal food.", "caps": "Pushing it | through your *intestines | like normal *food" },
            { "text": "Within a few days, it quietly leaves your body.", "caps": "Within a *few days | it *quietly *leaves | your *body" },
            { "text": "Just don't swallow a huge wad at once, or it could cause a blockage.", "caps": "Never swallow | a *huge wad | could cause a *blockage", "gap": 0.2 }
        ],
        "metadata": {
            "title": "What Happens If You Swallow Gum? (Truth Revealed) #shorts",
            "description": "Does swallowing chewing gum really stay in your body for 7 years? Here's the science breakdown of what actually happens inside your digestive system. #shorts #science #facts #animation",
            "tags": ["shorts", "science", "facts", "animation", "health", "human body"]
        }
    },
    {
        "title": "What Happens If You Crack Your Knuckles?",
        "voice": "am_michael",
        "speed": 1.03,
        "lead": 0.35,
        "outro": 1.0,
        "gap": 0.26,
        "music": "tension",
        "sources": [
            "Harvard Health, 'Does knuckle popping cause arthritis?'",
            "Radiological Society of North America (ultrasound analysis of cavitation bubbles)"
        ],
        "lines": [
            { "text": "What is actually happening inside your fingers when you crack your knuckles?", "caps": "What *happens | inside your *fingers | when you *crack them?" },
            { "text": "It turns out, your bones are not rubbing together at all.", "caps": "Your *bones | are not *rubbing | together at *all" },
            { "text": "Between your joints, there is a slippery fluid called synovial fluid.", "caps": "Between *joints | a slippery *fluid | lubricates *movement" },
            { "text": "When you pull or bend your finger,", "caps": "When you *pull | or *bend | your *finger" },
            { "text": "the joint expands, creating a sudden drop in pressure.", "caps": "The joint *expands | sudden *drop | in *pressure" },
            { "text": "This pressure drop causes microscopic gas bubbles to rapidly form and collapse.", "caps": "Gas *bubbles | rapidly *form | and *collapse" },
            { "text": "That loud pop you hear is literally gas cavities forming in the fluid.", "caps": "That loud *pop | is *gas cavities | in the *fluid" },
            { "text": "And no, decades of medical studies prove it does not cause arthritis.", "caps": "Decades of *studies | prove it *does not | cause *arthritis" },
            { "text": "It takes about twenty minutes for the gas to dissolve back before you can pop them again.", "caps": "Takes *20 minutes | for gas to *dissolve | before next *pop", "gap": 0.2 }
        ],
        "metadata": {
            "title": "What Happens When You Crack Your Knuckles? #shorts",
            "description": "What causes that loud popping sound when you crack your knuckles? Here is what's really happening inside your joint fluid. #shorts #facts #health #science",
            "tags": ["shorts", "science", "facts", "knuckles", "health", "animation"]
        }
    },
    {
        "title": "What Happens If You Drink Sea Water?",
        "voice": "am_michael",
        "speed": 1.04,
        "lead": 0.35,
        "outro": 1.0,
        "gap": 0.26,
        "music": "tension",
        "sources": [
            "National Oceanic and Atmospheric Administration (NOAA), 'Can humans drink seawater?'",
            "Wilderness Medical Society"
        ],
        "lines": [
            { "text": "If you're stranded at sea, drinking ocean water will actually dehydrate you faster.", "caps": "Drinking ocean *water | dehydrates you *faster | than *nothing" },
            { "text": "Here is the terrifying reason why.", "caps": "Here is the | *terrifying *reason | why" },
            { "text": "Ocean water is nearly four times saltier than your human blood.", "caps": "Ocean water is | *4 times *saltier | than your *blood" },
            { "text": "When you swallow it, the heavy salt concentration floods your bloodstream.", "caps": "Heavy *salt floods | your *bloodstream" },
            { "text": "Your kidneys desperately try to flush the excess sodium out through urine,", "caps": "Your *kidneys | try to *flush | the excess *sodium" },
            { "text": "but your kidneys can only produce urine that is less salty than the sea.", "caps": "Kidneys can only *filter | water less *salty | than the *sea" },
            { "text": "So to get rid of that salt, your body pulls water straight out of your cells.", "caps": "Body *pulls water | straight out of | your living *cells" },
            { "text": "Your cells shrink, your organs begin failing,", "caps": "Your cells *shrink | your *organs | begin *failing" },
            { "text": "and extreme dehydration sets in twice as fast.", "caps": "Extreme *dehydration | sets in *twice as *fast", "gap": 0.2 }
        ],
        "metadata": {
            "title": "What Happens If You Drink Sea Water? #shorts",
            "description": "Why does drinking ocean water dehydrate you faster than drinking nothing at all? The biological breakdown of saltwater toxicity. #shorts #survival #science #facts",
            "tags": ["shorts", "survival", "science", "ocean", "biology", "animation"]
        }
    },
    {
        "title": "What Happens If You Hold in a Sneeze?",
        "voice": "am_michael",
        "speed": 1.02,
        "lead": 0.35,
        "outro": 1.0,
        "gap": 0.26,
        "music": "tension",
        "sources": [
            "BMJ Case Reports, 'Snap, crackle and pop: when sneezing leads to complications'",
            "University of Texas Health Science Center"
        ],
        "lines": [
            { "text": "Holding in a violent sneeze can cause shocking damage to your body.", "caps": "Holding in a *sneeze | can cause *shocking | *damage" },
            { "text": "A standard sneeze blasts air out of your nose at up to one hundred miles per hour.", "caps": "Air blasts *out | at up to | *100 miles per *hour" },
            { "text": "When you pinch your nose and clamp your mouth shut,", "caps": "When you *pinch | your nose and *clamp | your mouth *shut" },
            { "text": "all of that explosive pressure has nowhere to go.", "caps": "All of that *pressure | has *nowhere | to *go" },
            { "text": "Instead, the pressure wave redirects backward into your throat and sinuses.", "caps": "Pressure redirects | *backward into | throat and *sinuses" },
            { "text": "The pressure can be up to twenty times higher than a normal sneeze.", "caps": "Pressure spikes | up to *20 times | *higher" },
            { "text": "This sudden force can rupture your eardrums, pop blood vessels in your eyes,", "caps": "Can *rupture eardrums | pop *blood vessels | in your *eyes" },
            { "text": "and in rare cases, even tear a hole in your windpipe.", "caps": "Even tear a *hole | in your *windpipe" },
            { "text": "Doctors strongly recommend: always let the sneeze out.", "caps": "Doctors *warn: | always let the *sneeze | *out", "gap": 0.2 }
        ],
        "metadata": {
            "title": "What Happens If You Hold in a Sneeze? (Dangerous!) #shorts",
            "description": "Never pinch your nose to stop a sneeze. Here's what doctors say about the explosive pressure redirected inside your head. #shorts #health #science #facts",
            "tags": ["shorts", "health", "sneeze", "science", "facts", "animation"]
        }
    }
]


def generate_3d_script(api_key: str = "", past_topics: list = None) -> dict:
    """
    Generates a high-retention 'What happens if...?' 3D explainer script via Gemini API,
    with smart deduplication against past_topics and curated fallback pool.
    """
    past_topics = past_topics or []
    past_topics_str = ", ".join(past_topics[-40:]) if past_topics else "None yet"

    prompt = f"""You are an expert scriptwriter for viral 3D animated shorts in the style of Zack D. Films.
Write a script for a 30 to 40 second vertical explainer short answering a captivating "What happens if...?" question about human anatomy, health, biology, strange medical facts, or extreme survival situations.

CRITICAL DEDUPLICATION RULE:
You MUST choose a completely unique topic.
DO NOT use any of these topics that were ALREADY covered:
{past_topics_str}

Format Requirements:
Output ONLY valid JSON matching this schema:
{{
  "title": "What Happens If You [Topic]?",
  "voice": "am_michael",
  "speed": 1.03,
  "lead": 0.35,
  "outro": 1.0,
  "gap": 0.26,
  "music": "tension",
  "sources": [
    "Medical or scientific source 1",
    "Medical or scientific source 2"
  ],
  "lines": [
    {{ "text": "Hook line explaining the premise in natural conversational English.", "caps": "3-5 word *caps | chunked with *asterisks | for *karaoke" }},
    {{ "text": "Second line advancing the story.", "caps": "Line 2 *caps | with *keywords" }},
    ... (between 8 and 11 lines total, tightly paced, ~70-90 words spoken total)
  ],
  "metadata": {{
    "title": "Catchy YouTube Title #shorts",
    "description": "2-sentence high-retention description with tags",
    "tags": ["shorts", "science", "facts", "animation", "health"]
  }}
}}

Make every line punchy, educational, and scientifically accurate.
"""

    if api_key:
        candidate_models = ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash"]
        for model in candidate_models:
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
                payload = json.dumps({
                    "contents": [{"parts": [{"text": prompt}]}],
                    "generationConfig": {
                        "response_mime_type": "application/json",
                        "temperature": 0.8
                    }
                }).encode("utf-8")
                req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"}, method="POST")
                with urllib.request.urlopen(req, timeout=25) as resp:
                    res_data = json.loads(resp.read().decode("utf-8"))
                raw_text = res_data["candidates"][0]["content"]["parts"][0]["text"].strip()
                match = re.search(r"\{.*\}", raw_text, re.DOTALL)
                parsed = json.loads(match.group(0)) if match else json.loads(raw_text)
                if "lines" in parsed and "title" in parsed:
                    print(f"[SUCCESS] Gemini ({model}) generated fresh 3D script: '{parsed.get('title')}'")
                    return parsed
            except Exception as err:
                print(f"[WARN] Gemini model {model} attempt failed: {err}")

    # Fallback to curated pool
    unvisited = [s for s in CURATED_3D_POOL if s["title"] not in past_topics]
    if unvisited:
        chosen = unvisited[0]
        print(f"[POOL] Selected fresh unvisited topic from curated pool: '{chosen['title']}'")
        return chosen

    chosen = random.choice(CURATED_3D_POOL)
    print(f"[POOL] Selected topic from curated pool: '{chosen['title']}'")
    return chosen
