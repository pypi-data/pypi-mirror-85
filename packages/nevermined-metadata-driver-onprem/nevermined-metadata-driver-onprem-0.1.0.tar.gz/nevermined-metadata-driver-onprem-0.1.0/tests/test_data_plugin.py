from metadata_driver_onprem.data_plugin import Plugin


def test_data_plugin():
    assert Plugin().type() == 'On premise'


def test_generate_url():
    url = 'https://www.example.com'
    assert Plugin().generate_url(url) == url
