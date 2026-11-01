# Technical Note

## Architecture
Static front-end + engine (JS) mirrored by a Python engine for evaluation. Pipeline: **Analysis** (extract signals and tokens from the reference) → **Discovery** (score every candidate in the pool; candidates with no school-ecosystem signal are down-weighted ×0.25) → **Ranking** → **Explanations**.

## Data retrieval
Authorised data only. This MVP uses a labelled synthetic dataset because direct LinkedIn access is not permitted without authorisation. Compliant production paths: (1) LinkedIn Talent/Sales Navigator or Marketing APIs under a partner agreement, (2) licensed data vendors (e.g. People Data Labs, Proxycurl-style providers with lawful sourcing), (3) the client’s own CRM and opted-in/consented lists, (4) public school-association member directories and conference speaker lists. Store source and retrieval date per record for traceability.

## AI/ML method
1. **Concept normalisation:** synonyms are collapsed (headmaster/headteacher→principal, adviser→advisor, founder/promoter→owner) and concept tokens (K-12, advisory, leadership, multi-school, decision-maker) are appended, so matches do not depend on exact keywords. Phrases such as "business school" or "school of law" are stripped so academia is not mistaken for K-12.
2. **Similarity:** TF-IDF vectors (sublinear tf, smoothed idf) over headline, role, organisation, summary and experience; cosine similarity to the reference, normalised by the top score.
3. **Ecosystem signals:** advisory/consulting (0.30), works across multiple schools (0.30; ≥3 schools or network/chain/cluster language), school leadership background (0.25), engages decision-makers (0.15).
4. **Score:** `gate × (0.5 × similarity + 0.5 × signals) × 100`, gate = 1 if any K-12 signal else 0.25.
5. **Explanations** are generated from the exact signals and shared terms that drove the score, so they are traceable rather than free-form.

## Results (synthetic test set)
75 candidates (40 relevant, 35 distractors including classroom teachers, business-school lecturers and corporate trainers). For the test reference the top 25 are all relevant; precision@20 = 1.00, and mean precision@20 over 40 leave-one-out relevant references = 1.00. **Caveat:** the dataset is synthetic and generated from the same concept families the signals use, so this number demonstrates the pipeline works, not real-world accuracy.

## Limitations
Hand-weighted signals and lexical TF-IDF; no real LinkedIn data; English only; no network-graph (mutual connections) signal; evaluation is on synthetic labels.

## Next steps
Replace TF-IDF with sentence embeddings (e.g. a multilingual encoder) plus a vector index; learn signal weights from outreach feedback (learning-to-rank); add an LLM re-ranker/explainer for top-50; add graph features from licensed connection data; deduplication and consent management.
