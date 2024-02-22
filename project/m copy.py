ls = {
    11: {
        "name": ["How good is your organization's portfolio process?",
                "What is the level of improvement in your organization's portfolio management planning process?",
                "What is the level of improvement in your organization's Authorize portfolio process?",
                "What does your organization's oversight process look like?",
                "What is the level of improvement in your organization's portfolio management planning process?",],
        "description": ["Define Portfolio Process standards are established.",
                "Optimize Portfolio Process standards are established.",
                "Authorize Portfolio Process standards are established.",
                "Provide Portfolio Oversight Process standards that are established.",
                "Develop Portfolio Management Plan Process standards are established."]
    },
    12: {
        "name": ["How improved is your portfolio communication management plan development process?",
                "What is the level of improvement in your organization's portfolio information management process?",],
        "description": ["Develop Portfolio Communication Management Plan Process standards are established.",
                "Manage Portfolio Information Process standards are established"]
    },
    13: {
        "name": ["How good is your organization's 'Strategic Change Management process?",
                "What is the level of improvement in your organization's 'Strategic Portfolio Planning process?",
                "How has your organization's portfolio charter development process improved?",
                "What is the level of improvement in the process of defining your portfolio roadmap?",],
        "description": ["Manage Strategic Change Process standards are established.",
                "Develop Portfolio Strategic Plan Process standards are established.",
                "Develop Portfolio Charter Process standards are established.",
                "Define Portfolio Roadmap Process standards are established"]
    },
    14: {
        "name": ["What does your organization's process for developing a portfolio risk management plan look like?",
                "What does your organization’s Portfolio Risk Management process look like?",],
        "description": ["Develop Portfolio Risk Management Plan Process standards are established.",
                "Manage Portfolio Risks Process standards are established."]
    },
    15: {
        "name": ["What is the level of improvement in your organization's portfolio performance management planning process?",
                "What is the level of improvement in your organization's supply and demand management process?",
                "At what level is the Portfolio Value Management process in your organization?",],
        "description": ["Develop Portfolio Performance Management Plan Process standards are established.",
                "Manage Supply and Demand Process standards are established.",
                "Manage Portfolio Value Process standards are established."]
    }
}
ka = [11, 12, 13, 14, 15]

combined = []

for category in ka:
    dsl = ["standardize", "measure", "control", "improve"]
    for idx, name in enumerate(ls[category]["name"]):
        # Ensuring the lengths of names and descriptions are the same
        min_length = min(len(ls[category]["name"]), len(ls[category]["description"]))
        if idx < min_length:
            for stage in dsl:
                combined.append({
                    "name": ls[category]["name"][idx],
                    "description": ls[category]["description"][idx],
                    "domain": "program",
                    "stage": stage,
                    "knowledge_area": category
                })

print(len(combined))
