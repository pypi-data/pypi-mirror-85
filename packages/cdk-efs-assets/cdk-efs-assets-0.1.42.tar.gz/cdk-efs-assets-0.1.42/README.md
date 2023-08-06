# cdk-efs-assets

CDK construct library to populate Amazon EFS assets from Github or S3.

# `GithubSourceSync`

The `GithubSourceSync` deploys your Amazon EFS assets from specified Github repository.

## Sample

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from cdk_efs_assets import GithubSourceSync

app = App()

env = {
    "region": process.env.CDK_DEFAULT_REGION ?? AWS_DEFAULT_REGION,
    "account": process.env.CDK_DEFAULT_ACCOUNT
}

stack = Stack(app, "testing-stack", env=env)

vpc = ec2.Vpc.from_lookup(stack, "Vpc", is_default=True)

fs = efs.FileSystem(stack, "Filesystem",
    vpc=vpc,
    removal_policy=RemovalPolicy.DESTROY
)

efs_access_point = fs.add_access_point("EfsAccessPoint",
    path="/demo",
    create_acl={
        "owner_gid": "1001",
        "owner_uid": "1001",
        "permissions": "0755"
    },
    posix_user={
        "uid": "1001",
        "gid": "1001"
    }
)

# create the one-time sync from Github repository to Amaozn EFS
GithubSourceSync(stack, "GithubSourceSync",
    repository="https://github.com/pahud/cdk-efs-assets.git",
    efs_access_point=efs_access_point,
    runs_after=[fs.mount_targets_available],
    vpc=vpc
)
```

# `S3SourceSync`

TBD
