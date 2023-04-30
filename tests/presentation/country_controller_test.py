import pytest
from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient

from main import app


@pytest.fixture(scope="module")
def test_app():
    client = TestClient(app)
    yield client


@pytest.mark.unit
def test_get_country_by_alpha_2_iso_code__existing_country(test_app, mocker, test_country_1):
    mock_method = mocker.patch("src.presentation.country_controller.get_country", return_value=test_country_1)
    response = test_app.get("/country/GB")
    assert response.status_code == 200
    assert response.json()["alpha_2_iso_code"] == test_country_1.alpha_2_iso_code
    assert response.json()["name"] == test_country_1.name
    assert response.json()["company_number_regex"] == test_country_1.company_number_regex
    assert response.json()["created_at"] == test_country_1.created_at.isoformat()
    assert response.json()["updated_at"] == test_country_1.updated_at.isoformat()
    mock_method.assert_called_once()


@pytest.mark.unit
@pytest.mark.parametrize("test_input", ["G", "Great Britain", "DEU"])
def test_get_country_by_alpha_2_iso_code__invalid_request(test_app, test_input):
    response = test_app.get("/country/" + test_input)
    assert response.status_code == 422


@pytest.mark.unit
def test_get_all_countries__with_existing_countries(test_app, mocker, test_country_list_json):
    mock_method = mocker.patch("src.presentation.country_controller.get_countries", return_value=test_country_list_json)
    response = test_app.get("/country")
    assert response.status_code == 200
    assert response.json() == test_country_list_json
    mock_method.assert_called_once()


@pytest.mark.unit
def test_get_all_countries__with_no_existing_countries(test_app, mocker):
    mock_method = mocker.patch("src.presentation.country_controller.get_countries", return_value=[])
    response = test_app.get("/country")
    assert response.status_code == 200
    assert response.json() == []
    mock_method.assert_called_once()


@pytest.mark.unit
def test_create_new_country__with_valid_country(test_app, mocker, test_country_create_1, test_country_1):
    mock_get_method = mocker.patch("src.presentation.country_controller.get_country", return_value=None)
    mock_create_method = mocker.patch("src.presentation.country_controller.create_country",
                                      return_value=test_country_1)
    json_country_create = jsonable_encoder(test_country_create_1)
    json_country = jsonable_encoder(test_country_1)
    response = test_app.post("/country", json=json_country_create)
    assert response.status_code == 201
    assert response.json() == json_country
    mock_get_method.assert_called_once()
    mock_create_method.assert_called_once()


@pytest.mark.unit
def test_create_new_country__with_invalid_country(test_app, mocker, test_country_1):
    mock_get_method = mocker.patch("src.presentation.country_controller.get_country", return_value=None)
    mock_create_method = mocker.patch("src.presentation.country_controller.create_country",
                                      return_value=test_country_1)
    response = test_app.post("/country", json={"name": "United Kingdom", "company_number_regex": "^[a-zA-Z]$"})
    assert response.status_code == 422
    mock_get_method.assert_not_called()
    mock_create_method.assert_not_called()


@pytest.mark.unit
def test_create_new_country__with_existing_country(test_app, mocker, test_country_create_1, test_country_1):
    mock_get_method = mocker.patch("src.presentation.country_controller.get_country", return_value=test_country_1)
    json_country_create = jsonable_encoder(test_country_create_1)
    response = test_app.post("/country", json=json_country_create)
    assert response.status_code == 400
    mock_get_method.assert_called_once()
