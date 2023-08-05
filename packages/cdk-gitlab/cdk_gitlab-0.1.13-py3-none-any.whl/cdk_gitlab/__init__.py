"""
[![NPM version](https://badge.fury.io/js/cdk-gitlab.svg)](https://badge.fury.io/js/cdk-gitlab)
[![PyPI version](https://badge.fury.io/py/cdk-gitlab.svg)](https://badge.fury.io/py/cdk-gitlab)
![Release](https://github.com/pahud/cdk-gitlab/workflows/Release/badge.svg)

# cdk-gitlab

High level CDK construct to provision GitLab integrations with AWS

# Sample

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from cdk_gitlab import Provider, FargateJobExecutor, FargateRunner, JobExecutorImage

provider = Provider(stack, "GitlabProvider", vpc=vpc)

# create a Amazon EKS cluster
provider.create_fargate_eks_cluster(stack, "GitlabEksCluster",
    cluster_options={
        "vpc": vpc,
        "version": eks.KubernetesVersion.V1_18
    }
)

# create a default fargate runner with its job executor
provider.create_fargate_runner()

# alternatively, create the runner and the executor indivicually.
# first, create the executor
executor = FargateJobExecutor(stack, "JobExecutor",
    image=JobExecutorImage.DEBIAN
)

# second, create the runner with the task definition of the executor
FargateRunner(stack, "FargateRunner",
    vpc=vpc,
    executor=executor
)

# TBD - create Amazon EC2 runner for the GitLab
provider.create_ec2_runner(...)
```

# Fargate Runner with Aamzon ECS

On deployment with `createFargateRunner()`, the **Fargate Runner** will be provisioned in Amazon ECS with AWS Fargate and [Amazon ECS Capacity Providers](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/cluster-capacity-providers.html). By default, the `FARGATE` and `FARGATE_SPOT` capacity providers are available for the Amazon ECS cluster and the runner and job executor will run on `FARGATE_SPOT`. You can specify your custom `clusterDefaultCapacityProviderStrategy` and `serviceDefaultCapacityProviderStrategy` properties from the `FargateRunner` construct for different capacity provider strategies.

# Deploy

```sh
cdk deploy -c GITLAB_REGISTRATION_TOKEN=<TOKEN>
```
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
import aws_cdk.aws_ecs
import aws_cdk.aws_eks
import aws_cdk.aws_iam
import aws_cdk.core


@jsii.data_type(
    jsii_type="cdk-gitlab.CapacityProviderStrategyItem",
    jsii_struct_bases=[],
    name_mapping={
        "capacity_provider": "capacityProvider",
        "weight": "weight",
        "base": "base",
    },
)
class CapacityProviderStrategyItem:
    def __init__(
        self,
        *,
        capacity_provider: "FargateCapacityProviderType",
        weight: jsii.Number,
        base: typing.Optional[jsii.Number] = None,
    ) -> None:
        """The Capacity Provider strategy.

        :param capacity_provider: 
        :param weight: 
        :param base: 
        """
        self._values: typing.Dict[str, typing.Any] = {
            "capacity_provider": capacity_provider,
            "weight": weight,
        }
        if base is not None:
            self._values["base"] = base

    @builtins.property
    def capacity_provider(self) -> "FargateCapacityProviderType":
        result = self._values.get("capacity_provider")
        assert result is not None, "Required property 'capacity_provider' is missing"
        return result

    @builtins.property
    def weight(self) -> jsii.Number:
        result = self._values.get("weight")
        assert result is not None, "Required property 'weight' is missing"
        return result

    @builtins.property
    def base(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("base")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CapacityProviderStrategyItem(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-gitlab.EksClusterOptions",
    jsii_struct_bases=[],
    name_mapping={"cluster_options": "clusterOptions", "rbac": "rbac"},
)
class EksClusterOptions:
    def __init__(
        self,
        *,
        cluster_options: aws_cdk.aws_eks.ClusterProps,
        rbac: typing.Optional[builtins.bool] = None,
    ) -> None:
        """
        :param cluster_options: cluster properties for Amazon EKS cluster.
        :param rbac: create serivce account and rbac ClusterRoleBinding for gitlab. Default: true
        """
        if isinstance(cluster_options, dict):
            cluster_options = aws_cdk.aws_eks.ClusterProps(**cluster_options)
        self._values: typing.Dict[str, typing.Any] = {
            "cluster_options": cluster_options,
        }
        if rbac is not None:
            self._values["rbac"] = rbac

    @builtins.property
    def cluster_options(self) -> aws_cdk.aws_eks.ClusterProps:
        """cluster properties for Amazon EKS cluster."""
        result = self._values.get("cluster_options")
        assert result is not None, "Required property 'cluster_options' is missing"
        return result

    @builtins.property
    def rbac(self) -> typing.Optional[builtins.bool]:
        """create serivce account and rbac ClusterRoleBinding for gitlab.

        :default: true

        :see: https://docs.gitlab.com/ee/user/project/clusters/add_remove_clusters.html#add-existing-cluster
        """
        result = self._values.get("rbac")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EksClusterOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="cdk-gitlab.FargateCapacityProviderType")
class FargateCapacityProviderType(enum.Enum):
    """Amazon ECS Capacity Providers for AWS Fargate."""

    FARGATE = "FARGATE"
    FARGATE_SPOT = "FARGATE_SPOT"


@jsii.data_type(
    jsii_type="cdk-gitlab.FargateEksClusterOptions",
    jsii_struct_bases=[],
    name_mapping={"cluster_options": "clusterOptions", "rbac": "rbac"},
)
class FargateEksClusterOptions:
    def __init__(
        self,
        *,
        cluster_options: aws_cdk.aws_eks.FargateClusterProps,
        rbac: typing.Optional[builtins.bool] = None,
    ) -> None:
        """
        :param cluster_options: cluster properties for Amazon EKS cluster.
        :param rbac: create serivce account and rbac ClusterRoleBinding for gitlab. Default: true
        """
        if isinstance(cluster_options, dict):
            cluster_options = aws_cdk.aws_eks.FargateClusterProps(**cluster_options)
        self._values: typing.Dict[str, typing.Any] = {
            "cluster_options": cluster_options,
        }
        if rbac is not None:
            self._values["rbac"] = rbac

    @builtins.property
    def cluster_options(self) -> aws_cdk.aws_eks.FargateClusterProps:
        """cluster properties for Amazon EKS cluster."""
        result = self._values.get("cluster_options")
        assert result is not None, "Required property 'cluster_options' is missing"
        return result

    @builtins.property
    def rbac(self) -> typing.Optional[builtins.bool]:
        """create serivce account and rbac ClusterRoleBinding for gitlab.

        :default: true

        :see: https://docs.gitlab.com/ee/user/project/clusters/add_remove_clusters.html#add-existing-cluster
        """
        result = self._values.get("rbac")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FargateEksClusterOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FargateJobExecutor(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-gitlab.FargateJobExecutor",
):
    """The FargateJobExecutor."""

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        cluster: typing.Optional[aws_cdk.aws_ecs.ICluster] = None,
        image: typing.Optional["JobExecutorImage"] = None,
        region: typing.Optional[builtins.str] = None,
        security_group: typing.Optional[aws_cdk.aws_ec2.ISecurityGroup] = None,
        subnet: typing.Optional[aws_cdk.aws_ec2.ISubnet] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param cluster: 
        :param image: The docker image for the job executor container.
        :param region: AWS region for the job executor.
        :param security_group: 
        :param subnet: 
        """
        props = FargateJobExecutorProps(
            cluster=cluster,
            image=image,
            region=region,
            security_group=security_group,
            subnet=subnet,
        )

        jsii.create(FargateJobExecutor, self, [scope, id, props])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return jsii.get(self, "region")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="taskDefinitionArn")
    def task_definition_arn(self) -> builtins.str:
        """task definition arn."""
        return jsii.get(self, "taskDefinitionArn")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cluster")
    def cluster(self) -> typing.Optional[aws_cdk.aws_ecs.ICluster]:
        return jsii.get(self, "cluster")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="securityGroup")
    def security_group(self) -> typing.Optional[aws_cdk.aws_ec2.ISecurityGroup]:
        return jsii.get(self, "securityGroup")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="subnet")
    def subnet(self) -> typing.Optional[aws_cdk.aws_ec2.ISubnet]:
        return jsii.get(self, "subnet")


@jsii.data_type(
    jsii_type="cdk-gitlab.FargateJobExecutorProps",
    jsii_struct_bases=[],
    name_mapping={
        "cluster": "cluster",
        "image": "image",
        "region": "region",
        "security_group": "securityGroup",
        "subnet": "subnet",
    },
)
class FargateJobExecutorProps:
    def __init__(
        self,
        *,
        cluster: typing.Optional[aws_cdk.aws_ecs.ICluster] = None,
        image: typing.Optional["JobExecutorImage"] = None,
        region: typing.Optional[builtins.str] = None,
        security_group: typing.Optional[aws_cdk.aws_ec2.ISecurityGroup] = None,
        subnet: typing.Optional[aws_cdk.aws_ec2.ISubnet] = None,
    ) -> None:
        """The properties for the FargateJobExecutor.

        :param cluster: 
        :param image: The docker image for the job executor container.
        :param region: AWS region for the job executor.
        :param security_group: 
        :param subnet: 
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if cluster is not None:
            self._values["cluster"] = cluster
        if image is not None:
            self._values["image"] = image
        if region is not None:
            self._values["region"] = region
        if security_group is not None:
            self._values["security_group"] = security_group
        if subnet is not None:
            self._values["subnet"] = subnet

    @builtins.property
    def cluster(self) -> typing.Optional[aws_cdk.aws_ecs.ICluster]:
        result = self._values.get("cluster")
        return result

    @builtins.property
    def image(self) -> typing.Optional["JobExecutorImage"]:
        """The docker image for the job executor container."""
        result = self._values.get("image")
        return result

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        """AWS region for the job executor."""
        result = self._values.get("region")
        return result

    @builtins.property
    def security_group(self) -> typing.Optional[aws_cdk.aws_ec2.ISecurityGroup]:
        result = self._values.get("security_group")
        return result

    @builtins.property
    def subnet(self) -> typing.Optional[aws_cdk.aws_ec2.ISubnet]:
        result = self._values.get("subnet")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FargateJobExecutorProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FargateRunner(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-gitlab.FargateRunner",
):
    """The FargateRunner."""

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        vpc: aws_cdk.aws_ec2.IVpc,
        cluster_default_capacity_provider_strategy: typing.Optional[typing.List[CapacityProviderStrategyItem]] = None,
        executor: typing.Optional[FargateJobExecutor] = None,
        fargate_job_subnet: typing.Optional[aws_cdk.aws_ec2.SubnetSelection] = None,
        gitlab_url: typing.Optional[builtins.str] = None,
        registration_token: typing.Optional[builtins.str] = None,
        security_group: typing.Optional[aws_cdk.aws_ec2.ISecurityGroup] = None,
        service_default_capacity_provider_strategy: typing.Optional[typing.List[CapacityProviderStrategyItem]] = None,
        tags: typing.Optional[typing.List[builtins.str]] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param vpc: VPC for the fargate.
        :param cluster_default_capacity_provider_strategy: Default capacity provider strategy for the Amazon ECS cluster. Default: DEFAULT_CLUSTER_CAPACITY_PROVIDER_STRATEGY
        :param executor: Fargate job executor options.
        :param fargate_job_subnet: subnet for fargate CI task.
        :param gitlab_url: gitlab URL prefix. Default: - 'https://gitlab.com'
        :param registration_token: GitLab registration token for the runner.
        :param security_group: The security group for Fargate CI task.
        :param service_default_capacity_provider_strategy: Default capacity provider strategy for the Amazon ECS service. Default: DEFAULT_SERVICE_CAPACITY_PROVIDER_STRATEGY
        :param tags: tags for the runner.
        """
        props = FargateRunnerProps(
            vpc=vpc,
            cluster_default_capacity_provider_strategy=cluster_default_capacity_provider_strategy,
            executor=executor,
            fargate_job_subnet=fargate_job_subnet,
            gitlab_url=gitlab_url,
            registration_token=registration_token,
            security_group=security_group,
            service_default_capacity_provider_strategy=service_default_capacity_provider_strategy,
            tags=tags,
        )

        jsii.create(FargateRunner, self, [scope, id, props])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> aws_cdk.aws_ec2.IVpc:
        return jsii.get(self, "vpc")


@jsii.data_type(
    jsii_type="cdk-gitlab.FargateRunnerProps",
    jsii_struct_bases=[],
    name_mapping={
        "vpc": "vpc",
        "cluster_default_capacity_provider_strategy": "clusterDefaultCapacityProviderStrategy",
        "executor": "executor",
        "fargate_job_subnet": "fargateJobSubnet",
        "gitlab_url": "gitlabURL",
        "registration_token": "registrationToken",
        "security_group": "securityGroup",
        "service_default_capacity_provider_strategy": "serviceDefaultCapacityProviderStrategy",
        "tags": "tags",
    },
)
class FargateRunnerProps:
    def __init__(
        self,
        *,
        vpc: aws_cdk.aws_ec2.IVpc,
        cluster_default_capacity_provider_strategy: typing.Optional[typing.List[CapacityProviderStrategyItem]] = None,
        executor: typing.Optional[FargateJobExecutor] = None,
        fargate_job_subnet: typing.Optional[aws_cdk.aws_ec2.SubnetSelection] = None,
        gitlab_url: typing.Optional[builtins.str] = None,
        registration_token: typing.Optional[builtins.str] = None,
        security_group: typing.Optional[aws_cdk.aws_ec2.ISecurityGroup] = None,
        service_default_capacity_provider_strategy: typing.Optional[typing.List[CapacityProviderStrategyItem]] = None,
        tags: typing.Optional[typing.List[builtins.str]] = None,
    ) -> None:
        """Properties for the FargateRunner.

        :param vpc: VPC for the fargate.
        :param cluster_default_capacity_provider_strategy: Default capacity provider strategy for the Amazon ECS cluster. Default: DEFAULT_CLUSTER_CAPACITY_PROVIDER_STRATEGY
        :param executor: Fargate job executor options.
        :param fargate_job_subnet: subnet for fargate CI task.
        :param gitlab_url: gitlab URL prefix. Default: - 'https://gitlab.com'
        :param registration_token: GitLab registration token for the runner.
        :param security_group: The security group for Fargate CI task.
        :param service_default_capacity_provider_strategy: Default capacity provider strategy for the Amazon ECS service. Default: DEFAULT_SERVICE_CAPACITY_PROVIDER_STRATEGY
        :param tags: tags for the runner.
        """
        if isinstance(fargate_job_subnet, dict):
            fargate_job_subnet = aws_cdk.aws_ec2.SubnetSelection(**fargate_job_subnet)
        self._values: typing.Dict[str, typing.Any] = {
            "vpc": vpc,
        }
        if cluster_default_capacity_provider_strategy is not None:
            self._values["cluster_default_capacity_provider_strategy"] = cluster_default_capacity_provider_strategy
        if executor is not None:
            self._values["executor"] = executor
        if fargate_job_subnet is not None:
            self._values["fargate_job_subnet"] = fargate_job_subnet
        if gitlab_url is not None:
            self._values["gitlab_url"] = gitlab_url
        if registration_token is not None:
            self._values["registration_token"] = registration_token
        if security_group is not None:
            self._values["security_group"] = security_group
        if service_default_capacity_provider_strategy is not None:
            self._values["service_default_capacity_provider_strategy"] = service_default_capacity_provider_strategy
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def vpc(self) -> aws_cdk.aws_ec2.IVpc:
        """VPC for the fargate."""
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return result

    @builtins.property
    def cluster_default_capacity_provider_strategy(
        self,
    ) -> typing.Optional[typing.List[CapacityProviderStrategyItem]]:
        """Default capacity provider strategy for the Amazon ECS cluster.

        :default: DEFAULT_CLUSTER_CAPACITY_PROVIDER_STRATEGY
        """
        result = self._values.get("cluster_default_capacity_provider_strategy")
        return result

    @builtins.property
    def executor(self) -> typing.Optional[FargateJobExecutor]:
        """Fargate job executor options."""
        result = self._values.get("executor")
        return result

    @builtins.property
    def fargate_job_subnet(self) -> typing.Optional[aws_cdk.aws_ec2.SubnetSelection]:
        """subnet for fargate CI task."""
        result = self._values.get("fargate_job_subnet")
        return result

    @builtins.property
    def gitlab_url(self) -> typing.Optional[builtins.str]:
        """gitlab URL prefix.

        :default: - 'https://gitlab.com'
        """
        result = self._values.get("gitlab_url")
        return result

    @builtins.property
    def registration_token(self) -> typing.Optional[builtins.str]:
        """GitLab registration token for the runner."""
        result = self._values.get("registration_token")
        return result

    @builtins.property
    def security_group(self) -> typing.Optional[aws_cdk.aws_ec2.ISecurityGroup]:
        """The security group for Fargate CI task."""
        result = self._values.get("security_group")
        return result

    @builtins.property
    def service_default_capacity_provider_strategy(
        self,
    ) -> typing.Optional[typing.List[CapacityProviderStrategyItem]]:
        """Default capacity provider strategy for the Amazon ECS service.

        :default: DEFAULT_SERVICE_CAPACITY_PROVIDER_STRATEGY
        """
        result = self._values.get("service_default_capacity_provider_strategy")
        return result

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[builtins.str]]:
        """tags for the runner."""
        result = self._values.get("tags")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FargateRunnerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class JobExecutorImage(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-gitlab.JobExecutorImage",
):
    """The docker image for the job executor."""

    @jsii.member(jsii_name="of")
    @builtins.classmethod
    def of(cls, image: builtins.str) -> "JobExecutorImage":
        """Custom image.

        :param image: custom image registry URI.
        """
        return jsii.sinvoke(cls, "of", [image])

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="DEBIAN")
    def DEBIAN(cls) -> "JobExecutorImage":
        """Debian.

        :see: https://gitlab.com/tmaczukin-test-projects/fargate-driver-debian
        """
        return jsii.sget(cls, "DEBIAN")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="JSII")
    def JSII(cls) -> "JobExecutorImage":
        """JSII for AWS CDK.

        :see: https://gitlab.com/pahud/docker-jsii-cdk-gitlab-ci-fargate
        """
        return jsii.sget(cls, "JSII")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="NODE")
    def NODE(cls) -> "JobExecutorImage":
        """Node.

        :see: https://gitlab.com/aws-fargate-driver-demo/docker-nodejs-gitlab-ci-fargate
        """
        return jsii.sget(cls, "NODE")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return jsii.get(self, "uri")


class Provider(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-gitlab.Provider",
):
    """The Provider to create GitLab Integrations with AWS."""

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        vpc: typing.Optional[aws_cdk.aws_ec2.IVpc] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param vpc: 
        """
        props = ProviderProps(vpc=vpc)

        jsii.create(Provider, self, [scope, id, props])

    @jsii.member(jsii_name="createEksCluster")
    def create_eks_cluster(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        cluster_options: aws_cdk.aws_eks.ClusterProps,
        rbac: typing.Optional[builtins.bool] = None,
    ) -> aws_cdk.aws_eks.Cluster:
        """
        :param scope: -
        :param id: -
        :param cluster_options: cluster properties for Amazon EKS cluster.
        :param rbac: create serivce account and rbac ClusterRoleBinding for gitlab. Default: true
        """
        props = EksClusterOptions(cluster_options=cluster_options, rbac=rbac)

        return jsii.invoke(self, "createEksCluster", [scope, id, props])

    @jsii.member(jsii_name="createEksServiceRole")
    def create_eks_service_role(self) -> aws_cdk.aws_iam.Role:
        return jsii.invoke(self, "createEksServiceRole", [])

    @jsii.member(jsii_name="createFargateEksCluster")
    def create_fargate_eks_cluster(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        cluster_options: aws_cdk.aws_eks.FargateClusterProps,
        rbac: typing.Optional[builtins.bool] = None,
    ) -> aws_cdk.aws_eks.Cluster:
        """
        :param scope: -
        :param id: -
        :param cluster_options: cluster properties for Amazon EKS cluster.
        :param rbac: create serivce account and rbac ClusterRoleBinding for gitlab. Default: true
        """
        props = FargateEksClusterOptions(cluster_options=cluster_options, rbac=rbac)

        return jsii.invoke(self, "createFargateEksCluster", [scope, id, props])

    @jsii.member(jsii_name="createFargateRunner")
    def create_fargate_runner(
        self,
        executor: typing.Optional[FargateJobExecutor] = None,
    ) -> None:
        """
        :param executor: -
        """
        return jsii.invoke(self, "createFargateRunner", [executor])

    @jsii.member(jsii_name="createGitlabManagedEksRole")
    def create_gitlab_managed_eks_role(
        self,
        *,
        account_id: builtins.str,
        external_id: builtins.str,
    ) -> None:
        """
        :param account_id: 
        :param external_id: 
        """
        props = RoleProps(account_id=account_id, external_id=external_id)

        return jsii.invoke(self, "createGitlabManagedEksRole", [props])

    @jsii.member(jsii_name="createSecurityGroup")
    def create_security_group(self) -> aws_cdk.aws_ec2.SecurityGroup:
        return jsii.invoke(self, "createSecurityGroup", [])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> aws_cdk.aws_ec2.IVpc:
        return jsii.get(self, "vpc")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="gitlabEksRole")
    def gitlab_eks_role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        return jsii.get(self, "gitlabEksRole")

    @gitlab_eks_role.setter # type: ignore
    def gitlab_eks_role(self, value: typing.Optional[aws_cdk.aws_iam.IRole]) -> None:
        jsii.set(self, "gitlabEksRole", value)


@jsii.data_type(
    jsii_type="cdk-gitlab.ProviderProps",
    jsii_struct_bases=[],
    name_mapping={"vpc": "vpc"},
)
class ProviderProps:
    def __init__(self, *, vpc: typing.Optional[aws_cdk.aws_ec2.IVpc] = None) -> None:
        """
        :param vpc: 
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if vpc is not None:
            self._values["vpc"] = vpc

    @builtins.property
    def vpc(self) -> typing.Optional[aws_cdk.aws_ec2.IVpc]:
        result = self._values.get("vpc")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProviderProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-gitlab.RoleProps",
    jsii_struct_bases=[],
    name_mapping={"account_id": "accountId", "external_id": "externalId"},
)
class RoleProps:
    def __init__(self, *, account_id: builtins.str, external_id: builtins.str) -> None:
        """
        :param account_id: 
        :param external_id: 
        """
        self._values: typing.Dict[str, typing.Any] = {
            "account_id": account_id,
            "external_id": external_id,
        }

    @builtins.property
    def account_id(self) -> builtins.str:
        result = self._values.get("account_id")
        assert result is not None, "Required property 'account_id' is missing"
        return result

    @builtins.property
    def external_id(self) -> builtins.str:
        result = self._values.get("external_id")
        assert result is not None, "Required property 'external_id' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RoleProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CapacityProviderStrategyItem",
    "EksClusterOptions",
    "FargateCapacityProviderType",
    "FargateEksClusterOptions",
    "FargateJobExecutor",
    "FargateJobExecutorProps",
    "FargateRunner",
    "FargateRunnerProps",
    "JobExecutorImage",
    "Provider",
    "ProviderProps",
    "RoleProps",
]

publication.publish()
