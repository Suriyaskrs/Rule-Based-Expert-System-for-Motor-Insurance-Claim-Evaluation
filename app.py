"""
Streamlit User Interface for
FOL-Based Motor Insurance Claim Evaluation Expert System

This UI demonstrates the complete system:
- Knowledge Representation (FOL)
- Knowledge Base (predicates and rules)
- Inference Engine (forward chaining)
- Reasoning Mechanism (domain logic)
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import io

from motor_insurance_expert_system import (
    MotorInsuranceExpertSystem,
    parse_date,
    parse_boolean
)


def process_csv(uploaded_file) -> pd.DataFrame:
    """Process uploaded CSV file and evaluate all claims"""
    try:
        # Read CSV
        df = pd.read_csv(uploaded_file)
        
        # Validate required columns
        required_columns = [
            'policy_type', 'policy_start_date', 'policy_end_date', 'loss_date',
            'loss_type', 'claim_amount', 'sum_insured', 'deductible',
            'fir_submitted', 'documents_complete', 'previous_claims'
        ]
        
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            st.error(f"Missing required columns: {', '.join(missing_columns)}")
            return None
        
        # Initialize expert system
        expert_system = MotorInsuranceExpertSystem()
        
        # Prepare output columns
        results = []
        
        for idx, row in df.iterrows():
            try:
                # Prepare input data
                input_data = {
                    'policy_type': str(row['policy_type']).strip().lower(),
                    'policy_start_date': parse_date(row['policy_start_date']),
                    'policy_end_date': parse_date(row['policy_end_date']),
                    'loss_date': parse_date(row['loss_date']),
                    'loss_type': str(row['loss_type']).strip().lower(),
                    'claim_amount': float(row['claim_amount']),
                    'sum_insured': float(row['sum_insured']),
                    'deductible': float(row['deductible']),
                    'fir_submitted': parse_boolean(row['fir_submitted']),
                    'documents_complete': parse_boolean(row['documents_complete']),
                    'previous_claims': int(row['previous_claims'])
                }
                
                # Evaluate claim
                result = expert_system.evaluate_claim(input_data)
                results.append(result)
                
            except Exception as e:
                st.warning(f"Error processing row {idx + 1}: {str(e)}")
                # Add a placeholder result for failed rows
                results.append({
                    'claim_validity': 'error',
                    'coverage_status': 'error',
                    'decision': 'error',
                    'payable_amount': 0,
                    'fraud_risk': 'unknown',
                    'explanation': f'Error: {str(e)}'
                })
        
        # Add results to dataframe
        df['claim_validity'] = [r['claim_validity'] for r in results]
        df['coverage_status'] = [r['coverage_status'] for r in results]
        df['claim_decision'] = [r['decision'] for r in results]
        df['payable_amount'] = [r['payable_amount'] for r in results]
        df['fraud_risk'] = [r['fraud_risk'] for r in results]
        df['explanation'] = [r['explanation'] for r in results]
        
        return df
        
    except Exception as e:
        st.error(f"Error processing CSV file: {str(e)}")
        return None


def main():
    """Main Streamlit UI"""
    
    st.set_page_config(
        page_title="FOL Insurance Expert System",
        layout="wide",
        page_icon="🧠"
    )
    
    st.title("🧠 First-Order Logic Expert System")
    st.markdown("**Rule-Based Expert System for Motor Insurance Claim Evaluation**")
    st.markdown("*Using First-Order Logic Knowledge Representation & Forward Chaining Inference*")
    
    st.markdown("---")
    
    # Sidebar
    st.sidebar.header("🔬 System Architecture")
    st.sidebar.info(
        "**Knowledge Representation:**\n"
        "- First-Order Logic (FOL)\n"
        "- Predicates with quantifiers\n"
        "- Horn clauses (rules)\n\n"
        "**Inference Engine:**\n"
        "- Forward chaining\n"
        "- Unification algorithm\n"
        "- Modus ponens reasoning\n\n"
        "**Reasoning Mechanism:**\n"
        "- Domain-specific logic\n"
        "- Fact derivation\n"
        "- Explanation generation"
    )
    
    # Main content tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📝 Claim Evaluation", 
        "📂 Batch Processing", 
        "📚 Knowledge Base", 
        "🔍 System Details"
    ])
    
    # ==================== TAB 1: CLAIM EVALUATION ====================
    with tab1:
        st.header("📝 Single Claim Evaluation")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Policy Information")
            policy_type = st.selectbox(
                "Policy Type",
                ["comprehensive", "third_party"],
                help="Type of motor insurance policy"
            )
            policy_start_date = st.date_input(
                "Policy Start Date",
                value=datetime(2024, 1, 1)
            )
            policy_end_date = st.date_input(
                "Policy End Date",
                value=datetime(2025, 1, 1)
            )
            sum_insured = st.number_input(
                "Sum Insured (₹)",
                min_value=0,
                value=500000,
                step=10000,
                help="Maximum coverage amount"
            )
            deductible = st.number_input(
                "Deductible/Excess (₹)",
                min_value=0,
                value=5000,
                step=1000,
                help="Policy excess to be deducted from claim"
            )
        
        with col2:
            st.subheader("Claim Information")
            loss_date = st.date_input(
                "Loss Date",
                value=datetime(2024, 6, 15),
                help="Date when the loss occurred"
            )
            loss_type = st.selectbox(
                "Loss Type",
                ["accident", "theft", "fire", "own_damage", "third_party_damage"],
                help="Type of loss/damage"
            )
            claim_amount = st.number_input(
                "Claim Amount (₹)",
                min_value=0,
                value=100000,
                step=10000,
                help="Amount being claimed"
            )
            fir_submitted = st.checkbox(
                "FIR Submitted",
                value=False,
                help="Police FIR (mandatory for theft/fire)"
            )
            documents_complete = st.checkbox(
                "All Documents Complete",
                value=True,
                help="All required documents submitted"
            )
            previous_claims = st.number_input(
                "Previous Claims (Last Year)",
                min_value=0,
                value=0,
                step=1,
                help="Number of claims made in the last year"
            )
        
        st.markdown("---")
        
        if st.button("🧠 Evaluate Claim Using FOL Reasoning", type="primary", use_container_width=True):
            # Prepare input
            input_data = {
                'policy_type': policy_type,
                'policy_start_date': datetime.combine(policy_start_date, datetime.min.time()),
                'policy_end_date': datetime.combine(policy_end_date, datetime.min.time()),
                'loss_date': datetime.combine(loss_date, datetime.min.time()),
                'loss_type': loss_type,
                'claim_amount': float(claim_amount),
                'sum_insured': float(sum_insured),
                'deductible': float(deductible),
                'fir_submitted': fir_submitted,
                'documents_complete': documents_complete,
                'previous_claims': int(previous_claims)
            }
            
            # Run expert system
            with st.spinner("Running FOL inference engine..."):
                expert_system = MotorInsuranceExpertSystem()
                result = expert_system.evaluate_claim(input_data)
            
            st.markdown("---")
            st.header("📊 Evaluation Results")
            
            # Display decision with color coding
            decision = result['decision']
            if decision == 'approved':
                st.success(f"**Decision:** {decision.upper()}")
            elif decision == 'rejected':
                st.error(f"**Decision:** {decision.upper()}")
            else:
                st.warning(f"**Decision:** {decision.upper()}")
            
            # Display key metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Claim Validity", result['claim_validity'].upper())
            with col2:
                st.metric("Coverage Status", result['coverage_status'].replace('_', ' ').upper())
            with col3:
                st.metric("Payable Amount", f"₹{result['payable_amount']:,.2f}")
            with col4:
                fraud_color = {'low': '🟢', 'medium': '🟡', 'high': '🔴'}
                risk_level = result['fraud_risk']
                st.metric("Fraud Risk", f"{fraud_color.get(risk_level, '⚪')} {risk_level.upper()}")
            
            # Explanation
            st.subheader("💬 Explanation (Generated from FOL Reasoning)")
            st.info(result['explanation'])
            
            # FOL Inference Trace
            with st.expander("🔬 View FOL Inference Trace (Forward Chaining Process)", expanded=False):
                st.code("\n".join(result['inference_trace']), language="text")
            
            # Knowledge Base View
            with st.expander("📚 View Knowledge Base State", expanded=False):
                kb_display = expert_system.display_knowledge_base()
                st.code(kb_display, language="text")
            
            # Reasoning Summary
            with st.expander("🧠 View Reasoning Summary", expanded=False):
                reasoning_summary = expert_system.display_reasoning_summary()
                st.code(reasoning_summary, language="text")
    
    # ==================== TAB 2: BATCH PROCESSING ====================
    with tab2:
        st.header("📂 Batch Claim Evaluation via CSV")
        
        # Sample CSV download
        st.markdown("**Step 1:** Download the template CSV")
        sample_data = {
            'policy_type': ['comprehensive', 'third_party', 'comprehensive'],
            'policy_start_date': ['2024-01-01', '2024-02-15', '2023-12-01'],
            'policy_end_date': ['2025-01-01', '2025-02-15', '2024-12-01'],
            'loss_date': ['2024-06-15', '2024-07-20', '2024-08-10'],
            'loss_type': ['accident', 'third_party_damage', 'theft'],
            'claim_amount': [150000, 80000, 250000],
            'sum_insured': [500000, 300000, 600000],
            'deductible': [5000, 3000, 10000],
            'fir_submitted': ['yes', 'no', 'yes'],
            'documents_complete': ['yes', 'yes', 'yes'],
            'previous_claims': [1, 0, 3]
        }
        sample_df = pd.DataFrame(sample_data)
        
        csv_buffer = io.StringIO()
        sample_df.to_csv(csv_buffer, index=False)
        st.download_button(
            label="⬇️ Download CSV Template",
            data=csv_buffer.getvalue(),
            file_name="claims_template.csv",
            mime="text/csv"
        )
        
        st.markdown("**Step 2:** Upload your filled CSV file")
        uploaded_file = st.file_uploader("Choose a CSV file", type=['csv'])
        
        if uploaded_file is not None:
            if st.button("🧠 Evaluate All Claims with FOL", type="primary", use_container_width=True):
                with st.spinner("Processing claims using FOL reasoning..."):
                    result_df = process_csv(uploaded_file)
                
                if result_df is not None:
                    st.success(f"✅ Processed {len(result_df)} claims successfully!")
                    
                    st.subheader("📊 Results Summary")
                    
                    # Summary statistics
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        approved = (result_df['claim_decision'] == 'approved').sum()
                        st.metric("Approved", approved, delta=f"{approved/len(result_df)*100:.1f}%")
                    with col2:
                        rejected = (result_df['claim_decision'] == 'rejected').sum()
                        st.metric("Rejected", rejected, delta=f"{rejected/len(result_df)*100:.1f}%")
                    with col3:
                        investigating = (result_df['claim_decision'] == 'under_investigation').sum()
                        st.metric("Under Investigation", investigating)
                    with col4:
                        total_payout = result_df['payable_amount'].sum()
                        st.metric("Total Payout", f"₹{total_payout:,.0f}")
                    
                    # Display results table
                    st.subheader("📋 Detailed Results")
                    
                    # Color code decision column
                    def highlight_decision(row):
                        if row['claim_decision'] == 'approved':
                            return ['background-color: #d4edda; color: black'] * len(row)
                        elif row['claim_decision'] == 'rejected':
                            return ['background-color: #f8d7da; color: black'] * len(row)
                        else:
                            return ['background-color: #fff3cd; color: black'] * len(row)
                    styled_df = result_df.style.apply(highlight_decision, axis=1)
                    st.dataframe(styled_df, use_container_width=True)
                    
                    # Download processed CSV
                    csv_output = io.StringIO()
                    result_df.to_csv(csv_output, index=False)
                    st.download_button(
                        label="⬇️ Download Evaluated Results",
                        data=csv_output.getvalue(),
                        file_name="evaluated_claims.csv",
                        mime="text/csv"
                    )
    
    # ==================== TAB 3: KNOWLEDGE BASE ====================
    with tab3:
        st.header("📚 First-Order Logic Knowledge Base")
        
        st.markdown("""
        This tab displays the complete FOL knowledge base including:
        - **Predicates**: Domain vocabulary
        - **Rules**: Horn clauses with quantifiers
        - **Facts**: Current state (populated after evaluation)
        """)
        
        # Create a fresh expert system to show the KB
        demo_system = MotorInsuranceExpertSystem()
        
        # Show predicate definitions
        st.subheader("🔤 Predicate Definitions")
        st.markdown("*Vocabulary of the domain represented as FOL predicates*")
        
        predicates_text = []
        for pred_name, definition in demo_system.kb.predicate_definitions.items():
            predicates_text.append(f"• **{pred_name}**: {definition}")
        
        st.markdown("\n".join(predicates_text))
        
        st.markdown("---")
        
        # Show rules
        st.subheader("📐 Rules (Horn Clauses)")
        st.markdown("*∀x, y, z... (Antecedent₁ ∧ Antecedent₂ ∧ ... → Consequent)*")
        
        for rule in demo_system.kb.rules:
            with st.expander(f"[{rule.rule_id}] {rule.description} (Priority: {rule.priority})"):
                st.code(str(rule), language="text")
                st.markdown(f"**Variables:** {', '.join(rule.variables)}")
                st.markdown(f"**Antecedents ({len(rule.antecedents)}):**")
                for ant in rule.antecedents:
                    st.markdown(f"  - {ant}")
                st.markdown(f"**Consequent:**")
                st.markdown(f"  - {rule.consequent}")
        
        st.markdown("---")
        
        # Show domain facts
        st.subheader("🌍 Domain Facts")
        st.markdown("*Static facts about the insurance domain*")
        
        domain_facts = [
            f for f in demo_system.kb.facts
        ]
        
        if domain_facts:
            for fact in sorted(domain_facts, key=str):
                st.code(str(fact), language="text")
        else:
            st.info("Domain facts are initialized when evaluating a claim")
    
    # ==================== TAB 4: SYSTEM DETAILS ====================
    with tab4:
        st.header("🔍 System Architecture & Details")
        
        st.subheader("🏗️ Architecture Overview")
        
        architecture_diagram = """
┌───────────────────────────────────────────────────────┐
│                    USER INTERFACE                     │
│                  (streamlit_fol_app.py)               │
└────────────────────┬──────────────────────────────────┘
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
        """
        st.code(architecture_diagram, language="text")
        
        st.markdown("---")
        
        st.subheader("🧩 Component Details")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **1. Knowledge Representation**
            - First-Order Logic (FOL)
            - Predicates: PolicyActive(p, d)
            - Quantifiers: ∀, ∃
            - Connectives: ∧, ∨, →, ¬
            - Horn Clauses: A₁ ∧ A₂ → C
            
            **2. Knowledge Base**
            - 30+ predicate definitions
            - 20 inference rules
            - Domain facts (static)
            - Claim facts (dynamic)
            
            **3. Inference Engine**
            - Forward chaining algorithm
            - Unification for pattern matching
            - Modus ponens reasoning
            - Iterative fact derivation
            """)
        
        with col2:
            st.markdown("""
            **4. Reasoning Mechanism**
            - Claim evaluation logic
            - Decision extraction
            - Amount calculation
            - Explanation generation
            
            **5. User Interface**
            - Manual claim entry
            - Batch CSV processing
            - Interactive knowledge base view
            - Inference trace display
            
            **6. Features**
            - ✅ Explainable AI
            - ✅ Deterministic results
            - ✅ Audit trail
            - ✅ Modular design
            """)
        
        st.markdown("---")
        
        st.subheader("🎯 Key Advantages of FOL Approach")
        
        advantages = """
        1. **Expressive Power**: FOL can represent complex relationships and quantified statements
        2. **Modularity**: Rules can be added/modified independently
        3. **Explainability**: Every inference step is traceable
        4. **Soundness**: Logical inference guarantees valid conclusions
        5. **Flexibility**: Easy to extend domain knowledge
        6. **Transparency**: Complete visibility into reasoning process
        7. **Verification**: Rules can be verified for logical consistency
        8. **Domain Independence**: Same inference engine works for different domains
        """
        st.markdown(advantages)
        
        st.markdown("---")
        
        st.subheader("📖 Example FOL Inference")
        
        st.markdown("""
        **Input Facts:**
        ```
        PolicyType(policy1, comprehensive)
        LossType(claim1, accident)
        ClaimOnPolicy(claim1, policy1)
        ComprehensiveCoverage(accident)
        ```
        
        **Rule R4:**
        ```
        ∀p, c, t (PolicyType(p, comprehensive) ∧ 
                  LossType(c, t) ∧ 
                  ClaimOnPolicy(c, p) ∧ 
                  ComprehensiveCoverage(t) 
                  → CoverageApplies(c))
        ```
        
        **Unification:**
        ```
        Substitution θ = {?p: policy1, ?c: claim1, ?t: accident}
        ```
        
        **Modus Ponens:**
        ```
        All antecedents satisfied under θ
        → Derive: CoverageApplies(claim1)
        ```
        
        **Result:**
        ```
        New fact added to KB: CoverageApplies(claim1)
        ```
        """)
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: gray;'>"
        "First-Order Logic Expert System for Motor Insurance Claim Evaluation<br>"
        "Knowledge Engineering • Forward Chaining • Unification • Modus Ponens"
        "</div>",
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()