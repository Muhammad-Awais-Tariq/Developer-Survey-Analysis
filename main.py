import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
from io import BytesIO

def get_required_info(raw_data):
    required_coloumns = [
        'Country', 'Age', 'Gender', 'EdLevel', 'UndergradMajor', 'Hobbyist',
        'Age1stCode', 'YearsCode', 'YearsCodePro', 'LanguageWorkedWith',
        'LanguageDesireNextYear', 'NEWLearn', 'NEWStuck', 'Employment', 'DevType',
        'WorkWeekHrs', 'JobSat', 'JobFactors', 'NEWOvertime', 'NEWEdImpt'
    ]
    return raw_data[required_coloumns].copy()

def convert_numeric(df, coloumn):
    df[coloumn] = pd.to_numeric(df[coloumn], errors="coerce")

def drop_incorrect(df, coloumn, max=1000000, min=0):
    df.drop(df[df[coloumn] > max].index, inplace=True)
    df.drop(df[df[coloumn] < min].index, inplace=True)

def replace_multiselect(df, coloumn):
    df.where(~(df[coloumn].str.contains(";", na=False)), np.nan, inplace=True)

def split_multicolumn(series):
    results_df = pd.DataFrame(index=series.index)
    options = []
    for idx, value in series.dropna().items():
        for option in value.split(";"):
            option = option.strip()
            if option not in results_df.columns:
                results_df[option] = False
                options.append(option)
            results_df.loc[idx, option] = True
    return results_df[options]

def save_fig(fig):
    """
    This methood is to save image in the buffer and then return as the png so to avoid clipping
    """
    buf = BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", dpi=120, facecolor="white")
    buf.seek(0)
    plt.close(fig)
    return buf

def plot_hbar(df, coloumn, title):
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.countplot(y=df[coloumn], ax=ax, order=df[coloumn].value_counts().index, color="steelblue")
    ax.set_title(title, fontsize=14, color="black")
    ax.set_xlabel("Count", color="black")
    ax.set_ylabel("", color="black")
    ax.tick_params(colors="black")
    plt.tight_layout()
    return save_fig(fig)

def plot_bar(df, coloumn, title, total_num=10):
    top_values = df[coloumn].value_counts().head(total_num)
    fig, ax = plt.subplots(figsize=(14, 6))
    sns.barplot(x=top_values.index, y=top_values, ax=ax, color="steelblue")
    ax.set_title(title, fontsize=14, color="black")
    ax.set_ylabel("Count", color="black")
    ax.set_xlabel("", color="black")
    ax.tick_params(colors="black")
    plt.xticks(rotation=75, ha="right")
    plt.tight_layout()
    return save_fig(fig)

def plot_hist(df, coloumn, title):
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.histplot(data=df[coloumn], bins=np.arange(10, 80, 5), color="purple", ax=ax)
    ax.set_title(title, fontsize=14, color="black")
    ax.set_xlabel(coloumn, color="black")
    ax.set_ylabel("Count", color="black")
    ax.tick_params(colors="black")
    plt.tight_layout()
    return save_fig(fig)

def plot_pie(values, labels, title):
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(values, labels=labels, autopct="%1.1f%%", startangle=180)
    ax.set_title(title, fontsize=14, color="black")
    plt.tight_layout()
    return save_fig(fig)

def plot_barh(data, title):
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x=data.values, y=data.index, ax=ax, color="steelblue")
    ax.set_title(title, fontsize=14, color="black")
    ax.set_xlabel("Avg Hours / Week", color="black")
    ax.set_ylabel("", color="black")
    ax.tick_params(colors="black")
    plt.tight_layout()
    return save_fig(fig)