from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional, List
from uuid import UUID

from shuttl_geo import Location
from shuttlis.serialization import serialize


class CredentialType(Enum):
    USERNAME = "USERNAME"
    MOBILE = "MOBILE"
    OAUTH = "OAUTH"

    def __str__(self):
        return self.value


class CountryCode(Enum):
    INDIA = "IN"
    THAILAND = "TH"

    def __str__(self):
        return self.value


class Gender(Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    OTHER = "OTHER"

    def __str__(self):
        return self.value


@dataclass
class Address:
    location_name: str
    location: Location
    street_address: Optional[str] = None
    usual_departure_time: Optional[int] = None

    @classmethod
    def from_dict(cls, _dict: dict) -> "Address":
        return cls(
            location=Location(_dict["location"]["lat"], _dict["location"]["lng"]),
            location_name=_dict["location_name"],
            street_address=_dict.get("street_address"),
            usual_departure_time=_dict.get("usual_departure_time"),
        )

    def to_dict(self):
        rv = {"location_name": self.location_name, "location": serialize(self.location)}

        if self.street_address:
            rv["street_address"] = self.street_address

        if self.usual_departure_time:
            rv["usual_departure_time"] = self.usual_departure_time

        return rv


@dataclass
class UserProfile:
    user_id: UUID
    name: str
    gender: Gender
    home_address: Address
    work_address: Address
    zone_id: Optional[str] = None
    dob: Optional[datetime] = None
    email: Optional[str] = None
    img_url: Optional[str] = None
    push_notification_id: Optional[str] = None
    fb_access_token: Optional[str] = None
    user_types: List[str] = field(default_factory=list)
    user_specific_features: List[str] = field(default_factory=list)
    features: List[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, _dict) -> "UserProfile":
        return UserProfile(
            user_id=_dict["id"],
            name=_dict.get("name"),
            gender=Gender(_dict["gender"]) if _dict.get("gender") else None,
            zone_id=_dict.get("zone_id"),
            home_address=Address.from_dict(_dict["home_address"])
            if _dict.get("home_address")
            else None,
            work_address=Address.from_dict(_dict["work_address"])
            if _dict.get("work_address")
            else None,
            email=_dict.get("email"),
            img_url=_dict.get("img_url"),
            push_notification_id=_dict.get("push_notification_id"),
            dob=datetime.fromisoformat(_dict["dob"]) if _dict.get("dob") else None,
            fb_access_token=_dict.get("fb_access_token"),
            user_types=_dict.get("user_types") or [],
            user_specific_features=_dict.get("user_specific_features") or [],
            features=_dict.get("features") or [],
        )

    def to_dict(self):
        rv = {"id": str(self.user_id)}
        if self.name:
            rv["name"] = self.name
        if self.gender:
            rv["gender"] = self.gender.name
        if self.home_address:
            rv["home_address"] = self.home_address.to_dict()
        if self.work_address:
            rv["work_address"] = self.work_address.to_dict()

        if self.zone_id:
            rv["zone_id"] = self.zone_id
        if self.dob:
            rv["dob"] = self.dob
        if self.email:
            rv["email"] = self.email
        if self.img_url:
            rv["img_url"] = self.img_url
        if self.push_notification_id:
            rv["push_notification_id"] = self.push_notification_id
        if self.fb_access_token:
            rv["fb_access_token"] = self.fb_access_token
        if self.user_types:
            rv["user_types"] = self.user_types
        if self.user_specific_features:
            rv["user_specific_features"] = self.user_specific_features
        return rv

    def add_user_type(self, type: str):
        if type not in self.user_types:
            self.user_types.append(type)

    def remove_user_type(self, type: str):
        if type in self.user_types:
            self.user_types.remove(type)

    def add_user_specific_feature(self, feature: str):
        if feature not in self.user_specific_features:
            self.user_specific_features.append(feature)

    def remove_user_specific_feature(self, feature: str):
        if feature in self.user_specific_features:
            self.user_specific_features.remove(feature)


@dataclass
class UserDevice:
    user_id: UUID
    device_id: str
    app_version: str = None
    platform: str = None

    @classmethod
    def from_dict(cls, _dict: dict):
        return cls(
            user_id=_dict["user_id"],
            device_id=_dict["device_id"],
            app_version=_dict.get("app_version"),
            platform=_dict.get("platform"),
        )

    def to_dict(self):
        rv = {"user_id": str(self.user_id), "device_id": self.device_id}

        if self.app_version:
            rv["app_version"] = self.app_version

        if self.platform:
            rv["platform"] = self.platform

        return rv


@dataclass
class Credential:
    id: UUID
    type: CredentialType
    identity: str
    verified: bool

    @classmethod
    def from_dict(cls, _dict: dict) -> "Credential":
        return Credential(
            id=_dict["id"],
            type=CredentialType(_dict["identity_type"]),
            identity=_dict["identity"],
            verified=_dict["verified"],
        )


@dataclass
class User:
    id: UUID
    identities: [Credential]

    @classmethod
    def from_dict(cls, _dict) -> "User":
        return cls(
            id=_dict["id"],
            identities=[Credential.from_dict(cred) for cred in _dict["credentials"]],
        )

    @property
    def primary_cred(self):
        return self.identities[0]

    @property
    def primary_identity(self):
        return self.primary_cred.identity


@dataclass
class Session:
    id: str
    user: User

    @classmethod
    def from_dict(cls, _dict) -> "Session":
        user = User.from_dict(_dict.get("user"))
        return Session(_dict.get("session_id"), user=user)


@dataclass
class UserRequest:
    credential_type: CredentialType
    identity: str
    requires_verification: bool = True
    password: str = None
    region: str = CountryCode.INDIA
    id: str = None

    def to_dict(self):
        request = {
            "credential_type": self.credential_type.value,
            "identity": self.identity,
            "requires_verification": self.requires_verification,
            "region": str(self.region),
        }

        if self.password:
            request["password"] = self.password

        if self.id:
            request["id"] = self.id

        return request
