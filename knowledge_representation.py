"""
First-Order Logic Knowledge Representation Module
For Motor Insurance Claim Evaluation Expert System

This module defines the FOL predicates, facts, and rules using formal logic notation.
"""

from dataclasses import dataclass
from typing import List, Dict, Any, Set, Tuple
from datetime import datetime
from enum import Enum


class PredicateType(Enum):
    """Types of predicates in our FOL system"""
    POLICY = "policy"
    CLAIM = "claim"
    COVERAGE = "coverage"
    DOCUMENT = "document"
    RISK = "risk"
    DECISION = "decision"
    AMOUNT = "amount"


@dataclass
class Predicate:
    """
    Represents a First-Order Logic Predicate
    
    Format: predicate_name(argument1, argument2, ..., argumentN)
    Example: PolicyActive(policy1, 2024-06-15)
             Covers(comprehensive, accident)
    """
    name: str
    arguments: Tuple[Any, ...]
    predicate_type: PredicateType
    
    def __str__(self):
        args_str = ", ".join(str(arg) for arg in self.arguments)
        return f"{self.name}({args_str})"
    
    def __hash__(self):
        return hash((self.name, self.arguments))
    
    def __eq__(self, other):
        if not isinstance(other, Predicate):
            return False
        return self.name == other.name and self.arguments == other.arguments


@dataclass
class Rule:
    """
    Represents a First-Order Logic Rule (Horn Clause)
    
    Format: ∀x, y, z... (Antecedent1 ∧ Antecedent2 ∧ ... → Consequent)
    
    Example: ∀p, d (PolicyActive(p, d) ∧ DateInRange(d, p.start, p.end) → ValidClaim(p, d))
    """
    rule_id: str
    antecedents: List[Predicate]  # Conditions that must be true
    consequent: Predicate          # Conclusion if antecedents are true
    variables: Set[str]            # Quantified variables (∀x, y, z)
    description: str
    priority: int = 0              # For conflict resolution
    
    def __str__(self):
        vars_str = ", ".join(self.variables) if self.variables else ""
        ant_str = " ∧ ".join(str(ant) for ant in self.antecedents)
        return f"∀{vars_str} ({ant_str} → {self.consequent})"


class FOLKnowledgeBase:
    """
    First-Order Logic Knowledge Base for Insurance Claims
    
    Contains:
    1. Domain predicates (vocabulary)
    2. Facts (ground predicates - no variables)
    3. Rules (Horn clauses with quantifiers)
    """
    
    def __init__(self):
        self.facts: Set[Predicate] = set()
        self.rules: List[Rule] = []
        self.predicate_definitions = {}
        self._initialize_predicates()
    
    def _initialize_predicates(self):
        """
        Define the vocabulary of predicates used in the domain
        
        Predicates represent relationships and properties in FOL
        """
        self.predicate_definitions = {
            # Policy Predicates
            'PolicyType': 'PolicyType(policy, type) - The type of insurance policy',
            'PolicyPeriod': 'PolicyPeriod(policy, start_date, end_date) - Policy validity period',
            'PolicyActive': 'PolicyActive(policy, date) - Policy is active on given date',
            'SumInsured': 'SumInsured(policy, amount) - Maximum coverage amount',
            'Deductible': 'Deductible(policy, amount) - Policy excess amount',
            
            # Loss/Claim Predicates
            'LossOccurred': 'LossOccurred(claim, date, type) - Loss event occurred',
            'LossType': 'LossType(claim, type) - Type of loss (accident, theft, etc.)',
            'ClaimAmount': 'ClaimAmount(claim, amount) - Amount claimed',
            'ClaimOnPolicy': 'ClaimOnPolicy(claim, policy) - Claim is against this policy',
            
            # Coverage Predicates
            'Covers': 'Covers(policy_type, loss_type) - Policy type covers loss type',
            'CoverageApplies': 'CoverageApplies(claim) - Claim is covered',
            'NotCovered': 'NotCovered(claim) - Claim is not covered',
            
            # Document Predicates
            'FIRSubmitted': 'FIRSubmitted(claim) - Police FIR has been submitted',
            'FIRRequired': 'FIRRequired(loss_type) - FIR is mandatory for this loss type',
            'DocumentsComplete': 'DocumentsComplete(claim) - All documents submitted',
            
            # Risk Predicates
            'PreviousClaims': 'PreviousClaims(policy, count) - Number of previous claims',
            'FraudRisk': 'FraudRisk(claim, level) - Fraud risk level (low/medium/high)',
            'HighRisk': 'HighRisk(claim) - Claim has high fraud risk',
            
            # Temporal Predicates
            'DateInRange': 'DateInRange(date, start, end) - Date falls within range',
            'DateBefore': 'DateBefore(date1, date2) - date1 is before date2',
            'DateAfter': 'DateAfter(date1, date2) - date1 is after date2',
            
            # Validity Predicates
            'ValidClaim': 'ValidClaim(claim) - Claim is valid',
            'InvalidClaim': 'InvalidClaim(claim) - Claim is invalid',
            
            # Decision Predicates
            'Approved': 'Approved(claim) - Claim is approved',
            'Rejected': 'Rejected(claim) - Claim is rejected',
            'UnderInvestigation': 'UnderInvestigation(claim) - Claim needs investigation',
            
            # Amount Predicates
            'AdmissibleLoss': 'AdmissibleLoss(claim, amount) - Maximum payable amount',
            'PayableAmount': 'PayableAmount(claim, amount) - Final payout amount',
        }
    
    def add_fact(self, predicate: Predicate):
        """Add a ground fact to the knowledge base"""
        self.facts.add(predicate)
    
    def add_rule(self, rule: Rule):
        """Add a new rule to the knowledge base"""
        self.rules.append(rule)
        # Sort rules by priority (higher priority first)
        self.rules.sort(key=lambda r: r.priority, reverse=True)
    
    def get_rules_by_consequent(self, predicate_name: str) -> List[Rule]:
        """Get all rules that can derive a specific predicate"""
        return [rule for rule in self.rules if rule.consequent.name == predicate_name]
    
    def get_facts_by_predicate(self, predicate_name: str) -> Set[Predicate]:
        """Get all facts matching a predicate name"""
        return {fact for fact in self.facts if fact.name == predicate_name}
    
    def clear_facts(self):
        """Clear all facts (keep rules)"""
        self.facts.clear()
    
    def display_knowledge_base(self) -> str:
        """Generate a human-readable representation of the KB"""
        output = []
        output.append("=" * 80)
        output.append("FIRST-ORDER LOGIC KNOWLEDGE BASE")
        output.append("=" * 80)
        
        output.append("\nPREDICATE DEFINITIONS:")
        output.append("-" * 80)
        for pred_name, definition in self.predicate_definitions.items():
            output.append(f"  {definition}")
        
        output.append("\nRULES (Horn Clauses):")
        output.append("-" * 80)
        for rule in self.rules:
            output.append(f"  [{rule.rule_id}] Priority: {rule.priority}")
            output.append(f"      {rule.description}")
            output.append(f"      {rule}")
            output.append("")
        
        output.append("FACTS (Ground Predicates):")
        output.append("-" * 80)
        if self.facts:
            for fact in sorted(self.facts, key=lambda f: (f.predicate_type.value, f.name)):
                output.append(f"  {fact}")
        else:
            output.append("  (No facts currently in KB)")
        
        output.append("=" * 80)
        return "\n".join(output)
