from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"matches": []}


def test_read_main_with_query():
    response = client.get("/?keywords=circular&keywords=decarbonisation")
    assert response.status_code == 200
    assert response.json() == {"matches": [{"similarity": 16.379772349819046, "policyId": 9757,
                                            "policyTitle": " Circular economy – Strategy for the transition in Sweden",
                                            "sectors": ["Economy-wide"]},
                                           {"similarity": 13.395237259293886, "policyId": 9756,
                                            "policyTitle": "Spanish Strategy for Circular Economy (España Circular 2030)",
                                            "sectors": ["Economy-wide"]},
                                           {"similarity": 10.567243624619014, "policyId": 9632,
                                            "policyTitle": "France Relaunch Plan (\"France Relance\")",
                                            "sectors": ["Transportation", "Public Sector", "Industry", "Economy-wide",
                                                        "Coastal zones", "Buildings", "Agriculture"]},
                                           {"similarity": 9.131604466451375, "policyId": 9516,
                                            "policyTitle": "Slovenia's integrated National Energy and Climate Plan",
                                            "sectors": ["Waste", "Urban", "Transportation", "Industry", "Health",
                                                        "Energy", "Economy-wide", "Buildings", "Agriculture"]},
                                           {"similarity": 7.93962873036614, "policyId": 9435,
                                            "policyTitle": "Resolution no 107/2019 of the Council of Ministers approving the Long-Term Strategy for Carbon Neutrality of the Portuguese Economy in 2050",
                                            "sectors": ["Transportation", "Energy", "Economy-wide"]}]}
