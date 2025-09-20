"""
Knowledge base for parenting advice based on professional literature
for children aged 0-3 years old.
"""

PARENTING_KNOWLEDGE = {
    "crying": {
        "0-3_months": {
            "common_causes": [
                "Hunger - check if it's been 2-3 hours since last feeding",
                "Dirty diaper - check and change if needed",
                "Sleepiness - try swaddling and gentle rocking",
                "Overstimulation - move to quiet, dimly lit room",
                "Gas/colic - try bicycle legs or gentle tummy massage"
            ],
            "response_steps": [
                "1. Check basic needs first (hunger, diaper, sleep)",
                "2. Try the 5 S's: Swaddle, Side/Stomach position, Shush, Swing, Suck",
                "3. If crying persists for more than 2 hours, contact pediatrician",
                "4. Never shake the baby - this can cause serious brain injury"
            ],
            "when_to_worry": [
                "Crying for more than 3 hours continuously",
                "High-pitched or unusual cry",
                "Crying with fever, vomiting, or other symptoms",
                "Baby seems lethargic or unresponsive"
            ]
        },
        "3-6_months": {
            "common_causes": [
                "Teething - look for drooling, chewing, swollen gums",
                "Separation anxiety - baby recognizes primary caregivers",
                "Sleep regression - growth spurts affect sleep patterns",
                "Overstimulation - too much activity or new experiences"
            ],
            "response_steps": [
                "1. Check for teething signs and offer cold teething ring",
                "2. Provide comfort and reassurance with gentle voice",
                "3. Maintain consistent routines for sleep and feeding",
                "4. Try gentle distraction with toys or music"
            ]
        },
        "6-12_months": {
            "common_causes": [
                "Stranger anxiety - fear of unfamiliar people",
                "Frustration with motor skills - wanting to crawl/walk",
                "Teething continues - molars coming in",
                "Sleep changes - transitioning to fewer naps"
            ],
            "response_steps": [
                "1. Acknowledge feelings and provide comfort",
                "2. Help with motor skill practice safely",
                "3. Maintain consistent bedtime routine",
                "4. Introduce new people gradually"
            ]
        },
        "1-3_years": {
            "common_causes": [
                "Tantrums - normal part of emotional development",
                "Frustration with communication - limited vocabulary",
                "Testing boundaries - normal part of development",
                "Changes in routine - moving, new sibling, etc."
            ],
            "response_steps": [
                "1. Stay calm and don't give in to tantrums",
                "2. Use simple language to acknowledge feelings",
                "3. Offer choices when possible to give sense of control",
                "4. Use time-outs sparingly and appropriately"
            ]
        }
    },
    
    "medical_checkups": {
        "0-3_months": {
            "schedule": [
                "Newborn visit: 3-5 days after birth",
                "1 month: Weight, length, head circumference check",
                "2 months: First vaccines (DTaP, Hib, PCV13, Polio, Rotavirus)",
                "4 months: Second round of vaccines"
            ],
            "what_to_expect": [
                "Physical examination and measurements",
                "Developmental milestone assessment",
                "Feeding and sleep pattern discussion",
                "Safety and injury prevention guidance"
            ]
        },
        "3-6_months": {
            "schedule": [
                "6 months: Third round of vaccines",
                "9 months: Developmental assessment"
            ],
            "what_to_expect": [
                "Growth tracking and percentile assessment",
                "Motor skill development evaluation",
                "Feeding transition guidance (introducing solids)",
                "Sleep training recommendations if needed"
            ]
        },
        "6-12_months": {
            "schedule": [
                "12 months: MMR, Varicella, Hepatitis A vaccines",
                "15 months: Fourth DTaP, Hib, PCV13 vaccines"
            ],
            "what_to_expect": [
                "Language development assessment",
                "Social and emotional development check",
                "Safety proofing home guidance",
                "Nutrition and feeding advice"
            ]
        },
        "1-3_years": {
            "schedule": [
                "18 months: Developmental screening",
                "24 months: 2-year checkup",
                "30 months: Developmental screening",
                "36 months: 3-year checkup"
            ],
            "what_to_expect": [
                "Comprehensive developmental assessment",
                "Behavioral and social development evaluation",
                "Potty training readiness assessment",
                "Preschool readiness evaluation"
            ]
        }
    },
    
    "age_appropriate_activities": {
        "0-3_months": {
            "motor_skills": [
                "Tummy time - 3-5 minutes, 2-3 times daily",
                "Gentle massage and touch",
                "Tracking objects with eyes",
                "Holding head up briefly during tummy time"
            ],
            "cognitive_development": [
                "High contrast black and white images",
                "Soft music and lullabies",
                "Gentle talking and singing",
                "Mirror play (safe, unbreakable mirrors)"
            ],
            "social_emotional": [
                "Skin-to-skin contact",
                "Responding to baby's cues promptly",
                "Gentle eye contact and smiling",
                "Consistent caregiving routines"
            ]
        },
        "3-6_months": {
            "motor_skills": [
                "Reaching for and grasping toys",
                "Rolling over (both directions)",
                "Sitting with support",
                "Pushing up on arms during tummy time"
            ],
            "cognitive_development": [
                "Cause and effect toys (rattles, musical toys)",
                "Peek-a-boo games",
                "Reading board books with simple pictures",
                "Exploring different textures"
            ],
            "social_emotional": [
                "Interactive games and songs",
                "Responding to name",
                "Showing preferences for familiar people",
                "Beginning to show stranger anxiety"
            ]
        },
        "6-12_months": {
            "motor_skills": [
                "Crawling and creeping",
                "Pulling up to standing",
                "Cruising along furniture",
                "Pincer grasp development"
            ],
            "cognitive_development": [
                "Object permanence games (hide and seek)",
                "Stacking and nesting toys",
                "Simple puzzles with large pieces",
                "Musical instruments and cause-effect toys"
            ],
            "social_emotional": [
                "Parallel play with other children",
                "Imitating adult actions",
                "Showing affection to caregivers",
                "Beginning to understand 'no'"
            ]
        },
        "1-3_years": {
            "motor_skills": [
                "Walking independently",
                "Running and climbing",
                "Kicking and throwing balls",
                "Fine motor activities (coloring, building blocks)"
            ],
            "cognitive_development": [
                "Shape sorters and simple puzzles",
                "Pretend play and imagination",
                "Learning colors, numbers, and letters",
                "Following simple 2-step instructions"
            ],
            "social_emotional": [
                "Parallel and beginning cooperative play",
                "Sharing and taking turns (with guidance)",
                "Expressing emotions verbally",
                "Developing independence and self-help skills"
            ]
        }
    }
}

def get_knowledge_for_age_group(age_group, topic):
    """Get specific knowledge for an age group and topic."""
    if topic in PARENTING_KNOWLEDGE and age_group in PARENTING_KNOWLEDGE[topic]:
        return PARENTING_KNOWLEDGE[topic][age_group]
    return None

def get_all_topics():
    """Get all available topics in the knowledge base."""
    return list(PARENTING_KNOWLEDGE.keys())

def get_age_groups_for_topic(topic):
    """Get all age groups available for a specific topic."""
    if topic in PARENTING_KNOWLEDGE:
        return list(PARENTING_KNOWLEDGE[topic].keys())
    return []
