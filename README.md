# Bitcoin-analyysisovellus

Tämä sovellus hakee Bitcoinin markkinadataa CoinGeckosta ja näyttää sen verkkosivuna, jossa on diagrammeja ja tilastoja. Käyttäjä voi valita päivämäärävälin, jonka perusteella sovellus laskee:

1. Pisimmän laskutrendin pituus päivinä
2. Päivämäärän, jolloin volyymi oli suurin
3. Parhaan osto- ja myyntipäivän, joka tuottaisi suurimman tuoton
4. Päivittäisen hinnan ja volyymin pylväsdiagrammeina

## Teknologiat

- FastAPI (Python) backend
- Chart.js frontend-grafiikka
- Ei tietokantaa
- Haetut tiedot tulevat CoinGeckon julkisesta API:sta

## Asennus

backendin terminaalisss run
python -m uvicorn main:app --reload
ja sitten
Avaa `frontend/index.html` selaimessa.

## Käyttö

1. Aseta alku- ja loppupäivä sivun yläreunassa
2. Paina Hae
3. Sivulle päivittyvät:
   - Diagrammit
   - Laskutrendi
   - Suurin volyymipäivä
   - Paras osto- ja myyntipäivä

## Huomio

CoinGecko rajoittaa pyyntöjen määrää. Suuria date range -hakuja kannattaa välttää.

