# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from . import _utilities, _tables

__all__ = [
    'GetGroupResult',
    'AwaitableGetGroupResult',
    'get_group',
]

@pulumi.output_type
class GetGroupResult:
    """
    A collection of values returned by getGroup.
    """
    def __init__(__self__, description=None, id=None, members=None, name=None, object_id=None, owners=None):
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if members and not isinstance(members, list):
            raise TypeError("Expected argument 'members' to be a list")
        pulumi.set(__self__, "members", members)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if object_id and not isinstance(object_id, str):
            raise TypeError("Expected argument 'object_id' to be a str")
        pulumi.set(__self__, "object_id", object_id)
        if owners and not isinstance(owners, list):
            raise TypeError("Expected argument 'owners' to be a list")
        pulumi.set(__self__, "owners", owners)

    @property
    @pulumi.getter
    def description(self) -> str:
        """
        The description of the AD Group.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def members(self) -> Sequence[str]:
        """
        The Object IDs of the Azure AD Group members.
        """
        return pulumi.get(self, "members")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the Azure AD Group.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="objectId")
    def object_id(self) -> str:
        return pulumi.get(self, "object_id")

    @property
    @pulumi.getter
    def owners(self) -> Sequence[str]:
        """
        The Object IDs of the Azure AD Group owners.
        """
        return pulumi.get(self, "owners")


class AwaitableGetGroupResult(GetGroupResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetGroupResult(
            description=self.description,
            id=self.id,
            members=self.members,
            name=self.name,
            object_id=self.object_id,
            owners=self.owners)


def get_group(name: Optional[str] = None,
              object_id: Optional[str] = None,
              opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetGroupResult:
    """
    Gets information about an Azure Active Directory group.

    > **NOTE:** If you're authenticating using a Service Principal then it must have permissions to `Read directory data` within the `Windows Azure Active Directory` API.

    ## Example Usage
    ### By Group Display Name)

    ```python
    import pulumi
    import pulumi_azuread as azuread

    example = azuread.get_group(name="A-AD-Group")
    ```


    :param str name: The Name of the AD Group we want to lookup.
    :param str object_id: Specifies the Object ID of the AD Group within Azure Active Directory.
    """
    __args__ = dict()
    __args__['name'] = name
    __args__['objectId'] = object_id
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azuread:index/getGroup:getGroup', __args__, opts=opts, typ=GetGroupResult).value

    return AwaitableGetGroupResult(
        description=__ret__.description,
        id=__ret__.id,
        members=__ret__.members,
        name=__ret__.name,
        object_id=__ret__.object_id,
        owners=__ret__.owners)
