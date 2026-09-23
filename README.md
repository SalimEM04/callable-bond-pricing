# Callable Bond Pricing & Risk Management

A Python project for pricing and analyzing the interest-rate risk of a callable fixed-rate bond using a one-factor Hull–White model and a calibrated trinomial tree.

The project focuses on the impact of the embedded issuer call option on bond valuation, duration, DV01, convexity, and volatility exposure.

---

## Project Overview

A callable bond can be interpreted as a straight bond combined with an embedded option sold by the investor to the issuer:

**Callable Bond = Straight Bond − Issuer Call Option**

When interest rates decline, the issuer has an incentive to redeem the bond early and refinance at a lower rate. This limits the investor's upside and makes the bond's interest-rate exposure state-dependent.

This project develops a framework to model this behavior using a one-factor Hull–White short-rate model.

---

## Bond Structure

The instrument considered is a fixed-rate callable bond with:

- **Face value:** 100
- **Maturity:** 5 years
- **Annual coupon rate:** 5%
- **Call protection:** 2 years
- **Call dates:** 2Y, 3Y and 4Y
- **Call price:** 100
- **Call convention:** call dates coincide with coupon payment dates

The structure can therefore be described as a **5Y NC2 callable bond**, callable annually at par after the non-call period.

---

## Methodology

The pricing framework follows five main steps:

1. Construct an illustrative zero-coupon yield curve.
2. Model short-rate dynamics using the one-factor Hull–White model.
3. Build a recombining trinomial interest-rate tree.
4. Calibrate the tree to the initial term structure using Arrow-Debreu state prices.
5. Price the straight and callable bonds by backward induction.

At each call date, the callable bond value is determined by the lower of the continuation value and the contractual call price, with the coupon payment added according to the model convention:

**Callable Bond Value = Coupon + min(Continuation Value, Call Price)**

The issuer exercises the call whenever the continuation value of the bond exceeds the call price.

---

## Key Results

Under the base-case assumptions:

| Metric | Straight Bond | Callable Bond |
|---|---:|---:|
| Price | 106.68 | 103.63 |
| Effective Duration | 4.56 | 2.59 |
| DV01 | 0.0486 | 0.0268 |
| Effective Convexity | 21.92 | 8.06 |

The value of the embedded issuer call is approximately:

**Embedded Call Value = Straight Bond Value − Callable Bond Value = 3.05**

The call feature therefore materially reduces both the value and the interest-rate sensitivity of the bond.

---

## Interest-Rate Sensitivity

![Rate Sensitivity](figures/rate_sensitivity.png)

The callable bond exhibits lower sensitivity to declining interest rates than the equivalent straight bond.

As rates fall, the probability of early redemption increases. The expected maturity of the callable bond shortens and its price appreciation becomes progressively constrained by the issuer's call option.

The embedded option therefore creates a state-dependent duration and convexity profile.

In the base scenario, effective duration decreases from **4.56** for the straight bond to **2.59** for the callable bond, while DV01 decreases from **0.0486** to **0.0268**.

---

## Convexity

The embedded call option significantly modifies the convexity profile of the bond.

The straight bond has an effective convexity of approximately **21.92**, compared with **8.06** for the callable bond.

The callable bond therefore retains positive convexity around the current market scenario, but substantially less than the equivalent straight bond.

When interest rates decline, the probability of early redemption increases. This limits the price appreciation of the callable bond and progressively reduces its convexity.

A callable bond does not necessarily exhibit negative convexity in every interest-rate environment. Its convexity depends on the level of interest rates, the call schedule, volatility, and the proximity to the exercise boundary.

---

## Volatility Sensitivity

![Volatility Sensitivity](figures/volatility_sensitivity.png)

Higher short-rate volatility increases the value of the issuer's embedded call option.

In the model, increasing the Hull–White volatility parameter from **0.5% to 3.0%** increases the embedded call value from approximately **2.58 to 5.52**, while the callable bond value decreases from approximately **104.10 to 101.16**.

This relationship follows directly from the investor's position:

**Long Callable Bond = Long Straight Bond − Long Issuer Call**

The investor is therefore short the embedded optionality.

The volatility sensitivity presented here should be interpreted as sensitivity to the **Hull–White short-rate volatility parameter**, rather than as a market-quoted option vega.

---

## Trading & Risk Management Interpretation

From a trading perspective, a callable bond cannot be managed using only the duration of an equivalent straight bond.

A first-order interest-rate hedge can be constructed using government bonds or interest-rate swaps to offset DV01. However, the hedge is inherently dynamic because the probability of exercise changes as interest rates move.

When rates decline, the call option becomes more relevant and the expected maturity of the callable bond shortens. When rates rise, the call becomes less relevant and the callable bond increasingly behaves like a straight bond.

The position also contains convexity and volatility exposure generated by the embedded call option. Interest-rate options such as swaptions can therefore be used to manage part of this optionality risk.

The overall risk profile can be summarized as:

**Interest-Rate Risk + Convexity Risk + Volatility Risk**

Managing a callable bond therefore requires dynamic risk management as market conditions and exercise probabilities evolve.

---

## Repository Structure

```text
callable-bond-pricing/
│
├── notebooks/
│   └── callable_bond_pricing.ipynb
│
├── src/
│   ├── hull_white.py
│   └── callable_bond.py
│
├── figures/
│   ├── rate_sensitivity.png
│   └── volatility_sensitivity.png
│
├── README.md
├── requirements.txt
└── .gitignore
```

The full analysis, mathematical derivations, Python implementation, numerical results, and financial interpretation are available in the Jupyter notebook:

[Open the full notebook](notebooks/callable_bond_pricing.ipynb)

---

## Model Limitations

This project is designed to capture the main economic mechanisms of callable bond pricing and risk management rather than reproduce a production-level pricing library.

The interest-rate dynamics are represented using a simplified one-factor Hull–White trinomial tree calibrated to an illustrative zero-coupon curve.

The Hull–White mean-reversion and volatility parameters are treated as model inputs rather than being calibrated to a market surface of interest-rate options.

The callable bond is modeled as a five-year fixed-rate bond with two years of call protection, followed by annual call opportunities at par on coupon payment dates. This simplified structure avoids additional contractual features such as irregular call schedules, accrued-interest conventions, detailed day-count conventions, settlement rules, and business-day adjustments.

In a production environment, the initial yield curve would typically be constructed from liquid market instruments, while the Hull–White parameters would be calibrated to market prices or implied volatilities of interest-rate derivatives such as swaptions.

Additional factors such as issuer credit risk, liquidity, transaction costs, and funding considerations would also need to be incorporated for a complete market valuation.

---

## Technologies

- Python
- NumPy
- Pandas
- SciPy
- Matplotlib
- Jupyter Notebook

---

## How to Run

Clone the repository and install the required dependencies:

```bash
pip install -r requirements.txt
```

Then open:

```text
notebooks/callable_bond_pricing.ipynb
```

and run the notebook from top to bottom.