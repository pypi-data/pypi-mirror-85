from unittest.mock import patch

import responses
import pytest

from user_sdk.openid_connect import (
    OpenIDConnectAuth,
    OIDCAuthError,
    InsufficientPermissionError,
)


def _jw_key_set():
    return {
        "keys": [
            {
                "alg": "RS256",
                "kty": "RSA",
                "use": "sig",
                "n": "60U6mBmsm6kHKqv9Q8iYv_QTfyhjL0LpJQOVEbZsWdI9nxJzh2Clmro6tv_zvZsaLhl4BJ392gdATGrcYqnAooNa-6pDG9Z-WrhEkTHna-bcqB_LaROpdCW8InJlMvWg4CdPE0lfDHGjhIA8AKNk0Hh7-zPkoNeqrizgCZR_COSW-I3jzWF4m5UumGQqGXxjUcGipyZVmy8qyrQ8-xaTyHxFxgqnOsypkPaDZzjuSjCaXCpqDlC1-uW3qeB-SRD0XFqp_4lNm65HuvGeIzlVMgAunpTqJbm4seknnwbWvedotm4L8XxOnZIFI0uTQ5PqSGsx8N5TA-butSkKLY5TDQ",
                "e": "AQAB",
                "kid": "N_68xPq0IVA9TJkB9fB4j",
            },
            {
                "alg": "RS256",
                "kty": "RSA",
                "use": "sig",
                "n": "uzG86qsHYs0PPIoFPe1IIIYmh3fBbgWPD2xpxiPkOEajoohg8_YkAYbFp2gZhFosO2L88le5DpmDSsjwsWUXTcr0cYnAnOPMoZUE--rwGezHyvt4Tq4k3DQf3szSgbRm4DrUBLqr368eJ9pPkIyzaTxQmLjgp2_WZ2vTuhRiU0UAMiwLkrVkcO_K42TYHeci9en5uYajAUAxLwFnUlBQYEEU7p8NQVeCHMJ0-LWiPIJT3SAz6uyglYJjNV3rsJ2wDJjBmT44l6otHmLDVM53mTtMTf-hBB1Gl9QbSPL3_r4Xsul-VvscJcCxUNlluHO-ehyAak4DgwFdFy7gqdeI4w",
                "e": "AQAB",
                "kid": "S0T8Tr7PjB4FIHRCsXptG",
            },
        ]
    }


def _user_info(email):
    return {
        "sub": "auth0|5f649a4215ab3a00772db6a6",
        "nickname": "Rodya",
        "name": "Rodion Romanovich Raskolnikov",
        "picture": "https://www.some.picture",
        "updated_at": "2020-09-18T11:30:11.171Z",
        "email": email,
        "email_verified": False,
    }


@patch("jose.jwt.get_unverified_claims")
@patch("jose.jwt.get_unverified_header")
@patch("jose.jwt.decode")
@responses.activate
def test_authorize(mock_jwt_decode, mock_get_headers, mock_get_claims):
    jw_key_set = _jw_key_set()
    email = "e@m.ail"
    responses.add("GET", "https://issuer.url/.well-known/jwks.json", json=jw_key_set)
    responses.add("GET", "https://issuer.url/userinfo", json=_user_info(email))
    mock_get_headers.return_value = {"kid": jw_key_set["keys"][0]["kid"]}
    mock_get_claims.return_value = {"permissions": ["read:abc"]}

    sso = OpenIDConnectAuth(
        issuer_url="https://issuer.url", audience="test-audience", algorithms=["RS256"],
    )
    assert sso.authorize(access_token="token", required_permission="read:abc") == email
    key_set = jw_key_set["keys"][0].copy()
    key_set.pop("alg")
    mock_jwt_decode.assert_called_with(
        "token",
        key_set,
        algorithms=["RS256"],
        audience="test-audience",
        issuer="https://issuer.url/",
    )
    mock_get_headers.assert_called_with("token")
    mock_get_claims.assert_called_with("token")
    responses.assert_call_count("https://issuer.url/.well-known/jwks.json", 1)
    responses.assert_call_count("https://issuer.url/userinfo", 1)


@patch("jose.jwt.get_unverified_claims")
@patch("jose.jwt.get_unverified_header")
@patch("jose.jwt.decode")
@responses.activate
def test_authorize_with_insufficient_permission(
    mock_jwt_decode, mock_get_headers, mock_get_claims
):
    jw_key_set = _jw_key_set()
    responses.add("GET", "https://issuer.url/.well-known/jwks.json", json=jw_key_set)
    responses.add("GET", "https://issuer.url/userinfo", json=_user_info("e@m.ail"))
    mock_get_headers.return_value = {"kid": jw_key_set["keys"][0]["kid"]}
    mock_get_claims.return_value = {"permissions": ["read:abc"]}

    sso = OpenIDConnectAuth(
        issuer_url="https://issuer.url", audience="test-audience", algorithms=["RS256"],
    )

    with pytest.raises(InsufficientPermissionError):
        assert sso.authorize(access_token="token", required_permission="read:xyz")
    responses.assert_call_count("https://issuer.url/userinfo", 0)


@pytest.mark.parametrize(
    "granted_permissions, required_permission, result",
    [
        (["read:vehicles", "write:vehicles"], "write:vehicles", True),
        (["read:vehicles", "write:vehicles"], "read:vehicles", True),
        (["read:vehicles", "write:vehicles"], "read:persons", False),
        (["read:*", "write:vehicles", "read:stops"], "read:persons", True),
        (["read:vehicles", "write:*"], "write:persons", True),
        ([], "read:vehicles", False),
        (["*:persons"], "read:persons", False),
    ],
)
@patch("jose.jwt.get_unverified_claims")
def test_has_permission(
    mock_get_unverified_claims, granted_permissions, required_permission, result
):
    mock_get_unverified_claims.return_value = {"permissions": granted_permissions}
    assert OpenIDConnectAuth._has_permission("abc-token", required_permission) == result
