"""
FOL-Based Motor Insurance Claim Evaluation Expert System

Architecture:
1. Knowledge Representation (FOL predicates and rules)
2. Knowledge Base (facts and rules storage)
3. Inference Engine (forward chaining with unification)
4. Reasoning Mechanism (domain-specific logic)
5. User Interface (Streamlit)
"""

from datetime import datetime
from typing import Dict, Any
from knowledge_representation import (
    FOLKnowledgeBase, Predicate, PredicateType
)
from inference_engine import (
    FOLInferenceEngine, ReasoningMechanism
)
from knowledge_base import motor_insurance_kb


class MotorInsuranceExpertSystem:
    """
    Main Expert System for Motor Insurance Claim Evaluation
    
    Uses First-Order Logic for knowledge representation and reasoning
    """
    
    def __init__(self):
        self.kb = FOLKnowledgeBase()
        
        # Load domain facts from separate knowledge base module
        for fact in motor_insurance_kb.get_domain_facts():
            self.kb.add_fact(fact)
        
        # Load inference rules from separate knowledge base module
        for rule in motor_insurance_kb.get_inference_rules():
            self.kb.add_rule(rule)
        
        self.inference_engine = FOLInferenceEngine(self.kb)
        self.reasoning = ReasoningMechanism(self.inference_engine)
    
    def load_claim_data(self, claim_data: Dict[str, Any]):
        """
        Convert claim input data into FOL predicates and add to KB
        
        This is the bridge between user input and FOL representation
        """
        claim_id = "claim1"  # In real system, would be unique per claim
        policy_id = "policy1"
        
        # Clear previous claim facts (keep rules and domain facts)
        self._clear_claim_facts()
        
        # Extract data
        policy_type = claim_data['policy_type']
        policy_start = claim_data['policy_start_date']
        policy_end = claim_data['policy_end_date']
        loss_date = claim_data['loss_date']
        loss_type = claim_data['loss_type']
        claim_amount = claim_data['claim_amount']
        sum_insured = claim_data['sum_insured']
        deductible = claim_data['deductible']
        fir_submitted = claim_data['fir_submitted']
        documents_complete = claim_data['documents_complete']
        previous_claims = claim_data['previous_claims']
        
        # === POLICY FACTS ===
        self.kb.add_fact(Predicate(
            "PolicyType", (policy_id, policy_type), PredicateType.POLICY
        ))
        
        self.kb.add_fact(Predicate(
            "PolicyPeriod", (policy_id, policy_start, policy_end), PredicateType.POLICY
        ))
        
        self.kb.add_fact(Predicate(
            "SumInsured", (policy_id, sum_insured), PredicateType.POLICY
        ))
        
        self.kb.add_fact(Predicate(
            "Deductible", (policy_id, deductible), PredicateType.POLICY
        ))
        
        # === CLAIM FACTS ===
        self.kb.add_fact(Predicate(
            "ClaimOnPolicy", (claim_id, policy_id), PredicateType.CLAIM
        ))
        
        self.kb.add_fact(Predicate(
            "LossOccurred", (claim_id, loss_date, loss_type), PredicateType.CLAIM
        ))
        
        self.kb.add_fact(Predicate(
            "LossType", (claim_id, loss_type), PredicateType.CLAIM
        ))
        
        self.kb.add_fact(Predicate(
            "ClaimAmount", (claim_id, claim_amount), PredicateType.AMOUNT
        ))
        
        # === TEMPORAL FACTS ===
        # Check if date is in range
        if policy_start <= loss_date <= policy_end:
            self.kb.add_fact(Predicate(
                "DateInRange", (loss_date, policy_start, policy_end), PredicateType.POLICY
            ))
        else:
            self.kb.add_fact(Predicate(
                "PolicyNotActive", (policy_id, loss_date), PredicateType.POLICY
            ))
        
        # === DOCUMENT FACTS ===
        if documents_complete:
            self.kb.add_fact(Predicate(
                "DocumentsComplete", (claim_id,), PredicateType.DOCUMENT
            ))
        else:
            self.kb.add_fact(Predicate(
                "DocumentsIncomplete", (claim_id,), PredicateType.DOCUMENT
            ))
        
        if fir_submitted:
            self.kb.add_fact(Predicate(
                "FIRSubmitted", (claim_id,), PredicateType.DOCUMENT
            ))
            self.kb.add_fact(Predicate(
                "FIRConditionMet", (claim_id,), PredicateType.DOCUMENT
            ))
        else:
            self.kb.add_fact(Predicate(
                "FIRNotSubmitted", (claim_id,), PredicateType.DOCUMENT
            ))
            # Check if FIR is required
            if loss_type in ['theft', 'fire']:
                # FIR condition NOT met (required but not submitted)
                pass
            else:
                # FIR not required, so condition is met
                self.kb.add_fact(Predicate(
                    "FIRConditionMet", (claim_id,), PredicateType.DOCUMENT
                ))
        
        # === RISK FACTS ===
        self.kb.add_fact(Predicate(
            "PreviousClaims", (policy_id, previous_claims), PredicateType.RISK
        ))
        
        # Add comparison predicates
        if previous_claims >= 3:
            self.kb.add_fact(Predicate(
                "GreaterThanEqual", (previous_claims, 3), PredicateType.RISK
            ))
        
        if previous_claims <= 1:
            self.kb.add_fact(Predicate(
                "LessThanEqual", (previous_claims, 1), PredicateType.RISK
            ))
        
        # Add high/low risk helper facts
        if previous_claims < 3:
            self.kb.add_fact(Predicate(
                "NotHighRisk", (claim_id,), PredicateType.RISK
            ))
        
        # === AMOUNT FACTS ===
        self.kb.add_fact(Predicate(
            "SumInsuredFor", (claim_id, sum_insured), PredicateType.AMOUNT
        ))
        
        self.kb.add_fact(Predicate(
            "DeductibleFor", (claim_id, deductible), PredicateType.AMOUNT
        ))
        
        # For amount calculation, we need to add these as intermediate facts
        # that the inference engine can use since FOL rules can't do arithmetic directly
        
        # Pre-calculate admissible loss for approved claims
        # This will be used by the inference engine
        admissible_loss = min(claim_amount, sum_insured)
        
        # Pre-calculate payable amount
        payable_amount = max(0, admissible_loss - deductible)
    
    def _clear_claim_facts(self):
        """Clear claim-specific facts, keeping domain facts and rules"""
        # Remove all facts except domain facts from the knowledge base module
        domain_predicates = {"ComprehensiveCoverage", "FIRMandatoryFor"}
        self.kb.facts = {
            fact for fact in self.kb.facts 
            if fact.name in domain_predicates
        }
    
    def evaluate_claim(self, claim_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main entry point for claim evaluation
        
        Steps:
        1. Load claim data as FOL predicates
        2. Run forward chaining inference
        3. Extract results from derived facts
        4. Generate explanation
        """
        # Load claim data into KB
        self.load_claim_data(claim_data)
        
        # Run FOL reasoning
        result = self.reasoning.evaluate_claim("claim1")
        
        # Add original input for reference
        result['input_data'] = claim_data
        
        return result
    
    def display_knowledge_base(self) -> str:
        """Display the current knowledge base"""
        return self.kb.display_knowledge_base()
    
    def display_reasoning_summary(self) -> str:
        """Display reasoning summary"""
        return self.reasoning.display_reasoning_summary()


def parse_date(date_input) -> datetime:
    """Parse date from various formats"""
    if isinstance(date_input, datetime):
        return date_input
    if isinstance(date_input, str):
        for fmt in ['%Y-%m-%d', '%d/%m/%Y', '%d-%m-%Y']:
            try:
                return datetime.strptime(date_input, fmt)
            except:
                continue
    return date_input


def parse_boolean(bool_input) -> bool:
    """Parse boolean from various formats"""
    if isinstance(bool_input, bool):
        return bool_input
    if isinstance(bool_input, str):
        return bool_input.lower() in ['yes', 'true', '1', 'y']
    return bool(bool_input)


# Example usage
if __name__ == "__main__":
    # Create expert system
    expert_system = MotorInsuranceExpertSystem()
    
    # Example claim
    claim_data = {
        'policy_type': 'comprehensive',
        'policy_start_date': datetime(2024, 1, 1),
        'policy_end_date': datetime(2025, 1, 1),
        'loss_date': datetime(2024, 6, 15),
        'loss_type': 'accident',
        'claim_amount': 150000,
        'sum_insured': 500000,
        'deductible': 5000,
        'fir_submitted': True,
        'documents_complete': True,
        'previous_claims': 1
    }
    
    # Evaluate
    result = expert_system.evaluate_claim(claim_data)
    
    print("=" * 80)
    print("CLAIM EVALUATION RESULT")
    print("=" * 80)
    print(f"Decision: {result['decision']}")
    print(f"Validity: {result['claim_validity']}")
    print(f"Coverage: {result['coverage_status']}")
    print(f"Fraud Risk: {result['fraud_risk']}")
    print(f"Payable Amount: ₹{result['payable_amount']:,.2f}")
    print("")
    print("Explanation:")
    print(result['explanation'])
    print("")
    
    # Display KB
    print(expert_system.display_knowledge_base())
    
    # Display reasoning summary
    print(expert_system.display_reasoning_summary())
    
    # Display inference trace
    print("=" * 80)
    print("INFERENCE TRACE")
    print("=" * 80)
    for line in result['inference_trace']:
        print(line)