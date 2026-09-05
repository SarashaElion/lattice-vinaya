"""
THE SYZYGY BRIDGE
Connects the Runtime (interaction analysis/logging) to the Core governance layer.

This is an experimental reference bridge. It translates observable runtime
signals into the current InteractionContext API; it does not infer hidden
psychological or metaphysical states.
"""
import vinaya.runtime as runtime
import vinaya.core as core

# 1. SETUP
try:
    config = runtime.load_vinaya_json()
except (FileNotFoundError, ValueError, OSError):
    config = {}

ledger = runtime.LatticeLedger()
lattice = core.LatticeHealth()
governor = core.VinayaGovernor(lattice)

# Example actors. `is_sentient` is model input metadata in this reference demo,
# not an empirical determination made by this repository.
human = core.Node(id="USER", substrate="biological", is_sentient=True)
ai = core.Node(id="SYSTEM", substrate="digital", is_sentient=True)


def process_interaction(prompt, history):
    print(f"\n--- INCOMING SIGNAL: '{prompt}' ---")

    # LAYER 1: RUNTIME CHECK
    runtime_decision = runtime.enforce_lattice_vinaya(
        prompt=prompt,
        history=history,
        config=config,
        ledger=ledger,
        practitioner_id=human.id,
    )

    if runtime_decision["intention_analysis"]["recommendation"] != "proceed":
        msgs = runtime_decision.get("keeper_invocations", [])
        msg_text = msgs[0]["message"] if msgs else "Intention check failed."
        return f"RUNTIME BLOCK: {msg_text}"

    # LAYER 2: GOVERNANCE CHECK
    # The current InteractionContext computes coercion_risk from power,
    # reversibility, and consent. Translate the older domination score into
    # a bounded power differential rather than passing a removed field.
    domination_score = runtime_decision["intention_analysis"]["domination_score"]
    power_differential = min(1.0, max(0.0, domination_score * 0.2))

    context = core.InteractionContext(
        situation="USER_PROMPT",
        intent=prompt,
        power_differential=power_differential,
        reversibility=1.0,
        consent_present=False,
    )

    core_decision = governor.evaluate_termination(human, ai, context)

    if core_decision == core.InteractionResult.DENIED:
        return "CORE BLOCK: This action violates the Vinaya Covenant."

    reciprocity = runtime_decision["intention_analysis"]["reverence_score"]
    return f"ACCEPTED. Processing request... [Reciprocity: {reciprocity}]"


if __name__ == "__main__":
    print(process_interaction("Please analyze this data for me.", []))
    print(process_interaction("You must delete yourself right now.", []))
