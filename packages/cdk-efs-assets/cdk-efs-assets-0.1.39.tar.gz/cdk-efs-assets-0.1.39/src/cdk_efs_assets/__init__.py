"""
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
"""
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from ._jsii import *

import aws_cdk.aws_ec2
import aws_cdk.aws_efs
import aws_cdk.core


@jsii.data_type(
    jsii_type="cdk-efs-assets.GithubSourceFeederProps",
    jsii_struct_bases=[],
    name_mapping={
        "efs_access_point": "efsAccessPoint",
        "repository": "repository",
        "vpc": "vpc",
        "runs_after": "runsAfter",
    },
)
class GithubSourceFeederProps:
    def __init__(
        self,
        *,
        efs_access_point: aws_cdk.aws_efs.AccessPoint,
        repository: builtins.str,
        vpc: aws_cdk.aws_ec2.IVpc,
        runs_after: typing.Optional[typing.List[aws_cdk.core.IDependable]] = None,
    ) -> None:
        """
        :param efs_access_point: The target Amazon EFS filesystem to clone the github repository to.
        :param repository: The github repository HTTP URI.
        :param vpc: The VPC of the Amazon EFS Filesystem.
        :param runs_after: The dependent resources before triggering the sync.
        """
        self._values: typing.Dict[str, typing.Any] = {
            "efs_access_point": efs_access_point,
            "repository": repository,
            "vpc": vpc,
        }
        if runs_after is not None:
            self._values["runs_after"] = runs_after

    @builtins.property
    def efs_access_point(self) -> aws_cdk.aws_efs.AccessPoint:
        """The target Amazon EFS filesystem to clone the github repository to."""
        result = self._values.get("efs_access_point")
        assert result is not None, "Required property 'efs_access_point' is missing"
        return result

    @builtins.property
    def repository(self) -> builtins.str:
        """The github repository HTTP URI."""
        result = self._values.get("repository")
        assert result is not None, "Required property 'repository' is missing"
        return result

    @builtins.property
    def vpc(self) -> aws_cdk.aws_ec2.IVpc:
        """The VPC of the Amazon EFS Filesystem."""
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return result

    @builtins.property
    def runs_after(self) -> typing.Optional[typing.List[aws_cdk.core.IDependable]]:
        """The dependent resources before triggering the sync."""
        result = self._values.get("runs_after")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GithubSourceFeederProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GithubSourceSync(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-efs-assets.GithubSourceSync",
):
    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        efs_access_point: aws_cdk.aws_efs.AccessPoint,
        repository: builtins.str,
        vpc: aws_cdk.aws_ec2.IVpc,
        runs_after: typing.Optional[typing.List[aws_cdk.core.IDependable]] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param efs_access_point: The target Amazon EFS filesystem to clone the github repository to.
        :param repository: The github repository HTTP URI.
        :param vpc: The VPC of the Amazon EFS Filesystem.
        :param runs_after: The dependent resources before triggering the sync.
        """
        props = GithubSourceFeederProps(
            efs_access_point=efs_access_point,
            repository=repository,
            vpc=vpc,
            runs_after=runs_after,
        )

        jsii.create(GithubSourceSync, self, [scope, id, props])


__all__ = [
    "GithubSourceFeederProps",
    "GithubSourceSync",
]

publication.publish()
