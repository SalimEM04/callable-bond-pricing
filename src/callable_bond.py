import numpy as np


def price_bonds_from_tree(
    rate_tree,
    transition_probabilities,
    times,
    notional,
    coupon_rate,
    call_dates,
    call_price,
    dt
):
    """
    Price a straight bond and a callable bond
    using backward induction on a Hull-White tree.

    Parameters
    ----------
    rate_tree : list
        Calibrated Hull-White short-rate tree.
    transition_probabilities : list
        Trinomial transition probabilities.
    times : ndarray
        Time grid of the tree.
    notional : float
        Bond face value.
    coupon_rate : float
        Annual coupon rate.
    call_dates : list
        Dates at which the issuer can call the bond.
    call_price : float
        Redemption price if the call is exercised.
    dt : float
        Time step.

    Returns
    -------
    straight_price : float
        Price of the equivalent straight bond.
    callable_price : float
        Price of the callable bond.
    """

    n_steps = len(times) - 1

    annual_coupon = (
        notional * coupon_rate
    )

    # Build cash-flow schedule
    cash_flows = np.zeros(
        n_steps + 1
    )

    for i, t in enumerate(times):

        if (
            t > 0
            and np.isclose(
                t % 1.0,
                0.0
            )
        ):
            cash_flows[i] += annual_coupon

    # Principal repayment at maturity
    cash_flows[-1] += notional

    # Terminal values
    number_terminal_nodes = (
        2 * n_steps + 1
    )

    straight_values = np.full(
        number_terminal_nodes,
        cash_flows[-1]
    )

    callable_values = np.full(
        number_terminal_nodes,
        cash_flows[-1]
    )

    # Backward induction through the tree
    for i in range(
        n_steps - 1,
        -1,
        -1
    ):

        number_nodes = len(
            rate_tree[i]
        )

        new_straight_values = np.zeros(
            number_nodes
        )

        new_callable_values = np.zeros(
            number_nodes
        )

        for position in range(
            number_nodes
        ):

            rate = rate_tree[i][position]

            (
                p_down,
                p_middle,
                p_up
            ) = transition_probabilities[i][position]

            # Straight bond continuation value
            straight_continuation = np.exp(
                -rate * dt
            ) * (
                p_down
                * straight_values[position]
                + p_middle
                * straight_values[position + 1]
                + p_up
                * straight_values[position + 2]
            )

            # Callable bond continuation value
            callable_continuation = np.exp(
                -rate * dt
            ) * (
                p_down
                * callable_values[position]
                + p_middle
                * callable_values[position + 1]
                + p_up
                * callable_values[position + 2]
            )

            # Check whether the current date is callable
            is_call_date = any(
                np.isclose(
                    times[i],
                    call_date
                )
                for call_date in call_dates
            )

            if is_call_date:

                # Issuer exercises when continuation value
                # exceeds the contractual call price
                callable_ex_coupon = min(
                    callable_continuation,
                    call_price
                )

            else:

                callable_ex_coupon = (
                    callable_continuation
                )

            # Coupon at the current date is added after
            # the call decision (call dates coincide
            # with coupon payment dates)
            new_straight_values[position] = (
                straight_continuation
                + cash_flows[i]
            )

            new_callable_values[position] = (
                callable_ex_coupon
                + cash_flows[i]
            )

        straight_values = (
            new_straight_values
        )

        callable_values = (
            new_callable_values
        )

    return (
        straight_values[0],
        callable_values[0]
    )