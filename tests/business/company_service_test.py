import pytest

from src.business.company_service import validate_company_number_with_regex, get_company_by_company_number_and_iso_code, \
    create_company_if_not_exist, get_or_create_company


@pytest.mark.unit
def test_validate_company_number_with_regex__with_valid_regex():
    assert validate_company_number_with_regex(company_number="12345678", regex="^[0-9]*$") is True
    assert validate_company_number_with_regex(company_number="SC123456",
                                              regex="^([a-zA-Z]{2}[0-9]{6}|[0-9]{8})$") is True


@pytest.mark.unit
def test_validate_company_number_with_regex__with_invalid_regex():
    assert validate_company_number_with_regex(company_number="123", regex="^([a-zA-Z]{2}[0-9]{6}|[0-9]{8})$") is False
    assert validate_company_number_with_regex(company_number=" ", regex="^[0-9]+$") is False
    assert validate_company_number_with_regex(company_number="", regex="^[0-9]+$") is False


@pytest.mark.unit
def test_get_company_by_company_number_and_iso_code__with_existing_company(mocker, test_company_1, mock_db):
    mock_method = mocker.patch("src.business.company_service.get_company_by_company_number",
                               return_value=test_company_1)
    assert test_company_1 == get_company_by_company_number_and_iso_code(mock_db,
                                                                        test_company_1.company_number,
                                                                        test_company_1.country_alpha_2_iso_code)
    mock_method.assert_called_once()


@pytest.mark.unit
def test_get_company_by_company_number_and_iso_code__with_new_company(mocker, mock_db, test_company_1, test_company_2):
    mock_method = mocker.patch("src.business.company_service.get_company_by_company_number",
                               return_value=test_company_2)
    assert get_company_by_company_number_and_iso_code(mock_db,
                                                      test_company_1.company_number,
                                                      test_company_1.country_alpha_2_iso_code) is None
    mock_method.assert_called_once()


@pytest.mark.unit
def test_create_company_if_not_exist__company_exists(mocker, test_company_create_1, test_company_1, mock_db):
    mock_method = mocker.patch("src.business.company_service.get_company_by_company_number",
                               return_value=test_company_1)
    assert create_company_if_not_exist(test_company_create_1, mock_db) is None
    mock_method.assert_called_once()


@pytest.mark.unit
def test_create_company_if_not_exist__new_company(mocker, test_company_1, test_company_create_1, mock_db):
    mock_get_method = mocker.patch("src.business.company_service.get_company_by_company_number", return_value=None)
    mock_create_method = mocker.patch("src.business.company_service.__create_new_company", return_value=test_company_1)
    assert create_company_if_not_exist(test_company_create_1, mock_db) == test_company_1
    mock_get_method.assert_called_once()
    mock_create_method.assert_called_once()


@pytest.mark.unit
def test_get_or_create_company__existing_company(mocker, test_company_1, mock_db):
    mock_get_method = mocker.patch("src.business.company_service.get_company_by_company_number_and_iso_code",
                                   return_value=test_company_1)
    assert get_or_create_company(mock_db,
                                 test_company_1.company_number,
                                 test_company_1.country_alpha_2_iso_code) == test_company_1
    mock_get_method.assert_called_once()


@pytest.mark.unit
def test_get_or_create_company__new_company_valid_request(mocker, test_company_1, mock_db):
    mock_get_method = mocker.patch("src.business.company_service.get_company_by_company_number_and_iso_code",
                                   return_value=None)
    mock_create_method = mocker.patch("src.business.company_service.__create_new_company", return_value=test_company_1)
    assert get_or_create_company(test_company_1.company_number, test_company_1.country_alpha_2_iso_code,
                                 mock_db) == test_company_1
    mock_get_method.assert_called_once()
    mock_create_method.assert_called_once()


@pytest.mark.unit
def test_get_or_create_company__new_company_invalid_country(mocker, test_company_2, test_company_create_2, mock_db):
    mock_get_method = mocker.patch("src.business.company_service.get_company_by_company_number_and_iso_code",
                                   return_value=None)
    mock_create_method = mocker.patch("src.business.company_service.__create_new_company", return_value=None)
    assert get_or_create_company(test_company_2.company_number, test_company_2.country_alpha_2_iso_code,
                                 mock_db) is None
    mock_get_method.assert_called_once()
    mock_create_method.assert_called_with(company=test_company_create_2, db=mock_db)


@pytest.mark.unit
def test_get_or_create_company__new_company_invalid_company_no(mocker, mock_db, test_country_1, test_company_create_2):
    mock_get_method = mocker.patch("src.business.company_service.get_company_by_company_number_and_iso_code",
                                   return_value=None)
    mock_country_method = mocker.patch("src.business.company_service.get_country", return_value=test_country_1)
    assert get_or_create_company(test_company_create_2.company_number,
                                 test_company_create_2.country_alpha_2_iso_code,
                                 mock_db) is None
    mock_get_method.assert_called_with(db=mock_db, company_number=test_company_create_2.company_number,
                                       country_iso_code=test_company_create_2.country_alpha_2_iso_code)
    mock_country_method.assert_called_with(alpha_2_iso_code=test_company_create_2.country_alpha_2_iso_code, db=mock_db)
