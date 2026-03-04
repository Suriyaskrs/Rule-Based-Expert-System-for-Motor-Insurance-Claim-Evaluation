# 🧠 First-Order Logic Expert System for Motor Insurance Claim Evaluation

## Rule-Based Expert System Using FOL Knowledge Representation

---

## 📖 Overview

This project implements a **complete First-Order Logic (FOL) based expert system** for motor insurance claim evaluation. Unlike simple if-else rule systems, this implementation uses:

- **First-Order Logic** for knowledge representation
- **Forward Chaining** inference with unification
- **Modus Ponens** reasoning mechanism
- **Horn Clauses** for rule representation
- **Complete separation** of knowledge base and inference engine

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    USER INTERFACE                       │
│                  (streamlit_fol_app.py)                 │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌───────────────────────────────────────────────────────┐
│              MOTOR INSURANCE EXPERT SYSTEM            │
│           (motor_insurance_expert_system.py)          │
│  ┌─────────────────────────────────────────────────┐  │
│  │     REASONING MECHANISM                         │  │
│  │  • Domain-specific claim evaluation             │  │
│  │  • Result interpretation                        │  │
│  │  • Explanation generation                       │  │
│  └──────────────────┬──────────────────────────────┘  │
│                     │                                 │
│                     ▼                                 │
│  ┌─────────────────────────────────────────────────┐  │
│  │     INFERENCE ENGINE                            │  │
│  │     (fol_inference_engine.py)                   │  │
│  │  ┌──────────────────────────────────────────┐   │  │
│  │  │  Forward Chaining Algorithm              │   │  │
│  │  │  • Rule matching                         │   │  │
│  │  │  • Fact derivation                       │   │  │
│  │  │  • Iterative inference                   │   │  │
│  │  └──────────────────────────────────────────┘   │  │
│  │  ┌──────────────────────────────────────────┐   │  │
│  │  │  Unification                             │   │  │
│  │  │  • Pattern matching                      │   │  │
│  │  │  • Variable binding                      │   │  │
│  │  │  • Substitution merging                  │   │  │
│  │  └──────────────────────────────────────────┘   │  │
│  └──────────────────┬──────────────────────────────┘  │
│                     │                                 │
│                     ▼                                 │
│  ┌────────────────────────────────────────────────┐   │
│  │     KNOWLEDGE BASE                             │   │
│  │     (fol_knowledge_representation.py)          │   │
│  │  ┌──────────────────┐  ┌────────────────────┐  │   │
│  │  │  FACTS           │  │  RULES             │  │   │
│  │  │  • Predicates    │  │  • Horn Clauses    │  │   │
│  │  │  • Ground atoms  │  │  • Quantifiers     │  │   │
│  │  │                  │  │  • Variables       │  │   │
│  │  └──────────────────┘  └────────────────────┘  │   │
│  └────────────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────┘
```

---

## 📂 Project Structure

```
.
├── fol_knowledge_representation.py   # FOL predicates, rules, KB
├── fol_inference_engine.py           # Forward chaining, unification
├── motor_insurance_expert_system.py  # Main expert system
├── streamlit_fol_app.py              # User interface
├── requirements.txt                  # Dependencies
├── README.md                         # This file
└── sample_claims_data.csv            # Test data
```

---

## 🔬 First-Order Logic Components

### 1. **Predicates**

Predicates represent relationships and properties:

```
PolicyActive(policy, date)
Covers(policy_type, loss_type)
FraudRisk(claim, risk_level)
PayableAmount(claim, amount)
```

### 2. **Rules (Horn Clauses)**

Rules use quantifiers and logical connectives:

```
∀p, d, s, e (PolicyPeriod(p, s, e) ∧ DateInRange(d, s, e) → PolicyActive(p, d))

∀c, p (PolicyType(p, third_party) ∧ 
       LossType(c, own_damage) ∧ 
       ClaimOnPolicy(c, p) 
       → NotCovered(c))

∀c (HighRisk(c) → UnderInvestigation(c))
```

### 3. **Facts**

Ground predicates (no variables):

```
PolicyType(policy1, comprehensive)
LossOccurred(claim1, 2024-06-15, accident)
DocumentsComplete(claim1)
```

### 4. **Unification**

Pattern matching to bind variables:

```
Unify:
  PolicyActive(?p, ?d)
  PolicyActive(policy1, 2024-06-15)

Result:
  θ = {?p: policy1, ?d: 2024-06-15}
```

### 5. **Modus Ponens**

Inference rule:

```
Given:  A → B  (rule)
        A      (fact)
Derive: B      (new fact)
```

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- pip package manager

### Step 1: Install dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run the application
```bash
streamlit run streamlit_fol_app.py
```

### Step 3: Access the web interface
```
http://localhost:8501
```

---

## 💻 Usage

### Mode 1: Single Claim Evaluation

1. Navigate to "Claim Evaluation" tab
2. Enter policy and claim details
3. Click "Evaluate Claim Using FOL Reasoning"
4. View decision, explanation, and FOL inference trace

### Mode 2: Batch Processing

1. Navigate to "Batch Processing" tab
2. Download CSV template
3. Fill in claim data
4. Upload and process
5. Download results

### Mode 3: Knowledge Base Exploration

1. Navigate to "Knowledge Base" tab
2. View all predicate definitions
3. Examine FOL rules with quantifiers
4. Explore domain facts

---

## 📊 Example Evaluation

### Input:
```python
{
    'policy_type': 'comprehensive',
    'loss_date': datetime(2024, 6, 15),
    'loss_type': 'accident',
    'claim_amount': 150000,
    'sum_insured': 500000,
    'deductible': 5000,
    'documents_complete': True,
    'previous_claims': 1
}
```

### FOL Inference Process:

**Step 1: Load facts into KB**
```
PolicyType(policy1, comprehensive)
LossOccurred(claim1, 2024-06-15, accident)
ClaimAmount(claim1, 150000)
...
```

**Step 2: Apply Rule R1 (Policy Active)**
```
Rule: ∀p, d, s, e (PolicyPeriod(p, s, e) ∧ DateInRange(d, s, e) → PolicyActive(p, d))
Match: PolicyPeriod(policy1, 2024-01-01, 2025-01-01) ✓
       DateInRange(2024-06-15, 2024-01-01, 2025-01-01) ✓
θ = {?p: policy1, ?d: 2024-06-15}
Derive: PolicyActive(policy1, 2024-06-15)
```

**Step 3: Apply Rule R2 (Valid Claim)**
```
Rule: ∀c, p, d (ClaimOnPolicy(c, p) ∧ PolicyActive(p, d) → ValidClaim(c))
Match: ClaimOnPolicy(claim1, policy1) ✓
       PolicyActive(policy1, 2024-06-15) ✓
Derive: ValidClaim(claim1)
```

**Step 4: Apply Rule R4 (Coverage)**
```
Rule: ∀p, c, t (PolicyType(p, comprehensive) ∧ 
                 ComprehensiveCoverage(t) → CoverageApplies(c))
Match: PolicyType(policy1, comprehensive) ✓
       ComprehensiveCoverage(accident) ✓
Derive: CoverageApplies(claim1)
```

**Step 5: Apply Rule R14 (Approval)**
```
Rule: ∀c (ValidClaim(c) ∧ CoverageApplies(c) ∧ ... → Approved(c))
All antecedents satisfied ✓
Derive: Approved(claim1)
```

**Step 6: Apply Rule R17 (Amount)**
```
Rule: ∀c, ca, si (ClaimAmount(c, ca) ∧ SumInsured(c, si) → AdmissibleLoss(c, MIN(ca, si)))
Calculate: MIN(150000, 500000) = 150000
Derive: AdmissibleLoss(claim1, 150000)
```

**Step 7: Apply Rule R18 (Payable)**
```
Rule: ∀c, al, d (AdmissibleLoss(c, al) ∧ Deductible(c, d) → PayableAmount(c, al - d))
Calculate: 150000 - 5000 = 145000
Derive: PayableAmount(claim1, 145000)
```

### Output:
```
Decision: APPROVED
Payable Amount: ₹145,000
Explanation: Claim approved - valid period, covered loss, documents complete
```

---

## 🧠 Knowledge Base Details

### Predicate Categories

| Category | Predicates | Example |
|----------|-----------|---------|
| **Policy** | PolicyType, PolicyPeriod, PolicyActive | PolicyActive(p1, date) |
| **Claim** | LossOccurred, ClaimAmount, ValidClaim | ValidClaim(c1) |
| **Coverage** | Covers, CoverageApplies, NotCovered | CoverageApplies(c1) |
| **Document** | FIRSubmitted, DocumentsComplete | DocumentsComplete(c1) |
| **Risk** | FraudRisk, HighRisk, PreviousClaims | HighRisk(c1) |
| **Decision** | Approved, Rejected, UnderInvestigation | Approved(c1) |
| **Amount** | PayableAmount, AdmissibleLoss | PayableAmount(c1, 145000) |

### Rule Categories (20 Total Rules)

1. **Policy Validity** (R1-R3): Check policy active status
2. **Coverage** (R4-R6): Determine what's covered
3. **Documentation** (R7-R9): Verify required documents
4. **Fraud Risk** (R10-R12): Assess fraud risk level
5. **Investigation** (R13): Flag for investigation
6. **Approval** (R14): Approve qualifying claims
7. **Rejection** (R15-R16): Reject invalid claims
8. **Amount Calculation** (R17-R20): Calculate payout

---

## 🔍 Key Differences from Simple If-Else

| Feature | If-Else System | FOL Expert System |
|---------|---------------|-------------------|
| **Representation** | Procedural code | Declarative logic |
| **Knowledge** | Hardcoded in code | Separate KB |
| **Inference** | Sequential execution | Forward chaining |
| **Pattern Matching** | Explicit checks | Unification algorithm |
| **Variables** | Local variables | Quantified variables |
| **Extensibility** | Modify code | Add rules to KB |
| **Explanation** | Manual trace | Automatic derivation |
| **Formal Semantics** | No | Yes (FOL semantics) |

---

## 🎯 Advantages of FOL Approach

### 1. **Expressiveness**
FOL can represent complex relationships:
```
∀c, p, n (ClaimOnPolicy(c, p) ∧ PreviousClaims(p, n) ∧ n ≥ 3 → HighRisk(c))
```

### 2. **Modularity**
Rules are independent and can be added/modified separately:
```python
kb.add_rule(new_rule)  # Add without changing other rules
```

### 3. **Soundness**
Logical inference guarantees valid conclusions from valid premises

### 4. **Explainability**
Complete trace of logical derivations:
```
PolicyActive(p1, d) ← PolicyPeriod(p1, s, e) ∧ DateInRange(d, s, e)
ValidClaim(c1) ← PolicyActive(p1, d) ∧ ClaimOnPolicy(c1, p1)
Approved(c1) ← ValidClaim(c1) ∧ CoverageApplies(c1) ∧ ...
```

### 5. **Separation of Concerns**
- **KB**: What we know (domain knowledge)
- **Inference**: How we reason (logical rules)
- **UI**: How we interact (user interface)

---

## 📚 Technical Details

### Unification Algorithm

Implemented in `fol_inference_engine.py`:

```python
def unify_predicates(pred1, pred2) -> Substitution:
    """
    Unify two predicates
    Returns substitution θ that makes them identical
    """
    # Match predicate names and arity
    # Recursively unify arguments
    # Build substitution mapping
```

### Forward Chaining

Implemented in `fol_inference_engine.py`:

```python
def forward_chain():
    """
    Repeatedly apply rules until no new facts derived
    """
    while new_facts:
        for rule in rules:
            # Find all substitutions matching antecedents
            for θ in unify_conjunction(rule.antecedents, facts):
                # Apply θ to consequent
                new_fact = θ.apply(rule.consequent)
                if new_fact not in facts:
                    facts.add(new_fact)  # Modus ponens
```

### Reasoning Mechanism

Implemented in `motor_insurance_expert_system.py`:

```python
def evaluate_claim(claim_data):
    """
    1. Convert input to FOL facts
    2. Run forward chaining
    3. Query derived facts for decision
    4. Generate explanation
    """
```

---

## 🧪 Testing

### Test Case 1: Approved Claim
```
Input: Comprehensive policy, accident, all docs complete
Expected: Approved, payable = claim - deductible
FOL Trace: ValidClaim → CoverageApplies → Approved → PayableAmount
```

### Test Case 2: Coverage Rejection
```
Input: Third-party policy, own damage
Expected: Rejected, not covered
FOL Trace: NotCovered → Rejected → PayableAmount(0)
```

### Test Case 3: High Fraud Risk
```
Input: 3+ previous claims
Expected: Under investigation
FOL Trace: HighRisk → UnderInvestigation
```

---

## 📖 Code Examples

### Adding a New Rule

```python
# Define new rule in FOL
new_rule = Rule(
    rule_id="R21",
    antecedents=[
        Predicate("LossType", ("?claim", "total_loss"), PredicateType.CLAIM),
        Predicate("ClaimAmount", ("?claim", "?amt"), PredicateType.AMOUNT),
        Predicate("SumInsured", ("?policy", "?si"), PredicateType.POLICY)
    ],
    consequent=Predicate("SpecialReview", ("?claim",), PredicateType.DECISION),
    variables={"?claim", "?policy", "?amt", "?si"},
    description="Total loss claims need special review"
)

# Add to knowledge base
kb.add_rule(new_rule)
```

### Querying the KB

```python
# Query for approved claims
approved_query = Predicate("Approved", ("?claim",), PredicateType.DECISION)
results = inference_engine.query(approved_query)

for θ in results:
    print(f"Approved claim: {θ.lookup('?claim')}")
```

---

## 🎓 Educational Value

This project demonstrates:

1. **Knowledge Engineering Lifecycle**
   - Knowledge acquisition
   - Representation in FOL
   - Inference mechanism
   - Explanation facility

2. **AI Fundamentals**
   - First-order logic
   - Unification algorithm
   - Forward chaining
   - Pattern matching

3. **Software Engineering**
   - Separation of concerns
   - Modular architecture
   - Clean code principles

---

## 🔮 Future Enhancements

1. **Backward Chaining**: Goal-driven reasoning
2. **Uncertainty**: Fuzzy logic or probabilistic reasoning
3. **Learning**: Rule learning from examples
4. **Optimization**: Rete algorithm for efficiency
5. **Visualization**: Graphical rule network display

---

## 📝 References

- **FOL**: Russell & Norvig - Artificial Intelligence: A Modern Approach
- **Expert Systems**: Jackson - Introduction to Expert Systems
- **Unification**: Robinson - A Machine-Oriented Logic Based on Resolution
- **Forward Chaining**: Forgy - Rete: A Fast Algorithm for Many Patterns

---

## 🤝 Contributing

This is an educational project demonstrating FOL-based expert systems.
Suggestions for improvements:
- Additional insurance rules
- Performance optimizations
- Enhanced explanations
- More comprehensive testing

---

## 📄 License

Educational/Academic Use

---

## ✨ Key Takeaways

✅ **FOL provides formal semantics** for knowledge representation  
✅ **Unification enables pattern matching** with variables  
✅ **Forward chaining derives conclusions** from facts  
✅ **Separation of KB and inference** enables modularity  
✅ **Complete explanation** through logical derivation  
✅ **Extensible** through declarative rule addition  

---

**Built with:** Python, Streamlit, First-Order Logic  
**Paradigm:** Rule-Based Expert System with FOL  
**Inference:** Forward Chaining + Unification + Modus Ponens  
**Domain:** Motor Insurance Claim Evaluation
