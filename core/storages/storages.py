from storages.backends.s3boto3 import S3ManifestStaticStorage, S3StaticStorage


class StaticStorage(S3ManifestStaticStorage):
    location = 'static'
    default_acl = 'public-read'


class PublicMediaStorage(S3StaticStorage):
    location = 'uploads'
    default_acl = 'public-read'
    file_overwrite = False
