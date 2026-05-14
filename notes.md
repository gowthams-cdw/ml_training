# Sentiment Analysis — Full Line-by-Line Explanation
### Explained like you are 5 years old, with zero assumed knowledge

---

> **What does this whole project do?**
> It teaches a computer to read product reviews and decide: is this review **positive** 😊, **neutral** 😐, or **negative** 😠?
> The computer learns this by reading hundreds of thousands of real reviews and slowly figuring out patterns — just like how you learned what "happy" and "sad" mean by seeing people's faces over and over.

---

## Table of Contents

1. [eda.ipynb — Exploring the Data](#1-edaipynb--exploring-the-data)
2. [preprocessing.ipynb — Cleaning the Data](#2-preprocessingipynb--cleaning-the-data)
3. [lstm.ipynb — Building and Training the Brain](#3-lstmipynb--building-and-training-the-brain)
4. [How Everything Connects](#4-how-everything-connects)
5. [Parameters Quick Reference](#5-parameters-quick-reference)

---

# 1. `eda.ipynb` — Exploring the Data

> **EDA** stands for **Exploratory Data Analysis**. Before building anything, you look at your data. Like checking the ingredients before cooking. You want to know: how much data do I have? Is it clean? Is it balanced? What do the reviews look like?

---

### Cell 0 — Installing libraries

```python
!uv add numpy
!uv add pandas
!uv add matplotlib
!uv add seaborn
!uv add wordcloud
```

**What is happening here?**
The `!` at the start means "run this in the terminal, not in Python." `uv add` is a modern package manager (like an app store for Python tools). It downloads and installs each library.

**Why each one?**

| Library | What it is (ELI5) |
|---|---|
| `numpy` | Super fast math helper. Handles big lists of numbers efficiently. |
| `pandas` | Like Excel inside Python. Loads your CSV files and lets you look at rows and columns. |
| `matplotlib` | Draws charts and graphs. The basic drawing tool. |
| `seaborn` | A prettier version of matplotlib. Makes charts look nicer with less code. |
| `wordcloud` | Creates those picture-clouds where big words appear more often. |

---

### Cell 1 — Importing libraries

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
from wordcloud import WordCloud
```

**What is happening here?**
`import` means "load this library so I can use it." The `as np`, `as pd`, etc. are **nicknames** — instead of typing `numpy` every time, you just type `np`. It's like calling your friend "Sam" instead of their full name "Samantha."

- `matplotlib.pyplot` — the part of matplotlib that actually draws charts (`plt` is the nickname)
- `matplotlib.gridspec` — helps arrange multiple charts in a grid layout
- `from wordcloud import WordCloud` — instead of importing the whole library, just grab the `WordCloud` class from it

---

### Cell 2 — Silencing warnings

```python
import warnings
warnings.filterwarnings("ignore")
```

**What is happening here?**
Libraries sometimes print yellow warning messages that aren't actual errors — just reminders about things being slightly outdated. This tells Python to stop showing those. It doesn't hide real errors — just the noisy ones that don't matter.

---

### Cell 3 — Setting folder paths

```python
DATA_PATH   = "./data"
OUTPUT_PATH = "./output"
```

**What is happening here?**
These are just variable names that store folder locations. Instead of typing `"./data"` every time you load a file, you write `DATA_PATH`. If your folder name ever changes, you only need to update it in one place.

`./` means "in the same folder as this notebook."

---

### Cell 4 — Creating the output folder

```python
import os
os.makedirs("./output", exist_ok=True)
```

**What is happening here?**
`os` is a library that lets Python talk to your operating system (Windows/Mac/Linux). `makedirs` creates a folder. `exist_ok=True` means "if the folder already exists, don't crash — just move on." Without this, the code would throw an error if the folder was already there.

---

### Cell 5 — Plot settings

```python
sns.set_style("whitegrid")

plt.rcParams.update({
  "figure.dpi": 150,
  "figure.figsize": (12, 6),
  "axes.spines.right": False,
  "axes.spines.top": False,
  "axes.labelsize": 14,
  "axes.titlesize": 16,
})
```

**What is happening here?**
This is like setting your art preferences before you start drawing.

| Setting | What it does |
|---|---|
| `sns.set_style("whitegrid")` | All charts get a white background with light grid lines. Easier to read. |
| `figure.dpi: 150` | DPI = dots per inch. Higher = sharper, crisper charts. 150 is good quality. |
| `figure.figsize: (12, 6)` | Default chart size: 12 inches wide, 6 inches tall. |
| `axes.spines.right: False` | Remove the right border line from charts. Cleaner look. |
| `axes.spines.top: False` | Remove the top border line from charts. |
| `axes.labelsize: 14` | X and Y axis labels will be font size 14. |
| `axes.titlesize: 16` | Chart titles will be font size 16. |

---

### Cell 6 — Loading the full dataset

```python
df_full = pd.read_csv(f"{DATA_PATH}/sentiment.csv", encoding="latin-1", low_memory=False)
df_full.head(1)
```

**What is happening here?**
`pd.read_csv()` loads a CSV file (a spreadsheet saved as plain text) into a **DataFrame** — which is basically a table you can work with in Python.

| Part | Meaning |
|---|---|
| `f"{DATA_PATH}/sentiment.csv"` | `f"..."` is an f-string — it puts the value of `DATA_PATH` inside the string. Result: `"./data/sentiment.csv"` |
| `encoding="latin-1"` | CSV files have different "languages" for storing special characters (like é, ñ, ü). `latin-1` is the encoding used here. Without it, Python might crash on those characters. |
| `low_memory=False` | Tells pandas to read the whole file before guessing column types, instead of guessing halfway through. Prevents type detection errors. |
| `df_full.head(1)` | Show the first 1 row of the table. Just to see what the data looks like. |

`df` is short for DataFrame — a common convention you'll see everywhere.

---

### Cell 7 — Summarizing the full dataset

```python
summary = pd.DataFrame({
  "data_type": df_full.dtypes,
  "missing_values": df_full.isnull().sum(),
  "n_unique_values": df_full.nunique(),
  "sample": df_full.iloc[0],
})
print(f"{df_full.shape[0]} rows and {df_full.shape[1]} columns in the full dataset.\n")
print(summary)
```

**What is happening here?**
This creates a mini-report table about the dataset. Think of it as running a health check.

| Part | Meaning |
|---|---|
| `df_full.dtypes` | The data type of each column (text, number, date, etc.) |
| `df_full.isnull().sum()` | Count how many values are missing (empty/blank) in each column. Missing = `NaN` (Not a Number). |
| `df_full.nunique()` | How many unique different values are in each column. |
| `df_full.iloc[0]` | The first row of the table, as a sample to look at. `iloc` = "integer location" — get by row number. |
| `df_full.shape[0]` | `.shape` gives you `(rows, columns)`. `[0]` gets the rows count. |
| `df_full.shape[1]` | `[1]` gets the columns count. |

---

### Cells 8–11 — Loading and summarizing the other two datasets

```python
df_equal = pd.read_csv(f"{DATA_PATH}/equal.csv", encoding="latin-1", low_memory=False)
df_ratio = pd.read_csv(f"{DATA_PATH}/ratio.csv", encoding="latin-1", low_memory=False)
```

**Three different datasets, why?**
The project has three versions of the data:

| File | What it is |
|---|---|
| `sentiment.csv` | The full raw dataset. May have unequal amounts of positive/negative/neutral. |
| `equal.csv` | A balanced version — same number of positive, neutral, and negative reviews. Used for training. |
| `ratio.csv` | A proportional version — keeps the natural real-world ratio of sentiments. |

Cells 9 and 11 run the same summary report (`pd.DataFrame({...})`) on these other datasets.

---

### Cell 12 — Checking unique sentiment values

```python
print(f"unique values in full dataset: {df_full['Sentiment'].unique()}\n")
print(f"unique values in equal dataset: {df_equal['Sentiment'].unique()}\n")
print(f"unique values in ratio dataset: {df_ratio['Sentiment'].unique()}")
```

**What is happening here?**
`df['Sentiment']` selects just the "Sentiment" column. `.unique()` returns all the different values it contains — like `['Positive', 'positive', 'POSITIVE', 'negative', ...]`. This step reveals if there are inconsistencies (uppercase/lowercase, extra spaces, typos) that need to be fixed.

---

### Cell 13 — Normalizing sentiment labels

```python
df_full["Sentiment"]  = df_full["Sentiment"].str.lower().str.strip()
df_equal["Sentiment"] = df_equal["Sentiment"].str.lower().str.strip()
df_ratio["Sentiment"] = df_ratio["Sentiment"].str.lower().str.strip()
```

**What is happening here?**
`.str.lower()` — converts all text to lowercase. So "Positive", "POSITIVE", "positive" all become "positive."
`.str.strip()` — removes any invisible spaces at the start or end. "positive " and " positive" both become "positive."

Without this, "Positive" and "positive" would be treated as two different categories — which would break everything.

---

### Cell 14 — Dropping rows with missing important values

```python
df_full.dropna(
    subset=["ProductPrice", "Rate", "Review", "Summary", "Sentiment"],
    inplace=True
)
```

**What is happening here?**
`dropna()` removes rows that have missing (empty) values. `subset=[...]` means "only check these specific columns." If any of these columns is empty in a row, that entire row is deleted.

`inplace=True` means "modify the original DataFrame directly, don't create a copy." Without it, the change would be lost.

**Why?** You can't train a model on a review that doesn't exist, or a sentiment label that's missing.

---

### Cell 15 — Grouping datasets for easy looping

```python
datasets = {
    "Full Dataset\n(sentiment.csv)": df_full,
    "Balanced Dataset\n(Equal.csv)":  df_equal,
    "Ratio Dataset\n(RATIO.csv)":     df_ratio
}
```

**What is happening here?**
A Python dictionary that maps a display name to each DataFrame. The `\n` in the string creates a line break in chart titles. This lets the next cells loop over all three datasets without repeating code three times.

---

### Cell 16 — Plotting sentiment distribution

```python
fig, axes = plt.subplots(1, 3, figsize=(18, 6))

colors = ['#2ecc71', '#3498db', '#e74c3c']

for ax, (title, df) in zip(axes, datasets.items()):
    counts = df['Sentiment'].value_counts()
    bars = ax.bar(counts.index, counts.values, color=colors[:len(counts)], ...)
    ...
    for bar, count in zip(bars, counts.values):
        ax.text(bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 200,
                f'{count:,}', ...)

plt.savefig(f'{OUTPUT_PATH}/sentiment_distribution.png', bbox_inches='tight')
```

**What is happening here?**
This draws a bar chart showing how many positive/neutral/negative reviews are in each dataset.

| Part | Meaning |
|---|---|
| `plt.subplots(1, 3)` | Create 1 row, 3 columns of charts side by side. Returns the figure (`fig`) and 3 axes (`axes`). |
| `figsize=(18, 6)` | Total figure is 18 inches wide, 6 tall. |
| `colors = ['#2ecc71', '#3498db', '#e74c3c']` | Green, Blue, Red — hex color codes for positive, neutral, negative bars. |
| `zip(axes, datasets.items())` | Pairs each chart slot with a dataset, so you can loop over them together. |
| `df['Sentiment'].value_counts()` | Counts how many times each sentiment appears. Returns something like `positive: 5000, negative: 4800`. |
| `ax.bar(...)` | Draws the actual bars. |
| `bar.get_x() + bar.get_width() / 2` | Finds the horizontal center of each bar, to place the count label there. |
| `f'{count:,}'` | Formats number with commas: 5000 → "5,000". Easier to read. |
| `bbox_inches='tight'` | Saves the chart without cutting off any labels at the edges. |

---

### Cell 17 — Adding word and character count columns

```python
for dataset in datasets.values():
    dataset["review_word_count"] = dataset["Review"].str.split().str.len()
    dataset["review_char_count"] = dataset["Review"].str.len()
```

**What is happening here?**
For every dataset, this adds two new columns.

- `.str.split()` — splits each review into a list of words: `"good product"` → `["good", "product"]`
- `.str.len()` on the split result — counts how many words are in that list: `2`
- `.str.len()` directly on the text — counts how many characters (letters) are in the review

This lets you answer: are negative reviews shorter or longer than positive ones?

---

### Cell 18 — Plotting review length distribution

```python
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

axes[0].hist(df['review_word_count'].clip(upper=200), bins=50, ...)
axes[0].axvline(df['review_word_count'].median(), color='red', linestyle='--', ...)

axes[1].boxplot([...], labels=['Positive', 'Neutral', 'Negative'], ...)
```

**What is happening here?**

Left chart — a histogram (frequency bar chart):
- `.clip(upper=200)` — caps all values at 200 words. If a review has 5000 words, it gets treated as 200, so it doesn't stretch the chart into empty space.
- `bins=50` — divides the range (0 to 200 words) into 50 buckets and counts how many reviews fall in each.
- `axvline(df['review_word_count'].median(), ...)` — draws a vertical red dashed line at the **median** (the middle value). Median is better than average here because a few very long reviews would drag the average up unfairly.

Right chart — a box plot:
- Shows word count distribution split by sentiment class.
- The box shows the middle 50% of values. The line in the box is the median. Dots outside are outliers (unusually long/short reviews).

---

### Cell 19 — Star rating vs sentiment heatmap

```python
df_equal_clean = df_equal.copy()
df_equal_clean['Rate'] = pd.to_numeric(df_equal_clean['Rate'], errors='coerce')
df_equal_clean = df_equal_clean.dropna(subset=['Rate'])
df_equal_clean['Rate'] = df_equal_clean['Rate'].round().astype(int)
df_equal_clean = df_equal_clean[df_equal_clean['Rate'].between(1, 5)]

ct = pd.crosstab(df_equal_clean['Rate'], df_equal_clean['Sentiment'])
```

**What is happening here?**

| Part | Meaning |
|---|---|
| `.copy()` | Make a copy so you don't accidentally modify the original. |
| `pd.to_numeric(..., errors='coerce')` | Try to convert the Rate column to numbers. If a value is text like "N/A", instead of crashing, turn it into `NaN`. |
| `.dropna(subset=['Rate'])` | Remove rows where Rate is now NaN (because it couldn't be converted). |
| `.round().astype(int)` | Round to nearest whole number (4.7 → 5), then convert to integer type. |
| `.between(1, 5)` | Keep only rows where Rate is 1, 2, 3, 4, or 5. Filter out garbage values. |
| `pd.crosstab(...)` | Creates a table that counts how many reviews fall into each Rate + Sentiment combination. Like a pivot table. |

Then two heatmaps are drawn:
- Left: raw counts (how many 5-star reviews are positive?)
- Right: percentages (what % of 5-star reviews are positive?)

`sns.heatmap(..., fmt='d')` — `fmt='d'` means format numbers as integers (no decimals). `fmt='.1f'` means 1 decimal place for percentages.

---

### Cell 20 — Word clouds

```python
def simple_clean(text):
    if not isinstance(text, str): return ""
    text = text.lower()
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'[^a-z\s]', '', text)
    return text

STOPWORDS = {'the', 'a', 'an', 'is', 'it', ...}

for ax, sentiment, colormap in zip(axes, sentiments, cloud_colors):
    texts   = df_equal[df_equal['Sentiment'] == sentiment]['Review'].dropna()
    combined = ' '.join(texts.apply(simple_clean))
    wc = WordCloud(width=600, height=400, ...).generate(combined)
    ax.imshow(wc, interpolation='bilinear')
    ax.axis('off')
```

**What is happening here?**

`simple_clean()` does a quick light clean just for visualization:
- `re.sub(r'http\S+', '', text)` — removes URLs (`\S+` means "one or more non-space characters after http")
- `re.sub(r'[^a-z\s]', '', text)` — removes everything that isn't a letter or space. `[^...]` means "not these characters."

`STOPWORDS` — common words that don't carry meaning and would dominate the cloud ("the", "a", "is"). Filtered out so interesting words appear bigger.

`' '.join(texts.apply(simple_clean))` — takes all reviews of one sentiment, cleans each one, and joins them into one giant string of text.

`WordCloud(...).generate(combined)` — counts word frequencies and generates the visual cloud. Bigger word = appears more often.

`ax.imshow(wc, interpolation='bilinear')` — displays the word cloud image in the chart. `bilinear` smooths the image rendering.

`ax.axis('off')` — hides the X and Y axis lines/ticks (they make no sense on an image).

---

### Cell 21 — Top 15 words per sentiment

```python
from collections import Counter

for ax, sentiment in zip(axes, ['positive', 'neutral', 'negative']):
    texts = df_equal[df_equal['Sentiment'] == sentiment]['Review'].dropna()
    all_words = []

    for review in texts:
        clean = simple_clean(str(review))
        words = [w for w in clean.split() if w not in STOPWORDS and len(w) >= 3]
        all_words.extend(words)

    top_words = Counter(all_words).most_common(15)
    words, counts = zip(*top_words)

    ax.barh(range(len(words)), counts, ...)
    ax.set_yticks(range(len(words)))
    ax.set_yticklabels(words)
    ax.invert_yaxis()
```

**What is happening here?**

`Counter(all_words)` — counts how many times each word appears. Like a tally chart.
`.most_common(15)` — returns the top 15 most frequent words as a list of `(word, count)` tuples.
`zip(*top_words)` — the `*` "unpacks" the list. This separates the words list from the counts list. Like unzipping a zipper — you had pairs, now you have two separate lists.

`ax.barh(...)` — horizontal bar chart (`barh` = bar horizontal). Shows the 15 words with bars going left to right.
`ax.invert_yaxis()` — puts the most common word at the top instead of the bottom.
`[w for w in clean.split() if w not in STOPWORDS and len(w) >= 3]` — a **list comprehension**: only keep word `w` if it's not a stopword AND has at least 3 characters (skips "ok", "so", "hi").

---

# 2. `preprocessing.ipynb` — Cleaning the Data

> **What does this file do?** Takes the raw reviews and turns them into a form the neural network can actually understand. Words can't go into a neural network — only numbers can. This file cleans the text, converts words to numbers, splits into train/val/test sets, and saves everything to disk.

---

### Cell 0 — Installing libraries

```python
!uv add numpy pandas nltk contractions scikit-learn tqdm joblib tensorflow keras
```

Same idea as EDA — downloading the tools. Extra ones here:

| Library | Why needed here |
|---|---|
| `nltk` | Natural Language Toolkit. Has word lists (stopwords), grammar tools, and word simplification. |
| `contractions` | Expands "can't" → "cannot", "I'm" → "I am", etc. |
| `scikit-learn` | ML helper tools: splitting data, encoding labels, computing class weights. |
| `tqdm` | Progress bar for long loops. |
| `joblib` | Saves Python objects to disk files. |
| `tensorflow / keras` | Used here just for the Tokenizer and pad_sequences tools. |

---

### Cell 1 — Imports

```python
import pandas as pd
import numpy as np
import contractions
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.utils import class_weight
import re
import os
import joblib
```

| Import | What it's for |
|---|---|
| `from sklearn.model_selection import train_test_split` | A function that randomly splits data into train/test sets. |
| `from sklearn.preprocessing import LabelEncoder` | Converts text labels ("positive") into numbers (2). |
| `from sklearn.utils import class_weight` | Calculates how much to weight each class during training. |
| `import re` | Regular expressions — a language for finding and replacing text patterns. |
| `import joblib` | Saves/loads Python objects to disk. |

---

### Cell 2 — Suppress warnings

```python
import warnings
warnings.filterwarnings("ignore")
```

Same as EDA — hides noisy but harmless warning messages.

---

### Cell 3 — NLTK downloads

```python
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

nltk.download("stopwords", quiet=True)
nltk.download("punkt", quiet=True)
nltk.download("wordnet", quiet=True)
nltk.download("averaged_perceptron_tagger", quiet=True)
```

**What is NLTK and why download?**
NLTK is a toolkit for human language. It comes with pre-built datasets and models, but you have to download them separately the first time.

| Download | What it is |
|---|---|
| `stopwords` | A list of ~180 common English words ("the", "is", "at") that carry no meaning for sentiment. |
| `punkt` | A sentence/word splitter that knows "Dr. Smith" isn't two sentences. |
| `wordnet` | A huge English word dictionary used for lemmatization. |
| `averaged_perceptron_tagger` | A grammar tool that labels words as noun, verb, adjective, etc. Used internally by the lemmatizer. |

`quiet=True` — don't print download messages to the screen.

`from nltk.corpus import stopwords` — loads the stopwords list.
`from nltk.stem import WordNetLemmatizer` — loads the word simplifier.

---

### Cell 4 — Create folders

```python
os.makedirs('models', exist_ok=True)
os.makedirs('output', exist_ok=True)
```

Creates the `models/` folder (to save trained model files) and `output/` (for charts). `exist_ok=True` — don't crash if already exists.

---

### Cell 5 — Load the dataset

```python
df = pd.read_csv('./data/equal.csv', encoding='latin-1')

df['Sentiment'] = df['Sentiment'].str.lower().str.strip()
df = df.dropna(subset=['Review', 'Sentiment'])
df = df.reset_index(drop=True)

df.head(3)
```

**Why `equal.csv`?**
The balanced dataset is used for training. If one class (say "positive") has 10x more data than "negative," the model learns to always guess positive — even for negative reviews — because it's right 10x more often. Equal classes force it to learn all three.

`df.reset_index(drop=True)` — after dropping rows with missing values, the row numbers (index) have gaps: 0, 1, 5, 8, 12... This resets them to 0, 1, 2, 3, 4... clean and continuous. `drop=True` means don't keep the old index as a column.

---

### Cell 6 — Defining the cleaning toolkit

```python
lemmatizer = WordNetLemmatizer()

STOPWORDS_SET = set(stopwords.words('english'))
NEGATION_WORDS = {'not', 'no', 'never', "n't", 'neither', 'nor', 'none'}

STOPWORDS_SET -= NEGATION_WORDS
```

**`WordNetLemmatizer()`** — creates the lemmatizer object. Think of it as hiring a librarian who knows that "running", "runs", "ran" all mean the same root word "run."

**`set(stopwords.words('english'))`** — loads the 180 stopwords as a Python `set`. Sets are much faster than lists for checking "is this word in here?" — like using an index in a book vs reading every page.

**`STOPWORDS_SET -= NEGATION_WORDS`** — removes negation words FROM the stopwords set. This is critical! If "not" is removed as a stopword, then "not good" becomes "good" — the opposite meaning. The model needs to know "not" to understand negativity.

---

```python
def expand_contractions(text):
    return re.sub(r'<[^>]+>', ' ', text)
```

⚠️ **This is a bug in the code.** The function is named `expand_contractions` but the body is actually removing HTML tags (same as `remove_html_tags`). Likely a copy-paste error from when the code was being written. In practice, the `contractions` library was imported but this function doesn't actually use it. The HTML tags still get removed by the real `remove_html_tags` function below, so the output is still correct — it's just that contractions like "can't" aren't being expanded.

```python
def remove_html_tags(text):
    return re.sub(r'<[^>]+>', ' ', text)
```

`re.sub(pattern, replacement, string)` — replaces all matches of `pattern` in `string` with `replacement`.
`r'<[^>]+>'` — a regex pattern:
- `<` — literal opening angle bracket
- `[^>]+` — one or more characters that are NOT `>`
- `>` — literal closing angle bracket

This matches any HTML tag like `<br>`, `<b>`, `<div class="x">` and replaces it with a space.

```python
def remove_urls(text):
    return re.sub(r'https?://\S+|www\.\S+', '', text)
```

`https?://` — matches "http://" or "https://" (the `?` makes the `s` optional).
`\S+` — one or more non-space characters (the rest of the URL).
`|` — OR.
`www\.\S+` — matches URLs starting with "www." (the `\.` is an escaped dot — a literal dot, not "any character").

```python
def remove_special_characters(text):
    return re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
```

`[^a-zA-Z0-9\s]` — matches anything that is NOT a letter (a-z, A-Z), digit (0-9), or whitespace (`\s`). Replaces punctuation, symbols, etc. with a space.

```python
def remove_extra_spaces(text):
    return re.sub(r'\s+', ' ', text).strip()
```

`\s+` — matches one or more whitespace characters (spaces, tabs, newlines). Replaces all of them with a single space. `.strip()` removes leading and trailing spaces.

```python
def remove_stopwords(text):
    words = text.split()
    filtered = [word for word in words if word not in STOPWORDS_SET]
    return ' '.join(filtered)
```

`text.split()` — splits the text into a list of words by spaces.
`[word for word in words if word not in STOPWORDS_SET]` — list comprehension: keep each word only if it's NOT in the stopwords set.
`' '.join(filtered)` — joins the remaining words back into a string with spaces.

```python
def lemmatize_text(text):
    words = text.split()
    lemmatized = [lemmatizer.lemmatize(word) for word in words]
    return ' '.join(lemmatized)
```

`lemmatizer.lemmatize(word)` — converts a word to its base form. "dogs" → "dog", "running" → "running" (without knowing it's a verb, the lemmatizer defaults to noun form, so "running" stays as is). For better results, you'd also tell it the part of speech, but that's more complex.

```python
def handle_emojis(text):
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)
```

Emojis are Unicode characters in specific ranges. This regex pattern matches any character in those ranges and removes them. `re.compile(...)` creates a compiled pattern object (faster if used many times). `flags=re.UNICODE` ensures it handles Unicode properly.

---

### Cell 7 — The master cleaning function

```python
def full_preprocess(text, use_lemmatization=True):
    if not isinstance(text, str):
        return ""

    text = expand_contractions(text)
    text = text.lower()
    text = remove_html_tags(text)
    text = remove_urls(text)
    text = handle_emojis(text)
    text = remove_special_characters(text)
    text = remove_stopwords(text)

    if use_lemmatization:
        text = lemmatize_text(text)

    text = remove_extra_spaces(text)

    return text
```

This calls all the cleaning functions in order. Every review passes through this pipeline.

`if not isinstance(text, str): return ""` — safety check. If the input isn't a string (maybe it's a number or `None`), return an empty string instead of crashing.

`use_lemmatization=True` — a default parameter. If you don't specify it, lemmatization is ON. But in Cell 9, it's called with `use_lemmatization=False` — turning lemmatization off. Why? Because the LSTM model is powerful enough to learn that "running" and "ran" are related. Lemmatizing can actually remove useful signal (tense matters for sentiment sometimes).

**The order matters:**
1. Expand contractions first (before lowercasing changes "I'm")
2. Lowercase so everything is consistent
3. Remove HTML (before special chars, since `<` and `>` are special chars)
4. Remove URLs (before special chars removes the `//` and `.`)
5. Remove emojis (Unicode — handled before stripping to letters only)
6. Remove special chars (now all that's left is letters, numbers, spaces)
7. Remove stopwords (words only, no punctuation to confuse matching)
8. Lemmatize (optional — simplify words to root forms)
9. Remove extra spaces (clean up whatever gaps remain)

---

### Cell 8 — Combining Summary and Review columns

```python
df['combined_text'] = (
    df['Summary'].fillna('') + ' ' + df['Review'].fillna('')
)
df.head(1)
```

**Why combine?**
The dataset has two text columns: `Summary` (short title like "Great product!") and `Review` (longer body text). Both contain sentiment signals. Combining them gives the model more to work with.

`.fillna('')` — replaces any missing values with an empty string, so concatenation doesn't produce "Great product! NaN."

---

### Cell 9 — Actually running the cleaning

```python
from tqdm import tqdm
tqdm.pandas(desc="Preprocessing")

df['clean_text'] = df['combined_text'].progress_apply(
    lambda x: full_preprocess(x, use_lemmatization=False)
)

df = df[df['clean_text'].str.len() > 5]
df = df.reset_index(drop=True)
df.head(1)
```

`tqdm.pandas(desc="Preprocessing")` — patches pandas so `.progress_apply()` works. It adds a progress bar.

`.progress_apply(lambda x: full_preprocess(x, use_lemmatization=False))` — applies the cleaning function to every row. `lambda x: ...` is an anonymous (inline) function — like a tiny one-line function without needing `def`. `x` is each review text.

`df[df['clean_text'].str.len() > 5]` — after cleaning, some reviews might be basically empty (all their words were stopwords or symbols). This filters out any clean_text shorter than 6 characters. Can't learn much from an empty string.

---

### Cell 10 — Encoding labels (text → numbers)

```python
le = LabelEncoder()

df['label'] = le.fit_transform(df['Sentiment'])

print("   Label encoding map:")
for i, cls in enumerate(le.classes_):
    print(f"     {cls} → {i}")

joblib.dump(le, './models/label_encoder.pkl')
```

**Why convert labels to numbers?**
Neural networks only work with numbers. "positive" needs to become 2 (or 0 or 1 — it's arbitrary, but consistent).

`le.fit_transform(df['Sentiment'])`:
- `fit` — look at all unique values ("negative", "neutral", "positive") and assign each a number in alphabetical order: negative=0, neutral=1, positive=2
- `transform` — replace every value in the column with its number

`le.classes_` — the list of original class names in the order they were encoded. Used to print the mapping.

`joblib.dump(le, './models/label_encoder.pkl')` — saves the encoder to disk. When you later make predictions, you need this to convert the number back to a word (2 → "positive"). `.pkl` is a "pickle" file — Python's format for saving any object.

---

### Cell 11 — Splitting data into three sets

```python
X = df['clean_text'].values    # Features
y = df['label'].values          # Labels

X_train, X_temp, y_train, y_temp = train_test_split(
    X, y,
    test_size=0.30,
    random_state=42,
    stratify=y
)

X_val, X_test, y_val, y_test = train_test_split(
    X_temp, y_temp,
    test_size=0.50,
    random_state=42,
    stratify=y_temp
)
```

**`X` and `y`** — machine learning convention. `X` = inputs (the features — what you feed in). `y` = outputs (the labels — what you want to predict).

`.values` — converts the pandas Series to a plain numpy array. Slightly faster and more compatible with sklearn/tensorflow.

**First split:** Takes 30% of the data as `X_temp` (temporary). Keeps 70% as training.
**Second split:** Splits that 30% in half. 15% becomes validation, 15% becomes test.

**Final result:** 70% train, 15% validation, 15% test.

| Parameter | Meaning |
|---|---|
| `test_size=0.30` | Take 30% for the temporary set (will be split again). |
| `random_state=42` | The random seed — ensures the same split every time you run the code. 42 is just a convention (from Hitchhiker's Guide to the Galaxy). |
| `stratify=y` | Ensures each split has the same proportion of positive/neutral/negative. Without this, by bad luck you might get 90% positive in one split. |

**Why three sets instead of two?**
- **Training set** — what the model learns from. Sees this many times.
- **Validation set** — checked after each epoch (training round) to monitor progress. The model never learns FROM this, but its performance here guides decisions like "stop early" or "reduce learning rate."
- **Test set** — never touched until the very end. Gives you an honest final score. If you used validation for final evaluation, you'd be cheating because you made decisions (like early stopping) based on it.

---

### Cell 12 — Tokenizing and padding

```python
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

MAX_WORDS = 30000
MAX_LEN   = 100

tokenizer = Tokenizer(
    num_words=MAX_WORDS,
    oov_token='<OOV>',
    lower=True
)

tokenizer.fit_on_texts(X_train)
```

**What is tokenization?**
Words need to become numbers. A tokenizer builds a dictionary: "good" → 5, "not" → 3, "terrible" → 847. Then it converts every review into a list of those numbers.

| Parameter | Meaning |
|---|---|
| `num_words=30000` | Only keep the 30,000 most frequent words. Words that appear very rarely (once or twice) don't help the model learn — they're just noise. Any rarer word gets replaced with the OOV token. |
| `oov_token='<OOV>'` | Out Of Vocabulary. When a word from the validation or test set wasn't in the training vocabulary, it becomes `<OOV>` instead of crashing or being silently dropped. The model can learn that `<OOV>` means "unknown word." |
| `lower=True` | Convert to lowercase before tokenizing. So "Good" and "good" get the same ID. |

**`tokenizer.fit_on_texts(X_train)`** — this is the "learning" step. The tokenizer reads all training reviews, counts every word's frequency, and builds the vocabulary dictionary. It ONLY fits on training data — if it saw the test data, the model would have an unfair advantage.

```python
X_train_seq = tokenizer.texts_to_sequences(X_train)
X_val_seq   = tokenizer.texts_to_sequences(X_val)
X_test_seq  = tokenizer.texts_to_sequences(X_test)
```

`texts_to_sequences()` — converts each review from text to a list of numbers using the vocabulary dictionary built above. "good product" → [5, 234]. Unknown words become the OOV ID.

```python
X_train_pad = pad_sequences(X_train_seq, maxlen=MAX_LEN, padding='post', truncating='post')
X_val_pad   = pad_sequences(X_val_seq,   maxlen=MAX_LEN, padding='post', truncating='post')
X_test_pad  = pad_sequences(X_test_seq,  maxlen=MAX_LEN, padding='post', truncating='post')
```

**Why pad?**
Neural networks need all inputs to be the same length. Reviews have different lengths (some 3 words, some 500). Padding fixes this.

| Parameter | Meaning |
|---|---|
| `maxlen=100` | All sequences will be exactly 100 numbers long. |
| `padding='post'` | Add zeros at the END of short reviews. Prefer post-padding for RNNs because the model reads left-to-right and real content is at the start. |
| `truncating='post'` | If a review is longer than 100 words, cut off the END (keep the beginning). Most sentiment is stated early. |

```python
weights = class_weight.compute_class_weight(
    class_weight='balanced',
    classes=np.unique(y_train),
    y=y_train
)

class_weights_dict = dict(enumerate(weights))
```

**Why class weights?**
Even in `equal.csv`, there might be slight imbalances after cleaning and splitting. If the model sees 60% positive reviews, it could just always guess "positive" and be right 60% of the time — without actually learning anything. Class weights tell the model: "if you get a negative review wrong, that's MORE costly than getting a positive review wrong." Forces it to learn all classes equally.

`class_weight='balanced'` — automatically calculates weights: `total_samples / (n_classes * n_samples_in_class)`. Rarer classes get higher weights.

```python
np.save('models/X_train_pad.npy', X_train_pad)
# ... (saves all arrays)
joblib.dump(tokenizer, 'models/tokenizer.pkl')
joblib.dump({'MAX_WORDS': MAX_WORDS, 'MAX_LEN': MAX_LEN}, 'models/config.pkl')
```

**Saving everything to disk:**
- `.npy` files — numpy's format for saving arrays. Fast and compact.
- `.pkl` files — pickle format for saving any Python object (tokenizer, label encoder, config dict).
- These files are loaded by `lstm.ipynb` so you don't have to re-run preprocessing every time.

---

# 3. `lstm.ipynb` — Building and Training the Brain

> **What does this file do?** Loads the preprocessed data, builds the neural network, trains it, and evaluates its accuracy. This is where the actual "learning" happens.

---

### Cell 0 — Installing libraries

```python
!uv add numpy tensorflow keras seaborn joblib scikit-learn
```

Subset of the preprocessing libraries — only what the model training needs.

---

### Cell 1 — Imports

```python
import numpy as np
import os
import joblib
import matplotlib.pyplot as plt

import tensorflow as tf
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import (
    Embedding, LSTM, Bidirectional, Dense, Dropout,
    SpatialDropout1D, GlobalMaxPooling1D, Input, Conv1D
)
from tensorflow.keras.callbacks import (
    EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
)
from tensorflow.keras.optimizers import Adam
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns
```

**What each import is for:**

| Import | Purpose |
|---|---|
| `Sequential` | A model type where layers are stacked one after another in a line. Simple and clear. |
| `Model` | A more flexible model type (imported but not used here — probably left from experimentation). |
| `Embedding` | A layer that converts word IDs into dense vectors of numbers. |
| `LSTM` | The memory-based recurrent layer. Reads sequences and remembers context. |
| `Bidirectional` | A wrapper that runs an LSTM in both directions (forward + backward). |
| `Dense` | A fully connected layer — every neuron connects to every neuron in the next layer. |
| `Dropout` | Randomly turns off neurons during training to prevent memorization. |
| `SpatialDropout1D` | Like Dropout but drops entire word embedding dimensions rather than individual neurons — better for sequences. |
| `GlobalMaxPooling1D` | (imported but not used) — takes the max value across the time dimension. Alternative to using LSTM's final output. |
| `Input` | (imported but not used) — defines input shape for non-Sequential models. |
| `Conv1D` | (imported but not used) — 1D convolutional layer for text — alternative to LSTM. |
| `EarlyStopping` | Stops training if performance stops improving. |
| `ModelCheckpoint` | Saves the model to disk whenever it improves. |
| `ReduceLROnPlateau` | Reduces learning rate when stuck. |
| `Adam` | The optimizer — the algorithm that updates the model's weights. |
| `classification_report` | Prints precision, recall, F1 for each class. |
| `confusion_matrix` | Table showing what the model predicted vs what was actually correct. |

---

### Cell 2 — Suppress warnings

```python
import warnings
warnings.filterwarnings('ignore')
```

Same as before — hide non-critical warnings.

---

### Cell 3 — Setting random seeds

```python
np.random.seed(42)
tf.random.set_seed(42)
```

**Why?**
Neural networks involve randomness in many places: initial weights are random, dropout randomly drops neurons, data shuffling is random. Without setting seeds, you'd get slightly different results every run — making it hard to reproduce or compare experiments.

`42` is just a convention. Any number works. Setting both numpy and tensorflow seeds ensures reproducibility across all random operations in the pipeline.

---

### Cell 4 — Create folders

```python
os.makedirs('models', exist_ok=True)
os.makedirs('output', exist_ok=True)
```

Same safety step — ensure folders exist before trying to save files there.

---

### Cell 5 — Loading preprocessed data

```python
X_train = np.load('models/X_train_pad.npy')
X_val   = np.load('models/X_val_pad.npy')
X_test  = np.load('models/X_test_pad.npy')
y_train = np.load('models/y_train.npy')
y_val   = np.load('models/y_val.npy')
y_test  = np.load('models/y_test.npy')
class_weights = np.load('models/class_weights.npy')

config    = joblib.load('models/config.pkl')
MAX_WORDS = config['MAX_WORDS']
MAX_LEN   = config['MAX_LEN']

class_weights_dict = {i: w for i, w in enumerate(class_weights)}
```

`np.load()` — loads the `.npy` array files saved by preprocessing.
`joblib.load()` — loads the config dictionary (with MAX_WORDS and MAX_LEN) saved by preprocessing.
`{i: w for i, w in enumerate(class_weights)}` — a dictionary comprehension that converts the array `[1.1, 0.9, 1.0]` into `{0: 1.1, 1: 0.9, 2: 1.0}`. The model needs a dict mapping class index → weight.

**Why load from disk instead of re-running preprocessing?**
Preprocessing takes a long time (cleaning 100k+ reviews). By saving the output, you can train the model many times with different architectures without waiting for preprocessing each time.

---

### Cell 6 — Verifying shapes

```python
print(f"   X_train shape: {X_train.shape}")
print(f"   y_train shape: {y_train.shape}")
print(f"   Class weights: {class_weights_dict}")
```

A sanity check. If `X_train.shape` is `(70000, 100)`, that means 70,000 reviews, each 100 words long — which is what you expect. If something is wrong (e.g. shape is `(100, 70000)`), you'd catch it here before wasting training time.

---

### Cell 7 — Hyperparameters

```python
EMBEDDING_DIM = 128
LSTM_UNITS_1  = 128
LSTM_UNITS_2  = 64
DENSE_UNITS   = 64
DROPOUT_RATE  = 0.3
NUM_CLASSES   = 3
```

**Hyperparameters** are settings you choose before training — the model doesn't learn these, you decide them. Think of them as the recipe before cooking.

| Hyperparameter | Value | What it controls |
|---|---|---|
| `EMBEDDING_DIM` | 128 | Each word is represented as a list of 128 numbers. More dimensions = more nuance the model can capture about word meaning. 128 is a common sweet spot between expressiveness and efficiency. |
| `LSTM_UNITS_1` | 128 | The first LSTM has 128 "memory cells." More units = can remember more complex patterns, but also more parameters and slower training. |
| `LSTM_UNITS_2` | 64 | The second LSTM is smaller. It summarizes what the first found. The funnel shape (128 → 64) is a common architecture choice — compress information progressively. |
| `DENSE_UNITS` | 64 | The fully connected layer has 64 neurons. Learns combinations of the LSTM's features. |
| `DROPOUT_RATE` | 0.3 | 30% of neurons are randomly disabled during each training step. Prevents the model from memorizing specific patterns. |
| `NUM_CLASSES` | 3 | Three output categories: negative (0), neutral (1), positive (2). |

---

### Cell 8 — Model architecture

```python
model = Sequential([
    Embedding(
        input_dim=MAX_WORDS,
        output_dim=EMBEDDING_DIM,
        input_length=MAX_LEN,
        name='embedding'
    ),

    SpatialDropout1D(DROPOUT_RATE, name='spatial_dropout'),

    Bidirectional(
        LSTM(LSTM_UNITS_1, return_sequences=True, dropout=0.2, recurrent_dropout=0.1),
        name='bilstm_1'
    ),

    Bidirectional(
        LSTM(LSTM_UNITS_2, return_sequences=False, dropout=0.2, recurrent_dropout=0.1),
        name='bilstm_2'
    ),

    Dense(DENSE_UNITS, activation='relu', name='dense_1'),

    Dropout(DROPOUT_RATE, name='dropout_1'),

    Dense(NUM_CLASSES, activation='softmax', name='output')
])

model.summary()
```

**`Sequential([...])`** — stacks layers in order, like pancakes. Data flows from top to bottom through each layer.

---

**Layer 1: Embedding**
```python
Embedding(input_dim=MAX_WORDS, output_dim=EMBEDDING_DIM, input_length=MAX_LEN)
```
- Input: a review as 100 numbers (word IDs). Shape: `(100,)`
- Output: each word ID becomes a 128-number vector. Shape: `(100, 128)`
- `input_dim=30000` — vocabulary size. The embedding table has 30,000 rows.
- `output_dim=128` — each word maps to a 128-dimensional vector.
- `input_length=100` — how many word IDs come in. Must match MAX_LEN.
- The embedding vectors start random and get updated during training. Similar words (like "good" and "great") end up with similar vectors.
- Think of it as giving each word a "personality profile" of 128 numbers.

---

**Layer 2: SpatialDropout1D**
```python
SpatialDropout1D(0.3)
```
- Randomly drops entire embedding dimensions (entire "channels") rather than individual values.
- Regular Dropout would randomly zero out individual numbers. SpatialDropout1D zeroes out entire feature dimensions across the whole sequence.
- Why? In text, nearby words share similar features. Dropping individual values doesn't break the correlation enough. Dropping entire dimensions forces the model to not rely on any single feature.

---

**Layer 3: Bidirectional LSTM (128 units)**
```python
Bidirectional(
    LSTM(128, return_sequences=True, dropout=0.2, recurrent_dropout=0.1)
)
```
**What is LSTM?**
A regular neural network sees one input and produces one output, forgetting everything before. An LSTM has a "memory" — it maintains a hidden state that carries information from earlier words in the sequence.

Like reading: when you reach "terrible" at word 50, you still remember that word 10 was "not" — so "not terrible" means something good.

**Bidirectional** wraps the LSTM and runs it twice:
- Once forward (word 1 → word 100)
- Once backward (word 100 → word 1)
- Both outputs are concatenated. This doubles the output size (128 × 2 = 256 values per timestep).

Why bidirectional? Some words get meaning from what comes AFTER them. "I thought this was good — I was wrong." The word "good" only makes sense as negative once you read "I was wrong" after it.

| Parameter | Meaning |
|---|---|
| `return_sequences=True` | Return the output for EVERY word, not just the last one. Shape: `(100, 256)`. Needed because the next layer (another LSTM) also needs a sequence to process. |
| `dropout=0.2` | 20% dropout on the input at each timestep. |
| `recurrent_dropout=0.1` | 10% dropout on the recurrent (memory-to-memory) connections. Regularizes the memory itself. |

---

**Layer 4: Bidirectional LSTM (64 units)**
```python
Bidirectional(
    LSTM(64, return_sequences=False, dropout=0.2, recurrent_dropout=0.1)
)
```
Same concept but smaller (64 units) and `return_sequences=False` — only return the final output, not every word's output. Shape goes from `(100, 128)` to `(128,)` — a single 128-value vector that summarizes the entire review.

Why two LSTM layers? The first layer learns local patterns (word pairs, short phrases). The second layer learns longer patterns across the whole review. Stacking LSTMs is like reading sentences (first LSTM) and then understanding the whole paragraph (second LSTM).

---

**Layer 5: Dense (64 units, ReLU)**
```python
Dense(64, activation='relu')
```
A standard fully connected layer. Every one of the 128 inputs connects to all 64 neurons.

`activation='relu'` — ReLU (Rectified Linear Unit). The activation function is applied to each neuron's output. ReLU: if the value is negative, output 0. If positive, output the value unchanged. Simple but very effective.

Why use an activation function? Without it, stacking linear layers is mathematically equivalent to just one linear layer. Activations add non-linearity — the ability to learn complex, curved patterns rather than just straight lines.

---

**Layer 6: Dropout**
```python
Dropout(0.3)
```
Another dropout — this time after the Dense layer. 30% of the 64 neurons are randomly zeroed during training. Prevents the dense layer from over-relying on specific LSTM features.

---

**Layer 7: Output Dense (3 units, Softmax)**
```python
Dense(3, activation='softmax')
```
The final layer. 3 neurons — one for each class.

`activation='softmax'` — converts the 3 raw numbers into 3 probabilities that add up to exactly 1.0 (100%). For example: `[negative: 0.05, neutral: 0.15, positive: 0.80]`. The class with the highest probability is the prediction.

Why softmax? It makes the output interpretable as probabilities and forces the model to "choose" — it can't assign high probability to all three.

`model.summary()` — prints a table of all layers, their output shapes, and parameter counts. Total parameters are often millions — each one gets adjusted during training.

---

### Cell 9 — Compiling the model

```python
model.compile(
    optimizer=Adam(learning_rate=0.001),
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)
```

**`compile()`** tells the model HOW to learn — the rules of the learning game.

**`optimizer=Adam(learning_rate=0.001)`**
The optimizer is the algorithm that adjusts the model's millions of numbers after each batch of reviews.

Adam (Adaptive Moment Estimation) is smart:
- It keeps track of how each parameter has been changing recently.
- If a parameter keeps moving in the same direction, Adam speeds it up.
- If it's bouncing around, Adam slows it down.
- Much better than plain Gradient Descent which uses the same step size for everything.

`learning_rate=0.001` — how big each adjustment step is. Too big = overshoots and bounces around, never converging. Too small = takes forever. 0.001 is the standard Adam starting point.

**`loss='sparse_categorical_crossentropy'`**
The loss function measures how wrong the model's predictions are. Lower = better.

- `categorical_crossentropy` — for multi-class problems (more than 2 classes).
- `sparse_` prefix — means labels are plain integers (0, 1, 2) NOT one-hot encoded arrays ([1,0,0], [0,1,0], [0,0,1]). "Sparse" because most of the label array would be zeros — wasteful to store.

**`metrics=['accuracy']`**
Just for display during training. Shows what percentage of predictions are correct each epoch. Not used to update weights — only `loss` is used for that.

---

### Cell 10 — Callbacks

```python
callbacks = [
    EarlyStopping(
        monitor='val_loss',
        patience=5,
        restore_best_weights=True,
        verbose=1
    ),

    ModelCheckpoint(
        filepath='models/lstm_best_model.keras',
        monitor='val_loss',
        save_best_only=True,
        verbose=1
    ),

    ReduceLROnPlateau(
        monitor='val_loss',
        factor=0.5,
        patience=3,
        min_lr=1e-6,
        verbose=1
    ),
]
```

**Callbacks** are functions that automatically trigger at certain points during training (after each epoch, after each batch, etc.).

---

**EarlyStopping**

| Parameter | Meaning |
|---|---|
| `monitor='val_loss'` | Watch the validation loss after each epoch. |
| `patience=5` | If the validation loss hasn't improved for 5 consecutive epochs, stop training. Saves time and prevents overfitting. |
| `restore_best_weights=True` | When stopping, rewind the model's weights to the epoch where validation loss was lowest. Without this, you'd end up with the final weights (which are worse than the best). |
| `verbose=1` | Print a message when early stopping triggers. |

---

**ModelCheckpoint**

| Parameter | Meaning |
|---|---|
| `filepath='models/lstm_best_model.keras'` | Where to save the model file. `.keras` is TensorFlow's format. |
| `monitor='val_loss'` | Save only when validation loss improves (reaches a new best). |
| `save_best_only=True` | Don't overwrite the file unless the new epoch is genuinely better. |

Like saving your game every time you reach a new best score.

---

**ReduceLROnPlateau**

| Parameter | Meaning |
|---|---|
| `monitor='val_loss'` | Watch validation loss. |
| `factor=0.5` | When stuck, multiply the learning rate by 0.5 (cut it in half). |
| `patience=3` | Wait 3 epochs of no improvement before reducing. |
| `min_lr=1e-6` | Never go below 0.000001. Prevents the learning rate from reaching zero. |

Like easing off the gas when you're approaching your destination — smaller steps let you fine-tune.

---

### Cell 11 — Training

```python
EPOCHS     = 5
BATCH_SIZE = 64

history = model.fit(
    X_train, y_train,
    validation_data=(X_val, y_val),
    epochs=EPOCHS,
    batch_size=BATCH_SIZE,
    class_weight=class_weights_dict,
    callbacks=callbacks,
    verbose=1
)
```

**`model.fit()`** — starts the training loop.

| Parameter | Meaning |
|---|---|
| `X_train, y_train` | The input data and correct labels to learn from. |
| `validation_data=(X_val, y_val)` | After each epoch, evaluate on this data to see if learning is generalizing. |
| `epochs=5` | Go through the entire training set 5 times. Each full pass = one epoch. EarlyStopping may stop before 5 if no improvement. |
| `batch_size=64` | Process 64 reviews at a time, then update weights. Not one-by-one (too slow), not all at once (too imprecise). 64 is a sweet spot for memory and speed. |
| `class_weight=class_weights_dict` | Tell the model to penalize mistakes on underrepresented classes more. |
| `callbacks=callbacks` | The three automatic helpers from Cell 10. |
| `verbose=1` | Print progress bar and metrics after each epoch. |

**What happens inside one epoch:**
1. Take 64 reviews (one batch).
2. Run them through the model forward (make predictions).
3. Compare predictions to real labels — compute loss.
4. Run backwards through the model (backpropagation) — figure out which parameters contributed to the error.
5. Nudge all parameters slightly to reduce that error (optimizer step).
6. Repeat for the next 64 reviews, until all training data is used.
7. Run the validation set to get val_loss and val_accuracy.
8. Callbacks check: should we save? Stop? Reduce LR?

`history` stores all the metrics (train loss, val loss, accuracy) for each epoch — useful for plotting learning curves.

---

### Cell 12 — Evaluation

```python
from tensorflow.keras.models import load_model
best_model = load_model('models/lstm_best_model.keras')

test_loss, test_acc = best_model.evaluate(X_test, y_test, verbose=0)
print(f"   Test Accuracy: {test_acc:.4f} ({test_acc*100:.2f}%)")
print(f"   Test Loss:     {test_loss:.4f}")
```

`load_model(...)` — loads the best saved checkpoint (from ModelCheckpoint). This may not be the final epoch's model — it's the best one from all epochs.

`best_model.evaluate(X_test, y_test)` — runs the test set through the model and returns loss and accuracy. The test set was never seen during training or validation — this is your honest final score.

`{test_acc:.4f}` — format to 4 decimal places. `{test_acc*100:.2f}%` — multiply by 100 and show as percentage with 2 decimal places.

`verbose=0` — don't show a progress bar (the evaluate is fast enough that it's unnecessary).

---

# 4. How Everything Connects

```
equal.csv (raw reviews)
       │
       ▼
eda.ipynb          ← Explore: what does the data look like? Is it balanced?
       │
       ▼
preprocessing.ipynb
  ├── Clean text (remove HTML, URLs, stopwords, etc.)
  ├── Tokenize (words → numbers)
  ├── Pad sequences (make all reviews same length)
  ├── Split into train/val/test
  └── Save .npy and .pkl files to models/
       │
       ▼
lstm.ipynb
  ├── Load saved files
  ├── Build model (Embedding → BiLSTM → BiLSTM → Dense → Output)
  ├── Compile (Adam optimizer, cross-entropy loss)
  ├── Train with callbacks (EarlyStopping, Checkpoint, ReduceLR)
  └── Evaluate on test set → final accuracy
```

**Run order:** `eda.ipynb` → `preprocessing.ipynb` → `lstm.ipynb`

You MUST run `preprocessing.ipynb` before `lstm.ipynb` because lstm loads the `.npy` files that preprocessing saves.

---

# 5. Parameters Quick Reference

| Parameter | File | Value | What to change it to and why |
|---|---|---|---|
| `MAX_WORDS` | preprocessing | 30,000 | Increase to 50,000 if you have a huge, varied vocabulary. Decrease to 15,000 for faster training. |
| `MAX_LEN` | preprocessing | 100 | Increase to 200 if reviews tend to have sentiment in the second half. More memory cost. |
| `EMBEDDING_DIM` | lstm | 128 | Try 64 (faster) or 256 (more expressive). Must match what the model expects. |
| `LSTM_UNITS_1` | lstm | 128 | More units = learns richer patterns. Try 256. But more = slower and more memory. |
| `LSTM_UNITS_2` | lstm | 64 | Keep smaller than LSTM_UNITS_1 for a funnel shape. |
| `DROPOUT_RATE` | lstm | 0.3 | Increase to 0.5 if overfitting. Decrease to 0.1 if model is underfitting (val accuracy too low). |
| `BATCH_SIZE` | lstm | 64 | Try 32 (slower, noisier updates, sometimes better) or 128 (faster, smoother). |
| `EPOCHS` | lstm | 5 | EarlyStopping handles this anyway — can set to 50 and let early stopping decide. |
| `learning_rate` | lstm | 0.001 | Try 0.0005 if training is unstable. Try 0.003 if training is too slow. |
| `patience` (EarlyStopping) | lstm | 5 | Increase to 10 if you think the model needs more time to improve. |
| `factor` (ReduceLROnPlateau) | lstm | 0.5 | Try 0.3 to reduce LR more aggressively when stuck. |

---

> **You did well building this.** The architecture — balanced data, bidirectional LSTM, class weights, three-way split, callbacks — shows solid ML thinking. The main bug to fix is `expand_contractions()` which currently removes HTML instead of expanding contractions. Plugging in the actual `contractions.fix(text)` call would improve text cleaning.
