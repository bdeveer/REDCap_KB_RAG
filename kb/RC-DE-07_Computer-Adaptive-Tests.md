RC-DE-07

**Data Entry — Computer Adaptive Tests (CAT)**

| **Article ID** | RC-DE-07 |
|---|---|
| **Domain** | Data Entry |
| **Applies To** | Projects containing CAT instruments; data entry users and survey respondents |
| **Prerequisite** | RC-DE-02 — Basic Data Entry |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | REDCap Support |
| **Related Topics** | RC-DE-02 — Basic Data Entry; RC-SURV-01 — Surveys: Basics |

---

# 1. Overview

This article explains Computer Adaptive Tests (CATs) in REDCap — what they are, how they behave during data entry, and what to expect from them. CATs are a special class of validated measurement instruments that dynamically adjust which questions are displayed based on the answers given. From the perspective of a data entry user or survey respondent, the most important practical difference from a standard instrument is that a CAT will present a different set of questions on every administration. This is by design and is not an error.

---

# 2. Key Concepts & Definitions

**Computer Adaptive Test (CAT)**

A validated psychometric instrument that selects and presents questions dynamically based on the respondent's previous answers. The algorithm identifies the most informative next question given current responses, allowing the instrument to estimate a score accurately with fewer total questions than a fixed-length form.

**PROMIS (Patient-Reported Outcomes Measurement Information System)**

A widely used framework for patient-reported outcome measures developed by the NIH. Many of the CAT instruments available in REDCap are from the PROMIS library, including measures of physical function, fatigue, pain, and emotional health.

**Adaptive Algorithm**

The scoring and question-selection logic that runs behind the scenes during a CAT administration. As each answer is recorded, the algorithm selects the next most informative question from the item bank. Data entry users do not interact with the algorithm directly — it operates automatically.

**Item Bank**

The full pool of questions from which the adaptive algorithm draws during a CAT administration. A respondent typically sees only a subset of the item bank in any given session.

---

# 3. What to Expect During Data Entry with a CAT Instrument

### 3.1 Variable Question Sets

Unlike a standard instrument, which presents the same questions in the same order every time, a CAT presents a personalized subset of questions determined in real time by the respondent's answers. As a result:

- The number of questions presented may differ across administrations for the same participant.
- The specific questions displayed may differ across administrations.
- Two different participants filling out the same instrument on the same day may see entirely different question sets.

This variability is intentional and is how the instrument achieves measurement efficiency. It is not an error, a display problem, or a sign that something has gone wrong.

### 3.2 Entering Data into a CAT

The interaction model for answering CAT questions is the same as for any REDCap radio button or dropdown field. Select the response that best applies, and the next question will appear automatically. Continue until the instrument signals completion.

> **Important:** Do not attempt to navigate backwards through a CAT instrument to change earlier answers. The adaptive algorithm has already used each answer to determine subsequent questions — changing an earlier response after the fact may produce inconsistent or invalid data.

### 3.3 Completion

The CAT instrument determines when enough information has been gathered to produce a reliable score. It will signal completion automatically. You do not need to answer every question in the item bank — only the questions the algorithm presents.

---

# 4. Common Questions

**Q: The CAT instrument showed my participant different questions than it showed a previous participant. Is something broken?**

**A:** No. CAT instruments are designed to present different question sets to different respondents. The adaptive algorithm selects questions based on each individual's answers, so no two administrations are identical. This is the mechanism that makes the instrument efficient.

**Q: The CAT showed fewer questions today than it did last time for the same participant. Is that normal?**

**A:** Yes. The number of questions presented in a CAT administration varies depending on how the algorithm estimates the respondent's score as questions are answered. Fewer questions may be needed when responses are consistent and the algorithm reaches a reliable estimate quickly.

**Q: Can I go back and change an answer during a CAT administration?**

**A:** This should be avoided. Each answer influences the algorithm's selection of subsequent questions. Changing an earlier response after the algorithm has already adapted to it can produce an inconsistent dataset. If a correction is genuinely necessary, contact your project manager before modifying any records.

**Q: What is PROMIS and why does the CAT reference it?**

**A:** PROMIS (Patient-Reported Outcomes Measurement Information System) is a collection of validated patient-reported outcome measures developed by the NIH. Many REDCap CAT instruments, including the ASCQ-Me and various physical and emotional health measures, are drawn from the PROMIS library.

**Q: Does a CAT instrument require an internet connection to function?**

**A:** Yes. CAT instruments rely on real-time communication with an external scoring server to run the adaptive algorithm. If the connection to that server is unavailable, the instrument will not function properly. Verify connectivity before beginning a data entry session that includes a CAT.

---

# 5. Common Mistakes & Gotchas

**Assuming something is wrong when the question set changes.** Staff unfamiliar with CATs sometimes report a "bug" when they notice different questions across administrations. This is expected behavior, not an error. Brief all data entry staff about CAT behavior before project launch.

**Navigating backwards to change answers.** The adaptive algorithm uses each answer to determine the next question. Changing a previous answer after the algorithm has already adapted invalidates the assumption behind subsequent question selection. If a participant answers incorrectly, note the issue in the field comment log and consult your project manager.

**Attempting to complete a CAT without a reliable internet connection.** CAT instruments communicate with an external server in real time. Offline or restricted-network environments will prevent the instrument from loading or functioning. Always confirm connectivity before beginning a CAT administration.

---

# 6. Related Articles

- RC-DE-02 — Basic Data Entry (foundational data entry skills)
- RC-SURV-01 — Surveys: Basics (relevant if the CAT instrument is administered as a participant-facing survey)
- RC-DE-08 — Field Comment Log (how to document issues encountered during a CAT administration)
