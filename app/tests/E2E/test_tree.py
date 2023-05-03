from fastapi.testclient import TestClient
import urllib.parse
from app.main import app
from app.scheme import ParaphraseResponse

client = TestClient(app)

query = """(S (NP (NP (DT The) (JJ charming) (NNP Gothic) (NNP
Quarter) ) (, ,) (CC or) (NP (NNP Barri) (NNP Gòtic) ) ) (, ,) (VP (VBZ has) (NP (NP
(JJ narrow) (JJ medieval) (NNS streets) ) (VP (VBN filled) (PP (IN with) (NP (NP (JJ
trendy) (NNS bars) ) (, ,) (NP (NNS clubs) ) (CC and) (NP (JJ Catalan) (NNS
restaurants) ) ) ) ) ) ) )"""

expected = [
    {
        "tree": "(S (NP (NP (DT The) (JJ charming) (NNP Gothic) (NNP Quarter)) (, ,) (CC or) (NP (NNP Barri) (NNP Gòtic))) (, ,) (VP (VBZ has) (NP (NP (JJ narrow) (JJ medieval) (NNS streets)) (VP (VBN filled) (PP (IN with) (NP (NP (NNS clubs)) (, ,) (NP (JJ trendy) (NNS bars)) (CC and) (NP (JJ Catalan) (NNS restaurants))))))))"
    },
    {
        "tree": "(S (NP (NP (DT The) (JJ charming) (NNP Gothic) (NNP Quarter)) (, ,) (CC or) (NP (NNP Barri) (NNP Gòtic))) (, ,) (VP (VBZ has) (NP (NP (JJ narrow) (JJ medieval) (NNS streets)) (VP (VBN filled) (PP (IN with) (NP (NP (JJ trendy) (NNS bars)) (, ,) (NP (JJ Catalan) (NNS restaurants)) (CC and) (NP (NNS clubs))))))))"
    },
    {
        "tree": "(S (NP (NP (DT The) (JJ charming) (NNP Gothic) (NNP Quarter)) (, ,) (CC or) (NP (NNP Barri) (NNP Gòtic))) (, ,) (VP (VBZ has) (NP (NP (JJ narrow) (JJ medieval) (NNS streets)) (VP (VBN filled) (PP (IN with) (NP (NP (JJ Catalan) (NNS restaurants)) (, ,) (NP (NNS clubs)) (CC and) (NP (JJ trendy) (NNS bars))))))))"
    },
    {
        "tree": "(S (NP (NP (DT The) (JJ charming) (NNP Gothic) (NNP Quarter)) (, ,) (CC or) (NP (NNP Barri) (NNP Gòtic))) (, ,) (VP (VBZ has) (NP (NP (JJ narrow) (JJ medieval) (NNS streets)) (VP (VBN filled) (PP (IN with) (NP (NP (NNS clubs)) (, ,) (NP (JJ Catalan) (NNS restaurants)) (CC and) (NP (JJ trendy) (NNS bars))))))))"
    },
    {
        "tree": "(S (NP (NP (DT The) (JJ charming) (NNP Gothic) (NNP Quarter)) (, ,) (CC or) (NP (NNP Barri) (NNP Gòtic))) (, ,) (VP (VBZ has) (NP (NP (JJ narrow) (JJ medieval) (NNS streets)) (VP (VBN filled) (PP (IN with) (NP (NP (JJ Catalan) (NNS restaurants)) (, ,) (NP (JJ trendy) (NNS bars)) (CC and) (NP (NNS clubs))))))))"
    },
]
expected_list = list(map(lambda el: el["tree"], expected))

limit = 2
q = urllib.parse.quote(f"{query}")


def test_read_main() -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}


def test_paraphrase_success() -> None:
    response = client.get(f"/paraphrase?query={q}&limit={limit}")
    assert response.status_code == 200
    data = response.json()

    assert "paraphrase" in data

    # lte limin
    assert len(data["paraphrase"]) <= limit

    # Result in exptected
    assert data["paraphrase"][0]["text"] in expected_list

    # Each text is unique
    all_text = list(map(lambda x: x["text"], data["paraphrase"]))  # type: ignore
    assert len(set(all_text)) == len(all_text)


query_2 = urllib.parse.quote(f"(S(NP(NN query)))")


def test_paraphrase_non_result() -> None:
    response = client.get(f"/paraphrase?query={query_2}")
    assert response.status_code == 200
    data = response.json()
    assert "paraphrase" in data
    assert len(data["paraphrase"]) == 0


def test_paraphrase_invalid_input() -> None:
    response = client.get(f"/paraphrase?query=sdfasdf333)))")
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data
