"""
First-Order Logic Inference Engine
For Motor Insurance Claim Evaluation Expert System

This module implements:
1. Forward Chaining with FOL
2. Unification algorithm
3. Modus Ponens reasoning
4. Resolution-based inference
"""

from typing import Dict, List, Set, Tuple, Optional, Any
from copy import deepcopy
from fol_knowledge_representation import (
    Predicate, Rule, FOLKnowledgeBase, PredicateType
)


class Substitution:
    """
    Represents a substitution/binding of variables to values
    
    Example: {?x: "policy1", ?y: "2024-06-15"}
    """
    def __init__(self, bindings: Optional[Dict[str, Any]] = None):
        self.bindings = bindings or {}
    
    def bind(self, variable: str, value: Any):
        """Add a new variable binding"""
        self.bindings[variable] = value
    
    def lookup(self, variable: str) -> Optional[Any]:
        """Get the value bound to a variable"""
        return self.bindings.get(variable)
    
    def apply_to_predicate(self, predicate: Predicate) -> Predicate:
        """Apply substitution to a predicate, replacing variables with values"""
        new_args = []
        for arg in predicate.arguments:
            if isinstance(arg, str) and arg.startswith("?"):
                # It's a variable
                new_args.append(self.bindings.get(arg, arg))
            else:
                new_args.append(arg)
        return Predicate(predicate.name, tuple(new_args), predicate.predicate_type)
    
    def merge(self, other: 'Substitution') -> Optional['Substitution']:
        """
        Merge two substitutions
        Returns None if there's a conflict
        """
        new_bindings = self.bindings.copy()
        for var, val in other.bindings.items():
            if var in new_bindings:
                if new_bindings[var] != val:
                    return None  # Conflict
            else:
                new_bindings[var] = val
        return Substitution(new_bindings)
    
    def __str__(self):
        return "{" + ", ".join(f"{k}: {v}" for k, v in self.bindings.items()) + "}"
    
    def __bool__(self):
        return len(self.bindings) > 0


class Unifier:
    """
    Implements the Unification algorithm for First-Order Logic
    
    Unification finds a substitution that makes two predicates identical
    """
    
    @staticmethod
    def unify_predicates(pred1: Predicate, pred2: Predicate) -> Optional[Substitution]:
        """
        Unify two predicates
        
        Example:
            unify(PolicyActive(?p, ?d), PolicyActive(policy1, 2024-06-15))
            → {?p: policy1, ?d: 2024-06-15}
        """
        # Predicates must have same name and arity
        if pred1.name != pred2.name:
            return None
        if len(pred1.arguments) != len(pred2.arguments):
            return None
        
        substitution = Substitution()
        
        for arg1, arg2 in zip(pred1.arguments, pred2.arguments):
            if not Unifier._unify_terms(arg1, arg2, substitution):
                return None
        
        return substitution
    
    @staticmethod
    def _unify_terms(term1: Any, term2: Any, subst: Substitution) -> bool:
        """
        Unify two terms (recursive helper)
        """
        # If both are variables
        if isinstance(term1, str) and term1.startswith("?"):
            if isinstance(term2, str) and term2.startswith("?"):
                if term1 == term2:
                    return True
                # Bind first variable to second
                existing = subst.lookup(term1)
                if existing is None:
                    subst.bind(term1, term2)
                    return True
                return existing == term2
            else:
                # term1 is variable, term2 is constant
                existing = subst.lookup(term1)
                if existing is None:
                    subst.bind(term1, term2)
                    return True
                return existing == term2
        
        # If term2 is variable
        elif isinstance(term2, str) and term2.startswith("?"):
            existing = subst.lookup(term2)
            if existing is None:
                subst.bind(term2, term1)
                return True
            return existing == term1
        
        # Both are constants
        else:
            return term1 == term2
    
    @staticmethod
    def unify_conjunction(antecedents: List[Predicate], facts: Set[Predicate]) -> List[Substitution]:
        """
        Find all substitutions that satisfy all antecedents
        
        This is used for matching rule antecedents against known facts
        """
        if not antecedents:
            return [Substitution()]
        
        all_substitutions = []
        
        # Start with first antecedent
        first_ant = antecedents[0]
        remaining_ants = antecedents[1:]
        
        # Find all facts that unify with first antecedent
        for fact in facts:
            subst = Unifier.unify_predicates(first_ant, fact)
            if subst is not None:
                if not remaining_ants:
                    # No more antecedents, we're done
                    all_substitutions.append(subst)
                else:
                    # Apply substitution to remaining antecedents
                    remaining_with_subst = [subst.apply_to_predicate(ant) for ant in remaining_ants]
                    # Recursively unify remaining antecedents
                    sub_results = Unifier.unify_conjunction(remaining_with_subst, facts)
                    for sub_result in sub_results:
                        merged = subst.merge(sub_result)
                        if merged:
                            all_substitutions.append(merged)
        
        return all_substitutions


class FOLInferenceEngine:
    """
    Forward Chaining Inference Engine using First-Order Logic
    
    Implements:
    - Modus Ponens: If (A → B) and A is true, then infer B
    - Forward chaining: Start from facts, apply rules to derive new facts
    - Unification: Match rule patterns against facts
    """
    
    def __init__(self, knowledge_base: FOLKnowledgeBase):
        self.kb = knowledge_base
        self.inference_trace = []
        self.iteration_count = 0
        self.max_iterations = 100  # Prevent infinite loops
    
    def reset_trace(self):
        """Clear the inference trace"""
        self.inference_trace = []
        self.iteration_count = 0
    
    def forward_chain(self) -> Set[Predicate]:
        """
        Forward Chaining Algorithm with FOL
        
        Repeatedly apply rules to derive new facts until no new facts can be derived
        
        Returns: Set of all derived facts
        """
        self.reset_trace()
        
        self.inference_trace.append("=" * 80)
        self.inference_trace.append("FORWARD CHAINING INFERENCE ENGINE - FOL")
        self.inference_trace.append("=" * 80)
        self.inference_trace.append("")
        
        self.inference_trace.append("Initial Knowledge Base:")
        self.inference_trace.append(f"  Facts: {len(self.kb.facts)}")
        self.inference_trace.append(f"  Rules: {len(self.kb.rules)}")
        self.inference_trace.append("")
        
        new_facts = True
        
        while new_facts and self.iteration_count < self.max_iterations:
            self.iteration_count += 1
            new_facts = False
            
            self.inference_trace.append(f"--- Iteration {self.iteration_count} ---")
            
            # Try to apply each rule
            for rule in self.kb.rules:
                derived = self._apply_rule(rule)
                if derived:
                    new_facts = True
            
            self.inference_trace.append("")
        
        if self.iteration_count >= self.max_iterations:
            self.inference_trace.append(f"⚠️  WARNING: Reached maximum iterations ({self.max_iterations})")
        else:
            self.inference_trace.append(f"✓ Fixed point reached after {self.iteration_count} iterations")
        
        self.inference_trace.append(f"✓ Total facts in KB: {len(self.kb.facts)}")
        self.inference_trace.append("")
        
        return self.kb.facts
    
    def _apply_rule(self, rule: Rule) -> bool:
        """
        Apply a single rule using Modus Ponens
        
        If all antecedents match (with some substitution θ), 
        then add consequent with θ applied
        
        Returns: True if new facts were derived
        """
        new_facts_derived = False
        
        # Find all substitutions that satisfy the rule antecedents
        substitutions = Unifier.unify_conjunction(rule.antecedents, self.kb.facts)
        
        for subst in substitutions:
            # Apply substitution to consequent
            new_fact = subst.apply_to_predicate(rule.consequent)
            
            # Check if this is actually a new fact
            if new_fact not in self.kb.facts:
                self.kb.facts.add(new_fact)
                new_facts_derived = True
                
                self.inference_trace.append(f"  [Rule {rule.rule_id}] FIRED")
                self.inference_trace.append(f"    Substitution: {subst}")
                self.inference_trace.append(f"    Derived: {new_fact}")
                self.inference_trace.append(f"    Description: {rule.description}")
        
        return new_facts_derived
    
    def query(self, query_predicate: Predicate) -> List[Substitution]:
        """
        Query the knowledge base
        
        Find all substitutions that make the query true
        
        Example: query(Approved(?claim)) → [{?claim: claim1}, {?claim: claim5}]
        """
        results = []
        
        for fact in self.kb.facts:
            subst = Unifier.unify_predicates(query_predicate, fact)
            if subst is not None:
                results.append(subst)
        
        return results
    
    def explain_derivation(self, fact: Predicate) -> List[str]:
        """
        Explain how a fact was derived (backward trace)
        
        This provides explanation by showing which rules led to the fact
        """
        explanation = []
        explanation.append(f"Explaining derivation of: {fact}")
        explanation.append("")
        
        # Find rules that could have derived this fact
        matching_rules = [r for r in self.kb.rules if r.consequent.name == fact.name]
        
        if not matching_rules:
            explanation.append("This is a base fact (not derived from rules)")
            return explanation
        
        # Check which rule actually derived it
        for rule in matching_rules:
            # Try to unify rule consequent with our fact
            subst = Unifier.unify_predicates(rule.consequent, fact)
            if subst:
                # Check if antecedents are satisfied
                satisfied = True
                explanation.append(f"Possibly derived by Rule {rule.rule_id}:")
                explanation.append(f"  {rule.description}")
                explanation.append(f"  Rule: {rule}")
                explanation.append(f"  Substitution: {subst}")
                explanation.append("")
                explanation.append("  Required antecedents:")
                
                for ant in rule.antecedents:
                    ant_with_subst = subst.apply_to_predicate(ant)
                    if ant_with_subst in self.kb.facts:
                        explanation.append(f"    ✓ {ant_with_subst}")
                    else:
                        explanation.append(f"    ✗ {ant_with_subst} (NOT SATISFIED)")
                        satisfied = False
                
                if satisfied:
                    explanation.append("")
                    explanation.append("  ✓ All antecedents satisfied - this rule derived the fact")
                    break
                else:
                    explanation.append("")
                    explanation.append("  ✗ Not all antecedents satisfied")
                explanation.append("")
        
        return explanation
    
    def get_inference_trace(self) -> List[str]:
        """Get the complete inference trace"""
        return self.inference_trace
    
    def get_all_derived_facts(self, predicate_name: str) -> Set[Predicate]:
        """Get all facts with a specific predicate name"""
        return {f for f in self.kb.facts if f.name == predicate_name}


class ReasoningMechanism:
    """
    High-level reasoning mechanism that coordinates inference
    
    This layer translates domain problems into FOL queries and interprets results
    """
    
    def __init__(self, inference_engine: FOLInferenceEngine):
        self.engine = inference_engine
        self.kb = inference_engine.kb
    
    def evaluate_claim(self, claim_id: str) -> Dict[str, Any]:
        """
        Evaluate a claim using FOL reasoning
        
        Returns a structured result with decision, amounts, and explanations
        """
        # Run forward chaining to derive all facts
        self.engine.forward_chain()
        
        # Query for decision
        decision = self._get_claim_decision(claim_id)
        
        # Query for amounts
        payable_amount = self._get_payable_amount(claim_id)
        
        # Query for risk assessment
        fraud_risk = self._get_fraud_risk(claim_id)
        
        # Query for validity and coverage
        validity = self._get_claim_validity(claim_id)
        coverage = self._get_coverage_status(claim_id)
        
        # Generate explanation
        explanation = self._generate_explanation(claim_id, decision, validity, coverage)
        
        return {
            'claim_id': claim_id,
            'decision': decision,
            'claim_validity': validity,
            'coverage_status': coverage,
            'fraud_risk': fraud_risk,
            'payable_amount': payable_amount,
            'explanation': explanation,
            'inference_trace': self.engine.get_inference_trace()
        }
    
    def _get_claim_decision(self, claim_id: str) -> str:
        """Determine claim decision from derived facts"""
        # Check if approved
        approved_facts = self.kb.get_facts_by_predicate("Approved")
        for fact in approved_facts:
            if claim_id in fact.arguments:
                return "approved"
        
        # Check if rejected
        rejected_facts = self.kb.get_facts_by_predicate("Rejected")
        for fact in rejected_facts:
            if claim_id in fact.arguments:
                return "rejected"
        
        # Check if under investigation
        investigation_facts = self.kb.get_facts_by_predicate("UnderInvestigation")
        for fact in investigation_facts:
            if claim_id in fact.arguments:
                return "under_investigation"
        
        return "pending"
    
    def _get_payable_amount(self, claim_id: str) -> float:
        """Get payable amount from derived facts"""
        payable_facts = self.kb.get_facts_by_predicate("PayableAmount")
        for fact in payable_facts:
            if claim_id in fact.arguments:
                # Last argument should be the amount
                return float(fact.arguments[-1])
        return 0.0
    
    def _get_fraud_risk(self, claim_id: str) -> str:
        """Get fraud risk level from derived facts"""
        # Check for specific risk levels
        risk_facts = self.kb.get_facts_by_predicate("FraudRisk")
        for fact in risk_facts:
            if claim_id in fact.arguments:
                return str(fact.arguments[-1])
        
        # Check for HighRisk predicate
        high_risk_facts = self.kb.get_facts_by_predicate("HighRisk")
        for fact in high_risk_facts:
            if claim_id in fact.arguments:
                return "high"
        
        return "low"
    
    def _get_claim_validity(self, claim_id: str) -> str:
        """Get claim validity from derived facts"""
        valid_facts = self.kb.get_facts_by_predicate("ValidClaim")
        for fact in valid_facts:
            if claim_id in fact.arguments:
                return "valid"
        
        invalid_facts = self.kb.get_facts_by_predicate("InvalidClaim")
        for fact in invalid_facts:
            if claim_id in fact.arguments:
                return "invalid"
        
        return "unknown"
    
    def _get_coverage_status(self, claim_id: str) -> str:
        """Get coverage status from derived facts"""
        coverage_facts = self.kb.get_facts_by_predicate("CoverageApplies")
        for fact in coverage_facts:
            if claim_id in fact.arguments:
                return "covered"
        
        not_covered_facts = self.kb.get_facts_by_predicate("NotCovered")
        for fact in not_covered_facts:
            if claim_id in fact.arguments:
                return "not_covered"
        
        return "unknown"
    
    def _generate_explanation(self, claim_id: str, decision: str, 
                            validity: str, coverage: str) -> str:
        """Generate natural language explanation from FOL derivations"""
        
        explanation_parts = []
        
        # Decision-based explanation
        if decision == "approved":
            explanation_parts.append("✅ CLAIM APPROVED")
            explanation_parts.append(f"The claim {claim_id} has been approved because:")
            explanation_parts.append(f"  • Claim validity: {validity}")
            explanation_parts.append(f"  • Coverage status: {coverage}")
            explanation_parts.append(f"  • All mandatory documents were submitted")
            explanation_parts.append(f"  • Fraud risk assessment passed")
            
        elif decision == "rejected":
            explanation_parts.append("❌ CLAIM REJECTED")
            explanation_parts.append(f"The claim {claim_id} has been rejected because:")
            
            if validity == "invalid":
                explanation_parts.append(f"  • The claim is INVALID (loss date outside policy period)")
            if coverage == "not_covered":
                explanation_parts.append(f"  • The loss type is NOT COVERED under the policy")
            
            # Check for document issues
            docs_incomplete = any(
                claim_id in f.arguments 
                for f in self.kb.get_facts_by_predicate("DocumentsIncomplete")
            )
            if docs_incomplete:
                explanation_parts.append(f"  • Required documents are incomplete")
            
            # Check for FIR issues
            fir_not_submitted = any(
                claim_id in f.arguments 
                for f in self.kb.get_facts_by_predicate("FIRNotSubmitted")
            )
            fir_required = any(
                claim_id in f.arguments 
                for f in self.kb.get_facts_by_predicate("FIRRequired")
            )
            if fir_required and fir_not_submitted:
                explanation_parts.append(f"  • FIR is mandatory but was not submitted")
            
        elif decision == "under_investigation":
            explanation_parts.append("🔍 UNDER INVESTIGATION")
            explanation_parts.append(f"The claim {claim_id} has been flagged for investigation because:")
            explanation_parts.append(f"  • High fraud risk detected")
            explanation_parts.append(f"  • Multiple previous claims on this policy")
            explanation_parts.append(f"  • Manual review required before final decision")
        
        else:
            explanation_parts.append("⚠️  PENDING")
            explanation_parts.append(f"The claim {claim_id} is pending evaluation.")
        
        return "\n".join(explanation_parts)
    
    def display_reasoning_summary(self) -> str:
        """Display a summary of the reasoning process"""
        output = []
        output.append("=" * 80)
        output.append("REASONING MECHANISM SUMMARY")
        output.append("=" * 80)
        output.append("")
        output.append(f"Total facts derived: {len(self.kb.facts)}")
        output.append(f"Inference iterations: {self.engine.iteration_count}")
        output.append("")
        
        # Categorize facts by type
        output.append("Facts by Category:")
        for pred_type in PredicateType:
            facts_of_type = [f for f in self.kb.facts if f.predicate_type == pred_type]
            if facts_of_type:
                output.append(f"  {pred_type.value.upper()}: {len(facts_of_type)}")
                for fact in sorted(facts_of_type, key=str)[:5]:  # Show first 5
                    output.append(f"    - {fact}")
                if len(facts_of_type) > 5:
                    output.append(f"    ... and {len(facts_of_type) - 5} more")
        
        output.append("")
        output.append("=" * 80)
        return "\n".join(output)
