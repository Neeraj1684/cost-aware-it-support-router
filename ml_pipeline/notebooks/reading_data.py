import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("synthetic_it_support_tickets.csv")

# print(df.head(10))
# print(df.info())
# print("\n\n",df.shape)

# print("\n\nDuplicated values:-\n",df.duplicated().sum())

# print("\nUnique values:-\n",df.nunique())

# print("\nSummary Statistics:-\n",df.describe())

sns.histplot(df['resolution_time_hours'], bins=20)
plt.show()



