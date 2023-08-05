import json
from uuid import uuid4, UUID
from http import HTTPStatus

import pytest
import responses
from user_sdk.domain import User, UserProfile, Session
from user_sdk.error import TooManyRequests
from user_sdk.user_service import UserService

user_service = UserService(
    authentication_url="http://dummy_authentication",
    profile_url="http://dummy_profile",
    authorization_url="http://dummy_authorization",
)


def test_dict_to_user():
    user = User.from_dict(user_dict)
    assert user.id == "b402e055-2884-43a1-9e33-dbfe67e62971"
    assert 1 == len(user.identities)


def test_dict_to_user_profile():
    user_profile = UserProfile.from_dict(user_profile_dict)
    assert user_profile.name == "sample_name"
    assert "sample_work_address" == user_profile.work_address.location_name
    assert "sample_home_address" == user_profile.home_address.location_name
    assert "MALE" == user_profile.gender.name
    assert "gcm-is-fcm-is-gcm" == user_profile.push_notification_id


def test_dict_to_user_profile_for_incomplete_user_profile():
    user_profile = UserProfile.from_dict(incomplete_user_profile_dict)
    assert user_profile.name is None
    assert user_profile.work_address is None
    assert "sample_home_address" == user_profile.home_address.location_name
    assert user_profile.gender is None


def test_user_profile_to_dict():
    user_profile = UserProfile.from_dict(user_profile_dict)
    user_profile_new_dict = user_profile.to_dict()

    for key in [
        "id",
        "name",
        "gender",
        "home_address",
        "work_address",
        "user_types",
        "zone_id",
        "user_specific_features",
    ]:
        assert user_profile_dict[key] == user_profile_new_dict[key]


def test_user_profile_with_no_home_work_address_to_dict():
    user_profile = UserProfile.from_dict(user_profile_dict_with_no_home_or_work_address)
    user_profile_new_dict = user_profile.to_dict()

    for key in ["id", "name", "gender"]:
        assert (
            user_profile_dict_with_no_home_or_work_address[key]
            == user_profile_new_dict[key]
        )


def test_user_profile_with_no_name_gender_to_dict():
    user_profile = UserProfile.from_dict(user_profile_dict_with_no_name_or_gender)
    user_profile_new_dict = user_profile.to_dict()

    assert user_profile_dict_with_no_name_or_gender["id"] == user_profile_new_dict["id"]


def test_dict_to_session():
    session = Session.from_dict(session_response)
    assert session.user.id == "30944af3-dfe7-45e5-a860-31ac4a18bc69"
    assert (
        session.id
        == "FEZRHOQLBALFB4QE3S3LLN52RROVR6PTC4JQT44WFFZWNC4QKT3JTFQJX2E2LAKXGCFQD4BN63TTEIADCFKDFYAI4RCJRAHL7JCWHYY"
    )


def test_add_user_type_to_user_profile():
    user_profile = UserProfile.from_dict(incomplete_user_profile_dict)
    assert user_profile.user_types == []

    user_profile.add_user_type("PREMIUM")
    assert user_profile.user_types == ["PREMIUM"]


def test_remove_user_type_to_user_profile():
    user_profile = UserProfile.from_dict(user_profile_dict)
    assert user_profile.user_types == ["PREMIUM"]

    user_profile.remove_user_type("DUMMY")
    assert user_profile.user_types == ["PREMIUM"]

    user_profile.remove_user_type("PREMIUM")
    assert user_profile.user_types == []


def test_add_user_specific_feature_to_user_profile():
    user_profile = UserProfile.from_dict(incomplete_user_profile_dict)
    assert user_profile.user_specific_features == []

    user_profile.add_user_specific_feature("AUTO_BOOKING")
    assert user_profile.user_specific_features == ["AUTO_BOOKING"]


def test_remove_user_specific_feature_from_user_profile():
    user_profile = UserProfile.from_dict(user_profile_dict)
    assert user_profile.user_specific_features == ["AUTO_BOOKING"]

    user_profile.remove_user_specific_feature("DUMMY")
    assert user_profile.user_specific_features == ["AUTO_BOOKING"]

    user_profile.remove_user_specific_feature("AUTO_BOOKING")
    assert user_profile.user_specific_features == []


@responses.activate
def test_update_profile_on_adding_user_types_and_user_specific_features():
    user_profile = UserProfile.from_dict(incomplete_user_profile_dict)
    user_id = UUID(incomplete_user_profile_dict["id"])

    def request_callback(request):
        payload = json.loads(request.body)
        assert payload["user_types"] == ["PREMIUM"]
        assert payload["user_specific_features"] == ["AUTO_BOOKING"]
        return (
            200,
            {},
            json.dumps(
                {
                    "data": {
                        "id": str(user_id),
                        "user_types": payload["user_types"],
                        "user_specific_features": payload["user_specific_features"],
                    }
                }
            ),
        )

    responses.add_callback(
        responses.PATCH,
        f"http://dummy_profile/api/v1/new/profiles/{user_id}",
        callback=request_callback,
        content_type="application/json",
    )

    user_profile.add_user_type("PREMIUM")
    user_profile.add_user_specific_feature("AUTO_BOOKING")
    user_service.update_profile(
        user_id=user_id,
        profile={
            "user_types": user_profile.user_types,
            "user_specific_features": user_profile.user_specific_features,
        },
    )


@responses.activate
def test_update_profile_on_removing_user_types_and_user_specific_features():
    user_profile = UserProfile.from_dict(user_profile_dict)
    user_id = UUID(incomplete_user_profile_dict["id"])

    def request_callback(request):
        payload = json.loads(request.body)
        assert payload["user_types"] == []
        assert payload["user_specific_features"] == []
        return (
            200,
            {},
            json.dumps(
                {
                    "data": {
                        "id": str(user_id),
                        "user_types": payload["user_types"],
                        "user_specific_features": payload["user_specific_features"],
                    }
                }
            ),
        )

    responses.add_callback(
        responses.PATCH,
        f"http://dummy_profile/api/v1/new/profiles/{user_id}",
        callback=request_callback,
        content_type="application/json",
    )

    user_profile.remove_user_type("PREMIUM")
    user_profile.remove_user_specific_feature("AUTO_BOOKING")
    user_service.update_profile(
        user_id=user_id,
        profile={
            "user_types": user_profile.user_types,
            "user_specific_features": user_profile.user_specific_features,
        },
    )


@responses.activate
def test_get_user_from_session_throws_rte_if_non_ok_response():
    session_id = str(uuid4())
    responses.add(
        responses.GET,
        f"http://dummy_authentication/api/v1/sessions/{session_id}",
        status=500,
        json=dict(key="value"),
    )
    with pytest.raises(RuntimeError) as exc_info:
        user_service.get_user_from_session(session_id)

    assert "500" in str(exc_info.value)
    assert "key" in str(exc_info.value)
    assert "value" in str(exc_info.value)


@responses.activate
def test_get_user_from_active_session_for_ok_response():
    session_id = str(uuid4())

    def request_callback(request):
        return HTTPStatus.OK, {}, json.dumps({"data": session_response})

    responses.add_callback(
        responses.GET,
        f"http://dummy_authentication/api/v1/sessions/{session_id}/active",
        callback=request_callback,
        content_type="application/json",
    )
    session = user_service.get_user_from_active_session(session_id)
    assert Session.from_dict(session_response) == session


@responses.activate
def test_get_user_from_active_session_throws_rte_if_non_ok_response():
    session_id = str(uuid4())
    responses.add(
        responses.GET,
        f"http://dummy_authentication/api/v1/sessions/{session_id}/active",
        status=500,
        json=dict(key="value"),
    )
    with pytest.raises(RuntimeError) as exc_info:
        user_service.get_user_from_active_session(session_id)

    assert "500" in str(exc_info.value)
    assert "key" in str(exc_info.value)
    assert "value" in str(exc_info.value)


user_dict = {
    "created_at": "2018-10-18T09:05:59.334113",
    "credentials": [
        {
            "created-at": "2018-10-18 09:05:59.334075",
            "id": "d417ad09-d5ae-4a72-9060-419308e6756d",
            "identity": "+917042329887",
            "identity_type": "MOBILE",
            "updated-at": "2018-10-18 09:05:59.334091",
            "verified": True,
        }
    ],
    "id": "b402e055-2884-43a1-9e33-dbfe67e62971",
    "suspended": False,
    "updated_at": "2018-10-18T09:05:59.334119",
}

user_profile_dict = {
    "created_at": "2018-10-18T13:04:55.643673",
    "gender": "MALE",
    "home_address": {
        "location": {"lat": 28.88, "lng": 77.33},
        "location_name": "sample_home_address",
    },
    "id": "f77971a6-3a7f-4475-81b6-2fe9e085f0bc",
    "name": "sample_name",
    "zone_id": "b402e055-2884-43a1-9e33-dbfe67e62971",
    "updated_at": "2018-10-18T13:04:55.643673",
    "push_notification_id": "gcm-is-fcm-is-gcm",
    "work_address": {
        "location": {"lat": 27.88, "lng": 76.33},
        "location_name": "sample_work_address",
    },
    "user_types": ["PREMIUM"],
    "user_specific_features": ["AUTO_BOOKING"],
}

user_profile_dict_with_no_home_or_work_address = {
    "id": "f77971a6-3a7f-4475-81b6-2fe9e085f0bc",
    "gender": "MALE",
    "name": "Test",
}

user_profile_dict_with_no_name_or_gender = {
    "id": "f77971a6-3a7f-4475-81b6-2fe9e085f0bc"
}

incomplete_user_profile_dict = {
    "created_at": "2018-10-18T13:04:55.643673",
    "home_address": {
        "location": {"lat": 28.88, "lng": 77.33},
        "location_name": "sample_home_address",
    },
    "id": "f77971a6-3a7f-4475-81b6-2fe9e085f0bc",
    "updated_at": "2018-10-18T13:04:55.643673",
}

session_response = {
    "id": "fd335403-83bc-4eb5-b42e-6eb6674f4537",
    "created_at": "2018-10-21T13:52:50.208448",
    "updated_at": "2018-10-21T13:52:50.208457",
    "session_id": "FEZRHOQLBALFB4QE3S3LLN52RROVR6PTC4JQT44WFFZWNC4QKT3JTFQJX2E2LAKXGCFQD4BN63TTEIADCFKDFYAI4RCJRAHL7JCWHYY",
    "user": {
        "id": "30944af3-dfe7-45e5-a860-31ac4a18bc69",
        "created_at": "2018-10-21T07:41:36.034161",
        "updated_at": "2018-10-21T07:41:36.034184",
        "suspended": False,
        "credentials": [
            {
                "id": "c28ee1f5-8632-42e4-97a3-bbd60893bb7b",
                "created-at": "2018-10-21 07:41:36.023701",
                "updated-at": "2018-10-21 07:41:36.032386",
                "identity": "+917042329887",
                "identity_type": "MOBILE",
                "verified": True,
            }
        ],
    },
    "credential": {
        "id": "c28ee1f5-8632-42e4-97a3-bbd60893bb7b",
        "created-at": "2018-10-21 07:41:36.023701",
        "updated-at": "2018-10-21 07:41:36.032386",
        "identity": "+917042329887",
        "identity_type": "MOBILE",
        "verified": True,
    },
}


@responses.activate
def test_login_raises_too_many_requests_error_if_status_code_received_from_user_auth_service_is_429():
    responses.add(
        responses.POST,
        f"http://dummy_authentication/api/v1/sign_in",
        json={},
        status=HTTPStatus.TOO_MANY_REQUESTS,
    )
    with pytest.raises(TooManyRequests):
        user_service.login_with_mobile(phone_number="8130813081", otp="1339")


@responses.activate
def test_mobile_login_with_expiry():
    expiry = 600

    def request_callback(request):
        payload = json.loads(request.body)
        assert payload["expiry_seconds"] == expiry
        return (
            HTTPStatus.CREATED,
            {},
            json.dumps({"data": {**session_response, "expiry_seconds": expiry}}),
        )

    responses.add_callback(
        responses.POST,
        f"http://dummy_authentication/api/v1/sign_in",
        callback=request_callback,
        content_type="application/json",
    )
    user_service.login_with_mobile(
        phone_number="8130813081", otp="1339", expiry_seconds=expiry
    )
