import streamlit as st
import pandas as pd

st.set_page_config(page_title="Генератор на най-добри оферти", layout="wide")
st.title("Генератор на най-добри оферти")

st.write("Качете до 5 Excel файла с оферти (колони: Продукт, Доставчик, Цена, Количество, Дата на офертата)")

uploaded_files = st.file_uploader("Качи Excel файлове", type=["xlsx"], accept_multiple_files=True)

if uploaded_files:
    dfs = []
    for file in uploaded_files:
        try:
            df = pd.read_excel(file)
            dfs.append(df)
        except Exception as e:
            st.error(f"Грешка при зареждане на {file.name}: {e}")

    if dfs:
        # Обединяване на всички таблици
        df_all = pd.concat(dfs, ignore_index=True)
        st.subheader("Обединени оферти")
        st.dataframe(df_all)

        # Намиране на най-добрата цена за всеки продукт
        try:
            best_prices = df_all.loc[df_all.groupby("Продукт")["Цена"].idxmin()]
            st.subheader("Най-добри оферти")
            st.dataframe(best_prices)

            # Възможност за сваляне на Excel файл
            output_file = "най-добри_оферти.xlsx"
            best_prices.to_excel(output_file, index=False)
            with open(output_file, "rb") as f:
                st.download_button("Свали Excel файл с най-добри оферти", f, file_name=output_file)
        except Exception as e:
            st.error(f"Грешка при генериране на най-добрите оферти: {e}")
