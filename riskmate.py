#!/usr/bin/env python3
# RiskMate - Forex Risk & Lot Size Calculator (CLI)
# Author: (your name)
# Usage: python riskmate.py

from dataclasses import dataclass

@dataclass
class PairSpec:
    name: str
    pip_size: float         # price change for 1 pip
    pip_value_per_lot: float # USD per pip for 1.00 lot (standard lot)

# Common simplified specs (good enough for a portfolio mini project)
PAIR_SPECS = {
    "EURUSD": PairSpec("EURUSD", pip_size=0.0001, pip_value_per_lot=10.0),
    "GBPUSD": PairSpec("GBPUSD", pip_size=0.0001, pip_value_per_lot=10.0),
    "AUDUSD": PairSpec("AUDUSD", pip_size=0.0001, pip_value_per_lot=10.0),
    "USDCHF": PairSpec("USDCHF", pip_size=0.0001, pip_value_per_lot=10.0),
    "USDCAD": PairSpec("USDCAD", pip_size=0.0001, pip_value_per_lot=10.0),

    # JPY pairs use 0.01 pip size (simplified)
    "USDJPY": PairSpec("USDJPY", pip_size=0.01, pip_value_per_lot=10.0),
    "EURJPY": PairSpec("EURJPY", pip_size=0.01, pip_value_per_lot=10.0),

    # Gold (very broker-dependent; simplified assumption)
    # We'll treat 0.10 price move as "1 pip" and 1 lot pip value as $1
    "XAUUSD": PairSpec("XAUUSD", pip_size=0.10, pip_value_per_lot=1.0),
}

def ask_float(prompt: str) -> float:
    while True:
        try:
            return float(input(prompt).strip())
        except ValueError:
            print("❌ Sayı girmelisin. Örn: 10000 veya 1.5")

def ask_pair() -> PairSpec:
    print("\nDesteklenen pariteler:")
    print(", ".join(PAIR_SPECS.keys()))
    pair = input("Pair (örn EURUSD / XAUUSD): ").strip().upper()
    if pair in PAIR_SPECS:
        return PAIR_SPECS[pair]

    print("\n⚠️ Bu parite listede yok. Manuel girme moduna geçiyoruz.")
    pip_size = ask_float("Pip size (örn EURUSD için 0.0001, USDJPY için 0.01): ")
    pip_value = ask_float("1.00 lot için pip value (USD) (örn majors ~10): ")
    return PairSpec(pair, pip_size=pip_size, pip_value_per_lot=pip_value)

def calc_lot_size(risk_usd: float, stop_pips: float, pip_value_per_lot: float) -> float:
    # risk = stop_pips * pip_value_per_lot * lots
    if stop_pips <= 0 or pip_value_per_lot <= 0:
        return 0.0
    return risk_usd / (stop_pips * pip_value_per_lot)

def main():
    print("=== RiskMate | Forex Risk & Lot Size Calculator ===")

    balance = ask_float("Account balance (USD): ")
    risk_percent = ask_float("Risk % (örn 1): ")

    spec = ask_pair()

    entry = ask_float("Entry price: ")
    stop = ask_float("Stop loss price: ")

    risk_usd = balance * (risk_percent / 100.0)
    stop_distance_price = abs(entry - stop)
    stop_pips = stop_distance_price / spec.pip_size

    lots = calc_lot_size(risk_usd, stop_pips, spec.pip_value_per_lot)

    # Optional: TP levels for 1R/2R/3R
    direction = "LONG" if stop < entry else "SHORT"
    r1 = entry + (entry - stop) if direction == "LONG" else entry - (stop - entry)
    r2 = entry + 2*(entry - stop) if direction == "LONG" else entry - 2*(stop - entry)
    r3 = entry + 3*(entry - stop) if direction == "LONG" else entry - 3*(stop - entry)

    print("\n--- Sonuç ---")
    print(f"Pair: {spec.name}")
    print(f"Direction: {direction}")
    print(f"Risk Amount: ${risk_usd:.2f}")
    print(f"Stop Distance: {stop_pips:.1f} pips")
    print(f"Suggested Lot Size: {lots:.3f} lots")

    print("\nTP levels (R-multiple):")
    print(f"  1R: {r1:.5f}" if spec.pip_size < 0.01 else f"  1R: {r1:.2f}")
    print(f"  2R: {r2:.5f}" if spec.pip_size < 0.01 else f"  2R: {r2:.2f}")
    print(f"  3R: {r3:.5f}" if spec.pip_size < 0.01 else f"  3R: {r3:.2f}")

    print("\n✅ LinkedIn Featured için öneri: repo + README screenshot ekle.")

if __name__ == "__main__":
    main()
