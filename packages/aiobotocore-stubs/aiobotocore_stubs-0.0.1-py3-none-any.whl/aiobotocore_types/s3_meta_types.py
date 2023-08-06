"""Simple types used in requests and responses."""
from datetime import datetime
from typing import Dict, List, Literal, TypedDict, Union

CreateBucketConf = Dict[Literal['LocationConstraint'], Literal[
    'af-south-1', 'ap-east-1', 'ap-northeast-1', 'ap-northeast-2',
    'ap-northeast-3', 'ap-south-1', 'ap-southeast-1', 'ap-southeast-2',
    'ca-central-1', 'cn-north-1', 'cn-northwest-1', 'EU', 'eu-central-1',
    'eu-north-1', 'eu-south-1', 'eu-west-1', 'eu-west-2', 'eu-west-3',
    'me-south-1', 'sa-east-1', 'us-east-2', 'us-gov-east-1',
    'us-gov-west-1', 'us-west-1', 'us-west-2',
]]

StandardACL = Literal['private', 'public-read', 'public-read-write', 'authenticated-read']
BucketACL = StandardACL
ObjectACL = Literal[StandardACL, 'aws-exec-read', 'bucket-owner-read', 'bucket-owner-full-control']

StorageClass = Literal[
    'STANDARD',
    'REDUCED_REDUNDANCY',
    'STANDARD_IA',
    'ONEZONE_IA',
    'INTELLIGENT_TIERING',
    'GLACIER',
    'DEEP_ARCHIVE',
    'OUTPOSTS',
]
ServerSideEncryption = Literal['AES256', 'aws:kms']
ObjectLockMode = Literal['GOVERNANCE', 'COMPLIANCE']
ReplicationStatus = Literal['COMPLETE', 'PENDING', 'FAILED', 'REPLICA']

PartInCompleteMultipart = Dict[Literal['ETag', 'PartNumber'], Union[str, int]]
UploadDetailsInCompleteMultipart = Dict[Literal['Parts'], List[PartInCompleteMultipart]]

ObjectInDelete = Literal['Key', 'VersionId']
DeleteObjectsErrorKeys = Literal[ObjectInDelete, 'Code', 'Message']
DeleteObjectInBulkDeleteResponse = Dict[
    Literal[ObjectInDelete, 'DeleteMarker', 'DeleteMarkerVersionId'], Union[str, bool],
]
ObjectInBulkDelete = List[Dict[ObjectInDelete, str]]
S3ObjectsInBulkDelete = Dict[Literal['Objects', 'Quiet'], Union[ObjectInBulkDelete, bool]]


class S3ObjectInList(TypedDict):
    Key: str
    LastModified: datetime
    ETag: str
    Size: int
    StorageClass: StorageClass
    Owner: Dict[Literal['DisplayName', 'ID'], str]


class S3SimpleResponse(TypedDict):
    ResponseMetadata: Dict[str, Union[dict, str]]
