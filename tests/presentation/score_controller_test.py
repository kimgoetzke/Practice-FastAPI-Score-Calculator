import pytest
from fastapi.encoders import jsonable_encoder

from fastapi.testclient import TestClient

from main import app


@pytest.fixture(scope="module")
def test_app():
    client = TestClient(app)
    yield client


@pytest.mark.unit
def test_calculate_score__valid_request_1(test_app, mocker, test_company_1, test_financials_1, test_score_base_1):
    mock_method_1 = mocker.patch("src.presentation.score_controller.get_or_create_company", return_value=test_company_1)
    mock_method_2 = mocker.patch("src.presentation.score_controller.validate_financials", return_value=True)
    mock_method_3 = mocker.patch("src.presentation.score_controller.request_scores", return_value=[test_score_base_1])
    json_financials = {"financials": [jsonable_encoder(test_financials_1)]}
    response = test_app.post("/company/" +
                             test_company_1.country_alpha_2_iso_code + "/" +
                             test_company_1.company_number,
                             json=json_financials)
    assert response.status_code == 200
    assert response.json() == {"scores": [jsonable_encoder(test_score_base_1)]}
    mock_method_1.assert_called_once()
    mock_method_2.assert_called_once()
    mock_method_3.assert_called_once()


@pytest.mark.unit
def test_calculate_score__valid_request_2(test_app, mocker, test_company_1, test_financials_list, test_score_list):
    mock_method_1 = mocker.patch("src.presentation.score_controller.get_or_create_company", return_value=test_company_1)
    mock_method_2 = mocker.patch("src.presentation.score_controller.validate_financials", return_value=True)
    mock_method_3 = mocker.patch("src.presentation.score_controller.request_scores", return_value=test_score_list)
    json_financials = {"financials": jsonable_encoder(test_financials_list)}
    response = test_app.post("/company/" +
                             test_company_1.country_alpha_2_iso_code + "/" +
                             test_company_1.company_number,
                             json=json_financials)
    assert response.status_code == 200
    assert response.json() == {"scores": jsonable_encoder(test_score_list)}
    mock_method_1.assert_called_once()
    mock_method_2.assert_called_once()
    mock_method_3.assert_called_once()


@pytest.mark.unit
def test_calculate_score__invalid_financials(test_app, mocker, test_company_1, test_invalid_financials_list):
    mock_method_1 = mocker.patch("src.presentation.score_controller.get_or_create_company", return_value=test_company_1)
    mock_method_2 = mocker.patch("src.presentation.score_controller.validate_financials", return_value=False)
    json_financials = {"financials": jsonable_encoder(test_invalid_financials_list)}
    response = test_app.post("/company/" + test_company_1.country_alpha_2_iso_code + "/" + test_company_1.company_number,
                             json=json_financials)
    assert response.status_code == 400
    mock_method_1.assert_called_once()
    mock_method_2.assert_called_once()


@pytest.mark.unit
def test_calculate_score__invalid_company(test_app, mocker, test_company_1, test_financials_list):
    mock_method = mocker.patch("src.presentation.score_controller.get_or_create_company", return_value=None)
    json_financials = {"financials": jsonable_encoder(test_financials_list)}
    response = test_app.post("/company/" + test_company_1.country_alpha_2_iso_code + "/" + test_company_1.company_number,
                             json=json_financials)
    assert response.status_code == 400
    mock_method.assert_called_once()


@pytest.mark.unit
@pytest.mark.parametrize("test_input", ["G", "Great Britain", "DEU", "12"])
def test_calculate_score__invalid_request(test_app, mocker, test_company_1, test_input, test_financials_list):
    mock_method = mocker.patch("src.presentation.score_controller.get_or_create_company", return_value=test_company_1)
    json_financials = {"financials": jsonable_encoder(test_financials_list)}
    response = test_app.post("/company/" + test_input + "/12345678",
                             json=json_financials)
    assert response.status_code == 422
    mock_method.assert_not_called()


@pytest.mark.unit
def test_get_scores_by_company__existing_company_no_score(test_app, mocker, test_company_create_1, test_company_1):
    mock_method = mocker.patch("src.presentation.score_controller.get_company_by_company_number_and_iso_code",
                               return_value=test_company_1)
    response = test_app.get("/company/" +
                            test_company_create_1.country_alpha_2_iso_code + "/" +
                            test_company_create_1.company_number)
    assert response.status_code == 200
    assert response.json() == {"scores": []}
    mock_method.assert_called_once()


@pytest.mark.unit
def test_get_scores_by_company__existing_company_with_score(test_app, mocker, test_company_create_1, test_company_1,
                                                            test_score_1):
    json_country = jsonable_encoder(test_score_1)
    mock_company_method = mocker.patch("src.presentation.score_controller.get_company_by_company_number_and_iso_code",
                                       return_value=test_company_1)
    mock_score_method = mocker.patch("src.presentation.score_controller.get_scores_by_company_id",
                                     return_value=[test_score_1])
    response = test_app.get("/company/" +
                            test_company_create_1.country_alpha_2_iso_code + "/" +
                            test_company_create_1.company_number)
    assert response.status_code == 200
    assert response.json() == {"scores": [json_country]}
    mock_company_method.assert_called_once()
    mock_score_method.assert_called_once()


@pytest.mark.unit
def test_get_scores_by_company__company_does_not_exist(test_app, mocker, test_company_create_1):
    mock_method = mocker.patch("src.presentation.score_controller.get_company_by_company_number_and_iso_code",
                               return_value=None)
    response = test_app.get("/company/" +
                            test_company_create_1.country_alpha_2_iso_code + "/" +
                            test_company_create_1.company_number)
    assert response.status_code == 404
    mock_method.assert_called_once()


@pytest.mark.unit
@pytest.mark.parametrize("test_input", ["G", "Great Britain", "DEU"])
def test_get_scores_by_company__invalid_request(test_app, mocker, test_input):
    mock_method = mocker.patch("src.presentation.score_controller.get_company_by_company_number_and_iso_code",
                               return_value=None)
    response = test_app.get("/company/" + test_input + "/12345678")
    assert response.status_code == 422
    mock_method.assert_not_called()
