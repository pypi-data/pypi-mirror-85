"""Base types of x5-aios3-ext library."""
from .s3_meta_types import S3ObjectsInBulkDelete, UploadDetailsInCompleteMultipart
from .s3_responses import (
    AbortMultipartUploadResponse,
    CompleteMultipartUploadResponse,
    CreateBucketResponse,
    CreateMultipartUploadResponse,
    DeleteObjectResponse,
    DeleteObjectsResponse,
    GetObjectResponse,
    ListObjectsVersion2Response,
    PutObjectResponse,
    S3SimpleResponse,
    UploadPartResponse,
)
