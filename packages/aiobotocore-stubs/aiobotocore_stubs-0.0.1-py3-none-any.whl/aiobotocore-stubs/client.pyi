from datetime import datetime
from typing import IO, Dict, Literal, Optional, Union, Any

from aiobotocore_types import s3_meta_types, s3_responses


def __getattr__(name) -> Any: ...


class AioBaseClient(...):

    async def create_bucket(
        self,
        Bucket: str,
        ACL: Optional[s3_meta_types.BucketACL] = None,
        CreateBucketConfiguration: Optional[s3_meta_types.CreateBucketConf] = None,
        GrantFullControl: Optional[str] = None,
        GrantRead: Optional[str] = None,
        GrantReadACP: Optional[str] = None,
        GrantWrite: Optional[str] = None,
        GrantWriteACP: Optional[str] = None,
        ObjectLockEnabledForBucket: Optional[bool] = None,
    ) -> s3_responses.CreateBucketResponse:
        """Create new S3 bucket.

        To create a bucket, you must register with Amazon S3 and have a valid AWS Access Key ID to authenticate
        requests. Anonymous requests are never allowed to create buckets. By creating the bucket, you become the bucket
        owner.

        :param Bucket: name of bucket being deleted.
        :param ACL: canned ACL to apply to the bucket.
        :param CreateBucketConfiguration: configuration information for the bucket.
            `LocationConstraint` specifies the Region where the bucket will be created.
            If you don't specify a Region, the bucket is created in
            the US East (N. Virginia) Region (us-east-1).
        :param GrantFullControl: allows grantee the read, write, read ACP, and write ACP permissions on the bucket.
        :param GrantRead: allows grantee to list the objects in the bucket.
        :param GrantReadACP: allows grantee to read the bucket ACL.
        :param GrantWrite: allows grantee to create, overwrite, and delete any object in the bucket.
        :param GrantWriteACP: allows grantee to write the ACL for the applicable bucket.
        :param ObjectLockEnabledForBucket: specifies whether you want S3 Object Lock to be enabled for the new bucket.

        :return: CreateBucketResponse dictionary
        """

    async def delete_bucket(
        self,
        Bucket: str,
        ExpectedBucketOwner: Optional[str] = None,
    ) -> s3_responses.S3SimpleResponse:
        """Delete the S3 bucket.

        All objects (including all object versions and delete markers)
        in the bucket must be deleted before the bucket itself can be deleted.

        :param Bucket: name of bucket being deleted.
        :param ExpectedBucketOwner: account id of the expected bucket owner. If the bucket is owned
            by a different account, the request will fail with an HTTP 403 (Access Denied) error.

        :return: dictionary as: {'ResponseMetadata': { '...': '...', }
        """

    async def put_object(
        self,
        Bucket: str,
        Key: str,
        Body: Union[bytes, IO, None] = None,
        ACL: Optional[s3_meta_types.ObjectACL] = None,
        CacheControl: Optional[str] = None,
        ContentDisposition: Optional[str] = None,
        ContentEncoding: Optional[str] = None,
        ContentLanguage: Optional[str] = None,
        ContentLength: Optional[int] = None,
        ContentMD5: Optional[str] = None,
        ContentType: Optional[str] = None,
        Expires: Optional[datetime] = None,
        GrantFullControl: Optional[str] = None,
        GrantRead: Optional[str] = None,
        GrantReadACP: Optional[str] = None,
        GrantWriteACP: Optional[str] = None,
        Metadata: Optional[Dict[str, str]] = None,
        ServerSideEncryption: Optional[s3_meta_types.ServerSideEncryption] = None,
        StorageClass: Optional[s3_meta_types.StorageClass] = None,
        WebsiteRedirectLocation: Optional[str] = None,
        SSECustomerAlgorithm: Optional[str] = None,
        SSECustomerKey: Optional[str] = None,
        SSEKMSKeyId: Optional[str] = None,
        SSECustomerKeyMD5: Optional[str] = None,
        SSEKMSEncryptionContext: Optional[str] = None,
        RequestPayer: Optional[str] = None,
        Tagging: Optional[str] = None,
        ObjectLockMode: Optional[s3_meta_types.ObjectLockMode] = None,
        ObjectLockRetainUntilDate: Optional[datetime] = None,
        ObjectLockLegalHoldStatus: Optional[Literal['ON', 'OFF']] = None,
        ExpectedBucketOwner: Optional[str] = None,
    ) -> s3_responses.PutObjectResponse:
        """Add object to bucket.

        You must have WRITE permissions on a bucket to add an object to it.

        :param Bucket: bucket name to which the PUT operation was initiated.
        :param Key: object key for which the PUT operation was initiated.

        :param Body: bytes or seekable file-like object, object data.
        :param ACL: canned ACL to apply to the object.
        :param CacheControl: Can be used to specify caching behavior along the request/reply chain.
        :param ContentDisposition: Specifies presentational information for the object.
        :param ContentEncoding: Specifies what content encodings have been applied to the object and thus what decoding
            mechanisms must be applied to obtain the media-type referenced by the Content-Type header field.
        :param ContentLanguage: language the content is in.
        :param ContentLength: Size of the body in bytes, useful when the size of the body cannot
            be determined automatically.
        :param ContentMD5: base64-encoded 128-bit MD5 digest of the message (without the headers) according to RFC 1864.
            This header can be used as a message integrity check to verify that the data is the same data that was
            originally sent.
        :param ContentType: standard MIME type describing the format of the contents.
        :param Expires: datetime at which the object is no longer cacheable.

        This args not supported by Amazon S3 on Outposts:
            `GrantFullControl`, `GrantRead`, `GrantReadACP`, `GrantWriteACP`

        :param GrantFullControl: Gives the grantee READ, READ_ACP, and WRITE_ACP permissions on the object.
        :param GrantRead: Allows grantee to read the object data and its metadata.
        :param GrantReadACP: Allows grantee to read the object ACL.
        :param GrantWriteACP: Allows grantee to write the ACL for the applicable object.

        :param Metadata: map of metadata to store with the object in S3.
        :param ServerSideEncryption: The server-side encryption algorithm used when storing this object in Amazon S3.
        :param StorageClass: By default, Amazon S3 uses the STANDARD Storage Class to store newly created objects.
            The STANDARD storage class provides high durability and high availability. Depending on performance needs,
            you can specify a different Storage Class. Amazon S3 on Outposts only uses the OUTPOSTS Storage Class.
        :param WebsiteRedirectLocation: If the bucket is configured as a website, redirects requests for this object
            to another object in the same bucket or to an external URL.

        :param SSECustomerAlgorithm: Specifies the algorithm to use to when encrypting the object.
        :param SSECustomerKey: Specifies the customer-provided encryption key for Amazon S3 to use in encrypting data.
            This value is used to store the object and then it is discarded; Amazon S3 does not store the encryption
            key. The key must be appropriate for use with the algorithm specified in `SSECustomerAlgorithm`.
        :param SSECustomerKeyMD5: Specifies the 128-bit MD5 digest of the encryption key according to RFC 1321. Amazon
            S3 uses this header for a message integrity check to ensure that the encryption key was transmitted without
            error. This parameter is automatically populated if it is not provided.
        :param SSEKMSKeyId: If x-amz-server-side-encryption is present and has the value of "aws:kms",
            this header specifies the ID of the AWS Key Management Service (AWS KMS) symmetrical customer managed
            customer master key (CMK) that was used for the object.
        :param SSEKMSEncryptionContext: Specifies the AWS KMS Encryption Context to use for object encryption.
            The value of this header is a base64-encoded UTF-8 string holding JSON with the encryption context
            key-value pairs.

        :param RequestPayer: Confirms that the requester knows that they will be charged for the request. Bucket owners
            need not specify this parameter in their requests.
        :param Tagging: The tag-set for the object. The tag-set must be encoded as URL Query parameters.
            (For example, "Key1=Value1")
        :param ObjectLockMode: The Object Lock mode that you want to apply to this object.
        :param ObjectLockRetainUntilDate: The date and time when you want this object's Object Lock to expire.
        :param ObjectLockLegalHoldStatus: Specifies whether a legal hold will be applied to this object.
        :param ExpectedBucketOwner: The account id of the expected bucket owner. If the bucket is owned by a different
            account, the request will fail with an HTTP 403 (Access Denied) error.

        :return: PutObjectResponse dictionary
        """

    async def get_object(
        self,
        Bucket: str,
        Key: str,
        IfMatch: Optional[str] = None,
        IfModifiedSince: Optional[datetime] = None,
        IfNoneMatch: Optional[str] = None,
        IfUnmodifiedSince: Optional[datetime] = None,
        Range: Optional[str] = None,
        ResponseCacheControl: Optional[str] = None,
        ResponseContentDisposition: Optional[str] = None,
        ResponseContentEncoding: Optional[str] = None,
        ResponseContentLanguage: Optional[str] = None,
        ResponseContentType: Optional[str] = None,
        ResponseExpires: Optional[datetime] = None,
        VersionId: Optional[str] = None,
        SSECustomerAlgorithm: Optional[str] = None,
        SSECustomerKey: Optional[str] = None,
        RequestPayer: Optional[str] = None,
        PartNumber: Optional[int] = None,
        ExpectedBucketOwner: Optional[str] = None,
    ) -> s3_responses.GetObjectResponse:
        """Retrieve object from S3.

        To use it, you must have READ access to the object. If you grant READ access to
        the anonymous user, you can return the object without using an authorization header.

        :param Bucket: bucket name containing the object.
        :param Key: key of the object to get.

        :param IfMatch: return the object only if its entity tag (ETag) is the same
            as the one specified, otherwise return a 412 (precondition failed).
        :param IfModifiedSince: return the object only if it has been modified since
            the specified time, otherwise return a 304 (not modified).
        :param IfNoneMatch: return the object only if its entity tag (ETag) is different
            from the one specified, otherwise return a 304 (not modified).
        :param IfUnmodifiedSince: return the object only if it has not been modified since
            the specified time, otherwise return a 412 (precondition failed).
        :param Range: Downloads the specified range bytes of an object. For more information
            about the HTTP Range header, see https://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html#sec14.35
            Note: Amazon S3 doesn't support retrieving multiple ranges of data per GET request.
        :param ResponseCacheControl: sets the Cache-Control header of the response.
        :param ResponseContentDisposition: sets the Content-Disposition header of the response
        :param ResponseContentEncoding: sets the Content-Encoding header of the response.
        :param ResponseContentLanguage: sets the Content-Language header of the response.
        :param ResponseContentType: sets the Content-Type header of the response.
        :param ResponseExpires: sets the Expires header of the response.
        :param VersionId: versionId used to reference a specific version of the object.
        :param SSECustomerAlgorithm: specifies the algorithm to use to when encrypting the object (for example, AES256).
        :param SSECustomerKey: specifies the customer-provided encryption key for Amazon S3 to use in encrypting data.
            This value is used to store the object and then it is discarded; Amazon S3 does not store
            the encryption key. The key must be appropriate for use with the algorithm specified in
            the x-amz-server-side-encryption-customer-algorithm header.
        :param RequestPayer: confirms that the requester knows that they will be charged for the request.
            Bucket owners need not specify this parameter in their requests.
        :param PartNumber: part number of the object being read. This is a positive integer between 1 and 10,000.
            Effectively performs a 'ranged' GET request for the part specified. Useful for downloading just
            a part of an object.
        :param ExpectedBucketOwner: account id of the expected bucket owner. If the bucket is owned by
            a different account, the request will fail with an HTTP 403 (Access Denied) error.

        :return: GetObjectResponse dictionary
        """

    async def delete_object(
        self,
        Bucket: str,
        Key: str,
        MFA: Optional[str] = None,
        VersionId: Optional[str] = None,
        RequestPayer: Optional[str] = None,
        BypassGovernanceRetention: Optional[bool] = None,
        ExpectedBucketOwner: Optional[str] = None,
    ) -> s3_responses.DeleteObjectResponse:
        """Delete S3-object.

        Removes the null version (if there is one) of an object and inserts a delete marker,
        which becomes the latest version of the object. If there isn't a null version, Amazon S3
        does not remove any objects.

        :param Bucket: bucket name containing the object.
        :param Key: key of the object to delete.

        :param MFA: concatenation of the authentication device's serial number, a space, and the value that
            is displayed on your authentication device. Required to permanently delete a versioned object
            if versioning is configured with MFA delete enabled.
        :param VersionId: versionId used to reference a specific version of the object.
        :param RequestPayer: confirms that the requester knows that they will be charged for the request.
            Bucket owners need not specify this parameter in their requests.
        :param BypassGovernanceRetention: indicates whether S3 Object Lock should bypass Governance-mode restrictions
            to process this operation.
        :param ExpectedBucketOwner: account id of the expected bucket owner. If the bucket is owned by
            a different account, the request will fail with an HTTP 403 (Access Denied) error.

        :return: DeleteObjectResponse dictionary
        """

    async def delete_objects(
        self,
        Bucket: str,
        Delete: s3_meta_types.S3ObjectsInBulkDelete,
        MFA: Optional[str] = None,
        RequestPayer: Optional[str] = None,
        BypassGovernanceRetention: Optional[bool] = None,
        ExpectedBucketOwner: Optional[str] = None,
    ) -> s3_responses.DeleteObjectsResponse:
        """Delete multiple objects from a bucket using a single HTTP request.

        If you know the object keys that you want to delete, then this operation provides a suitable alternative
        to sending individual delete requests, reducing per-request overhead.

        The request contains a list of up to 1000 keys that you want to delete. In the XML, you provide the object
        key names, and optionally, version IDs if you want to delete a specific version of the object from a
        versioning-enabled bucket. For each key, Amazon S3 performs a delete operation and returns the result
        of that delete, success, or failure, in the response.

        NOTE: if the object specified in the request is not found, Amazon S3 returns the result as deleted.

        :param Bucket: bucket name containing the objects to delete.
        :param Delete: container for the request, e.g.: {'Objects': [{'Key': 'HappyFace.jpg'}], 'Quiet': False} .

        :param MFA: concatenation of the authentication device's serial number, a space, and the value that
            is displayed on your authentication device. Required to permanently delete a versioned object
            if versioning is configured with MFA delete enabled.
        :param RequestPayer: confirms that the requester knows that they will be charged for the request.
            Bucket owners need not specify this parameter in their requests.
        :param BypassGovernanceRetention: indicates whether S3 Object Lock should bypass Governance-mode restrictions
            to process this operation.
        :param ExpectedBucketOwner: account id of the expected bucket owner. If the bucket is owned by
            a different account, the request will fail with an HTTP 403 (Access Denied) error.

        :return: DeleteObjectsResponse dictionary
        """

    async def list_objects_v2(
        self,
        Bucket: str,
        Delimiter: Optional[str] = None,
        EncodingType: Optional[str] = None,
        MaxKeys: Optional[int] = None,
        Prefix: Optional[str] = None,
        ContinuationToken: Optional[str] = None,
        FetchOwner: Optional[bool] = None,
        StartAfter: Optional[str] = None,
        RequestPayer: Optional[str] = None,
        ExpectedBucketOwner: Optional[str] = None,
    ) -> s3_responses.ListObjectsVersion2Response:
        """Return some or all (up to 1,000) of the objects in a bucket.

        You can use the request parameters as selection criteria to return a subset of the objects in a bucket.
        A 200 OK response can contain valid or invalid XML. Make sure to design your application to parse the contents
        of the response and handle it appropriately.

        :param Bucket: name of the bucket containing the objects
        :param Delimiter: A delimiter is a character you use to group keys.
        :param EncodingType: Encoding type used by Amazon S3 to encode object keys in the response.
        :param MaxKeys: Sets the maximum number of keys returned in the response. By default the API returns up to
            1,000 key names. The response might contain fewer keys but will never contain more.
        :param Prefix: Limits the response to keys that begin with the specified prefix.
        :param ContinuationToken: ContinuationToken indicates Amazon S3 that the list is being continued on this bucket
            with a token. ContinuationToken is obfuscated and is not a real key.
        :param FetchOwner: The owner field is not present in listV2 by default, if you want to return owner field with
            each key in the result then set the fetch owner field to true.
        :param StartAfter: StartAfter is where you want Amazon S3 to start listing from. Amazon S3 starts listing after
            this specified key. StartAfter can be any key in the bucket.
        :param RequestPayer: Confirms that the requester knows that she or he will be charged for the list objects
            request in V2 style. Bucket owners need not specify this parameter in their requests.
        :param ExpectedBucketOwner: The account id of the expected bucket owner. If the bucket is owned by a different
            account, the request will fail with an HTTP 403 (Access Denied) error.

        :return: ListObjectsVersion2Response dictionary
        """

    async def create_multipart_upload(
        self,
        Bucket: str,
        Key: str,
        ACL: Optional[s3_meta_types.ObjectACL] = None,
        CacheControl: Optional[str] = None,
        ContentDisposition: Optional[str] = None,
        ContentEncoding: Optional[str] = None,
        ContentLanguage: Optional[str] = None,
        ContentType: Optional[str] = None,
        Expires: Optional[datetime] = None,
        GrantFullControl: Optional[str] = None,
        GrantRead: Optional[str] = None,
        GrantReadACP: Optional[str] = None,
        GrantWriteACP: Optional[str] = None,
        Metadata: Optional[Dict[str, str]] = None,
        ServerSideEncryption: Optional[s3_meta_types.ServerSideEncryption] = None,
        StorageClass: Optional[s3_meta_types.StorageClass] = None,
        WebsiteRedirectLocation: Optional[str] = None,
        SSECustomerAlgorithm: Optional[str] = None,
        SSECustomerKey: Optional[str] = None,
        SSECustomerKeyMD5: Optional[str] = None,
        SSEKMSKeyId: Optional[str] = None,
        SSEKMSEncryptionContext: Optional[str] = None,
        RequestPayer: Optional[str] = None,
        Tagging: Optional[str] = None,
        ObjectLockMode: Optional[s3_meta_types.ObjectLockMode] = None,
        ObjectLockRetainUntilDate: Optional[datetime] = None,
        ObjectLockLegalHoldStatus: Optional[Literal['ON', 'OFF']] = None,
        ExpectedBucketOwner: Optional[str] = None,
    ) -> s3_responses.CreateMultipartUploadResponse:
        """Initiate a multipart upload and returns an upload ID.

        This upload ID is used to associate all of the parts in the specific multipart upload. You specify this upload
        ID in each of your subsequent upload part requests. You also include this upload ID in the final request to
        either complete or abort the multipart upload request.

        :param Bucket: bucket name to which to initiate the upload.
        :param Key: object key for which the multipart upload is to be initiated.

        :param ACL: canned ACL to apply to the object.
        :param CacheControl: Can be used to specify caching behavior along the request/reply chain.
        :param ContentDisposition: Specifies presentational information for the object.
        :param ContentEncoding: Specifies what content encodings have been applied to the object and thus what decoding
            mechanisms must be applied to obtain the media-type referenced by the Content-Type header field.
        :param ContentLanguage: language the content is in.
        :param ContentType: standard MIME type describing the format of the contents.
        :param Expires: datetime at which the object is no longer cacheable.

        This args not supported by Amazon S3 on Outposts:
            `GrantFullControl`, `GrantRead`, `GrantReadACP`, `GrantWriteACP`

        :param GrantFullControl: Gives the grantee READ, READ_ACP, and WRITE_ACP permissions on the object.
        :param GrantRead: Allows grantee to read the object data and its metadata.
        :param GrantReadACP: Allows grantee to read the object ACL.
        :param GrantWriteACP: Allows grantee to write the ACL for the applicable object.

        :param Metadata: map of metadata to store with the object in S3.
        :param ServerSideEncryption: The server-side encryption algorithm used when storing this object in Amazon S3.
        :param StorageClass: By default, Amazon S3 uses the STANDARD Storage Class to store newly created objects.
            The STANDARD storage class provides high durability and high availability. Depending on performance needs,
            you can specify a different Storage Class. Amazon S3 on Outposts only uses the OUTPOSTS Storage Class.
        :param WebsiteRedirectLocation: If the bucket is configured as a website, redirects requests for this object
            to another object in the same bucket or to an external URL. Amazon S3 stores the value of this header in
            the object metadata.

        :param SSECustomerAlgorithm: Specifies the algorithm to use to when encrypting the object.
        :param SSECustomerKey: Specifies the customer-provided encryption key for Amazon S3 to use in encrypting data.
            This value is used to store the object and then it is discarded; Amazon S3 does not store the encryption
            key.
        :param SSECustomerKeyMD5: Specifies the 128-bit MD5 digest of the encryption key according to RFC 1321. Amazon
            S3 uses this header for a message integrity check to ensure that the encryption key was transmitted without
            error. This parameter is automatically populated if it is not provided.
        :param SSEKMSKeyId: Specifies the ID of the symmetric customer managed AWS KMS CMK to use for object encryption.
            All GET and PUT requests for an object protected by AWS KMS will fail if not made via SSL or using SigV4.
        :param SSEKMSEncryptionContext: Specifies the AWS KMS Encryption Context to use for object encryption.
            The value of this header is a base64-encoded UTF-8 string holding JSON with the encryption context
            key-value pairs.

        :param RequestPayer: Confirms that the requester knows that they will be charged for the request. Bucket owners
            need not specify this parameter in their requests.
        :param Tagging: tag-set for the object. The tag-set must be encoded as URL Query parameters, e.g. "Key1=Value1".
        :param ObjectLockMode: The Object Lock mode that you want to apply to this object.
        :param ObjectLockRetainUntilDate: The date and time when you want this object's Object Lock to expire.
        :param ObjectLockLegalHoldStatus: Specifies whether a legal hold will be applied to this object.
        :param ExpectedBucketOwner: The account id of the expected bucket owner. If the bucket is owned by a different
            account, the request will fail with an HTTP 403 (Access Denied) error.

        :return: CreateMultipartUploadResponse dictionary
        """

    async def upload_part(
        self,
        Bucket: str,
        Key: str,
        PartNumber: int,
        UploadId: str,
        Body: Optional[Union[bytes, IO]] = None,
        ContentLength: Optional[int] = None,
        ContentMD5: Optional[str] = None,
        SSECustomerAlgorithm: Optional[str] = None,
        SSECustomerKey: Optional[str] = None,
        SSECustomerKeyMD5: Optional[str] = None,
        RequestPayer: Optional[str] = None,
        ExpectedBucketOwner: Optional[str] = None,
    ) -> s3_responses.UploadPartResponse:
        """Upload a part in a multipart upload.

        You must initiate a multipart upload before you can upload any part. In response to your initiate request,
        Amazon S3 returns an upload ID, a unique identifier, that you must include in your upload part request.

        :param Bucket: bucket name to which the multipart upload was initiated.
        :param Key: object key for which the multipart upload was initiated.
        :param PartNumber: Part number of part being uploaded. This is a positive integer between 1 and 10,000.
        :param UploadId: Upload ID identifying the multipart upload whose part is being uploaded.

        :param Body: bytes or seekable file-like object, object data.
        :param ContentLength: Size of the body in bytes, useful when the size of the body cannot
            be determined automatically.
        :param ContentMD5: base64-encoded 128-bit MD5 digest of the part data. This parameter is auto-populated when
            using the command from the CLI. This parameter is required if object lock parameters are specified.

        :param SSECustomerAlgorithm: Specifies the algorithm to use to when encrypting the object.
        :param SSECustomerKey: Specifies the customer-provided encryption key for Amazon S3 to use in encrypting data.
            This value is used to store the object and then it is discarded; Amazon S3 does not store the encryption
            key. The key must be appropriate for use with the algorithm specified in `SSECustomerAlgorithm`.
        :param SSECustomerKeyMD5: Specifies the 128-bit MD5 digest of the encryption key according to RFC 1321. Amazon
            S3 uses this header for a message integrity check to ensure that the encryption key was transmitted without
            error. This parameter is automatically populated if it is not provided.

        :param RequestPayer: Confirms that the requester knows that they will be charged for the request. Bucket owners
            need not specify this parameter in their requests.
        :param ExpectedBucketOwner: The account id of the expected bucket owner. If the bucket is owned by a different
            account, the request will fail with an HTTP 403 (Access Denied) error.

        :return: UploadPartResponse dictionary
        """

    async def complete_multipart_upload(
        self,
        Bucket: str,
        Key: str,
        UploadId: str,
        MultipartUpload: Optional[s3_meta_types.UploadDetailsInCompleteMultipart] = None,
        RequestPayer: Optional[str] = None,
        ExpectedBucketOwner: Optional[str] = None,
    ) -> s3_responses.CompleteMultipartUploadResponse:
        """Complete a multipart upload by assembling previously uploaded parts.

        You first initiate the multipart upload and then upload all parts using the UploadPart operation. After
        successfully uploading all relevant parts of an upload, you call this operation to complete the upload.

        :param Bucket: bucket name to which the multipart upload was initiated.
        :param Key: object key for which the multipart upload was initiated.
        :param UploadId: Upload ID identifying the multipart upload whose part is being uploaded.

        :param MultipartUpload: container for the details of the parts that were uploaded.

        :param RequestPayer: Confirms that the requester knows that they will be charged for the request. Bucket owners
            need not specify this parameter in their requests.
        :param ExpectedBucketOwner: The account id of the expected bucket owner. If the bucket is owned by a different
            account, the request will fail with an HTTP 403 (Access Denied) error.

        :return: CompleteMultipartUploadResponse dictionary
        """

    async def abort_multipart_upload(
        self,
        Bucket: str,
        Key: str,
        UploadId: str,
        RequestPayer: Optional[str] = None,
        ExpectedBucketOwner: Optional[str] = None,
    ) -> s3_responses.AbortMultipartUploadResponse:
        """Abort a multipart upload.

        After a multipart upload is aborted, no additional parts can be uploaded using that upload ID. The storage
        consumed by any previously uploaded parts will be freed. However, if any part uploads are currently in progress,
        those part uploads might or might not succeed. As a result, it might be necessary to abort a given multipart
        upload multiple times in order to completely free all storage consumed by all parts.

        :param Bucket: bucket name to which the multipart upload was initiated.
        :param Key: object key for which the multipart upload was initiated.
        :param UploadId: Upload ID identifying the multipart upload.

        :param RequestPayer: Confirms that the requester knows that they will be charged for the request. Bucket owners
            need not specify this parameter in their requests.
        :param ExpectedBucketOwner: The account id of the expected bucket owner. If the bucket is owned by a different
            account, the request will fail with an HTTP 403 (Access Denied) error.

        :return: AbortMultipartUploadResponse dictionary
        """
