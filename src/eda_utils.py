import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List

# Premium Modern Theme setup
PALETTE = {
    'primary': '#1E3A8A',     # Sleek Royal Blue
    'secondary': '#0D9488',   # Teal
    'accent': '#E11D48',      # Rose Red
    'background': '#F8FAFC',  # Cool Gray light bg
    'grid': '#E2E8F0',        # Soft grid border
    'text': '#334155',        # Deep charcoal
    'coral': '#F97316',       # Warm Coral
    'purple': '#7C3AED'       # Royal Purple
}


def apply_modern_theme():
    """
    Applies custom styling to matplotlib for a modern, sleek aesthetic.
    """
    sns.set_theme(style="white")
    plt.rcParams.update({
        'figure.facecolor': '#FFFFFF',
        'axes.facecolor': '#FFFFFF',
        'axes.edgecolor': PALETTE['grid'],
        'axes.grid': True,
        'grid.color': PALETTE['grid'],
        'grid.linestyle': '--',
        'grid.alpha': 0.7,
        'axes.labelcolor': PALETTE['text'],
        'xtick.color': PALETTE['text'],
        'ytick.color': PALETTE['text'],
        'font.family': 'sans-serif',
        'text.color': PALETTE['text'],
        'figure.autolayout': True
    })


def plot_univariate_distributions(df: pd.DataFrame, num_cols: List[str], figsize=(15, 5)):
    """
    Plots histograms with KDE for numerical features.
    """
    apply_modern_theme()
    fig, axes = plt.subplots(1, len(num_cols), figsize=figsize)
    if len(num_cols) == 1:
        axes = [axes]

    for idx, col in enumerate(num_cols):
        ax = axes[idx]
        sns.histplot(df[col], kde=True, color=PALETTE['primary'], ax=ax, bins=30, edgecolor='white')
        ax.set_title(f'Distribution of {col}', fontsize=12, fontweight='bold', color=PALETTE['primary'])
        ax.set_xlabel(col, fontsize=10)
        ax.set_ylabel('Frequency', fontsize=10)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

    return fig


def plot_categorical_distributions(df: pd.DataFrame, cat_cols: List[str], figsize=(15, 6)):
    """
    Plots horizontal bar charts for categorical columns showing frequencies.
    """
    apply_modern_theme()
    fig, axes = plt.subplots(1, len(cat_cols), figsize=figsize)
    if len(cat_cols) == 1:
        axes = [axes]

    for idx, col in enumerate(cat_cols):
        ax = axes[idx]
        top_cats = df[col].value_counts().head(10)
        sns.barplot(x=top_cats.values, y=top_cats.index, ax=ax, palette="viridis", edgecolor='none')
        ax.set_title(f'Top 10 {col} Frequencies', fontsize=12, fontweight='bold', color=PALETTE['primary'])
        ax.set_xlabel('Count', fontsize=10)
        ax.set_ylabel(col, fontsize=10)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

    return fig


def plot_outliers(df: pd.DataFrame, cols: List[str], figsize=(12, 6)):
    """
    Plots box plots for numerical columns to identify outliers.
    """
    apply_modern_theme()
    fig, axes = plt.subplots(1, len(cols), figsize=figsize)
    if len(cols) == 1:
        axes = [axes]

    for idx, col in enumerate(cols):
        ax = axes[idx]
        sns.boxplot(y=df[col], ax=ax, color=PALETTE['secondary'], width=0.4)
        ax.set_title(f'Outliers in {col}', fontsize=12, fontweight='bold', color=PALETTE['primary'])
        ax.set_ylabel(col, fontsize=10)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

    return fig


def plot_premium_vs_claims_scatter(df: pd.DataFrame, sample_size: int = 5000):
    """
    Plots scatter plot of TotalPremium vs TotalClaims.
    """
    apply_modern_theme()
    fig, ax = plt.subplots(figsize=(10, 6))

    # Take a sample if dataset is too large to prevent visual overcrowding
    df_sample = df.sample(min(sample_size, len(df)), random_state=42)

    sns.scatterplot(
        data=df_sample, x='TotalPremium', y='TotalClaims',
        alpha=0.6, color=PALETTE['accent'], edgecolor='none', ax=ax
    )

    ax.set_title(
        'Bivariate Relationship: Total Premium vs Total Claims',
        fontsize=14, fontweight='bold', color=PALETTE['primary']
    )
    ax.set_xlabel('Total Premium', fontsize=11)
    ax.set_ylabel('Total Claims', fontsize=11)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    return fig


def plot_correlation_matrix(df: pd.DataFrame, num_cols: List[str], figsize=(10, 8)):
    """
    Computes and plots the correlation matrix of numeric columns.
    """
    apply_modern_theme()
    fig, ax = plt.subplots(figsize=figsize)

    corr = df[num_cols].corr()

    mask = np.triu(np.ones_like(corr, dtype=bool))

    sns.heatmap(
        corr, mask=mask, annot=True, fmt=".2f", cmap="coolwarm",
        vmin=-1, vmax=1, center=0, square=True, linewidths=.5,
        cbar_kws={"shrink": .8}, ax=ax
    )

    ax.set_title(
        'Correlation Matrix of Key Numerical Variables',
        fontsize=14, fontweight='bold', color=PALETTE['primary']
    )
    return fig


def plot_loss_ratio_by_category(df: pd.DataFrame, cat_col: str, title: str, top_n: int = 10, figsize=(10, 6)):
    """
    Plots the average Loss Ratio across different categories.
    """
    apply_modern_theme()
    fig, ax = plt.subplots(figsize=figsize)

    # Calculate average loss ratio and record count
    lr_data = df.groupby(cat_col).agg(
        Average_LossRatio=('LossRatio', 'mean'),
        Count=('LossRatio', 'count')
    ).reset_index()

    # Filter to categories with meaningful size and get top N
    lr_data = lr_data.sort_values(by='Average_LossRatio', ascending=False).head(top_n)

    sns.barplot(
        data=lr_data, x='Average_LossRatio', y=cat_col,
        palette="coolwarm", ax=ax, edgecolor='none'
    )

    ax.set_title(title, fontsize=14, fontweight='bold', color=PALETTE['primary'])
    ax.set_xlabel('Average Loss Ratio (Claims / Premium)', fontsize=11)
    ax.set_ylabel(cat_col, fontsize=11)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    return fig
