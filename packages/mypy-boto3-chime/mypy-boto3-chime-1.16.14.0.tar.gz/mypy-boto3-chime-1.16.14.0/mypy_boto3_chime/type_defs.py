"""
Main interface for chime service type definitions.

Usage::

    ```python
    from mypy_boto3_chime.type_defs import AccountSettingsTypeDef

    data: AccountSettingsTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import List

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "AccountSettingsTypeDef",
    "AccountTypeDef",
    "AlexaForBusinessMetadataTypeDef",
    "AttendeeTypeDef",
    "BotTypeDef",
    "BusinessCallingSettingsTypeDef",
    "ConversationRetentionSettingsTypeDef",
    "CreateAttendeeErrorTypeDef",
    "DNISEmergencyCallingConfigurationTypeDef",
    "EmergencyCallingConfigurationTypeDef",
    "EventsConfigurationTypeDef",
    "GeoMatchParamsTypeDef",
    "InviteTypeDef",
    "LoggingConfigurationTypeDef",
    "MediaPlacementTypeDef",
    "MeetingTypeDef",
    "MemberErrorTypeDef",
    "MemberTypeDef",
    "OrderedPhoneNumberTypeDef",
    "OriginationRouteTypeDef",
    "OriginationTypeDef",
    "ParticipantTypeDef",
    "PhoneNumberAssociationTypeDef",
    "PhoneNumberCapabilitiesTypeDef",
    "PhoneNumberErrorTypeDef",
    "PhoneNumberOrderTypeDef",
    "PhoneNumberTypeDef",
    "ProxySessionTypeDef",
    "ProxyTypeDef",
    "RetentionSettingsTypeDef",
    "RoomMembershipTypeDef",
    "RoomRetentionSettingsTypeDef",
    "RoomTypeDef",
    "SigninDelegateGroupTypeDef",
    "StreamingConfigurationTypeDef",
    "StreamingNotificationTargetTypeDef",
    "TagTypeDef",
    "TelephonySettingsTypeDef",
    "TerminationHealthTypeDef",
    "TerminationTypeDef",
    "UserErrorTypeDef",
    "UserSettingsTypeDef",
    "UserTypeDef",
    "VoiceConnectorGroupTypeDef",
    "VoiceConnectorItemTypeDef",
    "VoiceConnectorSettingsTypeDef",
    "VoiceConnectorTypeDef",
    "AssociatePhoneNumbersWithVoiceConnectorGroupResponseTypeDef",
    "AssociatePhoneNumbersWithVoiceConnectorResponseTypeDef",
    "BatchCreateAttendeeResponseTypeDef",
    "BatchCreateRoomMembershipResponseTypeDef",
    "BatchDeletePhoneNumberResponseTypeDef",
    "BatchSuspendUserResponseTypeDef",
    "BatchUnsuspendUserResponseTypeDef",
    "BatchUpdatePhoneNumberResponseTypeDef",
    "BatchUpdateUserResponseTypeDef",
    "CreateAccountResponseTypeDef",
    "CreateAttendeeRequestItemTypeDef",
    "CreateAttendeeResponseTypeDef",
    "CreateBotResponseTypeDef",
    "CreateMeetingResponseTypeDef",
    "CreateMeetingWithAttendeesResponseTypeDef",
    "CreatePhoneNumberOrderResponseTypeDef",
    "CreateProxySessionResponseTypeDef",
    "CreateRoomMembershipResponseTypeDef",
    "CreateRoomResponseTypeDef",
    "CreateUserResponseTypeDef",
    "CreateVoiceConnectorGroupResponseTypeDef",
    "CreateVoiceConnectorResponseTypeDef",
    "CredentialTypeDef",
    "DisassociatePhoneNumbersFromVoiceConnectorGroupResponseTypeDef",
    "DisassociatePhoneNumbersFromVoiceConnectorResponseTypeDef",
    "GetAccountResponseTypeDef",
    "GetAccountSettingsResponseTypeDef",
    "GetAttendeeResponseTypeDef",
    "GetBotResponseTypeDef",
    "GetEventsConfigurationResponseTypeDef",
    "GetGlobalSettingsResponseTypeDef",
    "GetMeetingResponseTypeDef",
    "GetPhoneNumberOrderResponseTypeDef",
    "GetPhoneNumberResponseTypeDef",
    "GetPhoneNumberSettingsResponseTypeDef",
    "GetProxySessionResponseTypeDef",
    "GetRetentionSettingsResponseTypeDef",
    "GetRoomResponseTypeDef",
    "GetUserResponseTypeDef",
    "GetUserSettingsResponseTypeDef",
    "GetVoiceConnectorEmergencyCallingConfigurationResponseTypeDef",
    "GetVoiceConnectorGroupResponseTypeDef",
    "GetVoiceConnectorLoggingConfigurationResponseTypeDef",
    "GetVoiceConnectorOriginationResponseTypeDef",
    "GetVoiceConnectorProxyResponseTypeDef",
    "GetVoiceConnectorResponseTypeDef",
    "GetVoiceConnectorStreamingConfigurationResponseTypeDef",
    "GetVoiceConnectorTerminationHealthResponseTypeDef",
    "GetVoiceConnectorTerminationResponseTypeDef",
    "InviteUsersResponseTypeDef",
    "ListAccountsResponseTypeDef",
    "ListAttendeeTagsResponseTypeDef",
    "ListAttendeesResponseTypeDef",
    "ListBotsResponseTypeDef",
    "ListMeetingTagsResponseTypeDef",
    "ListMeetingsResponseTypeDef",
    "ListPhoneNumberOrdersResponseTypeDef",
    "ListPhoneNumbersResponseTypeDef",
    "ListProxySessionsResponseTypeDef",
    "ListRoomMembershipsResponseTypeDef",
    "ListRoomsResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ListUsersResponseTypeDef",
    "ListVoiceConnectorGroupsResponseTypeDef",
    "ListVoiceConnectorTerminationCredentialsResponseTypeDef",
    "ListVoiceConnectorsResponseTypeDef",
    "MeetingNotificationConfigurationTypeDef",
    "MembershipItemTypeDef",
    "PaginatorConfigTypeDef",
    "PutEventsConfigurationResponseTypeDef",
    "PutRetentionSettingsResponseTypeDef",
    "PutVoiceConnectorEmergencyCallingConfigurationResponseTypeDef",
    "PutVoiceConnectorLoggingConfigurationResponseTypeDef",
    "PutVoiceConnectorOriginationResponseTypeDef",
    "PutVoiceConnectorProxyResponseTypeDef",
    "PutVoiceConnectorStreamingConfigurationResponseTypeDef",
    "PutVoiceConnectorTerminationResponseTypeDef",
    "RegenerateSecurityTokenResponseTypeDef",
    "ResetPersonalPINResponseTypeDef",
    "RestorePhoneNumberResponseTypeDef",
    "SearchAvailablePhoneNumbersResponseTypeDef",
    "UpdateAccountResponseTypeDef",
    "UpdateBotResponseTypeDef",
    "UpdatePhoneNumberRequestItemTypeDef",
    "UpdatePhoneNumberResponseTypeDef",
    "UpdateProxySessionResponseTypeDef",
    "UpdateRoomMembershipResponseTypeDef",
    "UpdateRoomResponseTypeDef",
    "UpdateUserRequestItemTypeDef",
    "UpdateUserResponseTypeDef",
    "UpdateVoiceConnectorGroupResponseTypeDef",
    "UpdateVoiceConnectorResponseTypeDef",
)

AccountSettingsTypeDef = TypedDict(
    "AccountSettingsTypeDef", {"DisableRemoteControl": bool, "EnableDialOut": bool}, total=False
)

_RequiredAccountTypeDef = TypedDict(
    "_RequiredAccountTypeDef", {"AwsAccountId": str, "AccountId": str, "Name": str}
)
_OptionalAccountTypeDef = TypedDict(
    "_OptionalAccountTypeDef",
    {
        "AccountType": Literal["Team", "EnterpriseDirectory", "EnterpriseLWA", "EnterpriseOIDC"],
        "CreatedTimestamp": datetime,
        "DefaultLicense": Literal["Basic", "Plus", "Pro", "ProTrial"],
        "SupportedLicenses": List[Literal["Basic", "Plus", "Pro", "ProTrial"]],
        "SigninDelegateGroups": List["SigninDelegateGroupTypeDef"],
    },
    total=False,
)


class AccountTypeDef(_RequiredAccountTypeDef, _OptionalAccountTypeDef):
    pass


AlexaForBusinessMetadataTypeDef = TypedDict(
    "AlexaForBusinessMetadataTypeDef",
    {"IsAlexaForBusinessEnabled": bool, "AlexaForBusinessRoomArn": str},
    total=False,
)

AttendeeTypeDef = TypedDict(
    "AttendeeTypeDef", {"ExternalUserId": str, "AttendeeId": str, "JoinToken": str}, total=False
)

BotTypeDef = TypedDict(
    "BotTypeDef",
    {
        "BotId": str,
        "UserId": str,
        "DisplayName": str,
        "BotType": Literal["ChatBot"],
        "Disabled": bool,
        "CreatedTimestamp": datetime,
        "UpdatedTimestamp": datetime,
        "BotEmail": str,
        "SecurityToken": str,
    },
    total=False,
)

BusinessCallingSettingsTypeDef = TypedDict(
    "BusinessCallingSettingsTypeDef", {"CdrBucket": str}, total=False
)

ConversationRetentionSettingsTypeDef = TypedDict(
    "ConversationRetentionSettingsTypeDef", {"RetentionDays": int}, total=False
)

CreateAttendeeErrorTypeDef = TypedDict(
    "CreateAttendeeErrorTypeDef",
    {"ExternalUserId": str, "ErrorCode": str, "ErrorMessage": str},
    total=False,
)

_RequiredDNISEmergencyCallingConfigurationTypeDef = TypedDict(
    "_RequiredDNISEmergencyCallingConfigurationTypeDef",
    {"EmergencyPhoneNumber": str, "CallingCountry": str},
)
_OptionalDNISEmergencyCallingConfigurationTypeDef = TypedDict(
    "_OptionalDNISEmergencyCallingConfigurationTypeDef", {"TestPhoneNumber": str}, total=False
)


class DNISEmergencyCallingConfigurationTypeDef(
    _RequiredDNISEmergencyCallingConfigurationTypeDef,
    _OptionalDNISEmergencyCallingConfigurationTypeDef,
):
    pass


EmergencyCallingConfigurationTypeDef = TypedDict(
    "EmergencyCallingConfigurationTypeDef",
    {"DNIS": List["DNISEmergencyCallingConfigurationTypeDef"]},
    total=False,
)

EventsConfigurationTypeDef = TypedDict(
    "EventsConfigurationTypeDef",
    {"BotId": str, "OutboundEventsHTTPSEndpoint": str, "LambdaFunctionArn": str},
    total=False,
)

GeoMatchParamsTypeDef = TypedDict("GeoMatchParamsTypeDef", {"Country": str, "AreaCode": str})

InviteTypeDef = TypedDict(
    "InviteTypeDef",
    {
        "InviteId": str,
        "Status": Literal["Pending", "Accepted", "Failed"],
        "EmailAddress": str,
        "EmailStatus": Literal["NotSent", "Sent", "Failed"],
    },
    total=False,
)

LoggingConfigurationTypeDef = TypedDict(
    "LoggingConfigurationTypeDef", {"EnableSIPLogs": bool}, total=False
)

MediaPlacementTypeDef = TypedDict(
    "MediaPlacementTypeDef",
    {
        "AudioHostUrl": str,
        "AudioFallbackUrl": str,
        "ScreenDataUrl": str,
        "ScreenSharingUrl": str,
        "ScreenViewingUrl": str,
        "SignalingUrl": str,
        "TurnControlUrl": str,
    },
    total=False,
)

MeetingTypeDef = TypedDict(
    "MeetingTypeDef",
    {
        "MeetingId": str,
        "ExternalMeetingId": str,
        "MediaPlacement": "MediaPlacementTypeDef",
        "MediaRegion": str,
    },
    total=False,
)

MemberErrorTypeDef = TypedDict(
    "MemberErrorTypeDef",
    {
        "MemberId": str,
        "ErrorCode": Literal[
            "BadRequest",
            "Conflict",
            "Forbidden",
            "NotFound",
            "PreconditionFailed",
            "ResourceLimitExceeded",
            "ServiceFailure",
            "AccessDenied",
            "ServiceUnavailable",
            "Throttled",
            "Throttling",
            "Unauthorized",
            "Unprocessable",
            "VoiceConnectorGroupAssociationsExist",
            "PhoneNumberAssociationsExist",
        ],
        "ErrorMessage": str,
    },
    total=False,
)

MemberTypeDef = TypedDict(
    "MemberTypeDef",
    {
        "MemberId": str,
        "MemberType": Literal["User", "Bot", "Webhook"],
        "Email": str,
        "FullName": str,
        "AccountId": str,
    },
    total=False,
)

OrderedPhoneNumberTypeDef = TypedDict(
    "OrderedPhoneNumberTypeDef",
    {"E164PhoneNumber": str, "Status": Literal["Processing", "Acquired", "Failed"]},
    total=False,
)

OriginationRouteTypeDef = TypedDict(
    "OriginationRouteTypeDef",
    {"Host": str, "Port": int, "Protocol": Literal["TCP", "UDP"], "Priority": int, "Weight": int},
    total=False,
)

OriginationTypeDef = TypedDict(
    "OriginationTypeDef", {"Routes": List["OriginationRouteTypeDef"], "Disabled": bool}, total=False
)

ParticipantTypeDef = TypedDict(
    "ParticipantTypeDef", {"PhoneNumber": str, "ProxyPhoneNumber": str}, total=False
)

PhoneNumberAssociationTypeDef = TypedDict(
    "PhoneNumberAssociationTypeDef",
    {
        "Value": str,
        "Name": Literal["AccountId", "UserId", "VoiceConnectorId", "VoiceConnectorGroupId"],
        "AssociatedTimestamp": datetime,
    },
    total=False,
)

PhoneNumberCapabilitiesTypeDef = TypedDict(
    "PhoneNumberCapabilitiesTypeDef",
    {
        "InboundCall": bool,
        "OutboundCall": bool,
        "InboundSMS": bool,
        "OutboundSMS": bool,
        "InboundMMS": bool,
        "OutboundMMS": bool,
    },
    total=False,
)

PhoneNumberErrorTypeDef = TypedDict(
    "PhoneNumberErrorTypeDef",
    {
        "PhoneNumberId": str,
        "ErrorCode": Literal[
            "BadRequest",
            "Conflict",
            "Forbidden",
            "NotFound",
            "PreconditionFailed",
            "ResourceLimitExceeded",
            "ServiceFailure",
            "AccessDenied",
            "ServiceUnavailable",
            "Throttled",
            "Throttling",
            "Unauthorized",
            "Unprocessable",
            "VoiceConnectorGroupAssociationsExist",
            "PhoneNumberAssociationsExist",
        ],
        "ErrorMessage": str,
    },
    total=False,
)

PhoneNumberOrderTypeDef = TypedDict(
    "PhoneNumberOrderTypeDef",
    {
        "PhoneNumberOrderId": str,
        "ProductType": Literal["BusinessCalling", "VoiceConnector"],
        "Status": Literal["Processing", "Successful", "Failed", "Partial"],
        "OrderedPhoneNumbers": List["OrderedPhoneNumberTypeDef"],
        "CreatedTimestamp": datetime,
        "UpdatedTimestamp": datetime,
    },
    total=False,
)

PhoneNumberTypeDef = TypedDict(
    "PhoneNumberTypeDef",
    {
        "PhoneNumberId": str,
        "E164PhoneNumber": str,
        "Type": Literal["Local", "TollFree"],
        "ProductType": Literal["BusinessCalling", "VoiceConnector"],
        "Status": Literal[
            "AcquireInProgress",
            "AcquireFailed",
            "Unassigned",
            "Assigned",
            "ReleaseInProgress",
            "DeleteInProgress",
            "ReleaseFailed",
            "DeleteFailed",
        ],
        "Capabilities": "PhoneNumberCapabilitiesTypeDef",
        "Associations": List["PhoneNumberAssociationTypeDef"],
        "CallingName": str,
        "CallingNameStatus": Literal[
            "Unassigned", "UpdateInProgress", "UpdateSucceeded", "UpdateFailed"
        ],
        "CreatedTimestamp": datetime,
        "UpdatedTimestamp": datetime,
        "DeletionTimestamp": datetime,
    },
    total=False,
)

ProxySessionTypeDef = TypedDict(
    "ProxySessionTypeDef",
    {
        "VoiceConnectorId": str,
        "ProxySessionId": str,
        "Name": str,
        "Status": Literal["Open", "InProgress", "Closed"],
        "ExpiryMinutes": int,
        "Capabilities": List[Literal["Voice", "SMS"]],
        "CreatedTimestamp": datetime,
        "UpdatedTimestamp": datetime,
        "EndedTimestamp": datetime,
        "Participants": List["ParticipantTypeDef"],
        "NumberSelectionBehavior": Literal["PreferSticky", "AvoidSticky"],
        "GeoMatchLevel": Literal["Country", "AreaCode"],
        "GeoMatchParams": "GeoMatchParamsTypeDef",
    },
    total=False,
)

ProxyTypeDef = TypedDict(
    "ProxyTypeDef",
    {
        "DefaultSessionExpiryMinutes": int,
        "Disabled": bool,
        "FallBackPhoneNumber": str,
        "PhoneNumberCountries": List[str],
    },
    total=False,
)

RetentionSettingsTypeDef = TypedDict(
    "RetentionSettingsTypeDef",
    {
        "RoomRetentionSettings": "RoomRetentionSettingsTypeDef",
        "ConversationRetentionSettings": "ConversationRetentionSettingsTypeDef",
    },
    total=False,
)

RoomMembershipTypeDef = TypedDict(
    "RoomMembershipTypeDef",
    {
        "RoomId": str,
        "Member": "MemberTypeDef",
        "Role": Literal["Administrator", "Member"],
        "InvitedBy": str,
        "UpdatedTimestamp": datetime,
    },
    total=False,
)

RoomRetentionSettingsTypeDef = TypedDict(
    "RoomRetentionSettingsTypeDef", {"RetentionDays": int}, total=False
)

RoomTypeDef = TypedDict(
    "RoomTypeDef",
    {
        "RoomId": str,
        "Name": str,
        "AccountId": str,
        "CreatedBy": str,
        "CreatedTimestamp": datetime,
        "UpdatedTimestamp": datetime,
    },
    total=False,
)

SigninDelegateGroupTypeDef = TypedDict(
    "SigninDelegateGroupTypeDef", {"GroupName": str}, total=False
)

_RequiredStreamingConfigurationTypeDef = TypedDict(
    "_RequiredStreamingConfigurationTypeDef", {"DataRetentionInHours": int}
)
_OptionalStreamingConfigurationTypeDef = TypedDict(
    "_OptionalStreamingConfigurationTypeDef",
    {"Disabled": bool, "StreamingNotificationTargets": List["StreamingNotificationTargetTypeDef"]},
    total=False,
)


class StreamingConfigurationTypeDef(
    _RequiredStreamingConfigurationTypeDef, _OptionalStreamingConfigurationTypeDef
):
    pass


StreamingNotificationTargetTypeDef = TypedDict(
    "StreamingNotificationTargetTypeDef",
    {"NotificationTarget": Literal["EventBridge", "SNS", "SQS"]},
)

TagTypeDef = TypedDict("TagTypeDef", {"Key": str, "Value": str})

TelephonySettingsTypeDef = TypedDict(
    "TelephonySettingsTypeDef", {"InboundCalling": bool, "OutboundCalling": bool, "SMS": bool}
)

TerminationHealthTypeDef = TypedDict(
    "TerminationHealthTypeDef", {"Timestamp": datetime, "Source": str}, total=False
)

TerminationTypeDef = TypedDict(
    "TerminationTypeDef",
    {
        "CpsLimit": int,
        "DefaultPhoneNumber": str,
        "CallingRegions": List[str],
        "CidrAllowedList": List[str],
        "Disabled": bool,
    },
    total=False,
)

UserErrorTypeDef = TypedDict(
    "UserErrorTypeDef",
    {
        "UserId": str,
        "ErrorCode": Literal[
            "BadRequest",
            "Conflict",
            "Forbidden",
            "NotFound",
            "PreconditionFailed",
            "ResourceLimitExceeded",
            "ServiceFailure",
            "AccessDenied",
            "ServiceUnavailable",
            "Throttled",
            "Throttling",
            "Unauthorized",
            "Unprocessable",
            "VoiceConnectorGroupAssociationsExist",
            "PhoneNumberAssociationsExist",
        ],
        "ErrorMessage": str,
    },
    total=False,
)

UserSettingsTypeDef = TypedDict("UserSettingsTypeDef", {"Telephony": "TelephonySettingsTypeDef"})

_RequiredUserTypeDef = TypedDict("_RequiredUserTypeDef", {"UserId": str})
_OptionalUserTypeDef = TypedDict(
    "_OptionalUserTypeDef",
    {
        "AccountId": str,
        "PrimaryEmail": str,
        "PrimaryProvisionedNumber": str,
        "DisplayName": str,
        "LicenseType": Literal["Basic", "Plus", "Pro", "ProTrial"],
        "UserType": Literal["PrivateUser", "SharedDevice"],
        "UserRegistrationStatus": Literal["Unregistered", "Registered", "Suspended"],
        "UserInvitationStatus": Literal["Pending", "Accepted", "Failed"],
        "RegisteredOn": datetime,
        "InvitedOn": datetime,
        "AlexaForBusinessMetadata": "AlexaForBusinessMetadataTypeDef",
        "PersonalPIN": str,
    },
    total=False,
)


class UserTypeDef(_RequiredUserTypeDef, _OptionalUserTypeDef):
    pass


VoiceConnectorGroupTypeDef = TypedDict(
    "VoiceConnectorGroupTypeDef",
    {
        "VoiceConnectorGroupId": str,
        "Name": str,
        "VoiceConnectorItems": List["VoiceConnectorItemTypeDef"],
        "CreatedTimestamp": datetime,
        "UpdatedTimestamp": datetime,
    },
    total=False,
)

VoiceConnectorItemTypeDef = TypedDict(
    "VoiceConnectorItemTypeDef", {"VoiceConnectorId": str, "Priority": int}
)

VoiceConnectorSettingsTypeDef = TypedDict(
    "VoiceConnectorSettingsTypeDef", {"CdrBucket": str}, total=False
)

VoiceConnectorTypeDef = TypedDict(
    "VoiceConnectorTypeDef",
    {
        "VoiceConnectorId": str,
        "AwsRegion": Literal["us-east-1", "us-west-2"],
        "Name": str,
        "OutboundHostName": str,
        "RequireEncryption": bool,
        "CreatedTimestamp": datetime,
        "UpdatedTimestamp": datetime,
    },
    total=False,
)

AssociatePhoneNumbersWithVoiceConnectorGroupResponseTypeDef = TypedDict(
    "AssociatePhoneNumbersWithVoiceConnectorGroupResponseTypeDef",
    {"PhoneNumberErrors": List["PhoneNumberErrorTypeDef"]},
    total=False,
)

AssociatePhoneNumbersWithVoiceConnectorResponseTypeDef = TypedDict(
    "AssociatePhoneNumbersWithVoiceConnectorResponseTypeDef",
    {"PhoneNumberErrors": List["PhoneNumberErrorTypeDef"]},
    total=False,
)

BatchCreateAttendeeResponseTypeDef = TypedDict(
    "BatchCreateAttendeeResponseTypeDef",
    {"Attendees": List["AttendeeTypeDef"], "Errors": List["CreateAttendeeErrorTypeDef"]},
    total=False,
)

BatchCreateRoomMembershipResponseTypeDef = TypedDict(
    "BatchCreateRoomMembershipResponseTypeDef", {"Errors": List["MemberErrorTypeDef"]}, total=False
)

BatchDeletePhoneNumberResponseTypeDef = TypedDict(
    "BatchDeletePhoneNumberResponseTypeDef",
    {"PhoneNumberErrors": List["PhoneNumberErrorTypeDef"]},
    total=False,
)

BatchSuspendUserResponseTypeDef = TypedDict(
    "BatchSuspendUserResponseTypeDef", {"UserErrors": List["UserErrorTypeDef"]}, total=False
)

BatchUnsuspendUserResponseTypeDef = TypedDict(
    "BatchUnsuspendUserResponseTypeDef", {"UserErrors": List["UserErrorTypeDef"]}, total=False
)

BatchUpdatePhoneNumberResponseTypeDef = TypedDict(
    "BatchUpdatePhoneNumberResponseTypeDef",
    {"PhoneNumberErrors": List["PhoneNumberErrorTypeDef"]},
    total=False,
)

BatchUpdateUserResponseTypeDef = TypedDict(
    "BatchUpdateUserResponseTypeDef", {"UserErrors": List["UserErrorTypeDef"]}, total=False
)

CreateAccountResponseTypeDef = TypedDict(
    "CreateAccountResponseTypeDef", {"Account": "AccountTypeDef"}, total=False
)

_RequiredCreateAttendeeRequestItemTypeDef = TypedDict(
    "_RequiredCreateAttendeeRequestItemTypeDef", {"ExternalUserId": str}
)
_OptionalCreateAttendeeRequestItemTypeDef = TypedDict(
    "_OptionalCreateAttendeeRequestItemTypeDef", {"Tags": List["TagTypeDef"]}, total=False
)


class CreateAttendeeRequestItemTypeDef(
    _RequiredCreateAttendeeRequestItemTypeDef, _OptionalCreateAttendeeRequestItemTypeDef
):
    pass


CreateAttendeeResponseTypeDef = TypedDict(
    "CreateAttendeeResponseTypeDef", {"Attendee": "AttendeeTypeDef"}, total=False
)

CreateBotResponseTypeDef = TypedDict("CreateBotResponseTypeDef", {"Bot": "BotTypeDef"}, total=False)

CreateMeetingResponseTypeDef = TypedDict(
    "CreateMeetingResponseTypeDef", {"Meeting": "MeetingTypeDef"}, total=False
)

CreateMeetingWithAttendeesResponseTypeDef = TypedDict(
    "CreateMeetingWithAttendeesResponseTypeDef",
    {
        "Meeting": "MeetingTypeDef",
        "Attendees": List["AttendeeTypeDef"],
        "Errors": List["CreateAttendeeErrorTypeDef"],
    },
    total=False,
)

CreatePhoneNumberOrderResponseTypeDef = TypedDict(
    "CreatePhoneNumberOrderResponseTypeDef",
    {"PhoneNumberOrder": "PhoneNumberOrderTypeDef"},
    total=False,
)

CreateProxySessionResponseTypeDef = TypedDict(
    "CreateProxySessionResponseTypeDef", {"ProxySession": "ProxySessionTypeDef"}, total=False
)

CreateRoomMembershipResponseTypeDef = TypedDict(
    "CreateRoomMembershipResponseTypeDef", {"RoomMembership": "RoomMembershipTypeDef"}, total=False
)

CreateRoomResponseTypeDef = TypedDict(
    "CreateRoomResponseTypeDef", {"Room": "RoomTypeDef"}, total=False
)

CreateUserResponseTypeDef = TypedDict(
    "CreateUserResponseTypeDef", {"User": "UserTypeDef"}, total=False
)

CreateVoiceConnectorGroupResponseTypeDef = TypedDict(
    "CreateVoiceConnectorGroupResponseTypeDef",
    {"VoiceConnectorGroup": "VoiceConnectorGroupTypeDef"},
    total=False,
)

CreateVoiceConnectorResponseTypeDef = TypedDict(
    "CreateVoiceConnectorResponseTypeDef", {"VoiceConnector": "VoiceConnectorTypeDef"}, total=False
)

CredentialTypeDef = TypedDict("CredentialTypeDef", {"Username": str, "Password": str}, total=False)

DisassociatePhoneNumbersFromVoiceConnectorGroupResponseTypeDef = TypedDict(
    "DisassociatePhoneNumbersFromVoiceConnectorGroupResponseTypeDef",
    {"PhoneNumberErrors": List["PhoneNumberErrorTypeDef"]},
    total=False,
)

DisassociatePhoneNumbersFromVoiceConnectorResponseTypeDef = TypedDict(
    "DisassociatePhoneNumbersFromVoiceConnectorResponseTypeDef",
    {"PhoneNumberErrors": List["PhoneNumberErrorTypeDef"]},
    total=False,
)

GetAccountResponseTypeDef = TypedDict(
    "GetAccountResponseTypeDef", {"Account": "AccountTypeDef"}, total=False
)

GetAccountSettingsResponseTypeDef = TypedDict(
    "GetAccountSettingsResponseTypeDef", {"AccountSettings": "AccountSettingsTypeDef"}, total=False
)

GetAttendeeResponseTypeDef = TypedDict(
    "GetAttendeeResponseTypeDef", {"Attendee": "AttendeeTypeDef"}, total=False
)

GetBotResponseTypeDef = TypedDict("GetBotResponseTypeDef", {"Bot": "BotTypeDef"}, total=False)

GetEventsConfigurationResponseTypeDef = TypedDict(
    "GetEventsConfigurationResponseTypeDef",
    {"EventsConfiguration": "EventsConfigurationTypeDef"},
    total=False,
)

GetGlobalSettingsResponseTypeDef = TypedDict(
    "GetGlobalSettingsResponseTypeDef",
    {
        "BusinessCalling": "BusinessCallingSettingsTypeDef",
        "VoiceConnector": "VoiceConnectorSettingsTypeDef",
    },
    total=False,
)

GetMeetingResponseTypeDef = TypedDict(
    "GetMeetingResponseTypeDef", {"Meeting": "MeetingTypeDef"}, total=False
)

GetPhoneNumberOrderResponseTypeDef = TypedDict(
    "GetPhoneNumberOrderResponseTypeDef",
    {"PhoneNumberOrder": "PhoneNumberOrderTypeDef"},
    total=False,
)

GetPhoneNumberResponseTypeDef = TypedDict(
    "GetPhoneNumberResponseTypeDef", {"PhoneNumber": "PhoneNumberTypeDef"}, total=False
)

GetPhoneNumberSettingsResponseTypeDef = TypedDict(
    "GetPhoneNumberSettingsResponseTypeDef",
    {"CallingName": str, "CallingNameUpdatedTimestamp": datetime},
    total=False,
)

GetProxySessionResponseTypeDef = TypedDict(
    "GetProxySessionResponseTypeDef", {"ProxySession": "ProxySessionTypeDef"}, total=False
)

GetRetentionSettingsResponseTypeDef = TypedDict(
    "GetRetentionSettingsResponseTypeDef",
    {"RetentionSettings": "RetentionSettingsTypeDef", "InitiateDeletionTimestamp": datetime},
    total=False,
)

GetRoomResponseTypeDef = TypedDict("GetRoomResponseTypeDef", {"Room": "RoomTypeDef"}, total=False)

GetUserResponseTypeDef = TypedDict("GetUserResponseTypeDef", {"User": "UserTypeDef"}, total=False)

GetUserSettingsResponseTypeDef = TypedDict(
    "GetUserSettingsResponseTypeDef", {"UserSettings": "UserSettingsTypeDef"}, total=False
)

GetVoiceConnectorEmergencyCallingConfigurationResponseTypeDef = TypedDict(
    "GetVoiceConnectorEmergencyCallingConfigurationResponseTypeDef",
    {"EmergencyCallingConfiguration": "EmergencyCallingConfigurationTypeDef"},
    total=False,
)

GetVoiceConnectorGroupResponseTypeDef = TypedDict(
    "GetVoiceConnectorGroupResponseTypeDef",
    {"VoiceConnectorGroup": "VoiceConnectorGroupTypeDef"},
    total=False,
)

GetVoiceConnectorLoggingConfigurationResponseTypeDef = TypedDict(
    "GetVoiceConnectorLoggingConfigurationResponseTypeDef",
    {"LoggingConfiguration": "LoggingConfigurationTypeDef"},
    total=False,
)

GetVoiceConnectorOriginationResponseTypeDef = TypedDict(
    "GetVoiceConnectorOriginationResponseTypeDef",
    {"Origination": "OriginationTypeDef"},
    total=False,
)

GetVoiceConnectorProxyResponseTypeDef = TypedDict(
    "GetVoiceConnectorProxyResponseTypeDef", {"Proxy": "ProxyTypeDef"}, total=False
)

GetVoiceConnectorResponseTypeDef = TypedDict(
    "GetVoiceConnectorResponseTypeDef", {"VoiceConnector": "VoiceConnectorTypeDef"}, total=False
)

GetVoiceConnectorStreamingConfigurationResponseTypeDef = TypedDict(
    "GetVoiceConnectorStreamingConfigurationResponseTypeDef",
    {"StreamingConfiguration": "StreamingConfigurationTypeDef"},
    total=False,
)

GetVoiceConnectorTerminationHealthResponseTypeDef = TypedDict(
    "GetVoiceConnectorTerminationHealthResponseTypeDef",
    {"TerminationHealth": "TerminationHealthTypeDef"},
    total=False,
)

GetVoiceConnectorTerminationResponseTypeDef = TypedDict(
    "GetVoiceConnectorTerminationResponseTypeDef",
    {"Termination": "TerminationTypeDef"},
    total=False,
)

InviteUsersResponseTypeDef = TypedDict(
    "InviteUsersResponseTypeDef", {"Invites": List["InviteTypeDef"]}, total=False
)

ListAccountsResponseTypeDef = TypedDict(
    "ListAccountsResponseTypeDef",
    {"Accounts": List["AccountTypeDef"], "NextToken": str},
    total=False,
)

ListAttendeeTagsResponseTypeDef = TypedDict(
    "ListAttendeeTagsResponseTypeDef", {"Tags": List["TagTypeDef"]}, total=False
)

ListAttendeesResponseTypeDef = TypedDict(
    "ListAttendeesResponseTypeDef",
    {"Attendees": List["AttendeeTypeDef"], "NextToken": str},
    total=False,
)

ListBotsResponseTypeDef = TypedDict(
    "ListBotsResponseTypeDef", {"Bots": List["BotTypeDef"], "NextToken": str}, total=False
)

ListMeetingTagsResponseTypeDef = TypedDict(
    "ListMeetingTagsResponseTypeDef", {"Tags": List["TagTypeDef"]}, total=False
)

ListMeetingsResponseTypeDef = TypedDict(
    "ListMeetingsResponseTypeDef",
    {"Meetings": List["MeetingTypeDef"], "NextToken": str},
    total=False,
)

ListPhoneNumberOrdersResponseTypeDef = TypedDict(
    "ListPhoneNumberOrdersResponseTypeDef",
    {"PhoneNumberOrders": List["PhoneNumberOrderTypeDef"], "NextToken": str},
    total=False,
)

ListPhoneNumbersResponseTypeDef = TypedDict(
    "ListPhoneNumbersResponseTypeDef",
    {"PhoneNumbers": List["PhoneNumberTypeDef"], "NextToken": str},
    total=False,
)

ListProxySessionsResponseTypeDef = TypedDict(
    "ListProxySessionsResponseTypeDef",
    {"ProxySessions": List["ProxySessionTypeDef"], "NextToken": str},
    total=False,
)

ListRoomMembershipsResponseTypeDef = TypedDict(
    "ListRoomMembershipsResponseTypeDef",
    {"RoomMemberships": List["RoomMembershipTypeDef"], "NextToken": str},
    total=False,
)

ListRoomsResponseTypeDef = TypedDict(
    "ListRoomsResponseTypeDef", {"Rooms": List["RoomTypeDef"], "NextToken": str}, total=False
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef", {"Tags": List["TagTypeDef"]}, total=False
)

ListUsersResponseTypeDef = TypedDict(
    "ListUsersResponseTypeDef", {"Users": List["UserTypeDef"], "NextToken": str}, total=False
)

ListVoiceConnectorGroupsResponseTypeDef = TypedDict(
    "ListVoiceConnectorGroupsResponseTypeDef",
    {"VoiceConnectorGroups": List["VoiceConnectorGroupTypeDef"], "NextToken": str},
    total=False,
)

ListVoiceConnectorTerminationCredentialsResponseTypeDef = TypedDict(
    "ListVoiceConnectorTerminationCredentialsResponseTypeDef", {"Usernames": List[str]}, total=False
)

ListVoiceConnectorsResponseTypeDef = TypedDict(
    "ListVoiceConnectorsResponseTypeDef",
    {"VoiceConnectors": List["VoiceConnectorTypeDef"], "NextToken": str},
    total=False,
)

MeetingNotificationConfigurationTypeDef = TypedDict(
    "MeetingNotificationConfigurationTypeDef", {"SnsTopicArn": str, "SqsQueueArn": str}, total=False
)

MembershipItemTypeDef = TypedDict(
    "MembershipItemTypeDef",
    {"MemberId": str, "Role": Literal["Administrator", "Member"]},
    total=False,
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef", {"MaxItems": int, "PageSize": int, "StartingToken": str}, total=False
)

PutEventsConfigurationResponseTypeDef = TypedDict(
    "PutEventsConfigurationResponseTypeDef",
    {"EventsConfiguration": "EventsConfigurationTypeDef"},
    total=False,
)

PutRetentionSettingsResponseTypeDef = TypedDict(
    "PutRetentionSettingsResponseTypeDef",
    {"RetentionSettings": "RetentionSettingsTypeDef", "InitiateDeletionTimestamp": datetime},
    total=False,
)

PutVoiceConnectorEmergencyCallingConfigurationResponseTypeDef = TypedDict(
    "PutVoiceConnectorEmergencyCallingConfigurationResponseTypeDef",
    {"EmergencyCallingConfiguration": "EmergencyCallingConfigurationTypeDef"},
    total=False,
)

PutVoiceConnectorLoggingConfigurationResponseTypeDef = TypedDict(
    "PutVoiceConnectorLoggingConfigurationResponseTypeDef",
    {"LoggingConfiguration": "LoggingConfigurationTypeDef"},
    total=False,
)

PutVoiceConnectorOriginationResponseTypeDef = TypedDict(
    "PutVoiceConnectorOriginationResponseTypeDef",
    {"Origination": "OriginationTypeDef"},
    total=False,
)

PutVoiceConnectorProxyResponseTypeDef = TypedDict(
    "PutVoiceConnectorProxyResponseTypeDef", {"Proxy": "ProxyTypeDef"}, total=False
)

PutVoiceConnectorStreamingConfigurationResponseTypeDef = TypedDict(
    "PutVoiceConnectorStreamingConfigurationResponseTypeDef",
    {"StreamingConfiguration": "StreamingConfigurationTypeDef"},
    total=False,
)

PutVoiceConnectorTerminationResponseTypeDef = TypedDict(
    "PutVoiceConnectorTerminationResponseTypeDef",
    {"Termination": "TerminationTypeDef"},
    total=False,
)

RegenerateSecurityTokenResponseTypeDef = TypedDict(
    "RegenerateSecurityTokenResponseTypeDef", {"Bot": "BotTypeDef"}, total=False
)

ResetPersonalPINResponseTypeDef = TypedDict(
    "ResetPersonalPINResponseTypeDef", {"User": "UserTypeDef"}, total=False
)

RestorePhoneNumberResponseTypeDef = TypedDict(
    "RestorePhoneNumberResponseTypeDef", {"PhoneNumber": "PhoneNumberTypeDef"}, total=False
)

SearchAvailablePhoneNumbersResponseTypeDef = TypedDict(
    "SearchAvailablePhoneNumbersResponseTypeDef", {"E164PhoneNumbers": List[str]}, total=False
)

UpdateAccountResponseTypeDef = TypedDict(
    "UpdateAccountResponseTypeDef", {"Account": "AccountTypeDef"}, total=False
)

UpdateBotResponseTypeDef = TypedDict("UpdateBotResponseTypeDef", {"Bot": "BotTypeDef"}, total=False)

_RequiredUpdatePhoneNumberRequestItemTypeDef = TypedDict(
    "_RequiredUpdatePhoneNumberRequestItemTypeDef", {"PhoneNumberId": str}
)
_OptionalUpdatePhoneNumberRequestItemTypeDef = TypedDict(
    "_OptionalUpdatePhoneNumberRequestItemTypeDef",
    {"ProductType": Literal["BusinessCalling", "VoiceConnector"], "CallingName": str},
    total=False,
)


class UpdatePhoneNumberRequestItemTypeDef(
    _RequiredUpdatePhoneNumberRequestItemTypeDef, _OptionalUpdatePhoneNumberRequestItemTypeDef
):
    pass


UpdatePhoneNumberResponseTypeDef = TypedDict(
    "UpdatePhoneNumberResponseTypeDef", {"PhoneNumber": "PhoneNumberTypeDef"}, total=False
)

UpdateProxySessionResponseTypeDef = TypedDict(
    "UpdateProxySessionResponseTypeDef", {"ProxySession": "ProxySessionTypeDef"}, total=False
)

UpdateRoomMembershipResponseTypeDef = TypedDict(
    "UpdateRoomMembershipResponseTypeDef", {"RoomMembership": "RoomMembershipTypeDef"}, total=False
)

UpdateRoomResponseTypeDef = TypedDict(
    "UpdateRoomResponseTypeDef", {"Room": "RoomTypeDef"}, total=False
)

_RequiredUpdateUserRequestItemTypeDef = TypedDict(
    "_RequiredUpdateUserRequestItemTypeDef", {"UserId": str}
)
_OptionalUpdateUserRequestItemTypeDef = TypedDict(
    "_OptionalUpdateUserRequestItemTypeDef",
    {
        "LicenseType": Literal["Basic", "Plus", "Pro", "ProTrial"],
        "UserType": Literal["PrivateUser", "SharedDevice"],
        "AlexaForBusinessMetadata": "AlexaForBusinessMetadataTypeDef",
    },
    total=False,
)


class UpdateUserRequestItemTypeDef(
    _RequiredUpdateUserRequestItemTypeDef, _OptionalUpdateUserRequestItemTypeDef
):
    pass


UpdateUserResponseTypeDef = TypedDict(
    "UpdateUserResponseTypeDef", {"User": "UserTypeDef"}, total=False
)

UpdateVoiceConnectorGroupResponseTypeDef = TypedDict(
    "UpdateVoiceConnectorGroupResponseTypeDef",
    {"VoiceConnectorGroup": "VoiceConnectorGroupTypeDef"},
    total=False,
)

UpdateVoiceConnectorResponseTypeDef = TypedDict(
    "UpdateVoiceConnectorResponseTypeDef", {"VoiceConnector": "VoiceConnectorTypeDef"}, total=False
)
