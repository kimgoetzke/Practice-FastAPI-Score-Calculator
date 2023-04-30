import pytest
from fastapi.encoders import jsonable_encoder

from src.business.score_service import validate_financials, calculate_score, request_scores


@pytest.mark.unit
def test_validate_financials__invalid_financials(test_invalid_financials_list):
    assert validate_financials(test_invalid_financials_list) is False


@pytest.mark.unit
def test_validate_financials__valid_financials(test_financials_list):
    assert validate_financials(test_financials_list) is True


@pytest.mark.unit
def test_calculate_score__error_when_invalid(test_zero_financials):
    with pytest.raises(ZeroDivisionError):
        calculate_score(test_zero_financials)


@pytest.mark.unit
def test_calculate_score__success_when_valid(test_financials_1, test_financials_2):
    assert calculate_score(test_financials_1) == 6.54
    assert calculate_score(test_financials_2) == 6.79


@pytest.mark.unit
def test_request_score(mocker, test_financials_list, test_company_1, mock_db, test_score_list):
    mock_method = mocker.patch("src.business.score_service.create_score", return_value=None)
    json_score_report = jsonable_encoder(test_score_list)
    assert request_scores(test_financials_list, test_company_1, mock_db) == json_score_report
    mock_method.assert_called()
