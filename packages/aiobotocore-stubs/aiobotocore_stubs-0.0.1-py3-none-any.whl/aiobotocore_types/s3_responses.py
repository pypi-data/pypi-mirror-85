"""Type annotations for S3 responses.

Copied and adapted Python from:
 https://botocore.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html .
"""
from datetime import datetime
from typing import Dict, List, Literal

from aiobotocore.response import StreamingBody

from . import s3_meta_types
from .s3_meta_types import S3SimpleResponse


class CreateBucketResponse(S3SimpleResponse):
    Location: str


class GetObjectResponse(S3SimpleResponse):
    Body: StreamingBody
    DeleteMarker: bool
    AcceptRanges: str
    Expiration: str
    Restore: str
    LastModified: datetime
    ContentLength: int
    ETag: str
    MissingMeta: int
    VersionId: str
    CacheControl: str
    ContentDisposition: str
    ContentEncoding: str
    ContentLanguage: str
    ContentRange: str
    ContentType: str
    Expires: datetime
    WebsiteRedirectLocation: str
    ServerSideEncryption: s3_meta_types.ServerSideEncryption
    Metadata: Dict[str, str]
    SSECustomerAlgorithm: str
    SSECustomerKeyMD5: str
    SSEKMSKeyId: str
    StorageClass: s3_meta_types.StorageClass
    RequestCharged: str
    ReplicationStatus: s3_meta_types.ReplicationStatus
    PartsCount: int
    TagCount: int
    ObjectLockMode: s3_meta_types.ObjectLockMode
    ObjectLockRetainUntilDate: datetime
    ObjectLockLegalHoldStatus: Literal['ON', 'OFF']


class PutObjectResponse(S3SimpleResponse):
    Expiration: str
    ETag: str
    ServerSideEncryption: s3_meta_types.ServerSideEncryption
    VersionId: str
    SSECustomerAlgorithm: str
    SSECustomerKeyMD5: str
    SSEKMSKeyId: str
    SSEKMSEncryptionContext: str
    RequestCharged: str


class ListObjectsVersion2Response(S3SimpleResponse):
    IsTruncated: bool
    Contents: List[s3_meta_types.S3ObjectInList]
    Name: str
    Prefix: str
    Delimiter: str
    MaxKeys: int
    CommonPrefixes: Dict[Literal['Prefix'], str]
    EncodingType: str
    KeyCount: int
    ContinuationToken: str
    NextContinuationToken: str
    StartAfter: str


class DeleteObjectResponse(S3SimpleResponse):
    VersionId: str
    DeleteMarker: bool
    RequestCharged: str


class DeleteObjectsResponse(S3SimpleResponse):
    Deleted: List[s3_meta_types.DeleteObjectInBulkDeleteResponse]
    RequestCharged: str
    Errors: List[Dict[s3_meta_types.DeleteObjectsErrorKeys, str]]


class CreateMultipartUploadResponse(S3SimpleResponse):
    AbortDate: datetime
    AbortRuleId: str
    Bucket: str
    Key: str
    UploadId: str
    ServerSideEncryption: s3_meta_types.ServerSideEncryption
    SSECustomerAlgorithm: str
    SSECustomerKeyMD5: str
    SSEKMSKeyId: str
    SSEKMSEncryptionContext: str
    RequestCharged: str


class UploadPartResponse(S3SimpleResponse):
    ServerSideEncryption: s3_meta_types.ServerSideEncryption
    ETag: str
    SSECustomerAlgorithm: str
    SSECustomerKeyMD5: str
    SSEKMSKeyId: str
    RequestCharged: str


class CompleteMultipartUploadResponse(S3SimpleResponse):
    Location: str
    Bucket: str
    Key: str
    Expiration: str
    ETag: str
    ServerSideEncryption: s3_meta_types.ServerSideEncryption
    VersionId: str
    SSEKMSKeyId: str
    RequestCharged: str


class AbortMultipartUploadResponse(S3SimpleResponse):
    RequestCharged: str
