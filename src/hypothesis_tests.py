import pandas as pd
from scipy import stats


def run_t_test(df: pd.DataFrame, group_col: str, value_col: str):
    """
    Performs a two-sample t-test on a numerical variable between two groups.
    """
    groups = df[group_col].unique()
    if len(groups) != 2:
        raise ValueError("Group column must contain exactly 2 unique values for a t-test.")

    group1_vals = df[df[group_col] == groups[0]][value_col].dropna()
    group2_vals = df[df[group_col] == groups[1]][value_col].dropna()

    t_stat, p_val = stats.ttest_ind(group1_vals, group2_vals, equal_var=False)

    return {
        'test_statistic': t_stat,
        'p_value': p_val,
        'group1_mean': group1_vals.mean(),
        'group2_mean': group2_vals.mean()
    }


def run_chi_square_test(df: pd.DataFrame, col1: str, col2: str):
    """
    Performs a Chi-Square test of independence between two categorical variables.
    """
    contingency_table = pd.crosstab(df[col1], df[col2])
    chi2, p, dof, expected = stats.chi2_contingency(contingency_table)

    return {
        'chi2_statistic': chi2,
        'p_value': p,
        'dof': dof
    }
