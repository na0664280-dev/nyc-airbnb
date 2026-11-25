import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="NYC Airbnb", layout="wide")
st.title("🏙️ تحليل أسعار Airbnb في نيويورك")

df = pd.read_csv("clean.csv")
t1, t2, t3 = st.tabs(["نظرة عامة", "الاكتشافات", "المنتج"])

with t1:
    area = st.selectbox("المنطقة", ["الكل"] + sorted(df["neighbourhood_group"].unique()))
    d = df if area == "الكل" else df[df["neighbourhood_group"] == area]
    c1, c2, c3 = st.columns(3)
    c1.metric("عدد الإعلانات", f"{len(d):,}")
    c2.metric("متوسط السعر", f"{d['price'].mean():.0f}")
    c3.metric("وسيط السعر", f"{d['price'].median():.0f}")
    st.dataframe(d.head(20))

with t2:
    a = df.groupby("neighbourhood_group")["price"].mean().sort_values().reset_index()
    st.plotly_chart(px.bar(a, x="neighbourhood_group", y="price"))
    st.write("Manhattan الأغلى بمتوسط ≈ 180، وBronx الأرخص ≈ 85.")

    b = df.groupby("room_type")["price"].median().reset_index()
    st.plotly_chart(px.bar(b, x="room_type", y="price"))
    st.write("الشقة الكاملة أغلى من الغرفة الخاصة بحوالي 2.5 مرة.")

    c = df["neighbourhood_group"].value_counts().reset_index()
    st.plotly_chart(px.bar(c, x="neighbourhood_group", y="count"))
    st.write("Manhattan وBrooklyn فيهم أغلب الإعلانات.")

    st.subheader("أهم الاكتشافات والتوصيات")
    st.write("- المنطقة ونوع الغرفة أكثر عاملين يأثرون في السعر.")

with t3:
    st.subheader("🔮 اعرف السعر المتوقع")
    g = st.selectbox("المنطقة ", sorted(df["neighbourhood_group"].unique()))
    r = st.selectbox("نوع الغرفة", sorted(df["room_type"].unique()))
    m = df[(df["neighbourhood_group"] == g) & (df["room_type"] == r)]
    if len(m) > 0:
        st.metric("السعر المتوقع (الوسيط)", f"{m['price'].median():.0f}")
        st.write(f"محسوب من {len(m):,} إعلان مشابه في {g} من نوع {r}.")
    else:
        st.warning("ما فيه بيانات لهذا الاختيار")
