"""
## AWS CodeBuild Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

![cdk-constructs: Stable](https://img.shields.io/badge/cdk--constructs-stable-success.svg?style=for-the-badge)

---
<!--END STABILITY BANNER-->

AWS CodeBuild is a fully managed continuous integration service that compiles
source code, runs tests, and produces software packages that are ready to
deploy. With CodeBuild, you don’t need to provision, manage, and scale your own
build servers. CodeBuild scales continuously and processes multiple builds
concurrently, so your builds are not left waiting in a queue. You can get
started quickly by using prepackaged build environments, or you can create
custom build environments that use your own build tools. With CodeBuild, you are
charged by the minute for the compute resources you use.

## Installation

Install the module:

```console
$ npm i @aws-cdk/aws-codebuild
```

Import it into your code:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_codebuild as codebuild
```

The `codebuild.Project` construct represents a build project resource. See the
reference documentation for a comprehensive list of initialization properties,
methods and attributes.

## Source

Build projects are usually associated with a *source*, which is specified via
the `source` property which accepts a class that extends the `Source`
abstract base class.
The default is to have no source associated with the build project;
the `buildSpec` option is required in that case.

Here's a CodeBuild project with no source which simply prints `Hello, CodeBuild!`:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
codebuild.Project(self, "MyProject",
    build_spec=codebuild.BuildSpec.from_object({
        "version": "0.2",
        "phases": {
            "build": {
                "commands": ["echo \"Hello, CodeBuild!\""
                ]
            }
        }
    })
)
```

### `CodeCommitSource`

Use an AWS CodeCommit repository as the source of this build:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_codebuild as codebuild
import aws_cdk.aws_codecommit as codecommit

repository = codecommit.Repository(self, "MyRepo", repository_name="foo")
codebuild.Project(self, "MyFirstCodeCommitProject",
    source=codebuild.Source.code_commit(repository=repository)
)
```

### `S3Source`

Create a CodeBuild project with an S3 bucket as the source:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_codebuild as codebuild
import aws_cdk.aws_s3 as s3

bucket = s3.Bucket(self, "MyBucket")
codebuild.Project(self, "MyProject",
    source=codebuild.Source.s3(
        bucket=bucket,
        path="path/to/file.zip"
    )
)
```

### `GitHubSource` and `GitHubEnterpriseSource`

These source types can be used to build code from a GitHub repository.
Example:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
git_hub_source = codebuild.Source.git_hub(
    owner="awslabs",
    repo="aws-cdk",
    webhook=True, # optional, default: true if `webhookFilters` were provided, false otherwise
    webhook_filters=[
        codebuild.FilterGroup.in_event_of(codebuild.EventAction.PUSH).and_branch_is("master")
    ]
)
```

To provide GitHub credentials, please either go to AWS CodeBuild Console to connect
or call `ImportSourceCredentials` to persist your personal access token.
Example:

```
aws codebuild import-source-credentials --server-type GITHUB --auth-type PERSONAL_ACCESS_TOKEN --token <token_value>
```

### `BitBucketSource`

This source type can be used to build code from a BitBucket repository.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
bb_source = codebuild.Source.bit_bucket(
    owner="owner",
    repo="repo"
)
```

## Artifacts

CodeBuild Projects can produce Artifacts and upload them to S3. For example:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
project = codebuild.Project(stack, "MyProject",
    build_spec=codebuild.BuildSpec.from_object(
        version="0.2"
    ),
    artifacts=codebuild.Artifacts.s3(
        bucket=bucket,
        include_build_id=False,
        package_zip=True,
        path="another/path",
        identifier="AddArtifact1"
    )
)
```

Because we've not set the `name` property, this example will set the
`overrideArtifactName` parameter, and produce an artifact named as defined in
the Buildspec file, uploaded to an S3 bucket (`bucket`). The path will be
`another/path` and the artifact will be a zipfile.

## CodePipeline

To add a CodeBuild Project as an Action to CodePipeline,
use the `PipelineProject` class instead of `Project`.
It's a simple class that doesn't allow you to specify `sources`,
`secondarySources`, `artifacts` or `secondaryArtifacts`,
as these are handled by setting input and output CodePipeline `Artifact` instances on the Action,
instead of setting them on the Project.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
project = codebuild.PipelineProject(self, "Project")
```

For more details, see the readme of the `@aws-cdk/@aws-codepipeline-actions` package.

## Caching

You can save time when your project builds by using a cache. A cache can store reusable pieces of your build environment and use them across multiple builds. Your build project can use one of two types of caching: Amazon S3 or local. In general, S3 caching is a good option for small and intermediate build artifacts that are more expensive to build than to download. Local caching is a good option for large intermediate build artifacts because the cache is immediately available on the build host.

### S3 Caching

With S3 caching, the cache is stored in an S3 bucket which is available from multiple hosts.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
codebuild.Project(self, "Project",
    source=codebuild.Source.bit_bucket(
        owner="awslabs",
        repo="aws-cdk"
    ),
    cache=codebuild.Cache.bucket(Bucket(self, "Bucket"))
)
```

### Local Caching

With local caching, the cache is stored on the codebuild instance itself. This is simple,
cheap and fast, but CodeBuild cannot guarantee a reuse of instance and hence cannot
guarantee cache hits. For example, when a build starts and caches files locally, if two subsequent builds start at the same time afterwards only one of those builds would get the cache. Three different cache modes are supported, which can be turned on individually.

* `LocalCacheMode.SOURCE` caches Git metadata for primary and secondary sources.
* `LocalCacheMode.DOCKER_LAYER` caches existing Docker layers.
* `LocalCacheMode.CUSTOM` caches directories you specify in the buildspec file.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
codebuild.Project(self, "Project",
    source=codebuild.Source.git_hub_enterprise(
        https_clone_url="https://my-github-enterprise.com/owner/repo"
    ),

    # Enable Docker AND custom caching
    cache=codebuild.Cache.local(LocalCacheMode.DOCKER_LAYER, LocalCacheMode.CUSTOM)
)
```

## Environment

By default, projects use a small instance with an Ubuntu 18.04 image. You
can use the `environment` property to customize the build environment:

* `buildImage` defines the Docker image used. See [Images](#images) below for
  details on how to define build images.
* `computeType` defines the instance type used for the build.
* `privileged` can be set to `true` to allow privileged access.
* `environmentVariables` can be set at this level (and also at the project
  level).

## Images

The CodeBuild library supports both Linux and Windows images via the
`LinuxBuildImage` and `WindowsBuildImage` classes, respectively.

You can specify one of the predefined Windows/Linux images by using one
of the constants such as `WindowsBuildImage.WINDOWS_BASE_2_0` or
`LinuxBuildImage.STANDARD_2_0`.

Alternatively, you can specify a custom image using one of the static methods on
`XxxBuildImage`:

* Use `.fromDockerRegistry(image[, { secretsManagerCredentials }])` to reference an image in any public or private Docker registry.
* Use `.fromEcrRepository(repo[, tag])` to reference an image available in an
  ECR repository.
* Use `.fromAsset(directory)` to use an image created from a
  local asset.
* Use `.fromCodeBuildImageId(id)` to reference a pre-defined, CodeBuild-provided Docker image.

The following example shows how to define an image from a Docker asset:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
environment=BuildEnvironment(
    build_image=codebuild.LinuxBuildImage.from_asset(self, "MyImage",
        directory=path.join(__dirname, "demo-image")
    )
)
```

The following example shows how to define an image from an ECR repository:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
environment=BuildEnvironment(
    build_image=codebuild.LinuxBuildImage.from_ecr_repository(ecr_repository, "v1.0")
)
```

The following example shows how to define an image from a private docker registry:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
environment=BuildEnvironment(
    build_image=codebuild.LinuxBuildImage.from_docker_registry("my-registry/my-repo",
        secrets_manager_credentials=secrets
    )
)
```

## Credentials

CodeBuild allows you to store credentials used when communicating with various sources,
like GitHub:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
codebuild.GitHubSourceCredentials(self, "CodeBuildGitHubCreds",
    access_token=cdk.SecretValue.secrets_manager("my-token")
)
```

and BitBucket:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
codebuild.BitBucketSourceCredentials(self, "CodeBuildBitBucketCreds",
    username=cdk.SecretValue.secrets_manager("my-bitbucket-creds", json_field="username"),
    password=cdk.SecretValue.secrets_manager("my-bitbucket-creds", json_field="password")
)
```

**Note**: the credentials are global to a given account in a given region -
they are not defined per CodeBuild project.
CodeBuild only allows storing a single credential of a given type
(GitHub, GitHub Enterprise or BitBucket)
in a given account in a given region -
any attempt to save more than one will result in an error.
You can use the [`list-source-credentials` AWS CLI operation](https://docs.aws.amazon.com/cli/latest/reference/codebuild/list-source-credentials.html)
to inspect what credentials are stored in your account.

## Test reports

You can specify a test report in your buildspec:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
project = codebuild.Project(self, "Project",
    build_spec=codebuild.BuildSpec.from_object(
        # ...
        reports={
            "my_report": {
                "files": "**/*",
                "base-directory": "build/test-results"
            }
        }
    )
)
```

This will create a new test report group,
with the name `<ProjectName>-myReport`.

The project's role in the CDK will always be granted permissions to create and use report groups
with names starting with the project's name;
if you'd rather not have those permissions added,
you can opt out of it when creating the project:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
project = codebuild.Project(self, "Project",
    # ...
    grant_report_group_permissions=False
)
```

Alternatively, you can specify an ARN of an existing resource group,
instead of a simple name, in your buildspec:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
# create a new ReportGroup
report_group = codebuild.ReportGroup(self, "ReportGroup")

project = codebuild.Project(self, "Project",
    build_spec=codebuild.BuildSpec.from_object(
        # ...
        reports={
            "[reportGroup.reportGroupArn]": {
                "files": "**/*",
                "base-directory": "build/test-results"
            }
        }
    )
)
```

If you do that, you need to grant the project's role permissions to write reports to that report group:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
report_group.grant_write(project)
```

For more information on the test reports feature,
see the [AWS CodeBuild documentation](https://docs.aws.amazon.com/codebuild/latest/userguide/test-reporting.html).

## Events

CodeBuild projects can be used either as a source for events or be triggered
by events via an event rule.

### Using Project as an event target

The `@aws-cdk/aws-events-targets.CodeBuildProject` allows using an AWS CodeBuild
project as a AWS CloudWatch event rule target:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
# start build when a commit is pushed
import aws_cdk.aws_events_targets as targets

code_commit_repository.on_commit("OnCommit",
    target=targets.CodeBuildProject(project)
)
```

### Using Project as an event source

To define Amazon CloudWatch event rules for build projects, use one of the `onXxx`
methods:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
rule = project.on_state_change("BuildStateChange",
    target=targets.LambdaFunction(fn)
)
```

## Secondary sources and artifacts

CodeBuild Projects can get their sources from multiple places, and produce
multiple outputs. For example:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
project = codebuild.Project(self, "MyProject",
    secondary_sources=[
        codebuild.Source.code_commit(
            identifier="source2",
            repository=repo
        )
    ],
    secondary_artifacts=[
        codebuild.Artifacts.s3(
            identifier="artifact2",
            bucket=bucket,
            path="some/path",
            name="file.zip"
        )
    ]
)
```

Note that the `identifier` property is required for both secondary sources and
artifacts.

The contents of the secondary source is available to the build under the
directory specified by the `CODEBUILD_SRC_DIR_<identifier>` environment variable
(so, `CODEBUILD_SRC_DIR_source2` in the above case).

The secondary artifacts have their own section in the buildspec, under the
regular `artifacts` one. Each secondary artifact has its own section, beginning
with their identifier.

So, a buildspec for the above Project could look something like this:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
project = codebuild.Project(self, "MyProject",
    # secondary sources and artifacts as above...
    build_spec=codebuild.BuildSpec.from_object(
        version="0.2",
        phases={
            "build": {
                "commands": ["cd $CODEBUILD_SRC_DIR_source2", "touch output2.txt"
                ]
            }
        },
        artifacts={
            "secondary-artifacts": {
                "artifact2": {
                    "base-directory": "$CODEBUILD_SRC_DIR_source2",
                    "files": ["output2.txt"
                    ]
                }
            }
        }
    )
)
```

### Definition of VPC configuration in CodeBuild Project

Typically, resources in an VPC are not accessible by AWS CodeBuild. To enable
access, you must provide additional VPC-specific configuration information as
part of your CodeBuild project configuration. This includes the VPC ID, the
VPC subnet IDs, and the VPC security group IDs. VPC-enabled builds are then
able to access resources inside your VPC.

For further Information see https://docs.aws.amazon.com/codebuild/latest/userguide/vpc-support.html

**Use Cases**
VPC connectivity from AWS CodeBuild builds makes it possible to:

* Run integration tests from your build against data in an Amazon RDS database that's isolated on a private subnet.
* Query data in an Amazon ElastiCache cluster directly from tests.
* Interact with internal web services hosted on Amazon EC2, Amazon ECS, or services that use internal Elastic Load Balancing.
* Retrieve dependencies from self-hosted, internal artifact repositories, such as PyPI for Python, Maven for Java, and npm for Node.js.
* Access objects in an Amazon S3 bucket configured to allow access through an Amazon VPC endpoint only.
* Query external web services that require fixed IP addresses through the Elastic IP address of the NAT gateway or NAT instance associated with your subnet(s).

Your builds can access any resource that's hosted in your VPC.

**Enable Amazon VPC Access in your CodeBuild Projects**

Pass the VPC when defining your Project, then make sure to
give the CodeBuild's security group the right permissions
to access the resources that it needs by using the
`connections` object.

For example:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
vpc = ec2.Vpc(self, "MyVPC")
project = codebuild.Project(self, "MyProject",
    vpc=vpc,
    build_spec=codebuild.BuildSpec.from_object()
)

project.connections.allow_to(load_balancer, ec2.Port.tcp(443))
```

## Project File System Location EFS

Add support for CodeBuild to build on AWS EFS file system mounts using
the new ProjectFileSystemLocation.
The `fileSystemLocations` property which accepts a list `ProjectFileSystemLocation`
as represented by the interface `IFileSystemLocations`.
The only supported file system type is `EFS`.

For example:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
codebuild.Project(stack, "MyProject",
    build_spec=codebuild.BuildSpec.from_object(
        version="0.2"
    ),
    file_system_locations=[
        codebuild.FileSystemLocation.efs(
            identifier="myidentifier2",
            location="myclodation.mydnsroot.com:/loc",
            mount_point="/media",
            mount_options="opts"
        )
    ]
)
```

Here's a CodeBuild project with a simple example that creates a project mounted on AWS EFS:

[Minimal Example](./test/integ.project-file-system-location.ts)
"""
import abc
import builtins
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from ._jsii import *

import aws_cdk.aws_cloudwatch
import aws_cdk.aws_codecommit
import aws_cdk.aws_ec2
import aws_cdk.aws_ecr
import aws_cdk.aws_ecr_assets
import aws_cdk.aws_events
import aws_cdk.aws_iam
import aws_cdk.aws_kms
import aws_cdk.aws_s3
import aws_cdk.aws_secretsmanager
import aws_cdk.core


@jsii.data_type(
    jsii_type="@aws-cdk/aws-codebuild.ArtifactsConfig",
    jsii_struct_bases=[],
    name_mapping={"artifacts_property": "artifactsProperty"},
)
class ArtifactsConfig:
    def __init__(self, *, artifacts_property: "CfnProject.ArtifactsProperty") -> None:
        """The type returned from {@link IArtifacts#bind}.

        :param artifacts_property: The low-level CloudFormation artifacts property.
        """
        if isinstance(artifacts_property, dict):
            artifacts_property = CfnProject.ArtifactsProperty(**artifacts_property)
        self._values = {
            "artifacts_property": artifacts_property,
        }

    @builtins.property
    def artifacts_property(self) -> "CfnProject.ArtifactsProperty":
        """The low-level CloudFormation artifacts property."""
        return self._values.get("artifacts_property")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ArtifactsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-codebuild.ArtifactsProps",
    jsii_struct_bases=[],
    name_mapping={"identifier": "identifier"},
)
class ArtifactsProps:
    def __init__(self, *, identifier: typing.Optional[str] = None) -> None:
        """Properties common to all Artifacts classes.

        :param identifier: The artifact identifier. This property is required on secondary artifacts.
        """
        self._values = {}
        if identifier is not None:
            self._values["identifier"] = identifier

    @builtins.property
    def identifier(self) -> typing.Optional[str]:
        """The artifact identifier.

        This property is required on secondary artifacts.
        """
        return self._values.get("identifier")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ArtifactsProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-codebuild.BindToCodePipelineOptions",
    jsii_struct_bases=[],
    name_mapping={"artifact_bucket": "artifactBucket"},
)
class BindToCodePipelineOptions:
    def __init__(self, *, artifact_bucket: aws_cdk.aws_s3.IBucket) -> None:
        """The extra options passed to the {@link IProject.bindToCodePipeline} method.

        :param artifact_bucket: The artifact bucket that will be used by the action that invokes this project.
        """
        self._values = {
            "artifact_bucket": artifact_bucket,
        }

    @builtins.property
    def artifact_bucket(self) -> aws_cdk.aws_s3.IBucket:
        """The artifact bucket that will be used by the action that invokes this project."""
        return self._values.get("artifact_bucket")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BindToCodePipelineOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BitBucketSourceCredentials(
    aws_cdk.core.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-codebuild.BitBucketSourceCredentials",
):
    """The source credentials used when contacting the BitBucket API.

    **Note**: CodeBuild only allows a single credential for BitBucket
    to be saved in a given AWS account in a given region -
    any attempt to add more than one will result in an error.

    resource:
    :resource:: AWS::CodeBuild::SourceCredential
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: str,
        *,
        password: aws_cdk.core.SecretValue,
        username: aws_cdk.core.SecretValue,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param password: Your BitBucket application password.
        :param username: Your BitBucket username.
        """
        props = BitBucketSourceCredentialsProps(password=password, username=username)

        jsii.create(BitBucketSourceCredentials, self, [scope, id, props])


@jsii.data_type(
    jsii_type="@aws-cdk/aws-codebuild.BitBucketSourceCredentialsProps",
    jsii_struct_bases=[],
    name_mapping={"password": "password", "username": "username"},
)
class BitBucketSourceCredentialsProps:
    def __init__(
        self, *, password: aws_cdk.core.SecretValue, username: aws_cdk.core.SecretValue
    ) -> None:
        """Construction properties of {@link BitBucketSourceCredentials}.

        :param password: Your BitBucket application password.
        :param username: Your BitBucket username.
        """
        self._values = {
            "password": password,
            "username": username,
        }

    @builtins.property
    def password(self) -> aws_cdk.core.SecretValue:
        """Your BitBucket application password."""
        return self._values.get("password")

    @builtins.property
    def username(self) -> aws_cdk.core.SecretValue:
        """Your BitBucket username."""
        return self._values.get("username")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BitBucketSourceCredentialsProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-codebuild.BucketCacheOptions",
    jsii_struct_bases=[],
    name_mapping={"prefix": "prefix"},
)
class BucketCacheOptions:
    def __init__(self, *, prefix: typing.Optional[str] = None) -> None:
        """
        :param prefix: The prefix to use to store the cache in the bucket.
        """
        self._values = {}
        if prefix is not None:
            self._values["prefix"] = prefix

    @builtins.property
    def prefix(self) -> typing.Optional[str]:
        """The prefix to use to store the cache in the bucket."""
        return self._values.get("prefix")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BucketCacheOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-codebuild.BuildEnvironment",
    jsii_struct_bases=[],
    name_mapping={
        "build_image": "buildImage",
        "compute_type": "computeType",
        "environment_variables": "environmentVariables",
        "privileged": "privileged",
    },
)
class BuildEnvironment:
    def __init__(
        self,
        *,
        build_image: typing.Optional["IBuildImage"] = None,
        compute_type: typing.Optional["ComputeType"] = None,
        environment_variables: typing.Optional[
            typing.Mapping[str, "BuildEnvironmentVariable"]
        ] = None,
        privileged: typing.Optional[bool] = None,
    ) -> None:
        """
        :param build_image: The image used for the builds. Default: LinuxBuildImage.STANDARD_1_0
        :param compute_type: The type of compute to use for this build. See the {@link ComputeType} enum for the possible values. Default: taken from {@link #buildImage#defaultComputeType}
        :param environment_variables: The environment variables that your builds can use.
        :param privileged: Indicates how the project builds Docker images. Specify true to enable running the Docker daemon inside a Docker container. This value must be set to true only if this build project will be used to build Docker images, and the specified build environment image is not one provided by AWS CodeBuild with Docker support. Otherwise, all associated builds that attempt to interact with the Docker daemon will fail. Default: false
        """
        self._values = {}
        if build_image is not None:
            self._values["build_image"] = build_image
        if compute_type is not None:
            self._values["compute_type"] = compute_type
        if environment_variables is not None:
            self._values["environment_variables"] = environment_variables
        if privileged is not None:
            self._values["privileged"] = privileged

    @builtins.property
    def build_image(self) -> typing.Optional["IBuildImage"]:
        """The image used for the builds.

        default
        :default: LinuxBuildImage.STANDARD_1_0
        """
        return self._values.get("build_image")

    @builtins.property
    def compute_type(self) -> typing.Optional["ComputeType"]:
        """The type of compute to use for this build.

        See the {@link ComputeType} enum for the possible values.

        default
        :default: taken from {@link #buildImage#defaultComputeType}
        """
        return self._values.get("compute_type")

    @builtins.property
    def environment_variables(
        self,
    ) -> typing.Optional[typing.Mapping[str, "BuildEnvironmentVariable"]]:
        """The environment variables that your builds can use."""
        return self._values.get("environment_variables")

    @builtins.property
    def privileged(self) -> typing.Optional[bool]:
        """Indicates how the project builds Docker images.

        Specify true to enable
        running the Docker daemon inside a Docker container. This value must be
        set to true only if this build project will be used to build Docker
        images, and the specified build environment image is not one provided by
        AWS CodeBuild with Docker support. Otherwise, all associated builds that
        attempt to interact with the Docker daemon will fail.

        default
        :default: false
        """
        return self._values.get("privileged")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BuildEnvironment(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-codebuild.BuildEnvironmentVariable",
    jsii_struct_bases=[],
    name_mapping={"value": "value", "type": "type"},
)
class BuildEnvironmentVariable:
    def __init__(
        self,
        *,
        value: typing.Any,
        type: typing.Optional["BuildEnvironmentVariableType"] = None,
    ) -> None:
        """
        :param value: The value of the environment variable (or the name of the parameter in the SSM parameter store.).
        :param type: The type of environment variable. Default: PlainText
        """
        self._values = {
            "value": value,
        }
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def value(self) -> typing.Any:
        """The value of the environment variable (or the name of the parameter in the SSM parameter store.)."""
        return self._values.get("value")

    @builtins.property
    def type(self) -> typing.Optional["BuildEnvironmentVariableType"]:
        """The type of environment variable.

        default
        :default: PlainText
        """
        return self._values.get("type")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BuildEnvironmentVariable(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-codebuild.BuildEnvironmentVariableType")
class BuildEnvironmentVariableType(enum.Enum):
    PLAINTEXT = "PLAINTEXT"
    """An environment variable in plaintext format."""
    PARAMETER_STORE = "PARAMETER_STORE"
    """An environment variable stored in Systems Manager Parameter Store."""
    SECRETS_MANAGER = "SECRETS_MANAGER"
    """An environment variable stored in AWS Secrets Manager."""


class BuildSpec(
    metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-codebuild.BuildSpec"
):
    """BuildSpec for CodeBuild projects."""

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _BuildSpecProxy

    def __init__(self) -> None:
        jsii.create(BuildSpec, self, [])

    @jsii.member(jsii_name="fromObject")
    @builtins.classmethod
    def from_object(cls, value: typing.Mapping[str, typing.Any]) -> "BuildSpec":
        """
        :param value: -
        """
        return jsii.sinvoke(cls, "fromObject", [value])

    @jsii.member(jsii_name="fromSourceFilename")
    @builtins.classmethod
    def from_source_filename(cls, filename: str) -> "BuildSpec":
        """Use a file from the source as buildspec.

        Use this if you want to use a file different from 'buildspec.yml'`

        :param filename: -
        """
        return jsii.sinvoke(cls, "fromSourceFilename", [filename])

    @jsii.member(jsii_name="toBuildSpec")
    @abc.abstractmethod
    def to_build_spec(self) -> str:
        """Render the represented BuildSpec."""
        ...

    @builtins.property
    @jsii.member(jsii_name="isImmediate")
    @abc.abstractmethod
    def is_immediate(self) -> bool:
        """Whether the buildspec is directly available or deferred until build-time."""
        ...


class _BuildSpecProxy(BuildSpec):
    @jsii.member(jsii_name="toBuildSpec")
    def to_build_spec(self) -> str:
        """Render the represented BuildSpec."""
        return jsii.invoke(self, "toBuildSpec", [])

    @builtins.property
    @jsii.member(jsii_name="isImmediate")
    def is_immediate(self) -> bool:
        """Whether the buildspec is directly available or deferred until build-time."""
        return jsii.get(self, "isImmediate")


class Cache(metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-codebuild.Cache"):
    """Cache options for CodeBuild Project.

    A cache can store reusable pieces of your build environment and use them across multiple builds.

    see
    :see: https://docs.aws.amazon.com/codebuild/latest/userguide/build-caching.html
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _CacheProxy

    def __init__(self) -> None:
        jsii.create(Cache, self, [])

    @jsii.member(jsii_name="bucket")
    @builtins.classmethod
    def bucket(
        cls, bucket: aws_cdk.aws_s3.IBucket, *, prefix: typing.Optional[str] = None
    ) -> "Cache":
        """Create an S3 caching strategy.

        :param bucket: the S3 bucket to use for caching.
        :param prefix: The prefix to use to store the cache in the bucket.
        """
        options = BucketCacheOptions(prefix=prefix)

        return jsii.sinvoke(cls, "bucket", [bucket, options])

    @jsii.member(jsii_name="local")
    @builtins.classmethod
    def local(cls, *modes: "LocalCacheMode") -> "Cache":
        """Create a local caching strategy.

        :param modes: the mode(s) to enable for local caching.
        """
        return jsii.sinvoke(cls, "local", [*modes])

    @jsii.member(jsii_name="none")
    @builtins.classmethod
    def none(cls) -> "Cache":
        return jsii.sinvoke(cls, "none", [])


class _CacheProxy(Cache):
    pass


@jsii.implements(aws_cdk.core.IInspectable)
class CfnProject(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-codebuild.CfnProject",
):
    """A CloudFormation ``AWS::CodeBuild::Project``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html
    cloudformationResource:
    :cloudformationResource:: AWS::CodeBuild::Project
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: str,
        *,
        artifacts: typing.Union["ArtifactsProperty", aws_cdk.core.IResolvable],
        environment: typing.Union[aws_cdk.core.IResolvable, "EnvironmentProperty"],
        service_role: str,
        source: typing.Union["SourceProperty", aws_cdk.core.IResolvable],
        badge_enabled: typing.Optional[
            typing.Union[bool, aws_cdk.core.IResolvable]
        ] = None,
        cache: typing.Optional[
            typing.Union[aws_cdk.core.IResolvable, "ProjectCacheProperty"]
        ] = None,
        description: typing.Optional[str] = None,
        encryption_key: typing.Optional[str] = None,
        file_system_locations: typing.Optional[
            typing.Union[
                aws_cdk.core.IResolvable,
                typing.List[
                    typing.Union[
                        "ProjectFileSystemLocationProperty", aws_cdk.core.IResolvable
                    ]
                ],
            ]
        ] = None,
        logs_config: typing.Optional[
            typing.Union[aws_cdk.core.IResolvable, "LogsConfigProperty"]
        ] = None,
        name: typing.Optional[str] = None,
        queued_timeout_in_minutes: typing.Optional[jsii.Number] = None,
        secondary_artifacts: typing.Optional[
            typing.Union[
                aws_cdk.core.IResolvable,
                typing.List[
                    typing.Union["ArtifactsProperty", aws_cdk.core.IResolvable]
                ],
            ]
        ] = None,
        secondary_sources: typing.Optional[
            typing.Union[
                aws_cdk.core.IResolvable,
                typing.List[typing.Union["SourceProperty", aws_cdk.core.IResolvable]],
            ]
        ] = None,
        secondary_source_versions: typing.Optional[
            typing.Union[
                aws_cdk.core.IResolvable,
                typing.List[
                    typing.Union[
                        aws_cdk.core.IResolvable, "ProjectSourceVersionProperty"
                    ]
                ],
            ]
        ] = None,
        source_version: typing.Optional[str] = None,
        tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]] = None,
        timeout_in_minutes: typing.Optional[jsii.Number] = None,
        triggers: typing.Optional[
            typing.Union[aws_cdk.core.IResolvable, "ProjectTriggersProperty"]
        ] = None,
        vpc_config: typing.Optional[
            typing.Union[aws_cdk.core.IResolvable, "VpcConfigProperty"]
        ] = None,
    ) -> None:
        """Create a new ``AWS::CodeBuild::Project``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param artifacts: ``AWS::CodeBuild::Project.Artifacts``.
        :param environment: ``AWS::CodeBuild::Project.Environment``.
        :param service_role: ``AWS::CodeBuild::Project.ServiceRole``.
        :param source: ``AWS::CodeBuild::Project.Source``.
        :param badge_enabled: ``AWS::CodeBuild::Project.BadgeEnabled``.
        :param cache: ``AWS::CodeBuild::Project.Cache``.
        :param description: ``AWS::CodeBuild::Project.Description``.
        :param encryption_key: ``AWS::CodeBuild::Project.EncryptionKey``.
        :param file_system_locations: ``AWS::CodeBuild::Project.FileSystemLocations``.
        :param logs_config: ``AWS::CodeBuild::Project.LogsConfig``.
        :param name: ``AWS::CodeBuild::Project.Name``.
        :param queued_timeout_in_minutes: ``AWS::CodeBuild::Project.QueuedTimeoutInMinutes``.
        :param secondary_artifacts: ``AWS::CodeBuild::Project.SecondaryArtifacts``.
        :param secondary_sources: ``AWS::CodeBuild::Project.SecondarySources``.
        :param secondary_source_versions: ``AWS::CodeBuild::Project.SecondarySourceVersions``.
        :param source_version: ``AWS::CodeBuild::Project.SourceVersion``.
        :param tags: ``AWS::CodeBuild::Project.Tags``.
        :param timeout_in_minutes: ``AWS::CodeBuild::Project.TimeoutInMinutes``.
        :param triggers: ``AWS::CodeBuild::Project.Triggers``.
        :param vpc_config: ``AWS::CodeBuild::Project.VpcConfig``.
        """
        props = CfnProjectProps(
            artifacts=artifacts,
            environment=environment,
            service_role=service_role,
            source=source,
            badge_enabled=badge_enabled,
            cache=cache,
            description=description,
            encryption_key=encryption_key,
            file_system_locations=file_system_locations,
            logs_config=logs_config,
            name=name,
            queued_timeout_in_minutes=queued_timeout_in_minutes,
            secondary_artifacts=secondary_artifacts,
            secondary_sources=secondary_sources,
            secondary_source_versions=secondary_source_versions,
            source_version=source_version,
            tags=tags,
            timeout_in_minutes=timeout_in_minutes,
            triggers=triggers,
            vpc_config=vpc_config,
        )

        jsii.create(CfnProject, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(
        cls,
        scope: aws_cdk.core.Construct,
        id: str,
        resource_attributes: typing.Any,
        *,
        finder: aws_cdk.core.ICfnFinder,
    ) -> "CfnProject":
        """A factory method that creates a new instance of this class from an object containing the CloudFormation properties of this resource.

        Used in the @aws-cdk/cloudformation-include module.

        :param scope: -
        :param id: -
        :param resource_attributes: -
        :param finder: The finder interface used to resolve references across the template.

        stability
        :stability: experimental
        """
        options = aws_cdk.core.FromCloudFormationOptions(finder=finder)

        return jsii.sinvoke(
            cls, "fromCloudFormation", [scope, id, resource_attributes, options]
        )

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        """Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self, props: typing.Mapping[str, typing.Any]
    ) -> typing.Mapping[str, typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: Arn
        """
        return jsii.get(self, "attrArn")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        """``AWS::CodeBuild::Project.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-tags
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="artifacts")
    def artifacts(self) -> typing.Union["ArtifactsProperty", aws_cdk.core.IResolvable]:
        """``AWS::CodeBuild::Project.Artifacts``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-artifacts
        """
        return jsii.get(self, "artifacts")

    @artifacts.setter
    def artifacts(
        self, value: typing.Union["ArtifactsProperty", aws_cdk.core.IResolvable]
    ) -> None:
        jsii.set(self, "artifacts", value)

    @builtins.property
    @jsii.member(jsii_name="environment")
    def environment(
        self,
    ) -> typing.Union[aws_cdk.core.IResolvable, "EnvironmentProperty"]:
        """``AWS::CodeBuild::Project.Environment``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-environment
        """
        return jsii.get(self, "environment")

    @environment.setter
    def environment(
        self, value: typing.Union[aws_cdk.core.IResolvable, "EnvironmentProperty"]
    ) -> None:
        jsii.set(self, "environment", value)

    @builtins.property
    @jsii.member(jsii_name="serviceRole")
    def service_role(self) -> str:
        """``AWS::CodeBuild::Project.ServiceRole``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-servicerole
        """
        return jsii.get(self, "serviceRole")

    @service_role.setter
    def service_role(self, value: str) -> None:
        jsii.set(self, "serviceRole", value)

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> typing.Union["SourceProperty", aws_cdk.core.IResolvable]:
        """``AWS::CodeBuild::Project.Source``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-source
        """
        return jsii.get(self, "source")

    @source.setter
    def source(
        self, value: typing.Union["SourceProperty", aws_cdk.core.IResolvable]
    ) -> None:
        jsii.set(self, "source", value)

    @builtins.property
    @jsii.member(jsii_name="badgeEnabled")
    def badge_enabled(
        self,
    ) -> typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]]:
        """``AWS::CodeBuild::Project.BadgeEnabled``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-badgeenabled
        """
        return jsii.get(self, "badgeEnabled")

    @badge_enabled.setter
    def badge_enabled(
        self, value: typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]]
    ) -> None:
        jsii.set(self, "badgeEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="cache")
    def cache(
        self,
    ) -> typing.Optional[
        typing.Union[aws_cdk.core.IResolvable, "ProjectCacheProperty"]
    ]:
        """``AWS::CodeBuild::Project.Cache``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-cache
        """
        return jsii.get(self, "cache")

    @cache.setter
    def cache(
        self,
        value: typing.Optional[
            typing.Union[aws_cdk.core.IResolvable, "ProjectCacheProperty"]
        ],
    ) -> None:
        jsii.set(self, "cache", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[str]:
        """``AWS::CodeBuild::Project.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-description
        """
        return jsii.get(self, "description")

    @description.setter
    def description(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="encryptionKey")
    def encryption_key(self) -> typing.Optional[str]:
        """``AWS::CodeBuild::Project.EncryptionKey``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-encryptionkey
        """
        return jsii.get(self, "encryptionKey")

    @encryption_key.setter
    def encryption_key(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "encryptionKey", value)

    @builtins.property
    @jsii.member(jsii_name="fileSystemLocations")
    def file_system_locations(
        self,
    ) -> typing.Optional[
        typing.Union[
            aws_cdk.core.IResolvable,
            typing.List[
                typing.Union[
                    "ProjectFileSystemLocationProperty", aws_cdk.core.IResolvable
                ]
            ],
        ]
    ]:
        """``AWS::CodeBuild::Project.FileSystemLocations``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-filesystemlocations
        """
        return jsii.get(self, "fileSystemLocations")

    @file_system_locations.setter
    def file_system_locations(
        self,
        value: typing.Optional[
            typing.Union[
                aws_cdk.core.IResolvable,
                typing.List[
                    typing.Union[
                        "ProjectFileSystemLocationProperty", aws_cdk.core.IResolvable
                    ]
                ],
            ]
        ],
    ) -> None:
        jsii.set(self, "fileSystemLocations", value)

    @builtins.property
    @jsii.member(jsii_name="logsConfig")
    def logs_config(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "LogsConfigProperty"]]:
        """``AWS::CodeBuild::Project.LogsConfig``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-logsconfig
        """
        return jsii.get(self, "logsConfig")

    @logs_config.setter
    def logs_config(
        self,
        value: typing.Optional[
            typing.Union[aws_cdk.core.IResolvable, "LogsConfigProperty"]
        ],
    ) -> None:
        jsii.set(self, "logsConfig", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[str]:
        """``AWS::CodeBuild::Project.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-name
        """
        return jsii.get(self, "name")

    @name.setter
    def name(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="queuedTimeoutInMinutes")
    def queued_timeout_in_minutes(self) -> typing.Optional[jsii.Number]:
        """``AWS::CodeBuild::Project.QueuedTimeoutInMinutes``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-queuedtimeoutinminutes
        """
        return jsii.get(self, "queuedTimeoutInMinutes")

    @queued_timeout_in_minutes.setter
    def queued_timeout_in_minutes(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "queuedTimeoutInMinutes", value)

    @builtins.property
    @jsii.member(jsii_name="secondaryArtifacts")
    def secondary_artifacts(
        self,
    ) -> typing.Optional[
        typing.Union[
            aws_cdk.core.IResolvable,
            typing.List[typing.Union["ArtifactsProperty", aws_cdk.core.IResolvable]],
        ]
    ]:
        """``AWS::CodeBuild::Project.SecondaryArtifacts``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-secondaryartifacts
        """
        return jsii.get(self, "secondaryArtifacts")

    @secondary_artifacts.setter
    def secondary_artifacts(
        self,
        value: typing.Optional[
            typing.Union[
                aws_cdk.core.IResolvable,
                typing.List[
                    typing.Union["ArtifactsProperty", aws_cdk.core.IResolvable]
                ],
            ]
        ],
    ) -> None:
        jsii.set(self, "secondaryArtifacts", value)

    @builtins.property
    @jsii.member(jsii_name="secondarySources")
    def secondary_sources(
        self,
    ) -> typing.Optional[
        typing.Union[
            aws_cdk.core.IResolvable,
            typing.List[typing.Union["SourceProperty", aws_cdk.core.IResolvable]],
        ]
    ]:
        """``AWS::CodeBuild::Project.SecondarySources``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-secondarysources
        """
        return jsii.get(self, "secondarySources")

    @secondary_sources.setter
    def secondary_sources(
        self,
        value: typing.Optional[
            typing.Union[
                aws_cdk.core.IResolvable,
                typing.List[typing.Union["SourceProperty", aws_cdk.core.IResolvable]],
            ]
        ],
    ) -> None:
        jsii.set(self, "secondarySources", value)

    @builtins.property
    @jsii.member(jsii_name="secondarySourceVersions")
    def secondary_source_versions(
        self,
    ) -> typing.Optional[
        typing.Union[
            aws_cdk.core.IResolvable,
            typing.List[
                typing.Union[aws_cdk.core.IResolvable, "ProjectSourceVersionProperty"]
            ],
        ]
    ]:
        """``AWS::CodeBuild::Project.SecondarySourceVersions``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-secondarysourceversions
        """
        return jsii.get(self, "secondarySourceVersions")

    @secondary_source_versions.setter
    def secondary_source_versions(
        self,
        value: typing.Optional[
            typing.Union[
                aws_cdk.core.IResolvable,
                typing.List[
                    typing.Union[
                        aws_cdk.core.IResolvable, "ProjectSourceVersionProperty"
                    ]
                ],
            ]
        ],
    ) -> None:
        jsii.set(self, "secondarySourceVersions", value)

    @builtins.property
    @jsii.member(jsii_name="sourceVersion")
    def source_version(self) -> typing.Optional[str]:
        """``AWS::CodeBuild::Project.SourceVersion``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-sourceversion
        """
        return jsii.get(self, "sourceVersion")

    @source_version.setter
    def source_version(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "sourceVersion", value)

    @builtins.property
    @jsii.member(jsii_name="timeoutInMinutes")
    def timeout_in_minutes(self) -> typing.Optional[jsii.Number]:
        """``AWS::CodeBuild::Project.TimeoutInMinutes``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-timeoutinminutes
        """
        return jsii.get(self, "timeoutInMinutes")

    @timeout_in_minutes.setter
    def timeout_in_minutes(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "timeoutInMinutes", value)

    @builtins.property
    @jsii.member(jsii_name="triggers")
    def triggers(
        self,
    ) -> typing.Optional[
        typing.Union[aws_cdk.core.IResolvable, "ProjectTriggersProperty"]
    ]:
        """``AWS::CodeBuild::Project.Triggers``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-triggers
        """
        return jsii.get(self, "triggers")

    @triggers.setter
    def triggers(
        self,
        value: typing.Optional[
            typing.Union[aws_cdk.core.IResolvable, "ProjectTriggersProperty"]
        ],
    ) -> None:
        jsii.set(self, "triggers", value)

    @builtins.property
    @jsii.member(jsii_name="vpcConfig")
    def vpc_config(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "VpcConfigProperty"]]:
        """``AWS::CodeBuild::Project.VpcConfig``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-vpcconfig
        """
        return jsii.get(self, "vpcConfig")

    @vpc_config.setter
    def vpc_config(
        self,
        value: typing.Optional[
            typing.Union[aws_cdk.core.IResolvable, "VpcConfigProperty"]
        ],
    ) -> None:
        jsii.set(self, "vpcConfig", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-codebuild.CfnProject.ArtifactsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "type": "type",
            "artifact_identifier": "artifactIdentifier",
            "encryption_disabled": "encryptionDisabled",
            "location": "location",
            "name": "name",
            "namespace_type": "namespaceType",
            "override_artifact_name": "overrideArtifactName",
            "packaging": "packaging",
            "path": "path",
        },
    )
    class ArtifactsProperty:
        def __init__(
            self,
            *,
            type: str,
            artifact_identifier: typing.Optional[str] = None,
            encryption_disabled: typing.Optional[
                typing.Union[bool, aws_cdk.core.IResolvable]
            ] = None,
            location: typing.Optional[str] = None,
            name: typing.Optional[str] = None,
            namespace_type: typing.Optional[str] = None,
            override_artifact_name: typing.Optional[
                typing.Union[bool, aws_cdk.core.IResolvable]
            ] = None,
            packaging: typing.Optional[str] = None,
            path: typing.Optional[str] = None,
        ) -> None:
            """
            :param type: ``CfnProject.ArtifactsProperty.Type``.
            :param artifact_identifier: ``CfnProject.ArtifactsProperty.ArtifactIdentifier``.
            :param encryption_disabled: ``CfnProject.ArtifactsProperty.EncryptionDisabled``.
            :param location: ``CfnProject.ArtifactsProperty.Location``.
            :param name: ``CfnProject.ArtifactsProperty.Name``.
            :param namespace_type: ``CfnProject.ArtifactsProperty.NamespaceType``.
            :param override_artifact_name: ``CfnProject.ArtifactsProperty.OverrideArtifactName``.
            :param packaging: ``CfnProject.ArtifactsProperty.Packaging``.
            :param path: ``CfnProject.ArtifactsProperty.Path``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-artifacts.html
            """
            self._values = {
                "type": type,
            }
            if artifact_identifier is not None:
                self._values["artifact_identifier"] = artifact_identifier
            if encryption_disabled is not None:
                self._values["encryption_disabled"] = encryption_disabled
            if location is not None:
                self._values["location"] = location
            if name is not None:
                self._values["name"] = name
            if namespace_type is not None:
                self._values["namespace_type"] = namespace_type
            if override_artifact_name is not None:
                self._values["override_artifact_name"] = override_artifact_name
            if packaging is not None:
                self._values["packaging"] = packaging
            if path is not None:
                self._values["path"] = path

        @builtins.property
        def type(self) -> str:
            """``CfnProject.ArtifactsProperty.Type``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-artifacts.html#cfn-codebuild-project-artifacts-type
            """
            return self._values.get("type")

        @builtins.property
        def artifact_identifier(self) -> typing.Optional[str]:
            """``CfnProject.ArtifactsProperty.ArtifactIdentifier``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-artifacts.html#cfn-codebuild-project-artifacts-artifactidentifier
            """
            return self._values.get("artifact_identifier")

        @builtins.property
        def encryption_disabled(
            self,
        ) -> typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]]:
            """``CfnProject.ArtifactsProperty.EncryptionDisabled``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-artifacts.html#cfn-codebuild-project-artifacts-encryptiondisabled
            """
            return self._values.get("encryption_disabled")

        @builtins.property
        def location(self) -> typing.Optional[str]:
            """``CfnProject.ArtifactsProperty.Location``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-artifacts.html#cfn-codebuild-project-artifacts-location
            """
            return self._values.get("location")

        @builtins.property
        def name(self) -> typing.Optional[str]:
            """``CfnProject.ArtifactsProperty.Name``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-artifacts.html#cfn-codebuild-project-artifacts-name
            """
            return self._values.get("name")

        @builtins.property
        def namespace_type(self) -> typing.Optional[str]:
            """``CfnProject.ArtifactsProperty.NamespaceType``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-artifacts.html#cfn-codebuild-project-artifacts-namespacetype
            """
            return self._values.get("namespace_type")

        @builtins.property
        def override_artifact_name(
            self,
        ) -> typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]]:
            """``CfnProject.ArtifactsProperty.OverrideArtifactName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-artifacts.html#cfn-codebuild-project-artifacts-overrideartifactname
            """
            return self._values.get("override_artifact_name")

        @builtins.property
        def packaging(self) -> typing.Optional[str]:
            """``CfnProject.ArtifactsProperty.Packaging``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-artifacts.html#cfn-codebuild-project-artifacts-packaging
            """
            return self._values.get("packaging")

        @builtins.property
        def path(self) -> typing.Optional[str]:
            """``CfnProject.ArtifactsProperty.Path``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-artifacts.html#cfn-codebuild-project-artifacts-path
            """
            return self._values.get("path")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ArtifactsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-codebuild.CfnProject.BuildStatusConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"context": "context", "target_url": "targetUrl"},
    )
    class BuildStatusConfigProperty:
        def __init__(
            self,
            *,
            context: typing.Optional[str] = None,
            target_url: typing.Optional[str] = None,
        ) -> None:
            """
            :param context: ``CfnProject.BuildStatusConfigProperty.Context``.
            :param target_url: ``CfnProject.BuildStatusConfigProperty.TargetUrl``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-buildstatusconfig.html
            """
            self._values = {}
            if context is not None:
                self._values["context"] = context
            if target_url is not None:
                self._values["target_url"] = target_url

        @builtins.property
        def context(self) -> typing.Optional[str]:
            """``CfnProject.BuildStatusConfigProperty.Context``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-buildstatusconfig.html#cfn-codebuild-project-buildstatusconfig-context
            """
            return self._values.get("context")

        @builtins.property
        def target_url(self) -> typing.Optional[str]:
            """``CfnProject.BuildStatusConfigProperty.TargetUrl``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-buildstatusconfig.html#cfn-codebuild-project-buildstatusconfig-targeturl
            """
            return self._values.get("target_url")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BuildStatusConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-codebuild.CfnProject.CloudWatchLogsConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "status": "status",
            "group_name": "groupName",
            "stream_name": "streamName",
        },
    )
    class CloudWatchLogsConfigProperty:
        def __init__(
            self,
            *,
            status: str,
            group_name: typing.Optional[str] = None,
            stream_name: typing.Optional[str] = None,
        ) -> None:
            """
            :param status: ``CfnProject.CloudWatchLogsConfigProperty.Status``.
            :param group_name: ``CfnProject.CloudWatchLogsConfigProperty.GroupName``.
            :param stream_name: ``CfnProject.CloudWatchLogsConfigProperty.StreamName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-cloudwatchlogsconfig.html
            """
            self._values = {
                "status": status,
            }
            if group_name is not None:
                self._values["group_name"] = group_name
            if stream_name is not None:
                self._values["stream_name"] = stream_name

        @builtins.property
        def status(self) -> str:
            """``CfnProject.CloudWatchLogsConfigProperty.Status``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-cloudwatchlogsconfig.html#cfn-codebuild-project-cloudwatchlogsconfig-status
            """
            return self._values.get("status")

        @builtins.property
        def group_name(self) -> typing.Optional[str]:
            """``CfnProject.CloudWatchLogsConfigProperty.GroupName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-cloudwatchlogsconfig.html#cfn-codebuild-project-cloudwatchlogsconfig-groupname
            """
            return self._values.get("group_name")

        @builtins.property
        def stream_name(self) -> typing.Optional[str]:
            """``CfnProject.CloudWatchLogsConfigProperty.StreamName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-cloudwatchlogsconfig.html#cfn-codebuild-project-cloudwatchlogsconfig-streamname
            """
            return self._values.get("stream_name")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CloudWatchLogsConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-codebuild.CfnProject.EnvironmentProperty",
        jsii_struct_bases=[],
        name_mapping={
            "compute_type": "computeType",
            "image": "image",
            "type": "type",
            "certificate": "certificate",
            "environment_variables": "environmentVariables",
            "image_pull_credentials_type": "imagePullCredentialsType",
            "privileged_mode": "privilegedMode",
            "registry_credential": "registryCredential",
        },
    )
    class EnvironmentProperty:
        def __init__(
            self,
            *,
            compute_type: str,
            image: str,
            type: str,
            certificate: typing.Optional[str] = None,
            environment_variables: typing.Optional[
                typing.Union[
                    aws_cdk.core.IResolvable,
                    typing.List[
                        typing.Union[
                            aws_cdk.core.IResolvable,
                            "CfnProject.EnvironmentVariableProperty",
                        ]
                    ],
                ]
            ] = None,
            image_pull_credentials_type: typing.Optional[str] = None,
            privileged_mode: typing.Optional[
                typing.Union[bool, aws_cdk.core.IResolvable]
            ] = None,
            registry_credential: typing.Optional[
                typing.Union[
                    aws_cdk.core.IResolvable, "CfnProject.RegistryCredentialProperty"
                ]
            ] = None,
        ) -> None:
            """
            :param compute_type: ``CfnProject.EnvironmentProperty.ComputeType``.
            :param image: ``CfnProject.EnvironmentProperty.Image``.
            :param type: ``CfnProject.EnvironmentProperty.Type``.
            :param certificate: ``CfnProject.EnvironmentProperty.Certificate``.
            :param environment_variables: ``CfnProject.EnvironmentProperty.EnvironmentVariables``.
            :param image_pull_credentials_type: ``CfnProject.EnvironmentProperty.ImagePullCredentialsType``.
            :param privileged_mode: ``CfnProject.EnvironmentProperty.PrivilegedMode``.
            :param registry_credential: ``CfnProject.EnvironmentProperty.RegistryCredential``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-environment.html
            """
            self._values = {
                "compute_type": compute_type,
                "image": image,
                "type": type,
            }
            if certificate is not None:
                self._values["certificate"] = certificate
            if environment_variables is not None:
                self._values["environment_variables"] = environment_variables
            if image_pull_credentials_type is not None:
                self._values[
                    "image_pull_credentials_type"
                ] = image_pull_credentials_type
            if privileged_mode is not None:
                self._values["privileged_mode"] = privileged_mode
            if registry_credential is not None:
                self._values["registry_credential"] = registry_credential

        @builtins.property
        def compute_type(self) -> str:
            """``CfnProject.EnvironmentProperty.ComputeType``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-environment.html#cfn-codebuild-project-environment-computetype
            """
            return self._values.get("compute_type")

        @builtins.property
        def image(self) -> str:
            """``CfnProject.EnvironmentProperty.Image``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-environment.html#cfn-codebuild-project-environment-image
            """
            return self._values.get("image")

        @builtins.property
        def type(self) -> str:
            """``CfnProject.EnvironmentProperty.Type``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-environment.html#cfn-codebuild-project-environment-type
            """
            return self._values.get("type")

        @builtins.property
        def certificate(self) -> typing.Optional[str]:
            """``CfnProject.EnvironmentProperty.Certificate``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-environment.html#cfn-codebuild-project-environment-certificate
            """
            return self._values.get("certificate")

        @builtins.property
        def environment_variables(
            self,
        ) -> typing.Optional[
            typing.Union[
                aws_cdk.core.IResolvable,
                typing.List[
                    typing.Union[
                        aws_cdk.core.IResolvable,
                        "CfnProject.EnvironmentVariableProperty",
                    ]
                ],
            ]
        ]:
            """``CfnProject.EnvironmentProperty.EnvironmentVariables``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-environment.html#cfn-codebuild-project-environment-environmentvariables
            """
            return self._values.get("environment_variables")

        @builtins.property
        def image_pull_credentials_type(self) -> typing.Optional[str]:
            """``CfnProject.EnvironmentProperty.ImagePullCredentialsType``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-environment.html#cfn-codebuild-project-environment-imagepullcredentialstype
            """
            return self._values.get("image_pull_credentials_type")

        @builtins.property
        def privileged_mode(
            self,
        ) -> typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]]:
            """``CfnProject.EnvironmentProperty.PrivilegedMode``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-environment.html#cfn-codebuild-project-environment-privilegedmode
            """
            return self._values.get("privileged_mode")

        @builtins.property
        def registry_credential(
            self,
        ) -> typing.Optional[
            typing.Union[
                aws_cdk.core.IResolvable, "CfnProject.RegistryCredentialProperty"
            ]
        ]:
            """``CfnProject.EnvironmentProperty.RegistryCredential``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-environment.html#cfn-codebuild-project-environment-registrycredential
            """
            return self._values.get("registry_credential")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EnvironmentProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-codebuild.CfnProject.EnvironmentVariableProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "value": "value", "type": "type"},
    )
    class EnvironmentVariableProperty:
        def __init__(
            self, *, name: str, value: str, type: typing.Optional[str] = None
        ) -> None:
            """
            :param name: ``CfnProject.EnvironmentVariableProperty.Name``.
            :param value: ``CfnProject.EnvironmentVariableProperty.Value``.
            :param type: ``CfnProject.EnvironmentVariableProperty.Type``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-environmentvariable.html
            """
            self._values = {
                "name": name,
                "value": value,
            }
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def name(self) -> str:
            """``CfnProject.EnvironmentVariableProperty.Name``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-environmentvariable.html#cfn-codebuild-project-environmentvariable-name
            """
            return self._values.get("name")

        @builtins.property
        def value(self) -> str:
            """``CfnProject.EnvironmentVariableProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-environmentvariable.html#cfn-codebuild-project-environmentvariable-value
            """
            return self._values.get("value")

        @builtins.property
        def type(self) -> typing.Optional[str]:
            """``CfnProject.EnvironmentVariableProperty.Type``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-environmentvariable.html#cfn-codebuild-project-environmentvariable-type
            """
            return self._values.get("type")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EnvironmentVariableProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-codebuild.CfnProject.GitSubmodulesConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"fetch_submodules": "fetchSubmodules"},
    )
    class GitSubmodulesConfigProperty:
        def __init__(
            self, *, fetch_submodules: typing.Union[bool, aws_cdk.core.IResolvable]
        ) -> None:
            """
            :param fetch_submodules: ``CfnProject.GitSubmodulesConfigProperty.FetchSubmodules``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-gitsubmodulesconfig.html
            """
            self._values = {
                "fetch_submodules": fetch_submodules,
            }

        @builtins.property
        def fetch_submodules(self) -> typing.Union[bool, aws_cdk.core.IResolvable]:
            """``CfnProject.GitSubmodulesConfigProperty.FetchSubmodules``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-gitsubmodulesconfig.html#cfn-codebuild-project-gitsubmodulesconfig-fetchsubmodules
            """
            return self._values.get("fetch_submodules")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GitSubmodulesConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-codebuild.CfnProject.LogsConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"cloud_watch_logs": "cloudWatchLogs", "s3_logs": "s3Logs"},
    )
    class LogsConfigProperty:
        def __init__(
            self,
            *,
            cloud_watch_logs: typing.Optional[
                typing.Union[
                    aws_cdk.core.IResolvable, "CfnProject.CloudWatchLogsConfigProperty"
                ]
            ] = None,
            s3_logs: typing.Optional[
                typing.Union[
                    aws_cdk.core.IResolvable, "CfnProject.S3LogsConfigProperty"
                ]
            ] = None,
        ) -> None:
            """
            :param cloud_watch_logs: ``CfnProject.LogsConfigProperty.CloudWatchLogs``.
            :param s3_logs: ``CfnProject.LogsConfigProperty.S3Logs``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-logsconfig.html
            """
            self._values = {}
            if cloud_watch_logs is not None:
                self._values["cloud_watch_logs"] = cloud_watch_logs
            if s3_logs is not None:
                self._values["s3_logs"] = s3_logs

        @builtins.property
        def cloud_watch_logs(
            self,
        ) -> typing.Optional[
            typing.Union[
                aws_cdk.core.IResolvable, "CfnProject.CloudWatchLogsConfigProperty"
            ]
        ]:
            """``CfnProject.LogsConfigProperty.CloudWatchLogs``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-logsconfig.html#cfn-codebuild-project-logsconfig-cloudwatchlogs
            """
            return self._values.get("cloud_watch_logs")

        @builtins.property
        def s3_logs(
            self,
        ) -> typing.Optional[
            typing.Union[aws_cdk.core.IResolvable, "CfnProject.S3LogsConfigProperty"]
        ]:
            """``CfnProject.LogsConfigProperty.S3Logs``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-logsconfig.html#cfn-codebuild-project-logsconfig-s3logs
            """
            return self._values.get("s3_logs")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LogsConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-codebuild.CfnProject.ProjectCacheProperty",
        jsii_struct_bases=[],
        name_mapping={"type": "type", "location": "location", "modes": "modes"},
    )
    class ProjectCacheProperty:
        def __init__(
            self,
            *,
            type: str,
            location: typing.Optional[str] = None,
            modes: typing.Optional[typing.List[str]] = None,
        ) -> None:
            """
            :param type: ``CfnProject.ProjectCacheProperty.Type``.
            :param location: ``CfnProject.ProjectCacheProperty.Location``.
            :param modes: ``CfnProject.ProjectCacheProperty.Modes``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-projectcache.html
            """
            self._values = {
                "type": type,
            }
            if location is not None:
                self._values["location"] = location
            if modes is not None:
                self._values["modes"] = modes

        @builtins.property
        def type(self) -> str:
            """``CfnProject.ProjectCacheProperty.Type``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-projectcache.html#cfn-codebuild-project-projectcache-type
            """
            return self._values.get("type")

        @builtins.property
        def location(self) -> typing.Optional[str]:
            """``CfnProject.ProjectCacheProperty.Location``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-projectcache.html#cfn-codebuild-project-projectcache-location
            """
            return self._values.get("location")

        @builtins.property
        def modes(self) -> typing.Optional[typing.List[str]]:
            """``CfnProject.ProjectCacheProperty.Modes``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-projectcache.html#cfn-codebuild-project-projectcache-modes
            """
            return self._values.get("modes")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ProjectCacheProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-codebuild.CfnProject.ProjectFileSystemLocationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "identifier": "identifier",
            "location": "location",
            "mount_point": "mountPoint",
            "type": "type",
            "mount_options": "mountOptions",
        },
    )
    class ProjectFileSystemLocationProperty:
        def __init__(
            self,
            *,
            identifier: str,
            location: str,
            mount_point: str,
            type: str,
            mount_options: typing.Optional[str] = None,
        ) -> None:
            """
            :param identifier: ``CfnProject.ProjectFileSystemLocationProperty.Identifier``.
            :param location: ``CfnProject.ProjectFileSystemLocationProperty.Location``.
            :param mount_point: ``CfnProject.ProjectFileSystemLocationProperty.MountPoint``.
            :param type: ``CfnProject.ProjectFileSystemLocationProperty.Type``.
            :param mount_options: ``CfnProject.ProjectFileSystemLocationProperty.MountOptions``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-projectfilesystemlocation.html
            """
            self._values = {
                "identifier": identifier,
                "location": location,
                "mount_point": mount_point,
                "type": type,
            }
            if mount_options is not None:
                self._values["mount_options"] = mount_options

        @builtins.property
        def identifier(self) -> str:
            """``CfnProject.ProjectFileSystemLocationProperty.Identifier``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-projectfilesystemlocation.html#cfn-codebuild-project-projectfilesystemlocation-identifier
            """
            return self._values.get("identifier")

        @builtins.property
        def location(self) -> str:
            """``CfnProject.ProjectFileSystemLocationProperty.Location``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-projectfilesystemlocation.html#cfn-codebuild-project-projectfilesystemlocation-location
            """
            return self._values.get("location")

        @builtins.property
        def mount_point(self) -> str:
            """``CfnProject.ProjectFileSystemLocationProperty.MountPoint``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-projectfilesystemlocation.html#cfn-codebuild-project-projectfilesystemlocation-mountpoint
            """
            return self._values.get("mount_point")

        @builtins.property
        def type(self) -> str:
            """``CfnProject.ProjectFileSystemLocationProperty.Type``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-projectfilesystemlocation.html#cfn-codebuild-project-projectfilesystemlocation-type
            """
            return self._values.get("type")

        @builtins.property
        def mount_options(self) -> typing.Optional[str]:
            """``CfnProject.ProjectFileSystemLocationProperty.MountOptions``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-projectfilesystemlocation.html#cfn-codebuild-project-projectfilesystemlocation-mountoptions
            """
            return self._values.get("mount_options")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ProjectFileSystemLocationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-codebuild.CfnProject.ProjectSourceVersionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "source_identifier": "sourceIdentifier",
            "source_version": "sourceVersion",
        },
    )
    class ProjectSourceVersionProperty:
        def __init__(
            self, *, source_identifier: str, source_version: typing.Optional[str] = None
        ) -> None:
            """
            :param source_identifier: ``CfnProject.ProjectSourceVersionProperty.SourceIdentifier``.
            :param source_version: ``CfnProject.ProjectSourceVersionProperty.SourceVersion``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-projectsourceversion.html
            """
            self._values = {
                "source_identifier": source_identifier,
            }
            if source_version is not None:
                self._values["source_version"] = source_version

        @builtins.property
        def source_identifier(self) -> str:
            """``CfnProject.ProjectSourceVersionProperty.SourceIdentifier``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-projectsourceversion.html#cfn-codebuild-project-projectsourceversion-sourceidentifier
            """
            return self._values.get("source_identifier")

        @builtins.property
        def source_version(self) -> typing.Optional[str]:
            """``CfnProject.ProjectSourceVersionProperty.SourceVersion``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-projectsourceversion.html#cfn-codebuild-project-projectsourceversion-sourceversion
            """
            return self._values.get("source_version")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ProjectSourceVersionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-codebuild.CfnProject.ProjectTriggersProperty",
        jsii_struct_bases=[],
        name_mapping={"filter_groups": "filterGroups", "webhook": "webhook"},
    )
    class ProjectTriggersProperty:
        def __init__(
            self,
            *,
            filter_groups: typing.Optional[
                typing.Union[
                    aws_cdk.core.IResolvable,
                    typing.List[
                        typing.Union[
                            aws_cdk.core.IResolvable,
                            typing.List[
                                typing.Union[
                                    aws_cdk.core.IResolvable,
                                    "CfnProject.WebhookFilterProperty",
                                ]
                            ],
                        ]
                    ],
                ]
            ] = None,
            webhook: typing.Optional[
                typing.Union[bool, aws_cdk.core.IResolvable]
            ] = None,
        ) -> None:
            """
            :param filter_groups: ``CfnProject.ProjectTriggersProperty.FilterGroups``.
            :param webhook: ``CfnProject.ProjectTriggersProperty.Webhook``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-projecttriggers.html
            """
            self._values = {}
            if filter_groups is not None:
                self._values["filter_groups"] = filter_groups
            if webhook is not None:
                self._values["webhook"] = webhook

        @builtins.property
        def filter_groups(
            self,
        ) -> typing.Optional[
            typing.Union[
                aws_cdk.core.IResolvable,
                typing.List[
                    typing.Union[
                        aws_cdk.core.IResolvable,
                        typing.List[
                            typing.Union[
                                aws_cdk.core.IResolvable,
                                "CfnProject.WebhookFilterProperty",
                            ]
                        ],
                    ]
                ],
            ]
        ]:
            """``CfnProject.ProjectTriggersProperty.FilterGroups``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-projecttriggers.html#cfn-codebuild-project-projecttriggers-filtergroups
            """
            return self._values.get("filter_groups")

        @builtins.property
        def webhook(
            self,
        ) -> typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]]:
            """``CfnProject.ProjectTriggersProperty.Webhook``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-projecttriggers.html#cfn-codebuild-project-projecttriggers-webhook
            """
            return self._values.get("webhook")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ProjectTriggersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-codebuild.CfnProject.RegistryCredentialProperty",
        jsii_struct_bases=[],
        name_mapping={
            "credential": "credential",
            "credential_provider": "credentialProvider",
        },
    )
    class RegistryCredentialProperty:
        def __init__(self, *, credential: str, credential_provider: str) -> None:
            """
            :param credential: ``CfnProject.RegistryCredentialProperty.Credential``.
            :param credential_provider: ``CfnProject.RegistryCredentialProperty.CredentialProvider``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-registrycredential.html
            """
            self._values = {
                "credential": credential,
                "credential_provider": credential_provider,
            }

        @builtins.property
        def credential(self) -> str:
            """``CfnProject.RegistryCredentialProperty.Credential``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-registrycredential.html#cfn-codebuild-project-registrycredential-credential
            """
            return self._values.get("credential")

        @builtins.property
        def credential_provider(self) -> str:
            """``CfnProject.RegistryCredentialProperty.CredentialProvider``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-registrycredential.html#cfn-codebuild-project-registrycredential-credentialprovider
            """
            return self._values.get("credential_provider")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RegistryCredentialProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-codebuild.CfnProject.S3LogsConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "status": "status",
            "encryption_disabled": "encryptionDisabled",
            "location": "location",
        },
    )
    class S3LogsConfigProperty:
        def __init__(
            self,
            *,
            status: str,
            encryption_disabled: typing.Optional[
                typing.Union[bool, aws_cdk.core.IResolvable]
            ] = None,
            location: typing.Optional[str] = None,
        ) -> None:
            """
            :param status: ``CfnProject.S3LogsConfigProperty.Status``.
            :param encryption_disabled: ``CfnProject.S3LogsConfigProperty.EncryptionDisabled``.
            :param location: ``CfnProject.S3LogsConfigProperty.Location``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-s3logsconfig.html
            """
            self._values = {
                "status": status,
            }
            if encryption_disabled is not None:
                self._values["encryption_disabled"] = encryption_disabled
            if location is not None:
                self._values["location"] = location

        @builtins.property
        def status(self) -> str:
            """``CfnProject.S3LogsConfigProperty.Status``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-s3logsconfig.html#cfn-codebuild-project-s3logsconfig-status
            """
            return self._values.get("status")

        @builtins.property
        def encryption_disabled(
            self,
        ) -> typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]]:
            """``CfnProject.S3LogsConfigProperty.EncryptionDisabled``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-s3logsconfig.html#cfn-codebuild-project-s3logsconfig-encryptiondisabled
            """
            return self._values.get("encryption_disabled")

        @builtins.property
        def location(self) -> typing.Optional[str]:
            """``CfnProject.S3LogsConfigProperty.Location``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-s3logsconfig.html#cfn-codebuild-project-s3logsconfig-location
            """
            return self._values.get("location")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3LogsConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-codebuild.CfnProject.SourceAuthProperty",
        jsii_struct_bases=[],
        name_mapping={"type": "type", "resource": "resource"},
    )
    class SourceAuthProperty:
        def __init__(self, *, type: str, resource: typing.Optional[str] = None) -> None:
            """
            :param type: ``CfnProject.SourceAuthProperty.Type``.
            :param resource: ``CfnProject.SourceAuthProperty.Resource``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-sourceauth.html
            """
            self._values = {
                "type": type,
            }
            if resource is not None:
                self._values["resource"] = resource

        @builtins.property
        def type(self) -> str:
            """``CfnProject.SourceAuthProperty.Type``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-sourceauth.html#cfn-codebuild-project-sourceauth-type
            """
            return self._values.get("type")

        @builtins.property
        def resource(self) -> typing.Optional[str]:
            """``CfnProject.SourceAuthProperty.Resource``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-sourceauth.html#cfn-codebuild-project-sourceauth-resource
            """
            return self._values.get("resource")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SourceAuthProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-codebuild.CfnProject.SourceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "type": "type",
            "auth": "auth",
            "build_spec": "buildSpec",
            "build_status_config": "buildStatusConfig",
            "git_clone_depth": "gitCloneDepth",
            "git_submodules_config": "gitSubmodulesConfig",
            "insecure_ssl": "insecureSsl",
            "location": "location",
            "report_build_status": "reportBuildStatus",
            "source_identifier": "sourceIdentifier",
        },
    )
    class SourceProperty:
        def __init__(
            self,
            *,
            type: str,
            auth: typing.Optional[
                typing.Union[aws_cdk.core.IResolvable, "CfnProject.SourceAuthProperty"]
            ] = None,
            build_spec: typing.Optional[str] = None,
            build_status_config: typing.Optional[
                typing.Union[
                    aws_cdk.core.IResolvable, "CfnProject.BuildStatusConfigProperty"
                ]
            ] = None,
            git_clone_depth: typing.Optional[jsii.Number] = None,
            git_submodules_config: typing.Optional[
                typing.Union[
                    aws_cdk.core.IResolvable, "CfnProject.GitSubmodulesConfigProperty"
                ]
            ] = None,
            insecure_ssl: typing.Optional[
                typing.Union[bool, aws_cdk.core.IResolvable]
            ] = None,
            location: typing.Optional[str] = None,
            report_build_status: typing.Optional[
                typing.Union[bool, aws_cdk.core.IResolvable]
            ] = None,
            source_identifier: typing.Optional[str] = None,
        ) -> None:
            """
            :param type: ``CfnProject.SourceProperty.Type``.
            :param auth: ``CfnProject.SourceProperty.Auth``.
            :param build_spec: ``CfnProject.SourceProperty.BuildSpec``.
            :param build_status_config: ``CfnProject.SourceProperty.BuildStatusConfig``.
            :param git_clone_depth: ``CfnProject.SourceProperty.GitCloneDepth``.
            :param git_submodules_config: ``CfnProject.SourceProperty.GitSubmodulesConfig``.
            :param insecure_ssl: ``CfnProject.SourceProperty.InsecureSsl``.
            :param location: ``CfnProject.SourceProperty.Location``.
            :param report_build_status: ``CfnProject.SourceProperty.ReportBuildStatus``.
            :param source_identifier: ``CfnProject.SourceProperty.SourceIdentifier``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-source.html
            """
            self._values = {
                "type": type,
            }
            if auth is not None:
                self._values["auth"] = auth
            if build_spec is not None:
                self._values["build_spec"] = build_spec
            if build_status_config is not None:
                self._values["build_status_config"] = build_status_config
            if git_clone_depth is not None:
                self._values["git_clone_depth"] = git_clone_depth
            if git_submodules_config is not None:
                self._values["git_submodules_config"] = git_submodules_config
            if insecure_ssl is not None:
                self._values["insecure_ssl"] = insecure_ssl
            if location is not None:
                self._values["location"] = location
            if report_build_status is not None:
                self._values["report_build_status"] = report_build_status
            if source_identifier is not None:
                self._values["source_identifier"] = source_identifier

        @builtins.property
        def type(self) -> str:
            """``CfnProject.SourceProperty.Type``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-source.html#cfn-codebuild-project-source-type
            """
            return self._values.get("type")

        @builtins.property
        def auth(
            self,
        ) -> typing.Optional[
            typing.Union[aws_cdk.core.IResolvable, "CfnProject.SourceAuthProperty"]
        ]:
            """``CfnProject.SourceProperty.Auth``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-source.html#cfn-codebuild-project-source-auth
            """
            return self._values.get("auth")

        @builtins.property
        def build_spec(self) -> typing.Optional[str]:
            """``CfnProject.SourceProperty.BuildSpec``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-source.html#cfn-codebuild-project-source-buildspec
            """
            return self._values.get("build_spec")

        @builtins.property
        def build_status_config(
            self,
        ) -> typing.Optional[
            typing.Union[
                aws_cdk.core.IResolvable, "CfnProject.BuildStatusConfigProperty"
            ]
        ]:
            """``CfnProject.SourceProperty.BuildStatusConfig``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-source.html#cfn-codebuild-project-source-buildstatusconfig
            """
            return self._values.get("build_status_config")

        @builtins.property
        def git_clone_depth(self) -> typing.Optional[jsii.Number]:
            """``CfnProject.SourceProperty.GitCloneDepth``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-source.html#cfn-codebuild-project-source-gitclonedepth
            """
            return self._values.get("git_clone_depth")

        @builtins.property
        def git_submodules_config(
            self,
        ) -> typing.Optional[
            typing.Union[
                aws_cdk.core.IResolvable, "CfnProject.GitSubmodulesConfigProperty"
            ]
        ]:
            """``CfnProject.SourceProperty.GitSubmodulesConfig``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-source.html#cfn-codebuild-project-source-gitsubmodulesconfig
            """
            return self._values.get("git_submodules_config")

        @builtins.property
        def insecure_ssl(
            self,
        ) -> typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]]:
            """``CfnProject.SourceProperty.InsecureSsl``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-source.html#cfn-codebuild-project-source-insecuressl
            """
            return self._values.get("insecure_ssl")

        @builtins.property
        def location(self) -> typing.Optional[str]:
            """``CfnProject.SourceProperty.Location``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-source.html#cfn-codebuild-project-source-location
            """
            return self._values.get("location")

        @builtins.property
        def report_build_status(
            self,
        ) -> typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]]:
            """``CfnProject.SourceProperty.ReportBuildStatus``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-source.html#cfn-codebuild-project-source-reportbuildstatus
            """
            return self._values.get("report_build_status")

        @builtins.property
        def source_identifier(self) -> typing.Optional[str]:
            """``CfnProject.SourceProperty.SourceIdentifier``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-source.html#cfn-codebuild-project-source-sourceidentifier
            """
            return self._values.get("source_identifier")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-codebuild.CfnProject.VpcConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "security_group_ids": "securityGroupIds",
            "subnets": "subnets",
            "vpc_id": "vpcId",
        },
    )
    class VpcConfigProperty:
        def __init__(
            self,
            *,
            security_group_ids: typing.Optional[typing.List[str]] = None,
            subnets: typing.Optional[typing.List[str]] = None,
            vpc_id: typing.Optional[str] = None,
        ) -> None:
            """
            :param security_group_ids: ``CfnProject.VpcConfigProperty.SecurityGroupIds``.
            :param subnets: ``CfnProject.VpcConfigProperty.Subnets``.
            :param vpc_id: ``CfnProject.VpcConfigProperty.VpcId``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-vpcconfig.html
            """
            self._values = {}
            if security_group_ids is not None:
                self._values["security_group_ids"] = security_group_ids
            if subnets is not None:
                self._values["subnets"] = subnets
            if vpc_id is not None:
                self._values["vpc_id"] = vpc_id

        @builtins.property
        def security_group_ids(self) -> typing.Optional[typing.List[str]]:
            """``CfnProject.VpcConfigProperty.SecurityGroupIds``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-vpcconfig.html#cfn-codebuild-project-vpcconfig-securitygroupids
            """
            return self._values.get("security_group_ids")

        @builtins.property
        def subnets(self) -> typing.Optional[typing.List[str]]:
            """``CfnProject.VpcConfigProperty.Subnets``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-vpcconfig.html#cfn-codebuild-project-vpcconfig-subnets
            """
            return self._values.get("subnets")

        @builtins.property
        def vpc_id(self) -> typing.Optional[str]:
            """``CfnProject.VpcConfigProperty.VpcId``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-vpcconfig.html#cfn-codebuild-project-vpcconfig-vpcid
            """
            return self._values.get("vpc_id")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VpcConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-codebuild.CfnProject.WebhookFilterProperty",
        jsii_struct_bases=[],
        name_mapping={
            "pattern": "pattern",
            "type": "type",
            "exclude_matched_pattern": "excludeMatchedPattern",
        },
    )
    class WebhookFilterProperty:
        def __init__(
            self,
            *,
            pattern: str,
            type: str,
            exclude_matched_pattern: typing.Optional[
                typing.Union[bool, aws_cdk.core.IResolvable]
            ] = None,
        ) -> None:
            """
            :param pattern: ``CfnProject.WebhookFilterProperty.Pattern``.
            :param type: ``CfnProject.WebhookFilterProperty.Type``.
            :param exclude_matched_pattern: ``CfnProject.WebhookFilterProperty.ExcludeMatchedPattern``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-webhookfilter.html
            """
            self._values = {
                "pattern": pattern,
                "type": type,
            }
            if exclude_matched_pattern is not None:
                self._values["exclude_matched_pattern"] = exclude_matched_pattern

        @builtins.property
        def pattern(self) -> str:
            """``CfnProject.WebhookFilterProperty.Pattern``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-webhookfilter.html#cfn-codebuild-project-webhookfilter-pattern
            """
            return self._values.get("pattern")

        @builtins.property
        def type(self) -> str:
            """``CfnProject.WebhookFilterProperty.Type``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-webhookfilter.html#cfn-codebuild-project-webhookfilter-type
            """
            return self._values.get("type")

        @builtins.property
        def exclude_matched_pattern(
            self,
        ) -> typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]]:
            """``CfnProject.WebhookFilterProperty.ExcludeMatchedPattern``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-webhookfilter.html#cfn-codebuild-project-webhookfilter-excludematchedpattern
            """
            return self._values.get("exclude_matched_pattern")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "WebhookFilterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-codebuild.CfnProjectProps",
    jsii_struct_bases=[],
    name_mapping={
        "artifacts": "artifacts",
        "environment": "environment",
        "service_role": "serviceRole",
        "source": "source",
        "badge_enabled": "badgeEnabled",
        "cache": "cache",
        "description": "description",
        "encryption_key": "encryptionKey",
        "file_system_locations": "fileSystemLocations",
        "logs_config": "logsConfig",
        "name": "name",
        "queued_timeout_in_minutes": "queuedTimeoutInMinutes",
        "secondary_artifacts": "secondaryArtifacts",
        "secondary_sources": "secondarySources",
        "secondary_source_versions": "secondarySourceVersions",
        "source_version": "sourceVersion",
        "tags": "tags",
        "timeout_in_minutes": "timeoutInMinutes",
        "triggers": "triggers",
        "vpc_config": "vpcConfig",
    },
)
class CfnProjectProps:
    def __init__(
        self,
        *,
        artifacts: typing.Union[
            "CfnProject.ArtifactsProperty", aws_cdk.core.IResolvable
        ],
        environment: typing.Union[
            aws_cdk.core.IResolvable, "CfnProject.EnvironmentProperty"
        ],
        service_role: str,
        source: typing.Union["CfnProject.SourceProperty", aws_cdk.core.IResolvable],
        badge_enabled: typing.Optional[
            typing.Union[bool, aws_cdk.core.IResolvable]
        ] = None,
        cache: typing.Optional[
            typing.Union[aws_cdk.core.IResolvable, "CfnProject.ProjectCacheProperty"]
        ] = None,
        description: typing.Optional[str] = None,
        encryption_key: typing.Optional[str] = None,
        file_system_locations: typing.Optional[
            typing.Union[
                aws_cdk.core.IResolvable,
                typing.List[
                    typing.Union[
                        "CfnProject.ProjectFileSystemLocationProperty",
                        aws_cdk.core.IResolvable,
                    ]
                ],
            ]
        ] = None,
        logs_config: typing.Optional[
            typing.Union[aws_cdk.core.IResolvable, "CfnProject.LogsConfigProperty"]
        ] = None,
        name: typing.Optional[str] = None,
        queued_timeout_in_minutes: typing.Optional[jsii.Number] = None,
        secondary_artifacts: typing.Optional[
            typing.Union[
                aws_cdk.core.IResolvable,
                typing.List[
                    typing.Union[
                        "CfnProject.ArtifactsProperty", aws_cdk.core.IResolvable
                    ]
                ],
            ]
        ] = None,
        secondary_sources: typing.Optional[
            typing.Union[
                aws_cdk.core.IResolvable,
                typing.List[
                    typing.Union["CfnProject.SourceProperty", aws_cdk.core.IResolvable]
                ],
            ]
        ] = None,
        secondary_source_versions: typing.Optional[
            typing.Union[
                aws_cdk.core.IResolvable,
                typing.List[
                    typing.Union[
                        aws_cdk.core.IResolvable,
                        "CfnProject.ProjectSourceVersionProperty",
                    ]
                ],
            ]
        ] = None,
        source_version: typing.Optional[str] = None,
        tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]] = None,
        timeout_in_minutes: typing.Optional[jsii.Number] = None,
        triggers: typing.Optional[
            typing.Union[aws_cdk.core.IResolvable, "CfnProject.ProjectTriggersProperty"]
        ] = None,
        vpc_config: typing.Optional[
            typing.Union[aws_cdk.core.IResolvable, "CfnProject.VpcConfigProperty"]
        ] = None,
    ) -> None:
        """Properties for defining a ``AWS::CodeBuild::Project``.

        :param artifacts: ``AWS::CodeBuild::Project.Artifacts``.
        :param environment: ``AWS::CodeBuild::Project.Environment``.
        :param service_role: ``AWS::CodeBuild::Project.ServiceRole``.
        :param source: ``AWS::CodeBuild::Project.Source``.
        :param badge_enabled: ``AWS::CodeBuild::Project.BadgeEnabled``.
        :param cache: ``AWS::CodeBuild::Project.Cache``.
        :param description: ``AWS::CodeBuild::Project.Description``.
        :param encryption_key: ``AWS::CodeBuild::Project.EncryptionKey``.
        :param file_system_locations: ``AWS::CodeBuild::Project.FileSystemLocations``.
        :param logs_config: ``AWS::CodeBuild::Project.LogsConfig``.
        :param name: ``AWS::CodeBuild::Project.Name``.
        :param queued_timeout_in_minutes: ``AWS::CodeBuild::Project.QueuedTimeoutInMinutes``.
        :param secondary_artifacts: ``AWS::CodeBuild::Project.SecondaryArtifacts``.
        :param secondary_sources: ``AWS::CodeBuild::Project.SecondarySources``.
        :param secondary_source_versions: ``AWS::CodeBuild::Project.SecondarySourceVersions``.
        :param source_version: ``AWS::CodeBuild::Project.SourceVersion``.
        :param tags: ``AWS::CodeBuild::Project.Tags``.
        :param timeout_in_minutes: ``AWS::CodeBuild::Project.TimeoutInMinutes``.
        :param triggers: ``AWS::CodeBuild::Project.Triggers``.
        :param vpc_config: ``AWS::CodeBuild::Project.VpcConfig``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html
        """
        self._values = {
            "artifacts": artifacts,
            "environment": environment,
            "service_role": service_role,
            "source": source,
        }
        if badge_enabled is not None:
            self._values["badge_enabled"] = badge_enabled
        if cache is not None:
            self._values["cache"] = cache
        if description is not None:
            self._values["description"] = description
        if encryption_key is not None:
            self._values["encryption_key"] = encryption_key
        if file_system_locations is not None:
            self._values["file_system_locations"] = file_system_locations
        if logs_config is not None:
            self._values["logs_config"] = logs_config
        if name is not None:
            self._values["name"] = name
        if queued_timeout_in_minutes is not None:
            self._values["queued_timeout_in_minutes"] = queued_timeout_in_minutes
        if secondary_artifacts is not None:
            self._values["secondary_artifacts"] = secondary_artifacts
        if secondary_sources is not None:
            self._values["secondary_sources"] = secondary_sources
        if secondary_source_versions is not None:
            self._values["secondary_source_versions"] = secondary_source_versions
        if source_version is not None:
            self._values["source_version"] = source_version
        if tags is not None:
            self._values["tags"] = tags
        if timeout_in_minutes is not None:
            self._values["timeout_in_minutes"] = timeout_in_minutes
        if triggers is not None:
            self._values["triggers"] = triggers
        if vpc_config is not None:
            self._values["vpc_config"] = vpc_config

    @builtins.property
    def artifacts(
        self,
    ) -> typing.Union["CfnProject.ArtifactsProperty", aws_cdk.core.IResolvable]:
        """``AWS::CodeBuild::Project.Artifacts``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-artifacts
        """
        return self._values.get("artifacts")

    @builtins.property
    def environment(
        self,
    ) -> typing.Union[aws_cdk.core.IResolvable, "CfnProject.EnvironmentProperty"]:
        """``AWS::CodeBuild::Project.Environment``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-environment
        """
        return self._values.get("environment")

    @builtins.property
    def service_role(self) -> str:
        """``AWS::CodeBuild::Project.ServiceRole``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-servicerole
        """
        return self._values.get("service_role")

    @builtins.property
    def source(
        self,
    ) -> typing.Union["CfnProject.SourceProperty", aws_cdk.core.IResolvable]:
        """``AWS::CodeBuild::Project.Source``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-source
        """
        return self._values.get("source")

    @builtins.property
    def badge_enabled(
        self,
    ) -> typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]]:
        """``AWS::CodeBuild::Project.BadgeEnabled``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-badgeenabled
        """
        return self._values.get("badge_enabled")

    @builtins.property
    def cache(
        self,
    ) -> typing.Optional[
        typing.Union[aws_cdk.core.IResolvable, "CfnProject.ProjectCacheProperty"]
    ]:
        """``AWS::CodeBuild::Project.Cache``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-cache
        """
        return self._values.get("cache")

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """``AWS::CodeBuild::Project.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-description
        """
        return self._values.get("description")

    @builtins.property
    def encryption_key(self) -> typing.Optional[str]:
        """``AWS::CodeBuild::Project.EncryptionKey``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-encryptionkey
        """
        return self._values.get("encryption_key")

    @builtins.property
    def file_system_locations(
        self,
    ) -> typing.Optional[
        typing.Union[
            aws_cdk.core.IResolvable,
            typing.List[
                typing.Union[
                    "CfnProject.ProjectFileSystemLocationProperty",
                    aws_cdk.core.IResolvable,
                ]
            ],
        ]
    ]:
        """``AWS::CodeBuild::Project.FileSystemLocations``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-filesystemlocations
        """
        return self._values.get("file_system_locations")

    @builtins.property
    def logs_config(
        self,
    ) -> typing.Optional[
        typing.Union[aws_cdk.core.IResolvable, "CfnProject.LogsConfigProperty"]
    ]:
        """``AWS::CodeBuild::Project.LogsConfig``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-logsconfig
        """
        return self._values.get("logs_config")

    @builtins.property
    def name(self) -> typing.Optional[str]:
        """``AWS::CodeBuild::Project.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-name
        """
        return self._values.get("name")

    @builtins.property
    def queued_timeout_in_minutes(self) -> typing.Optional[jsii.Number]:
        """``AWS::CodeBuild::Project.QueuedTimeoutInMinutes``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-queuedtimeoutinminutes
        """
        return self._values.get("queued_timeout_in_minutes")

    @builtins.property
    def secondary_artifacts(
        self,
    ) -> typing.Optional[
        typing.Union[
            aws_cdk.core.IResolvable,
            typing.List[
                typing.Union["CfnProject.ArtifactsProperty", aws_cdk.core.IResolvable]
            ],
        ]
    ]:
        """``AWS::CodeBuild::Project.SecondaryArtifacts``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-secondaryartifacts
        """
        return self._values.get("secondary_artifacts")

    @builtins.property
    def secondary_sources(
        self,
    ) -> typing.Optional[
        typing.Union[
            aws_cdk.core.IResolvable,
            typing.List[
                typing.Union["CfnProject.SourceProperty", aws_cdk.core.IResolvable]
            ],
        ]
    ]:
        """``AWS::CodeBuild::Project.SecondarySources``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-secondarysources
        """
        return self._values.get("secondary_sources")

    @builtins.property
    def secondary_source_versions(
        self,
    ) -> typing.Optional[
        typing.Union[
            aws_cdk.core.IResolvable,
            typing.List[
                typing.Union[
                    aws_cdk.core.IResolvable, "CfnProject.ProjectSourceVersionProperty"
                ]
            ],
        ]
    ]:
        """``AWS::CodeBuild::Project.SecondarySourceVersions``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-secondarysourceversions
        """
        return self._values.get("secondary_source_versions")

    @builtins.property
    def source_version(self) -> typing.Optional[str]:
        """``AWS::CodeBuild::Project.SourceVersion``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-sourceversion
        """
        return self._values.get("source_version")

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        """``AWS::CodeBuild::Project.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-tags
        """
        return self._values.get("tags")

    @builtins.property
    def timeout_in_minutes(self) -> typing.Optional[jsii.Number]:
        """``AWS::CodeBuild::Project.TimeoutInMinutes``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-timeoutinminutes
        """
        return self._values.get("timeout_in_minutes")

    @builtins.property
    def triggers(
        self,
    ) -> typing.Optional[
        typing.Union[aws_cdk.core.IResolvable, "CfnProject.ProjectTriggersProperty"]
    ]:
        """``AWS::CodeBuild::Project.Triggers``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-triggers
        """
        return self._values.get("triggers")

    @builtins.property
    def vpc_config(
        self,
    ) -> typing.Optional[
        typing.Union[aws_cdk.core.IResolvable, "CfnProject.VpcConfigProperty"]
    ]:
        """``AWS::CodeBuild::Project.VpcConfig``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-vpcconfig
        """
        return self._values.get("vpc_config")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnProjectProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnReportGroup(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-codebuild.CfnReportGroup",
):
    """A CloudFormation ``AWS::CodeBuild::ReportGroup``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-reportgroup.html
    cloudformationResource:
    :cloudformationResource:: AWS::CodeBuild::ReportGroup
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: str,
        *,
        export_config: typing.Union[
            aws_cdk.core.IResolvable, "ReportExportConfigProperty"
        ],
        type: str,
        name: typing.Optional[str] = None,
        tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]] = None,
    ) -> None:
        """Create a new ``AWS::CodeBuild::ReportGroup``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param export_config: ``AWS::CodeBuild::ReportGroup.ExportConfig``.
        :param type: ``AWS::CodeBuild::ReportGroup.Type``.
        :param name: ``AWS::CodeBuild::ReportGroup.Name``.
        :param tags: ``AWS::CodeBuild::ReportGroup.Tags``.
        """
        props = CfnReportGroupProps(
            export_config=export_config, type=type, name=name, tags=tags
        )

        jsii.create(CfnReportGroup, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(
        cls,
        scope: aws_cdk.core.Construct,
        id: str,
        resource_attributes: typing.Any,
        *,
        finder: aws_cdk.core.ICfnFinder,
    ) -> "CfnReportGroup":
        """A factory method that creates a new instance of this class from an object containing the CloudFormation properties of this resource.

        Used in the @aws-cdk/cloudformation-include module.

        :param scope: -
        :param id: -
        :param resource_attributes: -
        :param finder: The finder interface used to resolve references across the template.

        stability
        :stability: experimental
        """
        options = aws_cdk.core.FromCloudFormationOptions(finder=finder)

        return jsii.sinvoke(
            cls, "fromCloudFormation", [scope, id, resource_attributes, options]
        )

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        """Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self, props: typing.Mapping[str, typing.Any]
    ) -> typing.Mapping[str, typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: Arn
        """
        return jsii.get(self, "attrArn")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        """``AWS::CodeBuild::ReportGroup.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-reportgroup.html#cfn-codebuild-reportgroup-tags
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="exportConfig")
    def export_config(
        self,
    ) -> typing.Union[aws_cdk.core.IResolvable, "ReportExportConfigProperty"]:
        """``AWS::CodeBuild::ReportGroup.ExportConfig``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-reportgroup.html#cfn-codebuild-reportgroup-exportconfig
        """
        return jsii.get(self, "exportConfig")

    @export_config.setter
    def export_config(
        self,
        value: typing.Union[aws_cdk.core.IResolvable, "ReportExportConfigProperty"],
    ) -> None:
        jsii.set(self, "exportConfig", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> str:
        """``AWS::CodeBuild::ReportGroup.Type``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-reportgroup.html#cfn-codebuild-reportgroup-type
        """
        return jsii.get(self, "type")

    @type.setter
    def type(self, value: str) -> None:
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[str]:
        """``AWS::CodeBuild::ReportGroup.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-reportgroup.html#cfn-codebuild-reportgroup-name
        """
        return jsii.get(self, "name")

    @name.setter
    def name(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "name", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-codebuild.CfnReportGroup.ReportExportConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "export_config_type": "exportConfigType",
            "s3_destination": "s3Destination",
        },
    )
    class ReportExportConfigProperty:
        def __init__(
            self,
            *,
            export_config_type: str,
            s3_destination: typing.Optional[
                typing.Union[
                    aws_cdk.core.IResolvable,
                    "CfnReportGroup.S3ReportExportConfigProperty",
                ]
            ] = None,
        ) -> None:
            """
            :param export_config_type: ``CfnReportGroup.ReportExportConfigProperty.ExportConfigType``.
            :param s3_destination: ``CfnReportGroup.ReportExportConfigProperty.S3Destination``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-reportgroup-reportexportconfig.html
            """
            self._values = {
                "export_config_type": export_config_type,
            }
            if s3_destination is not None:
                self._values["s3_destination"] = s3_destination

        @builtins.property
        def export_config_type(self) -> str:
            """``CfnReportGroup.ReportExportConfigProperty.ExportConfigType``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-reportgroup-reportexportconfig.html#cfn-codebuild-reportgroup-reportexportconfig-exportconfigtype
            """
            return self._values.get("export_config_type")

        @builtins.property
        def s3_destination(
            self,
        ) -> typing.Optional[
            typing.Union[
                aws_cdk.core.IResolvable, "CfnReportGroup.S3ReportExportConfigProperty"
            ]
        ]:
            """``CfnReportGroup.ReportExportConfigProperty.S3Destination``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-reportgroup-reportexportconfig.html#cfn-codebuild-reportgroup-reportexportconfig-s3destination
            """
            return self._values.get("s3_destination")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ReportExportConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-codebuild.CfnReportGroup.S3ReportExportConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bucket": "bucket",
            "encryption_disabled": "encryptionDisabled",
            "encryption_key": "encryptionKey",
            "packaging": "packaging",
            "path": "path",
        },
    )
    class S3ReportExportConfigProperty:
        def __init__(
            self,
            *,
            bucket: str,
            encryption_disabled: typing.Optional[
                typing.Union[bool, aws_cdk.core.IResolvable]
            ] = None,
            encryption_key: typing.Optional[str] = None,
            packaging: typing.Optional[str] = None,
            path: typing.Optional[str] = None,
        ) -> None:
            """
            :param bucket: ``CfnReportGroup.S3ReportExportConfigProperty.Bucket``.
            :param encryption_disabled: ``CfnReportGroup.S3ReportExportConfigProperty.EncryptionDisabled``.
            :param encryption_key: ``CfnReportGroup.S3ReportExportConfigProperty.EncryptionKey``.
            :param packaging: ``CfnReportGroup.S3ReportExportConfigProperty.Packaging``.
            :param path: ``CfnReportGroup.S3ReportExportConfigProperty.Path``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-reportgroup-s3reportexportconfig.html
            """
            self._values = {
                "bucket": bucket,
            }
            if encryption_disabled is not None:
                self._values["encryption_disabled"] = encryption_disabled
            if encryption_key is not None:
                self._values["encryption_key"] = encryption_key
            if packaging is not None:
                self._values["packaging"] = packaging
            if path is not None:
                self._values["path"] = path

        @builtins.property
        def bucket(self) -> str:
            """``CfnReportGroup.S3ReportExportConfigProperty.Bucket``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-reportgroup-s3reportexportconfig.html#cfn-codebuild-reportgroup-s3reportexportconfig-bucket
            """
            return self._values.get("bucket")

        @builtins.property
        def encryption_disabled(
            self,
        ) -> typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]]:
            """``CfnReportGroup.S3ReportExportConfigProperty.EncryptionDisabled``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-reportgroup-s3reportexportconfig.html#cfn-codebuild-reportgroup-s3reportexportconfig-encryptiondisabled
            """
            return self._values.get("encryption_disabled")

        @builtins.property
        def encryption_key(self) -> typing.Optional[str]:
            """``CfnReportGroup.S3ReportExportConfigProperty.EncryptionKey``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-reportgroup-s3reportexportconfig.html#cfn-codebuild-reportgroup-s3reportexportconfig-encryptionkey
            """
            return self._values.get("encryption_key")

        @builtins.property
        def packaging(self) -> typing.Optional[str]:
            """``CfnReportGroup.S3ReportExportConfigProperty.Packaging``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-reportgroup-s3reportexportconfig.html#cfn-codebuild-reportgroup-s3reportexportconfig-packaging
            """
            return self._values.get("packaging")

        @builtins.property
        def path(self) -> typing.Optional[str]:
            """``CfnReportGroup.S3ReportExportConfigProperty.Path``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-reportgroup-s3reportexportconfig.html#cfn-codebuild-reportgroup-s3reportexportconfig-path
            """
            return self._values.get("path")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3ReportExportConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-codebuild.CfnReportGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "export_config": "exportConfig",
        "type": "type",
        "name": "name",
        "tags": "tags",
    },
)
class CfnReportGroupProps:
    def __init__(
        self,
        *,
        export_config: typing.Union[
            aws_cdk.core.IResolvable, "CfnReportGroup.ReportExportConfigProperty"
        ],
        type: str,
        name: typing.Optional[str] = None,
        tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]] = None,
    ) -> None:
        """Properties for defining a ``AWS::CodeBuild::ReportGroup``.

        :param export_config: ``AWS::CodeBuild::ReportGroup.ExportConfig``.
        :param type: ``AWS::CodeBuild::ReportGroup.Type``.
        :param name: ``AWS::CodeBuild::ReportGroup.Name``.
        :param tags: ``AWS::CodeBuild::ReportGroup.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-reportgroup.html
        """
        self._values = {
            "export_config": export_config,
            "type": type,
        }
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def export_config(
        self,
    ) -> typing.Union[
        aws_cdk.core.IResolvable, "CfnReportGroup.ReportExportConfigProperty"
    ]:
        """``AWS::CodeBuild::ReportGroup.ExportConfig``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-reportgroup.html#cfn-codebuild-reportgroup-exportconfig
        """
        return self._values.get("export_config")

    @builtins.property
    def type(self) -> str:
        """``AWS::CodeBuild::ReportGroup.Type``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-reportgroup.html#cfn-codebuild-reportgroup-type
        """
        return self._values.get("type")

    @builtins.property
    def name(self) -> typing.Optional[str]:
        """``AWS::CodeBuild::ReportGroup.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-reportgroup.html#cfn-codebuild-reportgroup-name
        """
        return self._values.get("name")

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        """``AWS::CodeBuild::ReportGroup.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-reportgroup.html#cfn-codebuild-reportgroup-tags
        """
        return self._values.get("tags")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnReportGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnSourceCredential(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-codebuild.CfnSourceCredential",
):
    """A CloudFormation ``AWS::CodeBuild::SourceCredential``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-sourcecredential.html
    cloudformationResource:
    :cloudformationResource:: AWS::CodeBuild::SourceCredential
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: str,
        *,
        auth_type: str,
        server_type: str,
        token: str,
        username: typing.Optional[str] = None,
    ) -> None:
        """Create a new ``AWS::CodeBuild::SourceCredential``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param auth_type: ``AWS::CodeBuild::SourceCredential.AuthType``.
        :param server_type: ``AWS::CodeBuild::SourceCredential.ServerType``.
        :param token: ``AWS::CodeBuild::SourceCredential.Token``.
        :param username: ``AWS::CodeBuild::SourceCredential.Username``.
        """
        props = CfnSourceCredentialProps(
            auth_type=auth_type, server_type=server_type, token=token, username=username
        )

        jsii.create(CfnSourceCredential, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(
        cls,
        scope: aws_cdk.core.Construct,
        id: str,
        resource_attributes: typing.Any,
        *,
        finder: aws_cdk.core.ICfnFinder,
    ) -> "CfnSourceCredential":
        """A factory method that creates a new instance of this class from an object containing the CloudFormation properties of this resource.

        Used in the @aws-cdk/cloudformation-include module.

        :param scope: -
        :param id: -
        :param resource_attributes: -
        :param finder: The finder interface used to resolve references across the template.

        stability
        :stability: experimental
        """
        options = aws_cdk.core.FromCloudFormationOptions(finder=finder)

        return jsii.sinvoke(
            cls, "fromCloudFormation", [scope, id, resource_attributes, options]
        )

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        """Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self, props: typing.Mapping[str, typing.Any]
    ) -> typing.Mapping[str, typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="authType")
    def auth_type(self) -> str:
        """``AWS::CodeBuild::SourceCredential.AuthType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-sourcecredential.html#cfn-codebuild-sourcecredential-authtype
        """
        return jsii.get(self, "authType")

    @auth_type.setter
    def auth_type(self, value: str) -> None:
        jsii.set(self, "authType", value)

    @builtins.property
    @jsii.member(jsii_name="serverType")
    def server_type(self) -> str:
        """``AWS::CodeBuild::SourceCredential.ServerType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-sourcecredential.html#cfn-codebuild-sourcecredential-servertype
        """
        return jsii.get(self, "serverType")

    @server_type.setter
    def server_type(self, value: str) -> None:
        jsii.set(self, "serverType", value)

    @builtins.property
    @jsii.member(jsii_name="token")
    def token(self) -> str:
        """``AWS::CodeBuild::SourceCredential.Token``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-sourcecredential.html#cfn-codebuild-sourcecredential-token
        """
        return jsii.get(self, "token")

    @token.setter
    def token(self, value: str) -> None:
        jsii.set(self, "token", value)

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> typing.Optional[str]:
        """``AWS::CodeBuild::SourceCredential.Username``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-sourcecredential.html#cfn-codebuild-sourcecredential-username
        """
        return jsii.get(self, "username")

    @username.setter
    def username(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "username", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-codebuild.CfnSourceCredentialProps",
    jsii_struct_bases=[],
    name_mapping={
        "auth_type": "authType",
        "server_type": "serverType",
        "token": "token",
        "username": "username",
    },
)
class CfnSourceCredentialProps:
    def __init__(
        self,
        *,
        auth_type: str,
        server_type: str,
        token: str,
        username: typing.Optional[str] = None,
    ) -> None:
        """Properties for defining a ``AWS::CodeBuild::SourceCredential``.

        :param auth_type: ``AWS::CodeBuild::SourceCredential.AuthType``.
        :param server_type: ``AWS::CodeBuild::SourceCredential.ServerType``.
        :param token: ``AWS::CodeBuild::SourceCredential.Token``.
        :param username: ``AWS::CodeBuild::SourceCredential.Username``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-sourcecredential.html
        """
        self._values = {
            "auth_type": auth_type,
            "server_type": server_type,
            "token": token,
        }
        if username is not None:
            self._values["username"] = username

    @builtins.property
    def auth_type(self) -> str:
        """``AWS::CodeBuild::SourceCredential.AuthType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-sourcecredential.html#cfn-codebuild-sourcecredential-authtype
        """
        return self._values.get("auth_type")

    @builtins.property
    def server_type(self) -> str:
        """``AWS::CodeBuild::SourceCredential.ServerType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-sourcecredential.html#cfn-codebuild-sourcecredential-servertype
        """
        return self._values.get("server_type")

    @builtins.property
    def token(self) -> str:
        """``AWS::CodeBuild::SourceCredential.Token``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-sourcecredential.html#cfn-codebuild-sourcecredential-token
        """
        return self._values.get("token")

    @builtins.property
    def username(self) -> typing.Optional[str]:
        """``AWS::CodeBuild::SourceCredential.Username``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-sourcecredential.html#cfn-codebuild-sourcecredential-username
        """
        return self._values.get("username")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSourceCredentialProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-codebuild.CommonProjectProps",
    jsii_struct_bases=[],
    name_mapping={
        "allow_all_outbound": "allowAllOutbound",
        "badge": "badge",
        "build_spec": "buildSpec",
        "cache": "cache",
        "description": "description",
        "encryption_key": "encryptionKey",
        "environment": "environment",
        "environment_variables": "environmentVariables",
        "file_system_locations": "fileSystemLocations",
        "grant_report_group_permissions": "grantReportGroupPermissions",
        "project_name": "projectName",
        "role": "role",
        "security_groups": "securityGroups",
        "subnet_selection": "subnetSelection",
        "timeout": "timeout",
        "vpc": "vpc",
    },
)
class CommonProjectProps:
    def __init__(
        self,
        *,
        allow_all_outbound: typing.Optional[bool] = None,
        badge: typing.Optional[bool] = None,
        build_spec: typing.Optional["BuildSpec"] = None,
        cache: typing.Optional["Cache"] = None,
        description: typing.Optional[str] = None,
        encryption_key: typing.Optional[aws_cdk.aws_kms.IKey] = None,
        environment: typing.Optional["BuildEnvironment"] = None,
        environment_variables: typing.Optional[
            typing.Mapping[str, "BuildEnvironmentVariable"]
        ] = None,
        file_system_locations: typing.Optional[
            typing.List["IFileSystemLocation"]
        ] = None,
        grant_report_group_permissions: typing.Optional[bool] = None,
        project_name: typing.Optional[str] = None,
        role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
        security_groups: typing.Optional[
            typing.List[aws_cdk.aws_ec2.ISecurityGroup]
        ] = None,
        subnet_selection: typing.Optional[aws_cdk.aws_ec2.SubnetSelection] = None,
        timeout: typing.Optional[aws_cdk.core.Duration] = None,
        vpc: typing.Optional[aws_cdk.aws_ec2.IVpc] = None,
    ) -> None:
        """
        :param allow_all_outbound: Whether to allow the CodeBuild to send all network traffic. If set to false, you must individually add traffic rules to allow the CodeBuild project to connect to network targets. Only used if 'vpc' is supplied. Default: true
        :param badge: Indicates whether AWS CodeBuild generates a publicly accessible URL for your project's build badge. For more information, see Build Badges Sample in the AWS CodeBuild User Guide. Default: false
        :param build_spec: Filename or contents of buildspec in JSON format. Default: - Empty buildspec.
        :param cache: Caching strategy to use. Default: Cache.none
        :param description: A description of the project. Use the description to identify the purpose of the project. Default: - No description.
        :param encryption_key: Encryption key to use to read and write artifacts. Default: - The AWS-managed CMK for Amazon Simple Storage Service (Amazon S3) is used.
        :param environment: Build environment to use for the build. Default: BuildEnvironment.LinuxBuildImage.STANDARD_1_0
        :param environment_variables: Additional environment variables to add to the build environment. Default: - No additional environment variables are specified.
        :param file_system_locations: An ProjectFileSystemLocation objects for a CodeBuild build project. A ProjectFileSystemLocation object specifies the identifier, location, mountOptions, mountPoint, and type of a file system created using Amazon Elastic File System. Default: - no file system locations
        :param grant_report_group_permissions: Add permissions to this project's role to create and use test report groups with name starting with the name of this project. That is the standard report group that gets created when a simple name (in contrast to an ARN) is used in the 'reports' section of the buildspec of this project. This is usually harmless, but you can turn these off if you don't plan on using test reports in this project. Default: true
        :param project_name: The physical, human-readable name of the CodeBuild Project. Default: - Name is automatically generated.
        :param role: Service Role to assume while running the build. Default: - A role will be created.
        :param security_groups: What security group to associate with the codebuild project's network interfaces. If no security group is identified, one will be created automatically. Only used if 'vpc' is supplied. Default: - Security group will be automatically created.
        :param subnet_selection: Where to place the network interfaces within the VPC. Only used if 'vpc' is supplied. Default: - All private subnets.
        :param timeout: The number of minutes after which AWS CodeBuild stops the build if it's not complete. For valid values, see the timeoutInMinutes field in the AWS CodeBuild User Guide. Default: Duration.hours(1)
        :param vpc: VPC network to place codebuild network interfaces. Specify this if the codebuild project needs to access resources in a VPC. Default: - No VPC is specified.
        """
        if isinstance(environment, dict):
            environment = BuildEnvironment(**environment)
        if isinstance(subnet_selection, dict):
            subnet_selection = aws_cdk.aws_ec2.SubnetSelection(**subnet_selection)
        self._values = {}
        if allow_all_outbound is not None:
            self._values["allow_all_outbound"] = allow_all_outbound
        if badge is not None:
            self._values["badge"] = badge
        if build_spec is not None:
            self._values["build_spec"] = build_spec
        if cache is not None:
            self._values["cache"] = cache
        if description is not None:
            self._values["description"] = description
        if encryption_key is not None:
            self._values["encryption_key"] = encryption_key
        if environment is not None:
            self._values["environment"] = environment
        if environment_variables is not None:
            self._values["environment_variables"] = environment_variables
        if file_system_locations is not None:
            self._values["file_system_locations"] = file_system_locations
        if grant_report_group_permissions is not None:
            self._values[
                "grant_report_group_permissions"
            ] = grant_report_group_permissions
        if project_name is not None:
            self._values["project_name"] = project_name
        if role is not None:
            self._values["role"] = role
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if subnet_selection is not None:
            self._values["subnet_selection"] = subnet_selection
        if timeout is not None:
            self._values["timeout"] = timeout
        if vpc is not None:
            self._values["vpc"] = vpc

    @builtins.property
    def allow_all_outbound(self) -> typing.Optional[bool]:
        """Whether to allow the CodeBuild to send all network traffic.

        If set to false, you must individually add traffic rules to allow the
        CodeBuild project to connect to network targets.

        Only used if 'vpc' is supplied.

        default
        :default: true
        """
        return self._values.get("allow_all_outbound")

    @builtins.property
    def badge(self) -> typing.Optional[bool]:
        """Indicates whether AWS CodeBuild generates a publicly accessible URL for your project's build badge.

        For more information, see Build Badges Sample
        in the AWS CodeBuild User Guide.

        default
        :default: false
        """
        return self._values.get("badge")

    @builtins.property
    def build_spec(self) -> typing.Optional["BuildSpec"]:
        """Filename or contents of buildspec in JSON format.

        default
        :default: - Empty buildspec.

        see
        :see: https://docs.aws.amazon.com/codebuild/latest/userguide/build-spec-ref.html#build-spec-ref-example
        """
        return self._values.get("build_spec")

    @builtins.property
    def cache(self) -> typing.Optional["Cache"]:
        """Caching strategy to use.

        default
        :default: Cache.none
        """
        return self._values.get("cache")

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """A description of the project.

        Use the description to identify the purpose
        of the project.

        default
        :default: - No description.
        """
        return self._values.get("description")

    @builtins.property
    def encryption_key(self) -> typing.Optional[aws_cdk.aws_kms.IKey]:
        """Encryption key to use to read and write artifacts.

        default
        :default: - The AWS-managed CMK for Amazon Simple Storage Service (Amazon S3) is used.
        """
        return self._values.get("encryption_key")

    @builtins.property
    def environment(self) -> typing.Optional["BuildEnvironment"]:
        """Build environment to use for the build.

        default
        :default: BuildEnvironment.LinuxBuildImage.STANDARD_1_0
        """
        return self._values.get("environment")

    @builtins.property
    def environment_variables(
        self,
    ) -> typing.Optional[typing.Mapping[str, "BuildEnvironmentVariable"]]:
        """Additional environment variables to add to the build environment.

        default
        :default: - No additional environment variables are specified.
        """
        return self._values.get("environment_variables")

    @builtins.property
    def file_system_locations(
        self,
    ) -> typing.Optional[typing.List["IFileSystemLocation"]]:
        """An  ProjectFileSystemLocation objects for a CodeBuild build project.

        A ProjectFileSystemLocation object specifies the identifier, location, mountOptions, mountPoint,
        and type of a file system created using Amazon Elastic File System.

        default
        :default: - no file system locations
        """
        return self._values.get("file_system_locations")

    @builtins.property
    def grant_report_group_permissions(self) -> typing.Optional[bool]:
        """Add permissions to this project's role to create and use test report groups with name starting with the name of this project.

        That is the standard report group that gets created when a simple name
        (in contrast to an ARN)
        is used in the 'reports' section of the buildspec of this project.
        This is usually harmless, but you can turn these off if you don't plan on using test
        reports in this project.

        default
        :default: true

        see
        :see: https://docs.aws.amazon.com/codebuild/latest/userguide/test-report-group-naming.html
        """
        return self._values.get("grant_report_group_permissions")

    @builtins.property
    def project_name(self) -> typing.Optional[str]:
        """The physical, human-readable name of the CodeBuild Project.

        default
        :default: - Name is automatically generated.
        """
        return self._values.get("project_name")

    @builtins.property
    def role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """Service Role to assume while running the build.

        default
        :default: - A role will be created.
        """
        return self._values.get("role")

    @builtins.property
    def security_groups(
        self,
    ) -> typing.Optional[typing.List[aws_cdk.aws_ec2.ISecurityGroup]]:
        """What security group to associate with the codebuild project's network interfaces.

        If no security group is identified, one will be created automatically.

        Only used if 'vpc' is supplied.

        default
        :default: - Security group will be automatically created.
        """
        return self._values.get("security_groups")

    @builtins.property
    def subnet_selection(self) -> typing.Optional[aws_cdk.aws_ec2.SubnetSelection]:
        """Where to place the network interfaces within the VPC.

        Only used if 'vpc' is supplied.

        default
        :default: - All private subnets.
        """
        return self._values.get("subnet_selection")

    @builtins.property
    def timeout(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The number of minutes after which AWS CodeBuild stops the build if it's not complete.

        For valid values, see the timeoutInMinutes field in the AWS
        CodeBuild User Guide.

        default
        :default: Duration.hours(1)
        """
        return self._values.get("timeout")

    @builtins.property
    def vpc(self) -> typing.Optional[aws_cdk.aws_ec2.IVpc]:
        """VPC network to place codebuild network interfaces.

        Specify this if the codebuild project needs to access resources in a VPC.

        default
        :default: - No VPC is specified.
        """
        return self._values.get("vpc")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CommonProjectProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-codebuild.ComputeType")
class ComputeType(enum.Enum):
    """Build machine compute type."""

    SMALL = "SMALL"
    MEDIUM = "MEDIUM"
    LARGE = "LARGE"
    X2_LARGE = "X2_LARGE"


@jsii.data_type(
    jsii_type="@aws-cdk/aws-codebuild.DockerImageOptions",
    jsii_struct_bases=[],
    name_mapping={"secrets_manager_credentials": "secretsManagerCredentials"},
)
class DockerImageOptions:
    def __init__(
        self,
        *,
        secrets_manager_credentials: typing.Optional[
            aws_cdk.aws_secretsmanager.ISecret
        ] = None,
    ) -> None:
        """The options when creating a CodeBuild Docker build image using {@link LinuxBuildImage.fromDockerRegistry} or {@link WindowsBuildImage.fromDockerRegistry}.

        :param secrets_manager_credentials: The credentials, stored in Secrets Manager, used for accessing the repository holding the image, if the repository is private. Default: no credentials will be used (we assume the repository is public)
        """
        self._values = {}
        if secrets_manager_credentials is not None:
            self._values["secrets_manager_credentials"] = secrets_manager_credentials

    @builtins.property
    def secrets_manager_credentials(
        self,
    ) -> typing.Optional[aws_cdk.aws_secretsmanager.ISecret]:
        """The credentials, stored in Secrets Manager, used for accessing the repository holding the image, if the repository is private.

        default
        :default: no credentials will be used (we assume the repository is public)
        """
        return self._values.get("secrets_manager_credentials")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DockerImageOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-codebuild.EfsFileSystemLocationProps",
    jsii_struct_bases=[],
    name_mapping={
        "identifier": "identifier",
        "location": "location",
        "mount_point": "mountPoint",
        "mount_options": "mountOptions",
    },
)
class EfsFileSystemLocationProps:
    def __init__(
        self,
        *,
        identifier: str,
        location: str,
        mount_point: str,
        mount_options: typing.Optional[str] = None,
    ) -> None:
        """Construction properties for {@link EfsFileSystemLocation}.

        :param identifier: The name used to access a file system created by Amazon EFS.
        :param location: A string that specifies the location of the file system, like Amazon EFS.
        :param mount_point: The location in the container where you mount the file system.
        :param mount_options: The mount options for a file system such as Amazon EFS. Default: 'nfsvers=4.1,rsize=1048576,wsize=1048576,hard,timeo=600,retrans=2'.
        """
        self._values = {
            "identifier": identifier,
            "location": location,
            "mount_point": mount_point,
        }
        if mount_options is not None:
            self._values["mount_options"] = mount_options

    @builtins.property
    def identifier(self) -> str:
        """The name used to access a file system created by Amazon EFS."""
        return self._values.get("identifier")

    @builtins.property
    def location(self) -> str:
        """A string that specifies the location of the file system, like Amazon EFS.

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            "fs-abcd1234.efs.us-west-2.amazonaws.com:/my-efs-mount-directory".
        """
        return self._values.get("location")

    @builtins.property
    def mount_point(self) -> str:
        """The location in the container where you mount the file system."""
        return self._values.get("mount_point")

    @builtins.property
    def mount_options(self) -> typing.Optional[str]:
        """The mount options for a file system such as Amazon EFS.

        default
        :default: 'nfsvers=4.1,rsize=1048576,wsize=1048576,hard,timeo=600,retrans=2'.
        """
        return self._values.get("mount_options")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EfsFileSystemLocationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-codebuild.EventAction")
class EventAction(enum.Enum):
    """The types of webhook event actions."""

    PUSH = "PUSH"
    """A push (of a branch, or a tag) to the repository."""
    PULL_REQUEST_CREATED = "PULL_REQUEST_CREATED"
    """Creating a Pull Request."""
    PULL_REQUEST_UPDATED = "PULL_REQUEST_UPDATED"
    """Updating a Pull Request."""
    PULL_REQUEST_MERGED = "PULL_REQUEST_MERGED"
    """Merging a Pull Request."""
    PULL_REQUEST_REOPENED = "PULL_REQUEST_REOPENED"
    """Re-opening a previously closed Pull Request.

    Note that this event is only supported for GitHub and GitHubEnterprise sources.
    """


@jsii.data_type(
    jsii_type="@aws-cdk/aws-codebuild.FileSystemConfig",
    jsii_struct_bases=[],
    name_mapping={"location": "location"},
)
class FileSystemConfig:
    def __init__(
        self, *, location: "CfnProject.ProjectFileSystemLocationProperty"
    ) -> None:
        """The type returned from {@link IFileSystemLocation#bind}.

        :param location: File system location wrapper property.
        """
        if isinstance(location, dict):
            location = CfnProject.ProjectFileSystemLocationProperty(**location)
        self._values = {
            "location": location,
        }

    @builtins.property
    def location(self) -> "CfnProject.ProjectFileSystemLocationProperty":
        """File system location wrapper property.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-projectfilesystemlocation.html
        """
        return self._values.get("location")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FileSystemConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FileSystemLocation(
    metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codebuild.FileSystemLocation"
):
    """FileSystemLocation provider definition for a CodeBuild Project."""

    def __init__(self) -> None:
        jsii.create(FileSystemLocation, self, [])

    @jsii.member(jsii_name="efs")
    @builtins.classmethod
    def efs(
        cls,
        *,
        identifier: str,
        location: str,
        mount_point: str,
        mount_options: typing.Optional[str] = None,
    ) -> "IFileSystemLocation":
        """EFS file system provider.

        :param identifier: The name used to access a file system created by Amazon EFS.
        :param location: A string that specifies the location of the file system, like Amazon EFS.
        :param mount_point: The location in the container where you mount the file system.
        :param mount_options: The mount options for a file system such as Amazon EFS. Default: 'nfsvers=4.1,rsize=1048576,wsize=1048576,hard,timeo=600,retrans=2'.
        """
        props = EfsFileSystemLocationProps(
            identifier=identifier,
            location=location,
            mount_point=mount_point,
            mount_options=mount_options,
        )

        return jsii.sinvoke(cls, "efs", [props])


class FilterGroup(
    metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codebuild.FilterGroup"
):
    """An object that represents a group of filter conditions for a webhook.

    Every condition in a given FilterGroup must be true in order for the whole group to be true.
    You construct instances of it by calling the {@link #inEventOf} static factory method,
    and then calling various ``andXyz`` instance methods to create modified instances of it
    (this class is immutable).

    You pass instances of this class to the ``webhookFilters`` property when constructing a source.
    """

    @jsii.member(jsii_name="inEventOf")
    @builtins.classmethod
    def in_event_of(cls, *actions: "EventAction") -> "FilterGroup":
        """Creates a new event FilterGroup that triggers on any of the provided actions.

        :param actions: the actions to trigger the webhook on.
        """
        return jsii.sinvoke(cls, "inEventOf", [*actions])

    @jsii.member(jsii_name="andActorAccountIs")
    def and_actor_account_is(self, pattern: str) -> "FilterGroup":
        """Create a new FilterGroup with an added condition: the account ID of the actor initiating the event must match the given pattern.

        :param pattern: a regular expression.
        """
        return jsii.invoke(self, "andActorAccountIs", [pattern])

    @jsii.member(jsii_name="andActorAccountIsNot")
    def and_actor_account_is_not(self, pattern: str) -> "FilterGroup":
        """Create a new FilterGroup with an added condition: the account ID of the actor initiating the event must not match the given pattern.

        :param pattern: a regular expression.
        """
        return jsii.invoke(self, "andActorAccountIsNot", [pattern])

    @jsii.member(jsii_name="andBaseBranchIs")
    def and_base_branch_is(self, branch_name: str) -> "FilterGroup":
        """Create a new FilterGroup with an added condition: the Pull Request that is the source of the event must target the given base branch.

        Note that you cannot use this method if this Group contains the ``PUSH`` event action.

        :param branch_name: the name of the branch (can be a regular expression).
        """
        return jsii.invoke(self, "andBaseBranchIs", [branch_name])

    @jsii.member(jsii_name="andBaseBranchIsNot")
    def and_base_branch_is_not(self, branch_name: str) -> "FilterGroup":
        """Create a new FilterGroup with an added condition: the Pull Request that is the source of the event must not target the given base branch.

        Note that you cannot use this method if this Group contains the ``PUSH`` event action.

        :param branch_name: the name of the branch (can be a regular expression).
        """
        return jsii.invoke(self, "andBaseBranchIsNot", [branch_name])

    @jsii.member(jsii_name="andBaseRefIs")
    def and_base_ref_is(self, pattern: str) -> "FilterGroup":
        """Create a new FilterGroup with an added condition: the Pull Request that is the source of the event must target the given Git reference.

        Note that you cannot use this method if this Group contains the ``PUSH`` event action.

        :param pattern: a regular expression.
        """
        return jsii.invoke(self, "andBaseRefIs", [pattern])

    @jsii.member(jsii_name="andBaseRefIsNot")
    def and_base_ref_is_not(self, pattern: str) -> "FilterGroup":
        """Create a new FilterGroup with an added condition: the Pull Request that is the source of the event must not target the given Git reference.

        Note that you cannot use this method if this Group contains the ``PUSH`` event action.

        :param pattern: a regular expression.
        """
        return jsii.invoke(self, "andBaseRefIsNot", [pattern])

    @jsii.member(jsii_name="andBranchIs")
    def and_branch_is(self, branch_name: str) -> "FilterGroup":
        """Create a new FilterGroup with an added condition: the event must affect the given branch.

        :param branch_name: the name of the branch (can be a regular expression).
        """
        return jsii.invoke(self, "andBranchIs", [branch_name])

    @jsii.member(jsii_name="andBranchIsNot")
    def and_branch_is_not(self, branch_name: str) -> "FilterGroup":
        """Create a new FilterGroup with an added condition: the event must not affect the given branch.

        :param branch_name: the name of the branch (can be a regular expression).
        """
        return jsii.invoke(self, "andBranchIsNot", [branch_name])

    @jsii.member(jsii_name="andFilePathIs")
    def and_file_path_is(self, pattern: str) -> "FilterGroup":
        """Create a new FilterGroup with an added condition: the push that is the source of the event must affect a file that matches the given pattern.

        Note that you can only use this method if this Group contains only the ``PUSH`` event action,
        and only for GitHub and GitHubEnterprise sources.

        :param pattern: a regular expression.
        """
        return jsii.invoke(self, "andFilePathIs", [pattern])

    @jsii.member(jsii_name="andFilePathIsNot")
    def and_file_path_is_not(self, pattern: str) -> "FilterGroup":
        """Create a new FilterGroup with an added condition: the push that is the source of the event must not affect a file that matches the given pattern.

        Note that you can only use this method if this Group contains only the ``PUSH`` event action,
        and only for GitHub and GitHubEnterprise sources.

        :param pattern: a regular expression.
        """
        return jsii.invoke(self, "andFilePathIsNot", [pattern])

    @jsii.member(jsii_name="andHeadRefIs")
    def and_head_ref_is(self, pattern: str) -> "FilterGroup":
        """Create a new FilterGroup with an added condition: the event must affect a Git reference (ie., a branch or a tag) that matches the given pattern.

        :param pattern: a regular expression.
        """
        return jsii.invoke(self, "andHeadRefIs", [pattern])

    @jsii.member(jsii_name="andHeadRefIsNot")
    def and_head_ref_is_not(self, pattern: str) -> "FilterGroup":
        """Create a new FilterGroup with an added condition: the event must not affect a Git reference (ie., a branch or a tag) that matches the given pattern.

        :param pattern: a regular expression.
        """
        return jsii.invoke(self, "andHeadRefIsNot", [pattern])

    @jsii.member(jsii_name="andTagIs")
    def and_tag_is(self, tag_name: str) -> "FilterGroup":
        """Create a new FilterGroup with an added condition: the event must affect the given tag.

        :param tag_name: the name of the tag (can be a regular expression).
        """
        return jsii.invoke(self, "andTagIs", [tag_name])

    @jsii.member(jsii_name="andTagIsNot")
    def and_tag_is_not(self, tag_name: str) -> "FilterGroup":
        """Create a new FilterGroup with an added condition: the event must not affect the given tag.

        :param tag_name: the name of the tag (can be a regular expression).
        """
        return jsii.invoke(self, "andTagIsNot", [tag_name])


class GitHubEnterpriseSourceCredentials(
    aws_cdk.core.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-codebuild.GitHubEnterpriseSourceCredentials",
):
    """The source credentials used when contacting the GitHub Enterprise API.

    **Note**: CodeBuild only allows a single credential for GitHub Enterprise
    to be saved in a given AWS account in a given region -
    any attempt to add more than one will result in an error.

    resource:
    :resource:: AWS::CodeBuild::SourceCredential
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: str,
        *,
        access_token: aws_cdk.core.SecretValue,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param access_token: The personal access token to use when contacting the instance of the GitHub Enterprise API.
        """
        props = GitHubEnterpriseSourceCredentialsProps(access_token=access_token)

        jsii.create(GitHubEnterpriseSourceCredentials, self, [scope, id, props])


@jsii.data_type(
    jsii_type="@aws-cdk/aws-codebuild.GitHubEnterpriseSourceCredentialsProps",
    jsii_struct_bases=[],
    name_mapping={"access_token": "accessToken"},
)
class GitHubEnterpriseSourceCredentialsProps:
    def __init__(self, *, access_token: aws_cdk.core.SecretValue) -> None:
        """Creation properties for {@link GitHubEnterpriseSourceCredentials}.

        :param access_token: The personal access token to use when contacting the instance of the GitHub Enterprise API.
        """
        self._values = {
            "access_token": access_token,
        }

    @builtins.property
    def access_token(self) -> aws_cdk.core.SecretValue:
        """The personal access token to use when contacting the instance of the GitHub Enterprise API."""
        return self._values.get("access_token")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GitHubEnterpriseSourceCredentialsProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GitHubSourceCredentials(
    aws_cdk.core.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-codebuild.GitHubSourceCredentials",
):
    """The source credentials used when contacting the GitHub API.

    **Note**: CodeBuild only allows a single credential for GitHub
    to be saved in a given AWS account in a given region -
    any attempt to add more than one will result in an error.

    resource:
    :resource:: AWS::CodeBuild::SourceCredential
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: str,
        *,
        access_token: aws_cdk.core.SecretValue,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param access_token: The personal access token to use when contacting the GitHub API.
        """
        props = GitHubSourceCredentialsProps(access_token=access_token)

        jsii.create(GitHubSourceCredentials, self, [scope, id, props])


@jsii.data_type(
    jsii_type="@aws-cdk/aws-codebuild.GitHubSourceCredentialsProps",
    jsii_struct_bases=[],
    name_mapping={"access_token": "accessToken"},
)
class GitHubSourceCredentialsProps:
    def __init__(self, *, access_token: aws_cdk.core.SecretValue) -> None:
        """Creation properties for {@link GitHubSourceCredentials}.

        :param access_token: The personal access token to use when contacting the GitHub API.
        """
        self._values = {
            "access_token": access_token,
        }

    @builtins.property
    def access_token(self) -> aws_cdk.core.SecretValue:
        """The personal access token to use when contacting the GitHub API."""
        return self._values.get("access_token")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GitHubSourceCredentialsProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="@aws-cdk/aws-codebuild.IArtifacts")
class IArtifacts(jsii.compat.Protocol):
    """The abstract interface of a CodeBuild build output.

    Implemented by {@link Artifacts}.
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IArtifactsProxy

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> str:
        """The CodeBuild type of this artifact."""
        ...

    @builtins.property
    @jsii.member(jsii_name="identifier")
    def identifier(self) -> typing.Optional[str]:
        """The artifact identifier.

        This property is required on secondary artifacts.
        """
        ...

    @jsii.member(jsii_name="bind")
    def bind(
        self, scope: aws_cdk.core.Construct, project: "IProject"
    ) -> "ArtifactsConfig":
        """Callback when an Artifacts class is used in a CodeBuild Project.

        :param scope: a root Construct that allows creating new Constructs.
        :param project: the Project this Artifacts is used in.
        """
        ...


class _IArtifactsProxy:
    """The abstract interface of a CodeBuild build output.

    Implemented by {@link Artifacts}.
    """

    __jsii_type__ = "@aws-cdk/aws-codebuild.IArtifacts"

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> str:
        """The CodeBuild type of this artifact."""
        return jsii.get(self, "type")

    @builtins.property
    @jsii.member(jsii_name="identifier")
    def identifier(self) -> typing.Optional[str]:
        """The artifact identifier.

        This property is required on secondary artifacts.
        """
        return jsii.get(self, "identifier")

    @jsii.member(jsii_name="bind")
    def bind(
        self, scope: aws_cdk.core.Construct, project: "IProject"
    ) -> "ArtifactsConfig":
        """Callback when an Artifacts class is used in a CodeBuild Project.

        :param scope: a root Construct that allows creating new Constructs.
        :param project: the Project this Artifacts is used in.
        """
        return jsii.invoke(self, "bind", [scope, project])


@jsii.interface(jsii_type="@aws-cdk/aws-codebuild.IBuildImage")
class IBuildImage(jsii.compat.Protocol):
    """Represents a Docker image used for the CodeBuild Project builds.

    Use the concrete subclasses, either:
    {@link LinuxBuildImage} or {@link WindowsBuildImage}.
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IBuildImageProxy

    @builtins.property
    @jsii.member(jsii_name="defaultComputeType")
    def default_compute_type(self) -> "ComputeType":
        """The default {@link ComputeType} to use with this image, if one was not specified in {@link BuildEnvironment#computeType} explicitly."""
        ...

    @builtins.property
    @jsii.member(jsii_name="imageId")
    def image_id(self) -> str:
        """The Docker image identifier that the build environment uses.

        see
        :see: https://docs.aws.amazon.com/codebuild/latest/userguide/build-env-ref-available.html
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> str:
        """The type of build environment."""
        ...

    @builtins.property
    @jsii.member(jsii_name="imagePullPrincipalType")
    def image_pull_principal_type(self) -> typing.Optional["ImagePullPrincipalType"]:
        """The type of principal that CodeBuild will use to pull this build Docker image.

        default
        :default: ImagePullPrincipalType.SERVICE_ROLE
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="repository")
    def repository(self) -> typing.Optional[aws_cdk.aws_ecr.IRepository]:
        """An optional ECR repository that the image is hosted in.

        default
        :default: no repository
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="secretsManagerCredentials")
    def secrets_manager_credentials(
        self,
    ) -> typing.Optional[aws_cdk.aws_secretsmanager.ISecret]:
        """The secretsManagerCredentials for access to a private registry.

        default
        :default: no credentials will be used
        """
        ...

    @jsii.member(jsii_name="runScriptBuildspec")
    def run_script_buildspec(self, entrypoint: str) -> "BuildSpec":
        """Make a buildspec to run the indicated script.

        :param entrypoint: -
        """
        ...

    @jsii.member(jsii_name="validate")
    def validate(
        self,
        *,
        build_image: typing.Optional["IBuildImage"] = None,
        compute_type: typing.Optional["ComputeType"] = None,
        environment_variables: typing.Optional[
            typing.Mapping[str, "BuildEnvironmentVariable"]
        ] = None,
        privileged: typing.Optional[bool] = None,
    ) -> typing.List[str]:
        """Allows the image a chance to validate whether the passed configuration is correct.

        :param build_image: The image used for the builds. Default: LinuxBuildImage.STANDARD_1_0
        :param compute_type: The type of compute to use for this build. See the {@link ComputeType} enum for the possible values. Default: taken from {@link #buildImage#defaultComputeType}
        :param environment_variables: The environment variables that your builds can use.
        :param privileged: Indicates how the project builds Docker images. Specify true to enable running the Docker daemon inside a Docker container. This value must be set to true only if this build project will be used to build Docker images, and the specified build environment image is not one provided by AWS CodeBuild with Docker support. Otherwise, all associated builds that attempt to interact with the Docker daemon will fail. Default: false
        """
        ...


class _IBuildImageProxy:
    """Represents a Docker image used for the CodeBuild Project builds.

    Use the concrete subclasses, either:
    {@link LinuxBuildImage} or {@link WindowsBuildImage}.
    """

    __jsii_type__ = "@aws-cdk/aws-codebuild.IBuildImage"

    @builtins.property
    @jsii.member(jsii_name="defaultComputeType")
    def default_compute_type(self) -> "ComputeType":
        """The default {@link ComputeType} to use with this image, if one was not specified in {@link BuildEnvironment#computeType} explicitly."""
        return jsii.get(self, "defaultComputeType")

    @builtins.property
    @jsii.member(jsii_name="imageId")
    def image_id(self) -> str:
        """The Docker image identifier that the build environment uses.

        see
        :see: https://docs.aws.amazon.com/codebuild/latest/userguide/build-env-ref-available.html
        """
        return jsii.get(self, "imageId")

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> str:
        """The type of build environment."""
        return jsii.get(self, "type")

    @builtins.property
    @jsii.member(jsii_name="imagePullPrincipalType")
    def image_pull_principal_type(self) -> typing.Optional["ImagePullPrincipalType"]:
        """The type of principal that CodeBuild will use to pull this build Docker image.

        default
        :default: ImagePullPrincipalType.SERVICE_ROLE
        """
        return jsii.get(self, "imagePullPrincipalType")

    @builtins.property
    @jsii.member(jsii_name="repository")
    def repository(self) -> typing.Optional[aws_cdk.aws_ecr.IRepository]:
        """An optional ECR repository that the image is hosted in.

        default
        :default: no repository
        """
        return jsii.get(self, "repository")

    @builtins.property
    @jsii.member(jsii_name="secretsManagerCredentials")
    def secrets_manager_credentials(
        self,
    ) -> typing.Optional[aws_cdk.aws_secretsmanager.ISecret]:
        """The secretsManagerCredentials for access to a private registry.

        default
        :default: no credentials will be used
        """
        return jsii.get(self, "secretsManagerCredentials")

    @jsii.member(jsii_name="runScriptBuildspec")
    def run_script_buildspec(self, entrypoint: str) -> "BuildSpec":
        """Make a buildspec to run the indicated script.

        :param entrypoint: -
        """
        return jsii.invoke(self, "runScriptBuildspec", [entrypoint])

    @jsii.member(jsii_name="validate")
    def validate(
        self,
        *,
        build_image: typing.Optional["IBuildImage"] = None,
        compute_type: typing.Optional["ComputeType"] = None,
        environment_variables: typing.Optional[
            typing.Mapping[str, "BuildEnvironmentVariable"]
        ] = None,
        privileged: typing.Optional[bool] = None,
    ) -> typing.List[str]:
        """Allows the image a chance to validate whether the passed configuration is correct.

        :param build_image: The image used for the builds. Default: LinuxBuildImage.STANDARD_1_0
        :param compute_type: The type of compute to use for this build. See the {@link ComputeType} enum for the possible values. Default: taken from {@link #buildImage#defaultComputeType}
        :param environment_variables: The environment variables that your builds can use.
        :param privileged: Indicates how the project builds Docker images. Specify true to enable running the Docker daemon inside a Docker container. This value must be set to true only if this build project will be used to build Docker images, and the specified build environment image is not one provided by AWS CodeBuild with Docker support. Otherwise, all associated builds that attempt to interact with the Docker daemon will fail. Default: false
        """
        build_environment = BuildEnvironment(
            build_image=build_image,
            compute_type=compute_type,
            environment_variables=environment_variables,
            privileged=privileged,
        )

        return jsii.invoke(self, "validate", [build_environment])


@jsii.interface(jsii_type="@aws-cdk/aws-codebuild.IFileSystemLocation")
class IFileSystemLocation(jsii.compat.Protocol):
    """The interface of a CodeBuild FileSystemLocation.

    Implemented by {@link EfsFileSystemLocation}.
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IFileSystemLocationProxy

    @jsii.member(jsii_name="bind")
    def bind(
        self, scope: aws_cdk.core.Construct, project: "IProject"
    ) -> "FileSystemConfig":
        """Called by the project when a file system is added so it can perform binding operations on this file system location.

        :param scope: -
        :param project: -
        """
        ...


class _IFileSystemLocationProxy:
    """The interface of a CodeBuild FileSystemLocation.

    Implemented by {@link EfsFileSystemLocation}.
    """

    __jsii_type__ = "@aws-cdk/aws-codebuild.IFileSystemLocation"

    @jsii.member(jsii_name="bind")
    def bind(
        self, scope: aws_cdk.core.Construct, project: "IProject"
    ) -> "FileSystemConfig":
        """Called by the project when a file system is added so it can perform binding operations on this file system location.

        :param scope: -
        :param project: -
        """
        return jsii.invoke(self, "bind", [scope, project])


@jsii.interface(jsii_type="@aws-cdk/aws-codebuild.IProject")
class IProject(
    aws_cdk.core.IResource,
    aws_cdk.aws_iam.IGrantable,
    aws_cdk.aws_ec2.IConnectable,
    jsii.compat.Protocol,
):
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IProjectProxy

    @builtins.property
    @jsii.member(jsii_name="projectArn")
    def project_arn(self) -> str:
        """The ARN of this Project.

        attribute:
        :attribute:: true
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="projectName")
    def project_name(self) -> str:
        """The human-visible name of this Project.

        attribute:
        :attribute:: true
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """The IAM service Role of this Project.

        Undefined for imported Projects.
        """
        ...

    @jsii.member(jsii_name="addToRolePolicy")
    def add_to_role_policy(
        self, policy_statement: aws_cdk.aws_iam.PolicyStatement
    ) -> None:
        """
        :param policy_statement: -
        """
        ...

    @jsii.member(jsii_name="metric")
    def metric(
        self,
        metric_name: str,
        *,
        account: typing.Optional[str] = None,
        color: typing.Optional[str] = None,
        dimensions: typing.Optional[typing.Mapping[str, typing.Any]] = None,
        label: typing.Optional[str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[str] = None,
        statistic: typing.Optional[str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        """
        :param metric_name: The name of the metric.
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        return
        :return: a CloudWatch metric associated with this build project.
        """
        ...

    @jsii.member(jsii_name="metricBuilds")
    def metric_builds(
        self,
        *,
        account: typing.Optional[str] = None,
        color: typing.Optional[str] = None,
        dimensions: typing.Optional[typing.Mapping[str, typing.Any]] = None,
        label: typing.Optional[str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[str] = None,
        statistic: typing.Optional[str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        """Measures the number of builds triggered.

        Units: Count

        Valid CloudWatch statistics: Sum

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        default
        :default: sum over 5 minutes
        """
        ...

    @jsii.member(jsii_name="metricDuration")
    def metric_duration(
        self,
        *,
        account: typing.Optional[str] = None,
        color: typing.Optional[str] = None,
        dimensions: typing.Optional[typing.Mapping[str, typing.Any]] = None,
        label: typing.Optional[str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[str] = None,
        statistic: typing.Optional[str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        """Measures the duration of all builds over time.

        Units: Seconds

        Valid CloudWatch statistics: Average (recommended), Maximum, Minimum

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        default
        :default: average over 5 minutes
        """
        ...

    @jsii.member(jsii_name="metricFailedBuilds")
    def metric_failed_builds(
        self,
        *,
        account: typing.Optional[str] = None,
        color: typing.Optional[str] = None,
        dimensions: typing.Optional[typing.Mapping[str, typing.Any]] = None,
        label: typing.Optional[str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[str] = None,
        statistic: typing.Optional[str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        """Measures the number of builds that failed because of client error or because of a timeout.

        Units: Count

        Valid CloudWatch statistics: Sum

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        default
        :default: sum over 5 minutes
        """
        ...

    @jsii.member(jsii_name="metricSucceededBuilds")
    def metric_succeeded_builds(
        self,
        *,
        account: typing.Optional[str] = None,
        color: typing.Optional[str] = None,
        dimensions: typing.Optional[typing.Mapping[str, typing.Any]] = None,
        label: typing.Optional[str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[str] = None,
        statistic: typing.Optional[str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        """Measures the number of successful builds.

        Units: Count

        Valid CloudWatch statistics: Sum

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        default
        :default: sum over 5 minutes
        """
        ...

    @jsii.member(jsii_name="onBuildFailed")
    def on_build_failed(
        self,
        id: str,
        *,
        description: typing.Optional[str] = None,
        event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern] = None,
        rule_name: typing.Optional[str] = None,
        target: typing.Optional[aws_cdk.aws_events.IRuleTarget] = None,
    ) -> aws_cdk.aws_events.Rule:
        """Defines an event rule which triggers when a build fails.

        :param id: -
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        """
        ...

    @jsii.member(jsii_name="onBuildStarted")
    def on_build_started(
        self,
        id: str,
        *,
        description: typing.Optional[str] = None,
        event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern] = None,
        rule_name: typing.Optional[str] = None,
        target: typing.Optional[aws_cdk.aws_events.IRuleTarget] = None,
    ) -> aws_cdk.aws_events.Rule:
        """Defines an event rule which triggers when a build starts.

        :param id: -
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        """
        ...

    @jsii.member(jsii_name="onBuildSucceeded")
    def on_build_succeeded(
        self,
        id: str,
        *,
        description: typing.Optional[str] = None,
        event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern] = None,
        rule_name: typing.Optional[str] = None,
        target: typing.Optional[aws_cdk.aws_events.IRuleTarget] = None,
    ) -> aws_cdk.aws_events.Rule:
        """Defines an event rule which triggers when a build completes successfully.

        :param id: -
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        """
        ...

    @jsii.member(jsii_name="onEvent")
    def on_event(
        self,
        id: str,
        *,
        description: typing.Optional[str] = None,
        event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern] = None,
        rule_name: typing.Optional[str] = None,
        target: typing.Optional[aws_cdk.aws_events.IRuleTarget] = None,
    ) -> aws_cdk.aws_events.Rule:
        """Defines a CloudWatch event rule triggered when something happens with this project.

        :param id: -
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        see
        :see: https://docs.aws.amazon.com/codebuild/latest/userguide/sample-build-notifications.html
        """
        ...

    @jsii.member(jsii_name="onPhaseChange")
    def on_phase_change(
        self,
        id: str,
        *,
        description: typing.Optional[str] = None,
        event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern] = None,
        rule_name: typing.Optional[str] = None,
        target: typing.Optional[aws_cdk.aws_events.IRuleTarget] = None,
    ) -> aws_cdk.aws_events.Rule:
        """Defines a CloudWatch event rule that triggers upon phase change of this build project.

        :param id: -
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        see
        :see: https://docs.aws.amazon.com/codebuild/latest/userguide/sample-build-notifications.html
        """
        ...

    @jsii.member(jsii_name="onStateChange")
    def on_state_change(
        self,
        id: str,
        *,
        description: typing.Optional[str] = None,
        event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern] = None,
        rule_name: typing.Optional[str] = None,
        target: typing.Optional[aws_cdk.aws_events.IRuleTarget] = None,
    ) -> aws_cdk.aws_events.Rule:
        """Defines a CloudWatch event rule triggered when the build project state changes.

        You can filter specific build status events using an event
        pattern filter on the ``build-status`` detail field::

           const rule = project.onStateChange('OnBuildStarted', { target });
           rule.addEventPattern({
             detail: {
               'build-status': [
                 "IN_PROGRESS",
                 "SUCCEEDED",
                 "FAILED",
                 "STOPPED"
               ]
             }
           });

        You can also use the methods ``onBuildFailed`` and ``onBuildSucceeded`` to define rules for
        these specific state changes.

        To access fields from the event in the event target input,
        use the static fields on the ``StateChangeEvent`` class.

        :param id: -
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        see
        :see: https://docs.aws.amazon.com/codebuild/latest/userguide/sample-build-notifications.html
        """
        ...


class _IProjectProxy(
    jsii.proxy_for(aws_cdk.core.IResource),
    jsii.proxy_for(aws_cdk.aws_iam.IGrantable),
    jsii.proxy_for(aws_cdk.aws_ec2.IConnectable),
):
    __jsii_type__ = "@aws-cdk/aws-codebuild.IProject"

    @builtins.property
    @jsii.member(jsii_name="projectArn")
    def project_arn(self) -> str:
        """The ARN of this Project.

        attribute:
        :attribute:: true
        """
        return jsii.get(self, "projectArn")

    @builtins.property
    @jsii.member(jsii_name="projectName")
    def project_name(self) -> str:
        """The human-visible name of this Project.

        attribute:
        :attribute:: true
        """
        return jsii.get(self, "projectName")

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """The IAM service Role of this Project.

        Undefined for imported Projects.
        """
        return jsii.get(self, "role")

    @jsii.member(jsii_name="addToRolePolicy")
    def add_to_role_policy(
        self, policy_statement: aws_cdk.aws_iam.PolicyStatement
    ) -> None:
        """
        :param policy_statement: -
        """
        return jsii.invoke(self, "addToRolePolicy", [policy_statement])

    @jsii.member(jsii_name="metric")
    def metric(
        self,
        metric_name: str,
        *,
        account: typing.Optional[str] = None,
        color: typing.Optional[str] = None,
        dimensions: typing.Optional[typing.Mapping[str, typing.Any]] = None,
        label: typing.Optional[str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[str] = None,
        statistic: typing.Optional[str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        """
        :param metric_name: The name of the metric.
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        return
        :return: a CloudWatch metric associated with this build project.
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metric", [metric_name, props])

    @jsii.member(jsii_name="metricBuilds")
    def metric_builds(
        self,
        *,
        account: typing.Optional[str] = None,
        color: typing.Optional[str] = None,
        dimensions: typing.Optional[typing.Mapping[str, typing.Any]] = None,
        label: typing.Optional[str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[str] = None,
        statistic: typing.Optional[str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        """Measures the number of builds triggered.

        Units: Count

        Valid CloudWatch statistics: Sum

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        default
        :default: sum over 5 minutes
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metricBuilds", [props])

    @jsii.member(jsii_name="metricDuration")
    def metric_duration(
        self,
        *,
        account: typing.Optional[str] = None,
        color: typing.Optional[str] = None,
        dimensions: typing.Optional[typing.Mapping[str, typing.Any]] = None,
        label: typing.Optional[str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[str] = None,
        statistic: typing.Optional[str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        """Measures the duration of all builds over time.

        Units: Seconds

        Valid CloudWatch statistics: Average (recommended), Maximum, Minimum

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        default
        :default: average over 5 minutes
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metricDuration", [props])

    @jsii.member(jsii_name="metricFailedBuilds")
    def metric_failed_builds(
        self,
        *,
        account: typing.Optional[str] = None,
        color: typing.Optional[str] = None,
        dimensions: typing.Optional[typing.Mapping[str, typing.Any]] = None,
        label: typing.Optional[str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[str] = None,
        statistic: typing.Optional[str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        """Measures the number of builds that failed because of client error or because of a timeout.

        Units: Count

        Valid CloudWatch statistics: Sum

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        default
        :default: sum over 5 minutes
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metricFailedBuilds", [props])

    @jsii.member(jsii_name="metricSucceededBuilds")
    def metric_succeeded_builds(
        self,
        *,
        account: typing.Optional[str] = None,
        color: typing.Optional[str] = None,
        dimensions: typing.Optional[typing.Mapping[str, typing.Any]] = None,
        label: typing.Optional[str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[str] = None,
        statistic: typing.Optional[str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        """Measures the number of successful builds.

        Units: Count

        Valid CloudWatch statistics: Sum

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        default
        :default: sum over 5 minutes
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metricSucceededBuilds", [props])

    @jsii.member(jsii_name="onBuildFailed")
    def on_build_failed(
        self,
        id: str,
        *,
        description: typing.Optional[str] = None,
        event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern] = None,
        rule_name: typing.Optional[str] = None,
        target: typing.Optional[aws_cdk.aws_events.IRuleTarget] = None,
    ) -> aws_cdk.aws_events.Rule:
        """Defines an event rule which triggers when a build fails.

        :param id: -
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        """
        options = aws_cdk.aws_events.OnEventOptions(
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
            target=target,
        )

        return jsii.invoke(self, "onBuildFailed", [id, options])

    @jsii.member(jsii_name="onBuildStarted")
    def on_build_started(
        self,
        id: str,
        *,
        description: typing.Optional[str] = None,
        event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern] = None,
        rule_name: typing.Optional[str] = None,
        target: typing.Optional[aws_cdk.aws_events.IRuleTarget] = None,
    ) -> aws_cdk.aws_events.Rule:
        """Defines an event rule which triggers when a build starts.

        :param id: -
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        """
        options = aws_cdk.aws_events.OnEventOptions(
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
            target=target,
        )

        return jsii.invoke(self, "onBuildStarted", [id, options])

    @jsii.member(jsii_name="onBuildSucceeded")
    def on_build_succeeded(
        self,
        id: str,
        *,
        description: typing.Optional[str] = None,
        event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern] = None,
        rule_name: typing.Optional[str] = None,
        target: typing.Optional[aws_cdk.aws_events.IRuleTarget] = None,
    ) -> aws_cdk.aws_events.Rule:
        """Defines an event rule which triggers when a build completes successfully.

        :param id: -
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        """
        options = aws_cdk.aws_events.OnEventOptions(
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
            target=target,
        )

        return jsii.invoke(self, "onBuildSucceeded", [id, options])

    @jsii.member(jsii_name="onEvent")
    def on_event(
        self,
        id: str,
        *,
        description: typing.Optional[str] = None,
        event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern] = None,
        rule_name: typing.Optional[str] = None,
        target: typing.Optional[aws_cdk.aws_events.IRuleTarget] = None,
    ) -> aws_cdk.aws_events.Rule:
        """Defines a CloudWatch event rule triggered when something happens with this project.

        :param id: -
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        see
        :see: https://docs.aws.amazon.com/codebuild/latest/userguide/sample-build-notifications.html
        """
        options = aws_cdk.aws_events.OnEventOptions(
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
            target=target,
        )

        return jsii.invoke(self, "onEvent", [id, options])

    @jsii.member(jsii_name="onPhaseChange")
    def on_phase_change(
        self,
        id: str,
        *,
        description: typing.Optional[str] = None,
        event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern] = None,
        rule_name: typing.Optional[str] = None,
        target: typing.Optional[aws_cdk.aws_events.IRuleTarget] = None,
    ) -> aws_cdk.aws_events.Rule:
        """Defines a CloudWatch event rule that triggers upon phase change of this build project.

        :param id: -
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        see
        :see: https://docs.aws.amazon.com/codebuild/latest/userguide/sample-build-notifications.html
        """
        options = aws_cdk.aws_events.OnEventOptions(
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
            target=target,
        )

        return jsii.invoke(self, "onPhaseChange", [id, options])

    @jsii.member(jsii_name="onStateChange")
    def on_state_change(
        self,
        id: str,
        *,
        description: typing.Optional[str] = None,
        event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern] = None,
        rule_name: typing.Optional[str] = None,
        target: typing.Optional[aws_cdk.aws_events.IRuleTarget] = None,
    ) -> aws_cdk.aws_events.Rule:
        """Defines a CloudWatch event rule triggered when the build project state changes.

        You can filter specific build status events using an event
        pattern filter on the ``build-status`` detail field::

           const rule = project.onStateChange('OnBuildStarted', { target });
           rule.addEventPattern({
             detail: {
               'build-status': [
                 "IN_PROGRESS",
                 "SUCCEEDED",
                 "FAILED",
                 "STOPPED"
               ]
             }
           });

        You can also use the methods ``onBuildFailed`` and ``onBuildSucceeded`` to define rules for
        these specific state changes.

        To access fields from the event in the event target input,
        use the static fields on the ``StateChangeEvent`` class.

        :param id: -
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        see
        :see: https://docs.aws.amazon.com/codebuild/latest/userguide/sample-build-notifications.html
        """
        options = aws_cdk.aws_events.OnEventOptions(
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
            target=target,
        )

        return jsii.invoke(self, "onStateChange", [id, options])


@jsii.interface(jsii_type="@aws-cdk/aws-codebuild.IReportGroup")
class IReportGroup(aws_cdk.core.IResource, jsii.compat.Protocol):
    """The interface representing the ReportGroup resource - either an existing one, imported using the {@link ReportGroup.fromReportGroupName} method, or a new one, created with the {@link ReportGroup} class."""

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IReportGroupProxy

    @builtins.property
    @jsii.member(jsii_name="reportGroupArn")
    def report_group_arn(self) -> str:
        """The ARN of the ReportGroup.

        attribute:
        :attribute:: true
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="reportGroupName")
    def report_group_name(self) -> str:
        """The name of the ReportGroup.

        attribute:
        :attribute:: true
        """
        ...

    @jsii.member(jsii_name="grantWrite")
    def grant_write(
        self, identity: aws_cdk.aws_iam.IGrantable
    ) -> aws_cdk.aws_iam.Grant:
        """Grants the given entity permissions to write (that is, upload reports to) this report group.

        :param identity: -
        """
        ...


class _IReportGroupProxy(jsii.proxy_for(aws_cdk.core.IResource)):
    """The interface representing the ReportGroup resource - either an existing one, imported using the {@link ReportGroup.fromReportGroupName} method, or a new one, created with the {@link ReportGroup} class."""

    __jsii_type__ = "@aws-cdk/aws-codebuild.IReportGroup"

    @builtins.property
    @jsii.member(jsii_name="reportGroupArn")
    def report_group_arn(self) -> str:
        """The ARN of the ReportGroup.

        attribute:
        :attribute:: true
        """
        return jsii.get(self, "reportGroupArn")

    @builtins.property
    @jsii.member(jsii_name="reportGroupName")
    def report_group_name(self) -> str:
        """The name of the ReportGroup.

        attribute:
        :attribute:: true
        """
        return jsii.get(self, "reportGroupName")

    @jsii.member(jsii_name="grantWrite")
    def grant_write(
        self, identity: aws_cdk.aws_iam.IGrantable
    ) -> aws_cdk.aws_iam.Grant:
        """Grants the given entity permissions to write (that is, upload reports to) this report group.

        :param identity: -
        """
        return jsii.invoke(self, "grantWrite", [identity])


@jsii.interface(jsii_type="@aws-cdk/aws-codebuild.ISource")
class ISource(jsii.compat.Protocol):
    """The abstract interface of a CodeBuild source.

    Implemented by {@link Source}.
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _ISourceProxy

    @builtins.property
    @jsii.member(jsii_name="badgeSupported")
    def badge_supported(self) -> bool:
        ...

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> str:
        ...

    @builtins.property
    @jsii.member(jsii_name="identifier")
    def identifier(self) -> typing.Optional[str]:
        ...

    @jsii.member(jsii_name="bind")
    def bind(
        self, scope: aws_cdk.core.Construct, project: "IProject"
    ) -> "SourceConfig":
        """
        :param scope: -
        :param project: -
        """
        ...


class _ISourceProxy:
    """The abstract interface of a CodeBuild source.

    Implemented by {@link Source}.
    """

    __jsii_type__ = "@aws-cdk/aws-codebuild.ISource"

    @builtins.property
    @jsii.member(jsii_name="badgeSupported")
    def badge_supported(self) -> bool:
        return jsii.get(self, "badgeSupported")

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> str:
        return jsii.get(self, "type")

    @builtins.property
    @jsii.member(jsii_name="identifier")
    def identifier(self) -> typing.Optional[str]:
        return jsii.get(self, "identifier")

    @jsii.member(jsii_name="bind")
    def bind(
        self, scope: aws_cdk.core.Construct, project: "IProject"
    ) -> "SourceConfig":
        """
        :param scope: -
        :param project: -
        """
        return jsii.invoke(self, "bind", [scope, project])


@jsii.enum(jsii_type="@aws-cdk/aws-codebuild.ImagePullPrincipalType")
class ImagePullPrincipalType(enum.Enum):
    """The type of principal CodeBuild will use to pull your build Docker image."""

    CODEBUILD = "CODEBUILD"
    """CODEBUILD specifies that CodeBuild uses its own identity when pulling the image.

    This means the resource policy of the ECR repository that hosts the image will be modified to trust
    CodeBuild's service principal.
    This is the required principal type when using CodeBuild's pre-defined images.
    """
    SERVICE_ROLE = "SERVICE_ROLE"
    """SERVICE_ROLE specifies that AWS CodeBuild uses the project's role when pulling the image.

    The role will be granted pull permissions on the ECR repository hosting the image.
    """


@jsii.implements(IBuildImage)
class LinuxBuildImage(
    metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codebuild.LinuxBuildImage"
):
    """A CodeBuild image running Linux.

    This class has a bunch of public constants that represent the most popular images.

    You can also specify a custom image using one of the static methods:

    - LinuxBuildImage.fromDockerRegistry(image[, { secretsManagerCredentials }])
    - LinuxBuildImage.fromEcrRepository(repo[, tag])
    - LinuxBuildImage.fromAsset(parent, id, props)

    see
    :see: https://docs.aws.amazon.com/codebuild/latest/userguide/build-env-ref-available.html
    """

    @jsii.member(jsii_name="fromAsset")
    @builtins.classmethod
    def from_asset(
        cls,
        scope: aws_cdk.core.Construct,
        id: str,
        *,
        directory: str,
        build_args: typing.Optional[typing.Mapping[str, str]] = None,
        file: typing.Optional[str] = None,
        repository_name: typing.Optional[str] = None,
        target: typing.Optional[str] = None,
        extra_hash: typing.Optional[str] = None,
        exclude: typing.Optional[typing.List[str]] = None,
        follow: typing.Optional[aws_cdk.assets.FollowMode] = None,
    ) -> "IBuildImage":
        """Uses an Docker image asset as a Linux build image.

        :param scope: -
        :param id: -
        :param directory: The directory where the Dockerfile is stored.
        :param build_args: Build args to pass to the ``docker build`` command. Since Docker build arguments are resolved before deployment, keys and values cannot refer to unresolved tokens (such as ``lambda.functionArn`` or ``queue.queueUrl``). Default: - no build args are passed
        :param file: Path to the Dockerfile (relative to the directory). Default: 'Dockerfile'
        :param repository_name: ECR repository name. Specify this property if you need to statically address the image, e.g. from a Kubernetes Pod. Note, this is only the repository name, without the registry and the tag parts. Default: - the default ECR repository for CDK assets
        :param target: Docker target to build to. Default: - no target
        :param extra_hash: Extra information to encode into the fingerprint (e.g. build instructions and other inputs). Default: - hash is only based on source content
        :param exclude: Glob patterns to exclude from the copy. Default: nothing is excluded
        :param follow: A strategy for how to handle symlinks. Default: Never
        """
        props = aws_cdk.aws_ecr_assets.DockerImageAssetProps(
            directory=directory,
            build_args=build_args,
            file=file,
            repository_name=repository_name,
            target=target,
            extra_hash=extra_hash,
            exclude=exclude,
            follow=follow,
        )

        return jsii.sinvoke(cls, "fromAsset", [scope, id, props])

    @jsii.member(jsii_name="fromCodeBuildImageId")
    @builtins.classmethod
    def from_code_build_image_id(cls, id: str) -> "IBuildImage":
        """Uses a Docker image provided by CodeBuild.

        :param id: The image identifier.

        return
        :return: A Docker image provided by CodeBuild.

        see
        :see: https://docs.aws.amazon.com/codebuild/latest/userguide/build-env-ref-available.html

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            "aws/codebuild/standard:4.0"
        """
        return jsii.sinvoke(cls, "fromCodeBuildImageId", [id])

    @jsii.member(jsii_name="fromDockerRegistry")
    @builtins.classmethod
    def from_docker_registry(
        cls,
        name: str,
        *,
        secrets_manager_credentials: typing.Optional[
            aws_cdk.aws_secretsmanager.ISecret
        ] = None,
    ) -> "IBuildImage":
        """
        :param name: -
        :param secrets_manager_credentials: The credentials, stored in Secrets Manager, used for accessing the repository holding the image, if the repository is private. Default: no credentials will be used (we assume the repository is public)

        return
        :return: a Linux build image from a Docker Hub image.
        """
        options = DockerImageOptions(
            secrets_manager_credentials=secrets_manager_credentials
        )

        return jsii.sinvoke(cls, "fromDockerRegistry", [name, options])

    @jsii.member(jsii_name="fromEcrRepository")
    @builtins.classmethod
    def from_ecr_repository(
        cls, repository: aws_cdk.aws_ecr.IRepository, tag: typing.Optional[str] = None
    ) -> "IBuildImage":
        """
        :param repository: The ECR repository.
        :param tag: Image tag (default "latest").

        return
        :return:

        A Linux build image from an ECR repository.

        NOTE: if the repository is external (i.e. imported), then we won't be able to add
        a resource policy statement for it so CodeBuild can pull the image.

        see
        :see: https://docs.aws.amazon.com/codebuild/latest/userguide/sample-ecr.html
        """
        return jsii.sinvoke(cls, "fromEcrRepository", [repository, tag])

    @jsii.member(jsii_name="runScriptBuildspec")
    def run_script_buildspec(self, entrypoint: str) -> "BuildSpec":
        """Make a buildspec to run the indicated script.

        :param entrypoint: -
        """
        return jsii.invoke(self, "runScriptBuildspec", [entrypoint])

    @jsii.member(jsii_name="validate")
    def validate(
        self,
        *,
        build_image: typing.Optional["IBuildImage"] = None,
        compute_type: typing.Optional["ComputeType"] = None,
        environment_variables: typing.Optional[
            typing.Mapping[str, "BuildEnvironmentVariable"]
        ] = None,
        privileged: typing.Optional[bool] = None,
    ) -> typing.List[str]:
        """Allows the image a chance to validate whether the passed configuration is correct.

        :param build_image: The image used for the builds. Default: LinuxBuildImage.STANDARD_1_0
        :param compute_type: The type of compute to use for this build. See the {@link ComputeType} enum for the possible values. Default: taken from {@link #buildImage#defaultComputeType}
        :param environment_variables: The environment variables that your builds can use.
        :param privileged: Indicates how the project builds Docker images. Specify true to enable running the Docker daemon inside a Docker container. This value must be set to true only if this build project will be used to build Docker images, and the specified build environment image is not one provided by AWS CodeBuild with Docker support. Otherwise, all associated builds that attempt to interact with the Docker daemon will fail. Default: false
        """
        _ = BuildEnvironment(
            build_image=build_image,
            compute_type=compute_type,
            environment_variables=environment_variables,
            privileged=privileged,
        )

        return jsii.invoke(self, "validate", [_])

    @jsii.python.classproperty
    @jsii.member(jsii_name="AMAZON_LINUX_2")
    def AMAZON_LINUX_2(cls) -> "IBuildImage":
        return jsii.sget(cls, "AMAZON_LINUX_2")

    @jsii.python.classproperty
    @jsii.member(jsii_name="AMAZON_LINUX_2_2")
    def AMAZON_LINUX_2_2(cls) -> "IBuildImage":
        return jsii.sget(cls, "AMAZON_LINUX_2_2")

    @jsii.python.classproperty
    @jsii.member(jsii_name="AMAZON_LINUX_2_3")
    def AMAZON_LINUX_2_3(cls) -> "IBuildImage":
        """The Amazon Linux 2 x86_64 standard image, version ``3.0``."""
        return jsii.sget(cls, "AMAZON_LINUX_2_3")

    @jsii.python.classproperty
    @jsii.member(jsii_name="AMAZON_LINUX_2_ARM")
    def AMAZON_LINUX_2_ARM(cls) -> "IBuildImage":
        return jsii.sget(cls, "AMAZON_LINUX_2_ARM")

    @jsii.python.classproperty
    @jsii.member(jsii_name="STANDARD_1_0")
    def STANDARD_1_0(cls) -> "IBuildImage":
        return jsii.sget(cls, "STANDARD_1_0")

    @jsii.python.classproperty
    @jsii.member(jsii_name="STANDARD_2_0")
    def STANDARD_2_0(cls) -> "IBuildImage":
        return jsii.sget(cls, "STANDARD_2_0")

    @jsii.python.classproperty
    @jsii.member(jsii_name="STANDARD_3_0")
    def STANDARD_3_0(cls) -> "IBuildImage":
        return jsii.sget(cls, "STANDARD_3_0")

    @jsii.python.classproperty
    @jsii.member(jsii_name="STANDARD_4_0")
    def STANDARD_4_0(cls) -> "IBuildImage":
        """The ``aws/codebuild/standard:4.0`` build image."""
        return jsii.sget(cls, "STANDARD_4_0")

    @jsii.python.classproperty
    @jsii.member(jsii_name="UBUNTU_14_04_ANDROID_JAVA8_24_4_1")
    def UBUNTU_14_04_ANDROID_JAVA8_24_4_1(cls) -> "IBuildImage":
        """
        deprecated
        :deprecated: Use {@link STANDARD_2_0} and specify runtime in buildspec runtime-versions section

        stability
        :stability: deprecated
        """
        return jsii.sget(cls, "UBUNTU_14_04_ANDROID_JAVA8_24_4_1")

    @jsii.python.classproperty
    @jsii.member(jsii_name="UBUNTU_14_04_ANDROID_JAVA8_26_1_1")
    def UBUNTU_14_04_ANDROID_JAVA8_26_1_1(cls) -> "IBuildImage":
        """
        deprecated
        :deprecated: Use {@link STANDARD_2_0} and specify runtime in buildspec runtime-versions section

        stability
        :stability: deprecated
        """
        return jsii.sget(cls, "UBUNTU_14_04_ANDROID_JAVA8_26_1_1")

    @jsii.python.classproperty
    @jsii.member(jsii_name="UBUNTU_14_04_BASE")
    def UBUNTU_14_04_BASE(cls) -> "IBuildImage":
        """
        deprecated
        :deprecated: Use {@link STANDARD_2_0} and specify runtime in buildspec runtime-versions section

        stability
        :stability: deprecated
        """
        return jsii.sget(cls, "UBUNTU_14_04_BASE")

    @jsii.python.classproperty
    @jsii.member(jsii_name="UBUNTU_14_04_DOCKER_17_09_0")
    def UBUNTU_14_04_DOCKER_17_09_0(cls) -> "IBuildImage":
        """
        deprecated
        :deprecated: Use {@link STANDARD_2_0} and specify runtime in buildspec runtime-versions section

        stability
        :stability: deprecated
        """
        return jsii.sget(cls, "UBUNTU_14_04_DOCKER_17_09_0")

    @jsii.python.classproperty
    @jsii.member(jsii_name="UBUNTU_14_04_DOCKER_18_09_0")
    def UBUNTU_14_04_DOCKER_18_09_0(cls) -> "IBuildImage":
        """
        deprecated
        :deprecated: Use {@link STANDARD_2_0} and specify runtime in buildspec runtime-versions section

        stability
        :stability: deprecated
        """
        return jsii.sget(cls, "UBUNTU_14_04_DOCKER_18_09_0")

    @jsii.python.classproperty
    @jsii.member(jsii_name="UBUNTU_14_04_DOTNET_CORE_1_1")
    def UBUNTU_14_04_DOTNET_CORE_1_1(cls) -> "IBuildImage":
        """
        deprecated
        :deprecated: Use {@link STANDARD_2_0} and specify runtime in buildspec runtime-versions section

        stability
        :stability: deprecated
        """
        return jsii.sget(cls, "UBUNTU_14_04_DOTNET_CORE_1_1")

    @jsii.python.classproperty
    @jsii.member(jsii_name="UBUNTU_14_04_DOTNET_CORE_2_0")
    def UBUNTU_14_04_DOTNET_CORE_2_0(cls) -> "IBuildImage":
        """
        deprecated
        :deprecated: Use {@link STANDARD_2_0} and specify runtime in buildspec runtime-versions section

        stability
        :stability: deprecated
        """
        return jsii.sget(cls, "UBUNTU_14_04_DOTNET_CORE_2_0")

    @jsii.python.classproperty
    @jsii.member(jsii_name="UBUNTU_14_04_DOTNET_CORE_2_1")
    def UBUNTU_14_04_DOTNET_CORE_2_1(cls) -> "IBuildImage":
        """
        deprecated
        :deprecated: Use {@link STANDARD_2_0} and specify runtime in buildspec runtime-versions section

        stability
        :stability: deprecated
        """
        return jsii.sget(cls, "UBUNTU_14_04_DOTNET_CORE_2_1")

    @jsii.python.classproperty
    @jsii.member(jsii_name="UBUNTU_14_04_GOLANG_1_10")
    def UBUNTU_14_04_GOLANG_1_10(cls) -> "IBuildImage":
        """
        deprecated
        :deprecated: Use {@link STANDARD_2_0} and specify runtime in buildspec runtime-versions section

        stability
        :stability: deprecated
        """
        return jsii.sget(cls, "UBUNTU_14_04_GOLANG_1_10")

    @jsii.python.classproperty
    @jsii.member(jsii_name="UBUNTU_14_04_GOLANG_1_11")
    def UBUNTU_14_04_GOLANG_1_11(cls) -> "IBuildImage":
        """
        deprecated
        :deprecated: Use {@link STANDARD_2_0} and specify runtime in buildspec runtime-versions section

        stability
        :stability: deprecated
        """
        return jsii.sget(cls, "UBUNTU_14_04_GOLANG_1_11")

    @jsii.python.classproperty
    @jsii.member(jsii_name="UBUNTU_14_04_NODEJS_10_1_0")
    def UBUNTU_14_04_NODEJS_10_1_0(cls) -> "IBuildImage":
        """
        deprecated
        :deprecated: Use {@link STANDARD_2_0} and specify runtime in buildspec runtime-versions section

        stability
        :stability: deprecated
        """
        return jsii.sget(cls, "UBUNTU_14_04_NODEJS_10_1_0")

    @jsii.python.classproperty
    @jsii.member(jsii_name="UBUNTU_14_04_NODEJS_10_14_1")
    def UBUNTU_14_04_NODEJS_10_14_1(cls) -> "IBuildImage":
        """
        deprecated
        :deprecated: Use {@link STANDARD_2_0} and specify runtime in buildspec runtime-versions section

        stability
        :stability: deprecated
        """
        return jsii.sget(cls, "UBUNTU_14_04_NODEJS_10_14_1")

    @jsii.python.classproperty
    @jsii.member(jsii_name="UBUNTU_14_04_NODEJS_6_3_1")
    def UBUNTU_14_04_NODEJS_6_3_1(cls) -> "IBuildImage":
        """
        deprecated
        :deprecated: Use {@link STANDARD_2_0} and specify runtime in buildspec runtime-versions section

        stability
        :stability: deprecated
        """
        return jsii.sget(cls, "UBUNTU_14_04_NODEJS_6_3_1")

    @jsii.python.classproperty
    @jsii.member(jsii_name="UBUNTU_14_04_NODEJS_8_11_0")
    def UBUNTU_14_04_NODEJS_8_11_0(cls) -> "IBuildImage":
        """
        deprecated
        :deprecated: Use {@link STANDARD_2_0} and specify runtime in buildspec runtime-versions section

        stability
        :stability: deprecated
        """
        return jsii.sget(cls, "UBUNTU_14_04_NODEJS_8_11_0")

    @jsii.python.classproperty
    @jsii.member(jsii_name="UBUNTU_14_04_OPEN_JDK_11")
    def UBUNTU_14_04_OPEN_JDK_11(cls) -> "IBuildImage":
        """
        deprecated
        :deprecated: Use {@link STANDARD_2_0} and specify runtime in buildspec runtime-versions section

        stability
        :stability: deprecated
        """
        return jsii.sget(cls, "UBUNTU_14_04_OPEN_JDK_11")

    @jsii.python.classproperty
    @jsii.member(jsii_name="UBUNTU_14_04_OPEN_JDK_8")
    def UBUNTU_14_04_OPEN_JDK_8(cls) -> "IBuildImage":
        """
        deprecated
        :deprecated: Use {@link STANDARD_2_0} and specify runtime in buildspec runtime-versions section

        stability
        :stability: deprecated
        """
        return jsii.sget(cls, "UBUNTU_14_04_OPEN_JDK_8")

    @jsii.python.classproperty
    @jsii.member(jsii_name="UBUNTU_14_04_OPEN_JDK_9")
    def UBUNTU_14_04_OPEN_JDK_9(cls) -> "IBuildImage":
        """
        deprecated
        :deprecated: Use {@link STANDARD_2_0} and specify runtime in buildspec runtime-versions section

        stability
        :stability: deprecated
        """
        return jsii.sget(cls, "UBUNTU_14_04_OPEN_JDK_9")

    @jsii.python.classproperty
    @jsii.member(jsii_name="UBUNTU_14_04_PHP_5_6")
    def UBUNTU_14_04_PHP_5_6(cls) -> "IBuildImage":
        """
        deprecated
        :deprecated: Use {@link STANDARD_2_0} and specify runtime in buildspec runtime-versions section

        stability
        :stability: deprecated
        """
        return jsii.sget(cls, "UBUNTU_14_04_PHP_5_6")

    @jsii.python.classproperty
    @jsii.member(jsii_name="UBUNTU_14_04_PHP_7_0")
    def UBUNTU_14_04_PHP_7_0(cls) -> "IBuildImage":
        """
        deprecated
        :deprecated: Use {@link STANDARD_2_0} and specify runtime in buildspec runtime-versions section

        stability
        :stability: deprecated
        """
        return jsii.sget(cls, "UBUNTU_14_04_PHP_7_0")

    @jsii.python.classproperty
    @jsii.member(jsii_name="UBUNTU_14_04_PHP_7_1")
    def UBUNTU_14_04_PHP_7_1(cls) -> "IBuildImage":
        """
        deprecated
        :deprecated: Use {@link STANDARD_2_0} and specify runtime in buildspec runtime-versions section

        stability
        :stability: deprecated
        """
        return jsii.sget(cls, "UBUNTU_14_04_PHP_7_1")

    @jsii.python.classproperty
    @jsii.member(jsii_name="UBUNTU_14_04_PYTHON_2_7_12")
    def UBUNTU_14_04_PYTHON_2_7_12(cls) -> "IBuildImage":
        """
        deprecated
        :deprecated: Use {@link STANDARD_2_0} and specify runtime in buildspec runtime-versions section

        stability
        :stability: deprecated
        """
        return jsii.sget(cls, "UBUNTU_14_04_PYTHON_2_7_12")

    @jsii.python.classproperty
    @jsii.member(jsii_name="UBUNTU_14_04_PYTHON_3_3_6")
    def UBUNTU_14_04_PYTHON_3_3_6(cls) -> "IBuildImage":
        """
        deprecated
        :deprecated: Use {@link STANDARD_2_0} and specify runtime in buildspec runtime-versions section

        stability
        :stability: deprecated
        """
        return jsii.sget(cls, "UBUNTU_14_04_PYTHON_3_3_6")

    @jsii.python.classproperty
    @jsii.member(jsii_name="UBUNTU_14_04_PYTHON_3_4_5")
    def UBUNTU_14_04_PYTHON_3_4_5(cls) -> "IBuildImage":
        """
        deprecated
        :deprecated: Use {@link STANDARD_2_0} and specify runtime in buildspec runtime-versions section

        stability
        :stability: deprecated
        """
        return jsii.sget(cls, "UBUNTU_14_04_PYTHON_3_4_5")

    @jsii.python.classproperty
    @jsii.member(jsii_name="UBUNTU_14_04_PYTHON_3_5_2")
    def UBUNTU_14_04_PYTHON_3_5_2(cls) -> "IBuildImage":
        """
        deprecated
        :deprecated: Use {@link STANDARD_2_0} and specify runtime in buildspec runtime-versions section

        stability
        :stability: deprecated
        """
        return jsii.sget(cls, "UBUNTU_14_04_PYTHON_3_5_2")

    @jsii.python.classproperty
    @jsii.member(jsii_name="UBUNTU_14_04_PYTHON_3_6_5")
    def UBUNTU_14_04_PYTHON_3_6_5(cls) -> "IBuildImage":
        """
        deprecated
        :deprecated: Use {@link STANDARD_2_0} and specify runtime in buildspec runtime-versions section

        stability
        :stability: deprecated
        """
        return jsii.sget(cls, "UBUNTU_14_04_PYTHON_3_6_5")

    @jsii.python.classproperty
    @jsii.member(jsii_name="UBUNTU_14_04_PYTHON_3_7_1")
    def UBUNTU_14_04_PYTHON_3_7_1(cls) -> "IBuildImage":
        """
        deprecated
        :deprecated: Use {@link STANDARD_2_0} and specify runtime in buildspec runtime-versions section

        stability
        :stability: deprecated
        """
        return jsii.sget(cls, "UBUNTU_14_04_PYTHON_3_7_1")

    @jsii.python.classproperty
    @jsii.member(jsii_name="UBUNTU_14_04_RUBY_2_2_5")
    def UBUNTU_14_04_RUBY_2_2_5(cls) -> "IBuildImage":
        """
        deprecated
        :deprecated: Use {@link STANDARD_2_0} and specify runtime in buildspec runtime-versions section

        stability
        :stability: deprecated
        """
        return jsii.sget(cls, "UBUNTU_14_04_RUBY_2_2_5")

    @jsii.python.classproperty
    @jsii.member(jsii_name="UBUNTU_14_04_RUBY_2_3_1")
    def UBUNTU_14_04_RUBY_2_3_1(cls) -> "IBuildImage":
        """
        deprecated
        :deprecated: Use {@link STANDARD_2_0} and specify runtime in buildspec runtime-versions section

        stability
        :stability: deprecated
        """
        return jsii.sget(cls, "UBUNTU_14_04_RUBY_2_3_1")

    @jsii.python.classproperty
    @jsii.member(jsii_name="UBUNTU_14_04_RUBY_2_5_1")
    def UBUNTU_14_04_RUBY_2_5_1(cls) -> "IBuildImage":
        """
        deprecated
        :deprecated: Use {@link STANDARD_2_0} and specify runtime in buildspec runtime-versions section

        stability
        :stability: deprecated
        """
        return jsii.sget(cls, "UBUNTU_14_04_RUBY_2_5_1")

    @jsii.python.classproperty
    @jsii.member(jsii_name="UBUNTU_14_04_RUBY_2_5_3")
    def UBUNTU_14_04_RUBY_2_5_3(cls) -> "IBuildImage":
        """
        deprecated
        :deprecated: Use {@link STANDARD_2_0} and specify runtime in buildspec runtime-versions section

        stability
        :stability: deprecated
        """
        return jsii.sget(cls, "UBUNTU_14_04_RUBY_2_5_3")

    @builtins.property
    @jsii.member(jsii_name="defaultComputeType")
    def default_compute_type(self) -> "ComputeType":
        """The default {@link ComputeType} to use with this image, if one was not specified in {@link BuildEnvironment#computeType} explicitly."""
        return jsii.get(self, "defaultComputeType")

    @builtins.property
    @jsii.member(jsii_name="imageId")
    def image_id(self) -> str:
        """The Docker image identifier that the build environment uses."""
        return jsii.get(self, "imageId")

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> str:
        """The type of build environment."""
        return jsii.get(self, "type")

    @builtins.property
    @jsii.member(jsii_name="imagePullPrincipalType")
    def image_pull_principal_type(self) -> typing.Optional["ImagePullPrincipalType"]:
        """The type of principal that CodeBuild will use to pull this build Docker image."""
        return jsii.get(self, "imagePullPrincipalType")

    @builtins.property
    @jsii.member(jsii_name="repository")
    def repository(self) -> typing.Optional[aws_cdk.aws_ecr.IRepository]:
        """An optional ECR repository that the image is hosted in."""
        return jsii.get(self, "repository")

    @builtins.property
    @jsii.member(jsii_name="secretsManagerCredentials")
    def secrets_manager_credentials(
        self,
    ) -> typing.Optional[aws_cdk.aws_secretsmanager.ISecret]:
        """The secretsManagerCredentials for access to a private registry."""
        return jsii.get(self, "secretsManagerCredentials")


@jsii.enum(jsii_type="@aws-cdk/aws-codebuild.LocalCacheMode")
class LocalCacheMode(enum.Enum):
    """Local cache modes to enable for the CodeBuild Project."""

    SOURCE = "SOURCE"
    """Caches Git metadata for primary and secondary sources."""
    DOCKER_LAYER = "DOCKER_LAYER"
    """Caches existing Docker layers."""
    CUSTOM = "CUSTOM"
    """Caches directories you specify in the buildspec file."""


class PhaseChangeEvent(
    metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codebuild.PhaseChangeEvent"
):
    """Event fields for the CodeBuild "phase change" event.

    see
    :see: https://docs.aws.amazon.com/codebuild/latest/userguide/sample-build-notifications.html#sample-build-notifications-ref
    """

    @jsii.python.classproperty
    @jsii.member(jsii_name="buildComplete")
    def build_complete(cls) -> str:
        """Whether the build is complete."""
        return jsii.sget(cls, "buildComplete")

    @jsii.python.classproperty
    @jsii.member(jsii_name="buildId")
    def build_id(cls) -> str:
        """The triggering build's id."""
        return jsii.sget(cls, "buildId")

    @jsii.python.classproperty
    @jsii.member(jsii_name="completedPhase")
    def completed_phase(cls) -> str:
        """The phase that was just completed."""
        return jsii.sget(cls, "completedPhase")

    @jsii.python.classproperty
    @jsii.member(jsii_name="completedPhaseDurationSeconds")
    def completed_phase_duration_seconds(cls) -> str:
        """The duration of the completed phase."""
        return jsii.sget(cls, "completedPhaseDurationSeconds")

    @jsii.python.classproperty
    @jsii.member(jsii_name="completedPhaseStatus")
    def completed_phase_status(cls) -> str:
        """The status of the completed phase."""
        return jsii.sget(cls, "completedPhaseStatus")

    @jsii.python.classproperty
    @jsii.member(jsii_name="projectName")
    def project_name(cls) -> str:
        """The triggering build's project name."""
        return jsii.sget(cls, "projectName")


@jsii.data_type(
    jsii_type="@aws-cdk/aws-codebuild.PipelineProjectProps",
    jsii_struct_bases=[CommonProjectProps],
    name_mapping={
        "allow_all_outbound": "allowAllOutbound",
        "badge": "badge",
        "build_spec": "buildSpec",
        "cache": "cache",
        "description": "description",
        "encryption_key": "encryptionKey",
        "environment": "environment",
        "environment_variables": "environmentVariables",
        "file_system_locations": "fileSystemLocations",
        "grant_report_group_permissions": "grantReportGroupPermissions",
        "project_name": "projectName",
        "role": "role",
        "security_groups": "securityGroups",
        "subnet_selection": "subnetSelection",
        "timeout": "timeout",
        "vpc": "vpc",
    },
)
class PipelineProjectProps(CommonProjectProps):
    def __init__(
        self,
        *,
        allow_all_outbound: typing.Optional[bool] = None,
        badge: typing.Optional[bool] = None,
        build_spec: typing.Optional["BuildSpec"] = None,
        cache: typing.Optional["Cache"] = None,
        description: typing.Optional[str] = None,
        encryption_key: typing.Optional[aws_cdk.aws_kms.IKey] = None,
        environment: typing.Optional["BuildEnvironment"] = None,
        environment_variables: typing.Optional[
            typing.Mapping[str, "BuildEnvironmentVariable"]
        ] = None,
        file_system_locations: typing.Optional[
            typing.List["IFileSystemLocation"]
        ] = None,
        grant_report_group_permissions: typing.Optional[bool] = None,
        project_name: typing.Optional[str] = None,
        role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
        security_groups: typing.Optional[
            typing.List[aws_cdk.aws_ec2.ISecurityGroup]
        ] = None,
        subnet_selection: typing.Optional[aws_cdk.aws_ec2.SubnetSelection] = None,
        timeout: typing.Optional[aws_cdk.core.Duration] = None,
        vpc: typing.Optional[aws_cdk.aws_ec2.IVpc] = None,
    ) -> None:
        """
        :param allow_all_outbound: Whether to allow the CodeBuild to send all network traffic. If set to false, you must individually add traffic rules to allow the CodeBuild project to connect to network targets. Only used if 'vpc' is supplied. Default: true
        :param badge: Indicates whether AWS CodeBuild generates a publicly accessible URL for your project's build badge. For more information, see Build Badges Sample in the AWS CodeBuild User Guide. Default: false
        :param build_spec: Filename or contents of buildspec in JSON format. Default: - Empty buildspec.
        :param cache: Caching strategy to use. Default: Cache.none
        :param description: A description of the project. Use the description to identify the purpose of the project. Default: - No description.
        :param encryption_key: Encryption key to use to read and write artifacts. Default: - The AWS-managed CMK for Amazon Simple Storage Service (Amazon S3) is used.
        :param environment: Build environment to use for the build. Default: BuildEnvironment.LinuxBuildImage.STANDARD_1_0
        :param environment_variables: Additional environment variables to add to the build environment. Default: - No additional environment variables are specified.
        :param file_system_locations: An ProjectFileSystemLocation objects for a CodeBuild build project. A ProjectFileSystemLocation object specifies the identifier, location, mountOptions, mountPoint, and type of a file system created using Amazon Elastic File System. Default: - no file system locations
        :param grant_report_group_permissions: Add permissions to this project's role to create and use test report groups with name starting with the name of this project. That is the standard report group that gets created when a simple name (in contrast to an ARN) is used in the 'reports' section of the buildspec of this project. This is usually harmless, but you can turn these off if you don't plan on using test reports in this project. Default: true
        :param project_name: The physical, human-readable name of the CodeBuild Project. Default: - Name is automatically generated.
        :param role: Service Role to assume while running the build. Default: - A role will be created.
        :param security_groups: What security group to associate with the codebuild project's network interfaces. If no security group is identified, one will be created automatically. Only used if 'vpc' is supplied. Default: - Security group will be automatically created.
        :param subnet_selection: Where to place the network interfaces within the VPC. Only used if 'vpc' is supplied. Default: - All private subnets.
        :param timeout: The number of minutes after which AWS CodeBuild stops the build if it's not complete. For valid values, see the timeoutInMinutes field in the AWS CodeBuild User Guide. Default: Duration.hours(1)
        :param vpc: VPC network to place codebuild network interfaces. Specify this if the codebuild project needs to access resources in a VPC. Default: - No VPC is specified.
        """
        if isinstance(environment, dict):
            environment = BuildEnvironment(**environment)
        if isinstance(subnet_selection, dict):
            subnet_selection = aws_cdk.aws_ec2.SubnetSelection(**subnet_selection)
        self._values = {}
        if allow_all_outbound is not None:
            self._values["allow_all_outbound"] = allow_all_outbound
        if badge is not None:
            self._values["badge"] = badge
        if build_spec is not None:
            self._values["build_spec"] = build_spec
        if cache is not None:
            self._values["cache"] = cache
        if description is not None:
            self._values["description"] = description
        if encryption_key is not None:
            self._values["encryption_key"] = encryption_key
        if environment is not None:
            self._values["environment"] = environment
        if environment_variables is not None:
            self._values["environment_variables"] = environment_variables
        if file_system_locations is not None:
            self._values["file_system_locations"] = file_system_locations
        if grant_report_group_permissions is not None:
            self._values[
                "grant_report_group_permissions"
            ] = grant_report_group_permissions
        if project_name is not None:
            self._values["project_name"] = project_name
        if role is not None:
            self._values["role"] = role
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if subnet_selection is not None:
            self._values["subnet_selection"] = subnet_selection
        if timeout is not None:
            self._values["timeout"] = timeout
        if vpc is not None:
            self._values["vpc"] = vpc

    @builtins.property
    def allow_all_outbound(self) -> typing.Optional[bool]:
        """Whether to allow the CodeBuild to send all network traffic.

        If set to false, you must individually add traffic rules to allow the
        CodeBuild project to connect to network targets.

        Only used if 'vpc' is supplied.

        default
        :default: true
        """
        return self._values.get("allow_all_outbound")

    @builtins.property
    def badge(self) -> typing.Optional[bool]:
        """Indicates whether AWS CodeBuild generates a publicly accessible URL for your project's build badge.

        For more information, see Build Badges Sample
        in the AWS CodeBuild User Guide.

        default
        :default: false
        """
        return self._values.get("badge")

    @builtins.property
    def build_spec(self) -> typing.Optional["BuildSpec"]:
        """Filename or contents of buildspec in JSON format.

        default
        :default: - Empty buildspec.

        see
        :see: https://docs.aws.amazon.com/codebuild/latest/userguide/build-spec-ref.html#build-spec-ref-example
        """
        return self._values.get("build_spec")

    @builtins.property
    def cache(self) -> typing.Optional["Cache"]:
        """Caching strategy to use.

        default
        :default: Cache.none
        """
        return self._values.get("cache")

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """A description of the project.

        Use the description to identify the purpose
        of the project.

        default
        :default: - No description.
        """
        return self._values.get("description")

    @builtins.property
    def encryption_key(self) -> typing.Optional[aws_cdk.aws_kms.IKey]:
        """Encryption key to use to read and write artifacts.

        default
        :default: - The AWS-managed CMK for Amazon Simple Storage Service (Amazon S3) is used.
        """
        return self._values.get("encryption_key")

    @builtins.property
    def environment(self) -> typing.Optional["BuildEnvironment"]:
        """Build environment to use for the build.

        default
        :default: BuildEnvironment.LinuxBuildImage.STANDARD_1_0
        """
        return self._values.get("environment")

    @builtins.property
    def environment_variables(
        self,
    ) -> typing.Optional[typing.Mapping[str, "BuildEnvironmentVariable"]]:
        """Additional environment variables to add to the build environment.

        default
        :default: - No additional environment variables are specified.
        """
        return self._values.get("environment_variables")

    @builtins.property
    def file_system_locations(
        self,
    ) -> typing.Optional[typing.List["IFileSystemLocation"]]:
        """An  ProjectFileSystemLocation objects for a CodeBuild build project.

        A ProjectFileSystemLocation object specifies the identifier, location, mountOptions, mountPoint,
        and type of a file system created using Amazon Elastic File System.

        default
        :default: - no file system locations
        """
        return self._values.get("file_system_locations")

    @builtins.property
    def grant_report_group_permissions(self) -> typing.Optional[bool]:
        """Add permissions to this project's role to create and use test report groups with name starting with the name of this project.

        That is the standard report group that gets created when a simple name
        (in contrast to an ARN)
        is used in the 'reports' section of the buildspec of this project.
        This is usually harmless, but you can turn these off if you don't plan on using test
        reports in this project.

        default
        :default: true

        see
        :see: https://docs.aws.amazon.com/codebuild/latest/userguide/test-report-group-naming.html
        """
        return self._values.get("grant_report_group_permissions")

    @builtins.property
    def project_name(self) -> typing.Optional[str]:
        """The physical, human-readable name of the CodeBuild Project.

        default
        :default: - Name is automatically generated.
        """
        return self._values.get("project_name")

    @builtins.property
    def role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """Service Role to assume while running the build.

        default
        :default: - A role will be created.
        """
        return self._values.get("role")

    @builtins.property
    def security_groups(
        self,
    ) -> typing.Optional[typing.List[aws_cdk.aws_ec2.ISecurityGroup]]:
        """What security group to associate with the codebuild project's network interfaces.

        If no security group is identified, one will be created automatically.

        Only used if 'vpc' is supplied.

        default
        :default: - Security group will be automatically created.
        """
        return self._values.get("security_groups")

    @builtins.property
    def subnet_selection(self) -> typing.Optional[aws_cdk.aws_ec2.SubnetSelection]:
        """Where to place the network interfaces within the VPC.

        Only used if 'vpc' is supplied.

        default
        :default: - All private subnets.
        """
        return self._values.get("subnet_selection")

    @builtins.property
    def timeout(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The number of minutes after which AWS CodeBuild stops the build if it's not complete.

        For valid values, see the timeoutInMinutes field in the AWS
        CodeBuild User Guide.

        default
        :default: Duration.hours(1)
        """
        return self._values.get("timeout")

    @builtins.property
    def vpc(self) -> typing.Optional[aws_cdk.aws_ec2.IVpc]:
        """VPC network to place codebuild network interfaces.

        Specify this if the codebuild project needs to access resources in a VPC.

        default
        :default: - No VPC is specified.
        """
        return self._values.get("vpc")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipelineProjectProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IProject)
class Project(
    aws_cdk.core.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-codebuild.Project",
):
    """A representation of a CodeBuild Project."""

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: str,
        *,
        artifacts: typing.Optional["IArtifacts"] = None,
        secondary_artifacts: typing.Optional[typing.List["IArtifacts"]] = None,
        secondary_sources: typing.Optional[typing.List["ISource"]] = None,
        source: typing.Optional["ISource"] = None,
        allow_all_outbound: typing.Optional[bool] = None,
        badge: typing.Optional[bool] = None,
        build_spec: typing.Optional["BuildSpec"] = None,
        cache: typing.Optional["Cache"] = None,
        description: typing.Optional[str] = None,
        encryption_key: typing.Optional[aws_cdk.aws_kms.IKey] = None,
        environment: typing.Optional["BuildEnvironment"] = None,
        environment_variables: typing.Optional[
            typing.Mapping[str, "BuildEnvironmentVariable"]
        ] = None,
        file_system_locations: typing.Optional[
            typing.List["IFileSystemLocation"]
        ] = None,
        grant_report_group_permissions: typing.Optional[bool] = None,
        project_name: typing.Optional[str] = None,
        role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
        security_groups: typing.Optional[
            typing.List[aws_cdk.aws_ec2.ISecurityGroup]
        ] = None,
        subnet_selection: typing.Optional[aws_cdk.aws_ec2.SubnetSelection] = None,
        timeout: typing.Optional[aws_cdk.core.Duration] = None,
        vpc: typing.Optional[aws_cdk.aws_ec2.IVpc] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param artifacts: Defines where build artifacts will be stored. Could be: PipelineBuildArtifacts, NoArtifacts and S3Artifacts. Default: NoArtifacts
        :param secondary_artifacts: The secondary artifacts for the Project. Can also be added after the Project has been created by using the {@link Project#addSecondaryArtifact} method. Default: - No secondary artifacts.
        :param secondary_sources: The secondary sources for the Project. Can be also added after the Project has been created by using the {@link Project#addSecondarySource} method. Default: - No secondary sources.
        :param source: The source of the build. *Note*: if {@link NoSource} is given as the source, then you need to provide an explicit ``buildSpec``. Default: - NoSource
        :param allow_all_outbound: Whether to allow the CodeBuild to send all network traffic. If set to false, you must individually add traffic rules to allow the CodeBuild project to connect to network targets. Only used if 'vpc' is supplied. Default: true
        :param badge: Indicates whether AWS CodeBuild generates a publicly accessible URL for your project's build badge. For more information, see Build Badges Sample in the AWS CodeBuild User Guide. Default: false
        :param build_spec: Filename or contents of buildspec in JSON format. Default: - Empty buildspec.
        :param cache: Caching strategy to use. Default: Cache.none
        :param description: A description of the project. Use the description to identify the purpose of the project. Default: - No description.
        :param encryption_key: Encryption key to use to read and write artifacts. Default: - The AWS-managed CMK for Amazon Simple Storage Service (Amazon S3) is used.
        :param environment: Build environment to use for the build. Default: BuildEnvironment.LinuxBuildImage.STANDARD_1_0
        :param environment_variables: Additional environment variables to add to the build environment. Default: - No additional environment variables are specified.
        :param file_system_locations: An ProjectFileSystemLocation objects for a CodeBuild build project. A ProjectFileSystemLocation object specifies the identifier, location, mountOptions, mountPoint, and type of a file system created using Amazon Elastic File System. Default: - no file system locations
        :param grant_report_group_permissions: Add permissions to this project's role to create and use test report groups with name starting with the name of this project. That is the standard report group that gets created when a simple name (in contrast to an ARN) is used in the 'reports' section of the buildspec of this project. This is usually harmless, but you can turn these off if you don't plan on using test reports in this project. Default: true
        :param project_name: The physical, human-readable name of the CodeBuild Project. Default: - Name is automatically generated.
        :param role: Service Role to assume while running the build. Default: - A role will be created.
        :param security_groups: What security group to associate with the codebuild project's network interfaces. If no security group is identified, one will be created automatically. Only used if 'vpc' is supplied. Default: - Security group will be automatically created.
        :param subnet_selection: Where to place the network interfaces within the VPC. Only used if 'vpc' is supplied. Default: - All private subnets.
        :param timeout: The number of minutes after which AWS CodeBuild stops the build if it's not complete. For valid values, see the timeoutInMinutes field in the AWS CodeBuild User Guide. Default: Duration.hours(1)
        :param vpc: VPC network to place codebuild network interfaces. Specify this if the codebuild project needs to access resources in a VPC. Default: - No VPC is specified.
        """
        props = ProjectProps(
            artifacts=artifacts,
            secondary_artifacts=secondary_artifacts,
            secondary_sources=secondary_sources,
            source=source,
            allow_all_outbound=allow_all_outbound,
            badge=badge,
            build_spec=build_spec,
            cache=cache,
            description=description,
            encryption_key=encryption_key,
            environment=environment,
            environment_variables=environment_variables,
            file_system_locations=file_system_locations,
            grant_report_group_permissions=grant_report_group_permissions,
            project_name=project_name,
            role=role,
            security_groups=security_groups,
            subnet_selection=subnet_selection,
            timeout=timeout,
            vpc=vpc,
        )

        jsii.create(Project, self, [scope, id, props])

    @jsii.member(jsii_name="fromProjectArn")
    @builtins.classmethod
    def from_project_arn(
        cls, scope: aws_cdk.core.Construct, id: str, project_arn: str
    ) -> "IProject":
        """
        :param scope: -
        :param id: -
        :param project_arn: -
        """
        return jsii.sinvoke(cls, "fromProjectArn", [scope, id, project_arn])

    @jsii.member(jsii_name="fromProjectName")
    @builtins.classmethod
    def from_project_name(
        cls, scope: aws_cdk.core.Construct, id: str, project_name: str
    ) -> "IProject":
        """Import a Project defined either outside the CDK, or in a different CDK Stack (and exported using the {@link export} method).

        :param scope: the parent Construct for this Construct.
        :param id: the logical name of this Construct.
        :param project_name: the name of the project to import.

        return
        :return: a reference to the existing Project

        note:
        :note::

        if you're importing a CodeBuild Project for use
        in a CodePipeline, make sure the existing Project
        has permissions to access the S3 Bucket of that Pipeline -
        otherwise, builds in that Pipeline will always fail.
        """
        return jsii.sinvoke(cls, "fromProjectName", [scope, id, project_name])

    @jsii.member(jsii_name="serializeEnvVariables")
    @builtins.classmethod
    def serialize_env_variables(
        cls, environment_variables: typing.Mapping[str, "BuildEnvironmentVariable"]
    ) -> typing.List["CfnProject.EnvironmentVariableProperty"]:
        """Convert the environment variables map of string to {@link BuildEnvironmentVariable}, which is the customer-facing type, to a list of {@link CfnProject.EnvironmentVariableProperty}, which is the representation of environment variables in CloudFormation.

        :param environment_variables: the map of string to environment variables.

        return
        :return: an array of {@link CfnProject.EnvironmentVariableProperty} instances
        """
        return jsii.sinvoke(cls, "serializeEnvVariables", [environment_variables])

    @jsii.member(jsii_name="addFileSystemLocation")
    def add_file_system_location(
        self, file_system_location: "IFileSystemLocation"
    ) -> None:
        """Adds a fileSystemLocation to the Project.

        :param file_system_location: the fileSystemLocation to add.
        """
        return jsii.invoke(self, "addFileSystemLocation", [file_system_location])

    @jsii.member(jsii_name="addSecondaryArtifact")
    def add_secondary_artifact(self, secondary_artifact: "IArtifacts") -> None:
        """Adds a secondary artifact to the Project.

        :param secondary_artifact: the artifact to add as a secondary artifact.

        see
        :see: https://docs.aws.amazon.com/codebuild/latest/userguide/sample-multi-in-out.html
        """
        return jsii.invoke(self, "addSecondaryArtifact", [secondary_artifact])

    @jsii.member(jsii_name="addSecondarySource")
    def add_secondary_source(self, secondary_source: "ISource") -> None:
        """Adds a secondary source to the Project.

        :param secondary_source: the source to add as a secondary source.

        see
        :see: https://docs.aws.amazon.com/codebuild/latest/userguide/sample-multi-in-out.html
        """
        return jsii.invoke(self, "addSecondarySource", [secondary_source])

    @jsii.member(jsii_name="addToRolePolicy")
    def add_to_role_policy(self, statement: aws_cdk.aws_iam.PolicyStatement) -> None:
        """Add a permission only if there's a policy attached.

        :param statement: The permissions statement to add.
        """
        return jsii.invoke(self, "addToRolePolicy", [statement])

    @jsii.member(jsii_name="bindToCodePipeline")
    def bind_to_code_pipeline(
        self, _scope: aws_cdk.core.Construct, *, artifact_bucket: aws_cdk.aws_s3.IBucket
    ) -> None:
        """A callback invoked when the given project is added to a CodePipeline.

        :param _scope: the construct the binding is taking place in.
        :param artifact_bucket: The artifact bucket that will be used by the action that invokes this project.
        """
        options = BindToCodePipelineOptions(artifact_bucket=artifact_bucket)

        return jsii.invoke(self, "bindToCodePipeline", [_scope, options])

    @jsii.member(jsii_name="metric")
    def metric(
        self,
        metric_name: str,
        *,
        account: typing.Optional[str] = None,
        color: typing.Optional[str] = None,
        dimensions: typing.Optional[typing.Mapping[str, typing.Any]] = None,
        label: typing.Optional[str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[str] = None,
        statistic: typing.Optional[str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        """
        :param metric_name: The name of the metric.
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        return
        :return: a CloudWatch metric associated with this build project.
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metric", [metric_name, props])

    @jsii.member(jsii_name="metricBuilds")
    def metric_builds(
        self,
        *,
        account: typing.Optional[str] = None,
        color: typing.Optional[str] = None,
        dimensions: typing.Optional[typing.Mapping[str, typing.Any]] = None,
        label: typing.Optional[str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[str] = None,
        statistic: typing.Optional[str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        """Measures the number of builds triggered.

        Units: Count

        Valid CloudWatch statistics: Sum

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        default
        :default: sum over 5 minutes
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metricBuilds", [props])

    @jsii.member(jsii_name="metricDuration")
    def metric_duration(
        self,
        *,
        account: typing.Optional[str] = None,
        color: typing.Optional[str] = None,
        dimensions: typing.Optional[typing.Mapping[str, typing.Any]] = None,
        label: typing.Optional[str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[str] = None,
        statistic: typing.Optional[str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        """Measures the duration of all builds over time.

        Units: Seconds

        Valid CloudWatch statistics: Average (recommended), Maximum, Minimum

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        default
        :default: average over 5 minutes
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metricDuration", [props])

    @jsii.member(jsii_name="metricFailedBuilds")
    def metric_failed_builds(
        self,
        *,
        account: typing.Optional[str] = None,
        color: typing.Optional[str] = None,
        dimensions: typing.Optional[typing.Mapping[str, typing.Any]] = None,
        label: typing.Optional[str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[str] = None,
        statistic: typing.Optional[str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        """Measures the number of builds that failed because of client error or because of a timeout.

        Units: Count

        Valid CloudWatch statistics: Sum

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        default
        :default: sum over 5 minutes
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metricFailedBuilds", [props])

    @jsii.member(jsii_name="metricSucceededBuilds")
    def metric_succeeded_builds(
        self,
        *,
        account: typing.Optional[str] = None,
        color: typing.Optional[str] = None,
        dimensions: typing.Optional[typing.Mapping[str, typing.Any]] = None,
        label: typing.Optional[str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[str] = None,
        statistic: typing.Optional[str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        """Measures the number of successful builds.

        Units: Count

        Valid CloudWatch statistics: Sum

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        default
        :default: sum over 5 minutes
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metricSucceededBuilds", [props])

    @jsii.member(jsii_name="onBuildFailed")
    def on_build_failed(
        self,
        id: str,
        *,
        description: typing.Optional[str] = None,
        event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern] = None,
        rule_name: typing.Optional[str] = None,
        target: typing.Optional[aws_cdk.aws_events.IRuleTarget] = None,
    ) -> aws_cdk.aws_events.Rule:
        """Defines an event rule which triggers when a build fails.

        To access fields from the event in the event target input,
        use the static fields on the ``StateChangeEvent`` class.

        :param id: -
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        """
        options = aws_cdk.aws_events.OnEventOptions(
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
            target=target,
        )

        return jsii.invoke(self, "onBuildFailed", [id, options])

    @jsii.member(jsii_name="onBuildStarted")
    def on_build_started(
        self,
        id: str,
        *,
        description: typing.Optional[str] = None,
        event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern] = None,
        rule_name: typing.Optional[str] = None,
        target: typing.Optional[aws_cdk.aws_events.IRuleTarget] = None,
    ) -> aws_cdk.aws_events.Rule:
        """Defines an event rule which triggers when a build starts.

        To access fields from the event in the event target input,
        use the static fields on the ``StateChangeEvent`` class.

        :param id: -
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        """
        options = aws_cdk.aws_events.OnEventOptions(
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
            target=target,
        )

        return jsii.invoke(self, "onBuildStarted", [id, options])

    @jsii.member(jsii_name="onBuildSucceeded")
    def on_build_succeeded(
        self,
        id: str,
        *,
        description: typing.Optional[str] = None,
        event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern] = None,
        rule_name: typing.Optional[str] = None,
        target: typing.Optional[aws_cdk.aws_events.IRuleTarget] = None,
    ) -> aws_cdk.aws_events.Rule:
        """Defines an event rule which triggers when a build completes successfully.

        To access fields from the event in the event target input,
        use the static fields on the ``StateChangeEvent`` class.

        :param id: -
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        """
        options = aws_cdk.aws_events.OnEventOptions(
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
            target=target,
        )

        return jsii.invoke(self, "onBuildSucceeded", [id, options])

    @jsii.member(jsii_name="onEvent")
    def on_event(
        self,
        id: str,
        *,
        description: typing.Optional[str] = None,
        event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern] = None,
        rule_name: typing.Optional[str] = None,
        target: typing.Optional[aws_cdk.aws_events.IRuleTarget] = None,
    ) -> aws_cdk.aws_events.Rule:
        """Defines a CloudWatch event rule triggered when something happens with this project.

        :param id: -
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        see
        :see: https://docs.aws.amazon.com/codebuild/latest/userguide/sample-build-notifications.html
        """
        options = aws_cdk.aws_events.OnEventOptions(
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
            target=target,
        )

        return jsii.invoke(self, "onEvent", [id, options])

    @jsii.member(jsii_name="onPhaseChange")
    def on_phase_change(
        self,
        id: str,
        *,
        description: typing.Optional[str] = None,
        event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern] = None,
        rule_name: typing.Optional[str] = None,
        target: typing.Optional[aws_cdk.aws_events.IRuleTarget] = None,
    ) -> aws_cdk.aws_events.Rule:
        """Defines a CloudWatch event rule that triggers upon phase change of this build project.

        :param id: -
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        see
        :see: https://docs.aws.amazon.com/codebuild/latest/userguide/sample-build-notifications.html
        """
        options = aws_cdk.aws_events.OnEventOptions(
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
            target=target,
        )

        return jsii.invoke(self, "onPhaseChange", [id, options])

    @jsii.member(jsii_name="onStateChange")
    def on_state_change(
        self,
        id: str,
        *,
        description: typing.Optional[str] = None,
        event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern] = None,
        rule_name: typing.Optional[str] = None,
        target: typing.Optional[aws_cdk.aws_events.IRuleTarget] = None,
    ) -> aws_cdk.aws_events.Rule:
        """Defines a CloudWatch event rule triggered when the build project state changes.

        You can filter specific build status events using an event
        pattern filter on the ``build-status`` detail field::

           const rule = project.onStateChange('OnBuildStarted', { target });
           rule.addEventPattern({
             detail: {
               'build-status': [
                 "IN_PROGRESS",
                 "SUCCEEDED",
                 "FAILED",
                 "STOPPED"
               ]
             }
           });

        You can also use the methods ``onBuildFailed`` and ``onBuildSucceeded`` to define rules for
        these specific state changes.

        To access fields from the event in the event target input,
        use the static fields on the ``StateChangeEvent`` class.

        :param id: -
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        see
        :see: https://docs.aws.amazon.com/codebuild/latest/userguide/sample-build-notifications.html
        """
        options = aws_cdk.aws_events.OnEventOptions(
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
            target=target,
        )

        return jsii.invoke(self, "onStateChange", [id, options])

    @jsii.member(jsii_name="validate")
    def _validate(self) -> typing.List[str]:
        """Validate the current construct.

        This method can be implemented by derived constructs in order to perform
        validation logic. It is called on all constructs before synthesis.

        override:
        :override:: true
        """
        return jsii.invoke(self, "validate", [])

    @builtins.property
    @jsii.member(jsii_name="connections")
    def connections(self) -> aws_cdk.aws_ec2.Connections:
        """Access the Connections object.

        Will fail if this Project does not have a VPC set.
        """
        return jsii.get(self, "connections")

    @builtins.property
    @jsii.member(jsii_name="grantPrincipal")
    def grant_principal(self) -> aws_cdk.aws_iam.IPrincipal:
        """The principal to grant permissions to."""
        return jsii.get(self, "grantPrincipal")

    @builtins.property
    @jsii.member(jsii_name="projectArn")
    def project_arn(self) -> str:
        """The ARN of the project."""
        return jsii.get(self, "projectArn")

    @builtins.property
    @jsii.member(jsii_name="projectName")
    def project_name(self) -> str:
        """The name of the project."""
        return jsii.get(self, "projectName")

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """The IAM role for this project."""
        return jsii.get(self, "role")


@jsii.data_type(
    jsii_type="@aws-cdk/aws-codebuild.ProjectProps",
    jsii_struct_bases=[CommonProjectProps],
    name_mapping={
        "allow_all_outbound": "allowAllOutbound",
        "badge": "badge",
        "build_spec": "buildSpec",
        "cache": "cache",
        "description": "description",
        "encryption_key": "encryptionKey",
        "environment": "environment",
        "environment_variables": "environmentVariables",
        "file_system_locations": "fileSystemLocations",
        "grant_report_group_permissions": "grantReportGroupPermissions",
        "project_name": "projectName",
        "role": "role",
        "security_groups": "securityGroups",
        "subnet_selection": "subnetSelection",
        "timeout": "timeout",
        "vpc": "vpc",
        "artifacts": "artifacts",
        "secondary_artifacts": "secondaryArtifacts",
        "secondary_sources": "secondarySources",
        "source": "source",
    },
)
class ProjectProps(CommonProjectProps):
    def __init__(
        self,
        *,
        allow_all_outbound: typing.Optional[bool] = None,
        badge: typing.Optional[bool] = None,
        build_spec: typing.Optional["BuildSpec"] = None,
        cache: typing.Optional["Cache"] = None,
        description: typing.Optional[str] = None,
        encryption_key: typing.Optional[aws_cdk.aws_kms.IKey] = None,
        environment: typing.Optional["BuildEnvironment"] = None,
        environment_variables: typing.Optional[
            typing.Mapping[str, "BuildEnvironmentVariable"]
        ] = None,
        file_system_locations: typing.Optional[
            typing.List["IFileSystemLocation"]
        ] = None,
        grant_report_group_permissions: typing.Optional[bool] = None,
        project_name: typing.Optional[str] = None,
        role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
        security_groups: typing.Optional[
            typing.List[aws_cdk.aws_ec2.ISecurityGroup]
        ] = None,
        subnet_selection: typing.Optional[aws_cdk.aws_ec2.SubnetSelection] = None,
        timeout: typing.Optional[aws_cdk.core.Duration] = None,
        vpc: typing.Optional[aws_cdk.aws_ec2.IVpc] = None,
        artifacts: typing.Optional["IArtifacts"] = None,
        secondary_artifacts: typing.Optional[typing.List["IArtifacts"]] = None,
        secondary_sources: typing.Optional[typing.List["ISource"]] = None,
        source: typing.Optional["ISource"] = None,
    ) -> None:
        """
        :param allow_all_outbound: Whether to allow the CodeBuild to send all network traffic. If set to false, you must individually add traffic rules to allow the CodeBuild project to connect to network targets. Only used if 'vpc' is supplied. Default: true
        :param badge: Indicates whether AWS CodeBuild generates a publicly accessible URL for your project's build badge. For more information, see Build Badges Sample in the AWS CodeBuild User Guide. Default: false
        :param build_spec: Filename or contents of buildspec in JSON format. Default: - Empty buildspec.
        :param cache: Caching strategy to use. Default: Cache.none
        :param description: A description of the project. Use the description to identify the purpose of the project. Default: - No description.
        :param encryption_key: Encryption key to use to read and write artifacts. Default: - The AWS-managed CMK for Amazon Simple Storage Service (Amazon S3) is used.
        :param environment: Build environment to use for the build. Default: BuildEnvironment.LinuxBuildImage.STANDARD_1_0
        :param environment_variables: Additional environment variables to add to the build environment. Default: - No additional environment variables are specified.
        :param file_system_locations: An ProjectFileSystemLocation objects for a CodeBuild build project. A ProjectFileSystemLocation object specifies the identifier, location, mountOptions, mountPoint, and type of a file system created using Amazon Elastic File System. Default: - no file system locations
        :param grant_report_group_permissions: Add permissions to this project's role to create and use test report groups with name starting with the name of this project. That is the standard report group that gets created when a simple name (in contrast to an ARN) is used in the 'reports' section of the buildspec of this project. This is usually harmless, but you can turn these off if you don't plan on using test reports in this project. Default: true
        :param project_name: The physical, human-readable name of the CodeBuild Project. Default: - Name is automatically generated.
        :param role: Service Role to assume while running the build. Default: - A role will be created.
        :param security_groups: What security group to associate with the codebuild project's network interfaces. If no security group is identified, one will be created automatically. Only used if 'vpc' is supplied. Default: - Security group will be automatically created.
        :param subnet_selection: Where to place the network interfaces within the VPC. Only used if 'vpc' is supplied. Default: - All private subnets.
        :param timeout: The number of minutes after which AWS CodeBuild stops the build if it's not complete. For valid values, see the timeoutInMinutes field in the AWS CodeBuild User Guide. Default: Duration.hours(1)
        :param vpc: VPC network to place codebuild network interfaces. Specify this if the codebuild project needs to access resources in a VPC. Default: - No VPC is specified.
        :param artifacts: Defines where build artifacts will be stored. Could be: PipelineBuildArtifacts, NoArtifacts and S3Artifacts. Default: NoArtifacts
        :param secondary_artifacts: The secondary artifacts for the Project. Can also be added after the Project has been created by using the {@link Project#addSecondaryArtifact} method. Default: - No secondary artifacts.
        :param secondary_sources: The secondary sources for the Project. Can be also added after the Project has been created by using the {@link Project#addSecondarySource} method. Default: - No secondary sources.
        :param source: The source of the build. *Note*: if {@link NoSource} is given as the source, then you need to provide an explicit ``buildSpec``. Default: - NoSource
        """
        if isinstance(environment, dict):
            environment = BuildEnvironment(**environment)
        if isinstance(subnet_selection, dict):
            subnet_selection = aws_cdk.aws_ec2.SubnetSelection(**subnet_selection)
        self._values = {}
        if allow_all_outbound is not None:
            self._values["allow_all_outbound"] = allow_all_outbound
        if badge is not None:
            self._values["badge"] = badge
        if build_spec is not None:
            self._values["build_spec"] = build_spec
        if cache is not None:
            self._values["cache"] = cache
        if description is not None:
            self._values["description"] = description
        if encryption_key is not None:
            self._values["encryption_key"] = encryption_key
        if environment is not None:
            self._values["environment"] = environment
        if environment_variables is not None:
            self._values["environment_variables"] = environment_variables
        if file_system_locations is not None:
            self._values["file_system_locations"] = file_system_locations
        if grant_report_group_permissions is not None:
            self._values[
                "grant_report_group_permissions"
            ] = grant_report_group_permissions
        if project_name is not None:
            self._values["project_name"] = project_name
        if role is not None:
            self._values["role"] = role
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if subnet_selection is not None:
            self._values["subnet_selection"] = subnet_selection
        if timeout is not None:
            self._values["timeout"] = timeout
        if vpc is not None:
            self._values["vpc"] = vpc
        if artifacts is not None:
            self._values["artifacts"] = artifacts
        if secondary_artifacts is not None:
            self._values["secondary_artifacts"] = secondary_artifacts
        if secondary_sources is not None:
            self._values["secondary_sources"] = secondary_sources
        if source is not None:
            self._values["source"] = source

    @builtins.property
    def allow_all_outbound(self) -> typing.Optional[bool]:
        """Whether to allow the CodeBuild to send all network traffic.

        If set to false, you must individually add traffic rules to allow the
        CodeBuild project to connect to network targets.

        Only used if 'vpc' is supplied.

        default
        :default: true
        """
        return self._values.get("allow_all_outbound")

    @builtins.property
    def badge(self) -> typing.Optional[bool]:
        """Indicates whether AWS CodeBuild generates a publicly accessible URL for your project's build badge.

        For more information, see Build Badges Sample
        in the AWS CodeBuild User Guide.

        default
        :default: false
        """
        return self._values.get("badge")

    @builtins.property
    def build_spec(self) -> typing.Optional["BuildSpec"]:
        """Filename or contents of buildspec in JSON format.

        default
        :default: - Empty buildspec.

        see
        :see: https://docs.aws.amazon.com/codebuild/latest/userguide/build-spec-ref.html#build-spec-ref-example
        """
        return self._values.get("build_spec")

    @builtins.property
    def cache(self) -> typing.Optional["Cache"]:
        """Caching strategy to use.

        default
        :default: Cache.none
        """
        return self._values.get("cache")

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """A description of the project.

        Use the description to identify the purpose
        of the project.

        default
        :default: - No description.
        """
        return self._values.get("description")

    @builtins.property
    def encryption_key(self) -> typing.Optional[aws_cdk.aws_kms.IKey]:
        """Encryption key to use to read and write artifacts.

        default
        :default: - The AWS-managed CMK for Amazon Simple Storage Service (Amazon S3) is used.
        """
        return self._values.get("encryption_key")

    @builtins.property
    def environment(self) -> typing.Optional["BuildEnvironment"]:
        """Build environment to use for the build.

        default
        :default: BuildEnvironment.LinuxBuildImage.STANDARD_1_0
        """
        return self._values.get("environment")

    @builtins.property
    def environment_variables(
        self,
    ) -> typing.Optional[typing.Mapping[str, "BuildEnvironmentVariable"]]:
        """Additional environment variables to add to the build environment.

        default
        :default: - No additional environment variables are specified.
        """
        return self._values.get("environment_variables")

    @builtins.property
    def file_system_locations(
        self,
    ) -> typing.Optional[typing.List["IFileSystemLocation"]]:
        """An  ProjectFileSystemLocation objects for a CodeBuild build project.

        A ProjectFileSystemLocation object specifies the identifier, location, mountOptions, mountPoint,
        and type of a file system created using Amazon Elastic File System.

        default
        :default: - no file system locations
        """
        return self._values.get("file_system_locations")

    @builtins.property
    def grant_report_group_permissions(self) -> typing.Optional[bool]:
        """Add permissions to this project's role to create and use test report groups with name starting with the name of this project.

        That is the standard report group that gets created when a simple name
        (in contrast to an ARN)
        is used in the 'reports' section of the buildspec of this project.
        This is usually harmless, but you can turn these off if you don't plan on using test
        reports in this project.

        default
        :default: true

        see
        :see: https://docs.aws.amazon.com/codebuild/latest/userguide/test-report-group-naming.html
        """
        return self._values.get("grant_report_group_permissions")

    @builtins.property
    def project_name(self) -> typing.Optional[str]:
        """The physical, human-readable name of the CodeBuild Project.

        default
        :default: - Name is automatically generated.
        """
        return self._values.get("project_name")

    @builtins.property
    def role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """Service Role to assume while running the build.

        default
        :default: - A role will be created.
        """
        return self._values.get("role")

    @builtins.property
    def security_groups(
        self,
    ) -> typing.Optional[typing.List[aws_cdk.aws_ec2.ISecurityGroup]]:
        """What security group to associate with the codebuild project's network interfaces.

        If no security group is identified, one will be created automatically.

        Only used if 'vpc' is supplied.

        default
        :default: - Security group will be automatically created.
        """
        return self._values.get("security_groups")

    @builtins.property
    def subnet_selection(self) -> typing.Optional[aws_cdk.aws_ec2.SubnetSelection]:
        """Where to place the network interfaces within the VPC.

        Only used if 'vpc' is supplied.

        default
        :default: - All private subnets.
        """
        return self._values.get("subnet_selection")

    @builtins.property
    def timeout(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The number of minutes after which AWS CodeBuild stops the build if it's not complete.

        For valid values, see the timeoutInMinutes field in the AWS
        CodeBuild User Guide.

        default
        :default: Duration.hours(1)
        """
        return self._values.get("timeout")

    @builtins.property
    def vpc(self) -> typing.Optional[aws_cdk.aws_ec2.IVpc]:
        """VPC network to place codebuild network interfaces.

        Specify this if the codebuild project needs to access resources in a VPC.

        default
        :default: - No VPC is specified.
        """
        return self._values.get("vpc")

    @builtins.property
    def artifacts(self) -> typing.Optional["IArtifacts"]:
        """Defines where build artifacts will be stored.

        Could be: PipelineBuildArtifacts, NoArtifacts and S3Artifacts.

        default
        :default: NoArtifacts
        """
        return self._values.get("artifacts")

    @builtins.property
    def secondary_artifacts(self) -> typing.Optional[typing.List["IArtifacts"]]:
        """The secondary artifacts for the Project.

        Can also be added after the Project has been created by using the {@link Project#addSecondaryArtifact} method.

        default
        :default: - No secondary artifacts.

        see
        :see: https://docs.aws.amazon.com/codebuild/latest/userguide/sample-multi-in-out.html
        """
        return self._values.get("secondary_artifacts")

    @builtins.property
    def secondary_sources(self) -> typing.Optional[typing.List["ISource"]]:
        """The secondary sources for the Project.

        Can be also added after the Project has been created by using the {@link Project#addSecondarySource} method.

        default
        :default: - No secondary sources.

        see
        :see: https://docs.aws.amazon.com/codebuild/latest/userguide/sample-multi-in-out.html
        """
        return self._values.get("secondary_sources")

    @builtins.property
    def source(self) -> typing.Optional["ISource"]:
        """The source of the build.

        *Note*: if {@link NoSource} is given as the source,
        then you need to provide an explicit ``buildSpec``.

        default
        :default: - NoSource
        """
        return self._values.get("source")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProjectProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IReportGroup)
class ReportGroup(
    aws_cdk.core.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-codebuild.ReportGroup",
):
    """The ReportGroup resource class."""

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: str,
        *,
        export_bucket: typing.Optional[aws_cdk.aws_s3.IBucket] = None,
        removal_policy: typing.Optional[aws_cdk.core.RemovalPolicy] = None,
        report_group_name: typing.Optional[str] = None,
        zip_export: typing.Optional[bool] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param export_bucket: An optional S3 bucket to export the reports to. Default: - the reports will not be exported
        :param removal_policy: What to do when this resource is deleted from a stack. As CodeBuild does not allow deleting a ResourceGroup that has reports inside of it, this is set to retain the resource by default. Default: RemovalPolicy.RETAIN
        :param report_group_name: The physical name of the report group. Default: - CloudFormation-generated name
        :param zip_export: Whether to output the report files into the export bucket as-is, or create a ZIP from them before doing the export. Ignored if {@link exportBucket} has not been provided. Default: - false (the files will not be ZIPped)
        """
        props = ReportGroupProps(
            export_bucket=export_bucket,
            removal_policy=removal_policy,
            report_group_name=report_group_name,
            zip_export=zip_export,
        )

        jsii.create(ReportGroup, self, [scope, id, props])

    @jsii.member(jsii_name="fromReportGroupName")
    @builtins.classmethod
    def from_report_group_name(
        cls, scope: aws_cdk.core.Construct, id: str, report_group_name: str
    ) -> "IReportGroup":
        """Reference an existing ReportGroup, defined outside of the CDK code, by name.

        :param scope: -
        :param id: -
        :param report_group_name: -
        """
        return jsii.sinvoke(cls, "fromReportGroupName", [scope, id, report_group_name])

    @jsii.member(jsii_name="grantWrite")
    def grant_write(
        self, identity: aws_cdk.aws_iam.IGrantable
    ) -> aws_cdk.aws_iam.Grant:
        """Grants the given entity permissions to write (that is, upload reports to) this report group.

        :param identity: -
        """
        return jsii.invoke(self, "grantWrite", [identity])

    @builtins.property
    @jsii.member(jsii_name="reportGroupArn")
    def report_group_arn(self) -> str:
        """The ARN of the ReportGroup."""
        return jsii.get(self, "reportGroupArn")

    @builtins.property
    @jsii.member(jsii_name="reportGroupName")
    def report_group_name(self) -> str:
        """The name of the ReportGroup."""
        return jsii.get(self, "reportGroupName")

    @builtins.property
    @jsii.member(jsii_name="exportBucket")
    def _export_bucket(self) -> typing.Optional[aws_cdk.aws_s3.IBucket]:
        return jsii.get(self, "exportBucket")


@jsii.data_type(
    jsii_type="@aws-cdk/aws-codebuild.ReportGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "export_bucket": "exportBucket",
        "removal_policy": "removalPolicy",
        "report_group_name": "reportGroupName",
        "zip_export": "zipExport",
    },
)
class ReportGroupProps:
    def __init__(
        self,
        *,
        export_bucket: typing.Optional[aws_cdk.aws_s3.IBucket] = None,
        removal_policy: typing.Optional[aws_cdk.core.RemovalPolicy] = None,
        report_group_name: typing.Optional[str] = None,
        zip_export: typing.Optional[bool] = None,
    ) -> None:
        """Construction properties for {@link ReportGroup}.

        :param export_bucket: An optional S3 bucket to export the reports to. Default: - the reports will not be exported
        :param removal_policy: What to do when this resource is deleted from a stack. As CodeBuild does not allow deleting a ResourceGroup that has reports inside of it, this is set to retain the resource by default. Default: RemovalPolicy.RETAIN
        :param report_group_name: The physical name of the report group. Default: - CloudFormation-generated name
        :param zip_export: Whether to output the report files into the export bucket as-is, or create a ZIP from them before doing the export. Ignored if {@link exportBucket} has not been provided. Default: - false (the files will not be ZIPped)
        """
        self._values = {}
        if export_bucket is not None:
            self._values["export_bucket"] = export_bucket
        if removal_policy is not None:
            self._values["removal_policy"] = removal_policy
        if report_group_name is not None:
            self._values["report_group_name"] = report_group_name
        if zip_export is not None:
            self._values["zip_export"] = zip_export

    @builtins.property
    def export_bucket(self) -> typing.Optional[aws_cdk.aws_s3.IBucket]:
        """An optional S3 bucket to export the reports to.

        default
        :default: - the reports will not be exported
        """
        return self._values.get("export_bucket")

    @builtins.property
    def removal_policy(self) -> typing.Optional[aws_cdk.core.RemovalPolicy]:
        """What to do when this resource is deleted from a stack.

        As CodeBuild does not allow deleting a ResourceGroup that has reports inside of it,
        this is set to retain the resource by default.

        default
        :default: RemovalPolicy.RETAIN
        """
        return self._values.get("removal_policy")

    @builtins.property
    def report_group_name(self) -> typing.Optional[str]:
        """The physical name of the report group.

        default
        :default: - CloudFormation-generated name
        """
        return self._values.get("report_group_name")

    @builtins.property
    def zip_export(self) -> typing.Optional[bool]:
        """Whether to output the report files into the export bucket as-is, or create a ZIP from them before doing the export.

        Ignored if {@link exportBucket} has not been provided.

        default
        :default: - false (the files will not be ZIPped)
        """
        return self._values.get("zip_export")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ReportGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-codebuild.S3ArtifactsProps",
    jsii_struct_bases=[ArtifactsProps],
    name_mapping={
        "identifier": "identifier",
        "bucket": "bucket",
        "encryption": "encryption",
        "include_build_id": "includeBuildId",
        "name": "name",
        "package_zip": "packageZip",
        "path": "path",
    },
)
class S3ArtifactsProps(ArtifactsProps):
    def __init__(
        self,
        *,
        identifier: typing.Optional[str] = None,
        bucket: aws_cdk.aws_s3.IBucket,
        encryption: typing.Optional[bool] = None,
        include_build_id: typing.Optional[bool] = None,
        name: typing.Optional[str] = None,
        package_zip: typing.Optional[bool] = None,
        path: typing.Optional[str] = None,
    ) -> None:
        """Construction properties for {@link S3Artifacts}.

        :param identifier: The artifact identifier. This property is required on secondary artifacts.
        :param bucket: The name of the output bucket.
        :param encryption: If this is false, build output will not be encrypted. This is useful if the artifact to publish a static website or sharing content with others Default: true - output will be encrypted
        :param include_build_id: Indicates if the build ID should be included in the path. If this is set to true, then the build artifact will be stored in "//". Default: true
        :param name: The name of the build output ZIP file or folder inside the bucket. The full S3 object key will be "//" or "/" depending on whether ``includeBuildId`` is set to true. If not set, ``overrideArtifactName`` will be set and the name from the buildspec will be used instead. Default: undefined, and use the name from the buildspec
        :param package_zip: If this is true, all build output will be packaged into a single .zip file. Otherwise, all files will be uploaded to /. Default: true - files will be archived
        :param path: The path inside of the bucket for the build output .zip file or folder. If a value is not specified, then build output will be stored at the root of the bucket (or under the directory if ``includeBuildId`` is set to true). Default: the root of the bucket
        """
        self._values = {
            "bucket": bucket,
        }
        if identifier is not None:
            self._values["identifier"] = identifier
        if encryption is not None:
            self._values["encryption"] = encryption
        if include_build_id is not None:
            self._values["include_build_id"] = include_build_id
        if name is not None:
            self._values["name"] = name
        if package_zip is not None:
            self._values["package_zip"] = package_zip
        if path is not None:
            self._values["path"] = path

    @builtins.property
    def identifier(self) -> typing.Optional[str]:
        """The artifact identifier.

        This property is required on secondary artifacts.
        """
        return self._values.get("identifier")

    @builtins.property
    def bucket(self) -> aws_cdk.aws_s3.IBucket:
        """The name of the output bucket."""
        return self._values.get("bucket")

    @builtins.property
    def encryption(self) -> typing.Optional[bool]:
        """If this is false, build output will not be encrypted.

        This is useful if the artifact to publish a static website or sharing content with others

        default
        :default: true - output will be encrypted
        """
        return self._values.get("encryption")

    @builtins.property
    def include_build_id(self) -> typing.Optional[bool]:
        """Indicates if the build ID should be included in the path.

        If this is set to true,
        then the build artifact will be stored in "//".

        default
        :default: true
        """
        return self._values.get("include_build_id")

    @builtins.property
    def name(self) -> typing.Optional[str]:
        """The name of the build output ZIP file or folder inside the bucket.

        The full S3 object key will be "//" or
        "/" depending on whether ``includeBuildId`` is set to true.

        If not set, ``overrideArtifactName`` will be set and the name from the
        buildspec will be used instead.

        default
        :default: undefined, and use the name from the buildspec
        """
        return self._values.get("name")

    @builtins.property
    def package_zip(self) -> typing.Optional[bool]:
        """If this is true, all build output will be packaged into a single .zip file. Otherwise, all files will be uploaded to /.

        default
        :default: true - files will be archived
        """
        return self._values.get("package_zip")

    @builtins.property
    def path(self) -> typing.Optional[str]:
        """The path inside of the bucket for the build output .zip file or folder. If a value is not specified, then build output will be stored at the root of the bucket (or under the  directory if ``includeBuildId`` is set to true).

        default
        :default: the root of the bucket
        """
        return self._values.get("path")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3ArtifactsProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(ISource)
class Source(
    metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-codebuild.Source"
):
    """Source provider definition for a CodeBuild Project."""

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _SourceProxy

    def __init__(self, *, identifier: typing.Optional[str] = None) -> None:
        """
        :param identifier: The source identifier. This property is required on secondary sources.
        """
        props = SourceProps(identifier=identifier)

        jsii.create(Source, self, [props])

    @jsii.member(jsii_name="bitBucket")
    @builtins.classmethod
    def bit_bucket(
        cls,
        *,
        owner: str,
        repo: str,
        branch_or_ref: typing.Optional[str] = None,
        clone_depth: typing.Optional[jsii.Number] = None,
        report_build_status: typing.Optional[bool] = None,
        webhook: typing.Optional[bool] = None,
        webhook_filters: typing.Optional[typing.List["FilterGroup"]] = None,
        identifier: typing.Optional[str] = None,
    ) -> "ISource":
        """
        :param owner: The BitBucket account/user that owns the repo.
        :param repo: The name of the repo (without the username).
        :param branch_or_ref: The commit ID, pull request ID, branch name, or tag name that corresponds to the version of the source code you want to build. Default: the default branch's HEAD commit ID is used
        :param clone_depth: The depth of history to download. Minimum value is 0. If this value is 0, greater than 25, or not provided, then the full history is downloaded with each build of the project.
        :param report_build_status: Whether to send notifications on your build's start and end. Default: true
        :param webhook: Whether to create a webhook that will trigger a build every time an event happens in the repository. Default: true if any ``webhookFilters`` were provided, false otherwise
        :param webhook_filters: A list of webhook filters that can constraint what events in the repository will trigger a build. A build is triggered if any of the provided filter groups match. Only valid if ``webhook`` was not provided as false. Default: every push and every Pull Request (create or update) triggers a build
        :param identifier: The source identifier. This property is required on secondary sources.
        """
        props = BitBucketSourceProps(
            owner=owner,
            repo=repo,
            branch_or_ref=branch_or_ref,
            clone_depth=clone_depth,
            report_build_status=report_build_status,
            webhook=webhook,
            webhook_filters=webhook_filters,
            identifier=identifier,
        )

        return jsii.sinvoke(cls, "bitBucket", [props])

    @jsii.member(jsii_name="codeCommit")
    @builtins.classmethod
    def code_commit(
        cls,
        *,
        repository: aws_cdk.aws_codecommit.IRepository,
        branch_or_ref: typing.Optional[str] = None,
        clone_depth: typing.Optional[jsii.Number] = None,
        identifier: typing.Optional[str] = None,
    ) -> "ISource":
        """
        :param repository: 
        :param branch_or_ref: The commit ID, pull request ID, branch name, or tag name that corresponds to the version of the source code you want to build. Default: the default branch's HEAD commit ID is used
        :param clone_depth: The depth of history to download. Minimum value is 0. If this value is 0, greater than 25, or not provided, then the full history is downloaded with each build of the project.
        :param identifier: The source identifier. This property is required on secondary sources.
        """
        props = CodeCommitSourceProps(
            repository=repository,
            branch_or_ref=branch_or_ref,
            clone_depth=clone_depth,
            identifier=identifier,
        )

        return jsii.sinvoke(cls, "codeCommit", [props])

    @jsii.member(jsii_name="gitHub")
    @builtins.classmethod
    def git_hub(
        cls,
        *,
        owner: str,
        repo: str,
        branch_or_ref: typing.Optional[str] = None,
        clone_depth: typing.Optional[jsii.Number] = None,
        report_build_status: typing.Optional[bool] = None,
        webhook: typing.Optional[bool] = None,
        webhook_filters: typing.Optional[typing.List["FilterGroup"]] = None,
        identifier: typing.Optional[str] = None,
    ) -> "ISource":
        """
        :param owner: The GitHub account/user that owns the repo.
        :param repo: The name of the repo (without the username).
        :param branch_or_ref: The commit ID, pull request ID, branch name, or tag name that corresponds to the version of the source code you want to build. Default: the default branch's HEAD commit ID is used
        :param clone_depth: The depth of history to download. Minimum value is 0. If this value is 0, greater than 25, or not provided, then the full history is downloaded with each build of the project.
        :param report_build_status: Whether to send notifications on your build's start and end. Default: true
        :param webhook: Whether to create a webhook that will trigger a build every time an event happens in the repository. Default: true if any ``webhookFilters`` were provided, false otherwise
        :param webhook_filters: A list of webhook filters that can constraint what events in the repository will trigger a build. A build is triggered if any of the provided filter groups match. Only valid if ``webhook`` was not provided as false. Default: every push and every Pull Request (create or update) triggers a build
        :param identifier: The source identifier. This property is required on secondary sources.
        """
        props = GitHubSourceProps(
            owner=owner,
            repo=repo,
            branch_or_ref=branch_or_ref,
            clone_depth=clone_depth,
            report_build_status=report_build_status,
            webhook=webhook,
            webhook_filters=webhook_filters,
            identifier=identifier,
        )

        return jsii.sinvoke(cls, "gitHub", [props])

    @jsii.member(jsii_name="gitHubEnterprise")
    @builtins.classmethod
    def git_hub_enterprise(
        cls,
        *,
        https_clone_url: str,
        branch_or_ref: typing.Optional[str] = None,
        clone_depth: typing.Optional[jsii.Number] = None,
        ignore_ssl_errors: typing.Optional[bool] = None,
        report_build_status: typing.Optional[bool] = None,
        webhook: typing.Optional[bool] = None,
        webhook_filters: typing.Optional[typing.List["FilterGroup"]] = None,
        identifier: typing.Optional[str] = None,
    ) -> "ISource":
        """
        :param https_clone_url: The HTTPS URL of the repository in your GitHub Enterprise installation.
        :param branch_or_ref: The commit ID, pull request ID, branch name, or tag name that corresponds to the version of the source code you want to build. Default: the default branch's HEAD commit ID is used
        :param clone_depth: The depth of history to download. Minimum value is 0. If this value is 0, greater than 25, or not provided, then the full history is downloaded with each build of the project.
        :param ignore_ssl_errors: Whether to ignore SSL errors when connecting to the repository. Default: false
        :param report_build_status: Whether to send notifications on your build's start and end. Default: true
        :param webhook: Whether to create a webhook that will trigger a build every time an event happens in the repository. Default: true if any ``webhookFilters`` were provided, false otherwise
        :param webhook_filters: A list of webhook filters that can constraint what events in the repository will trigger a build. A build is triggered if any of the provided filter groups match. Only valid if ``webhook`` was not provided as false. Default: every push and every Pull Request (create or update) triggers a build
        :param identifier: The source identifier. This property is required on secondary sources.
        """
        props = GitHubEnterpriseSourceProps(
            https_clone_url=https_clone_url,
            branch_or_ref=branch_or_ref,
            clone_depth=clone_depth,
            ignore_ssl_errors=ignore_ssl_errors,
            report_build_status=report_build_status,
            webhook=webhook,
            webhook_filters=webhook_filters,
            identifier=identifier,
        )

        return jsii.sinvoke(cls, "gitHubEnterprise", [props])

    @jsii.member(jsii_name="s3")
    @builtins.classmethod
    def s3(
        cls,
        *,
        bucket: aws_cdk.aws_s3.IBucket,
        path: str,
        version: typing.Optional[str] = None,
        identifier: typing.Optional[str] = None,
    ) -> "ISource":
        """
        :param bucket: 
        :param path: 
        :param version: The version ID of the object that represents the build input ZIP file to use. Default: latest
        :param identifier: The source identifier. This property is required on secondary sources.
        """
        props = S3SourceProps(
            bucket=bucket, path=path, version=version, identifier=identifier
        )

        return jsii.sinvoke(cls, "s3", [props])

    @jsii.member(jsii_name="bind")
    def bind(
        self, _scope: aws_cdk.core.Construct, _project: "IProject"
    ) -> "SourceConfig":
        """Called by the project when the source is added so that the source can perform binding operations on the source.

        For example, it can grant permissions to the
        code build project to read from the S3 bucket.

        :param _scope: -
        :param _project: -
        """
        return jsii.invoke(self, "bind", [_scope, _project])

    @builtins.property
    @jsii.member(jsii_name="badgeSupported")
    def badge_supported(self) -> bool:
        return jsii.get(self, "badgeSupported")

    @builtins.property
    @jsii.member(jsii_name="type")
    @abc.abstractmethod
    def type(self) -> str:
        ...

    @builtins.property
    @jsii.member(jsii_name="identifier")
    def identifier(self) -> typing.Optional[str]:
        return jsii.get(self, "identifier")


class _SourceProxy(Source):
    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> str:
        return jsii.get(self, "type")


@jsii.data_type(
    jsii_type="@aws-cdk/aws-codebuild.SourceConfig",
    jsii_struct_bases=[],
    name_mapping={
        "source_property": "sourceProperty",
        "build_triggers": "buildTriggers",
        "source_version": "sourceVersion",
    },
)
class SourceConfig:
    def __init__(
        self,
        *,
        source_property: "CfnProject.SourceProperty",
        build_triggers: typing.Optional["CfnProject.ProjectTriggersProperty"] = None,
        source_version: typing.Optional[str] = None,
    ) -> None:
        """The type returned from {@link ISource#bind}.

        :param source_property: 
        :param build_triggers: 
        :param source_version: ``AWS::CodeBuild::Project.SourceVersion``. Default: the latest version
        """
        if isinstance(source_property, dict):
            source_property = CfnProject.SourceProperty(**source_property)
        if isinstance(build_triggers, dict):
            build_triggers = CfnProject.ProjectTriggersProperty(**build_triggers)
        self._values = {
            "source_property": source_property,
        }
        if build_triggers is not None:
            self._values["build_triggers"] = build_triggers
        if source_version is not None:
            self._values["source_version"] = source_version

    @builtins.property
    def source_property(self) -> "CfnProject.SourceProperty":
        return self._values.get("source_property")

    @builtins.property
    def build_triggers(self) -> typing.Optional["CfnProject.ProjectTriggersProperty"]:
        return self._values.get("build_triggers")

    @builtins.property
    def source_version(self) -> typing.Optional[str]:
        """``AWS::CodeBuild::Project.SourceVersion``.

        default
        :default: the latest version

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-sourceversion
        """
        return self._values.get("source_version")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SourceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-codebuild.SourceProps",
    jsii_struct_bases=[],
    name_mapping={"identifier": "identifier"},
)
class SourceProps:
    def __init__(self, *, identifier: typing.Optional[str] = None) -> None:
        """Properties common to all Source classes.

        :param identifier: The source identifier. This property is required on secondary sources.
        """
        self._values = {}
        if identifier is not None:
            self._values["identifier"] = identifier

    @builtins.property
    def identifier(self) -> typing.Optional[str]:
        """The source identifier.

        This property is required on secondary sources.
        """
        return self._values.get("identifier")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SourceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StateChangeEvent(
    metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codebuild.StateChangeEvent"
):
    """Event fields for the CodeBuild "state change" event.

    see
    :see: https://docs.aws.amazon.com/codebuild/latest/userguide/sample-build-notifications.html#sample-build-notifications-ref
    """

    @jsii.python.classproperty
    @jsii.member(jsii_name="buildId")
    def build_id(cls) -> str:
        """Return the build id."""
        return jsii.sget(cls, "buildId")

    @jsii.python.classproperty
    @jsii.member(jsii_name="buildStatus")
    def build_status(cls) -> str:
        """The triggering build's status."""
        return jsii.sget(cls, "buildStatus")

    @jsii.python.classproperty
    @jsii.member(jsii_name="currentPhase")
    def current_phase(cls) -> str:
        return jsii.sget(cls, "currentPhase")

    @jsii.python.classproperty
    @jsii.member(jsii_name="projectName")
    def project_name(cls) -> str:
        """The triggering build's project name."""
        return jsii.sget(cls, "projectName")


@jsii.implements(IBuildImage)
class WindowsBuildImage(
    metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codebuild.WindowsBuildImage"
):
    """A CodeBuild image running Windows.

    This class has a bunch of public constants that represent the most popular images.

    You can also specify a custom image using one of the static methods:

    - WindowsBuildImage.fromDockerRegistry(image[, { secretsManagerCredentials }])
    - WindowsBuildImage.fromEcrRepository(repo[, tag])
    - WindowsBuildImage.fromAsset(parent, id, props)

    see
    :see: https://docs.aws.amazon.com/codebuild/latest/userguide/build-env-ref-available.html
    """

    @jsii.member(jsii_name="fromAsset")
    @builtins.classmethod
    def from_asset(
        cls,
        scope: aws_cdk.core.Construct,
        id: str,
        *,
        directory: str,
        build_args: typing.Optional[typing.Mapping[str, str]] = None,
        file: typing.Optional[str] = None,
        repository_name: typing.Optional[str] = None,
        target: typing.Optional[str] = None,
        extra_hash: typing.Optional[str] = None,
        exclude: typing.Optional[typing.List[str]] = None,
        follow: typing.Optional[aws_cdk.assets.FollowMode] = None,
    ) -> "IBuildImage":
        """Uses an Docker image asset as a Windows build image.

        :param scope: -
        :param id: -
        :param directory: The directory where the Dockerfile is stored.
        :param build_args: Build args to pass to the ``docker build`` command. Since Docker build arguments are resolved before deployment, keys and values cannot refer to unresolved tokens (such as ``lambda.functionArn`` or ``queue.queueUrl``). Default: - no build args are passed
        :param file: Path to the Dockerfile (relative to the directory). Default: 'Dockerfile'
        :param repository_name: ECR repository name. Specify this property if you need to statically address the image, e.g. from a Kubernetes Pod. Note, this is only the repository name, without the registry and the tag parts. Default: - the default ECR repository for CDK assets
        :param target: Docker target to build to. Default: - no target
        :param extra_hash: Extra information to encode into the fingerprint (e.g. build instructions and other inputs). Default: - hash is only based on source content
        :param exclude: Glob patterns to exclude from the copy. Default: nothing is excluded
        :param follow: A strategy for how to handle symlinks. Default: Never
        """
        props = aws_cdk.aws_ecr_assets.DockerImageAssetProps(
            directory=directory,
            build_args=build_args,
            file=file,
            repository_name=repository_name,
            target=target,
            extra_hash=extra_hash,
            exclude=exclude,
            follow=follow,
        )

        return jsii.sinvoke(cls, "fromAsset", [scope, id, props])

    @jsii.member(jsii_name="fromDockerRegistry")
    @builtins.classmethod
    def from_docker_registry(
        cls,
        name: str,
        *,
        secrets_manager_credentials: typing.Optional[
            aws_cdk.aws_secretsmanager.ISecret
        ] = None,
    ) -> "IBuildImage":
        """
        :param name: -
        :param secrets_manager_credentials: The credentials, stored in Secrets Manager, used for accessing the repository holding the image, if the repository is private. Default: no credentials will be used (we assume the repository is public)

        return
        :return: a Windows build image from a Docker Hub image.
        """
        options = DockerImageOptions(
            secrets_manager_credentials=secrets_manager_credentials
        )

        return jsii.sinvoke(cls, "fromDockerRegistry", [name, options])

    @jsii.member(jsii_name="fromEcrRepository")
    @builtins.classmethod
    def from_ecr_repository(
        cls, repository: aws_cdk.aws_ecr.IRepository, tag: typing.Optional[str] = None
    ) -> "IBuildImage":
        """
        :param repository: The ECR repository.
        :param tag: Image tag (default "latest").

        return
        :return:

        A Linux build image from an ECR repository.

        NOTE: if the repository is external (i.e. imported), then we won't be able to add
        a resource policy statement for it so CodeBuild can pull the image.

        see
        :see: https://docs.aws.amazon.com/codebuild/latest/userguide/sample-ecr.html
        """
        return jsii.sinvoke(cls, "fromEcrRepository", [repository, tag])

    @jsii.member(jsii_name="runScriptBuildspec")
    def run_script_buildspec(self, entrypoint: str) -> "BuildSpec":
        """Make a buildspec to run the indicated script.

        :param entrypoint: -
        """
        return jsii.invoke(self, "runScriptBuildspec", [entrypoint])

    @jsii.member(jsii_name="validate")
    def validate(
        self,
        *,
        build_image: typing.Optional["IBuildImage"] = None,
        compute_type: typing.Optional["ComputeType"] = None,
        environment_variables: typing.Optional[
            typing.Mapping[str, "BuildEnvironmentVariable"]
        ] = None,
        privileged: typing.Optional[bool] = None,
    ) -> typing.List[str]:
        """Allows the image a chance to validate whether the passed configuration is correct.

        :param build_image: The image used for the builds. Default: LinuxBuildImage.STANDARD_1_0
        :param compute_type: The type of compute to use for this build. See the {@link ComputeType} enum for the possible values. Default: taken from {@link #buildImage#defaultComputeType}
        :param environment_variables: The environment variables that your builds can use.
        :param privileged: Indicates how the project builds Docker images. Specify true to enable running the Docker daemon inside a Docker container. This value must be set to true only if this build project will be used to build Docker images, and the specified build environment image is not one provided by AWS CodeBuild with Docker support. Otherwise, all associated builds that attempt to interact with the Docker daemon will fail. Default: false
        """
        build_environment = BuildEnvironment(
            build_image=build_image,
            compute_type=compute_type,
            environment_variables=environment_variables,
            privileged=privileged,
        )

        return jsii.invoke(self, "validate", [build_environment])

    @jsii.python.classproperty
    @jsii.member(jsii_name="WIN_SERVER_CORE_2016_BASE")
    def WIN_SERVER_CORE_2016_BASE(cls) -> "IBuildImage":
        """Corresponds to the standard CodeBuild image ``aws/codebuild/windows-base:1.0``.

        deprecated
        :deprecated: ``WindowsBuildImage.WINDOWS_BASE_2_0`` should be used instead.

        stability
        :stability: deprecated
        """
        return jsii.sget(cls, "WIN_SERVER_CORE_2016_BASE")

    @jsii.python.classproperty
    @jsii.member(jsii_name="WINDOWS_BASE_2_0")
    def WINDOWS_BASE_2_0(cls) -> "IBuildImage":
        """The standard CodeBuild image ``aws/codebuild/windows-base:2.0``, which is based off Windows Server Core 2016."""
        return jsii.sget(cls, "WINDOWS_BASE_2_0")

    @builtins.property
    @jsii.member(jsii_name="defaultComputeType")
    def default_compute_type(self) -> "ComputeType":
        """The default {@link ComputeType} to use with this image, if one was not specified in {@link BuildEnvironment#computeType} explicitly."""
        return jsii.get(self, "defaultComputeType")

    @builtins.property
    @jsii.member(jsii_name="imageId")
    def image_id(self) -> str:
        """The Docker image identifier that the build environment uses."""
        return jsii.get(self, "imageId")

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> str:
        """The type of build environment."""
        return jsii.get(self, "type")

    @builtins.property
    @jsii.member(jsii_name="imagePullPrincipalType")
    def image_pull_principal_type(self) -> typing.Optional["ImagePullPrincipalType"]:
        """The type of principal that CodeBuild will use to pull this build Docker image."""
        return jsii.get(self, "imagePullPrincipalType")

    @builtins.property
    @jsii.member(jsii_name="repository")
    def repository(self) -> typing.Optional[aws_cdk.aws_ecr.IRepository]:
        """An optional ECR repository that the image is hosted in."""
        return jsii.get(self, "repository")

    @builtins.property
    @jsii.member(jsii_name="secretsManagerCredentials")
    def secrets_manager_credentials(
        self,
    ) -> typing.Optional[aws_cdk.aws_secretsmanager.ISecret]:
        """The secretsManagerCredentials for access to a private registry."""
        return jsii.get(self, "secretsManagerCredentials")


@jsii.implements(IArtifacts)
class Artifacts(
    metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-codebuild.Artifacts"
):
    """Artifacts definition for a CodeBuild Project."""

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _ArtifactsProxy

    def __init__(self, *, identifier: typing.Optional[str] = None) -> None:
        """
        :param identifier: The artifact identifier. This property is required on secondary artifacts.
        """
        props = ArtifactsProps(identifier=identifier)

        jsii.create(Artifacts, self, [props])

    @jsii.member(jsii_name="s3")
    @builtins.classmethod
    def s3(
        cls,
        *,
        bucket: aws_cdk.aws_s3.IBucket,
        encryption: typing.Optional[bool] = None,
        include_build_id: typing.Optional[bool] = None,
        name: typing.Optional[str] = None,
        package_zip: typing.Optional[bool] = None,
        path: typing.Optional[str] = None,
        identifier: typing.Optional[str] = None,
    ) -> "IArtifacts":
        """
        :param bucket: The name of the output bucket.
        :param encryption: If this is false, build output will not be encrypted. This is useful if the artifact to publish a static website or sharing content with others Default: true - output will be encrypted
        :param include_build_id: Indicates if the build ID should be included in the path. If this is set to true, then the build artifact will be stored in "//". Default: true
        :param name: The name of the build output ZIP file or folder inside the bucket. The full S3 object key will be "//" or "/" depending on whether ``includeBuildId`` is set to true. If not set, ``overrideArtifactName`` will be set and the name from the buildspec will be used instead. Default: undefined, and use the name from the buildspec
        :param package_zip: If this is true, all build output will be packaged into a single .zip file. Otherwise, all files will be uploaded to /. Default: true - files will be archived
        :param path: The path inside of the bucket for the build output .zip file or folder. If a value is not specified, then build output will be stored at the root of the bucket (or under the directory if ``includeBuildId`` is set to true). Default: the root of the bucket
        :param identifier: The artifact identifier. This property is required on secondary artifacts.
        """
        props = S3ArtifactsProps(
            bucket=bucket,
            encryption=encryption,
            include_build_id=include_build_id,
            name=name,
            package_zip=package_zip,
            path=path,
            identifier=identifier,
        )

        return jsii.sinvoke(cls, "s3", [props])

    @jsii.member(jsii_name="bind")
    def bind(
        self, _scope: aws_cdk.core.Construct, _project: "IProject"
    ) -> "ArtifactsConfig":
        """Callback when an Artifacts class is used in a CodeBuild Project.

        :param _scope: -
        :param _project: -
        """
        return jsii.invoke(self, "bind", [_scope, _project])

    @builtins.property
    @jsii.member(jsii_name="type")
    @abc.abstractmethod
    def type(self) -> str:
        """The CodeBuild type of this artifact."""
        ...

    @builtins.property
    @jsii.member(jsii_name="identifier")
    def identifier(self) -> typing.Optional[str]:
        """The artifact identifier.

        This property is required on secondary artifacts.
        """
        return jsii.get(self, "identifier")


class _ArtifactsProxy(Artifacts):
    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> str:
        """The CodeBuild type of this artifact."""
        return jsii.get(self, "type")


@jsii.data_type(
    jsii_type="@aws-cdk/aws-codebuild.BitBucketSourceProps",
    jsii_struct_bases=[SourceProps],
    name_mapping={
        "identifier": "identifier",
        "owner": "owner",
        "repo": "repo",
        "branch_or_ref": "branchOrRef",
        "clone_depth": "cloneDepth",
        "report_build_status": "reportBuildStatus",
        "webhook": "webhook",
        "webhook_filters": "webhookFilters",
    },
)
class BitBucketSourceProps(SourceProps):
    def __init__(
        self,
        *,
        identifier: typing.Optional[str] = None,
        owner: str,
        repo: str,
        branch_or_ref: typing.Optional[str] = None,
        clone_depth: typing.Optional[jsii.Number] = None,
        report_build_status: typing.Optional[bool] = None,
        webhook: typing.Optional[bool] = None,
        webhook_filters: typing.Optional[typing.List["FilterGroup"]] = None,
    ) -> None:
        """Construction properties for {@link BitBucketSource}.

        :param identifier: The source identifier. This property is required on secondary sources.
        :param owner: The BitBucket account/user that owns the repo.
        :param repo: The name of the repo (without the username).
        :param branch_or_ref: The commit ID, pull request ID, branch name, or tag name that corresponds to the version of the source code you want to build. Default: the default branch's HEAD commit ID is used
        :param clone_depth: The depth of history to download. Minimum value is 0. If this value is 0, greater than 25, or not provided, then the full history is downloaded with each build of the project.
        :param report_build_status: Whether to send notifications on your build's start and end. Default: true
        :param webhook: Whether to create a webhook that will trigger a build every time an event happens in the repository. Default: true if any ``webhookFilters`` were provided, false otherwise
        :param webhook_filters: A list of webhook filters that can constraint what events in the repository will trigger a build. A build is triggered if any of the provided filter groups match. Only valid if ``webhook`` was not provided as false. Default: every push and every Pull Request (create or update) triggers a build
        """
        self._values = {
            "owner": owner,
            "repo": repo,
        }
        if identifier is not None:
            self._values["identifier"] = identifier
        if branch_or_ref is not None:
            self._values["branch_or_ref"] = branch_or_ref
        if clone_depth is not None:
            self._values["clone_depth"] = clone_depth
        if report_build_status is not None:
            self._values["report_build_status"] = report_build_status
        if webhook is not None:
            self._values["webhook"] = webhook
        if webhook_filters is not None:
            self._values["webhook_filters"] = webhook_filters

    @builtins.property
    def identifier(self) -> typing.Optional[str]:
        """The source identifier.

        This property is required on secondary sources.
        """
        return self._values.get("identifier")

    @builtins.property
    def owner(self) -> str:
        """The BitBucket account/user that owns the repo.

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            "awslabs"
        """
        return self._values.get("owner")

    @builtins.property
    def repo(self) -> str:
        """The name of the repo (without the username).

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            "aws-cdk"
        """
        return self._values.get("repo")

    @builtins.property
    def branch_or_ref(self) -> typing.Optional[str]:
        """The commit ID, pull request ID, branch name, or tag name that corresponds to the version of the source code you want to build.

        default
        :default: the default branch's HEAD commit ID is used

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            "mybranch"
        """
        return self._values.get("branch_or_ref")

    @builtins.property
    def clone_depth(self) -> typing.Optional[jsii.Number]:
        """The depth of history to download.

        Minimum value is 0.
        If this value is 0, greater than 25, or not provided,
        then the full history is downloaded with each build of the project.
        """
        return self._values.get("clone_depth")

    @builtins.property
    def report_build_status(self) -> typing.Optional[bool]:
        """Whether to send notifications on your build's start and end.

        default
        :default: true
        """
        return self._values.get("report_build_status")

    @builtins.property
    def webhook(self) -> typing.Optional[bool]:
        """Whether to create a webhook that will trigger a build every time an event happens in the repository.

        default
        :default: true if any ``webhookFilters`` were provided, false otherwise
        """
        return self._values.get("webhook")

    @builtins.property
    def webhook_filters(self) -> typing.Optional[typing.List["FilterGroup"]]:
        """A list of webhook filters that can constraint what events in the repository will trigger a build.

        A build is triggered if any of the provided filter groups match.
        Only valid if ``webhook`` was not provided as false.

        default
        :default: every push and every Pull Request (create or update) triggers a build
        """
        return self._values.get("webhook_filters")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BitBucketSourceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-codebuild.CodeCommitSourceProps",
    jsii_struct_bases=[SourceProps],
    name_mapping={
        "identifier": "identifier",
        "repository": "repository",
        "branch_or_ref": "branchOrRef",
        "clone_depth": "cloneDepth",
    },
)
class CodeCommitSourceProps(SourceProps):
    def __init__(
        self,
        *,
        identifier: typing.Optional[str] = None,
        repository: aws_cdk.aws_codecommit.IRepository,
        branch_or_ref: typing.Optional[str] = None,
        clone_depth: typing.Optional[jsii.Number] = None,
    ) -> None:
        """Construction properties for {@link CodeCommitSource}.

        :param identifier: The source identifier. This property is required on secondary sources.
        :param repository: 
        :param branch_or_ref: The commit ID, pull request ID, branch name, or tag name that corresponds to the version of the source code you want to build. Default: the default branch's HEAD commit ID is used
        :param clone_depth: The depth of history to download. Minimum value is 0. If this value is 0, greater than 25, or not provided, then the full history is downloaded with each build of the project.
        """
        self._values = {
            "repository": repository,
        }
        if identifier is not None:
            self._values["identifier"] = identifier
        if branch_or_ref is not None:
            self._values["branch_or_ref"] = branch_or_ref
        if clone_depth is not None:
            self._values["clone_depth"] = clone_depth

    @builtins.property
    def identifier(self) -> typing.Optional[str]:
        """The source identifier.

        This property is required on secondary sources.
        """
        return self._values.get("identifier")

    @builtins.property
    def repository(self) -> aws_cdk.aws_codecommit.IRepository:
        return self._values.get("repository")

    @builtins.property
    def branch_or_ref(self) -> typing.Optional[str]:
        """The commit ID, pull request ID, branch name, or tag name that corresponds to the version of the source code you want to build.

        default
        :default: the default branch's HEAD commit ID is used

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            "mybranch"
        """
        return self._values.get("branch_or_ref")

    @builtins.property
    def clone_depth(self) -> typing.Optional[jsii.Number]:
        """The depth of history to download.

        Minimum value is 0.
        If this value is 0, greater than 25, or not provided,
        then the full history is downloaded with each build of the project.
        """
        return self._values.get("clone_depth")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodeCommitSourceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-codebuild.GitHubEnterpriseSourceProps",
    jsii_struct_bases=[SourceProps],
    name_mapping={
        "identifier": "identifier",
        "https_clone_url": "httpsCloneUrl",
        "branch_or_ref": "branchOrRef",
        "clone_depth": "cloneDepth",
        "ignore_ssl_errors": "ignoreSslErrors",
        "report_build_status": "reportBuildStatus",
        "webhook": "webhook",
        "webhook_filters": "webhookFilters",
    },
)
class GitHubEnterpriseSourceProps(SourceProps):
    def __init__(
        self,
        *,
        identifier: typing.Optional[str] = None,
        https_clone_url: str,
        branch_or_ref: typing.Optional[str] = None,
        clone_depth: typing.Optional[jsii.Number] = None,
        ignore_ssl_errors: typing.Optional[bool] = None,
        report_build_status: typing.Optional[bool] = None,
        webhook: typing.Optional[bool] = None,
        webhook_filters: typing.Optional[typing.List["FilterGroup"]] = None,
    ) -> None:
        """Construction properties for {@link GitHubEnterpriseSource}.

        :param identifier: The source identifier. This property is required on secondary sources.
        :param https_clone_url: The HTTPS URL of the repository in your GitHub Enterprise installation.
        :param branch_or_ref: The commit ID, pull request ID, branch name, or tag name that corresponds to the version of the source code you want to build. Default: the default branch's HEAD commit ID is used
        :param clone_depth: The depth of history to download. Minimum value is 0. If this value is 0, greater than 25, or not provided, then the full history is downloaded with each build of the project.
        :param ignore_ssl_errors: Whether to ignore SSL errors when connecting to the repository. Default: false
        :param report_build_status: Whether to send notifications on your build's start and end. Default: true
        :param webhook: Whether to create a webhook that will trigger a build every time an event happens in the repository. Default: true if any ``webhookFilters`` were provided, false otherwise
        :param webhook_filters: A list of webhook filters that can constraint what events in the repository will trigger a build. A build is triggered if any of the provided filter groups match. Only valid if ``webhook`` was not provided as false. Default: every push and every Pull Request (create or update) triggers a build
        """
        self._values = {
            "https_clone_url": https_clone_url,
        }
        if identifier is not None:
            self._values["identifier"] = identifier
        if branch_or_ref is not None:
            self._values["branch_or_ref"] = branch_or_ref
        if clone_depth is not None:
            self._values["clone_depth"] = clone_depth
        if ignore_ssl_errors is not None:
            self._values["ignore_ssl_errors"] = ignore_ssl_errors
        if report_build_status is not None:
            self._values["report_build_status"] = report_build_status
        if webhook is not None:
            self._values["webhook"] = webhook
        if webhook_filters is not None:
            self._values["webhook_filters"] = webhook_filters

    @builtins.property
    def identifier(self) -> typing.Optional[str]:
        """The source identifier.

        This property is required on secondary sources.
        """
        return self._values.get("identifier")

    @builtins.property
    def https_clone_url(self) -> str:
        """The HTTPS URL of the repository in your GitHub Enterprise installation."""
        return self._values.get("https_clone_url")

    @builtins.property
    def branch_or_ref(self) -> typing.Optional[str]:
        """The commit ID, pull request ID, branch name, or tag name that corresponds to the version of the source code you want to build.

        default
        :default: the default branch's HEAD commit ID is used

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            "mybranch"
        """
        return self._values.get("branch_or_ref")

    @builtins.property
    def clone_depth(self) -> typing.Optional[jsii.Number]:
        """The depth of history to download.

        Minimum value is 0.
        If this value is 0, greater than 25, or not provided,
        then the full history is downloaded with each build of the project.
        """
        return self._values.get("clone_depth")

    @builtins.property
    def ignore_ssl_errors(self) -> typing.Optional[bool]:
        """Whether to ignore SSL errors when connecting to the repository.

        default
        :default: false
        """
        return self._values.get("ignore_ssl_errors")

    @builtins.property
    def report_build_status(self) -> typing.Optional[bool]:
        """Whether to send notifications on your build's start and end.

        default
        :default: true
        """
        return self._values.get("report_build_status")

    @builtins.property
    def webhook(self) -> typing.Optional[bool]:
        """Whether to create a webhook that will trigger a build every time an event happens in the repository.

        default
        :default: true if any ``webhookFilters`` were provided, false otherwise
        """
        return self._values.get("webhook")

    @builtins.property
    def webhook_filters(self) -> typing.Optional[typing.List["FilterGroup"]]:
        """A list of webhook filters that can constraint what events in the repository will trigger a build.

        A build is triggered if any of the provided filter groups match.
        Only valid if ``webhook`` was not provided as false.

        default
        :default: every push and every Pull Request (create or update) triggers a build
        """
        return self._values.get("webhook_filters")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GitHubEnterpriseSourceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-codebuild.GitHubSourceProps",
    jsii_struct_bases=[SourceProps],
    name_mapping={
        "identifier": "identifier",
        "owner": "owner",
        "repo": "repo",
        "branch_or_ref": "branchOrRef",
        "clone_depth": "cloneDepth",
        "report_build_status": "reportBuildStatus",
        "webhook": "webhook",
        "webhook_filters": "webhookFilters",
    },
)
class GitHubSourceProps(SourceProps):
    def __init__(
        self,
        *,
        identifier: typing.Optional[str] = None,
        owner: str,
        repo: str,
        branch_or_ref: typing.Optional[str] = None,
        clone_depth: typing.Optional[jsii.Number] = None,
        report_build_status: typing.Optional[bool] = None,
        webhook: typing.Optional[bool] = None,
        webhook_filters: typing.Optional[typing.List["FilterGroup"]] = None,
    ) -> None:
        """Construction properties for {@link GitHubSource} and {@link GitHubEnterpriseSource}.

        :param identifier: The source identifier. This property is required on secondary sources.
        :param owner: The GitHub account/user that owns the repo.
        :param repo: The name of the repo (without the username).
        :param branch_or_ref: The commit ID, pull request ID, branch name, or tag name that corresponds to the version of the source code you want to build. Default: the default branch's HEAD commit ID is used
        :param clone_depth: The depth of history to download. Minimum value is 0. If this value is 0, greater than 25, or not provided, then the full history is downloaded with each build of the project.
        :param report_build_status: Whether to send notifications on your build's start and end. Default: true
        :param webhook: Whether to create a webhook that will trigger a build every time an event happens in the repository. Default: true if any ``webhookFilters`` were provided, false otherwise
        :param webhook_filters: A list of webhook filters that can constraint what events in the repository will trigger a build. A build is triggered if any of the provided filter groups match. Only valid if ``webhook`` was not provided as false. Default: every push and every Pull Request (create or update) triggers a build
        """
        self._values = {
            "owner": owner,
            "repo": repo,
        }
        if identifier is not None:
            self._values["identifier"] = identifier
        if branch_or_ref is not None:
            self._values["branch_or_ref"] = branch_or_ref
        if clone_depth is not None:
            self._values["clone_depth"] = clone_depth
        if report_build_status is not None:
            self._values["report_build_status"] = report_build_status
        if webhook is not None:
            self._values["webhook"] = webhook
        if webhook_filters is not None:
            self._values["webhook_filters"] = webhook_filters

    @builtins.property
    def identifier(self) -> typing.Optional[str]:
        """The source identifier.

        This property is required on secondary sources.
        """
        return self._values.get("identifier")

    @builtins.property
    def owner(self) -> str:
        """The GitHub account/user that owns the repo.

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            "awslabs"
        """
        return self._values.get("owner")

    @builtins.property
    def repo(self) -> str:
        """The name of the repo (without the username).

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            "aws-cdk"
        """
        return self._values.get("repo")

    @builtins.property
    def branch_or_ref(self) -> typing.Optional[str]:
        """The commit ID, pull request ID, branch name, or tag name that corresponds to the version of the source code you want to build.

        default
        :default: the default branch's HEAD commit ID is used

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            "mybranch"
        """
        return self._values.get("branch_or_ref")

    @builtins.property
    def clone_depth(self) -> typing.Optional[jsii.Number]:
        """The depth of history to download.

        Minimum value is 0.
        If this value is 0, greater than 25, or not provided,
        then the full history is downloaded with each build of the project.
        """
        return self._values.get("clone_depth")

    @builtins.property
    def report_build_status(self) -> typing.Optional[bool]:
        """Whether to send notifications on your build's start and end.

        default
        :default: true
        """
        return self._values.get("report_build_status")

    @builtins.property
    def webhook(self) -> typing.Optional[bool]:
        """Whether to create a webhook that will trigger a build every time an event happens in the repository.

        default
        :default: true if any ``webhookFilters`` were provided, false otherwise
        """
        return self._values.get("webhook")

    @builtins.property
    def webhook_filters(self) -> typing.Optional[typing.List["FilterGroup"]]:
        """A list of webhook filters that can constraint what events in the repository will trigger a build.

        A build is triggered if any of the provided filter groups match.
        Only valid if ``webhook`` was not provided as false.

        default
        :default: every push and every Pull Request (create or update) triggers a build
        """
        return self._values.get("webhook_filters")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GitHubSourceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PipelineProject(
    Project, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codebuild.PipelineProject"
):
    """A convenience class for CodeBuild Projects that are used in CodePipeline."""

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: str,
        *,
        allow_all_outbound: typing.Optional[bool] = None,
        badge: typing.Optional[bool] = None,
        build_spec: typing.Optional["BuildSpec"] = None,
        cache: typing.Optional["Cache"] = None,
        description: typing.Optional[str] = None,
        encryption_key: typing.Optional[aws_cdk.aws_kms.IKey] = None,
        environment: typing.Optional["BuildEnvironment"] = None,
        environment_variables: typing.Optional[
            typing.Mapping[str, "BuildEnvironmentVariable"]
        ] = None,
        file_system_locations: typing.Optional[
            typing.List["IFileSystemLocation"]
        ] = None,
        grant_report_group_permissions: typing.Optional[bool] = None,
        project_name: typing.Optional[str] = None,
        role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
        security_groups: typing.Optional[
            typing.List[aws_cdk.aws_ec2.ISecurityGroup]
        ] = None,
        subnet_selection: typing.Optional[aws_cdk.aws_ec2.SubnetSelection] = None,
        timeout: typing.Optional[aws_cdk.core.Duration] = None,
        vpc: typing.Optional[aws_cdk.aws_ec2.IVpc] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param allow_all_outbound: Whether to allow the CodeBuild to send all network traffic. If set to false, you must individually add traffic rules to allow the CodeBuild project to connect to network targets. Only used if 'vpc' is supplied. Default: true
        :param badge: Indicates whether AWS CodeBuild generates a publicly accessible URL for your project's build badge. For more information, see Build Badges Sample in the AWS CodeBuild User Guide. Default: false
        :param build_spec: Filename or contents of buildspec in JSON format. Default: - Empty buildspec.
        :param cache: Caching strategy to use. Default: Cache.none
        :param description: A description of the project. Use the description to identify the purpose of the project. Default: - No description.
        :param encryption_key: Encryption key to use to read and write artifacts. Default: - The AWS-managed CMK for Amazon Simple Storage Service (Amazon S3) is used.
        :param environment: Build environment to use for the build. Default: BuildEnvironment.LinuxBuildImage.STANDARD_1_0
        :param environment_variables: Additional environment variables to add to the build environment. Default: - No additional environment variables are specified.
        :param file_system_locations: An ProjectFileSystemLocation objects for a CodeBuild build project. A ProjectFileSystemLocation object specifies the identifier, location, mountOptions, mountPoint, and type of a file system created using Amazon Elastic File System. Default: - no file system locations
        :param grant_report_group_permissions: Add permissions to this project's role to create and use test report groups with name starting with the name of this project. That is the standard report group that gets created when a simple name (in contrast to an ARN) is used in the 'reports' section of the buildspec of this project. This is usually harmless, but you can turn these off if you don't plan on using test reports in this project. Default: true
        :param project_name: The physical, human-readable name of the CodeBuild Project. Default: - Name is automatically generated.
        :param role: Service Role to assume while running the build. Default: - A role will be created.
        :param security_groups: What security group to associate with the codebuild project's network interfaces. If no security group is identified, one will be created automatically. Only used if 'vpc' is supplied. Default: - Security group will be automatically created.
        :param subnet_selection: Where to place the network interfaces within the VPC. Only used if 'vpc' is supplied. Default: - All private subnets.
        :param timeout: The number of minutes after which AWS CodeBuild stops the build if it's not complete. For valid values, see the timeoutInMinutes field in the AWS CodeBuild User Guide. Default: Duration.hours(1)
        :param vpc: VPC network to place codebuild network interfaces. Specify this if the codebuild project needs to access resources in a VPC. Default: - No VPC is specified.
        """
        props = PipelineProjectProps(
            allow_all_outbound=allow_all_outbound,
            badge=badge,
            build_spec=build_spec,
            cache=cache,
            description=description,
            encryption_key=encryption_key,
            environment=environment,
            environment_variables=environment_variables,
            file_system_locations=file_system_locations,
            grant_report_group_permissions=grant_report_group_permissions,
            project_name=project_name,
            role=role,
            security_groups=security_groups,
            subnet_selection=subnet_selection,
            timeout=timeout,
            vpc=vpc,
        )

        jsii.create(PipelineProject, self, [scope, id, props])


@jsii.data_type(
    jsii_type="@aws-cdk/aws-codebuild.S3SourceProps",
    jsii_struct_bases=[SourceProps],
    name_mapping={
        "identifier": "identifier",
        "bucket": "bucket",
        "path": "path",
        "version": "version",
    },
)
class S3SourceProps(SourceProps):
    def __init__(
        self,
        *,
        identifier: typing.Optional[str] = None,
        bucket: aws_cdk.aws_s3.IBucket,
        path: str,
        version: typing.Optional[str] = None,
    ) -> None:
        """Construction properties for {@link S3Source}.

        :param identifier: The source identifier. This property is required on secondary sources.
        :param bucket: 
        :param path: 
        :param version: The version ID of the object that represents the build input ZIP file to use. Default: latest
        """
        self._values = {
            "bucket": bucket,
            "path": path,
        }
        if identifier is not None:
            self._values["identifier"] = identifier
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def identifier(self) -> typing.Optional[str]:
        """The source identifier.

        This property is required on secondary sources.
        """
        return self._values.get("identifier")

    @builtins.property
    def bucket(self) -> aws_cdk.aws_s3.IBucket:
        return self._values.get("bucket")

    @builtins.property
    def path(self) -> str:
        return self._values.get("path")

    @builtins.property
    def version(self) -> typing.Optional[str]:
        """The version ID of the object that represents the build input ZIP file to use.

        default
        :default: latest
        """
        return self._values.get("version")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3SourceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "Artifacts",
    "ArtifactsConfig",
    "ArtifactsProps",
    "BindToCodePipelineOptions",
    "BitBucketSourceCredentials",
    "BitBucketSourceCredentialsProps",
    "BitBucketSourceProps",
    "BucketCacheOptions",
    "BuildEnvironment",
    "BuildEnvironmentVariable",
    "BuildEnvironmentVariableType",
    "BuildSpec",
    "Cache",
    "CfnProject",
    "CfnProjectProps",
    "CfnReportGroup",
    "CfnReportGroupProps",
    "CfnSourceCredential",
    "CfnSourceCredentialProps",
    "CodeCommitSourceProps",
    "CommonProjectProps",
    "ComputeType",
    "DockerImageOptions",
    "EfsFileSystemLocationProps",
    "EventAction",
    "FileSystemConfig",
    "FileSystemLocation",
    "FilterGroup",
    "GitHubEnterpriseSourceCredentials",
    "GitHubEnterpriseSourceCredentialsProps",
    "GitHubEnterpriseSourceProps",
    "GitHubSourceCredentials",
    "GitHubSourceCredentialsProps",
    "GitHubSourceProps",
    "IArtifacts",
    "IBuildImage",
    "IFileSystemLocation",
    "IProject",
    "IReportGroup",
    "ISource",
    "ImagePullPrincipalType",
    "LinuxBuildImage",
    "LocalCacheMode",
    "PhaseChangeEvent",
    "PipelineProject",
    "PipelineProjectProps",
    "Project",
    "ProjectProps",
    "ReportGroup",
    "ReportGroupProps",
    "S3ArtifactsProps",
    "S3SourceProps",
    "Source",
    "SourceConfig",
    "SourceProps",
    "StateChangeEvent",
    "WindowsBuildImage",
]

publication.publish()
