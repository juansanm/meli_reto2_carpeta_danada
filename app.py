import pandas as pd
import streamlit as st
from pathlib import Path
import io    
st.set_page_config(page_title="Consulta de similitud", layout="wide")
@st.cache_data
def load_df(path: Path):
    if path.suffix == ".csv":
        return pd.read_csv(path)
    elif path.suffix == ".parquet":
        return pd.read_parquet(path)
    else:
        raise ValueError("Use .csv o .parquet")
DATA_PATH = Path("df_final.csv")
df = load_df(DATA_PATH)
st.title("Buscador de Items Similares")
csv_buffer = io.StringIO()
df.to_csv(csv_buffer, index=False)
st.download_button(
    label="⬇️ Descargar CSV completo",
    data=csv_buffer.getvalue(),
    file_name="df_final.csv",
    mime="text/csv",
    help="Exporta todo el DataFrame a un archivo CSV"
)
ite_options = df["ITE_ITEM_TITLE1"].sort_values().unique()
selected_title = st.selectbox("Título (ITE_ITEM_TITLE1)", ite_options, index=0)
resultados = df[df["ITE_ITEM_TITLE1"] == selected_title]
st.subheader(f"Coincidencias para «{selected_title}»")
st.dataframe(
    resultados[["ITE_ITEM_TITLE2", "Score_Similitud"]]
    .reset_index(drop=True)
    .style.format({"Score_Similitud": "{:.4f}"}),
    use_container_width=True
)