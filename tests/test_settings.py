async def test_settings(settings):
    assert settings.POSTGRES_HOST == 'localhost'
    assert settings.POSTGRES_PORT == 5432
    assert settings.POSTGRES_USER == 'postgres'
    assert settings.POSTGRES_PASSWORD.get_secret_value() == 'postgres'
    assert settings.LOGLEVEL == 'DEBUG'