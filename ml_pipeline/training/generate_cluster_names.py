import json
import joblib

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

from ml_pipeline.config import ARTIFACTS_DIR


load_dotenv()

df = joblib.load(
    ARTIFACTS_DIR / "clustered_dataset.joblib"
)

llm = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite",
    temperature = 0
)

category_map = {}

for cluster_id in sorted(df["cluster_label"].unique()):
    
    cluster_df = df[df["cluster_label"] == cluster_id]

    samples = cluster_df.sample(
        n = min(20, len(cluster_df)),
        random_state = 42
    )

    prompt = """

You are an experienced IT Service Management consultant.

Below are 20 representative IT support tickets belonging to the SAME cluster.

Your task is to give ONE concise enterprise category name.

Requirements:
- 2 to 4 words
- Title Case
- Professional sounding
- Suitable as a support queue name
- No explanations
- No punctuations
- Return ONLY the category name
- Examples:
  Network Operations
  Security Operations
  Marketing Operations
  Data Analytics
  Software Integrations

Tickets:

"""

    for _, row in samples.iterrows():
        prompt += f"""

Subject: {row['subject']}
Body: {row['body']}

"""
        
    response = llm.invoke(
        [HumanMessage(content=prompt)]
    )

    # print(type(response.content))
    # print(response.content)

    category = response.content[0]["text"].strip()

    category_map[int(cluster_id)] = category

    print(f"Cluster {cluster_id} -> {category}")


with open(
    ARTIFACTS_DIR / "category_map.json",
    "w",
    encoding="utf-8"
) as f:
    json.dump(
        category_map,
        f,
        indent=4,
        ensure_ascii=False
    )

print("\nSaved category_map.json")
