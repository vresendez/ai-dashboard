# 🇳🇱 Discussion of AI in Dutch Party Programs (2023–2025)
[![Streamlit](https://img.shields.io/badge/Made%20with-Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

This repository hosts the interactive dashboard **“Politicization of AI in Dutch Party Programs (2023–2025)”**, expanding upon the findings from:

> **Morosoli, S., Kieslich, K., Reséndez, V., & van Drunen, M. (2025).**  
> *AI governance in the spotlight: an empirical analysis of Dutch political parties’ strategies for the 2023 elections.*  
> *Journal of Information Technology & Politics.* https://doi.org/10.1080/19331681.2025.2504519  

This repository hosts a dashboard analyzing how related terms to **Artificial Intelligence (AI)** are discussed in **Dutch political party manifestos** between **2023 and 2025**, highlighting shifts in **the prominance and the type of discussions**.

It builds on the study by **Morosoli et al. (2025)** and extends it with:
- Additional party manifestos (2025).
- Additional categories of the discussion (e.g., Security).
- Comparison between **Governing (2025 Coalition)** and **Other** parties.

---

## Dashboard overview

| Section | Description |
|----------|-------------|
| **Prominance of AI discussion** | Tracks how often parties mention AI in 2023 vs. 2025 (normalized by 10,000 words). |
| **Ways AI is discussed** | Shows how the discussion of AI evolves across Policy, Ethical, and Societal dimensions. |
| **Example Statements** | Displays translated sample sentences for each dimension and party. |
| **Summary Stats** | Highlights overall change (Δ) in AI attention between 2023 → 2025. |

---

## Data sources

- **Party Programs (2023–2025):** Official political manifestos in Dutch.
- **Sentence-level annotation:** Automated classification of *sentiment* (Risk vs. Benefit) and *dimension* (Policy, Ethics, Society, Economy, Security, Labour).
- **Word counts:** Used to normalize AI salience per 10,000 words.

## Citation