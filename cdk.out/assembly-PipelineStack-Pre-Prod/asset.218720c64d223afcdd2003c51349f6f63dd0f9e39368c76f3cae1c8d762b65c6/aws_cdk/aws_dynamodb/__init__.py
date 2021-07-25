"""
## Amazon DynamoDB Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

![cdk-constructs: Stable](https://img.shields.io/badge/cdk--constructs-stable-success.svg?style=for-the-badge)

---
<!--END STABILITY BANNER-->

Here is a minimal deployable DynamoDB table definition:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_dynamodb as dynamodb

table = dynamodb.Table(self, "Table",
    partition_key=Attribute(name="id", type=dynamodb.AttributeType.STRING)
)
```

### Importing existing tables

To import an existing table into your CDK application, use the `Table.fromTableName`, `Table.fromTableArn` or `Table.fromTableAttributes`
factory method. This method accepts table name or table ARN which describes the properties of an already
existing table:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
table = Table.from_table_arn(self, "ImportedTable", "arn:aws:dynamodb:us-east-1:111111111:table/my-table")
# now you can just call methods on the table
table.grant_read_write_data(user)
```

If you intend to use the `tableStreamArn` (including indirectly, for example by creating an
`@aws-cdk/aws-lambda-event-source.DynamoEventSource` on the imported table), you *must* use the
`Table.fromTableAttributes` method and the `tableStreamArn` property *must* be populated.

### Keys

When a table is defined, you must define it's schema using the `partitionKey`
(required) and `sortKey` (optional) properties.

### Billing Mode

DynamoDB supports two billing modes:

* PROVISIONED - the default mode where the table and global secondary indexes have configured read and write capacity.
* PAY_PER_REQUEST - on-demand pricing and scaling. You only pay for what you use and there is no read and write capacity for the table or its global secondary indexes.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_dynamodb as dynamodb

table = dynamodb.Table(self, "Table",
    partition_key=Attribute(name="id", type=dynamodb.AttributeType.STRING),
    billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST
)
```

Further reading:
https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.ReadWriteCapacityMode.

### Configure AutoScaling for your table

You can have DynamoDB automatically raise and lower the read and write capacities
of your table by setting up autoscaling. You can use this to either keep your
tables at a desired utilization level, or by scaling up and down at preconfigured
times of the day:

Auto-scaling is only relevant for tables with the billing mode, PROVISIONED.

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
read_scaling = table.auto_scale_read_capacity(min_capacity=1, max_capacity=50)

read_scaling.scale_on_utilization(
    target_utilization_percent=50
)

read_scaling.scale_on_schedule("ScaleUpInTheMorning",
    schedule=appscaling.Schedule.cron(hour="8", minute="0"),
    min_capacity=20
)

read_scaling.scale_on_schedule("ScaleDownAtNight",
    schedule=appscaling.Schedule.cron(hour="20", minute="0"),
    max_capacity=20
)
```

Further reading:
https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/AutoScaling.html
https://aws.amazon.com/blogs/database/how-to-use-aws-cloudformation-to-configure-auto-scaling-for-amazon-dynamodb-tables-and-indexes/

### Amazon DynamoDB Global Tables

You can create DynamoDB Global Tables by setting the `replicationRegions` property on a `Table`:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_dynamodb as dynamodb

global_table = dynamodb.Table(self, "Table",
    partition_key=Attribute(name="id", type=dynamodb.AttributeType.STRING),
    replication_regions=["us-east-1", "us-east-2", "us-west-2"]
)
```

When doing so, a CloudFormation Custom Resource will be added to the stack in order to create the replica tables in the
selected regions.

### Encryption

All user data stored in Amazon DynamoDB is fully encrypted at rest. When creating a new table, you can choose to encrypt using the following customer master keys (CMK) to encrypt your table:

* AWS owned CMK - By default, all tables are encrypted under an AWS owned customer master key (CMK) in the DynamoDB service account (no additional charges apply).
* AWS managed CMK - AWS KMS keys (one per region) are created in your account, managed, and used on your behalf by AWS DynamoDB (AWS KMS chages apply).
* Customer managed CMK - You have full control over the KMS key used to encrypt the DynamoDB Table (AWS KMS charges apply).

Creating a Table encrypted with a customer managed CMK:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_dynamodb as dynamodb

table = dynamodb.Table(stack, "MyTable",
    partition_key=Attribute(name="id", type=dynamodb.AttributeType.STRING),
    encryption=TableEncryption.CUSTOMER_MANAGED
)

# You can access the CMK that was added to the stack on your behalf by the Table construct via:
table_encryption_key = table.encryption_key
```

You can also supply your own key:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_dynamodb as dynamodb
import aws_cdk.aws_kms as kms

encryption_key = kms.Key(stack, "Key",
    enable_key_rotation=True
)
table = dynamodb.Table(stack, "MyTable",
    partition_key=Attribute(name="id", type=dynamodb.AttributeType.STRING),
    encryption=TableEncryption.CUSTOMER_MANAGED,
    encryption_key=encryption_key
)
```

In order to use the AWS managed CMK instead, change the code to:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_dynamodb as dynamodb

table = dynamodb.Table(stack, "MyTable",
    partition_key=Attribute(name="id", type=dynamodb.AttributeType.STRING),
    encryption=TableEncryption.AWS_MANAGED
)
```
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

import aws_cdk.aws_applicationautoscaling
import aws_cdk.aws_cloudwatch
import aws_cdk.aws_iam
import aws_cdk.aws_kms
import aws_cdk.core


@jsii.data_type(
    jsii_type="@aws-cdk/aws-dynamodb.Attribute",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "type": "type"},
)
class Attribute:
    def __init__(self, *, name: str, type: "AttributeType") -> None:
        """Represents an attribute for describing the key schema for the table and indexes.

        :param name: The name of an attribute.
        :param type: The data type of an attribute.
        """
        self._values = {
            "name": name,
            "type": type,
        }

    @builtins.property
    def name(self) -> str:
        """The name of an attribute."""
        return self._values.get("name")

    @builtins.property
    def type(self) -> "AttributeType":
        """The data type of an attribute."""
        return self._values.get("type")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Attribute(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-dynamodb.AttributeType")
class AttributeType(enum.Enum):
    """Data types for attributes within a table.

    see
    :see: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.NamingRulesDataTypes.html#HowItWorks.DataTypes
    """

    BINARY = "BINARY"
    """Up to 400KiB of binary data (which must be encoded as base64 before sending to DynamoDB)."""
    NUMBER = "NUMBER"
    """Numeric values made of up to 38 digits (positive, negative or zero)."""
    STRING = "STRING"
    """Up to 400KiB of UTF-8 encoded text."""


@jsii.enum(jsii_type="@aws-cdk/aws-dynamodb.BillingMode")
class BillingMode(enum.Enum):
    """DyanmoDB's Read/Write capacity modes."""

    PAY_PER_REQUEST = "PAY_PER_REQUEST"
    """Pay only for what you use.

    You don't configure Read/Write capacity units.
    """
    PROVISIONED = "PROVISIONED"
    """Explicitly specified Read/Write capacity units."""


@jsii.implements(aws_cdk.core.IInspectable)
class CfnTable(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-dynamodb.CfnTable",
):
    """A CloudFormation ``AWS::DynamoDB::Table``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-table.html
    cloudformationResource:
    :cloudformationResource:: AWS::DynamoDB::Table
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: str,
        *,
        key_schema: typing.Union[
            aws_cdk.core.IResolvable,
            typing.List[typing.Union["KeySchemaProperty", aws_cdk.core.IResolvable]],
        ],
        attribute_definitions: typing.Optional[
            typing.Union[
                aws_cdk.core.IResolvable,
                typing.List[
                    typing.Union[
                        aws_cdk.core.IResolvable, "AttributeDefinitionProperty"
                    ]
                ],
            ]
        ] = None,
        billing_mode: typing.Optional[str] = None,
        global_secondary_indexes: typing.Optional[
            typing.Union[
                aws_cdk.core.IResolvable,
                typing.List[
                    typing.Union[
                        aws_cdk.core.IResolvable, "GlobalSecondaryIndexProperty"
                    ]
                ],
            ]
        ] = None,
        local_secondary_indexes: typing.Optional[
            typing.Union[
                aws_cdk.core.IResolvable,
                typing.List[
                    typing.Union[
                        aws_cdk.core.IResolvable, "LocalSecondaryIndexProperty"
                    ]
                ],
            ]
        ] = None,
        point_in_time_recovery_specification: typing.Optional[
            typing.Union[
                aws_cdk.core.IResolvable, "PointInTimeRecoverySpecificationProperty"
            ]
        ] = None,
        provisioned_throughput: typing.Optional[
            typing.Union[aws_cdk.core.IResolvable, "ProvisionedThroughputProperty"]
        ] = None,
        sse_specification: typing.Optional[
            typing.Union[aws_cdk.core.IResolvable, "SSESpecificationProperty"]
        ] = None,
        stream_specification: typing.Optional[
            typing.Union[aws_cdk.core.IResolvable, "StreamSpecificationProperty"]
        ] = None,
        table_name: typing.Optional[str] = None,
        tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]] = None,
        time_to_live_specification: typing.Optional[
            typing.Union[aws_cdk.core.IResolvable, "TimeToLiveSpecificationProperty"]
        ] = None,
    ) -> None:
        """Create a new ``AWS::DynamoDB::Table``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param key_schema: ``AWS::DynamoDB::Table.KeySchema``.
        :param attribute_definitions: ``AWS::DynamoDB::Table.AttributeDefinitions``.
        :param billing_mode: ``AWS::DynamoDB::Table.BillingMode``.
        :param global_secondary_indexes: ``AWS::DynamoDB::Table.GlobalSecondaryIndexes``.
        :param local_secondary_indexes: ``AWS::DynamoDB::Table.LocalSecondaryIndexes``.
        :param point_in_time_recovery_specification: ``AWS::DynamoDB::Table.PointInTimeRecoverySpecification``.
        :param provisioned_throughput: ``AWS::DynamoDB::Table.ProvisionedThroughput``.
        :param sse_specification: ``AWS::DynamoDB::Table.SSESpecification``.
        :param stream_specification: ``AWS::DynamoDB::Table.StreamSpecification``.
        :param table_name: ``AWS::DynamoDB::Table.TableName``.
        :param tags: ``AWS::DynamoDB::Table.Tags``.
        :param time_to_live_specification: ``AWS::DynamoDB::Table.TimeToLiveSpecification``.
        """
        props = CfnTableProps(
            key_schema=key_schema,
            attribute_definitions=attribute_definitions,
            billing_mode=billing_mode,
            global_secondary_indexes=global_secondary_indexes,
            local_secondary_indexes=local_secondary_indexes,
            point_in_time_recovery_specification=point_in_time_recovery_specification,
            provisioned_throughput=provisioned_throughput,
            sse_specification=sse_specification,
            stream_specification=stream_specification,
            table_name=table_name,
            tags=tags,
            time_to_live_specification=time_to_live_specification,
        )

        jsii.create(CfnTable, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(
        cls,
        scope: aws_cdk.core.Construct,
        id: str,
        resource_attributes: typing.Any,
        *,
        finder: aws_cdk.core.ICfnFinder,
    ) -> "CfnTable":
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
    @jsii.member(jsii_name="attrStreamArn")
    def attr_stream_arn(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: StreamArn
        """
        return jsii.get(self, "attrStreamArn")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        """``AWS::DynamoDB::Table.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-table.html#cfn-dynamodb-table-tags
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="keySchema")
    def key_schema(
        self,
    ) -> typing.Union[
        aws_cdk.core.IResolvable,
        typing.List[typing.Union["KeySchemaProperty", aws_cdk.core.IResolvable]],
    ]:
        """``AWS::DynamoDB::Table.KeySchema``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-table.html#cfn-dynamodb-table-keyschema
        """
        return jsii.get(self, "keySchema")

    @key_schema.setter
    def key_schema(
        self,
        value: typing.Union[
            aws_cdk.core.IResolvable,
            typing.List[typing.Union["KeySchemaProperty", aws_cdk.core.IResolvable]],
        ],
    ) -> None:
        jsii.set(self, "keySchema", value)

    @builtins.property
    @jsii.member(jsii_name="attributeDefinitions")
    def attribute_definitions(
        self,
    ) -> typing.Optional[
        typing.Union[
            aws_cdk.core.IResolvable,
            typing.List[
                typing.Union[aws_cdk.core.IResolvable, "AttributeDefinitionProperty"]
            ],
        ]
    ]:
        """``AWS::DynamoDB::Table.AttributeDefinitions``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-table.html#cfn-dynamodb-table-attributedef
        """
        return jsii.get(self, "attributeDefinitions")

    @attribute_definitions.setter
    def attribute_definitions(
        self,
        value: typing.Optional[
            typing.Union[
                aws_cdk.core.IResolvable,
                typing.List[
                    typing.Union[
                        aws_cdk.core.IResolvable, "AttributeDefinitionProperty"
                    ]
                ],
            ]
        ],
    ) -> None:
        jsii.set(self, "attributeDefinitions", value)

    @builtins.property
    @jsii.member(jsii_name="billingMode")
    def billing_mode(self) -> typing.Optional[str]:
        """``AWS::DynamoDB::Table.BillingMode``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-table.html#cfn-dynamodb-table-billingmode
        """
        return jsii.get(self, "billingMode")

    @billing_mode.setter
    def billing_mode(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "billingMode", value)

    @builtins.property
    @jsii.member(jsii_name="globalSecondaryIndexes")
    def global_secondary_indexes(
        self,
    ) -> typing.Optional[
        typing.Union[
            aws_cdk.core.IResolvable,
            typing.List[
                typing.Union[aws_cdk.core.IResolvable, "GlobalSecondaryIndexProperty"]
            ],
        ]
    ]:
        """``AWS::DynamoDB::Table.GlobalSecondaryIndexes``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-table.html#cfn-dynamodb-table-gsi
        """
        return jsii.get(self, "globalSecondaryIndexes")

    @global_secondary_indexes.setter
    def global_secondary_indexes(
        self,
        value: typing.Optional[
            typing.Union[
                aws_cdk.core.IResolvable,
                typing.List[
                    typing.Union[
                        aws_cdk.core.IResolvable, "GlobalSecondaryIndexProperty"
                    ]
                ],
            ]
        ],
    ) -> None:
        jsii.set(self, "globalSecondaryIndexes", value)

    @builtins.property
    @jsii.member(jsii_name="localSecondaryIndexes")
    def local_secondary_indexes(
        self,
    ) -> typing.Optional[
        typing.Union[
            aws_cdk.core.IResolvable,
            typing.List[
                typing.Union[aws_cdk.core.IResolvable, "LocalSecondaryIndexProperty"]
            ],
        ]
    ]:
        """``AWS::DynamoDB::Table.LocalSecondaryIndexes``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-table.html#cfn-dynamodb-table-lsi
        """
        return jsii.get(self, "localSecondaryIndexes")

    @local_secondary_indexes.setter
    def local_secondary_indexes(
        self,
        value: typing.Optional[
            typing.Union[
                aws_cdk.core.IResolvable,
                typing.List[
                    typing.Union[
                        aws_cdk.core.IResolvable, "LocalSecondaryIndexProperty"
                    ]
                ],
            ]
        ],
    ) -> None:
        jsii.set(self, "localSecondaryIndexes", value)

    @builtins.property
    @jsii.member(jsii_name="pointInTimeRecoverySpecification")
    def point_in_time_recovery_specification(
        self,
    ) -> typing.Optional[
        typing.Union[
            aws_cdk.core.IResolvable, "PointInTimeRecoverySpecificationProperty"
        ]
    ]:
        """``AWS::DynamoDB::Table.PointInTimeRecoverySpecification``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-table.html#cfn-dynamodb-table-pointintimerecoveryspecification
        """
        return jsii.get(self, "pointInTimeRecoverySpecification")

    @point_in_time_recovery_specification.setter
    def point_in_time_recovery_specification(
        self,
        value: typing.Optional[
            typing.Union[
                aws_cdk.core.IResolvable, "PointInTimeRecoverySpecificationProperty"
            ]
        ],
    ) -> None:
        jsii.set(self, "pointInTimeRecoverySpecification", value)

    @builtins.property
    @jsii.member(jsii_name="provisionedThroughput")
    def provisioned_throughput(
        self,
    ) -> typing.Optional[
        typing.Union[aws_cdk.core.IResolvable, "ProvisionedThroughputProperty"]
    ]:
        """``AWS::DynamoDB::Table.ProvisionedThroughput``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-table.html#cfn-dynamodb-table-provisionedthroughput
        """
        return jsii.get(self, "provisionedThroughput")

    @provisioned_throughput.setter
    def provisioned_throughput(
        self,
        value: typing.Optional[
            typing.Union[aws_cdk.core.IResolvable, "ProvisionedThroughputProperty"]
        ],
    ) -> None:
        jsii.set(self, "provisionedThroughput", value)

    @builtins.property
    @jsii.member(jsii_name="sseSpecification")
    def sse_specification(
        self,
    ) -> typing.Optional[
        typing.Union[aws_cdk.core.IResolvable, "SSESpecificationProperty"]
    ]:
        """``AWS::DynamoDB::Table.SSESpecification``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-table.html#cfn-dynamodb-table-ssespecification
        """
        return jsii.get(self, "sseSpecification")

    @sse_specification.setter
    def sse_specification(
        self,
        value: typing.Optional[
            typing.Union[aws_cdk.core.IResolvable, "SSESpecificationProperty"]
        ],
    ) -> None:
        jsii.set(self, "sseSpecification", value)

    @builtins.property
    @jsii.member(jsii_name="streamSpecification")
    def stream_specification(
        self,
    ) -> typing.Optional[
        typing.Union[aws_cdk.core.IResolvable, "StreamSpecificationProperty"]
    ]:
        """``AWS::DynamoDB::Table.StreamSpecification``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-table.html#cfn-dynamodb-table-streamspecification
        """
        return jsii.get(self, "streamSpecification")

    @stream_specification.setter
    def stream_specification(
        self,
        value: typing.Optional[
            typing.Union[aws_cdk.core.IResolvable, "StreamSpecificationProperty"]
        ],
    ) -> None:
        jsii.set(self, "streamSpecification", value)

    @builtins.property
    @jsii.member(jsii_name="tableName")
    def table_name(self) -> typing.Optional[str]:
        """``AWS::DynamoDB::Table.TableName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-table.html#cfn-dynamodb-table-tablename
        """
        return jsii.get(self, "tableName")

    @table_name.setter
    def table_name(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "tableName", value)

    @builtins.property
    @jsii.member(jsii_name="timeToLiveSpecification")
    def time_to_live_specification(
        self,
    ) -> typing.Optional[
        typing.Union[aws_cdk.core.IResolvable, "TimeToLiveSpecificationProperty"]
    ]:
        """``AWS::DynamoDB::Table.TimeToLiveSpecification``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-table.html#cfn-dynamodb-table-timetolivespecification
        """
        return jsii.get(self, "timeToLiveSpecification")

    @time_to_live_specification.setter
    def time_to_live_specification(
        self,
        value: typing.Optional[
            typing.Union[aws_cdk.core.IResolvable, "TimeToLiveSpecificationProperty"]
        ],
    ) -> None:
        jsii.set(self, "timeToLiveSpecification", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-dynamodb.CfnTable.AttributeDefinitionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "attribute_name": "attributeName",
            "attribute_type": "attributeType",
        },
    )
    class AttributeDefinitionProperty:
        def __init__(self, *, attribute_name: str, attribute_type: str) -> None:
            """
            :param attribute_name: ``CfnTable.AttributeDefinitionProperty.AttributeName``.
            :param attribute_type: ``CfnTable.AttributeDefinitionProperty.AttributeType``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-attributedef.html
            """
            self._values = {
                "attribute_name": attribute_name,
                "attribute_type": attribute_type,
            }

        @builtins.property
        def attribute_name(self) -> str:
            """``CfnTable.AttributeDefinitionProperty.AttributeName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-attributedef.html#cfn-dynamodb-attributedef-attributename
            """
            return self._values.get("attribute_name")

        @builtins.property
        def attribute_type(self) -> str:
            """``CfnTable.AttributeDefinitionProperty.AttributeType``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-attributedef.html#cfn-dynamodb-attributedef-attributename-attributetype
            """
            return self._values.get("attribute_type")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AttributeDefinitionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-dynamodb.CfnTable.GlobalSecondaryIndexProperty",
        jsii_struct_bases=[],
        name_mapping={
            "index_name": "indexName",
            "key_schema": "keySchema",
            "projection": "projection",
            "provisioned_throughput": "provisionedThroughput",
        },
    )
    class GlobalSecondaryIndexProperty:
        def __init__(
            self,
            *,
            index_name: str,
            key_schema: typing.Union[
                aws_cdk.core.IResolvable,
                typing.List[
                    typing.Union["CfnTable.KeySchemaProperty", aws_cdk.core.IResolvable]
                ],
            ],
            projection: typing.Union[
                aws_cdk.core.IResolvable, "CfnTable.ProjectionProperty"
            ],
            provisioned_throughput: typing.Optional[
                typing.Union[
                    aws_cdk.core.IResolvable, "CfnTable.ProvisionedThroughputProperty"
                ]
            ] = None,
        ) -> None:
            """
            :param index_name: ``CfnTable.GlobalSecondaryIndexProperty.IndexName``.
            :param key_schema: ``CfnTable.GlobalSecondaryIndexProperty.KeySchema``.
            :param projection: ``CfnTable.GlobalSecondaryIndexProperty.Projection``.
            :param provisioned_throughput: ``CfnTable.GlobalSecondaryIndexProperty.ProvisionedThroughput``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-gsi.html
            """
            self._values = {
                "index_name": index_name,
                "key_schema": key_schema,
                "projection": projection,
            }
            if provisioned_throughput is not None:
                self._values["provisioned_throughput"] = provisioned_throughput

        @builtins.property
        def index_name(self) -> str:
            """``CfnTable.GlobalSecondaryIndexProperty.IndexName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-gsi.html#cfn-dynamodb-gsi-indexname
            """
            return self._values.get("index_name")

        @builtins.property
        def key_schema(
            self,
        ) -> typing.Union[
            aws_cdk.core.IResolvable,
            typing.List[
                typing.Union["CfnTable.KeySchemaProperty", aws_cdk.core.IResolvable]
            ],
        ]:
            """``CfnTable.GlobalSecondaryIndexProperty.KeySchema``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-gsi.html#cfn-dynamodb-gsi-keyschema
            """
            return self._values.get("key_schema")

        @builtins.property
        def projection(
            self,
        ) -> typing.Union[aws_cdk.core.IResolvable, "CfnTable.ProjectionProperty"]:
            """``CfnTable.GlobalSecondaryIndexProperty.Projection``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-gsi.html#cfn-dynamodb-gsi-projection
            """
            return self._values.get("projection")

        @builtins.property
        def provisioned_throughput(
            self,
        ) -> typing.Optional[
            typing.Union[
                aws_cdk.core.IResolvable, "CfnTable.ProvisionedThroughputProperty"
            ]
        ]:
            """``CfnTable.GlobalSecondaryIndexProperty.ProvisionedThroughput``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-gsi.html#cfn-dynamodb-gsi-provisionedthroughput
            """
            return self._values.get("provisioned_throughput")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GlobalSecondaryIndexProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-dynamodb.CfnTable.KeySchemaProperty",
        jsii_struct_bases=[],
        name_mapping={"attribute_name": "attributeName", "key_type": "keyType"},
    )
    class KeySchemaProperty:
        def __init__(self, *, attribute_name: str, key_type: str) -> None:
            """
            :param attribute_name: ``CfnTable.KeySchemaProperty.AttributeName``.
            :param key_type: ``CfnTable.KeySchemaProperty.KeyType``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-keyschema.html
            """
            self._values = {
                "attribute_name": attribute_name,
                "key_type": key_type,
            }

        @builtins.property
        def attribute_name(self) -> str:
            """``CfnTable.KeySchemaProperty.AttributeName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-keyschema.html#aws-properties-dynamodb-keyschema-attributename
            """
            return self._values.get("attribute_name")

        @builtins.property
        def key_type(self) -> str:
            """``CfnTable.KeySchemaProperty.KeyType``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-keyschema.html#aws-properties-dynamodb-keyschema-keytype
            """
            return self._values.get("key_type")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "KeySchemaProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-dynamodb.CfnTable.LocalSecondaryIndexProperty",
        jsii_struct_bases=[],
        name_mapping={
            "index_name": "indexName",
            "key_schema": "keySchema",
            "projection": "projection",
        },
    )
    class LocalSecondaryIndexProperty:
        def __init__(
            self,
            *,
            index_name: str,
            key_schema: typing.Union[
                aws_cdk.core.IResolvable,
                typing.List[
                    typing.Union["CfnTable.KeySchemaProperty", aws_cdk.core.IResolvable]
                ],
            ],
            projection: typing.Union[
                aws_cdk.core.IResolvable, "CfnTable.ProjectionProperty"
            ],
        ) -> None:
            """
            :param index_name: ``CfnTable.LocalSecondaryIndexProperty.IndexName``.
            :param key_schema: ``CfnTable.LocalSecondaryIndexProperty.KeySchema``.
            :param projection: ``CfnTable.LocalSecondaryIndexProperty.Projection``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-lsi.html
            """
            self._values = {
                "index_name": index_name,
                "key_schema": key_schema,
                "projection": projection,
            }

        @builtins.property
        def index_name(self) -> str:
            """``CfnTable.LocalSecondaryIndexProperty.IndexName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-lsi.html#cfn-dynamodb-lsi-indexname
            """
            return self._values.get("index_name")

        @builtins.property
        def key_schema(
            self,
        ) -> typing.Union[
            aws_cdk.core.IResolvable,
            typing.List[
                typing.Union["CfnTable.KeySchemaProperty", aws_cdk.core.IResolvable]
            ],
        ]:
            """``CfnTable.LocalSecondaryIndexProperty.KeySchema``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-lsi.html#cfn-dynamodb-lsi-keyschema
            """
            return self._values.get("key_schema")

        @builtins.property
        def projection(
            self,
        ) -> typing.Union[aws_cdk.core.IResolvable, "CfnTable.ProjectionProperty"]:
            """``CfnTable.LocalSecondaryIndexProperty.Projection``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-lsi.html#cfn-dynamodb-lsi-projection
            """
            return self._values.get("projection")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LocalSecondaryIndexProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-dynamodb.CfnTable.PointInTimeRecoverySpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={"point_in_time_recovery_enabled": "pointInTimeRecoveryEnabled"},
    )
    class PointInTimeRecoverySpecificationProperty:
        def __init__(
            self,
            *,
            point_in_time_recovery_enabled: typing.Optional[
                typing.Union[bool, aws_cdk.core.IResolvable]
            ] = None,
        ) -> None:
            """
            :param point_in_time_recovery_enabled: ``CfnTable.PointInTimeRecoverySpecificationProperty.PointInTimeRecoveryEnabled``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-pointintimerecoveryspecification.html
            """
            self._values = {}
            if point_in_time_recovery_enabled is not None:
                self._values[
                    "point_in_time_recovery_enabled"
                ] = point_in_time_recovery_enabled

        @builtins.property
        def point_in_time_recovery_enabled(
            self,
        ) -> typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]]:
            """``CfnTable.PointInTimeRecoverySpecificationProperty.PointInTimeRecoveryEnabled``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-pointintimerecoveryspecification.html#cfn-dynamodb-table-pointintimerecoveryspecification-pointintimerecoveryenabled
            """
            return self._values.get("point_in_time_recovery_enabled")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PointInTimeRecoverySpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-dynamodb.CfnTable.ProjectionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "non_key_attributes": "nonKeyAttributes",
            "projection_type": "projectionType",
        },
    )
    class ProjectionProperty:
        def __init__(
            self,
            *,
            non_key_attributes: typing.Optional[typing.List[str]] = None,
            projection_type: typing.Optional[str] = None,
        ) -> None:
            """
            :param non_key_attributes: ``CfnTable.ProjectionProperty.NonKeyAttributes``.
            :param projection_type: ``CfnTable.ProjectionProperty.ProjectionType``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-projectionobject.html
            """
            self._values = {}
            if non_key_attributes is not None:
                self._values["non_key_attributes"] = non_key_attributes
            if projection_type is not None:
                self._values["projection_type"] = projection_type

        @builtins.property
        def non_key_attributes(self) -> typing.Optional[typing.List[str]]:
            """``CfnTable.ProjectionProperty.NonKeyAttributes``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-projectionobject.html#cfn-dynamodb-projectionobj-nonkeyatt
            """
            return self._values.get("non_key_attributes")

        @builtins.property
        def projection_type(self) -> typing.Optional[str]:
            """``CfnTable.ProjectionProperty.ProjectionType``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-projectionobject.html#cfn-dynamodb-projectionobj-projtype
            """
            return self._values.get("projection_type")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ProjectionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-dynamodb.CfnTable.ProvisionedThroughputProperty",
        jsii_struct_bases=[],
        name_mapping={
            "read_capacity_units": "readCapacityUnits",
            "write_capacity_units": "writeCapacityUnits",
        },
    )
    class ProvisionedThroughputProperty:
        def __init__(
            self, *, read_capacity_units: jsii.Number, write_capacity_units: jsii.Number
        ) -> None:
            """
            :param read_capacity_units: ``CfnTable.ProvisionedThroughputProperty.ReadCapacityUnits``.
            :param write_capacity_units: ``CfnTable.ProvisionedThroughputProperty.WriteCapacityUnits``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-provisionedthroughput.html
            """
            self._values = {
                "read_capacity_units": read_capacity_units,
                "write_capacity_units": write_capacity_units,
            }

        @builtins.property
        def read_capacity_units(self) -> jsii.Number:
            """``CfnTable.ProvisionedThroughputProperty.ReadCapacityUnits``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-provisionedthroughput.html#cfn-dynamodb-provisionedthroughput-readcapacityunits
            """
            return self._values.get("read_capacity_units")

        @builtins.property
        def write_capacity_units(self) -> jsii.Number:
            """``CfnTable.ProvisionedThroughputProperty.WriteCapacityUnits``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-provisionedthroughput.html#cfn-dynamodb-provisionedthroughput-writecapacityunits
            """
            return self._values.get("write_capacity_units")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ProvisionedThroughputProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-dynamodb.CfnTable.SSESpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "sse_enabled": "sseEnabled",
            "kms_master_key_id": "kmsMasterKeyId",
            "sse_type": "sseType",
        },
    )
    class SSESpecificationProperty:
        def __init__(
            self,
            *,
            sse_enabled: typing.Union[bool, aws_cdk.core.IResolvable],
            kms_master_key_id: typing.Optional[str] = None,
            sse_type: typing.Optional[str] = None,
        ) -> None:
            """
            :param sse_enabled: ``CfnTable.SSESpecificationProperty.SSEEnabled``.
            :param kms_master_key_id: ``CfnTable.SSESpecificationProperty.KMSMasterKeyId``.
            :param sse_type: ``CfnTable.SSESpecificationProperty.SSEType``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-ssespecification.html
            """
            self._values = {
                "sse_enabled": sse_enabled,
            }
            if kms_master_key_id is not None:
                self._values["kms_master_key_id"] = kms_master_key_id
            if sse_type is not None:
                self._values["sse_type"] = sse_type

        @builtins.property
        def sse_enabled(self) -> typing.Union[bool, aws_cdk.core.IResolvable]:
            """``CfnTable.SSESpecificationProperty.SSEEnabled``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-ssespecification.html#cfn-dynamodb-table-ssespecification-sseenabled
            """
            return self._values.get("sse_enabled")

        @builtins.property
        def kms_master_key_id(self) -> typing.Optional[str]:
            """``CfnTable.SSESpecificationProperty.KMSMasterKeyId``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-ssespecification.html#cfn-dynamodb-table-ssespecification-kmsmasterkeyid
            """
            return self._values.get("kms_master_key_id")

        @builtins.property
        def sse_type(self) -> typing.Optional[str]:
            """``CfnTable.SSESpecificationProperty.SSEType``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-ssespecification.html#cfn-dynamodb-table-ssespecification-ssetype
            """
            return self._values.get("sse_type")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SSESpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-dynamodb.CfnTable.StreamSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={"stream_view_type": "streamViewType"},
    )
    class StreamSpecificationProperty:
        def __init__(self, *, stream_view_type: str) -> None:
            """
            :param stream_view_type: ``CfnTable.StreamSpecificationProperty.StreamViewType``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-streamspecification.html
            """
            self._values = {
                "stream_view_type": stream_view_type,
            }

        @builtins.property
        def stream_view_type(self) -> str:
            """``CfnTable.StreamSpecificationProperty.StreamViewType``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-streamspecification.html#cfn-dynamodb-streamspecification-streamviewtype
            """
            return self._values.get("stream_view_type")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StreamSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-dynamodb.CfnTable.TimeToLiveSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={"attribute_name": "attributeName", "enabled": "enabled"},
    )
    class TimeToLiveSpecificationProperty:
        def __init__(
            self,
            *,
            attribute_name: str,
            enabled: typing.Union[bool, aws_cdk.core.IResolvable],
        ) -> None:
            """
            :param attribute_name: ``CfnTable.TimeToLiveSpecificationProperty.AttributeName``.
            :param enabled: ``CfnTable.TimeToLiveSpecificationProperty.Enabled``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-timetolivespecification.html
            """
            self._values = {
                "attribute_name": attribute_name,
                "enabled": enabled,
            }

        @builtins.property
        def attribute_name(self) -> str:
            """``CfnTable.TimeToLiveSpecificationProperty.AttributeName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-timetolivespecification.html#cfn-dynamodb-timetolivespecification-attributename
            """
            return self._values.get("attribute_name")

        @builtins.property
        def enabled(self) -> typing.Union[bool, aws_cdk.core.IResolvable]:
            """``CfnTable.TimeToLiveSpecificationProperty.Enabled``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-timetolivespecification.html#cfn-dynamodb-timetolivespecification-enabled
            """
            return self._values.get("enabled")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TimeToLiveSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-dynamodb.CfnTableProps",
    jsii_struct_bases=[],
    name_mapping={
        "key_schema": "keySchema",
        "attribute_definitions": "attributeDefinitions",
        "billing_mode": "billingMode",
        "global_secondary_indexes": "globalSecondaryIndexes",
        "local_secondary_indexes": "localSecondaryIndexes",
        "point_in_time_recovery_specification": "pointInTimeRecoverySpecification",
        "provisioned_throughput": "provisionedThroughput",
        "sse_specification": "sseSpecification",
        "stream_specification": "streamSpecification",
        "table_name": "tableName",
        "tags": "tags",
        "time_to_live_specification": "timeToLiveSpecification",
    },
)
class CfnTableProps:
    def __init__(
        self,
        *,
        key_schema: typing.Union[
            aws_cdk.core.IResolvable,
            typing.List[
                typing.Union["CfnTable.KeySchemaProperty", aws_cdk.core.IResolvable]
            ],
        ],
        attribute_definitions: typing.Optional[
            typing.Union[
                aws_cdk.core.IResolvable,
                typing.List[
                    typing.Union[
                        aws_cdk.core.IResolvable, "CfnTable.AttributeDefinitionProperty"
                    ]
                ],
            ]
        ] = None,
        billing_mode: typing.Optional[str] = None,
        global_secondary_indexes: typing.Optional[
            typing.Union[
                aws_cdk.core.IResolvable,
                typing.List[
                    typing.Union[
                        aws_cdk.core.IResolvable,
                        "CfnTable.GlobalSecondaryIndexProperty",
                    ]
                ],
            ]
        ] = None,
        local_secondary_indexes: typing.Optional[
            typing.Union[
                aws_cdk.core.IResolvable,
                typing.List[
                    typing.Union[
                        aws_cdk.core.IResolvable, "CfnTable.LocalSecondaryIndexProperty"
                    ]
                ],
            ]
        ] = None,
        point_in_time_recovery_specification: typing.Optional[
            typing.Union[
                aws_cdk.core.IResolvable,
                "CfnTable.PointInTimeRecoverySpecificationProperty",
            ]
        ] = None,
        provisioned_throughput: typing.Optional[
            typing.Union[
                aws_cdk.core.IResolvable, "CfnTable.ProvisionedThroughputProperty"
            ]
        ] = None,
        sse_specification: typing.Optional[
            typing.Union[aws_cdk.core.IResolvable, "CfnTable.SSESpecificationProperty"]
        ] = None,
        stream_specification: typing.Optional[
            typing.Union[
                aws_cdk.core.IResolvable, "CfnTable.StreamSpecificationProperty"
            ]
        ] = None,
        table_name: typing.Optional[str] = None,
        tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]] = None,
        time_to_live_specification: typing.Optional[
            typing.Union[
                aws_cdk.core.IResolvable, "CfnTable.TimeToLiveSpecificationProperty"
            ]
        ] = None,
    ) -> None:
        """Properties for defining a ``AWS::DynamoDB::Table``.

        :param key_schema: ``AWS::DynamoDB::Table.KeySchema``.
        :param attribute_definitions: ``AWS::DynamoDB::Table.AttributeDefinitions``.
        :param billing_mode: ``AWS::DynamoDB::Table.BillingMode``.
        :param global_secondary_indexes: ``AWS::DynamoDB::Table.GlobalSecondaryIndexes``.
        :param local_secondary_indexes: ``AWS::DynamoDB::Table.LocalSecondaryIndexes``.
        :param point_in_time_recovery_specification: ``AWS::DynamoDB::Table.PointInTimeRecoverySpecification``.
        :param provisioned_throughput: ``AWS::DynamoDB::Table.ProvisionedThroughput``.
        :param sse_specification: ``AWS::DynamoDB::Table.SSESpecification``.
        :param stream_specification: ``AWS::DynamoDB::Table.StreamSpecification``.
        :param table_name: ``AWS::DynamoDB::Table.TableName``.
        :param tags: ``AWS::DynamoDB::Table.Tags``.
        :param time_to_live_specification: ``AWS::DynamoDB::Table.TimeToLiveSpecification``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-table.html
        """
        self._values = {
            "key_schema": key_schema,
        }
        if attribute_definitions is not None:
            self._values["attribute_definitions"] = attribute_definitions
        if billing_mode is not None:
            self._values["billing_mode"] = billing_mode
        if global_secondary_indexes is not None:
            self._values["global_secondary_indexes"] = global_secondary_indexes
        if local_secondary_indexes is not None:
            self._values["local_secondary_indexes"] = local_secondary_indexes
        if point_in_time_recovery_specification is not None:
            self._values[
                "point_in_time_recovery_specification"
            ] = point_in_time_recovery_specification
        if provisioned_throughput is not None:
            self._values["provisioned_throughput"] = provisioned_throughput
        if sse_specification is not None:
            self._values["sse_specification"] = sse_specification
        if stream_specification is not None:
            self._values["stream_specification"] = stream_specification
        if table_name is not None:
            self._values["table_name"] = table_name
        if tags is not None:
            self._values["tags"] = tags
        if time_to_live_specification is not None:
            self._values["time_to_live_specification"] = time_to_live_specification

    @builtins.property
    def key_schema(
        self,
    ) -> typing.Union[
        aws_cdk.core.IResolvable,
        typing.List[
            typing.Union["CfnTable.KeySchemaProperty", aws_cdk.core.IResolvable]
        ],
    ]:
        """``AWS::DynamoDB::Table.KeySchema``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-table.html#cfn-dynamodb-table-keyschema
        """
        return self._values.get("key_schema")

    @builtins.property
    def attribute_definitions(
        self,
    ) -> typing.Optional[
        typing.Union[
            aws_cdk.core.IResolvable,
            typing.List[
                typing.Union[
                    aws_cdk.core.IResolvable, "CfnTable.AttributeDefinitionProperty"
                ]
            ],
        ]
    ]:
        """``AWS::DynamoDB::Table.AttributeDefinitions``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-table.html#cfn-dynamodb-table-attributedef
        """
        return self._values.get("attribute_definitions")

    @builtins.property
    def billing_mode(self) -> typing.Optional[str]:
        """``AWS::DynamoDB::Table.BillingMode``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-table.html#cfn-dynamodb-table-billingmode
        """
        return self._values.get("billing_mode")

    @builtins.property
    def global_secondary_indexes(
        self,
    ) -> typing.Optional[
        typing.Union[
            aws_cdk.core.IResolvable,
            typing.List[
                typing.Union[
                    aws_cdk.core.IResolvable, "CfnTable.GlobalSecondaryIndexProperty"
                ]
            ],
        ]
    ]:
        """``AWS::DynamoDB::Table.GlobalSecondaryIndexes``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-table.html#cfn-dynamodb-table-gsi
        """
        return self._values.get("global_secondary_indexes")

    @builtins.property
    def local_secondary_indexes(
        self,
    ) -> typing.Optional[
        typing.Union[
            aws_cdk.core.IResolvable,
            typing.List[
                typing.Union[
                    aws_cdk.core.IResolvable, "CfnTable.LocalSecondaryIndexProperty"
                ]
            ],
        ]
    ]:
        """``AWS::DynamoDB::Table.LocalSecondaryIndexes``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-table.html#cfn-dynamodb-table-lsi
        """
        return self._values.get("local_secondary_indexes")

    @builtins.property
    def point_in_time_recovery_specification(
        self,
    ) -> typing.Optional[
        typing.Union[
            aws_cdk.core.IResolvable,
            "CfnTable.PointInTimeRecoverySpecificationProperty",
        ]
    ]:
        """``AWS::DynamoDB::Table.PointInTimeRecoverySpecification``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-table.html#cfn-dynamodb-table-pointintimerecoveryspecification
        """
        return self._values.get("point_in_time_recovery_specification")

    @builtins.property
    def provisioned_throughput(
        self,
    ) -> typing.Optional[
        typing.Union[aws_cdk.core.IResolvable, "CfnTable.ProvisionedThroughputProperty"]
    ]:
        """``AWS::DynamoDB::Table.ProvisionedThroughput``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-table.html#cfn-dynamodb-table-provisionedthroughput
        """
        return self._values.get("provisioned_throughput")

    @builtins.property
    def sse_specification(
        self,
    ) -> typing.Optional[
        typing.Union[aws_cdk.core.IResolvable, "CfnTable.SSESpecificationProperty"]
    ]:
        """``AWS::DynamoDB::Table.SSESpecification``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-table.html#cfn-dynamodb-table-ssespecification
        """
        return self._values.get("sse_specification")

    @builtins.property
    def stream_specification(
        self,
    ) -> typing.Optional[
        typing.Union[aws_cdk.core.IResolvable, "CfnTable.StreamSpecificationProperty"]
    ]:
        """``AWS::DynamoDB::Table.StreamSpecification``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-table.html#cfn-dynamodb-table-streamspecification
        """
        return self._values.get("stream_specification")

    @builtins.property
    def table_name(self) -> typing.Optional[str]:
        """``AWS::DynamoDB::Table.TableName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-table.html#cfn-dynamodb-table-tablename
        """
        return self._values.get("table_name")

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        """``AWS::DynamoDB::Table.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-table.html#cfn-dynamodb-table-tags
        """
        return self._values.get("tags")

    @builtins.property
    def time_to_live_specification(
        self,
    ) -> typing.Optional[
        typing.Union[
            aws_cdk.core.IResolvable, "CfnTable.TimeToLiveSpecificationProperty"
        ]
    ]:
        """``AWS::DynamoDB::Table.TimeToLiveSpecification``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-table.html#cfn-dynamodb-table-timetolivespecification
        """
        return self._values.get("time_to_live_specification")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnTableProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-dynamodb.EnableScalingProps",
    jsii_struct_bases=[],
    name_mapping={"max_capacity": "maxCapacity", "min_capacity": "minCapacity"},
)
class EnableScalingProps:
    def __init__(self, *, max_capacity: jsii.Number, min_capacity: jsii.Number) -> None:
        """Properties for enabling DynamoDB capacity scaling.

        :param max_capacity: Maximum capacity to scale to.
        :param min_capacity: Minimum capacity to scale to.
        """
        self._values = {
            "max_capacity": max_capacity,
            "min_capacity": min_capacity,
        }

    @builtins.property
    def max_capacity(self) -> jsii.Number:
        """Maximum capacity to scale to."""
        return self._values.get("max_capacity")

    @builtins.property
    def min_capacity(self) -> jsii.Number:
        """Minimum capacity to scale to."""
        return self._values.get("min_capacity")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EnableScalingProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="@aws-cdk/aws-dynamodb.IScalableTableAttribute")
class IScalableTableAttribute(jsii.compat.Protocol):
    """Interface for scalable attributes."""

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IScalableTableAttributeProxy

    @jsii.member(jsii_name="scaleOnSchedule")
    def scale_on_schedule(
        self,
        id: str,
        *,
        schedule: aws_cdk.aws_applicationautoscaling.Schedule,
        end_time: typing.Optional[datetime.datetime] = None,
        max_capacity: typing.Optional[jsii.Number] = None,
        min_capacity: typing.Optional[jsii.Number] = None,
        start_time: typing.Optional[datetime.datetime] = None,
    ) -> None:
        """Add scheduled scaling for this scaling attribute.

        :param id: -
        :param schedule: When to perform this action.
        :param end_time: When this scheduled action expires. Default: The rule never expires.
        :param max_capacity: The new maximum capacity. During the scheduled time, the current capacity is above the maximum capacity, Application Auto Scaling scales in to the maximum capacity. At least one of maxCapacity and minCapacity must be supplied. Default: No new maximum capacity
        :param min_capacity: The new minimum capacity. During the scheduled time, if the current capacity is below the minimum capacity, Application Auto Scaling scales out to the minimum capacity. At least one of maxCapacity and minCapacity must be supplied. Default: No new minimum capacity
        :param start_time: When this scheduled action becomes active. Default: The rule is activate immediately
        """
        ...

    @jsii.member(jsii_name="scaleOnUtilization")
    def scale_on_utilization(
        self,
        *,
        target_utilization_percent: jsii.Number,
        disable_scale_in: typing.Optional[bool] = None,
        policy_name: typing.Optional[str] = None,
        scale_in_cooldown: typing.Optional[aws_cdk.core.Duration] = None,
        scale_out_cooldown: typing.Optional[aws_cdk.core.Duration] = None,
    ) -> None:
        """Scale out or in to keep utilization at a given level.

        :param target_utilization_percent: Target utilization percentage for the attribute.
        :param disable_scale_in: Indicates whether scale in by the target tracking policy is disabled. If the value is true, scale in is disabled and the target tracking policy won't remove capacity from the scalable resource. Otherwise, scale in is enabled and the target tracking policy can remove capacity from the scalable resource. Default: false
        :param policy_name: A name for the scaling policy. Default: - Automatically generated name.
        :param scale_in_cooldown: Period after a scale in activity completes before another scale in activity can start. Default: Duration.seconds(300) for the following scalable targets: ECS services, Spot Fleet requests, EMR clusters, AppStream 2.0 fleets, Aurora DB clusters, Amazon SageMaker endpoint variants, Custom resources. For all other scalable targets, the default value is Duration.seconds(0): DynamoDB tables, DynamoDB global secondary indexes, Amazon Comprehend document classification endpoints, Lambda provisioned concurrency
        :param scale_out_cooldown: Period after a scale out activity completes before another scale out activity can start. Default: Duration.seconds(300) for the following scalable targets: ECS services, Spot Fleet requests, EMR clusters, AppStream 2.0 fleets, Aurora DB clusters, Amazon SageMaker endpoint variants, Custom resources. For all other scalable targets, the default value is Duration.seconds(0): DynamoDB tables, DynamoDB global secondary indexes, Amazon Comprehend document classification endpoints, Lambda provisioned concurrency
        """
        ...


class _IScalableTableAttributeProxy:
    """Interface for scalable attributes."""

    __jsii_type__ = "@aws-cdk/aws-dynamodb.IScalableTableAttribute"

    @jsii.member(jsii_name="scaleOnSchedule")
    def scale_on_schedule(
        self,
        id: str,
        *,
        schedule: aws_cdk.aws_applicationautoscaling.Schedule,
        end_time: typing.Optional[datetime.datetime] = None,
        max_capacity: typing.Optional[jsii.Number] = None,
        min_capacity: typing.Optional[jsii.Number] = None,
        start_time: typing.Optional[datetime.datetime] = None,
    ) -> None:
        """Add scheduled scaling for this scaling attribute.

        :param id: -
        :param schedule: When to perform this action.
        :param end_time: When this scheduled action expires. Default: The rule never expires.
        :param max_capacity: The new maximum capacity. During the scheduled time, the current capacity is above the maximum capacity, Application Auto Scaling scales in to the maximum capacity. At least one of maxCapacity and minCapacity must be supplied. Default: No new maximum capacity
        :param min_capacity: The new minimum capacity. During the scheduled time, if the current capacity is below the minimum capacity, Application Auto Scaling scales out to the minimum capacity. At least one of maxCapacity and minCapacity must be supplied. Default: No new minimum capacity
        :param start_time: When this scheduled action becomes active. Default: The rule is activate immediately
        """
        actions = aws_cdk.aws_applicationautoscaling.ScalingSchedule(
            schedule=schedule,
            end_time=end_time,
            max_capacity=max_capacity,
            min_capacity=min_capacity,
            start_time=start_time,
        )

        return jsii.invoke(self, "scaleOnSchedule", [id, actions])

    @jsii.member(jsii_name="scaleOnUtilization")
    def scale_on_utilization(
        self,
        *,
        target_utilization_percent: jsii.Number,
        disable_scale_in: typing.Optional[bool] = None,
        policy_name: typing.Optional[str] = None,
        scale_in_cooldown: typing.Optional[aws_cdk.core.Duration] = None,
        scale_out_cooldown: typing.Optional[aws_cdk.core.Duration] = None,
    ) -> None:
        """Scale out or in to keep utilization at a given level.

        :param target_utilization_percent: Target utilization percentage for the attribute.
        :param disable_scale_in: Indicates whether scale in by the target tracking policy is disabled. If the value is true, scale in is disabled and the target tracking policy won't remove capacity from the scalable resource. Otherwise, scale in is enabled and the target tracking policy can remove capacity from the scalable resource. Default: false
        :param policy_name: A name for the scaling policy. Default: - Automatically generated name.
        :param scale_in_cooldown: Period after a scale in activity completes before another scale in activity can start. Default: Duration.seconds(300) for the following scalable targets: ECS services, Spot Fleet requests, EMR clusters, AppStream 2.0 fleets, Aurora DB clusters, Amazon SageMaker endpoint variants, Custom resources. For all other scalable targets, the default value is Duration.seconds(0): DynamoDB tables, DynamoDB global secondary indexes, Amazon Comprehend document classification endpoints, Lambda provisioned concurrency
        :param scale_out_cooldown: Period after a scale out activity completes before another scale out activity can start. Default: Duration.seconds(300) for the following scalable targets: ECS services, Spot Fleet requests, EMR clusters, AppStream 2.0 fleets, Aurora DB clusters, Amazon SageMaker endpoint variants, Custom resources. For all other scalable targets, the default value is Duration.seconds(0): DynamoDB tables, DynamoDB global secondary indexes, Amazon Comprehend document classification endpoints, Lambda provisioned concurrency
        """
        props = UtilizationScalingProps(
            target_utilization_percent=target_utilization_percent,
            disable_scale_in=disable_scale_in,
            policy_name=policy_name,
            scale_in_cooldown=scale_in_cooldown,
            scale_out_cooldown=scale_out_cooldown,
        )

        return jsii.invoke(self, "scaleOnUtilization", [props])


@jsii.interface(jsii_type="@aws-cdk/aws-dynamodb.ITable")
class ITable(aws_cdk.core.IResource, jsii.compat.Protocol):
    """An interface that represents a DynamoDB Table - either created with the CDK, or an existing one."""

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _ITableProxy

    @builtins.property
    @jsii.member(jsii_name="tableArn")
    def table_arn(self) -> str:
        """Arn of the dynamodb table.

        attribute:
        :attribute:: true
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="tableName")
    def table_name(self) -> str:
        """Table name of the dynamodb table.

        attribute:
        :attribute:: true
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="encryptionKey")
    def encryption_key(self) -> typing.Optional[aws_cdk.aws_kms.IKey]:
        """Optional KMS encryption key associated with this table."""
        ...

    @builtins.property
    @jsii.member(jsii_name="tableStreamArn")
    def table_stream_arn(self) -> typing.Optional[str]:
        """ARN of the table's stream, if there is one.

        attribute:
        :attribute:: true
        """
        ...

    @jsii.member(jsii_name="grant")
    def grant(
        self, grantee: aws_cdk.aws_iam.IGrantable, *actions: str
    ) -> aws_cdk.aws_iam.Grant:
        """Adds an IAM policy statement associated with this table to an IAM principal's policy.

        If ``encryptionKey`` is present, appropriate grants to the key needs to be added
        separately using the ``table.encryptionKey.grant*`` methods.

        :param grantee: The principal (no-op if undefined).
        :param actions: The set of actions to allow (i.e. "dynamodb:PutItem", "dynamodb:GetItem", ...).
        """
        ...

    @jsii.member(jsii_name="grantFullAccess")
    def grant_full_access(
        self, grantee: aws_cdk.aws_iam.IGrantable
    ) -> aws_cdk.aws_iam.Grant:
        """Permits all DynamoDB operations ("dynamodb:*") to an IAM principal.

        Appropriate grants will also be added to the customer-managed KMS key
        if one was configured.

        :param grantee: The principal to grant access to.
        """
        ...

    @jsii.member(jsii_name="grantReadData")
    def grant_read_data(
        self, grantee: aws_cdk.aws_iam.IGrantable
    ) -> aws_cdk.aws_iam.Grant:
        """Permits an IAM principal all data read operations from this table: BatchGetItem, GetRecords, GetShardIterator, Query, GetItem, Scan.

        Appropriate grants will also be added to the customer-managed KMS key
        if one was configured.

        :param grantee: The principal to grant access to.
        """
        ...

    @jsii.member(jsii_name="grantReadWriteData")
    def grant_read_write_data(
        self, grantee: aws_cdk.aws_iam.IGrantable
    ) -> aws_cdk.aws_iam.Grant:
        """Permits an IAM principal to all data read/write operations to this table.

        BatchGetItem, GetRecords, GetShardIterator, Query, GetItem, Scan,
        BatchWriteItem, PutItem, UpdateItem, DeleteItem

        Appropriate grants will also be added to the customer-managed KMS key
        if one was configured.

        :param grantee: The principal to grant access to.
        """
        ...

    @jsii.member(jsii_name="grantStream")
    def grant_stream(
        self, grantee: aws_cdk.aws_iam.IGrantable, *actions: str
    ) -> aws_cdk.aws_iam.Grant:
        """Adds an IAM policy statement associated with this table's stream to an IAM principal's policy.

        If ``encryptionKey`` is present, appropriate grants to the key needs to be added
        separately using the ``table.encryptionKey.grant*`` methods.

        :param grantee: The principal (no-op if undefined).
        :param actions: The set of actions to allow (i.e. "dynamodb:DescribeStream", "dynamodb:GetRecords", ...).
        """
        ...

    @jsii.member(jsii_name="grantStreamRead")
    def grant_stream_read(
        self, grantee: aws_cdk.aws_iam.IGrantable
    ) -> aws_cdk.aws_iam.Grant:
        """Permits an IAM principal all stream data read operations for this table's stream: DescribeStream, GetRecords, GetShardIterator, ListStreams.

        Appropriate grants will also be added to the customer-managed KMS key
        if one was configured.

        :param grantee: The principal to grant access to.
        """
        ...

    @jsii.member(jsii_name="grantTableListStreams")
    def grant_table_list_streams(
        self, grantee: aws_cdk.aws_iam.IGrantable
    ) -> aws_cdk.aws_iam.Grant:
        """Permits an IAM Principal to list streams attached to current dynamodb table.

        :param grantee: The principal (no-op if undefined).
        """
        ...

    @jsii.member(jsii_name="grantWriteData")
    def grant_write_data(
        self, grantee: aws_cdk.aws_iam.IGrantable
    ) -> aws_cdk.aws_iam.Grant:
        """Permits an IAM principal all data write operations to this table: BatchWriteItem, PutItem, UpdateItem, DeleteItem.

        Appropriate grants will also be added to the customer-managed KMS key
        if one was configured.

        :param grantee: The principal to grant access to.
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
        """Metric for the number of Errors executing all Lambdas.

        :param metric_name: -
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        """
        ...

    @jsii.member(jsii_name="metricConditionalCheckFailedRequests")
    def metric_conditional_check_failed_requests(
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
        """Metric for the conditional check failed requests.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        """
        ...

    @jsii.member(jsii_name="metricConsumedReadCapacityUnits")
    def metric_consumed_read_capacity_units(
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
        """Metric for the consumed read capacity units.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        """
        ...

    @jsii.member(jsii_name="metricConsumedWriteCapacityUnits")
    def metric_consumed_write_capacity_units(
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
        """Metric for the consumed write capacity units.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        """
        ...

    @jsii.member(jsii_name="metricSuccessfulRequestLatency")
    def metric_successful_request_latency(
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
        """Metric for the successful request latency.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        """
        ...

    @jsii.member(jsii_name="metricSystemErrors")
    def metric_system_errors(
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
        """Metric for the system errors.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        """
        ...

    @jsii.member(jsii_name="metricUserErrors")
    def metric_user_errors(
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
        """Metric for the user errors.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        """
        ...


class _ITableProxy(jsii.proxy_for(aws_cdk.core.IResource)):
    """An interface that represents a DynamoDB Table - either created with the CDK, or an existing one."""

    __jsii_type__ = "@aws-cdk/aws-dynamodb.ITable"

    @builtins.property
    @jsii.member(jsii_name="tableArn")
    def table_arn(self) -> str:
        """Arn of the dynamodb table.

        attribute:
        :attribute:: true
        """
        return jsii.get(self, "tableArn")

    @builtins.property
    @jsii.member(jsii_name="tableName")
    def table_name(self) -> str:
        """Table name of the dynamodb table.

        attribute:
        :attribute:: true
        """
        return jsii.get(self, "tableName")

    @builtins.property
    @jsii.member(jsii_name="encryptionKey")
    def encryption_key(self) -> typing.Optional[aws_cdk.aws_kms.IKey]:
        """Optional KMS encryption key associated with this table."""
        return jsii.get(self, "encryptionKey")

    @builtins.property
    @jsii.member(jsii_name="tableStreamArn")
    def table_stream_arn(self) -> typing.Optional[str]:
        """ARN of the table's stream, if there is one.

        attribute:
        :attribute:: true
        """
        return jsii.get(self, "tableStreamArn")

    @jsii.member(jsii_name="grant")
    def grant(
        self, grantee: aws_cdk.aws_iam.IGrantable, *actions: str
    ) -> aws_cdk.aws_iam.Grant:
        """Adds an IAM policy statement associated with this table to an IAM principal's policy.

        If ``encryptionKey`` is present, appropriate grants to the key needs to be added
        separately using the ``table.encryptionKey.grant*`` methods.

        :param grantee: The principal (no-op if undefined).
        :param actions: The set of actions to allow (i.e. "dynamodb:PutItem", "dynamodb:GetItem", ...).
        """
        return jsii.invoke(self, "grant", [grantee, *actions])

    @jsii.member(jsii_name="grantFullAccess")
    def grant_full_access(
        self, grantee: aws_cdk.aws_iam.IGrantable
    ) -> aws_cdk.aws_iam.Grant:
        """Permits all DynamoDB operations ("dynamodb:*") to an IAM principal.

        Appropriate grants will also be added to the customer-managed KMS key
        if one was configured.

        :param grantee: The principal to grant access to.
        """
        return jsii.invoke(self, "grantFullAccess", [grantee])

    @jsii.member(jsii_name="grantReadData")
    def grant_read_data(
        self, grantee: aws_cdk.aws_iam.IGrantable
    ) -> aws_cdk.aws_iam.Grant:
        """Permits an IAM principal all data read operations from this table: BatchGetItem, GetRecords, GetShardIterator, Query, GetItem, Scan.

        Appropriate grants will also be added to the customer-managed KMS key
        if one was configured.

        :param grantee: The principal to grant access to.
        """
        return jsii.invoke(self, "grantReadData", [grantee])

    @jsii.member(jsii_name="grantReadWriteData")
    def grant_read_write_data(
        self, grantee: aws_cdk.aws_iam.IGrantable
    ) -> aws_cdk.aws_iam.Grant:
        """Permits an IAM principal to all data read/write operations to this table.

        BatchGetItem, GetRecords, GetShardIterator, Query, GetItem, Scan,
        BatchWriteItem, PutItem, UpdateItem, DeleteItem

        Appropriate grants will also be added to the customer-managed KMS key
        if one was configured.

        :param grantee: The principal to grant access to.
        """
        return jsii.invoke(self, "grantReadWriteData", [grantee])

    @jsii.member(jsii_name="grantStream")
    def grant_stream(
        self, grantee: aws_cdk.aws_iam.IGrantable, *actions: str
    ) -> aws_cdk.aws_iam.Grant:
        """Adds an IAM policy statement associated with this table's stream to an IAM principal's policy.

        If ``encryptionKey`` is present, appropriate grants to the key needs to be added
        separately using the ``table.encryptionKey.grant*`` methods.

        :param grantee: The principal (no-op if undefined).
        :param actions: The set of actions to allow (i.e. "dynamodb:DescribeStream", "dynamodb:GetRecords", ...).
        """
        return jsii.invoke(self, "grantStream", [grantee, *actions])

    @jsii.member(jsii_name="grantStreamRead")
    def grant_stream_read(
        self, grantee: aws_cdk.aws_iam.IGrantable
    ) -> aws_cdk.aws_iam.Grant:
        """Permits an IAM principal all stream data read operations for this table's stream: DescribeStream, GetRecords, GetShardIterator, ListStreams.

        Appropriate grants will also be added to the customer-managed KMS key
        if one was configured.

        :param grantee: The principal to grant access to.
        """
        return jsii.invoke(self, "grantStreamRead", [grantee])

    @jsii.member(jsii_name="grantTableListStreams")
    def grant_table_list_streams(
        self, grantee: aws_cdk.aws_iam.IGrantable
    ) -> aws_cdk.aws_iam.Grant:
        """Permits an IAM Principal to list streams attached to current dynamodb table.

        :param grantee: The principal (no-op if undefined).
        """
        return jsii.invoke(self, "grantTableListStreams", [grantee])

    @jsii.member(jsii_name="grantWriteData")
    def grant_write_data(
        self, grantee: aws_cdk.aws_iam.IGrantable
    ) -> aws_cdk.aws_iam.Grant:
        """Permits an IAM principal all data write operations to this table: BatchWriteItem, PutItem, UpdateItem, DeleteItem.

        Appropriate grants will also be added to the customer-managed KMS key
        if one was configured.

        :param grantee: The principal to grant access to.
        """
        return jsii.invoke(self, "grantWriteData", [grantee])

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
        """Metric for the number of Errors executing all Lambdas.

        :param metric_name: -
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
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

    @jsii.member(jsii_name="metricConditionalCheckFailedRequests")
    def metric_conditional_check_failed_requests(
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
        """Metric for the conditional check failed requests.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
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

        return jsii.invoke(self, "metricConditionalCheckFailedRequests", [props])

    @jsii.member(jsii_name="metricConsumedReadCapacityUnits")
    def metric_consumed_read_capacity_units(
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
        """Metric for the consumed read capacity units.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
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

        return jsii.invoke(self, "metricConsumedReadCapacityUnits", [props])

    @jsii.member(jsii_name="metricConsumedWriteCapacityUnits")
    def metric_consumed_write_capacity_units(
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
        """Metric for the consumed write capacity units.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
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

        return jsii.invoke(self, "metricConsumedWriteCapacityUnits", [props])

    @jsii.member(jsii_name="metricSuccessfulRequestLatency")
    def metric_successful_request_latency(
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
        """Metric for the successful request latency.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
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

        return jsii.invoke(self, "metricSuccessfulRequestLatency", [props])

    @jsii.member(jsii_name="metricSystemErrors")
    def metric_system_errors(
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
        """Metric for the system errors.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
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

        return jsii.invoke(self, "metricSystemErrors", [props])

    @jsii.member(jsii_name="metricUserErrors")
    def metric_user_errors(
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
        """Metric for the user errors.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
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

        return jsii.invoke(self, "metricUserErrors", [props])


@jsii.enum(jsii_type="@aws-cdk/aws-dynamodb.ProjectionType")
class ProjectionType(enum.Enum):
    """The set of attributes that are projected into the index.

    see
    :see: https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_Projection.html
    """

    KEYS_ONLY = "KEYS_ONLY"
    """Only the index and primary keys are projected into the index."""
    INCLUDE = "INCLUDE"
    """Only the specified table attributes are projected into the index.

    The list of projected attributes is in ``nonKeyAttributes``.
    """
    ALL = "ALL"
    """All of the table attributes are projected into the index."""


@jsii.data_type(
    jsii_type="@aws-cdk/aws-dynamodb.SecondaryIndexProps",
    jsii_struct_bases=[],
    name_mapping={
        "index_name": "indexName",
        "non_key_attributes": "nonKeyAttributes",
        "projection_type": "projectionType",
    },
)
class SecondaryIndexProps:
    def __init__(
        self,
        *,
        index_name: str,
        non_key_attributes: typing.Optional[typing.List[str]] = None,
        projection_type: typing.Optional["ProjectionType"] = None,
    ) -> None:
        """Properties for a secondary index.

        :param index_name: The name of the secondary index.
        :param non_key_attributes: The non-key attributes that are projected into the secondary index. Default: - No additional attributes
        :param projection_type: The set of attributes that are projected into the secondary index. Default: ALL
        """
        self._values = {
            "index_name": index_name,
        }
        if non_key_attributes is not None:
            self._values["non_key_attributes"] = non_key_attributes
        if projection_type is not None:
            self._values["projection_type"] = projection_type

    @builtins.property
    def index_name(self) -> str:
        """The name of the secondary index."""
        return self._values.get("index_name")

    @builtins.property
    def non_key_attributes(self) -> typing.Optional[typing.List[str]]:
        """The non-key attributes that are projected into the secondary index.

        default
        :default: - No additional attributes
        """
        return self._values.get("non_key_attributes")

    @builtins.property
    def projection_type(self) -> typing.Optional["ProjectionType"]:
        """The set of attributes that are projected into the secondary index.

        default
        :default: ALL
        """
        return self._values.get("projection_type")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecondaryIndexProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-dynamodb.StreamViewType")
class StreamViewType(enum.Enum):
    """When an item in the table is modified, StreamViewType determines what information is written to the stream for this table.

    see
    :see: https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_StreamSpecification.html
    """

    NEW_IMAGE = "NEW_IMAGE"
    """The entire item, as it appears after it was modified, is written to the stream."""
    OLD_IMAGE = "OLD_IMAGE"
    """The entire item, as it appeared before it was modified, is written to the stream."""
    NEW_AND_OLD_IMAGES = "NEW_AND_OLD_IMAGES"
    """Both the new and the old item images of the item are written to the stream."""
    KEYS_ONLY = "KEYS_ONLY"
    """Only the key attributes of the modified item are written to the stream."""


@jsii.implements(ITable)
class Table(
    aws_cdk.core.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-dynamodb.Table",
):
    """Provides a DynamoDB table."""

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: str,
        *,
        table_name: typing.Optional[str] = None,
        partition_key: "Attribute",
        billing_mode: typing.Optional["BillingMode"] = None,
        encryption: typing.Optional["TableEncryption"] = None,
        encryption_key: typing.Optional[aws_cdk.aws_kms.IKey] = None,
        point_in_time_recovery: typing.Optional[bool] = None,
        read_capacity: typing.Optional[jsii.Number] = None,
        removal_policy: typing.Optional[aws_cdk.core.RemovalPolicy] = None,
        replication_regions: typing.Optional[typing.List[str]] = None,
        server_side_encryption: typing.Optional[bool] = None,
        sort_key: typing.Optional["Attribute"] = None,
        stream: typing.Optional["StreamViewType"] = None,
        time_to_live_attribute: typing.Optional[str] = None,
        write_capacity: typing.Optional[jsii.Number] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param table_name: Enforces a particular physical table name. Default: 
        :param partition_key: Partition key attribute definition.
        :param billing_mode: Specify how you are charged for read and write throughput and how you manage capacity. Default: PROVISIONED if ``replicationRegions`` is not specified, PAY_PER_REQUEST otherwise
        :param encryption: Whether server-side encryption with an AWS managed customer master key is enabled. This property cannot be set if ``serverSideEncryption`` is set. Default: - server-side encryption is enabled with an AWS owned customer master key
        :param encryption_key: External KMS key to use for table encryption. This property can only be set if ``encryption`` is set to ``TableEncryption.CUSTOMER_MANAGED``. Default: - If ``encryption`` is set to ``TableEncryption.CUSTOMER_MANAGED`` and this property is undefined, a new KMS key will be created and associated with this table.
        :param point_in_time_recovery: Whether point-in-time recovery is enabled. Default: - point-in-time recovery is disabled
        :param read_capacity: The read capacity for the table. Careful if you add Global Secondary Indexes, as those will share the table's provisioned throughput. Can only be provided if billingMode is Provisioned. Default: 5
        :param removal_policy: The removal policy to apply to the DynamoDB Table. Default: RemovalPolicy.RETAIN
        :param replication_regions: Regions where replica tables will be created. Default: - no replica tables are created
        :param server_side_encryption: Whether server-side encryption with an AWS managed customer master key is enabled. This property cannot be set if ``encryption`` and/or ``encryptionKey`` is set. Default: - server-side encryption is enabled with an AWS owned customer master key
        :param sort_key: Table sort key attribute definition. Default: no sort key
        :param stream: When an item in the table is modified, StreamViewType determines what information is written to the stream for this table. Default: - streams are disabled unless ``replicationRegions`` is specified
        :param time_to_live_attribute: The name of TTL attribute. Default: - TTL is disabled
        :param write_capacity: The write capacity for the table. Careful if you add Global Secondary Indexes, as those will share the table's provisioned throughput. Can only be provided if billingMode is Provisioned. Default: 5
        """
        props = TableProps(
            table_name=table_name,
            partition_key=partition_key,
            billing_mode=billing_mode,
            encryption=encryption,
            encryption_key=encryption_key,
            point_in_time_recovery=point_in_time_recovery,
            read_capacity=read_capacity,
            removal_policy=removal_policy,
            replication_regions=replication_regions,
            server_side_encryption=server_side_encryption,
            sort_key=sort_key,
            stream=stream,
            time_to_live_attribute=time_to_live_attribute,
            write_capacity=write_capacity,
        )

        jsii.create(Table, self, [scope, id, props])

    @jsii.member(jsii_name="fromTableArn")
    @builtins.classmethod
    def from_table_arn(
        cls, scope: aws_cdk.core.Construct, id: str, table_arn: str
    ) -> "ITable":
        """Creates a Table construct that represents an external table via table arn.

        :param scope: The parent creating construct (usually ``this``).
        :param id: The construct's name.
        :param table_arn: The table's ARN.
        """
        return jsii.sinvoke(cls, "fromTableArn", [scope, id, table_arn])

    @jsii.member(jsii_name="fromTableAttributes")
    @builtins.classmethod
    def from_table_attributes(
        cls,
        scope: aws_cdk.core.Construct,
        id: str,
        *,
        encryption_key: typing.Optional[aws_cdk.aws_kms.IKey] = None,
        global_indexes: typing.Optional[typing.List[str]] = None,
        local_indexes: typing.Optional[typing.List[str]] = None,
        table_arn: typing.Optional[str] = None,
        table_name: typing.Optional[str] = None,
        table_stream_arn: typing.Optional[str] = None,
    ) -> "ITable":
        """Creates a Table construct that represents an external table.

        :param scope: The parent creating construct (usually ``this``).
        :param id: The construct's name.
        :param encryption_key: KMS encryption key, if this table uses a customer-managed encryption key. Default: - no key
        :param global_indexes: The name of the global indexes set for this Table. Note that you need to set either this property, or {@link localIndexes}, if you want methods like grantReadData() to grant permissions for indexes as well as the table itself. Default: - no global indexes
        :param local_indexes: The name of the local indexes set for this Table. Note that you need to set either this property, or {@link globalIndexes}, if you want methods like grantReadData() to grant permissions for indexes as well as the table itself. Default: - no local indexes
        :param table_arn: The ARN of the dynamodb table. One of this, or {@link tableName}, is required. Default: - no table arn
        :param table_name: The table name of the dynamodb table. One of this, or {@link tableArn}, is required. Default: - no table name
        :param table_stream_arn: The ARN of the table's stream. Default: - no table stream
        """
        attrs = TableAttributes(
            encryption_key=encryption_key,
            global_indexes=global_indexes,
            local_indexes=local_indexes,
            table_arn=table_arn,
            table_name=table_name,
            table_stream_arn=table_stream_arn,
        )

        return jsii.sinvoke(cls, "fromTableAttributes", [scope, id, attrs])

    @jsii.member(jsii_name="fromTableName")
    @builtins.classmethod
    def from_table_name(
        cls, scope: aws_cdk.core.Construct, id: str, table_name: str
    ) -> "ITable":
        """Creates a Table construct that represents an external table via table name.

        :param scope: The parent creating construct (usually ``this``).
        :param id: The construct's name.
        :param table_name: The table's name.
        """
        return jsii.sinvoke(cls, "fromTableName", [scope, id, table_name])

    @jsii.member(jsii_name="grantListStreams")
    @builtins.classmethod
    def grant_list_streams(
        cls, grantee: aws_cdk.aws_iam.IGrantable
    ) -> aws_cdk.aws_iam.Grant:
        """Permits an IAM Principal to list all DynamoDB Streams.

        :param grantee: The principal (no-op if undefined).

        deprecated
        :deprecated: Use {@link #grantTableListStreams} for more granular permission

        stability
        :stability: deprecated
        """
        return jsii.sinvoke(cls, "grantListStreams", [grantee])

    @jsii.member(jsii_name="addGlobalSecondaryIndex")
    def add_global_secondary_index(
        self,
        *,
        partition_key: "Attribute",
        read_capacity: typing.Optional[jsii.Number] = None,
        sort_key: typing.Optional["Attribute"] = None,
        write_capacity: typing.Optional[jsii.Number] = None,
        index_name: str,
        non_key_attributes: typing.Optional[typing.List[str]] = None,
        projection_type: typing.Optional["ProjectionType"] = None,
    ) -> None:
        """Add a global secondary index of table.

        :param partition_key: The attribute of a partition key for the global secondary index.
        :param read_capacity: The read capacity for the global secondary index. Can only be provided if table billingMode is Provisioned or undefined. Default: 5
        :param sort_key: The attribute of a sort key for the global secondary index. Default: - No sort key
        :param write_capacity: The write capacity for the global secondary index. Can only be provided if table billingMode is Provisioned or undefined. Default: 5
        :param index_name: The name of the secondary index.
        :param non_key_attributes: The non-key attributes that are projected into the secondary index. Default: - No additional attributes
        :param projection_type: The set of attributes that are projected into the secondary index. Default: ALL
        """
        props = GlobalSecondaryIndexProps(
            partition_key=partition_key,
            read_capacity=read_capacity,
            sort_key=sort_key,
            write_capacity=write_capacity,
            index_name=index_name,
            non_key_attributes=non_key_attributes,
            projection_type=projection_type,
        )

        return jsii.invoke(self, "addGlobalSecondaryIndex", [props])

    @jsii.member(jsii_name="addLocalSecondaryIndex")
    def add_local_secondary_index(
        self,
        *,
        sort_key: "Attribute",
        index_name: str,
        non_key_attributes: typing.Optional[typing.List[str]] = None,
        projection_type: typing.Optional["ProjectionType"] = None,
    ) -> None:
        """Add a local secondary index of table.

        :param sort_key: The attribute of a sort key for the local secondary index.
        :param index_name: The name of the secondary index.
        :param non_key_attributes: The non-key attributes that are projected into the secondary index. Default: - No additional attributes
        :param projection_type: The set of attributes that are projected into the secondary index. Default: ALL
        """
        props = LocalSecondaryIndexProps(
            sort_key=sort_key,
            index_name=index_name,
            non_key_attributes=non_key_attributes,
            projection_type=projection_type,
        )

        return jsii.invoke(self, "addLocalSecondaryIndex", [props])

    @jsii.member(jsii_name="autoScaleGlobalSecondaryIndexReadCapacity")
    def auto_scale_global_secondary_index_read_capacity(
        self, index_name: str, *, max_capacity: jsii.Number, min_capacity: jsii.Number
    ) -> "IScalableTableAttribute":
        """Enable read capacity scaling for the given GSI.

        :param index_name: -
        :param max_capacity: Maximum capacity to scale to.
        :param min_capacity: Minimum capacity to scale to.

        return
        :return: An object to configure additional AutoScaling settings for this attribute
        """
        props = EnableScalingProps(max_capacity=max_capacity, min_capacity=min_capacity)

        return jsii.invoke(
            self, "autoScaleGlobalSecondaryIndexReadCapacity", [index_name, props]
        )

    @jsii.member(jsii_name="autoScaleGlobalSecondaryIndexWriteCapacity")
    def auto_scale_global_secondary_index_write_capacity(
        self, index_name: str, *, max_capacity: jsii.Number, min_capacity: jsii.Number
    ) -> "IScalableTableAttribute":
        """Enable write capacity scaling for the given GSI.

        :param index_name: -
        :param max_capacity: Maximum capacity to scale to.
        :param min_capacity: Minimum capacity to scale to.

        return
        :return: An object to configure additional AutoScaling settings for this attribute
        """
        props = EnableScalingProps(max_capacity=max_capacity, min_capacity=min_capacity)

        return jsii.invoke(
            self, "autoScaleGlobalSecondaryIndexWriteCapacity", [index_name, props]
        )

    @jsii.member(jsii_name="autoScaleReadCapacity")
    def auto_scale_read_capacity(
        self, *, max_capacity: jsii.Number, min_capacity: jsii.Number
    ) -> "IScalableTableAttribute":
        """Enable read capacity scaling for this table.

        :param max_capacity: Maximum capacity to scale to.
        :param min_capacity: Minimum capacity to scale to.

        return
        :return: An object to configure additional AutoScaling settings
        """
        props = EnableScalingProps(max_capacity=max_capacity, min_capacity=min_capacity)

        return jsii.invoke(self, "autoScaleReadCapacity", [props])

    @jsii.member(jsii_name="autoScaleWriteCapacity")
    def auto_scale_write_capacity(
        self, *, max_capacity: jsii.Number, min_capacity: jsii.Number
    ) -> "IScalableTableAttribute":
        """Enable write capacity scaling for this table.

        :param max_capacity: Maximum capacity to scale to.
        :param min_capacity: Minimum capacity to scale to.

        return
        :return: An object to configure additional AutoScaling settings for this attribute
        """
        props = EnableScalingProps(max_capacity=max_capacity, min_capacity=min_capacity)

        return jsii.invoke(self, "autoScaleWriteCapacity", [props])

    @jsii.member(jsii_name="grant")
    def grant(
        self, grantee: aws_cdk.aws_iam.IGrantable, *actions: str
    ) -> aws_cdk.aws_iam.Grant:
        """Adds an IAM policy statement associated with this table to an IAM principal's policy.

        If ``encryptionKey`` is present, appropriate grants to the key needs to be added
        separately using the ``table.encryptionKey.grant*`` methods.

        :param grantee: The principal (no-op if undefined).
        :param actions: The set of actions to allow (i.e. "dynamodb:PutItem", "dynamodb:GetItem", ...).
        """
        return jsii.invoke(self, "grant", [grantee, *actions])

    @jsii.member(jsii_name="grantFullAccess")
    def grant_full_access(
        self, grantee: aws_cdk.aws_iam.IGrantable
    ) -> aws_cdk.aws_iam.Grant:
        """Permits all DynamoDB operations ("dynamodb:*") to an IAM principal.

        Appropriate grants will also be added to the customer-managed KMS key
        if one was configured.

        :param grantee: The principal to grant access to.
        """
        return jsii.invoke(self, "grantFullAccess", [grantee])

    @jsii.member(jsii_name="grantReadData")
    def grant_read_data(
        self, grantee: aws_cdk.aws_iam.IGrantable
    ) -> aws_cdk.aws_iam.Grant:
        """Permits an IAM principal all data read operations from this table: BatchGetItem, GetRecords, GetShardIterator, Query, GetItem, Scan.

        Appropriate grants will also be added to the customer-managed KMS key
        if one was configured.

        :param grantee: The principal to grant access to.
        """
        return jsii.invoke(self, "grantReadData", [grantee])

    @jsii.member(jsii_name="grantReadWriteData")
    def grant_read_write_data(
        self, grantee: aws_cdk.aws_iam.IGrantable
    ) -> aws_cdk.aws_iam.Grant:
        """Permits an IAM principal to all data read/write operations to this table.

        BatchGetItem, GetRecords, GetShardIterator, Query, GetItem, Scan,
        BatchWriteItem, PutItem, UpdateItem, DeleteItem

        Appropriate grants will also be added to the customer-managed KMS key
        if one was configured.

        :param grantee: The principal to grant access to.
        """
        return jsii.invoke(self, "grantReadWriteData", [grantee])

    @jsii.member(jsii_name="grantStream")
    def grant_stream(
        self, grantee: aws_cdk.aws_iam.IGrantable, *actions: str
    ) -> aws_cdk.aws_iam.Grant:
        """Adds an IAM policy statement associated with this table's stream to an IAM principal's policy.

        If ``encryptionKey`` is present, appropriate grants to the key needs to be added
        separately using the ``table.encryptionKey.grant*`` methods.

        :param grantee: The principal (no-op if undefined).
        :param actions: The set of actions to allow (i.e. "dynamodb:DescribeStream", "dynamodb:GetRecords", ...).
        """
        return jsii.invoke(self, "grantStream", [grantee, *actions])

    @jsii.member(jsii_name="grantStreamRead")
    def grant_stream_read(
        self, grantee: aws_cdk.aws_iam.IGrantable
    ) -> aws_cdk.aws_iam.Grant:
        """Permits an IAM principal all stream data read operations for this table's stream: DescribeStream, GetRecords, GetShardIterator, ListStreams.

        Appropriate grants will also be added to the customer-managed KMS key
        if one was configured.

        :param grantee: The principal to grant access to.
        """
        return jsii.invoke(self, "grantStreamRead", [grantee])

    @jsii.member(jsii_name="grantTableListStreams")
    def grant_table_list_streams(
        self, grantee: aws_cdk.aws_iam.IGrantable
    ) -> aws_cdk.aws_iam.Grant:
        """Permits an IAM Principal to list streams attached to current dynamodb table.

        :param grantee: The principal (no-op if undefined).
        """
        return jsii.invoke(self, "grantTableListStreams", [grantee])

    @jsii.member(jsii_name="grantWriteData")
    def grant_write_data(
        self, grantee: aws_cdk.aws_iam.IGrantable
    ) -> aws_cdk.aws_iam.Grant:
        """Permits an IAM principal all data write operations to this table: BatchWriteItem, PutItem, UpdateItem, DeleteItem.

        Appropriate grants will also be added to the customer-managed KMS key
        if one was configured.

        :param grantee: The principal to grant access to.
        """
        return jsii.invoke(self, "grantWriteData", [grantee])

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
        """Return the given named metric for this Table.

        :param metric_name: -
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
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

    @jsii.member(jsii_name="metricConditionalCheckFailedRequests")
    def metric_conditional_check_failed_requests(
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
        """Metric for the conditional check failed requests this table.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        default
        :default: sum over a minute
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

        return jsii.invoke(self, "metricConditionalCheckFailedRequests", [props])

    @jsii.member(jsii_name="metricConsumedReadCapacityUnits")
    def metric_consumed_read_capacity_units(
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
        """Metric for the consumed read capacity units this table.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        default
        :default: sum over a minute
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

        return jsii.invoke(self, "metricConsumedReadCapacityUnits", [props])

    @jsii.member(jsii_name="metricConsumedWriteCapacityUnits")
    def metric_consumed_write_capacity_units(
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
        """Metric for the consumed write capacity units this table.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        default
        :default: sum over a minute
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

        return jsii.invoke(self, "metricConsumedWriteCapacityUnits", [props])

    @jsii.member(jsii_name="metricSuccessfulRequestLatency")
    def metric_successful_request_latency(
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
        """Metric for the successful request latency this table.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        default
        :default: avg over a minute
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

        return jsii.invoke(self, "metricSuccessfulRequestLatency", [props])

    @jsii.member(jsii_name="metricSystemErrors")
    def metric_system_errors(
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
        """Metric for the system errors this table.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        default
        :default: sum over a minute
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

        return jsii.invoke(self, "metricSystemErrors", [props])

    @jsii.member(jsii_name="metricUserErrors")
    def metric_user_errors(
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
        """Metric for the user errors this table.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        default
        :default: sum over a minute
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

        return jsii.invoke(self, "metricUserErrors", [props])

    @jsii.member(jsii_name="validate")
    def _validate(self) -> typing.List[str]:
        """Validate the table construct.

        return
        :return: an array of validation error message
        """
        return jsii.invoke(self, "validate", [])

    @builtins.property
    @jsii.member(jsii_name="hasIndex")
    def _has_index(self) -> bool:
        """Whether this table has indexes."""
        return jsii.get(self, "hasIndex")

    @builtins.property
    @jsii.member(jsii_name="regionalArns")
    def _regional_arns(self) -> typing.List[str]:
        return jsii.get(self, "regionalArns")

    @builtins.property
    @jsii.member(jsii_name="tableArn")
    def table_arn(self) -> str:
        """Arn of the dynamodb table.

        attribute:
        :attribute:: true
        """
        return jsii.get(self, "tableArn")

    @builtins.property
    @jsii.member(jsii_name="tableName")
    def table_name(self) -> str:
        """Table name of the dynamodb table.

        attribute:
        :attribute:: true
        """
        return jsii.get(self, "tableName")

    @builtins.property
    @jsii.member(jsii_name="encryptionKey")
    def encryption_key(self) -> typing.Optional[aws_cdk.aws_kms.IKey]:
        """KMS encryption key, if this table uses a customer-managed encryption key."""
        return jsii.get(self, "encryptionKey")

    @builtins.property
    @jsii.member(jsii_name="tableStreamArn")
    def table_stream_arn(self) -> typing.Optional[str]:
        """ARN of the table's stream, if there is one.

        attribute:
        :attribute:: true
        """
        return jsii.get(self, "tableStreamArn")


@jsii.data_type(
    jsii_type="@aws-cdk/aws-dynamodb.TableAttributes",
    jsii_struct_bases=[],
    name_mapping={
        "encryption_key": "encryptionKey",
        "global_indexes": "globalIndexes",
        "local_indexes": "localIndexes",
        "table_arn": "tableArn",
        "table_name": "tableName",
        "table_stream_arn": "tableStreamArn",
    },
)
class TableAttributes:
    def __init__(
        self,
        *,
        encryption_key: typing.Optional[aws_cdk.aws_kms.IKey] = None,
        global_indexes: typing.Optional[typing.List[str]] = None,
        local_indexes: typing.Optional[typing.List[str]] = None,
        table_arn: typing.Optional[str] = None,
        table_name: typing.Optional[str] = None,
        table_stream_arn: typing.Optional[str] = None,
    ) -> None:
        """Reference to a dynamodb table.

        :param encryption_key: KMS encryption key, if this table uses a customer-managed encryption key. Default: - no key
        :param global_indexes: The name of the global indexes set for this Table. Note that you need to set either this property, or {@link localIndexes}, if you want methods like grantReadData() to grant permissions for indexes as well as the table itself. Default: - no global indexes
        :param local_indexes: The name of the local indexes set for this Table. Note that you need to set either this property, or {@link globalIndexes}, if you want methods like grantReadData() to grant permissions for indexes as well as the table itself. Default: - no local indexes
        :param table_arn: The ARN of the dynamodb table. One of this, or {@link tableName}, is required. Default: - no table arn
        :param table_name: The table name of the dynamodb table. One of this, or {@link tableArn}, is required. Default: - no table name
        :param table_stream_arn: The ARN of the table's stream. Default: - no table stream
        """
        self._values = {}
        if encryption_key is not None:
            self._values["encryption_key"] = encryption_key
        if global_indexes is not None:
            self._values["global_indexes"] = global_indexes
        if local_indexes is not None:
            self._values["local_indexes"] = local_indexes
        if table_arn is not None:
            self._values["table_arn"] = table_arn
        if table_name is not None:
            self._values["table_name"] = table_name
        if table_stream_arn is not None:
            self._values["table_stream_arn"] = table_stream_arn

    @builtins.property
    def encryption_key(self) -> typing.Optional[aws_cdk.aws_kms.IKey]:
        """KMS encryption key, if this table uses a customer-managed encryption key.

        default
        :default: - no key
        """
        return self._values.get("encryption_key")

    @builtins.property
    def global_indexes(self) -> typing.Optional[typing.List[str]]:
        """The name of the global indexes set for this Table.

        Note that you need to set either this property,
        or {@link localIndexes},
        if you want methods like grantReadData()
        to grant permissions for indexes as well as the table itself.

        default
        :default: - no global indexes
        """
        return self._values.get("global_indexes")

    @builtins.property
    def local_indexes(self) -> typing.Optional[typing.List[str]]:
        """The name of the local indexes set for this Table.

        Note that you need to set either this property,
        or {@link globalIndexes},
        if you want methods like grantReadData()
        to grant permissions for indexes as well as the table itself.

        default
        :default: - no local indexes
        """
        return self._values.get("local_indexes")

    @builtins.property
    def table_arn(self) -> typing.Optional[str]:
        """The ARN of the dynamodb table.

        One of this, or {@link tableName}, is required.

        default
        :default: - no table arn
        """
        return self._values.get("table_arn")

    @builtins.property
    def table_name(self) -> typing.Optional[str]:
        """The table name of the dynamodb table.

        One of this, or {@link tableArn}, is required.

        default
        :default: - no table name
        """
        return self._values.get("table_name")

    @builtins.property
    def table_stream_arn(self) -> typing.Optional[str]:
        """The ARN of the table's stream.

        default
        :default: - no table stream
        """
        return self._values.get("table_stream_arn")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TableAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-dynamodb.TableEncryption")
class TableEncryption(enum.Enum):
    """What kind of server-side encryption to apply to this table."""

    DEFAULT = "DEFAULT"
    """Server-side KMS encryption with a master key owned by AWS."""
    CUSTOMER_MANAGED = "CUSTOMER_MANAGED"
    """Server-side KMS encryption with a customer master key managed by customer.

    If ``encryptionKey`` is specified, this key will be used, otherwise, one will be defined.
    """
    AWS_MANAGED = "AWS_MANAGED"
    """Server-side KMS encryption with a master key managed by AWS."""


@jsii.data_type(
    jsii_type="@aws-cdk/aws-dynamodb.TableOptions",
    jsii_struct_bases=[],
    name_mapping={
        "partition_key": "partitionKey",
        "billing_mode": "billingMode",
        "encryption": "encryption",
        "encryption_key": "encryptionKey",
        "point_in_time_recovery": "pointInTimeRecovery",
        "read_capacity": "readCapacity",
        "removal_policy": "removalPolicy",
        "replication_regions": "replicationRegions",
        "server_side_encryption": "serverSideEncryption",
        "sort_key": "sortKey",
        "stream": "stream",
        "time_to_live_attribute": "timeToLiveAttribute",
        "write_capacity": "writeCapacity",
    },
)
class TableOptions:
    def __init__(
        self,
        *,
        partition_key: "Attribute",
        billing_mode: typing.Optional["BillingMode"] = None,
        encryption: typing.Optional["TableEncryption"] = None,
        encryption_key: typing.Optional[aws_cdk.aws_kms.IKey] = None,
        point_in_time_recovery: typing.Optional[bool] = None,
        read_capacity: typing.Optional[jsii.Number] = None,
        removal_policy: typing.Optional[aws_cdk.core.RemovalPolicy] = None,
        replication_regions: typing.Optional[typing.List[str]] = None,
        server_side_encryption: typing.Optional[bool] = None,
        sort_key: typing.Optional["Attribute"] = None,
        stream: typing.Optional["StreamViewType"] = None,
        time_to_live_attribute: typing.Optional[str] = None,
        write_capacity: typing.Optional[jsii.Number] = None,
    ) -> None:
        """Properties of a DynamoDB Table.

        Use {@link TableProps} for all table properties

        :param partition_key: Partition key attribute definition.
        :param billing_mode: Specify how you are charged for read and write throughput and how you manage capacity. Default: PROVISIONED if ``replicationRegions`` is not specified, PAY_PER_REQUEST otherwise
        :param encryption: Whether server-side encryption with an AWS managed customer master key is enabled. This property cannot be set if ``serverSideEncryption`` is set. Default: - server-side encryption is enabled with an AWS owned customer master key
        :param encryption_key: External KMS key to use for table encryption. This property can only be set if ``encryption`` is set to ``TableEncryption.CUSTOMER_MANAGED``. Default: - If ``encryption`` is set to ``TableEncryption.CUSTOMER_MANAGED`` and this property is undefined, a new KMS key will be created and associated with this table.
        :param point_in_time_recovery: Whether point-in-time recovery is enabled. Default: - point-in-time recovery is disabled
        :param read_capacity: The read capacity for the table. Careful if you add Global Secondary Indexes, as those will share the table's provisioned throughput. Can only be provided if billingMode is Provisioned. Default: 5
        :param removal_policy: The removal policy to apply to the DynamoDB Table. Default: RemovalPolicy.RETAIN
        :param replication_regions: Regions where replica tables will be created. Default: - no replica tables are created
        :param server_side_encryption: Whether server-side encryption with an AWS managed customer master key is enabled. This property cannot be set if ``encryption`` and/or ``encryptionKey`` is set. Default: - server-side encryption is enabled with an AWS owned customer master key
        :param sort_key: Table sort key attribute definition. Default: no sort key
        :param stream: When an item in the table is modified, StreamViewType determines what information is written to the stream for this table. Default: - streams are disabled unless ``replicationRegions`` is specified
        :param time_to_live_attribute: The name of TTL attribute. Default: - TTL is disabled
        :param write_capacity: The write capacity for the table. Careful if you add Global Secondary Indexes, as those will share the table's provisioned throughput. Can only be provided if billingMode is Provisioned. Default: 5
        """
        if isinstance(partition_key, dict):
            partition_key = Attribute(**partition_key)
        if isinstance(sort_key, dict):
            sort_key = Attribute(**sort_key)
        self._values = {
            "partition_key": partition_key,
        }
        if billing_mode is not None:
            self._values["billing_mode"] = billing_mode
        if encryption is not None:
            self._values["encryption"] = encryption
        if encryption_key is not None:
            self._values["encryption_key"] = encryption_key
        if point_in_time_recovery is not None:
            self._values["point_in_time_recovery"] = point_in_time_recovery
        if read_capacity is not None:
            self._values["read_capacity"] = read_capacity
        if removal_policy is not None:
            self._values["removal_policy"] = removal_policy
        if replication_regions is not None:
            self._values["replication_regions"] = replication_regions
        if server_side_encryption is not None:
            self._values["server_side_encryption"] = server_side_encryption
        if sort_key is not None:
            self._values["sort_key"] = sort_key
        if stream is not None:
            self._values["stream"] = stream
        if time_to_live_attribute is not None:
            self._values["time_to_live_attribute"] = time_to_live_attribute
        if write_capacity is not None:
            self._values["write_capacity"] = write_capacity

    @builtins.property
    def partition_key(self) -> "Attribute":
        """Partition key attribute definition."""
        return self._values.get("partition_key")

    @builtins.property
    def billing_mode(self) -> typing.Optional["BillingMode"]:
        """Specify how you are charged for read and write throughput and how you manage capacity.

        default
        :default: PROVISIONED if ``replicationRegions`` is not specified, PAY_PER_REQUEST otherwise
        """
        return self._values.get("billing_mode")

    @builtins.property
    def encryption(self) -> typing.Optional["TableEncryption"]:
        """Whether server-side encryption with an AWS managed customer master key is enabled.

        This property cannot be set if ``serverSideEncryption`` is set.

        default
        :default: - server-side encryption is enabled with an AWS owned customer master key
        """
        return self._values.get("encryption")

    @builtins.property
    def encryption_key(self) -> typing.Optional[aws_cdk.aws_kms.IKey]:
        """External KMS key to use for table encryption.

        This property can only be set if ``encryption`` is set to ``TableEncryption.CUSTOMER_MANAGED``.

        default
        :default:

        - If ``encryption`` is set to ``TableEncryption.CUSTOMER_MANAGED`` and this
          property is undefined, a new KMS key will be created and associated with this table.
        """
        return self._values.get("encryption_key")

    @builtins.property
    def point_in_time_recovery(self) -> typing.Optional[bool]:
        """Whether point-in-time recovery is enabled.

        default
        :default: - point-in-time recovery is disabled
        """
        return self._values.get("point_in_time_recovery")

    @builtins.property
    def read_capacity(self) -> typing.Optional[jsii.Number]:
        """The read capacity for the table.

        Careful if you add Global Secondary Indexes, as
        those will share the table's provisioned throughput.

        Can only be provided if billingMode is Provisioned.

        default
        :default: 5
        """
        return self._values.get("read_capacity")

    @builtins.property
    def removal_policy(self) -> typing.Optional[aws_cdk.core.RemovalPolicy]:
        """The removal policy to apply to the DynamoDB Table.

        default
        :default: RemovalPolicy.RETAIN
        """
        return self._values.get("removal_policy")

    @builtins.property
    def replication_regions(self) -> typing.Optional[typing.List[str]]:
        """Regions where replica tables will be created.

        default
        :default: - no replica tables are created

        stability
        :stability: experimental
        """
        return self._values.get("replication_regions")

    @builtins.property
    def server_side_encryption(self) -> typing.Optional[bool]:
        """Whether server-side encryption with an AWS managed customer master key is enabled.

        This property cannot be set if ``encryption`` and/or ``encryptionKey`` is set.

        default
        :default: - server-side encryption is enabled with an AWS owned customer master key

        deprecated
        :deprecated:

        This property is deprecated. In order to obtain the same behavior as
        enabling this, set the ``encryption`` property to ``TableEncryption.AWS_MANAGED`` instead.

        stability
        :stability: deprecated
        """
        return self._values.get("server_side_encryption")

    @builtins.property
    def sort_key(self) -> typing.Optional["Attribute"]:
        """Table sort key attribute definition.

        default
        :default: no sort key
        """
        return self._values.get("sort_key")

    @builtins.property
    def stream(self) -> typing.Optional["StreamViewType"]:
        """When an item in the table is modified, StreamViewType determines what information is written to the stream for this table.

        default
        :default: - streams are disabled unless ``replicationRegions`` is specified
        """
        return self._values.get("stream")

    @builtins.property
    def time_to_live_attribute(self) -> typing.Optional[str]:
        """The name of TTL attribute.

        default
        :default: - TTL is disabled
        """
        return self._values.get("time_to_live_attribute")

    @builtins.property
    def write_capacity(self) -> typing.Optional[jsii.Number]:
        """The write capacity for the table.

        Careful if you add Global Secondary Indexes, as
        those will share the table's provisioned throughput.

        Can only be provided if billingMode is Provisioned.

        default
        :default: 5
        """
        return self._values.get("write_capacity")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TableOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-dynamodb.TableProps",
    jsii_struct_bases=[TableOptions],
    name_mapping={
        "partition_key": "partitionKey",
        "billing_mode": "billingMode",
        "encryption": "encryption",
        "encryption_key": "encryptionKey",
        "point_in_time_recovery": "pointInTimeRecovery",
        "read_capacity": "readCapacity",
        "removal_policy": "removalPolicy",
        "replication_regions": "replicationRegions",
        "server_side_encryption": "serverSideEncryption",
        "sort_key": "sortKey",
        "stream": "stream",
        "time_to_live_attribute": "timeToLiveAttribute",
        "write_capacity": "writeCapacity",
        "table_name": "tableName",
    },
)
class TableProps(TableOptions):
    def __init__(
        self,
        *,
        partition_key: "Attribute",
        billing_mode: typing.Optional["BillingMode"] = None,
        encryption: typing.Optional["TableEncryption"] = None,
        encryption_key: typing.Optional[aws_cdk.aws_kms.IKey] = None,
        point_in_time_recovery: typing.Optional[bool] = None,
        read_capacity: typing.Optional[jsii.Number] = None,
        removal_policy: typing.Optional[aws_cdk.core.RemovalPolicy] = None,
        replication_regions: typing.Optional[typing.List[str]] = None,
        server_side_encryption: typing.Optional[bool] = None,
        sort_key: typing.Optional["Attribute"] = None,
        stream: typing.Optional["StreamViewType"] = None,
        time_to_live_attribute: typing.Optional[str] = None,
        write_capacity: typing.Optional[jsii.Number] = None,
        table_name: typing.Optional[str] = None,
    ) -> None:
        """Properties for a DynamoDB Table.

        :param partition_key: Partition key attribute definition.
        :param billing_mode: Specify how you are charged for read and write throughput and how you manage capacity. Default: PROVISIONED if ``replicationRegions`` is not specified, PAY_PER_REQUEST otherwise
        :param encryption: Whether server-side encryption with an AWS managed customer master key is enabled. This property cannot be set if ``serverSideEncryption`` is set. Default: - server-side encryption is enabled with an AWS owned customer master key
        :param encryption_key: External KMS key to use for table encryption. This property can only be set if ``encryption`` is set to ``TableEncryption.CUSTOMER_MANAGED``. Default: - If ``encryption`` is set to ``TableEncryption.CUSTOMER_MANAGED`` and this property is undefined, a new KMS key will be created and associated with this table.
        :param point_in_time_recovery: Whether point-in-time recovery is enabled. Default: - point-in-time recovery is disabled
        :param read_capacity: The read capacity for the table. Careful if you add Global Secondary Indexes, as those will share the table's provisioned throughput. Can only be provided if billingMode is Provisioned. Default: 5
        :param removal_policy: The removal policy to apply to the DynamoDB Table. Default: RemovalPolicy.RETAIN
        :param replication_regions: Regions where replica tables will be created. Default: - no replica tables are created
        :param server_side_encryption: Whether server-side encryption with an AWS managed customer master key is enabled. This property cannot be set if ``encryption`` and/or ``encryptionKey`` is set. Default: - server-side encryption is enabled with an AWS owned customer master key
        :param sort_key: Table sort key attribute definition. Default: no sort key
        :param stream: When an item in the table is modified, StreamViewType determines what information is written to the stream for this table. Default: - streams are disabled unless ``replicationRegions`` is specified
        :param time_to_live_attribute: The name of TTL attribute. Default: - TTL is disabled
        :param write_capacity: The write capacity for the table. Careful if you add Global Secondary Indexes, as those will share the table's provisioned throughput. Can only be provided if billingMode is Provisioned. Default: 5
        :param table_name: Enforces a particular physical table name. Default: 
        """
        if isinstance(partition_key, dict):
            partition_key = Attribute(**partition_key)
        if isinstance(sort_key, dict):
            sort_key = Attribute(**sort_key)
        self._values = {
            "partition_key": partition_key,
        }
        if billing_mode is not None:
            self._values["billing_mode"] = billing_mode
        if encryption is not None:
            self._values["encryption"] = encryption
        if encryption_key is not None:
            self._values["encryption_key"] = encryption_key
        if point_in_time_recovery is not None:
            self._values["point_in_time_recovery"] = point_in_time_recovery
        if read_capacity is not None:
            self._values["read_capacity"] = read_capacity
        if removal_policy is not None:
            self._values["removal_policy"] = removal_policy
        if replication_regions is not None:
            self._values["replication_regions"] = replication_regions
        if server_side_encryption is not None:
            self._values["server_side_encryption"] = server_side_encryption
        if sort_key is not None:
            self._values["sort_key"] = sort_key
        if stream is not None:
            self._values["stream"] = stream
        if time_to_live_attribute is not None:
            self._values["time_to_live_attribute"] = time_to_live_attribute
        if write_capacity is not None:
            self._values["write_capacity"] = write_capacity
        if table_name is not None:
            self._values["table_name"] = table_name

    @builtins.property
    def partition_key(self) -> "Attribute":
        """Partition key attribute definition."""
        return self._values.get("partition_key")

    @builtins.property
    def billing_mode(self) -> typing.Optional["BillingMode"]:
        """Specify how you are charged for read and write throughput and how you manage capacity.

        default
        :default: PROVISIONED if ``replicationRegions`` is not specified, PAY_PER_REQUEST otherwise
        """
        return self._values.get("billing_mode")

    @builtins.property
    def encryption(self) -> typing.Optional["TableEncryption"]:
        """Whether server-side encryption with an AWS managed customer master key is enabled.

        This property cannot be set if ``serverSideEncryption`` is set.

        default
        :default: - server-side encryption is enabled with an AWS owned customer master key
        """
        return self._values.get("encryption")

    @builtins.property
    def encryption_key(self) -> typing.Optional[aws_cdk.aws_kms.IKey]:
        """External KMS key to use for table encryption.

        This property can only be set if ``encryption`` is set to ``TableEncryption.CUSTOMER_MANAGED``.

        default
        :default:

        - If ``encryption`` is set to ``TableEncryption.CUSTOMER_MANAGED`` and this
          property is undefined, a new KMS key will be created and associated with this table.
        """
        return self._values.get("encryption_key")

    @builtins.property
    def point_in_time_recovery(self) -> typing.Optional[bool]:
        """Whether point-in-time recovery is enabled.

        default
        :default: - point-in-time recovery is disabled
        """
        return self._values.get("point_in_time_recovery")

    @builtins.property
    def read_capacity(self) -> typing.Optional[jsii.Number]:
        """The read capacity for the table.

        Careful if you add Global Secondary Indexes, as
        those will share the table's provisioned throughput.

        Can only be provided if billingMode is Provisioned.

        default
        :default: 5
        """
        return self._values.get("read_capacity")

    @builtins.property
    def removal_policy(self) -> typing.Optional[aws_cdk.core.RemovalPolicy]:
        """The removal policy to apply to the DynamoDB Table.

        default
        :default: RemovalPolicy.RETAIN
        """
        return self._values.get("removal_policy")

    @builtins.property
    def replication_regions(self) -> typing.Optional[typing.List[str]]:
        """Regions where replica tables will be created.

        default
        :default: - no replica tables are created

        stability
        :stability: experimental
        """
        return self._values.get("replication_regions")

    @builtins.property
    def server_side_encryption(self) -> typing.Optional[bool]:
        """Whether server-side encryption with an AWS managed customer master key is enabled.

        This property cannot be set if ``encryption`` and/or ``encryptionKey`` is set.

        default
        :default: - server-side encryption is enabled with an AWS owned customer master key

        deprecated
        :deprecated:

        This property is deprecated. In order to obtain the same behavior as
        enabling this, set the ``encryption`` property to ``TableEncryption.AWS_MANAGED`` instead.

        stability
        :stability: deprecated
        """
        return self._values.get("server_side_encryption")

    @builtins.property
    def sort_key(self) -> typing.Optional["Attribute"]:
        """Table sort key attribute definition.

        default
        :default: no sort key
        """
        return self._values.get("sort_key")

    @builtins.property
    def stream(self) -> typing.Optional["StreamViewType"]:
        """When an item in the table is modified, StreamViewType determines what information is written to the stream for this table.

        default
        :default: - streams are disabled unless ``replicationRegions`` is specified
        """
        return self._values.get("stream")

    @builtins.property
    def time_to_live_attribute(self) -> typing.Optional[str]:
        """The name of TTL attribute.

        default
        :default: - TTL is disabled
        """
        return self._values.get("time_to_live_attribute")

    @builtins.property
    def write_capacity(self) -> typing.Optional[jsii.Number]:
        """The write capacity for the table.

        Careful if you add Global Secondary Indexes, as
        those will share the table's provisioned throughput.

        Can only be provided if billingMode is Provisioned.

        default
        :default: 5
        """
        return self._values.get("write_capacity")

    @builtins.property
    def table_name(self) -> typing.Optional[str]:
        """Enforces a particular physical table name.

        default
        :default: 
        """
        return self._values.get("table_name")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TableProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-dynamodb.UtilizationScalingProps",
    jsii_struct_bases=[aws_cdk.aws_applicationautoscaling.BaseTargetTrackingProps],
    name_mapping={
        "disable_scale_in": "disableScaleIn",
        "policy_name": "policyName",
        "scale_in_cooldown": "scaleInCooldown",
        "scale_out_cooldown": "scaleOutCooldown",
        "target_utilization_percent": "targetUtilizationPercent",
    },
)
class UtilizationScalingProps(
    aws_cdk.aws_applicationautoscaling.BaseTargetTrackingProps
):
    def __init__(
        self,
        *,
        disable_scale_in: typing.Optional[bool] = None,
        policy_name: typing.Optional[str] = None,
        scale_in_cooldown: typing.Optional[aws_cdk.core.Duration] = None,
        scale_out_cooldown: typing.Optional[aws_cdk.core.Duration] = None,
        target_utilization_percent: jsii.Number,
    ) -> None:
        """Properties for enabling DynamoDB utilization tracking.

        :param disable_scale_in: Indicates whether scale in by the target tracking policy is disabled. If the value is true, scale in is disabled and the target tracking policy won't remove capacity from the scalable resource. Otherwise, scale in is enabled and the target tracking policy can remove capacity from the scalable resource. Default: false
        :param policy_name: A name for the scaling policy. Default: - Automatically generated name.
        :param scale_in_cooldown: Period after a scale in activity completes before another scale in activity can start. Default: Duration.seconds(300) for the following scalable targets: ECS services, Spot Fleet requests, EMR clusters, AppStream 2.0 fleets, Aurora DB clusters, Amazon SageMaker endpoint variants, Custom resources. For all other scalable targets, the default value is Duration.seconds(0): DynamoDB tables, DynamoDB global secondary indexes, Amazon Comprehend document classification endpoints, Lambda provisioned concurrency
        :param scale_out_cooldown: Period after a scale out activity completes before another scale out activity can start. Default: Duration.seconds(300) for the following scalable targets: ECS services, Spot Fleet requests, EMR clusters, AppStream 2.0 fleets, Aurora DB clusters, Amazon SageMaker endpoint variants, Custom resources. For all other scalable targets, the default value is Duration.seconds(0): DynamoDB tables, DynamoDB global secondary indexes, Amazon Comprehend document classification endpoints, Lambda provisioned concurrency
        :param target_utilization_percent: Target utilization percentage for the attribute.
        """
        self._values = {
            "target_utilization_percent": target_utilization_percent,
        }
        if disable_scale_in is not None:
            self._values["disable_scale_in"] = disable_scale_in
        if policy_name is not None:
            self._values["policy_name"] = policy_name
        if scale_in_cooldown is not None:
            self._values["scale_in_cooldown"] = scale_in_cooldown
        if scale_out_cooldown is not None:
            self._values["scale_out_cooldown"] = scale_out_cooldown

    @builtins.property
    def disable_scale_in(self) -> typing.Optional[bool]:
        """Indicates whether scale in by the target tracking policy is disabled.

        If the value is true, scale in is disabled and the target tracking policy
        won't remove capacity from the scalable resource. Otherwise, scale in is
        enabled and the target tracking policy can remove capacity from the
        scalable resource.

        default
        :default: false
        """
        return self._values.get("disable_scale_in")

    @builtins.property
    def policy_name(self) -> typing.Optional[str]:
        """A name for the scaling policy.

        default
        :default: - Automatically generated name.
        """
        return self._values.get("policy_name")

    @builtins.property
    def scale_in_cooldown(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Period after a scale in activity completes before another scale in activity can start.

        default
        :default:

        Duration.seconds(300) for the following scalable targets: ECS services,
        Spot Fleet requests, EMR clusters, AppStream 2.0 fleets, Aurora DB clusters,
        Amazon SageMaker endpoint variants, Custom resources. For all other scalable
        targets, the default value is Duration.seconds(0): DynamoDB tables, DynamoDB
        global secondary indexes, Amazon Comprehend document classification endpoints,
        Lambda provisioned concurrency
        """
        return self._values.get("scale_in_cooldown")

    @builtins.property
    def scale_out_cooldown(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Period after a scale out activity completes before another scale out activity can start.

        default
        :default:

        Duration.seconds(300) for the following scalable targets: ECS services,
        Spot Fleet requests, EMR clusters, AppStream 2.0 fleets, Aurora DB clusters,
        Amazon SageMaker endpoint variants, Custom resources. For all other scalable
        targets, the default value is Duration.seconds(0): DynamoDB tables, DynamoDB
        global secondary indexes, Amazon Comprehend document classification endpoints,
        Lambda provisioned concurrency
        """
        return self._values.get("scale_out_cooldown")

    @builtins.property
    def target_utilization_percent(self) -> jsii.Number:
        """Target utilization percentage for the attribute."""
        return self._values.get("target_utilization_percent")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UtilizationScalingProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-dynamodb.GlobalSecondaryIndexProps",
    jsii_struct_bases=[SecondaryIndexProps],
    name_mapping={
        "index_name": "indexName",
        "non_key_attributes": "nonKeyAttributes",
        "projection_type": "projectionType",
        "partition_key": "partitionKey",
        "read_capacity": "readCapacity",
        "sort_key": "sortKey",
        "write_capacity": "writeCapacity",
    },
)
class GlobalSecondaryIndexProps(SecondaryIndexProps):
    def __init__(
        self,
        *,
        index_name: str,
        non_key_attributes: typing.Optional[typing.List[str]] = None,
        projection_type: typing.Optional["ProjectionType"] = None,
        partition_key: "Attribute",
        read_capacity: typing.Optional[jsii.Number] = None,
        sort_key: typing.Optional["Attribute"] = None,
        write_capacity: typing.Optional[jsii.Number] = None,
    ) -> None:
        """Properties for a global secondary index.

        :param index_name: The name of the secondary index.
        :param non_key_attributes: The non-key attributes that are projected into the secondary index. Default: - No additional attributes
        :param projection_type: The set of attributes that are projected into the secondary index. Default: ALL
        :param partition_key: The attribute of a partition key for the global secondary index.
        :param read_capacity: The read capacity for the global secondary index. Can only be provided if table billingMode is Provisioned or undefined. Default: 5
        :param sort_key: The attribute of a sort key for the global secondary index. Default: - No sort key
        :param write_capacity: The write capacity for the global secondary index. Can only be provided if table billingMode is Provisioned or undefined. Default: 5
        """
        if isinstance(partition_key, dict):
            partition_key = Attribute(**partition_key)
        if isinstance(sort_key, dict):
            sort_key = Attribute(**sort_key)
        self._values = {
            "index_name": index_name,
            "partition_key": partition_key,
        }
        if non_key_attributes is not None:
            self._values["non_key_attributes"] = non_key_attributes
        if projection_type is not None:
            self._values["projection_type"] = projection_type
        if read_capacity is not None:
            self._values["read_capacity"] = read_capacity
        if sort_key is not None:
            self._values["sort_key"] = sort_key
        if write_capacity is not None:
            self._values["write_capacity"] = write_capacity

    @builtins.property
    def index_name(self) -> str:
        """The name of the secondary index."""
        return self._values.get("index_name")

    @builtins.property
    def non_key_attributes(self) -> typing.Optional[typing.List[str]]:
        """The non-key attributes that are projected into the secondary index.

        default
        :default: - No additional attributes
        """
        return self._values.get("non_key_attributes")

    @builtins.property
    def projection_type(self) -> typing.Optional["ProjectionType"]:
        """The set of attributes that are projected into the secondary index.

        default
        :default: ALL
        """
        return self._values.get("projection_type")

    @builtins.property
    def partition_key(self) -> "Attribute":
        """The attribute of a partition key for the global secondary index."""
        return self._values.get("partition_key")

    @builtins.property
    def read_capacity(self) -> typing.Optional[jsii.Number]:
        """The read capacity for the global secondary index.

        Can only be provided if table billingMode is Provisioned or undefined.

        default
        :default: 5
        """
        return self._values.get("read_capacity")

    @builtins.property
    def sort_key(self) -> typing.Optional["Attribute"]:
        """The attribute of a sort key for the global secondary index.

        default
        :default: - No sort key
        """
        return self._values.get("sort_key")

    @builtins.property
    def write_capacity(self) -> typing.Optional[jsii.Number]:
        """The write capacity for the global secondary index.

        Can only be provided if table billingMode is Provisioned or undefined.

        default
        :default: 5
        """
        return self._values.get("write_capacity")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GlobalSecondaryIndexProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-dynamodb.LocalSecondaryIndexProps",
    jsii_struct_bases=[SecondaryIndexProps],
    name_mapping={
        "index_name": "indexName",
        "non_key_attributes": "nonKeyAttributes",
        "projection_type": "projectionType",
        "sort_key": "sortKey",
    },
)
class LocalSecondaryIndexProps(SecondaryIndexProps):
    def __init__(
        self,
        *,
        index_name: str,
        non_key_attributes: typing.Optional[typing.List[str]] = None,
        projection_type: typing.Optional["ProjectionType"] = None,
        sort_key: "Attribute",
    ) -> None:
        """Properties for a local secondary index.

        :param index_name: The name of the secondary index.
        :param non_key_attributes: The non-key attributes that are projected into the secondary index. Default: - No additional attributes
        :param projection_type: The set of attributes that are projected into the secondary index. Default: ALL
        :param sort_key: The attribute of a sort key for the local secondary index.
        """
        if isinstance(sort_key, dict):
            sort_key = Attribute(**sort_key)
        self._values = {
            "index_name": index_name,
            "sort_key": sort_key,
        }
        if non_key_attributes is not None:
            self._values["non_key_attributes"] = non_key_attributes
        if projection_type is not None:
            self._values["projection_type"] = projection_type

    @builtins.property
    def index_name(self) -> str:
        """The name of the secondary index."""
        return self._values.get("index_name")

    @builtins.property
    def non_key_attributes(self) -> typing.Optional[typing.List[str]]:
        """The non-key attributes that are projected into the secondary index.

        default
        :default: - No additional attributes
        """
        return self._values.get("non_key_attributes")

    @builtins.property
    def projection_type(self) -> typing.Optional["ProjectionType"]:
        """The set of attributes that are projected into the secondary index.

        default
        :default: ALL
        """
        return self._values.get("projection_type")

    @builtins.property
    def sort_key(self) -> "Attribute":
        """The attribute of a sort key for the local secondary index."""
        return self._values.get("sort_key")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LocalSecondaryIndexProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "Attribute",
    "AttributeType",
    "BillingMode",
    "CfnTable",
    "CfnTableProps",
    "EnableScalingProps",
    "GlobalSecondaryIndexProps",
    "IScalableTableAttribute",
    "ITable",
    "LocalSecondaryIndexProps",
    "ProjectionType",
    "SecondaryIndexProps",
    "StreamViewType",
    "Table",
    "TableAttributes",
    "TableEncryption",
    "TableOptions",
    "TableProps",
    "UtilizationScalingProps",
]

publication.publish()
