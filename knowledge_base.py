"""
Knowledge Base for Motor Insurance Claim Evaluation
Contains all domain-specific knowledge, facts, and rules

This module stores the knowledge separate from the representation structure
"""

from fol_knowledge_representation import Rule, Predicate, PredicateType


class MotorInsuranceKnowledgeBase:
    """
    Domain-specific knowledge base for motor insurance claims
    
    Contains:
    1. Domain facts (static knowledge about insurance)
    2. Inference rules (how to reason about claims)
    """
    
    def __init__(self):
        self.domain_facts = []
        self.inference_rules = []
        self._initialize_domain_facts()
        self._initialize_inference_rules()
    
    def _initialize_domain_facts(self):
        """
        Initialize domain-specific facts that are always true
        
        These are static facts about the insurance domain
        """
        # Comprehensive policy coverage facts
        self.domain_facts.extend([
            Predicate("ComprehensiveCoverage", ("accident",), PredicateType.COVERAGE),
            Predicate("ComprehensiveCoverage", ("theft",), PredicateType.COVERAGE),
            Predicate("ComprehensiveCoverage", ("fire",), PredicateType.COVERAGE),
            Predicate("ComprehensiveCoverage", ("own_damage",), PredicateType.COVERAGE),
        ])
        
        # FIR mandatory loss types
        self.domain_facts.extend([
            Predicate("FIRMandatoryFor", ("theft",), PredicateType.DOCUMENT),
            Predicate("FIRMandatoryFor", ("fire",), PredicateType.DOCUMENT),
        ])
    
    def _initialize_inference_rules(self):
        """
        Initialize all inference rules for claim evaluation
        
        Rules are organized by category for maintainability
        """
        
        # ==================== POLICY VALIDITY RULES ====================
        
        self.inference_rules.append(Rule(
            rule_id="R1",
            antecedents=[
                Predicate("PolicyPeriod", ("?policy", "?start", "?end"), PredicateType.POLICY),
                Predicate("DateInRange", ("?date", "?start", "?end"), PredicateType.POLICY)
            ],
            consequent=Predicate("PolicyActive", ("?policy", "?date"), PredicateType.POLICY),
            variables={"?policy", "?date", "?start", "?end"},
            description="Policy is active if date falls within policy period",
            priority=10
        ))
        
        self.inference_rules.append(Rule(
            rule_id="R2",
            antecedents=[
                Predicate("ClaimOnPolicy", ("?claim", "?policy"), PredicateType.CLAIM),
                Predicate("LossOccurred", ("?claim", "?date", "?type"), PredicateType.CLAIM),
                Predicate("PolicyActive", ("?policy", "?date"), PredicateType.POLICY)
            ],
            consequent=Predicate("ValidClaim", ("?claim",), PredicateType.CLAIM),
            variables={"?claim", "?policy", "?date", "?type"},
            description="Claim is valid if loss occurred during active policy period",
            priority=10
        ))
        
        self.inference_rules.append(Rule(
            rule_id="R3",
            antecedents=[
                Predicate("ClaimOnPolicy", ("?claim", "?policy"), PredicateType.CLAIM),
                Predicate("LossOccurred", ("?claim", "?date", "?type"), PredicateType.CLAIM),
                Predicate("PolicyNotActive", ("?policy", "?date"), PredicateType.POLICY)
            ],
            consequent=Predicate("InvalidClaim", ("?claim",), PredicateType.CLAIM),
            variables={"?claim", "?policy", "?date", "?type"},
            description="Claim is invalid if loss occurred outside policy period",
            priority=10
        ))
        
        # ==================== COVERAGE RULES ====================
        
        self.inference_rules.append(Rule(
            rule_id="R4",
            antecedents=[
                Predicate("PolicyType", ("?policy", "comprehensive"), PredicateType.POLICY),
                Predicate("LossType", ("?claim", "?loss_type"), PredicateType.CLAIM),
                Predicate("ClaimOnPolicy", ("?claim", "?policy"), PredicateType.CLAIM),
                Predicate("ComprehensiveCoverage", ("?loss_type",), PredicateType.COVERAGE)
            ],
            consequent=Predicate("CoverageApplies", ("?claim",), PredicateType.COVERAGE),
            variables={"?policy", "?claim", "?loss_type"},
            description="Comprehensive policy covers accident, theft, fire, own_damage",
            priority=9
        ))
        
        self.inference_rules.append(Rule(
            rule_id="R5",
            antecedents=[
                Predicate("PolicyType", ("?policy", "third_party"), PredicateType.POLICY),
                Predicate("LossType", ("?claim", "own_damage"), PredicateType.CLAIM),
                Predicate("ClaimOnPolicy", ("?claim", "?policy"), PredicateType.CLAIM)
            ],
            consequent=Predicate("NotCovered", ("?claim",), PredicateType.COVERAGE),
            variables={"?policy", "?claim"},
            description="Third-party policy does not cover own vehicle damage",
            priority=9
        ))
        
        self.inference_rules.append(Rule(
            rule_id="R6",
            antecedents=[
                Predicate("LossType", ("?claim", "third_party_damage"), PredicateType.CLAIM),
                Predicate("ClaimOnPolicy", ("?claim", "?policy"), PredicateType.CLAIM)
            ],
            consequent=Predicate("CoverageApplies", ("?claim",), PredicateType.COVERAGE),
            variables={"?claim", "?policy"},
            description="Third-party damage is covered by all policy types",
            priority=9
        ))
        
        # ==================== DOCUMENT RULES ====================
        
        self.inference_rules.append(Rule(
            rule_id="R7",
            antecedents=[
                Predicate("LossType", ("?claim", "?type"), PredicateType.CLAIM),
                Predicate("FIRMandatoryFor", ("?type",), PredicateType.DOCUMENT)
            ],
            consequent=Predicate("FIRRequired", ("?claim",), PredicateType.DOCUMENT),
            variables={"?claim", "?type"},
            description="FIR is mandatory for theft and fire claims",
            priority=8
        ))
        
        self.inference_rules.append(Rule(
            rule_id="R8",
            antecedents=[
                Predicate("FIRRequired", ("?claim",), PredicateType.DOCUMENT),
                Predicate("FIRNotSubmitted", ("?claim",), PredicateType.DOCUMENT)
            ],
            consequent=Predicate("Rejected", ("?claim",), PredicateType.DECISION),
            variables={"?claim"},
            description="Claim rejected if required FIR not submitted",
            priority=8
        ))
        
        self.inference_rules.append(Rule(
            rule_id="R9",
            antecedents=[
                Predicate("DocumentsIncomplete", ("?claim",), PredicateType.DOCUMENT)
            ],
            consequent=Predicate("Rejected", ("?claim",), PredicateType.DECISION),
            variables={"?claim"},
            description="Claim rejected if documents are incomplete",
            priority=8
        ))
        
        # ==================== FRAUD RISK RULES ====================
        
        self.inference_rules.append(Rule(
            rule_id="R10",
            antecedents=[
                Predicate("ClaimOnPolicy", ("?claim", "?policy"), PredicateType.CLAIM),
                Predicate("PreviousClaims", ("?policy", "?count"), PredicateType.RISK),
                Predicate("GreaterThanEqual", ("?count", 3), PredicateType.RISK)
            ],
            consequent=Predicate("HighRisk", ("?claim",), PredicateType.RISK),
            variables={"?claim", "?policy", "?count"},
            description="High fraud risk if 3 or more previous claims",
            priority=7
        ))
        
        self.inference_rules.append(Rule(
            rule_id="R11",
            antecedents=[
                Predicate("ClaimOnPolicy", ("?claim", "?policy"), PredicateType.CLAIM),
                Predicate("PreviousClaims", ("?policy", 2), PredicateType.RISK)
            ],
            consequent=Predicate("FraudRisk", ("?claim", "medium"), PredicateType.RISK),
            variables={"?claim", "?policy"},
            description="Medium fraud risk if 2 previous claims",
            priority=7
        ))
        
        self.inference_rules.append(Rule(
            rule_id="R12",
            antecedents=[
                Predicate("ClaimOnPolicy", ("?claim", "?policy"), PredicateType.CLAIM),
                Predicate("PreviousClaims", ("?policy", "?count"), PredicateType.RISK),
                Predicate("LessThanEqual", ("?count", 1), PredicateType.RISK)
            ],
            consequent=Predicate("FraudRisk", ("?claim", "low"), PredicateType.RISK),
            variables={"?claim", "?policy", "?count"},
            description="Low fraud risk if 1 or fewer previous claims",
            priority=7
        ))
        
        # ==================== INVESTIGATION RULES ====================
        
        self.inference_rules.append(Rule(
            rule_id="R13",
            antecedents=[
                Predicate("HighRisk", ("?claim",), PredicateType.RISK)
            ],
            consequent=Predicate("UnderInvestigation", ("?claim",), PredicateType.DECISION),
            variables={"?claim"},
            description="Claims with high fraud risk require investigation",
            priority=6
        ))
        
        # ==================== APPROVAL RULES ====================
        
        self.inference_rules.append(Rule(
            rule_id="R14",
            antecedents=[
                Predicate("ValidClaim", ("?claim",), PredicateType.CLAIM),
                Predicate("CoverageApplies", ("?claim",), PredicateType.COVERAGE),
                Predicate("DocumentsComplete", ("?claim",), PredicateType.DOCUMENT),
                Predicate("NotHighRisk", ("?claim",), PredicateType.RISK),
                Predicate("FIRConditionMet", ("?claim",), PredicateType.DOCUMENT)
            ],
            consequent=Predicate("Approved", ("?claim",), PredicateType.DECISION),
            variables={"?claim"},
            description="Claim approved if all conditions satisfied",
            priority=5
        ))
        
        self.inference_rules.append(Rule(
            rule_id="R15",
            antecedents=[
                Predicate("InvalidClaim", ("?claim",), PredicateType.CLAIM)
            ],
            consequent=Predicate("Rejected", ("?claim",), PredicateType.DECISION),
            variables={"?claim"},
            description="Invalid claims are rejected",
            priority=5
        ))
        
        self.inference_rules.append(Rule(
            rule_id="R16",
            antecedents=[
                Predicate("NotCovered", ("?claim",), PredicateType.COVERAGE)
            ],
            consequent=Predicate("Rejected", ("?claim",), PredicateType.DECISION),
            variables={"?claim"},
            description="Claims without coverage are rejected",
            priority=5
        ))
        
        # ==================== AMOUNT CALCULATION RULES ====================
        
        self.inference_rules.append(Rule(
            rule_id="R17",
            antecedents=[
                Predicate("ClaimAmount", ("?claim", "?claim_amt"), PredicateType.AMOUNT),
                Predicate("SumInsuredFor", ("?claim", "?sum_insured"), PredicateType.AMOUNT),
                Predicate("Approved", ("?claim",), PredicateType.DECISION)
            ],
            consequent=Predicate("AdmissibleLoss", ("?claim", "?admissible"), PredicateType.AMOUNT),
            variables={"?claim", "?claim_amt", "?sum_insured", "?admissible"},
            description="Admissible loss is minimum of claim amount and sum insured",
            priority=4
        ))
        
        self.inference_rules.append(Rule(
            rule_id="R18",
            antecedents=[
                Predicate("AdmissibleLoss", ("?claim", "?admissible"), PredicateType.AMOUNT),
                Predicate("DeductibleFor", ("?claim", "?deductible"), PredicateType.AMOUNT)
            ],
            consequent=Predicate("PayableAmount", ("?claim", "?payable"), PredicateType.AMOUNT),
            variables={"?claim", "?admissible", "?deductible", "?payable"},
            description="Payable amount is admissible loss minus deductible",
            priority=3
        ))
        
        self.inference_rules.append(Rule(
            rule_id="R19",
            antecedents=[
                Predicate("Rejected", ("?claim",), PredicateType.DECISION)
            ],
            consequent=Predicate("PayableAmount", ("?claim", 0), PredicateType.AMOUNT),
            variables={"?claim"},
            description="Rejected claims have zero payout",
            priority=3
        ))
        
        self.inference_rules.append(Rule(
            rule_id="R20",
            antecedents=[
                Predicate("UnderInvestigation", ("?claim",), PredicateType.DECISION)
            ],
            consequent=Predicate("PayableAmount", ("?claim", 0), PredicateType.AMOUNT),
            variables={"?claim"},
            description="Claims under investigation have zero payout pending resolution",
            priority=3
        ))
    
    def get_domain_facts(self):
        """Return all domain facts"""
        return self.domain_facts
    
    def get_inference_rules(self):
        """Return all inference rules"""
        return self.inference_rules
    
    def add_custom_rule(self, rule: Rule):
        """Add a custom rule to the knowledge base"""
        self.inference_rules.append(rule)
        # Sort by priority
        self.inference_rules.sort(key=lambda r: r.priority, reverse=True)
    
    def get_rule_by_id(self, rule_id: str):
        """Get a specific rule by its ID"""
        for rule in self.inference_rules:
            if rule.rule_id == rule_id:
                return rule
        return None
    
    def display_knowledge_summary(self):
        """Display a summary of the knowledge base"""
        output = []
        output.append("=" * 80)
        output.append("MOTOR INSURANCE KNOWLEDGE BASE SUMMARY")
        output.append("=" * 80)
        output.append(f"\nDomain Facts: {len(self.domain_facts)}")
        for fact in self.domain_facts:
            output.append(f"  - {fact}")
        
        output.append(f"\nInference Rules: {len(self.inference_rules)}")
        output.append("\nRules by Category:")
        
        # Group rules by category
        categories = {
            "Policy Validity": ["R1", "R2", "R3"],
            "Coverage": ["R4", "R5", "R6"],
            "Documentation": ["R7", "R8", "R9"],
            "Fraud Risk": ["R10", "R11", "R12"],
            "Investigation": ["R13"],
            "Approval/Rejection": ["R14", "R15", "R16"],
            "Amount Calculation": ["R17", "R18", "R19", "R20"]
        }
        
        for category, rule_ids in categories.items():
            output.append(f"\n  {category}:")
            for rule_id in rule_ids:
                rule = self.get_rule_by_id(rule_id)
                if rule:
                    output.append(f"    [{rule_id}] {rule.description}")
        
        output.append("\n" + "=" * 80)
        return "\n".join(output)


# Singleton instance for easy access
motor_insurance_kb = MotorInsuranceKnowledgeBase()
