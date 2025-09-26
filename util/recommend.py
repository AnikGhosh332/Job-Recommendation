from sentence_transformers import SentenceTransformer, util

# model = SentenceTransformer("msmarco-distilbert-dot-v5")

def recommend_jobs(model,summary_text,jobs):
    job_texts = []
    for job in jobs:
        job_text = job["about_role"] + " " + " ".join(job["skills_needed"])
        job_texts.append(job_text)

    summary_emb = model.encode(summary_text, convert_to_tensor=True)
    job_embs = model.encode(job_texts, convert_to_tensor=True)

    cosine_scores = util.cos_sim(summary_emb, job_embs)

    # Step 5: Rank jobs with full details
    job_matches = sorted(
        [
            {
                "company": jobs[i]["company_name"],
                "job_description": jobs[i]["about_role"],
                "skills_needed": jobs[i]["skills_needed"],
                "similarity": float(cosine_scores[0][i]),
            }
            for i in range(len(jobs))
        ],
        key=lambda x: x["similarity"],
        reverse=True
    )

    top_n = 4  # change this to any number you want
    top_matches = job_matches[:top_n]

    # Print results
    print("Top job matches:\n")
    for match in top_matches:
        print(f"🏢 {match['company']} (score: {match['similarity']:.3f})")
        print(f"   📌 Role: {match['job_description']}")
        print(f"   🛠 Skills: {', '.join(match['skills_needed'])}")
        print("-" * 80)
    
    return top_matches    
        


def find_skills_and_distribution(model, summary, domains,flag = 'Experience'):
    summary_emb = model.encode(summary, convert_to_tensor=True)

    domain_matches = {}
    domain_scores = {}  # store domain-level scores

    for domain, subs in domains.items():
        # Step 1: Domain similarity
        domain_emb = model.encode(domain, convert_to_tensor=True)
        domain_score = float(util.cos_sim(summary_emb, domain_emb)[0][0])

        if domain_score >= 0.15:  # threshold for domain relevance
            domain_scores[domain] = domain_score  # keep domain-level score

            # Step 2: Sub-skill similarity
            sub_embs = model.encode(subs, convert_to_tensor=True)
            cos_scores = util.cos_sim(summary_emb, sub_embs)[0]

            matched_subs = [
                (subs[i], float(cos_scores[i]))
                for i in range(len(subs))
                if cos_scores[i] >= 0.25
            ]
            matched_subs = sorted(matched_subs, key=lambda x: x[1], reverse=True)

            if matched_subs:
                domain_matches[domain] = matched_subs

    # Step 3: Normalize domain scores to percentages
    total_score = sum(domain_scores.values())
    domain_distribution = {
        domain: (score / total_score) * 100 for domain, score in domain_scores.items()
    }

    # Print results
    print("Matched domains and skills:")
    for domain, subs in domain_matches.items():
        skills = ", ".join([f"{s} ({score:.2f})" for s, score in subs])
        print(f"📌 {domain}: {skills}")

    print(f"\nExperience distribution based on {flag}:")
    for domain, pct in sorted(domain_distribution.items(), key=lambda x: x[1], reverse=True):
        print(f"📊 {domain}: {pct:.1f}%")

    return domain_matches, domain_distribution        