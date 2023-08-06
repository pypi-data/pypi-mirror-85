from metadata_driver_onprem.computing_plugin import Plugin


def test_computing_plugin():
    assert Plugin().type() == 'On premise'
