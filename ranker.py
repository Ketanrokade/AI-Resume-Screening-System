import pandas as pd
import pandas as pd

def recommendation(score):
    if score >= 80:
        return "🟢 Highly Recommended"
    elif score >= 60:
        return "🟡 Recommended"
    elif score >= 40:
        return "🟠 Consider"
    else:
        return "🔴 Not Recommended"

def rank_candidates(names, scores, matched_skills_list, missing_skills_list, threshold=0.0):
    rows = []
    for i, (name, score) in enumerate(zip(names, scores)):
        if score >= threshold:
            matched = matched_skills_list[i]
            missing = missing_skills_list[i]
            match_score = round(score * 100, 1)
            rows.append({
            "Rank": 0,
            "Candidate": name,
            "Match Score (%)": match_score,
            "Recommendation": recommendation(match_score),
            "Matched Skills": ", ".join(matched) if matched else "—",
            "Missing Skills": ", ".join(missing) if missing else "None ✅",
            "Matched Count": len(matched),
            "Missing Count": len(missing),
            })

    df = pd.DataFrame(rows)
    if df.empty:
        return df

    df = df.sort_values(
        by=["Match Score (%)", "Matched Count"],
        ascending=[False, False]
    ).reset_index(drop=True)

    df["Rank"] = df.index + 1
    df = df[[
    "Rank",
    "Candidate",
    "Match Score (%)",
    "Recommendation",
    "Matched Skills",
    "Missing Skills"
]]
    return df

def get_shortlist(df, top_n=5):
    return df.head(top_n)