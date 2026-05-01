import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ── Configuration ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="VentesShield · Dashboard Sénégal 2024",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

:root {
    --bg: #0a0d14;
    --surface: #111520;
    --surface2: #161c2e;
    --border: #1e2a42;
    --accent: #00e5ff;
    --accent2: #ff4757;
    --accent3: #ffd32a;
    --text: #e8edf5;
    --muted: #6b7a99;
    --green: #2ed573;
}

html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'Inter', sans-serif;
}

[data-testid="stSidebar"] {
    background-color: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] * { color: var(--text) !important; }

h1, h2, h3 { font-weight: 800 !important; }

.stSelectbox > div > div,
.stSlider > div,
.stNumberInput > div {
    background-color: var(--surface2) !important;
    border-color: var(--border) !important;
    color: var(--text) !important;
}

.metric-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
    position: relative;
    overflow: hidden;
}
.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: var(--accent);
}
.metric-label {
    font-size: 0.72rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--muted);
    font-family: 'JetBrains Mono', monospace;
}
.metric-value {
    font-size: 1.8rem;
    font-weight: 800;
    line-height: 1.1;
    margin-top: 0.3rem;
    color: var(--accent);
}

.section-title {
    font-size: 0.7rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--muted);
    font-family: 'JetBrains Mono', monospace;
    margin-bottom: 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid var(--border);
}

.stTabs [data-baseweb="tab-list"] { background: var(--surface) !important; border-radius: 10px; padding: 4px; }
.stTabs [data-baseweb="tab"] { color: var(--muted) !important; font-weight: 600 !important; }
.stTabs [aria-selected="true"] { background: var(--surface2) !important; color: var(--accent) !important; border-radius: 8px !important; }

[data-testid="stMarkdownContainer"] p { color: var(--text); }

div[data-testid="stExpander"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
}

::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

PLOTLY_LAYOUT = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family='Inter, sans-serif', color='#e8edf5'),
    margin=dict(l=10, r=10, t=40, b=10),
    xaxis=dict(gridcolor='#1e2a42', linecolor='#1e2a42'),
    yaxis=dict(gridcolor='#1e2a42', linecolor='#1e2a42'),
)

COULEURS = ["#00e5ff", "#2ed573", "#ffd32a", "#ff4757", "#7c83fd", "#ab47bc"]
MOIS_FR  = ["Jan","Fév","Mar","Avr","Mai","Jun","Jul","Aoû","Sep","Oct","Nov","Déc"]

# ── Chargement des données ─────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("data/sales_data.csv")
    df["date"]      = pd.to_datetime(df["date"])
    df["mois"]      = df["date"].dt.month
    df["mois_nom"]  = df["date"].dt.month.map(lambda m: MOIS_FR[m-1])
    df["trimestre"] = df["date"].dt.quarter.map(lambda q: f"T{q}")
    df["semaine"]   = df["date"].dt.isocalendar().week.astype(int)
    return df

df_raw = load_data()

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding: 0.5rem 0 1.5rem 0;">
        <div style="font-size:1.6rem; font-weight:800; color:#00e5ff; letter-spacing:-0.02em;">VentesShield</div>
        <div style="font-size:0.7rem; color:#6b7a99; letter-spacing:0.15em; text-transform:uppercase; font-family:'JetBrains Mono',monospace;">Dashboard · Sénégal 2024</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">Filtres globaux</div>', unsafe_allow_html=True)

    villes_dispo     = sorted(df_raw["ville"].dropna().unique())
    categories_dispo = sorted(df_raw["categorie"].dropna().unique())
    paiements_dispo  = sorted(df_raw["mode_paiement"].dropna().unique())

    villes_sel     = st.multiselect("Ville",       villes_dispo,     default=villes_dispo)
    categories_sel = st.multiselect("Catégorie",   categories_dispo, default=categories_dispo)
    paiements_sel  = st.multiselect("Paiement",    paiements_dispo,  default=paiements_dispo)
    mois_range     = st.slider("Période (mois)", 1, 12, (1, 12))

    st.markdown("---")
    st.markdown(f"""
    <div style="font-size:0.7rem; color:#6b7a99; font-family:'JetBrains Mono',monospace; line-height:1.8;">
        Dataset · {len(df_raw):,} transactions<br>
        Période · 2024<br>
        Contexte · Sénégal
    </div>
    """, unsafe_allow_html=True)

# ── Filtrage ───────────────────────────────────────────────────────────────────
df = df_raw[
    df_raw["ville"].isin(villes_sel) &
    df_raw["categorie"].isin(categories_sel) &
    df_raw["mode_paiement"].isin(paiements_sel) &
    df_raw["mois"].between(mois_range[0], mois_range[1])
].copy()

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown('<h1 style="color:#00e5ff; margin-bottom:0.2rem;">Dashboard Ventes</h1>', unsafe_allow_html=True)
st.markdown('<p style="color:#6b7a99; margin-bottom:2rem; font-family:\'JetBrains Mono\',monospace; font-size:0.8rem;">Sénégal 2024 · Analyse commerciale</p>', unsafe_allow_html=True)

# ── KPIs ───────────────────────────────────────────────────────────────────────
ca_total     = df["chiffre_affaires"].sum()
nb_trans     = len(df)
panier_moyen = df["chiffre_affaires"].mean()
nb_vendeurs  = df["vendeur"].nunique()
nb_produits  = df["produit"].nunique()
ville_leader = df.groupby("ville")["chiffre_affaires"].sum().idxmax() if len(df) > 0 else "—"

k1, k2, k3, k4, k5, k6 = st.columns(6)
kpis = [
    (k1, f"{ca_total/1e9:.2f} Md", "CA Total (FCFA)"),
    (k2, f"{nb_trans:,}",          "Transactions"),
    (k3, f"{panier_moyen:,.0f}",   "Panier moyen (FCFA)"),
    (k4, str(nb_vendeurs),         "Vendeurs actifs"),
    (k5, str(nb_produits),         "Produits distincts"),
    (k6, ville_leader,             "Ville leader"),
]
for col, val, label in kpis:
    with col:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{val}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Onglets ────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Aperçu",
    "Tendances",
    "Géographie",
    "Produits & Catégories",
    "Paiements & Vendeurs",
])

# ════════════════════════════════════════════════════════════════
# TAB 1 — Aperçu
# ════════════════════════════════════════════════════════════════
with tab1:
    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown('<div class="section-title">Répartition du CA par catégorie</div>', unsafe_allow_html=True)
        cat_ca = df.groupby("categorie")["chiffre_affaires"].sum().reset_index()
        fig = px.pie(cat_ca, names="categorie", values="chiffre_affaires",
                     color_discrete_sequence=COULEURS, hole=0.45)
        fig.update_traces(textposition="outside", textinfo="percent+label")
        fig.update_layout(**PLOTLY_LAYOUT, showlegend=False, height=300)
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        st.markdown('<div class="section-title">Distribution du chiffre d\'affaires</div>', unsafe_allow_html=True)
        fig = px.histogram(df, x="chiffre_affaires", nbins=60,
                           color_discrete_sequence=["#00e5ff"])
        fig.update_layout(**PLOTLY_LAYOUT, height=300,
                          xaxis_title="CA par transaction (FCFA)",
                          yaxis_title="Nombre de transactions")
        st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="section-title">Dernières transactions</div>', unsafe_allow_html=True)
    st.dataframe(
        df[["date","produit","categorie","prix","quantite","ville","mode_paiement","vendeur","chiffre_affaires"]]
        .sort_values("date", ascending=False).head(200).reset_index(drop=True),
        use_container_width=True, height=350, hide_index=True
    )

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<div class="section-title">Statistiques descriptives</div>', unsafe_allow_html=True)
        st.dataframe(df[["prix","quantite","chiffre_affaires"]].describe().round(2), use_container_width=True)
    with c2:
        st.markdown('<div class="section-title">Valeurs manquantes</div>', unsafe_allow_html=True)
        nulls = df.isnull().sum().reset_index()
        nulls.columns = ["Colonne", "Nulls"]
        nulls["% Manquant"] = (nulls["Nulls"] / len(df) * 100).round(2)
        st.dataframe(nulls, use_container_width=True, hide_index=True)
    with c3:
        st.markdown('<div class="section-title">Types de données</div>', unsafe_allow_html=True)
        types_df = df.dtypes.reset_index()
        types_df.columns = ["Colonne", "Type"]
        st.dataframe(types_df, use_container_width=True, hide_index=True)

# ════════════════════════════════════════════════════════════════
# TAB 2 — Tendances
# ════════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="section-title">Évolution mensuelle du CA</div>', unsafe_allow_html=True)
    monthly = (df.groupby("mois")["chiffre_affaires"]
                 .sum().reindex(range(mois_range[0], mois_range[1]+1))
                 .reset_index())
    monthly.columns = ["mois", "ca"]
    monthly["mois_nom"] = monthly["mois"].map(lambda m: MOIS_FR[m-1])

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=monthly["mois_nom"], y=monthly["ca"],
        mode="lines+markers+text",
        line=dict(color="#00e5ff", width=2),
        marker=dict(size=7, color="#00e5ff"),
        fill="tozeroy", fillcolor="rgba(0,229,255,0.07)",
        text=[f"{v/1e6:.0f}M" for v in monthly["ca"]],
        textposition="top center", textfont=dict(color="#00e5ff", size=11),
    ))
    fig.update_layout(**PLOTLY_LAYOUT, height=300,
                      xaxis_title="Mois", yaxis_title="CA (FCFA)")
    st.plotly_chart(fig, use_container_width=True)

    col_l, col_r = st.columns(2)

    with col_l:
        st.markdown('<div class="section-title">CA mensuel par catégorie</div>', unsafe_allow_html=True)
        mc = df.groupby(["mois","categorie"])["chiffre_affaires"].sum().reset_index()
        mc["mois_nom"] = mc["mois"].map(lambda m: MOIS_FR[m-1])
        fig = px.bar(mc, x="mois_nom", y="chiffre_affaires", color="categorie",
                     color_discrete_sequence=COULEURS, barmode="stack")
        fig.update_layout(**PLOTLY_LAYOUT, height=300,
                          xaxis_title="Mois", yaxis_title="CA (FCFA)", legend_title="Catégorie")
        st.plotly_chart(fig, use_container_width=True)

    with col_r:
        st.markdown('<div class="section-title">Transactions par mois</div>', unsafe_allow_html=True)
        mt = df.groupby("mois").size().reindex(range(mois_range[0], mois_range[1]+1)).reset_index()
        mt.columns = ["mois","nb"]
        mt["mois_nom"] = mt["mois"].map(lambda m: MOIS_FR[m-1])
        fig = px.bar(mt, x="mois_nom", y="nb", color_discrete_sequence=["#2ed573"])
        fig.update_layout(**PLOTLY_LAYOUT, height=300,
                          xaxis_title="Mois", yaxis_title="Transactions")
        st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="section-title">Saisonnalité — événements sénégalais</div>', unsafe_allow_html=True)
    evenements = {3:"Ramadan", 4:"Korité", 6:"Tabaski", 8:"Magal de Touba",
                  9:"Gamou", 10:"Rentrée scolaire", 12:"Fin d'année"}
    monthly["evenement"] = monthly["mois"].map(evenements)
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=monthly["mois_nom"], y=monthly["ca"],
        marker_color=["#ffd32a" if m in evenements else "#00e5ff" for m in monthly["mois"]],
        text=[f"{evenements[m]}" if m in evenements else "" for m in monthly["mois"]],
        textposition="outside",
        textfont=dict(family='JetBrains Mono', size=11)
    ))
    fig.update_layout(**PLOTLY_LAYOUT, height=300,
                      xaxis_title="Mois", yaxis_title="CA (FCFA)")
    st.plotly_chart(fig, use_container_width=True)

# ════════════════════════════════════════════════════════════════
# TAB 3 — Géographie
# ════════════════════════════════════════════════════════════════
with tab3:
    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown('<div class="section-title">CA par ville</div>', unsafe_allow_html=True)
        vc = df.groupby("ville")["chiffre_affaires"].sum().sort_values(ascending=True).reset_index()
        fig = go.Figure(go.Bar(
            y=vc["ville"], x=vc["chiffre_affaires"], orientation="h",
            marker=dict(color=vc["chiffre_affaires"],
                        colorscale=[[0, "#2ed573"],[0.5, "#ffd32a"],[1, "#00e5ff"]]),
            text=[f"{v/1e6:.0f}M" for v in vc["chiffre_affaires"]],
            textposition="outside",
            textfont=dict(family='JetBrains Mono', size=11)
        ))
        fig.update_layout(**PLOTLY_LAYOUT, height=300, xaxis_title="CA (FCFA)")
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        st.markdown('<div class="section-title">Transactions par ville</div>', unsafe_allow_html=True)
        vt = df.groupby("ville").size().reset_index(name="nb")
        fig = px.pie(vt, names="ville", values="nb",
                     color_discrete_sequence=COULEURS, hole=0.45)
        fig.update_traces(textposition="outside", textinfo="percent+label")
        fig.update_layout(**PLOTLY_LAYOUT, showlegend=False, height=300)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="section-title">CA par ville et catégorie</div>', unsafe_allow_html=True)
    vcat = df.groupby(["ville","categorie"])["chiffre_affaires"].sum().reset_index()
    fig = px.bar(vcat, x="ville", y="chiffre_affaires", color="categorie",
                 barmode="group", color_discrete_sequence=COULEURS)
    fig.update_layout(**PLOTLY_LAYOUT, height=350,
                      xaxis_title="Ville", yaxis_title="CA (FCFA)", legend_title="Catégorie")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="section-title">Panier moyen par ville</div>', unsafe_allow_html=True)
    pm = df.groupby("ville")["chiffre_affaires"].mean().sort_values(ascending=True).reset_index()
    pm.columns = ["ville","panier_moyen"]
    fig = go.Figure(go.Bar(
        y=pm["ville"], x=pm["panier_moyen"], orientation="h",
        marker_color="#ffd32a",
        text=[f"{v:,.0f}" for v in pm["panier_moyen"]],
        textposition="outside",
        textfont=dict(family='JetBrains Mono', size=11)
    ))
    fig.update_layout(**PLOTLY_LAYOUT, height=280, xaxis_title="Panier moyen (FCFA)")
    st.plotly_chart(fig, use_container_width=True)

# ════════════════════════════════════════════════════════════════
# TAB 4 — Produits & Catégories
# ════════════════════════════════════════════════════════════════
with tab4:
    col_a, col_b = st.columns([3, 2])

    with col_a:
        st.markdown('<div class="section-title">Top 15 produits par CA</div>', unsafe_allow_html=True)
        top15 = df.groupby("produit")["chiffre_affaires"].sum().sort_values(ascending=False).head(15).reset_index()
        top15_sorted = top15.sort_values("chiffre_affaires")
        fig = go.Figure(go.Bar(
            y=top15_sorted["produit"], x=top15_sorted["chiffre_affaires"], orientation="h",
            marker=dict(color=top15_sorted["chiffre_affaires"],
                        colorscale=[[0, "#2ed573"],[1, "#00e5ff"]]),
            text=[f"{v/1e6:.0f}M" for v in top15_sorted["chiffre_affaires"]],
            textposition="outside",
            textfont=dict(family='JetBrains Mono', size=11)
        ))
        fig.update_layout(**PLOTLY_LAYOUT, height=430, xaxis_title="CA (FCFA)")
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        st.markdown('<div class="section-title">CA par catégorie</div>', unsafe_allow_html=True)
        cat = df.groupby("categorie")["chiffre_affaires"].sum().sort_values(ascending=False).reset_index()
        fig = go.Figure(go.Bar(
            x=cat["categorie"], y=cat["chiffre_affaires"],
            marker_color=COULEURS[:len(cat)],
            text=[f"{v/1e6:.0f}M" for v in cat["chiffre_affaires"]],
            textposition="outside",
            textfont=dict(family='JetBrains Mono', size=11)
        ))
        fig.update_layout(**PLOTLY_LAYOUT, height=430,
                          xaxis_title="", yaxis_title="CA (FCFA)")
        fig.update_xaxes(tickangle=-30)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="section-title">Prix moyen vs quantité moyenne par catégorie</div>', unsafe_allow_html=True)
    catstat = df.groupby("categorie").agg(
        prix_moyen=("prix","mean"),
        qte_moyenne=("quantite","mean"),
        nb_transactions=("chiffre_affaires","count")
    ).reset_index().round(1)
    fig = px.scatter(catstat, x="prix_moyen", y="qte_moyenne", size="nb_transactions",
                     color="categorie", color_discrete_sequence=COULEURS,
                     hover_name="categorie", size_max=60,
                     labels={"prix_moyen":"Prix moyen (FCFA)","qte_moyenne":"Quantité moyenne"})
    fig.update_layout(**PLOTLY_LAYOUT, height=320)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="section-title">Évolution mensuelle par catégorie</div>', unsafe_allow_html=True)
    cat_m = df.groupby(["mois","categorie"])["chiffre_affaires"].sum().reset_index()
    cat_m["mois_nom"] = cat_m["mois"].map(lambda m: MOIS_FR[m-1])
    fig = px.line(cat_m, x="mois_nom", y="chiffre_affaires", color="categorie",
                  color_discrete_sequence=COULEURS, markers=True)
    fig.update_layout(**PLOTLY_LAYOUT, height=320,
                      xaxis_title="Mois", yaxis_title="CA (FCFA)", legend_title="Catégorie")
    st.plotly_chart(fig, use_container_width=True)

# ════════════════════════════════════════════════════════════════
# TAB 5 — Paiements & Vendeurs
# ════════════════════════════════════════════════════════════════
with tab5:
    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown('<div class="section-title">Répartition par mode de paiement</div>', unsafe_allow_html=True)
        pay = df["mode_paiement"].value_counts().reset_index()
        pay.columns = ["mode","nb"]
        fig = px.pie(pay, names="mode", values="nb",
                     color_discrete_sequence=COULEURS, hole=0.45)
        fig.update_traces(textposition="outside", textinfo="percent+label")
        fig.update_layout(**PLOTLY_LAYOUT, showlegend=False, height=300)
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        st.markdown('<div class="section-title">CA par mode de paiement</div>', unsafe_allow_html=True)
        pay_ca = df.groupby("mode_paiement")["chiffre_affaires"].sum().sort_values(ascending=True).reset_index()
        fig = go.Figure(go.Bar(
            y=pay_ca["mode_paiement"], x=pay_ca["chiffre_affaires"], orientation="h",
            marker=dict(color=pay_ca["chiffre_affaires"],
                        colorscale=[[0, "#2ed573"],[1, "#00e5ff"]]),
            text=[f"{v/1e6:.0f}M" for v in pay_ca["chiffre_affaires"]],
            textposition="outside",
            textfont=dict(family='JetBrains Mono', size=11)
        ))
        fig.update_layout(**PLOTLY_LAYOUT, height=300, xaxis_title="CA (FCFA)")
        st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="section-title">Mode de paiement par ville</div>', unsafe_allow_html=True)
    pv = df.groupby(["ville","mode_paiement"]).size().reset_index(name="nb")
    fig = px.bar(pv, x="ville", y="nb", color="mode_paiement",
                 barmode="stack", color_discrete_sequence=COULEURS)
    fig.update_layout(**PLOTLY_LAYOUT, height=300,
                      xaxis_title="Ville", yaxis_title="Transactions", legend_title="Mode de paiement")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="section-title">Top 20 vendeurs par CA</div>', unsafe_allow_html=True)
    top_v = df.groupby("vendeur")["chiffre_affaires"].sum().sort_values(ascending=False).head(20).reset_index()
    fig = go.Figure(go.Bar(
        x=top_v["vendeur"], y=top_v["chiffre_affaires"],
        marker=dict(color=top_v["chiffre_affaires"],
                    colorscale=[[0, "#2ed573"],[1, "#00e5ff"]]),
        text=[f"{v/1e6:.1f}M" for v in top_v["chiffre_affaires"]],
        textposition="outside",
        textfont=dict(family='JetBrains Mono', size=11)
    ))
    fig.update_layout(**PLOTLY_LAYOUT, height=320,
                      xaxis_title="Vendeur", yaxis_title="CA (FCFA)")
    st.plotly_chart(fig, use_container_width=True)

    col_l, col_r = st.columns(2)
    with col_l:
        st.markdown('<div class="section-title">Distribution du CA par vendeur</div>', unsafe_allow_html=True)
        vend_ca = df.groupby("vendeur")["chiffre_affaires"].sum()
        fig = px.histogram(vend_ca, nbins=30, color_discrete_sequence=["#ff4757"])
        fig.update_layout(**PLOTLY_LAYOUT, height=260,
                          xaxis_title="CA par vendeur (FCFA)", yaxis_title="Nombre de vendeurs")
        st.plotly_chart(fig, use_container_width=True)

    with col_r:
        st.markdown('<div class="section-title">Transactions par vendeur (top 10)</div>', unsafe_allow_html=True)
        vend_t = df.groupby("vendeur").size().sort_values(ascending=False).head(10).reset_index()
        vend_t.columns = ["vendeur","nb"]
        fig = go.Figure(go.Bar(
            x=vend_t["vendeur"], y=vend_t["nb"],
            marker_color="#ffd32a",
            text=vend_t["nb"], textposition="outside",
            textfont=dict(family='JetBrains Mono', size=11)
        ))
        fig.update_layout(**PLOTLY_LAYOUT, height=260,
                          xaxis_title="Vendeur", yaxis_title="Transactions")
        st.plotly_chart(fig, use_container_width=True)

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style="font-size:0.7rem; color:#6b7a99; font-family:'JetBrains Mono',monospace; text-align:center; line-height:1.8;">
    VentesShield · Dashboard Sénégal 2024 · Oumaro Titans DJIGUIMDE
</div>
""", unsafe_allow_html=True)
