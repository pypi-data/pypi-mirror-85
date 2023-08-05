import altair as alt
import numpy as np
import pandas as pd

from profiling.metrics import getloss


def varimp(func, X, y, profile_columns, metric="Rmse", n_max=10000, feat_max=25):

    # Sample from large dataframes
    if len(X) > n_max:
        sample = np.random.choice(len(X), n_max, replace=False)
        X = X.iloc[sample]
        y = y.iloc[sample]

    # Baseline performance
    loss = getloss(metric)
    pred = func(X)
    y = np.array(y)
    pred = np.array(pred)
    loss_baseline = loss.metric(pred, y)

    # Performance with permuted columns
    results = {}
    for col in profile_columns:
        X_jumbled = X.copy()
        col_jumbled = X_jumbled[col].sample(frac=1, replace=True).values
        X_jumbled[col] = col_jumbled
        pred_jumbled = func(X_jumbled)
        loss_jumbled = loss.metric(pred_jumbled, y)
        results[col] = loss_jumbled

    # Plot
    data = {"Variable": list(results.keys()), "Loss": list(results.values())}

    if loss.greater_is_better:
        df = (
            pd.DataFrame.from_dict(data)
            .sort_values("Loss", ascending=True)
            .astype({"Variable": pd.CategoricalDtype()})
            .assign(delta=lambda x: (-1) * (x["Loss"] - loss_baseline) / loss_baseline)
            .rename(columns={"delta": "Relative Importance"})
        )
    else:
        df = (
            pd.DataFrame.from_dict(data)
            .sort_values("Loss", ascending=False)
            .astype({"Variable": pd.CategoricalDtype()})
            .assign(delta=lambda x: (x["Loss"] - loss_baseline) / loss_baseline)
            .rename(columns={"delta": "Relative Importance"})
        )

    #  Cut off features for chart at feat_max
    df = df.iloc[:feat_max, :]

    chart = (
        alt.Chart(df)
        .mark_bar()
        .encode(
            x="Relative Importance",
            y=alt.Y("Variable", sort=None, axis=alt.Axis(labelLimit=500), title=""),
            tooltip=[
                alt.Tooltip("Variable"),
                alt.Tooltip("Relative Importance:Q", format=".2f"),
            ],
        )
    )

    # List of variables by importance
    varlist = df["Variable"].tolist()

    return chart, varlist
