import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ── Configuration ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Dashboard Ventes Sénégal 2024",
    page_icon="🇸🇳",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #0f1117; }
    .metric-card {
        background: linear-gradient(135deg, #1e2130, #252940);
        border: 1px solid #2e3250;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
    }
    .metric-value { font-size: 2rem; font-weight: 700; color: #00d4aa; }
    .metric-label { font-size: 0.85rem; color: #8891b2; margin-top: 4px; }
    .section-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #c5cae9;
        margin-bottom: 12px;
        border-left: 3px solid #00d4aa;
        padding-left: 10px;
    }
    div[data-testid="stSidebarContent"] { background-color: #161825; }
    .stTabs [data-baseweb="tab"] { color: #8891b2; }
    .stTabs [aria-selected="true"] { color: #00d4aa !important; }
</style>
""", unsafe_allow_html=True)

COULEURS = ["#00d4aa", "#7c83fd", "#f9a825", "#ef5350", "#42a5f5", "#ab47bc"]
MOIS_FR  = ["Jan","Fév","Mar","Avr","Mai","Jun","Jul","Aoû","Sep","Oct","Nov","Déc"]

# ── Chargement des données ─────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("data/sales_data.csv")
    df["date"]     = pd.to_datetime(df["date"])
    df["mois"]     = df["date"].dt.month
    df["mois_nom"] = df["date"].dt.month.map(lambda m: MOIS_FR[m-1])
    df["trimestre"]= df["date"].dt.quarter.map(lambda q: f"T{q}")
    df["semaine"]  = df["date"].dt.isocalendar().week.astype(int)
    return df

df_raw = load_data()

# ── Sidebar — Filtres ──────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🇸🇳 Ventes Sénégal 2024")
    st.markdown("---")
    st.markdown("### Filtres")

    villes_dispo     = sorted(df_raw["ville"].dropna().unique())
    categories_dispo = sorted(df_raw["categorie"].dropna().unique())
    paiements_dispo  = sorted(df_raw["mode_paiement"].dropna().unique())

    villes_sel     = st.multiselect("Villes",      villes_dispo,     default=villes_dispo)
    categories_sel = st.multiselect("Catégories",  categories_dispo, default=categories_dispo)
    paiements_sel  = st.multiselect("Paiements",   paiements_dispo,  default=paiements_dispo)

    mois_range = st.slider("Période (mois)", 1, 12, (1, 12))
    st.markdown("---")
    st.markdown("### Qualité des données")
    n_nulls = df_raw.isnull().sum().sum()
    st.metric("Valeurs manquantes", n_nulls)
    st.metric("Doublons", df_raw.duplicated().sum())

# ── Filtrage ───────────────────────────────────────────────────────────────────
df = df_raw[
    df_raw["ville"].isin(villes_sel) &
    df_raw["categorie"].isin(categories_sel) &
    df_raw["mode_paiement"].isin(paiements_sel) &
    df_raw["mois"].between(mois_range[0], mois_range[1])
].copy()

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("# 🇸🇳 Dashboard Ventes Sénégal 2024")
st.markdown(f"*{len(df):,} transactions affichées sur {len(df_raw):,} au total*")
st.markdown("---")

# ── KPIs ───────────────────────────────────────────────────────────────────────
ca_total      = df["chiffre_affaires"].sum()
nb_trans      = len(df)
panier_moyen  = df["chiffre_affaires"].mean()
nb_vendeurs   = df["vendeur"].nunique()
nb_produits   = df["produit"].nunique()
ca_par_ville  = df.groupby("ville")["chiffre_affaires"].sum().idxmax() if len(df) > 0 else "—"

k1, k2, k3, k4, k5, k6 = st.columns(6)
kpis = [
    (k1, f"{ca_total/1e9:.2f} Md", "CA Total (FCFA)"),
    (k2, f"{nb_trans:,}",          "Transactions"),
    (k3, f"{panier_moyen:,.0f}",   "Panier moyen (FCFA)"),
    (k4, str(nb_vendeurs),         "Vendeurs actifs"),
    (k5, str(nb_produits),         "Produits distincts"),
    (k6, ca_par_ville,             "Ville leader"),
]
for col, val, label in kpis:
    with col:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{val}</div>
            <div class="metric-label">{label}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("")

# ── Onglets ────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Aperçu",
    "📈 Tendances",
    "🗺️ Géographie",
    "🛒 Produits & Catégories",
    "💳 Paiements & Vendeurs",
])

# ════════════════════════════════════════════════════════════════
# TAB 1 — Aperçu
# ════════════════════════════════════════════════════════════════
with tab1:
    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown('<p class="section-title">Répartition du CA par catégorie</p>', unsafe_allow_html=True)
        cat_ca = df.groupby("categorie")["chiffre_affaires"].sum().reset_index()
        fig = px.pie(cat_ca, names="categorie", values="chiffre_affaires",
                     color_discrete_sequence=COULEURS, hole=0.45)
        fig.update_traces(textposition="outside", textinfo="percent+label")
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                          font_color="#c5cae9", showlegend=False, margin=dict(t=20,b=20,l=20,r=20))
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        st.markdown('<p class="section-title">Distribution du chiffre d\'affaires</p>', unsafe_allow_html=True)
        fig = px.histogram(df, x="chiffre_affaires", nbins=60,
                           color_discrete_sequence=["#00d4aa"])
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                          font_color="#c5cae9", xaxis_title="CA par transaction (FCFA)",
                          yaxis_title="Nombre de transactions",
                          margin=dict(t=20,b=20,l=20,r=20))
        st.plotly_chart(fig, use_container_width=True)

    st.markdown('<p class="section-title">Aperçu des données brutes</p>', unsafe_allow_html=True)
    st.dataframe(
        df[["date","produit","categorie","prix","quantite","ville","mode_paiement","vendeur","chiffre_affaires"]]
        .sort_values("date", ascending=False).head(200).reset_index(drop=True),
        use_container_width=True, height=350
    )

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<p class="section-title">Statistiques descriptives</p>', unsafe_allow_html=True)
        st.dataframe(df[["prix","quantite","chiffre_affaires"]].describe().round(2), use_container_width=True)
    with c2:
        st.markdown('<p class="section-title">Valeurs manquantes</p>', unsafe_allow_html=True)
        nulls = df.isnull().sum().reset_index()
        nulls.columns = ["Colonne", "Nulls"]
        nulls["% Manquant"] = (nulls["Nulls"] / len(df) * 100).round(2)
        st.dataframe(nulls, use_container_width=True)
    with c3:
        st.markdown('<p class="section-title">Types de données</p>', unsafe_allow_html=True)
        types_df = df.dtypes.reset_index()
        types_df.columns = ["Colonne", "Type"]
        st.dataframe(types_df, use_container_width=True)

# ════════════════════════════════════════════════════════════════
# TAB 2 — Tendances
# ════════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<p class="section-title">Évolution mensuelle du CA</p>', unsafe_allow_html=True)
    monthly = (df.groupby("mois")["chiffre_affaires"]
                 .sum().reindex(range(mois_range[0], mois_range[1]+1))
                 .reset_index())
    monthly.columns = ["mois", "ca"]
    monthly["mois_nom"] = monthly["mois"].map(lambda m: MOIS_FR[m-1])

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=monthly["mois_nom"], y=monthly["ca"],
        mode="lines+markers+text",
        line=dict(color="#00d4aa", width=3),
        marker=dict(size=8, color="#00d4aa"),
        fill="tozeroy", fillcolor="rgba(0,212,170,0.08)",
        text=[f"{v/1e6:.0f}M" for v in monthly["ca"]],
        textposition="top center", textfont=dict(color="#00d4aa", size=11),
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font_color="#c5cae9", xaxis_title="Mois", yaxis_title="CA (FCFA)",
        margin=dict(t=10,b=20,l=20,r=20), height=320,
        xaxis=dict(gridcolor="#1e2130"), yaxis=dict(gridcolor="#1e2130"),
    )
    st.plotly_chart(fig, use_container_width=True)

    col_l, col_r = st.columns(2)

    with col_l:
        st.markdown('<p class="section-title">CA mensuel par catégorie</p>', unsafe_allow_html=True)
        mc = df.groupby(["mois","categorie"])["chiffre_affaires"].sum().reset_index()
        mc["mois_nom"] = mc["mois"].map(lambda m: MOIS_FR[m-1])
        fig = px.bar(mc, x="mois_nom", y="chiffre_affaires", color="categorie",
                     color_discrete_sequence=COULEURS, barmode="stack")
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                          font_color="#c5cae9", xaxis_title="Mois",
                          yaxis_title="CA (FCFA)", legend_title="Catégorie",
                          margin=dict(t=10,b=20,l=20,r=20), height=320,
                          xaxis=dict(gridcolor="#1e2130"), yaxis=dict(gridcolor="#1e2130"))
        st.plotly_chart(fig, use_container_width=True)

    with col_r:
        st.markdown('<p class="section-title">Nombre de transactions par mois</p>', unsafe_allow_html=True)
        mt = df.groupby("mois").size().reindex(range(mois_range[0], mois_range[1]+1)).reset_index()
        mt.columns = ["mois","nb"]
        mt["mois_nom"] = mt["mois"].map(lambda m: MOIS_FR[m-1])
        fig = px.bar(mt, x="mois_nom", y="nb", color_discrete_sequence=["#7c83fd"])
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                          font_color="#c5cae9", xaxis_title="Mois",
                          yaxis_title="Transactions", margin=dict(t=10,b=20,l=20,r=20), height=320,
                          xaxis=dict(gridcolor="#1e2130"), yaxis=dict(gridcolor="#1e2130"))
        st.plotly_chart(fig, use_container_width=True)

    st.markdown('<p class="section-title">Saisonnalité — événements sénégalais</p>', unsafe_allow_html=True)
    evenements = {3:"Ramadan", 4:"Korité", 6:"Tabaski", 8:"Magal de Touba",
                  9:"Gamou", 10:"Rentrée scolaire", 12:"Fin d'année"}
    monthly["evenement"] = monthly["mois"].map(evenements)
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=monthly["mois_nom"], y=monthly["ca"],
        marker_color=["#f9a825" if m in evenements else "#00d4aa" for m in monthly["mois"]],
        text=[f"<b>{evenements[m]}</b>" if m in evenements else "" for m in monthly["mois"]],
        textposition="outside",
    ))
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      font_color="#c5cae9", xaxis_title="Mois", yaxis_title="CA (FCFA)",
                      margin=dict(t=20,b=20,l=20,r=20), height=320,
                      xaxis=dict(gridcolor="#1e2130"), yaxis=dict(gridcolor="#1e2130"))
    st.plotly_chart(fig, use_container_width=True)

# ════════════════════════════════════════════════════════════════
# TAB 3 — Géographie
# ════════════════════════════════════════════════════════════════
with tab3:
    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown('<p class="section-title">CA par ville</p>', unsafe_allow_html=True)
        vc = df.groupby("ville")["chiffre_affaires"].sum().sort_values(ascending=True).reset_index()
        fig = px.bar(vc, x="chiffre_affaires", y="ville", orientation="h",
                     color="chiffre_affaires", color_continuous_scale="teal",
                     text=vc["chiffre_affaires"].map(lambda v: f"{v/1e6:.0f}M"))
        fig.update_traces(textposition="outside")
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                          font_color="#c5cae9", xaxis_title="CA (FCFA)", yaxis_title="",
                          showlegend=False, coloraxis_showscale=False,
                          margin=dict(t=10,b=20,l=20,r=60), height=320)
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        st.markdown('<p class="section-title">Transactions par ville</p>', unsafe_allow_html=True)
        vt = df.groupby("ville").size().reset_index(name="nb")
        fig = px.pie(vt, names="ville", values="nb",
                     color_discrete_sequence=COULEURS, hole=0.4)
        fig.update_traces(textposition="outside", textinfo="percent+label")
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                          font_color="#c5cae9", showlegend=False,
                          margin=dict(t=10,b=20,l=20,r=20), height=320)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown('<p class="section-title">CA par ville et catégorie</p>', unsafe_allow_html=True)
    vcat = df.groupby(["ville","categorie"])["chiffre_affaires"].sum().reset_index()
    fig = px.bar(vcat, x="ville", y="chiffre_affaires", color="categorie",
                 barmode="group", color_discrete_sequence=COULEURS)
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      font_color="#c5cae9", xaxis_title="Ville", yaxis_title="CA (FCFA)",
                      legend_title="Catégorie", margin=dict(t=10,b=20,l=20,r=20), height=380,
                      xaxis=dict(gridcolor="#1e2130"), yaxis=dict(gridcolor="#1e2130"))
    st.plotly_chart(fig, use_container_width=True)

    st.markdown('<p class="section-title">Panier moyen par ville</p>', unsafe_allow_html=True)
    pm = df.groupby("ville")["chiffre_affaires"].mean().reset_index()
    pm.columns = ["ville","panier_moyen"]
    fig = px.bar(pm.sort_values("panier_moyen", ascending=False),
                 x="ville", y="panier_moyen", color_discrete_sequence=["#f9a825"],
                 text=pm.sort_values("panier_moyen",ascending=False)["panier_moyen"].map(lambda v: f"{v:,.0f}"))
    fig.update_traces(textposition="outside")
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      font_color="#c5cae9", xaxis_title="Ville", yaxis_title="Panier moyen (FCFA)",
                      margin=dict(t=10,b=20,l=20,r=20), height=300,
                      xaxis=dict(gridcolor="#1e2130"), yaxis=dict(gridcolor="#1e2130"))
    st.plotly_chart(fig, use_container_width=True)

# ════════════════════════════════════════════════════════════════
# TAB 4 — Produits & Catégories
# ════════════════════════════════════════════════════════════════
with tab4:
    col_a, col_b = st.columns([3, 2])

    with col_a:
        st.markdown('<p class="section-title">Top 15 produits par CA</p>', unsafe_allow_html=True)
        top15 = df.groupby("produit")["chiffre_affaires"].sum().sort_values(ascending=False).head(15).reset_index()
        fig = px.bar(top15.sort_values("chiffre_affaires"), x="chiffre_affaires", y="produit",
                     orientation="h", color="chiffre_affaires", color_continuous_scale="teal",
                     text=top15.sort_values("chiffre_affaires")["chiffre_affaires"].map(lambda v: f"{v/1e6:.0f}M"))
        fig.update_traces(textposition="outside")
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                          font_color="#c5cae9", xaxis_title="CA (FCFA)", yaxis_title="",
                          showlegend=False, coloraxis_showscale=False,
                          margin=dict(t=10,b=20,l=20,r=60), height=430)
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        st.markdown('<p class="section-title">CA par catégorie</p>', unsafe_allow_html=True)
        cat = df.groupby("categorie")["chiffre_affaires"].sum().sort_values(ascending=False).reset_index()
        fig = px.bar(cat, x="categorie", y="chiffre_affaires",
                     color="categorie", color_discrete_sequence=COULEURS,
                     text=cat["chiffre_affaires"].map(lambda v: f"{v/1e6:.0f}M"))
        fig.update_traces(textposition="outside")
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                          font_color="#c5cae9", xaxis_title="", yaxis_title="CA (FCFA)",
                          showlegend=False, margin=dict(t=10,b=20,l=20,r=20), height=430,
                          xaxis=dict(tickangle=-30), yaxis=dict(gridcolor="#1e2130"))
        st.plotly_chart(fig, use_container_width=True)

    st.markdown('<p class="section-title">Prix moyen et quantité moyenne par catégorie</p>', unsafe_allow_html=True)
    catstat = df.groupby("categorie").agg(
        prix_moyen=("prix","mean"),
        qte_moyenne=("quantite","mean"),
        nb_transactions=("chiffre_affaires","count")
    ).reset_index().round(1)
    fig = px.scatter(catstat, x="prix_moyen", y="qte_moyenne", size="nb_transactions",
                     color="categorie", color_discrete_sequence=COULEURS,
                     hover_name="categorie", size_max=60,
                     labels={"prix_moyen":"Prix moyen (FCFA)","qte_moyenne":"Quantité moyenne"})
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      font_color="#c5cae9", margin=dict(t=10,b=20,l=20,r=20), height=350,
                      xaxis=dict(gridcolor="#1e2130"), yaxis=dict(gridcolor="#1e2130"))
    st.plotly_chart(fig, use_container_width=True)

    st.markdown('<p class="section-title">Évolution mensuelle par catégorie</p>', unsafe_allow_html=True)
    cat_m = df.groupby(["mois","categorie"])["chiffre_affaires"].sum().reset_index()
    cat_m["mois_nom"] = cat_m["mois"].map(lambda m: MOIS_FR[m-1])
    fig = px.line(cat_m, x="mois_nom", y="chiffre_affaires", color="categorie",
                  color_discrete_sequence=COULEURS, markers=True)
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      font_color="#c5cae9", xaxis_title="Mois", yaxis_title="CA (FCFA)",
                      legend_title="Catégorie", margin=dict(t=10,b=20,l=20,r=20), height=350,
                      xaxis=dict(gridcolor="#1e2130"), yaxis=dict(gridcolor="#1e2130"))
    st.plotly_chart(fig, use_container_width=True)

# ════════════════════════════════════════════════════════════════
# TAB 5 — Paiements & Vendeurs
# ════════════════════════════════════════════════════════════════
with tab5:
    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown('<p class="section-title">Répartition par mode de paiement</p>', unsafe_allow_html=True)
        pay = df["mode_paiement"].value_counts().reset_index()
        pay.columns = ["mode","nb"]
        fig = px.pie(pay, names="mode", values="nb",
                     color_discrete_sequence=COULEURS, hole=0.4)
        fig.update_traces(textposition="outside", textinfo="percent+label")
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                          font_color="#c5cae9", showlegend=False,
                          margin=dict(t=10,b=20,l=20,r=20), height=320)
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        st.markdown('<p class="section-title">CA par mode de paiement</p>', unsafe_allow_html=True)
        pay_ca = df.groupby("mode_paiement")["chiffre_affaires"].sum().sort_values(ascending=True).reset_index()
        fig = px.bar(pay_ca, x="chiffre_affaires", y="mode_paiement", orientation="h",
                     color="chiffre_affaires", color_continuous_scale="teal",
                     text=pay_ca["chiffre_affaires"].map(lambda v: f"{v/1e6:.0f}M"))
        fig.update_traces(textposition="outside")
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                          font_color="#c5cae9", xaxis_title="CA (FCFA)", yaxis_title="",
                          showlegend=False, coloraxis_showscale=False,
                          margin=dict(t=10,b=20,l=20,r=60), height=320)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown('<p class="section-title">Mode de paiement par ville</p>', unsafe_allow_html=True)
    pv = df.groupby(["ville","mode_paiement"]).size().reset_index(name="nb")
    fig = px.bar(pv, x="ville", y="nb", color="mode_paiement",
                 barmode="stack", color_discrete_sequence=COULEURS)
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      font_color="#c5cae9", xaxis_title="Ville", yaxis_title="Transactions",
                      legend_title="Mode de paiement", margin=dict(t=10,b=20,l=20,r=20), height=320,
                      yaxis=dict(gridcolor="#1e2130"))
    st.plotly_chart(fig, use_container_width=True)

    st.markdown('<p class="section-title">Top 20 vendeurs par CA</p>', unsafe_allow_html=True)
    top_v = df.groupby("vendeur")["chiffre_affaires"].sum().sort_values(ascending=False).head(20).reset_index()
    fig = px.bar(top_v, x="vendeur", y="chiffre_affaires",
                 color="chiffre_affaires", color_continuous_scale="teal",
                 text=top_v["chiffre_affaires"].map(lambda v: f"{v/1e6:.1f}M"))
    fig.update_traces(textposition="outside")
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      font_color="#c5cae9", xaxis_title="Vendeur", yaxis_title="CA (FCFA)",
                      showlegend=False, coloraxis_showscale=False,
                      margin=dict(t=10,b=20,l=20,r=20), height=340,
                      xaxis=dict(gridcolor="#1e2130"), yaxis=dict(gridcolor="#1e2130"))
    st.plotly_chart(fig, use_container_width=True)

    col_l, col_r = st.columns(2)
    with col_l:
        st.markdown('<p class="section-title">Distribution du CA par vendeur</p>', unsafe_allow_html=True)
        vend_ca = df.groupby("vendeur")["chiffre_affaires"].sum()
        fig = px.histogram(vend_ca, nbins=30, color_discrete_sequence=["#ab47bc"])
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                          font_color="#c5cae9", xaxis_title="CA par vendeur (FCFA)",
                          yaxis_title="Nombre de vendeurs",
                          margin=dict(t=10,b=20,l=20,r=20), height=280,
                          xaxis=dict(gridcolor="#1e2130"), yaxis=dict(gridcolor="#1e2130"))
        st.plotly_chart(fig, use_container_width=True)

    with col_r:
        st.markdown('<p class="section-title">Transactions par vendeur (top 10)</p>', unsafe_allow_html=True)
        vend_t = df.groupby("vendeur").size().sort_values(ascending=False).head(10).reset_index()
        vend_t.columns = ["vendeur","nb"]
        fig = px.bar(vend_t, x="vendeur", y="nb", color_discrete_sequence=["#42a5f5"],
                     text="nb")
        fig.update_traces(textposition="outside")
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                          font_color="#c5cae9", xaxis_title="Vendeur", yaxis_title="Transactions",
                          margin=dict(t=10,b=20,l=20,r=20), height=280,
                          xaxis=dict(gridcolor="#1e2130"), yaxis=dict(gridcolor="#1e2130"))
        st.plotly_chart(fig, use_container_width=True)

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<p style='text-align:center;color:#8891b2;font-size:0.8rem;'>"
    "Dashboard Ventes Sénégal 2024 — Oumaro Titans DJIGUIMDE — "
    "45 965 transactions | CA Total : 3,49 Md FCFA"
    "</p>",
    unsafe_allow_html=True
)
