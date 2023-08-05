"""
# aws-lambda-sagemaker module

<!--BEGIN STABILITY BANNER-->---


![Stability: Experimental](https://img.shields.io/badge/stability-Experimental-important.svg?style=for-the-badge)

> All classes are under active development and subject to non-backward compatible changes or removal in any
> future version. These are not subject to the [Semantic Versioning](https://semver.org/) model.
> This means that while you may use them, you may need to update your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

| **Reference Documentation**:| <span style="font-weight: normal">https://docs.aws.amazon.com/solutions/latest/constructs/</span>|
|:-------------|:-------------|

<div style="height:8px"></div>

| **Language**     | **Package**        |
|:-------------|-----------------|
|![Python Logo](https://docs.aws.amazon.com/cdk/api/latest/img/python32.png) Python|`aws_solutions_constructs.aws_lambda_sagemaker`|
|![Typescript Logo](https://docs.aws.amazon.com/cdk/api/latest/img/typescript32.png) Typescript|`@aws-solutions-constructs/aws-lambda-sagemaker`|
|![Java Logo](https://docs.aws.amazon.com/cdk/api/latest/img/java32.png) Java|`software.amazon.awsconstructs.services.lambdasagemaker`|

This AWS Solutions Construct implements the AWS Lambda function and Amazon Sagemaker Notebook with the least privileged permissions.

Here is a minimal deployable pattern definition in Typescript:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from aws_solutions_constructs.aws_lambda_sagemaker import LambdaToSagemakerProps, LambdaToSagemaker
from aws_cdk.core import Aws

lambda_to_sagemaker_props = LambdaToSagemakerProps(
    lambda_function_props=FunctionProps(
        code=lambda_.Code.from_asset(f"{__dirname}/lambda"),
        runtime=lambda_.Runtime.NODEJS_12_X,
        handler="index.handler"
    )
)

construct = LambdaToSagemaker(stack, "test-lambda-sagemaker-stack", lambda_to_sagemaker_props)
```

## Initializer

```text
new LambdaToSagemaker(scope: Construct, id: string, props: LambdaToSagemakerProps);
```

*Parameters*

* scope [`Construct`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_core.Construct.html)
* id `string`
* props [`LambdaToSagemakerProps`](#pattern-construct-props)

## Pattern Construct Props

| **Name**     | **Type**        | **Description** |
|:-------------|:----------------|-----------------|
|existingLambdaObj?|[`lambda.Function`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-lambda.Function.html)|Existing instance of Lambda Function object, if this is set then the lambdaFunctionProps is ignored.|
|lambdaFunctionProps?|[`lambda.FunctionProps`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-lambda.FunctionProps.html)|User provided props to override the default props for the Lambda function.|
|sagemakerNotebookProps?|[`sagemaker.CfnNotebookInstanceProps`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-sagemaker.CfnNotebookInstance.html)|Optional user provided props to override the default props for a Sagemaker Notebook.|
|deployInsideVpc?|[`boolean`]()|Optional user provided props to deploy inside vpc. Defaults to `true`.|
|existingNotebookObj?|[`sagemaker.CfnNotebookInstanceProps`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-sagemaker.CfnNotebookInstance.html)|Existing instance of notebook object. If this is set then the sagemakerNotebookProps is ignored|

## Pattern Properties

| **Name**     | **Type**        | **Description** |
|:-------------|:----------------|-----------------|
|lambdaFunction|[`lambda.Function`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-lambda.Function.html)|Returns an instance of lambda.Function created by the construct|
|sagemakerNotebook|[`sagemaker.CfnNotebookInstanceProps`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-sagemaker.CfnNotebookInstance.html)|Returns an instance of sagemaker.CfnNotebookInstanceProps created by the construct|
|sagemakerRole|[`iam.Role`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-iam.Role.html)|Returns the iam.Role created by the construct|
|vpc?|[`ec2.Vpc`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-ec2.Vpc.html)|Returns the ec2.Vpc created by the construct|
|securityGroup?|[`ec2.SecurityGroup`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-ec2.SecurityGroup.html)|Returns the ec2.SecurityGroup created by the construct|

## Default settings

Out of the box implementation of the Construct without any override will set the following defaults:

### AWS Lambda Function

* Configure limited privilege access IAM role for Lambda function
* Enable reusing connections with Keep-Alive for NodeJs Lambda function

### Amazon SageMaker

* Configure least privilege access IAM role for the SageMaker Notebook Intance
* Deploy SageMaker NotebookInstance inside the VPC
* Enable server-side encryption for the SageMaker NotebookInstance using Customer Managed KMS Key

## Architecture

![Architecture Diagram](architecture.png)

---


© Copyright 2020 Amazon.com, Inc. or its affiliates. All Rights Reserved.
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
import aws_cdk.aws_iam
import aws_cdk.aws_lambda
import aws_cdk.aws_sagemaker
import aws_cdk.core


class LambdaToSagemaker(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-solutions-constructs/aws-lambda-sagemaker.LambdaToSagemaker",
):
    """
    :summary: The LambdaToSagemaker class.
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        deploy_inside_vpc: typing.Optional[builtins.bool] = None,
        existing_lambda_obj: typing.Optional[aws_cdk.aws_lambda.Function] = None,
        existing_notebook_obj: typing.Optional[aws_cdk.aws_sagemaker.CfnNotebookInstance] = None,
        lambda_function_props: typing.Optional[aws_cdk.aws_lambda.FunctionProps] = None,
        sagemaker_notebook_props: typing.Any = None,
    ) -> None:
        """
        :param scope: - represents the scope for all the resources.
        :param id: - this is a a scope-unique id.
        :param deploy_inside_vpc: Optional user provided props to deploy inside vpc. Default: - true
        :param existing_lambda_obj: Existing instance of Lambda Function object, if this is set then the lambdaFunctionProps is ignored. Default: - None
        :param existing_notebook_obj: Existing instance of notebook object. If this is set then the sagemakerNotebookProps is ignored Default: - None
        :param lambda_function_props: User provided props to override the default props for the Lambda function. Default: - Default props are used
        :param sagemaker_notebook_props: Optional user provided props to override the default props. Default: - Default props are used

        :access: public
        :since: 1.69.0
        :summary: Constructs a new instance of the LambdaToSagemaker class.
        """
        props = LambdaToSagemakerProps(
            deploy_inside_vpc=deploy_inside_vpc,
            existing_lambda_obj=existing_lambda_obj,
            existing_notebook_obj=existing_notebook_obj,
            lambda_function_props=lambda_function_props,
            sagemaker_notebook_props=sagemaker_notebook_props,
        )

        jsii.create(LambdaToSagemaker, self, [scope, id, props])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="lambdaFunction")
    def lambda_function(self) -> aws_cdk.aws_lambda.Function:
        return jsii.get(self, "lambdaFunction")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="sagemakerNotebook")
    def sagemaker_notebook(self) -> aws_cdk.aws_sagemaker.CfnNotebookInstance:
        return jsii.get(self, "sagemakerNotebook")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="sagemakerRole")
    def sagemaker_role(self) -> aws_cdk.aws_iam.Role:
        return jsii.get(self, "sagemakerRole")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="securityGroup")
    def security_group(self) -> typing.Optional[aws_cdk.aws_ec2.SecurityGroup]:
        return jsii.get(self, "securityGroup")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> typing.Optional[aws_cdk.aws_ec2.Vpc]:
        return jsii.get(self, "vpc")


@jsii.data_type(
    jsii_type="@aws-solutions-constructs/aws-lambda-sagemaker.LambdaToSagemakerProps",
    jsii_struct_bases=[],
    name_mapping={
        "deploy_inside_vpc": "deployInsideVpc",
        "existing_lambda_obj": "existingLambdaObj",
        "existing_notebook_obj": "existingNotebookObj",
        "lambda_function_props": "lambdaFunctionProps",
        "sagemaker_notebook_props": "sagemakerNotebookProps",
    },
)
class LambdaToSagemakerProps:
    def __init__(
        self,
        *,
        deploy_inside_vpc: typing.Optional[builtins.bool] = None,
        existing_lambda_obj: typing.Optional[aws_cdk.aws_lambda.Function] = None,
        existing_notebook_obj: typing.Optional[aws_cdk.aws_sagemaker.CfnNotebookInstance] = None,
        lambda_function_props: typing.Optional[aws_cdk.aws_lambda.FunctionProps] = None,
        sagemaker_notebook_props: typing.Any = None,
    ) -> None:
        """
        :param deploy_inside_vpc: Optional user provided props to deploy inside vpc. Default: - true
        :param existing_lambda_obj: Existing instance of Lambda Function object, if this is set then the lambdaFunctionProps is ignored. Default: - None
        :param existing_notebook_obj: Existing instance of notebook object. If this is set then the sagemakerNotebookProps is ignored Default: - None
        :param lambda_function_props: User provided props to override the default props for the Lambda function. Default: - Default props are used
        :param sagemaker_notebook_props: Optional user provided props to override the default props. Default: - Default props are used

        :summary: The properties for the LambdaToSagemaker Construct
        """
        if isinstance(lambda_function_props, dict):
            lambda_function_props = aws_cdk.aws_lambda.FunctionProps(**lambda_function_props)
        self._values: typing.Dict[str, typing.Any] = {}
        if deploy_inside_vpc is not None:
            self._values["deploy_inside_vpc"] = deploy_inside_vpc
        if existing_lambda_obj is not None:
            self._values["existing_lambda_obj"] = existing_lambda_obj
        if existing_notebook_obj is not None:
            self._values["existing_notebook_obj"] = existing_notebook_obj
        if lambda_function_props is not None:
            self._values["lambda_function_props"] = lambda_function_props
        if sagemaker_notebook_props is not None:
            self._values["sagemaker_notebook_props"] = sagemaker_notebook_props

    @builtins.property
    def deploy_inside_vpc(self) -> typing.Optional[builtins.bool]:
        """Optional user provided props to deploy inside vpc.

        :default: - true
        """
        result = self._values.get("deploy_inside_vpc")
        return result

    @builtins.property
    def existing_lambda_obj(self) -> typing.Optional[aws_cdk.aws_lambda.Function]:
        """Existing instance of Lambda Function object, if this is set then the lambdaFunctionProps is ignored.

        :default: - None
        """
        result = self._values.get("existing_lambda_obj")
        return result

    @builtins.property
    def existing_notebook_obj(
        self,
    ) -> typing.Optional[aws_cdk.aws_sagemaker.CfnNotebookInstance]:
        """Existing instance of notebook object.

        If this is set then the sagemakerNotebookProps is ignored

        :default: - None
        """
        result = self._values.get("existing_notebook_obj")
        return result

    @builtins.property
    def lambda_function_props(
        self,
    ) -> typing.Optional[aws_cdk.aws_lambda.FunctionProps]:
        """User provided props to override the default props for the Lambda function.

        :default: - Default props are used
        """
        result = self._values.get("lambda_function_props")
        return result

    @builtins.property
    def sagemaker_notebook_props(self) -> typing.Any:
        """Optional user provided props to override the default props.

        :default: - Default props are used
        """
        result = self._values.get("sagemaker_notebook_props")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaToSagemakerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "LambdaToSagemaker",
    "LambdaToSagemakerProps",
]

publication.publish()
