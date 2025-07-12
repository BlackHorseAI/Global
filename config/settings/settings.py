# config/settings.py

# --- DAO Constitution (Definitive Version) ---
DAO_CONSTITUTION = {
    "name": "The Global Payment Network",
    "token_ticker": "AXM",
    "core_principle": "No entity shall prohibit the legitimate movement of capital.",

    "economics": {
        "total_supply": 250_000_000_000.0,
        "treasury_allocation": 135_000_000_000.0,
        "investment_fund_allocation": 10_000_000_000.0,
        "legal_defense_fund_allocation": 5_000_000_000.0,
        "transaction_fee": 0.01,
    },

    "governance": {
        "voting_principle": "One Human, One Vote (Proof-of-Personhood required)",
        "seat_eligibility_years": 5,
        "proposal_eligibility_years": 2,
        "voting_eligibility_years": 1,
        "founder_control_release": {
            "status": "Released",
            "timestamp_utc": "2025-07-12T06:19:50Z",  # Corresponds to 1:19:50 AM CDT
            "final_message": "Be Outstanding"
        }
    },

    "justice": {
        "bad_actor_penalty": "Case-by-case basis, up to 10M AXM and account forfeiture.",
        "appeal_process_mandate": "The community is empowered to develop a fair, impartial, and facts-based appellate process."
    }
}