from enum import Enum


class Commands(Enum):
    CHANGE_USER = "ChangeUser"
    REGISTER_USER = "RegisterUser"


class RegisterUserCommandData:
    auth0_id: str
    email: str
    email_verified: bool
    first_name: str
    id: str
    last_name: str
    locale: str
    picture: str

    def __init__(self, auth0_id: str, email: str, email_verified: bool, first_name: str, id: str, last_name: str, locale: str, picture: str) -> None:
        self.auth0_id = auth0_id
        self.email = email
        self.email_verified = email_verified
        self.first_name = first_name
        self.id = id
        self.last_name = last_name
        self.locale = locale
        self.picture = picture


class Metadata:
    trace_id: str
    user_id: str

    def __init__(self, trace_id: str, user_id: str) -> None:
        self.trace_id = trace_id
        self.user_id = user_id


class RegisterUserCommandType(Enum):
    REGISTER_USER = "RegisterUser"


class RegisterUserCommand:
    data: RegisterUserCommandData
    id: str
    metadata: Metadata
    type: RegisterUserCommandType

    def __init__(self, data: RegisterUserCommandData, id: str, metadata: Metadata, type: RegisterUserCommandType) -> None:
        self.data = data
        self.id = id
        self.metadata = metadata
        self.type = type


class ChangeUserCommandData:
    first_name: str
    last_name: str
    locale: str
    picture: str

    def __init__(self, first_name: str, last_name: str, locale: str, picture: str) -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.locale = locale
        self.picture = picture


class ChangeUserCommandType(Enum):
    CHANGE_USER = "ChangeUser"


class ChangeUserCommand:
    data: ChangeUserCommandData
    id: str
    metadata: Metadata
    type: ChangeUserCommandType

    def __init__(self, data: ChangeUserCommandData, id: str, metadata: Metadata, type: ChangeUserCommandType) -> None:
        self.data = data
        self.id = id
        self.metadata = metadata
        self.type = type


class Events(Enum):
    USER_CHANGED = "UserChanged"
    USER_REGISTERED = "UserRegistered"


class UserRegisteredEventData:
    auth0_id: str
    email: str
    email_verified: bool
    first_name: str
    id: str
    last_name: str
    locale: str
    picture: str

    def __init__(self, auth0_id: str, email: str, email_verified: bool, first_name: str, id: str, last_name: str, locale: str, picture: str) -> None:
        self.auth0_id = auth0_id
        self.email = email
        self.email_verified = email_verified
        self.first_name = first_name
        self.id = id
        self.last_name = last_name
        self.locale = locale
        self.picture = picture


class UserRegisteredEventType(Enum):
    USER_REGISTERED = "UserRegistered"


class UserRegisteredEvent:
    data: UserRegisteredEventData
    id: str
    metadata: Metadata
    type: UserRegisteredEventType

    def __init__(self, data: UserRegisteredEventData, id: str, metadata: Metadata, type: UserRegisteredEventType) -> None:
        self.data = data
        self.id = id
        self.metadata = metadata
        self.type = type


class UserChangedEventData:
    first_name: str
    last_name: str
    locale: str
    picture: str

    def __init__(self, first_name: str, last_name: str, locale: str, picture: str) -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.locale = locale
        self.picture = picture


class UserChangedEventType(Enum):
    USER_CHANGED = "UserChanged"


class UserChangedEvent:
    data: UserChangedEventData
    id: str
    metadata: Metadata
    type: UserChangedEventType

    def __init__(self, data: UserChangedEventData, id: str, metadata: Metadata, type: UserChangedEventType) -> None:
        self.data = data
        self.id = id
        self.metadata = metadata
        self.type = type
