import pandas as pd
import os
import matplotlib.pyplot as plt

subor = "README.md"

def nacitaj_data():
    df = pd.read_csv("data_cisté.csv", sep=",")
    pocet_riadkov = len(df)
    pocet_krajin = df["country"].nunique()
    min_rok = df["year"].min()
    max_rok =df["year"].max()

    print(f"Načítaných riadkov: {pocet_riadkov:,}")
    print(f"Krajín: {pocet_krajin}")
    print(f"Rozsah rokov: {min_rok}–{max_rok}")

    return df
 
def vycisti(df):
    return df
    
def agreguj(df):
    df_agregovany = df.groupby("country")["population"].agg(["mean", "count"])

    return df_agregovany
    
def nakresli_grafy(df):
    prehlad = df.groupby("country")["population"].mean()
    top_10 = (prehlad.sort_values(ascending=False).head(10) / 1_000_000).sort_values(ascending=True)

    ax = top_10.plot(kind="barh")
    ax.set_title("Top 10 krajín podľa priemernej populácie (1750 – 2024)")
    ax.set_xlabel("Priemerná populácia (v miliónoch)"   )
    ax.set_ylabel("Krajiny")
    plt.tight_layout()
    plt.savefig("vystupy/graf1.png", dpi=150)
    plt.close()

    vyvoj_co2 = df.groupby("year")["co2"].sum()
    ax = vyvoj_co2.plot()
    ax.set_title("Celkové ročné emisie CO2 podľa roku")
    ax.set_xlabel("Rok")
    ax.set_ylabel("Emisie CO2 (v miliónoch ton)")
    plt.tight_layout()
    plt.savefig("vystupy/graf2.png", dpi=150)
    plt.close()

    ax = df["co2_per_capita"].plot(kind="hist", bins=40)
    ax.set_title("Rozdelenie emisií CO2 na obyvateľa")
    ax.set_xlabel("CO2 na obyvateľa (tony)")
    ax.set_ylabel("Počet záznamov")
    plt.tight_layout()
    plt.savefig("vystupy/graf3.png", dpi=150)
    plt.close()
    
def zapis_readme(df_vycisteny, df_agregovany, subor):
    with open(subor, "w", encoding="utf-8") as f:
        f.write("# Analýza populácie a CO2 emisií\n\n")
        f.write(f"Načítané riadky: {len(df_vycisteny)}\n")
        f.write("Zdroj - OWID CO2 dataset\n\n")
        f.write("## Top 5 krajín podľa populácie\n\n")
        top_5 = df_agregovany.sort_values(by="mean", ascending=False).head(5)
        f.write(f"```\n{top_5}\n```\n\n")
        f.write("## Grafy\n\n")
        f.write("![Top 10 krajín podľa priemernej populácie](vystupy/graf1.png)\n\n")
        f.write("![Vývoj celkových CO2 emisií podľa roku](vystupy/graf2.png)\n\n")
        f.write("![Rozdelenie emisií CO2 na obyvateľa](vystupy/graf3.png)\n\n")
        
        najvacsia = top_5.index[0]
        druha = top_5.index[1]
        pomer = top_5["mean"].iloc[0] / top_5["mean"].iloc[1]

        posledny_rok = df_vycisteny["year"].max()
        co2_posledny_rok = df_vycisteny[df_vycisteny["year"] == posledny_rok]["co2"].sum()

        podiel_top5 = top_5["mean"].sum() / df_agregovany["mean"].sum()

        f.write("## Zistenia\n\n")
        f.write(f"- {najvacsia} má najvyššiu priemernú populáciu spomedzi všetkých krajín, {pomer:.1f}x viac ako druhá {druha}.\n")
        f.write(f"- V roku {posledny_rok} vyprodukovali krajiny v datasete spolu {co2_posledny_rok:,.0f} miliónov ton CO2.\n")
        f.write(f"- Top 5 krajín podľa populácie tvorí {podiel_top5:.1%} priemernej populácie všetkých krajín v datasete.\n")
        f.write("\n## Dáta\n\n")
        f.write("Zdroj: [OWID CO2 dataset](https://github.com/owid/co2-data) (Our World in Data).\n")
        f.write(f"{len(df_vycisteny):,} riadkov po vyčistení, roky {df_vycisteny['year'].min()}–{df_vycisteny['year'].max()}, ")
        f.write(f"{df_vycisteny['country'].nunique()} krajín. Vstupný súbor `data_cisté.csv` (nie je v repozitári, pozri nižšie).\n\n")

        f.write("## Ako to spustiť\n\n")
        f.write("```\n")
        f.write("pip install -r requirements.txt\n")
        f.write("python analyza2.py\n")
        f.write("```\n\n")
        f.write("`data_cisté.csv` nie je v repozitári (je príliš veľký). Priprav si ho takto:\n\n")
        f.write("```python\n")
        f.write("import pandas as pd\n")
        f.write('co2_data = pd.read_csv("owid-co2-data.csv")\n')
        f.write('co2_data["population"] = co2_data["population"].fillna(co2_data["population"].mean())\n')
        f.write('co2_data_ciste = co2_data.dropna(subset=["iso_code"])\n')
        f.write('co2_data_ciste.to_csv("data_cisté.csv", index=False)\n')
        f.write("```\n\n")
        f.write("Surový CSV: https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv\n\n")

        f.write("## Štruktúra\n\n")
        f.write("- `analyza2.py` — načítanie, čistenie, agregácie, grafy a README, jedným spustením\n")
        f.write("- `data_cisté.csv` — vstupné dáta (treba vyrobiť, pozri vyššie)\n")
        f.write("- `vystupy/` — výstupné PNG grafy a `agregacia.csv` (generované skriptom)\n\n")

        f.write("## Čo by som dorobil\n\n")
        f.write("- Rozdelenie CO2 emisií podľa zdroja (uhlie, ropa, plyn) — dataset ich má, nevyužil som ich.\n")
        f.write("- Argument pri spustení na vlastnú cestu k CSV namiesto pevného mena súboru.\n")


def main():
    os.makedirs("vystupy", exist_ok=True)
    df = nacitaj_data()
    df_vycisteny = vycisti(df)
    df_agregovany = agreguj(df_vycisteny)
    df_agregovany.to_csv("vystupy/agregacia.csv")
    nakresli_grafy(df_vycisteny)
    zapis_readme(df_vycisteny, df_agregovany, subor)

if __name__ == "__main__": 
    main()