# Prior Authorization RAG — Requirement Review

Generated: 2026-10-11T00:05:53.693294+00:00
Embedding model: ethanteh/bge-finetuned-insurance-matryoshka
Retrieval: contextual V2, top 5 active chunks per payer

## Review instructions

For each query, verify against the original policy:

- [ ] Correct medication and indication
- [ ] Correct authorization pathway
- [ ] All mandatory requirements are present
- [ ] Nested AND/OR conditions are preserved
- [ ] No incorrect or historical requirements included

Do not treat an unchecked item as passed.
This report is a review worksheet, not a clinical accuracy score.


---

## AETNA-01

**Payer:** aetna

**Query:** Wegovy adult chronic weight management initial authorization BMI 35 and six month lifestyle program

**Expected pathway metadata:** `{"section": "COVERAGE CRITERIA", "indication_contains": "Chronic Weight Management (Adult)"}`

### Mandatory requirements — manual ground truth

- [ ] Review original policy and list every required condition here

### Retrieval review

- [ ] Correct pathway retrieved
- [ ] All mandatory conditions covered
- [ ] AND/OR logic preserved

### Rank 1 — Distance 0.6890

- Section: COVERAGE CRITERIA
- Medication: 
- Indication: Chronic Weight Management (Adult)
- Pathway: 

**Original policy text:**

```text
Chronic Weight Management (Adult)
Authorization may be granted when the requested drug will be used with a reduced
calorie diet and increased physical activity for chronic weight management when ALL of
the following criteria are met:
     •   The patient is 18 years of age or older
     •   The patient has participated in a comprehensive weight management program that
6/4/26, 8:17 PM
Weight Loss (BMI 35) GIP-GLP-1 GLP-1 Agonists PA with Limit 6450-C UDR 05-2024 - Pharmacy Clinical Policy Bulletins Aetna Non-Medicar…
https://www.aetna.com/products/rxnonmedicare/data/2024/Weight_Loss_(BMI 35)_GIP-GLP-1_GLP-1_Agonists_PA_with_Limit_6450-C_UDR_05-2024.html
2/8
encourages
          behavioral modification, reduced calorie diet, and increased physical activity with
continuing
          follow-up for at least 6 months prior to using drug therapy
     •   The patient has a baseline body mass index (BMI) greater than or equal to 35
kg/m2 [ACTION
          REQUIRED: Documentation is required for approval.]
```

### Rank 2 — Distance 0.7189

- Section: CONTINUATION OF THERAPY
- Medication: 
- Indication: Chronic Weight Management (Adult)
- Pathway: 

**Original policy text:**

```text
Chronic Weight Management (Adult)
Authorization may be granted when the requested drug will be used with a reduced
calorie diet and increased physical activity for chronic weight management when ALL of
the following criteria are met:
     •   The patient is 18 years of age or older
     •   The patient had a baseline body mass index (BMI) greater than or equal to 35
kg/m2 at the
          start of drug therapy for weight loss [ACTION REQUIRED: Documentation is
required for
          approval.]
     •   If the request is for Saxenda (liraglutide), then ALL of the following criteria are met:
               °   The patient has completed at least 16 weeks of therapy with the requested
drug
               °   The patient has lost at least 4 percent of baseline body weight OR the patient
has
                    continued to maintain their initial 4 percent weight loss [ACTION REQUIRED:
                    Documentation is required for approval.]
     •   If the request is for Wegovy (semaglutide), then ALL of the following criteria are met:
               °   The patient has completed at least 3 months of therapy with the requested
drug at a
                    stable maintenance dose
               °   The patient has lost at least 5 percent of baseline body weight OR the patient
has
                    continued to maintain their initial 5 percent weight loss [ACTION REQUIRED:
                    Documentation is required for approval.]
```

### Rank 3 — Distance 0.8206

- Section: COVERAGE CRITERIA
- Medication: 
- Indication: Chronic Weight Management (Pediatric) – Saxenda and Wegovy ONLY
- Pathway: 

**Original policy text:**

```text
Chronic Weight Management (Pediatric) – Saxenda and Wegovy ONLY
Authorization may be granted when the requested drug will be used with a reduced
calorie diet and increased physical activity for chronic weight management when ALL of
the following criteria are met:
     •   The patient is 12 to 17 years of age
     •   The patient has participated in a comprehensive weight management program that
encourages
          behavioral modification, reduced calorie diet, and increased physical activity with
continuing
          follow-up for at least 6 months prior to using drug therapy
     •    If the request is for Saxenda (liraglutide), then ALL of the following criteria are met:
          °   The patient has a body weight above 60 kg [ACTION REQUIRED:
Documentation is
               required for approval.]
          °   The patient has a baseline body mass index (BMI) corresponding to 30 kg/m2 or
greater for
               adults by international cut-off points based on the Cole Criteria [ACTION
REQUIRED: 
               Documentation is required for approval.]
     •   If the request is for Wegovy (semaglutide), then the following criteria is met:
          °   The patient has a baseline BMI in the 95th percentile or greater standardized for
age and
               sex (obesity) [ACTION REQUIRED: Documentation is required for approval.]
```

### Rank 4 — Distance 0.8643

- Section: CONTINUATION OF THERAPY
- Medication: 
- Indication: Chronic Weight Management (Pediatric) – Saxenda and Wegovy ONLY
- Pathway: 

**Original policy text:**

```text
patient has
                    continued to maintain their initial 1 percent reduction in BMI from baseline
[ACTION
                    REQUIRED: Documentation is required for approval.]
     •   If the request is for Wegovy (semaglutide), then ALL of the following criteria are met:
               °   The patient had a baseline BMI in the 95th percentile or greater standardized
for age and
                    sex (obesity) at the start of drug therapy for weight loss [ACTION
REQUIRED:
                    Documentation is required for approval.]
               °   The request is for continuation of therapy for a patient that has successfully
titrated to a
                    stable maintenance dose
               °   The patient has had a reduction from their baseline BMI OR the patient has
continued to
                    maintain their reduction in BMI from baseline [ACTION REQUIRED:
Documentation is
                    required for approval.]
```

### Rank 5 — Distance 0.8945

- Section: CONTINUATION OF THERAPY
- Medication: 
- Indication: Chronic Weight Management (Pediatric) – Saxenda and Wegovy ONLY
- Pathway: 

**Original policy text:**

```text
Chronic Weight Management (Pediatric) – Saxenda and Wegovy ONLY
Authorization may be granted when the requested drug will be used with a reduced
6/4/26, 8:17 PM
Weight Loss (BMI 35) GIP-GLP-1 GLP-1 Agonists PA with Limit 6450-C UDR 05-2024 - Pharmacy Clinical Policy Bulletins Aetna Non-Medicar…
https://www.aetna.com/products/rxnonmedicare/data/2024/Weight_Loss_(BMI 35)_GIP-GLP-1_GLP-1_Agonists_PA_with_Limit_6450-C_UDR_05-2024.html
4/8
calorie diet and increased physical activity for chronic weight management when ALL of
the following criteria are met:
     •   The patient is 12 to 17 years of age
     •   If the request is for Saxenda (liraglutide), then ALL of the following criteria are met:
               °   The patient had a baseline body mass index (BMI) corresponding to 30 kg/m2
or greater
                    for adults by international cut-off points based on the Cole Criteria at the start
of drug
                    therapy for weight loss [ACTION REQUIRED: Documentation is required for
approval.]
               °   The patient has completed at least 12 weeks of therapy on the maintenance
dose with
                    the requested drug
               °   The patient has had at least 1 percent reduction in BMI from baseline OR the
patient has
                    continued to maintain their initial 1 percent reduction in BMI from baseline
[ACTION
                    REQUIRED: Documentation is required for approval.]
```


---

## AETNA-02

**Payer:** aetna

**Query:** Aetna Wegovy adult continuation of therapy requirements

**Expected pathway metadata:** `{"section": "CONTINUATION OF THERAPY", "indication_contains": "Chronic Weight Management (Adult)"}`

### Mandatory requirements — manual ground truth

- [ ] Review original policy and list every required condition here

### Retrieval review

- [ ] Correct pathway retrieved
- [ ] All mandatory conditions covered
- [ ] AND/OR logic preserved

### Rank 1 — Distance 0.5415

- Section: CONTINUATION OF THERAPY
- Medication: 
- Indication: Chronic Weight Management (Pediatric) – Saxenda and Wegovy ONLY
- Pathway: 

**Original policy text:**

```text
patient has
                    continued to maintain their initial 1 percent reduction in BMI from baseline
[ACTION
                    REQUIRED: Documentation is required for approval.]
     •   If the request is for Wegovy (semaglutide), then ALL of the following criteria are met:
               °   The patient had a baseline BMI in the 95th percentile or greater standardized
for age and
                    sex (obesity) at the start of drug therapy for weight loss [ACTION
REQUIRED:
                    Documentation is required for approval.]
               °   The request is for continuation of therapy for a patient that has successfully
titrated to a
                    stable maintenance dose
               °   The patient has had a reduction from their baseline BMI OR the patient has
continued to
                    maintain their reduction in BMI from baseline [ACTION REQUIRED:
Documentation is
                    required for approval.]
```

### Rank 2 — Distance 0.6099

- Section: CONTINUATION OF THERAPY
- Medication: 
- Indication: 
- Pathway: 

**Original policy text:**

```text
CONTINUATION OF THERAPY
```

### Rank 3 — Distance 0.6227

- Section: CONTINUATION OF THERAPY
- Medication: 
- Indication: Chronic Weight Management (Adult)
- Pathway: 

**Original policy text:**

```text
Chronic Weight Management (Adult)
Authorization may be granted when the requested drug will be used with a reduced
calorie diet and increased physical activity for chronic weight management when ALL of
the following criteria are met:
     •   The patient is 18 years of age or older
     •   The patient had a baseline body mass index (BMI) greater than or equal to 35
kg/m2 at the
          start of drug therapy for weight loss [ACTION REQUIRED: Documentation is
required for
          approval.]
     •   If the request is for Saxenda (liraglutide), then ALL of the following criteria are met:
               °   The patient has completed at least 16 weeks of therapy with the requested
drug
               °   The patient has lost at least 4 percent of baseline body weight OR the patient
has
                    continued to maintain their initial 4 percent weight loss [ACTION REQUIRED:
                    Documentation is required for approval.]
     •   If the request is for Wegovy (semaglutide), then ALL of the following criteria are met:
               °   The patient has completed at least 3 months of therapy with the requested
drug at a
                    stable maintenance dose
               °   The patient has lost at least 5 percent of baseline body weight OR the patient
has
                    continued to maintain their initial 5 percent weight loss [ACTION REQUIRED:
                    Documentation is required for approval.]
```

### Rank 4 — Distance 0.6570

- Section: CONTINUATION OF THERAPY
- Medication: 
- Indication: Chronic Weight Management (Adult)
- Pathway: 

**Original policy text:**

```text
has
                    continued to maintain their initial 5 percent weight loss [ACTION REQUIRED:
                    Documentation is required for approval.]
     •   If the request is for Zepbound (tirzepatide), then ALL of the following criteria are met:
               °   The patient has completed at least 3 months of therapy with the requested
drug at a
                    stable maintenance dose
               °   The patient has lost at least 5 percent of baseline body weight OR the patient
has
                    continued to maintain their initial 5 percent weight loss [ACTION REQUIRED:
                    Documentation is required for approval.]
```

### Rank 5 — Distance 0.6881

- Section: CONTINUATION OF THERAPY
- Medication: 
- Indication: Chronic Weight Management (Pediatric) – Saxenda and Wegovy ONLY
- Pathway: 

**Original policy text:**

```text
Chronic Weight Management (Pediatric) – Saxenda and Wegovy ONLY
Authorization may be granted when the requested drug will be used with a reduced
6/4/26, 8:17 PM
Weight Loss (BMI 35) GIP-GLP-1 GLP-1 Agonists PA with Limit 6450-C UDR 05-2024 - Pharmacy Clinical Policy Bulletins Aetna Non-Medicar…
https://www.aetna.com/products/rxnonmedicare/data/2024/Weight_Loss_(BMI 35)_GIP-GLP-1_GLP-1_Agonists_PA_with_Limit_6450-C_UDR_05-2024.html
4/8
calorie diet and increased physical activity for chronic weight management when ALL of
the following criteria are met:
     •   The patient is 12 to 17 years of age
     •   If the request is for Saxenda (liraglutide), then ALL of the following criteria are met:
               °   The patient had a baseline body mass index (BMI) corresponding to 30 kg/m2
or greater
                    for adults by international cut-off points based on the Cole Criteria at the start
of drug
                    therapy for weight loss [ACTION REQUIRED: Documentation is required for
approval.]
               °   The patient has completed at least 12 weeks of therapy on the maintenance
dose with
                    the requested drug
               °   The patient has had at least 1 percent reduction in BMI from baseline OR the
patient has
                    continued to maintain their initial 1 percent reduction in BMI from baseline
[ACTION
                    REQUIRED: Documentation is required for approval.]
```


---

## AETNA-03

**Payer:** aetna

**Query:** Aetna Wegovy pediatric initial authorization age 12 to 17 and BMI eligibility

**Expected pathway metadata:** `{"section": "COVERAGE CRITERIA", "indication_contains": "Chronic Weight Management (Pediatric)"}`

### Mandatory requirements — manual ground truth

- [ ] Review original policy and list every required condition here

### Retrieval review

- [ ] Correct pathway retrieved
- [ ] All mandatory conditions covered
- [ ] AND/OR logic preserved

### Rank 1 — Distance 0.6400

- Section: COVERAGE CRITERIA
- Medication: 
- Indication: Chronic Weight Management (Pediatric) – Saxenda and Wegovy ONLY
- Pathway: 

**Original policy text:**

```text
Chronic Weight Management (Pediatric) – Saxenda and Wegovy ONLY
Authorization may be granted when the requested drug will be used with a reduced
calorie diet and increased physical activity for chronic weight management when ALL of
the following criteria are met:
     •   The patient is 12 to 17 years of age
     •   The patient has participated in a comprehensive weight management program that
encourages
          behavioral modification, reduced calorie diet, and increased physical activity with
continuing
          follow-up for at least 6 months prior to using drug therapy
     •    If the request is for Saxenda (liraglutide), then ALL of the following criteria are met:
          °   The patient has a body weight above 60 kg [ACTION REQUIRED:
Documentation is
               required for approval.]
          °   The patient has a baseline body mass index (BMI) corresponding to 30 kg/m2 or
greater for
               adults by international cut-off points based on the Cole Criteria [ACTION
REQUIRED: 
               Documentation is required for approval.]
     •   If the request is for Wegovy (semaglutide), then the following criteria is met:
          °   The patient has a baseline BMI in the 95th percentile or greater standardized for
age and
               sex (obesity) [ACTION REQUIRED: Documentation is required for approval.]
```

### Rank 2 — Distance 0.7739

- Section: COVERAGE CRITERIA
- Medication: 
- Indication: Chronic Weight Management (Adult)
- Pathway: 

**Original policy text:**

```text
Chronic Weight Management (Adult)
Authorization may be granted when the requested drug will be used with a reduced
calorie diet and increased physical activity for chronic weight management when ALL of
the following criteria are met:
     •   The patient is 18 years of age or older
     •   The patient has participated in a comprehensive weight management program that
6/4/26, 8:17 PM
Weight Loss (BMI 35) GIP-GLP-1 GLP-1 Agonists PA with Limit 6450-C UDR 05-2024 - Pharmacy Clinical Policy Bulletins Aetna Non-Medicar…
https://www.aetna.com/products/rxnonmedicare/data/2024/Weight_Loss_(BMI 35)_GIP-GLP-1_GLP-1_Agonists_PA_with_Limit_6450-C_UDR_05-2024.html
2/8
encourages
          behavioral modification, reduced calorie diet, and increased physical activity with
continuing
          follow-up for at least 6 months prior to using drug therapy
     •   The patient has a baseline body mass index (BMI) greater than or equal to 35
kg/m2 [ACTION
          REQUIRED: Documentation is required for approval.]
```

### Rank 3 — Distance 0.7850

- Section: CONTINUATION OF THERAPY
- Medication: 
- Indication: Chronic Weight Management (Pediatric) – Saxenda and Wegovy ONLY
- Pathway: 

**Original policy text:**

```text
Chronic Weight Management (Pediatric) – Saxenda and Wegovy ONLY
Authorization may be granted when the requested drug will be used with a reduced
6/4/26, 8:17 PM
Weight Loss (BMI 35) GIP-GLP-1 GLP-1 Agonists PA with Limit 6450-C UDR 05-2024 - Pharmacy Clinical Policy Bulletins Aetna Non-Medicar…
https://www.aetna.com/products/rxnonmedicare/data/2024/Weight_Loss_(BMI 35)_GIP-GLP-1_GLP-1_Agonists_PA_with_Limit_6450-C_UDR_05-2024.html
4/8
calorie diet and increased physical activity for chronic weight management when ALL of
the following criteria are met:
     •   The patient is 12 to 17 years of age
     •   If the request is for Saxenda (liraglutide), then ALL of the following criteria are met:
               °   The patient had a baseline body mass index (BMI) corresponding to 30 kg/m2
or greater
                    for adults by international cut-off points based on the Cole Criteria at the start
of drug
                    therapy for weight loss [ACTION REQUIRED: Documentation is required for
approval.]
               °   The patient has completed at least 12 weeks of therapy on the maintenance
dose with
                    the requested drug
               °   The patient has had at least 1 percent reduction in BMI from baseline OR the
patient has
                    continued to maintain their initial 1 percent reduction in BMI from baseline
[ACTION
                    REQUIRED: Documentation is required for approval.]
```

### Rank 4 — Distance 0.7897

- Section: CONTINUATION OF THERAPY
- Medication: 
- Indication: Chronic Weight Management (Pediatric) – Saxenda and Wegovy ONLY
- Pathway: 

**Original policy text:**

```text
patient has
                    continued to maintain their initial 1 percent reduction in BMI from baseline
[ACTION
                    REQUIRED: Documentation is required for approval.]
     •   If the request is for Wegovy (semaglutide), then ALL of the following criteria are met:
               °   The patient had a baseline BMI in the 95th percentile or greater standardized
for age and
                    sex (obesity) at the start of drug therapy for weight loss [ACTION
REQUIRED:
                    Documentation is required for approval.]
               °   The request is for continuation of therapy for a patient that has successfully
titrated to a
                    stable maintenance dose
               °   The patient has had a reduction from their baseline BMI OR the patient has
continued to
                    maintain their reduction in BMI from baseline [ACTION REQUIRED:
Documentation is
                    required for approval.]
```

### Rank 5 — Distance 0.8820

- Section: COVERAGE CRITERIA
- Medication: 
- Indication: Risk Reduction of Major Adverse Cardiovascular Events (Adult) – Wegovy ONLY
- Pathway: 

**Original policy text:**

```text
Risk Reduction of Major Adverse Cardiovascular Events (Adult) – Wegovy ONLY
Authorization may be granted when the requested drug will be used to reduce the risk of
major adverse cardiovascular events (cardiovascular death, non-fatal myocardial
infarction (MI), or non-fatal stroke) in an adult with established cardiovascular disease
AND either obesity or overweight when ALL of the following criteria are met:
     •   The request is for Wegovy (semaglutide)
     •   The requested drug is being used with a reduced calorie diet and increased physical
activity
     •   The patient has established cardiovascular disease with a history of ONE of the
following:
          previous MI; previous stroke; symptomatic peripheral arterial disease (PAD), as
evidenced by
          intermittent claudication with ankle-brachial index (ABI) less than 0.85 (at rest),
peripheral
          arterial revascularization procedure, or amputation due to atherosclerotic disease;
prior history
          of revascularization (coronary artery bypass grafting (CABG), percutaneous
coronary
          intervention (PCI), or angioplasty) [ACTION REQUIRED: Documentation is required
for
          approval.]
     •   The patient has a baseline body mass index (BMI) greater than or equal to 27
6/4/26, 8:17 PM
Weight Loss (BMI 35) GIP-GLP-1 GLP-1 Agonists PA with Limit 6450-C UDR 05-2024 - Pharmacy Clinical Policy Bulletins Aetna Non-Medicar…
```


---

## CIGNA-01

**Payer:** cigna

**Query:** Cigna Wegovy injection adult weight loss initial therapy BMI and behavioral modification

**Expected pathway metadata:** `{"medication": "Wegovy injection", "indication_contains": "Weight Loss in an Adult", "pathway_contains": "Initial Therapy"}`

### Mandatory requirements — manual ground truth

- [ ] Review original policy and list every required condition here

### Retrieval review

- [ ] Correct pathway retrieved
- [ ] All mandatory conditions covered
- [ ] AND/OR logic preserved

### Rank 1 — Distance 0.4097

- Section: III.
- Medication: Wegovy injection
- Indication: 1. Weight Loss in an Adult with Overweight or Obesity.  Approve for the
- Pathway: A) Initial Therapy.  Approve for 8 months if the patient meets ALL of the

**Original policy text:**

```text
A) Initial Therapy.  Approve for 8 months if the patient meets ALL of the 
following (i, ii, iii, and iv): 
i. Patient is ≥ 18 years of age; AND 
ii. Patient has engaged in a trial of behavioral modification and dietary 
restriction for at least 3 months; AND 
iii. Patient meets ONE of the following (a or b): 
a) At baseline, patient had a BMI ≥ 30 kg/m2; OR 
Note:  This refers to baseline prior to any glucagon-like peptide-1 
(GLP-1) agonist (e.g., liraglutide [Saxenda, generic], Wegovy) or GLP-
1/glucose-dependent insulinotropic polypeptide (GIP) receptor agonist 
(e.g., Zepbound). 
b) Patient meets BOTH of the following [(1) and (2)]: 
(1) 
At baseline, patient had a BMI ≥ 27 kg/m2; AND 
(2) 
At baseline, patient had, or patient currently has, at least ONE 
of the following weight-related comorbidities:  hypertension, type 2 
diabetes, dyslipidemia, obstructive sleep apnea, cardiovascular 
disease, knee osteoarthritis, asthma, chronic obstructive pulmonary 
disease, metabolic dysfunction-associated steatotic liver 
disease/non-alcoholic fatty liver disease, polycystic ovarian 
syndrome, or coronary artery disease; AND 
Note:  This refers to baseline prior to any glucagon-like peptide-1 
(GLP-1) agonist (e.g., liraglutide [Saxenda, generic], Wegovy) or GLP-
1/glucose-dependent insulinotropic polypeptide (GIP) receptor agonist 
(e.g., Zepbound). 
iv. The medication will be used concomitantly with behavioral modification 
and a reduced-calorie diet; OR 
```

### Rank 2 — Distance 0.4182

- Section: III.
- Medication: Wegovy injection
- Indication: 1. Weight Loss in an Adult with Overweight or Obesity.  Approve for the
- Pathway: 

**Original policy text:**

```text
1. Weight Loss in an Adult with Overweight or Obesity.  Approve for the 
duration noted if the patient meets ONE of the following (A or B): 
```

### Rank 3 — Distance 0.4549

- Section: III.
- Medication: Wegovy injection
- Indication: 1. Weight Loss in an Adult with Overweight or Obesity.  Approve for the
- Pathway: B) Patient is Currently Receiving Wegovy injection, Wegovy HD injection, or

**Original policy text:**

```text
B) Patient is Currently Receiving Wegovy injection, Wegovy HD injection, or 
Wegovy tablet.  Approve for 1 year if the patient meets ALL of the following 
(i, ii, iii, and iv): 
Note:  For a patient who has not completed 8 months of initial therapy with 
Wegovy injection, Wegovy HD injection, and/or Wegovy tablet, refer to Initial 
Therapy criteria above. 
i. Patient is ≥ 18 years of age; AND 
ii. Patient meets ONE of the following (a or b): 
a) At baseline, patient had a BMI ≥ 30 kg/m2; OR 
Note:  This refers to baseline prior to any glucagon-like peptide-1 
(GLP-1) agonist (e.g., liraglutide [Saxenda, generic], Wegovy) or GLP-
1/glucose-dependent insulinotropic polypeptide (GIP) receptor agonist 
(e.g., Zepbound). 
33 Pages  - Cigna National Formulary Coverage  - Policy:Weight Loss – Glucagon-Like Peptide-1 Agonists Prior 
Authorization Policy 
 
b) Patient meets BOTH of the following [(1) and (2)]: 
(1) 
At baseline, patient had a BMI ≥ 27 kg/m2; AND 
(2) 
At baseline, patient had, or patient currently has, at least ONE 
of the following weight-related comorbidities:  hypertension, type 2 
diabetes, dyslipidemia, obstructive sleep apnea, cardiovascular 
disease, knee osteoarthritis, asthma, chronic obstructive pulmonary 
disease, metabolic dysfunction-associated steatotic liver 
disease/non-alcoholic fatty liver disease, polycystic ovarian 
syndrome, or coronary artery disease; AND 
Note:  This refers to baseline prior to any glucagon-like peptide-1
```

### Rank 4 — Distance 0.4771

- Section: III.
- Medication: Wegovy injection
- Indication: 1. Weight Loss in an Adult with Overweight or Obesity.  Approve for the
- Pathway: B) Patient is Currently Receiving Wegovy injection, Wegovy HD injection, or

**Original policy text:**

```text
disease/non-alcoholic fatty liver disease, polycystic ovarian 
syndrome, or coronary artery disease; AND 
Note:  This refers to baseline prior to any glucagon-like peptide-1 
(GLP-1) agonist (e.g., liraglutide [Saxenda, generic], Wegovy) or GLP-
1/glucose-dependent insulinotropic polypeptide (GIP) receptor agonist 
(e.g., Zepbound). 
iii. Patient has lost ≥ 5% of baseline body weight; AND 
Note:  This refers to baseline prior to any glucagon-like peptide-1 (GLP-1) 
agonist (e.g., liraglutide [Saxenda, generic], Wegovy) or GLP-1/glucose-
dependent insulinotropic polypeptide (GIP) receptor agonist (e.g., 
Zepbound). 
iv. The medication will be used concomitantly with behavioral modification 
and a reduced-calorie diet.
```

### Rank 5 — Distance 0.5304

- Section: IV.
- Medication: Wegovy tablet
- Indication: 1. Weight Loss in an Adult with Overweight or Obesity.  Approve for the
- Pathway: A) Initial Therapy.  Approve for 8 months if the patient meets ALL of the

**Original policy text:**

```text
A) Initial Therapy.  Approve for 8 months if the patient meets ALL of the 
following (i, ii, iii, and iv): 
i. Patient is ≥ 18 years of age; AND 
ii. Patient has engaged in a trial of behavioral modification and dietary 
restriction for at least 3 months; AND 
iii. Patient meets ONE of the following (a or b): 
a) At baseline, patient had a BMI ≥ 30 kg/m2; OR 
Note:  This refers to baseline prior to any glucagon-like peptide-1 (GLP-1) 
agonist (e.g., liraglutide [Saxenda, generic], Wegovy) or GLP-1/glucose-
dependent insulinotropic polypeptide (GIP) receptor agonist (e.g., 
Zepbound). 
c) Patient meets BOTH of the following [(1) and (2)]: 
(1) 
At baseline, patient had a BMI ≥ 27 kg/m2; AND 
(2) 
At baseline, patient had, or patient currently has, at least ONE 
of the following weight-related comorbidities:  hypertension, type 2 
diabetes, dyslipidemia, obstructive sleep apnea, cardiovascular 
disease, knee osteoarthritis, asthma, chronic obstructive pulmonary 
disease, metabolic dysfunction-associated steatotic liver 
disease/non-alcoholic fatty liver disease, polycystic ovarian 
syndrome, or coronary artery disease; AND 
Note:  This refers to baseline prior to any glucagon-like peptide-1 
(GLP-1) agonist (e.g., liraglutide [Saxenda, generic], Wegovy) or GLP-
1/glucose-dependent insulinotropic polypeptide (GIP) receptor agonist 
(e.g., Zepbound). 
33 Pages  - Cigna National Formulary Coverage  - Policy:Weight Loss – Glucagon-Like Peptide-1 Agonists Prior
```


---

## CIGNA-02

**Payer:** cigna

**Query:** Cigna Wegovy injection adult weight loss continuation therapy requirements

**Expected pathway metadata:** `{"medication": "Wegovy injection", "indication_contains": "Weight Loss in an Adult", "pathway_contains": "Patient is Currently Receiving"}`

### Mandatory requirements — manual ground truth

- [ ] Review original policy and list every required condition here

### Retrieval review

- [ ] Correct pathway retrieved
- [ ] All mandatory conditions covered
- [ ] AND/OR logic preserved

### Rank 1 — Distance 0.4107

- Section: III.
- Medication: Wegovy injection
- Indication: 1. Weight Loss in an Adult with Overweight or Obesity.  Approve for the
- Pathway: 

**Original policy text:**

```text
1. Weight Loss in an Adult with Overweight or Obesity.  Approve for the 
duration noted if the patient meets ONE of the following (A or B): 
```

### Rank 2 — Distance 0.4245

- Section: III.
- Medication: Wegovy injection
- Indication: 1. Weight Loss in an Adult with Overweight or Obesity.  Approve for the
- Pathway: A) Initial Therapy.  Approve for 8 months if the patient meets ALL of the

**Original policy text:**

```text
A) Initial Therapy.  Approve for 8 months if the patient meets ALL of the 
following (i, ii, iii, and iv): 
i. Patient is ≥ 18 years of age; AND 
ii. Patient has engaged in a trial of behavioral modification and dietary 
restriction for at least 3 months; AND 
iii. Patient meets ONE of the following (a or b): 
a) At baseline, patient had a BMI ≥ 30 kg/m2; OR 
Note:  This refers to baseline prior to any glucagon-like peptide-1 
(GLP-1) agonist (e.g., liraglutide [Saxenda, generic], Wegovy) or GLP-
1/glucose-dependent insulinotropic polypeptide (GIP) receptor agonist 
(e.g., Zepbound). 
b) Patient meets BOTH of the following [(1) and (2)]: 
(1) 
At baseline, patient had a BMI ≥ 27 kg/m2; AND 
(2) 
At baseline, patient had, or patient currently has, at least ONE 
of the following weight-related comorbidities:  hypertension, type 2 
diabetes, dyslipidemia, obstructive sleep apnea, cardiovascular 
disease, knee osteoarthritis, asthma, chronic obstructive pulmonary 
disease, metabolic dysfunction-associated steatotic liver 
disease/non-alcoholic fatty liver disease, polycystic ovarian 
syndrome, or coronary artery disease; AND 
Note:  This refers to baseline prior to any glucagon-like peptide-1 
(GLP-1) agonist (e.g., liraglutide [Saxenda, generic], Wegovy) or GLP-
1/glucose-dependent insulinotropic polypeptide (GIP) receptor agonist 
(e.g., Zepbound). 
iv. The medication will be used concomitantly with behavioral modification 
and a reduced-calorie diet; OR 
```

### Rank 3 — Distance 0.4535

- Section: III.
- Medication: Wegovy injection
- Indication: 1. Weight Loss in an Adult with Overweight or Obesity.  Approve for the
- Pathway: B) Patient is Currently Receiving Wegovy injection, Wegovy HD injection, or

**Original policy text:**

```text
B) Patient is Currently Receiving Wegovy injection, Wegovy HD injection, or 
Wegovy tablet.  Approve for 1 year if the patient meets ALL of the following 
(i, ii, iii, and iv): 
Note:  For a patient who has not completed 8 months of initial therapy with 
Wegovy injection, Wegovy HD injection, and/or Wegovy tablet, refer to Initial 
Therapy criteria above. 
i. Patient is ≥ 18 years of age; AND 
ii. Patient meets ONE of the following (a or b): 
a) At baseline, patient had a BMI ≥ 30 kg/m2; OR 
Note:  This refers to baseline prior to any glucagon-like peptide-1 
(GLP-1) agonist (e.g., liraglutide [Saxenda, generic], Wegovy) or GLP-
1/glucose-dependent insulinotropic polypeptide (GIP) receptor agonist 
(e.g., Zepbound). 
33 Pages  - Cigna National Formulary Coverage  - Policy:Weight Loss – Glucagon-Like Peptide-1 Agonists Prior 
Authorization Policy 
 
b) Patient meets BOTH of the following [(1) and (2)]: 
(1) 
At baseline, patient had a BMI ≥ 27 kg/m2; AND 
(2) 
At baseline, patient had, or patient currently has, at least ONE 
of the following weight-related comorbidities:  hypertension, type 2 
diabetes, dyslipidemia, obstructive sleep apnea, cardiovascular 
disease, knee osteoarthritis, asthma, chronic obstructive pulmonary 
disease, metabolic dysfunction-associated steatotic liver 
disease/non-alcoholic fatty liver disease, polycystic ovarian 
syndrome, or coronary artery disease; AND 
Note:  This refers to baseline prior to any glucagon-like peptide-1
```

### Rank 4 — Distance 0.4949

- Section: III.
- Medication: Wegovy injection
- Indication: 1. Weight Loss in an Adult with Overweight or Obesity.  Approve for the
- Pathway: B) Patient is Currently Receiving Wegovy injection, Wegovy HD injection, or

**Original policy text:**

```text
disease/non-alcoholic fatty liver disease, polycystic ovarian 
syndrome, or coronary artery disease; AND 
Note:  This refers to baseline prior to any glucagon-like peptide-1 
(GLP-1) agonist (e.g., liraglutide [Saxenda, generic], Wegovy) or GLP-
1/glucose-dependent insulinotropic polypeptide (GIP) receptor agonist 
(e.g., Zepbound). 
iii. Patient has lost ≥ 5% of baseline body weight; AND 
Note:  This refers to baseline prior to any glucagon-like peptide-1 (GLP-1) 
agonist (e.g., liraglutide [Saxenda, generic], Wegovy) or GLP-1/glucose-
dependent insulinotropic polypeptide (GIP) receptor agonist (e.g., 
Zepbound). 
iv. The medication will be used concomitantly with behavioral modification 
and a reduced-calorie diet.
```

### Rank 5 — Distance 0.5247

- Section: IV.
- Medication: Wegovy tablet
- Indication: 1. Weight Loss in an Adult with Overweight or Obesity.  Approve for the
- Pathway: B) Patient is Currently Receiving Wegovy tablet, Wegovy injection, or Wegovy

**Original policy text:**

```text
B) Patient is Currently Receiving Wegovy tablet, Wegovy injection, or Wegovy 
HD injection.  Approve for 1 year if the patient meets ALL of the following (i, 
ii, iii, and iv): 
Note:  For a patient who has not completed 8 months of initial therapy with 
Wegovy tablet and/or Wegovy injection, refer to Initial Therapy criteria 
above. 
i. Patient is ≥ 18 years of age; AND 
ii. Patient meets ONE of the following (a or b): 
a) At baseline, patient had a BMI ≥ 30 kg/m2; OR 
Note:  This refers to baseline prior to any glucagon-like peptide-1 (GLP-1) 
agonist (e.g., liraglutide [Saxenda, generic], Wegovy) or GLP-1/glucose-
dependent insulinotropic polypeptide (GIP) receptor agonist (e.g., 
Zepbound). 
b) Patient meets BOTH of the following [(1) and (2)]: 
(1) 
At baseline, patient had a BMI ≥ 27 kg/m2; AND 
(2) 
At baseline, patient had, or patient currently has, at least ONE 
of the following weight-related comorbidities:  hypertension, type 2 
diabetes, dyslipidemia, obstructive sleep apnea, cardiovascular 
disease, knee osteoarthritis, asthma, chronic obstructive pulmonary 
disease, metabolic dysfunction-associated steatotic liver 
disease/non-alcoholic fatty liver disease, polycystic ovarian 
syndrome, or coronary artery disease; AND 
Note:  This refers to baseline prior to any glucagon-like peptide-1 
(GLP-1) agonist (e.g., liraglutide [Saxenda, generic], Wegovy) or GLP-
1/glucose-dependent insulinotropic polypeptide (GIP) receptor agonist 
(e.g., Zepbound).
```


---

## CIGNA-03

**Payer:** cigna

**Query:** Cigna Wegovy tablet adult weight loss initial authorization requirements

**Expected pathway metadata:** `{"medication": "Wegovy tablet", "indication_contains": "Weight Loss in an Adult", "pathway_contains": "Initial Therapy"}`

### Mandatory requirements — manual ground truth

- [ ] Review original policy and list every required condition here

### Retrieval review

- [ ] Correct pathway retrieved
- [ ] All mandatory conditions covered
- [ ] AND/OR logic preserved

### Rank 1 — Distance 0.4050

- Section: IV.
- Medication: Wegovy tablet
- Indication: 1. Weight Loss in an Adult with Overweight or Obesity.  Approve for the
- Pathway: 

**Original policy text:**

```text
1. Weight Loss in an Adult with Overweight or Obesity.  Approve for the 
duration noted if the patient meets ONE of the following (A or B): 
```

### Rank 2 — Distance 0.4314

- Section: IV.
- Medication: Wegovy tablet
- Indication: 1. Weight Loss in an Adult with Overweight or Obesity.  Approve for the
- Pathway: A) Initial Therapy.  Approve for 8 months if the patient meets ALL of the

**Original policy text:**

```text
1/glucose-dependent insulinotropic polypeptide (GIP) receptor agonist 
(e.g., Zepbound). 
33 Pages  - Cigna National Formulary Coverage  - Policy:Weight Loss – Glucagon-Like Peptide-1 Agonists Prior 
Authorization Policy 
 
iv. The medication will be used concomitantly with behavioral modification 
and a reduced-calorie diet; OR
```

### Rank 3 — Distance 0.4563

- Section: IV.
- Medication: Wegovy tablet
- Indication: 1. Weight Loss in an Adult with Overweight or Obesity.  Approve for the
- Pathway: A) Initial Therapy.  Approve for 8 months if the patient meets ALL of the

**Original policy text:**

```text
A) Initial Therapy.  Approve for 8 months if the patient meets ALL of the 
following (i, ii, iii, and iv): 
i. Patient is ≥ 18 years of age; AND 
ii. Patient has engaged in a trial of behavioral modification and dietary 
restriction for at least 3 months; AND 
iii. Patient meets ONE of the following (a or b): 
a) At baseline, patient had a BMI ≥ 30 kg/m2; OR 
Note:  This refers to baseline prior to any glucagon-like peptide-1 (GLP-1) 
agonist (e.g., liraglutide [Saxenda, generic], Wegovy) or GLP-1/glucose-
dependent insulinotropic polypeptide (GIP) receptor agonist (e.g., 
Zepbound). 
c) Patient meets BOTH of the following [(1) and (2)]: 
(1) 
At baseline, patient had a BMI ≥ 27 kg/m2; AND 
(2) 
At baseline, patient had, or patient currently has, at least ONE 
of the following weight-related comorbidities:  hypertension, type 2 
diabetes, dyslipidemia, obstructive sleep apnea, cardiovascular 
disease, knee osteoarthritis, asthma, chronic obstructive pulmonary 
disease, metabolic dysfunction-associated steatotic liver 
disease/non-alcoholic fatty liver disease, polycystic ovarian 
syndrome, or coronary artery disease; AND 
Note:  This refers to baseline prior to any glucagon-like peptide-1 
(GLP-1) agonist (e.g., liraglutide [Saxenda, generic], Wegovy) or GLP-
1/glucose-dependent insulinotropic polypeptide (GIP) receptor agonist 
(e.g., Zepbound). 
33 Pages  - Cigna National Formulary Coverage  - Policy:Weight Loss – Glucagon-Like Peptide-1 Agonists Prior
```

### Rank 4 — Distance 0.4787

- Section: III.
- Medication: Wegovy injection
- Indication: 1. Weight Loss in an Adult with Overweight or Obesity.  Approve for the
- Pathway: B) Patient is Currently Receiving Wegovy injection, Wegovy HD injection, or

**Original policy text:**

```text
B) Patient is Currently Receiving Wegovy injection, Wegovy HD injection, or 
Wegovy tablet.  Approve for 1 year if the patient meets ALL of the following 
(i, ii, iii, and iv): 
Note:  For a patient who has not completed 8 months of initial therapy with 
Wegovy injection, Wegovy HD injection, and/or Wegovy tablet, refer to Initial 
Therapy criteria above. 
i. Patient is ≥ 18 years of age; AND 
ii. Patient meets ONE of the following (a or b): 
a) At baseline, patient had a BMI ≥ 30 kg/m2; OR 
Note:  This refers to baseline prior to any glucagon-like peptide-1 
(GLP-1) agonist (e.g., liraglutide [Saxenda, generic], Wegovy) or GLP-
1/glucose-dependent insulinotropic polypeptide (GIP) receptor agonist 
(e.g., Zepbound). 
33 Pages  - Cigna National Formulary Coverage  - Policy:Weight Loss – Glucagon-Like Peptide-1 Agonists Prior 
Authorization Policy 
 
b) Patient meets BOTH of the following [(1) and (2)]: 
(1) 
At baseline, patient had a BMI ≥ 27 kg/m2; AND 
(2) 
At baseline, patient had, or patient currently has, at least ONE 
of the following weight-related comorbidities:  hypertension, type 2 
diabetes, dyslipidemia, obstructive sleep apnea, cardiovascular 
disease, knee osteoarthritis, asthma, chronic obstructive pulmonary 
disease, metabolic dysfunction-associated steatotic liver 
disease/non-alcoholic fatty liver disease, polycystic ovarian 
syndrome, or coronary artery disease; AND 
Note:  This refers to baseline prior to any glucagon-like peptide-1
```

### Rank 5 — Distance 0.4809

- Section: III.
- Medication: Wegovy injection
- Indication: 1. Weight Loss in an Adult with Overweight or Obesity.  Approve for the
- Pathway: 

**Original policy text:**

```text
1. Weight Loss in an Adult with Overweight or Obesity.  Approve for the 
duration noted if the patient meets ONE of the following (A or B): 
```


---

## CIGNA-04

**Payer:** cigna

**Query:** Cigna Zepbound adult obesity weight loss initial therapy BMI and dietary restriction

**Expected pathway metadata:** `{"medication": "Zepbound", "indication_contains": "Weight Loss in an Adult", "pathway_contains": "Initial Therapy"}`

### Mandatory requirements — manual ground truth

- [ ] Review original policy and list every required condition here

### Retrieval review

- [ ] Correct pathway retrieved
- [ ] All mandatory conditions covered
- [ ] AND/OR logic preserved

### Rank 1 — Distance 0.4116

- Section: V.
- Medication: Zepbound
- Indication: 1. Weight Loss in an Adult with Overweight or Obesity.  Approve for the
- Pathway: A) Initial Therapy.  Approve for 8 months if the patient meets ALL of the

**Original policy text:**

```text
A) Initial Therapy.  Approve for 8 months if the patient meets ALL of the 
following (i, ii, iii, and iv): 
i. Patient is ≥ 18 years of age; AND 
ii. Patient has engaged in a trial of behavioral modification and dietary 
restriction for at least 3 months; AND 
iii. Patient meets ONE of the following (a or b): 
a) At baseline, patient had a BMI ≥ 30 kg/m2; OR 
Note:  This refers to baseline prior to any glucagon-like peptide-1 
(GLP-1) agonist (e.g., liraglutide [Saxenda, generic], Wegovy) or GLP-
1/glucose-dependent insulinotropic polypeptide (GIP) receptor agonist 
(e.g., Zepbound). 
b) Patient meets BOTH of the following [(1) and (2)]: 
(1) 
At baseline, patient had a BMI ≥ 27 kg/m2; AND 
(2) 
At baseline, patient had, or patient currently has, at least ONE 
of the following weight-related comorbidities:  hypertension, type 2 
diabetes, dyslipidemia, obstructive sleep apnea, cardiovascular 
disease, knee osteoarthritis, asthma, chronic obstructive pulmonary 
disease, metabolic dysfunction-associated steatotic liver 
disease/non-alcoholic fatty liver disease, polycystic ovarian 
syndrome, or coronary artery disease; AND 
Note:  This refers to baseline prior to any glucagon-like peptide-1 
(GLP-1) agonist (e.g., liraglutide [Saxenda, generic], Wegovy) or GLP-
1/glucose-dependent insulinotropic polypeptide (GIP) receptor agonist 
(e.g., Zepbound). 
iv. The medication will be used concomitantly with behavioral modification 
and a reduced-calorie diet; OR
```

### Rank 2 — Distance 0.4358

- Section: V.
- Medication: Zepbound
- Indication: 1. Weight Loss in an Adult with Overweight or Obesity.  Approve for the
- Pathway: A) Initial Therapy.  Approve for 8 months if the patient meets ALL of the

**Original policy text:**

```text
1/glucose-dependent insulinotropic polypeptide (GIP) receptor agonist 
(e.g., Zepbound). 
iv. The medication will be used concomitantly with behavioral modification 
and a reduced-calorie diet; OR 
33 Pages  - Cigna National Formulary Coverage  - Policy:Weight Loss – Glucagon-Like Peptide-1 Agonists Prior 
Authorization Policy
```

### Rank 3 — Distance 0.4470

- Section: V.
- Medication: Zepbound
- Indication: 1. Weight Loss in an Adult with Overweight or Obesity.  Approve for the
- Pathway: 

**Original policy text:**

```text
1. Weight Loss in an Adult with Overweight or Obesity.  Approve for the 
duration noted if the patient meets ONE of the following (A or B): 
```

### Rank 4 — Distance 0.4603

- Section: V.
- Medication: Zepbound
- Indication: 1. Weight Loss in an Adult with Overweight or Obesity.  Approve for the
- Pathway: B) Patient is Currently Receiving Zepbound.  Approve for 1 year if the patient

**Original policy text:**

```text
B) Patient is Currently Receiving Zepbound.  Approve for 1 year if the patient 
meets ALL of the following (i, ii, iii, and iv): 
Note:  For a patient who has not completed 8 months of initial therapy, refer 
to Initial Therapy criteria above. 
i. Patient is ≥ 18 years of age; AND 
ii. Patient meets ONE of the following (a or b): 
a) At baseline, patient had a BMI ≥ 30 kg/m2; OR 
Note:  This refers to baseline prior to any glucagon-like peptide-1 
(GLP-1) agonist (e.g., liraglutide [Saxenda, generic], Wegovy) or GLP-
1/glucose-dependent insulinotropic polypeptide (GIP) receptor agonist 
(e.g., Zepbound). 
b) Patient meets BOTH of the following [(1) and (2)]: 
(1) 
At baseline, patient had a BMI ≥ 27 kg/m2; AND 
(2) 
At baseline, patient had, or patient currently has, at least ONE 
of the following weight-related comorbidities:  hypertension, type 2 
diabetes, dyslipidemia, obstructive sleep apnea, cardiovascular 
disease, knee osteoarthritis, asthma, chronic obstructive pulmonary 
disease, metabolic dysfunction-associated steatotic liver 
disease/non-alcoholic fatty liver disease, polycystic ovarian 
syndrome, or coronary artery disease; AND 
Note:  This refers to baseline prior to any glucagon-like peptide-1 
(GLP-1) agonist (e.g., liraglutide [Saxenda, generic], Wegovy) or GLP-
1/glucose-dependent insulinotropic polypeptide (GIP) receptor agonist 
(e.g., Zepbound). 
iii. Patient has lost ≥ 5% of baseline body weight; AND
```

### Rank 5 — Distance 0.4903

- Section: V.
- Medication: Zepbound
- Indication: 1. Weight Loss in an Adult with Overweight or Obesity.  Approve for the
- Pathway: B) Patient is Currently Receiving Zepbound.  Approve for 1 year if the patient

**Original policy text:**

```text
1/glucose-dependent insulinotropic polypeptide (GIP) receptor agonist 
(e.g., Zepbound). 
iii. Patient has lost ≥ 5% of baseline body weight; AND 
Note:  This refers to baseline prior to any glucagon-like peptide-1 (GLP-1) 
agonist (e.g., liraglutide [Saxenda, generic], Wegovy) or GLP-1/glucose-
dependent insulinotropic polypeptide (GIP) receptor agonist (e.g., 
Zepbound). 
iv. The medication will be used concomitantly with behavioral modification 
and a reduced-calorie diet.
```


---

## CIGNA-05

**Payer:** cigna

**Query:** Cigna liraglutide Saxenda pediatric obesity initial therapy requirements

**Expected pathway metadata:** `{"medication": "Liraglutide", "indication_contains": "Weight Loss in a Pediatric", "pathway_contains": "Initial Therapy"}`

### Mandatory requirements — manual ground truth

- [ ] Review original policy and list every required condition here

### Retrieval review

- [ ] Correct pathway retrieved
- [ ] All mandatory conditions covered
- [ ] AND/OR logic preserved

### Rank 1 — Distance 0.3350

- Section: I.
- Medication: Liraglutide
- Indication: 2. Weight Loss in a Pediatric Patient with Obesity.  Approve for the duration
- Pathway: A) Initial Therapy.  Approve for 4 months if the patient meets ALL of the

**Original policy text:**

```text
A) Initial Therapy.  Approve for 4 months if the patient meets ALL of the 
following (i, ii, iii, and iv): 
i. Patient is ≥ 12 years of age and < 18 years of age; AND 
ii. Patient has engaged in a trial of behavioral modification and dietary 
restriction for at least 3 months; AND 
iii. At baseline, patient had a BMI ≥ 95th percentile for age and sex; AND 
Note:  This refers to baseline prior to any glucagon-like peptide-1 (GLP-1) 
agonist (e.g., liraglutide [Saxenda, generic], Wegovy) or GLP-1/glucose-
dependent insulinotropic polypeptide (GIP) receptor agonist (e.g., 
Zepbound). 
iv. The medication will be used concomitantly with behavioral modification 
and a reduced-calorie diet; OR 
```

### Rank 2 — Distance 0.3455

- Section: I.
- Medication: Liraglutide
- Indication: 2. Weight Loss in a Pediatric Patient with Obesity.  Approve for the duration
- Pathway: B) Patient is Currently Receiving liraglutide (Saxenda, generic).  Approve for 1

**Original policy text:**

```text
B) Patient is Currently Receiving liraglutide (Saxenda, generic).  Approve for 1 
year if the patient meets ALL of the following (i, ii, iii, and iv): 
Note:  For a patient who has not completed 4 months of initial therapy, refer 
to Initial Therapy criteria above. 
i. Patient is ≥ 12 years of age and < 18 years of age; AND 
ii. At baseline, patient had a BMI ≥ 95th percentile for age and sex; AND 
Note:  This refers to baseline prior to any glucagon-like peptide-1 (GLP-1) 
agonist (e.g., liraglutide [Saxenda, generic], Wegovy) or GLP-1/glucose-
dependent insulinotropic polypeptide (GIP) receptor agonist (e.g., 
Zepbound). 
iii. Patient has had a reduction in BMI of ≥ 1% from baseline; AND 
Note:  This refers to baseline prior to any glucagon-like peptide-1 (GLP-1) 
agonist (e.g., liraglutide [Saxenda, generic], Wegovy) or GLP-1/glucose-
dependent insulinotropic polypeptide (GIP) receptor agonist (e.g., 
Zepbound). 
33 Pages  - Cigna National Formulary Coverage  - Policy:Weight Loss – Glucagon-Like Peptide-1 Agonists Prior 
Authorization Policy 
 
iv. The medication will be used concomitantly with behavioral modification 
and a reduced-calorie diet. 
 
 
```

### Rank 3 — Distance 0.3983

- Section: I.
- Medication: Liraglutide
- Indication: 2. Weight Loss in a Pediatric Patient with Obesity.  Approve for the duration
- Pathway: 

**Original policy text:**

```text
2. Weight Loss in a Pediatric Patient with Obesity.  Approve for the duration 
noted if the patient meets ONE of the following (A or B): 
```

### Rank 4 — Distance 0.4798

- Section: I.
- Medication: Liraglutide
- Indication: 1. Weight Loss in an Adult with Overweight or Obesity.  Approve for the
- Pathway: B) Patient is Currently Receiving liraglutide (Saxenda, generic).  Approve for 1

**Original policy text:**

```text
B) Patient is Currently Receiving liraglutide (Saxenda, generic).  Approve for 1 
year if the patient meets ALL of the following (i, ii, iii, and iv): 
Note:  For a patient who has not completed 4 months of initial therapy, refer 
to Initial Therapy criteria above. 
i. Patient is ≥ 18 years of age; AND 
ii. Patient meets ONE of the following (a or b):  
a) At baseline, patient had a BMI ≥ 30 kg/m2; OR 
Note:  This refers to baseline prior to any glucagon-like peptide-1 
(GLP-1) agonist (e.g., liraglutide [Saxenda, generic], Wegovy) or GLP-
1/glucose-dependent insulinotropic polypeptide (GIP) receptor agonist 
(e.g., Zepbound). 
b) Patient meets BOTH of the following [(1) and (2)]: 
(1) 
At baseline, patient had a BMI ≥ 27 kg/m2; AND 
33 Pages  - Cigna National Formulary Coverage  - Policy:Weight Loss – Glucagon-Like Peptide-1 Agonists Prior 
Authorization Policy 
 
(2) 
At baseline, patient had, or patient currently has, at least ONE 
of the following weight-related comorbidities:  hypertension, type 2 
diabetes, dyslipidemia, obstructive sleep apnea, cardiovascular 
disease, knee osteoarthritis, asthma, chronic obstructive pulmonary 
disease, metabolic dysfunction-associated steatotic liver 
disease/non-alcoholic fatty liver disease, polycystic ovarian 
syndrome, or coronary artery disease; AND 
Note:  This refers to baseline prior to any glucagon-like peptide-1 
(GLP-1) agonist (e.g., liraglutide [Saxenda, generic], Wegovy) or GLP-
```

### Rank 5 — Distance 0.4813

- Section: I.
- Medication: Liraglutide
- Indication: 1. Weight Loss in an Adult with Overweight or Obesity.  Approve for the
- Pathway: A) Initial Therapy.  Approve for 4 months if the patient meets ALL of the

**Original policy text:**

```text
A) Initial Therapy.  Approve for 4 months if the patient meets ALL of the 
following (i, ii, iii, and iv): 
i. Patient is ≥ 18 years of age; AND 
ii. Patient has engaged in a trial of behavioral modification and dietary 
restriction for at least 3 months; AND 
iii. Patient meets ONE of the following (a or b): 
a) At baseline, patient had a BMI ≥ 30 kg/m2; OR 
Note:  This refers to baseline prior to any glucagon-like peptide-1 
(GLP-1) agonist (e.g., liraglutide [Saxenda, generic], Wegovy) or GLP-
1/glucose-dependent insulinotropic polypeptide (GIP) receptor agonist 
(e.g., Zepbound). 
b) Patient meets BOTH of the following [(1) and (2)]: 
(1) 
At baseline, patient had a BMI ≥ 27 kg/m2; AND 
(2) 
At baseline, patient had, or patient currently has, at least ONE 
of the following weight-related comorbidities:  hypertension, type 2 
diabetes, dyslipidemia, obstructive sleep apnea, cardiovascular 
disease, knee osteoarthritis, asthma, chronic obstructive pulmonary 
disease, metabolic dysfunction-associated steatotic liver 
disease/non-alcoholic fatty liver disease, polycystic ovarian 
syndrome, or coronary artery disease; AND 
Note:  This refers to baseline prior to any glucagon-like peptide-1 
(GLP-1) agonist (e.g., liraglutide [Saxenda, generic], Wegovy) or GLP-
1/glucose-dependent insulinotropic polypeptide (GIP) receptor agonist 
(e.g., Zepbound). 
iv. The medication will be used concomitantly with behavioral modification 
and a reduced-calorie diet; OR 
```


---

## UHC-01

**Payer:** unitedhealthcare

**Query:** UnitedHealthcare North Dakota weight loss Wegovy initial authorization requirements

**Expected pathway metadata:** `{"section_contains": "North Dakota", "pathway_contains": "Initial Authorization"}`

### Mandatory requirements — manual ground truth

- [ ] Review original policy and list every required condition here

### Retrieval review

- [ ] Correct pathway retrieved
- [ ] All mandatory conditions covered
- [ ] AND/OR logic preserved

### Rank 1 — Distance 0.5105

- Section: Coverage Criteria for North Dakota Fully Insured EHB (Small Group and Individual)
- Medication: 
- Indication: 
- Pathway: B. Reauthorization

**Original policy text:**

```text
references. Formatting changes. 
9/2021 
Added Wegovy to criteria. Updated Saxenda criteria to allow for 
coverage for 12 years and older.  Updated Qsymia weight loss goal to 
greater than 3 percent per label and changed initial authorization to 4 
months. Updated references. 
9/2022 
Added background note that this program is intended to meet regulatory 
requirements for coverage of weight loss medications in California, 
Maryland, New Mexico and New York.  This program is replacing 
policy P 1172-8. Changed Qsymia age requirement to 12 or older due to 
new pediatric labeling.  Updated Imcivree to include new FDA 
approved indication for Bardet-Biedl syndrome.  Updated references.  
2/2023 
Updated Wegovy criteria to include pediatric patients based on new 
labeling. Added state mandate language. 
12/2023 
Added Zepbound to criteria.  Removed Maryland from background.     
5/2024 
Removed notation that Zepbound may be excluded at launch. Added 
coverage for secondary cardiovascular risk reduction for Wegovy. 
7/2024 
Added coverage requirements for North Dakota EHB. 
3/2025 
Added coverage for obstructive sleep apnea for Zepbound.  
5/2025 
Updated Wegovy initial authorization duration to 5 months.  
6/2025 
Added Vykat XR as in scope. Added Vykat XR criteria and updated 
program name to include appetite suppressants. Updated references. 
Formatting changes. 
11/2025 
Added coverage for MASH for Wegovy. Updated references. 
2/2026
```

### Rank 2 — Distance 0.5326

- Section: Coverage Criteria for North Dakota Fully Insured EHB (Small Group and Individual)
- Medication: 
- Indication: 
- Pathway: A. Initial Authorization

**Original policy text:**

```text
A. Initial Authorization  
 
1. Wegovy injection or tablet, or Zepbound will be approved based on all of the 
following criteria: 
 
a. One of the following: 
 
(1) Treatment is being requested for appetite suppression or weight loss 
(2)  Wegovy injection or tablet is being requested for risk reduction of major 
adverse cardiovascular events with established cardiovascular disease (i.e. 
prior myocardial infarction, ischemic or hemorrhagic stroke, or peripheral 
arterial disease)b 
(3)  Wegovy injection is being requested for treatment of metabolic dysfunction-
associated steatohepatitis (MASH) [formerly known as nonalcoholic 
steatohepatitis (NASH)] with moderate to advanced liver fibrosis (i.e., 
fibrosis stage F2 or F3)b 
(4)  Zepbound is being requested for moderate to severe obstructive sleep apneac 
 
-AND- 
 
b. One of the following:  
 
(1) Patient is ≥ 12 years of age for Wegovy injection 
(2) Patient is > 16 years of age for Wegovy tablet and Zepbound  
 
-AND- 
 
c. Used as an adjunct to lifestyle modification (e.g., dietary or caloric restriction, 
exercise, behavioral support, community-based program) 
 
-AND- 
 
d. One of the following: 
 
(1) Body Mass Index (BMI) ≥ 40 kg/m2 or for pediatric patients a BMI > 120% 
of 95th percentile  
 
-OR- 
 
 
© 2026 UnitedHealthcare Services Inc. 
6 
 
 
(2) Wegovy injection is being requested for treatment of MASHb 
 
Wegovy injection or tablet: Authorization will be issued for 5 months.
```

### Rank 3 — Distance 0.5599

- Section: Coverage Criteria for North Dakota Fully Insured EHB (Small Group and Individual)
- Medication: 
- Indication: 
- Pathway: A. Initial Authorization

**Original policy text:**

```text
-OR- 
 
 
© 2026 UnitedHealthcare Services Inc. 
6 
 
 
(2) Wegovy injection is being requested for treatment of MASHb 
 
Wegovy injection or tablet: Authorization will be issued for 5 months. 
 
Zepbound: Authorization will be issued for 6 months.
```

### Rank 4 — Distance 0.5627

- Section: Section 3:  Coverage criteria for North Dakota Fully Insured EHB (Small Group and Individual)
- Medication: 
- Indication: 
- Pathway: A. Initial Authorization

**Original policy text:**

```text
-AND- 
 
c. Used as an adjunct to lifestyle modification (e.g., dietary or caloric restriction, 
exercise, behavioral support, community-based program) 
 
-AND- 
  
d. One of the following: 
 
(1) Body Mass Index (BMI) ≥ 30 kg/m2 or for pediatric patients a BMI > 95th 
percentile  
 
-OR- 
 
(2) Both of the following:  
 
(a) BMI ≥ 27 kg/m2  
 
-AND- 
 
(b) Patient has a weight-related comorbidity (e.g., dyslipidemia, hypertension, 
type 2 diabetes, sleep apnea) 
 
-OR- 
 
(c) Wegovy injection is being requested for treatment of MASH 
 
© 2026 UnitedHealthcare Services Inc. 
3 
 
 
 
benzphetamine, diethylpropion, phendimetrazine, phentermine: Authorization will 
be issued for 3 months. 
 
Contrave, Qsymia or Saxenda: Authorization will be issued for 4 months. 
 
Wegovy injection or tablet: Authorization will be issued for 5 months. 
 
Xenical or Zepbound: Authorization will be issued for 6 months. 
 
2. Imcivree will be approved based on all of the following criteria:  
 
a. One of the following:  
 
(1)  Diagnosis of obesity is due to POMC, PCSK1, or LEPR gene deficiency 
confirmed with genetic testing interpreted as pathogenic, likely pathogenic, or of 
uncertain significance 
 
-OR- 
 
(2)  Diagnosis of Bardet-Biedl syndrome 
 
-AND- 
 
b. One of the following: 
 
(1) Adult patient with BMI ≥ 30 kg/m2  
 
-OR- 
 
(2) Pediatric patient with weight >95th percentile for age on growth chart assessment 
 
-AND-
```

### Rank 5 — Distance 0.5777

- Section: Coverage Criteria for North Dakota Fully Insured EHB (Small Group and Individual)
- Medication: 
- Indication: 
- Pathway: B. Reauthorization

**Original policy text:**

```text
B. Reauthorization 
 
1. Wegovy injection or tablet, or Zepbound will be approved based on both of the 
following criteria: 
 
a. One of the following: 
 
(1) Weight loss of ≥ 5% of baseline body weight for Zepbound 
 
-OR- 
 
(2) One of the following for Wegovy: 
(a) For Wegovy injection, all of the following: 
i. 
Requested for the treatment of MASHb 
ii. 
Documentation of positive clinical response to Wegovy injection 
(e.g., improvement in or stabilization of fibrosis) 
iii. 
Patient has not progressed to cirrhosis 
(b) For Wegovy injection or tablet, weight loss of ≥ 5% of baseline body 
weight 
 
-AND- 
 
b. Continuation of lifestyle modification 
 
Authorization will be issued for 12 months. 
 
a State mandates may apply.  Any federal regulatory requirements and the member specific 
benefit plan coverage may also impact coverage criteria. Other policies and utilization 
management programs may apply. 
b Refer to Nonformulary Wegovy criteria for plans that do not cover weight loss medications.   
c Refer to Nonformulary Zepbound criteria for plans that do not cover weight loss medications.   
 
4. 
Additional Clinical Rules: 
 
• 
Supply limits may be in place. 
 
5. 
References: 
 
1.    American Association of Clinical Endocrinologists and American College of 
Endocrinology Comprehensive Clinical Practice Guidelines for Medical Care of Patients 
with Obesity.  Endocr Pract. 2016;22(Suppl 3).   
2.
```


---

## UHC-02

**Payer:** unitedhealthcare

**Query:** UnitedHealthcare North Dakota weight loss reauthorization continuation requirements

**Expected pathway metadata:** `{"section_contains": "North Dakota", "pathway_contains": "Reauthorization"}`

### Mandatory requirements — manual ground truth

- [ ] Review original policy and list every required condition here

### Retrieval review

- [ ] Correct pathway retrieved
- [ ] All mandatory conditions covered
- [ ] AND/OR logic preserved

### Rank 1 — Distance 0.5095

- Section: Coverage Criteria for North Dakota Fully Insured EHB (Small Group and Individual)
- Medication: 
- Indication: 
- Pathway: B. Reauthorization

**Original policy text:**

```text
Change Control 
Date 
Change 
11/2013 
Reformatted to standard and updated references.  Clarified risk factors 
required in addition to BMI of 27-29.  Removed criteria that coverage 
would not be provided if used in combination with other weight loss 
agents.  Shortened initial authorization for sympathomimetics to 3 
months based on PI recommendations for short-term use.  Added 
reauthorization criteria for 6 months, changed initial authorization 
period of Xenical from 4 months to 3 months, and shortened 
reauthorization of Belviq and Xenical to 12 months for alignment with 
OptumRx.   
11/2014 
Added Contrave to guideline. 
7/2015 
Added Saxenda to guideline. 
9/2016 
Annual Review.  Added Belviq XR to guideline.  Revised authorization 
period for Xenical.  Removed ASO from title- program will remain as 
ASO option. 
9/2017 
Annual Review.  Added Lomaira.  Updated references.  Revised 
weightloss percentage for Saxenda per PI.  
 
© 2026 UnitedHealthcare Services Inc. 
8 
 
 
9/2018 
Annual Review.  Updated references. 
. 
9/2019 
Annual Review.  Revised background section.  Revised list of 
modifications of weight related comorbidity. 
9/2020 
Annual review. Updated references.  Removed Belviq/Belviq XR. 
4/2021 
Added Imcivree as in scope. Added Imcivree criteria. Updated 
references. Formatting changes. 
9/2021 
Added Wegovy to criteria. Updated Saxenda criteria to allow for 
coverage for 12 years and older.  Updated Qsymia weight loss goal to
```

### Rank 2 — Distance 0.6217

- Section: Section 3:  Coverage criteria for North Dakota Fully Insured EHB (Small Group and Individual)
- Medication: 
- Indication: 
- Pathway: B. Reauthorization

**Original policy text:**

```text
Authorization for benzphetamine, diethylpropion, phentermine or phendimetrazine 
or will be issued for 6 months.   
 
2. Imcivree will be approved based on one of the following criteria: 
 
a. If on therapy for less than 12 months, documentation of a positive clinical response 
to Imcivree therapy defined as weight loss ≥5% of baseline weight 
 
-OR- 
 
b. If on therapy for ≥12 months, documentation of a positive clinical response to 
Imcivree therapy defined as ≥10% weight loss from baseline 
 
Authorization will be issued for 12 months. 
 
3. Vykat XR will be approved based on the following criterion: 
 
a. Documentation of positive clinical response to Vykat XR therapy 
 
 
© 2026 UnitedHealthcare Services Inc. 
5 
 
 
Authorization will be issued for 12 months. 
 
a State mandates may apply.  Any federal regulatory requirements and the member specific benefit 
plan coverage may also impact coverage criteria. Other policies and utilization management 
programs may apply. 
b Refer to Nonformulary Wegovy criteria for plans that do not cover weight loss medications.  
c Refer to Nonformulary Zepbound criteria for plans that do not cover weight loss medications.   
 
3.
```

### Rank 3 — Distance 0.6231

- Section: Coverage Criteria for North Dakota Fully Insured EHB (Small Group and Individual)
- Medication: 
- Indication: 
- Pathway: B. Reauthorization

**Original policy text:**

```text
references. Formatting changes. 
9/2021 
Added Wegovy to criteria. Updated Saxenda criteria to allow for 
coverage for 12 years and older.  Updated Qsymia weight loss goal to 
greater than 3 percent per label and changed initial authorization to 4 
months. Updated references. 
9/2022 
Added background note that this program is intended to meet regulatory 
requirements for coverage of weight loss medications in California, 
Maryland, New Mexico and New York.  This program is replacing 
policy P 1172-8. Changed Qsymia age requirement to 12 or older due to 
new pediatric labeling.  Updated Imcivree to include new FDA 
approved indication for Bardet-Biedl syndrome.  Updated references.  
2/2023 
Updated Wegovy criteria to include pediatric patients based on new 
labeling. Added state mandate language. 
12/2023 
Added Zepbound to criteria.  Removed Maryland from background.     
5/2024 
Removed notation that Zepbound may be excluded at launch. Added 
coverage for secondary cardiovascular risk reduction for Wegovy. 
7/2024 
Added coverage requirements for North Dakota EHB. 
3/2025 
Added coverage for obstructive sleep apnea for Zepbound.  
5/2025 
Updated Wegovy initial authorization duration to 5 months.  
6/2025 
Added Vykat XR as in scope. Added Vykat XR criteria and updated 
program name to include appetite suppressants. Updated references. 
Formatting changes. 
11/2025 
Added coverage for MASH for Wegovy. Updated references. 
2/2026
```

### Rank 4 — Distance 0.6450

- Section: Coverage Criteria for North Dakota Fully Insured EHB (Small Group and Individual)
- Medication: 
- Indication: 
- Pathway: B. Reauthorization

**Original policy text:**

```text
Obesity Society.  Circulation. 2014; 129:S102-138 
12.  World Health Organization. (2006). Global Database on Body Mass Index.   Retrieved 
from https://www.who.int/data/gho/data/themes/topics/topic-details/GHO/body-mass-index 
13. 
Lomaira [package insert].  Newtown, PA: KVK-Tech, Inc.  December 2023. 
14.  Imcivree [package insert]. Boston, MA: Rhythm Pharmaceuticals, Inc; November 2023.  
15.  Wegovy [package insert]. Plainsboro, NJ: Novo Nordisk; December 2025.  
16.     Jastreboff, AM, et al.  Tirzepatide Once Weekly for the Treatment of Obesity.  N Engl J 
Med 2022 ; 387 : 205-216.  
17.   Zepbound [package insert].  Indianapolis, IN: Lilly USA, LLC ; December 2024.  
18.   Grunvald E, Shah R, Hernaez R, etc al. AGA Clinical Practice Guideline on 
Pharmacological Interventions for Adults with Obesity.  Gastroenterology 2022;163:1198-
1225. 
19.     Vykat XR [package insert]. Redwood City, CA : Soleno Therapeutics, Inc.; March 2025. 
20. 
Rinella ME, Neuschwander-Tetri BA, Siddiqui MS, et al. AASLD Practice Guidance on 
the clinical assessment and management of nonalcoholic fatty liver disease. Hepatology. 
2023;77(5):1797-1835. doi:10.1097/HEP.0000000000000323 
 
 
Program 
Plans with Weight Loss/Appetite Suppression Medication Coverage 
Change Control 
Date 
Change 
11/2013 
Reformatted to standard and updated references.  Clarified risk factors 
required in addition to BMI of 27-29.  Removed criteria that coverage
```

### Rank 5 — Distance 0.6705

- Section: Coverage Criteria for North Dakota Fully Insured EHB (Small Group and Individual)
- Medication: 
- Indication: 
- Pathway: B. Reauthorization

**Original policy text:**

```text
Endocrinology Comprehensive Clinical Practice Guidelines for Medical Care of Patients 
with Obesity.  Endocr Pract. 2016;22(Suppl 3).   
2.  
Benzphetamine [package insert]. Laurelton, NY: Epic Pharma, LLC; June 2023.   
3.  
Diethylpropion ER [package insert].  Congers, NY: Chartwell RX, LLC; March 2023.  
 
© 2026 UnitedHealthcare Services Inc. 
7 
 
 
4.  
Phendimetrazine Slow-Release Capsules [package insert].  Langhorne, PA: Acertis 
Pharmaceuticals, LLC; September 2019.  
5.  
Adipex-P [package insert].  Parsippany, NJ: Teva Pharmaceuticals USA, Inc; March 2024.  
6.      Xenical [package insert].  Montgomery, AL: H2-Pharma, LLC; July 2024.    
7.  
Qsymia [package insert].  Moutain View, CA.  Vivus, Inc ; September 2024.     
8. 
Contrave [package insert].  Brentwood, TN: Nalpropion Pharmaceuticals, LLC; May 2024.   
9. 
Saxenda [package insert].  Plainsboro, NJ: Novo Nordisk ; November 2024.  
10. 
Pharmacological Management of Obesity: An Endocrine Society Clinical Practice 
Guideline.  The Journal of Clinical Endocrinology & Metabolism 2015 100:2, 342-362  
11.  AHA/ACC/TOS Prevention Guideline: 2013 AHA/ACC/TOS Guideline for the 
Management of Overweight and Obesity in Adults: A Report to the American College of 
Cardiology/American Health Association Task Force on Practice Guidelines and The 
Obesity Society.  Circulation. 2014; 129:S102-138 
12.  World Health Organization. (2006). Global Database on Body Mass Index.   Retrieved
```
