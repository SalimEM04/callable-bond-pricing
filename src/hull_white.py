import numpy as np


def build_hull_white_tree(
    zero_curve_spline,
    maturity,
    a,
    sigma,
    dt
):
    """
    Build a calibrated Hull-White trinomial short-rate tree.

    Parameters
    ----------
    zero_curve_spline : CubicSpline
        Smooth zero-rate curve.
    maturity : float
        Final maturity of the tree.
    a : float
        Mean-reversion parameter.
    sigma : float
        Short-rate volatility.
    dt : float
        Time step of the tree.

    Returns
    -------
    hw_times : ndarray
        Time grid.
    x_tree : list
        Stochastic Hull-White state tree.
    rate_tree : list
        Calibrated short-rate tree.
    transition_probabilities : list
        Trinomial transition probabilities.
    market_discount_factors : ndarray
        Discount factors reproduced by the tree.
    """

    n_steps = int(maturity / dt)

    hw_times = np.arange(n_steps + 1) * dt

    # Market discount factors implied by the input zero curve
    zero_rates_grid = zero_curve_spline(hw_times)

    market_discount_factors = np.exp(
        -zero_rates_grid * hw_times
    )

    # Spacing between stochastic states
    dx = sigma * np.sqrt(3 * dt)

    # Build stochastic state tree
    x_tree = []

    for i in range(n_steps + 1):

        states = []

        for j in range(-i, i + 1):
            states.append(j * dx)

        x_tree.append(states)

    # Compute trinomial transition probabilities
    transition_probabilities = []

    for i in range(n_steps):

        probabilities = []

        for j in range(-i, i + 1):

            x = j * dx

            m = -a * x * dt / dx

            p_up = 1 / 6 + 0.5 * (m**2 + m)
            p_middle = 2 / 3 - m**2
            p_down = 1 / 6 + 0.5 * (m**2 - m)

            probabilities.append(
                (p_down, p_middle, p_up)
            )

        transition_probabilities.append(
            probabilities
        )

    # Arrow-Debreu state prices
    state_prices = [
        np.array([1.0])
    ]

    alpha = []

    # Calibrate each time slice to the initial yield curve
    for i in range(n_steps):

        current_state_prices = state_prices[i]

        x_states = np.array(
            x_tree[i]
        )

        numerator = np.sum(
            current_state_prices
            * np.exp(-x_states * dt)
        )

        alpha_i = (
            np.log(
                numerator
                / market_discount_factors[i + 1]
            )
            / dt
        )

        alpha.append(alpha_i)

        next_state_prices = np.zeros(
            2 * (i + 1) + 1
        )

        for position in range(
            len(x_tree[i])
        ):

            x = x_tree[i][position]

            short_rate = x + alpha_i

            discount = np.exp(
                -short_rate * dt
            )

            (
                p_down,
                p_middle,
                p_up
            ) = transition_probabilities[i][position]

            next_state_prices[position] += (
                current_state_prices[position]
                * discount
                * p_down
            )

            next_state_prices[position + 1] += (
                current_state_prices[position]
                * discount
                * p_middle
            )

            next_state_prices[position + 2] += (
                current_state_prices[position]
                * discount
                * p_up
            )

        state_prices.append(
            next_state_prices
        )

    # Construct calibrated short-rate tree
    rate_tree = []

    for i in range(n_steps):

        rates = []

        for x in x_tree[i]:
            rates.append(
                x + alpha[i]
            )

        rate_tree.append(rates)

    return (
        hw_times,
        x_tree,
        rate_tree,
        transition_probabilities,
        market_discount_factors
    )