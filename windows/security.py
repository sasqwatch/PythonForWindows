import ctypes
import sys

import windows
import windows.generated_def as gdef
from windows import winproxy

from windows.winobject.token import Token


# Specific access right

FILE_ACCESS_RIGHT = gdef.FlagMapper(
    gdef.FILE_READ_DATA,
    gdef.FILE_WRITE_DATA,
    gdef.FILE_APPEND_DATA,
    gdef.FILE_READ_EA,
    gdef.FILE_WRITE_EA,
    gdef.FILE_EXECUTE,
    gdef.FILE_READ_ATTRIBUTES,
    gdef.FILE_WRITE_ATTRIBUTES
)

DIRECTORY_ACCESS_RIGHT = gdef.FlagMapper(
    gdef.FILE_LIST_DIRECTORY,
    gdef.FILE_ADD_FILE,
    gdef.FILE_ADD_SUBDIRECTORY,
    gdef.FILE_READ_EA,
    gdef.FILE_WRITE_EA,
    gdef.FILE_TRAVERSE,
    gdef.FILE_DELETE_CHILD,
    gdef.FILE_READ_ATTRIBUTES,
    gdef.FILE_WRITE_ATTRIBUTES,
)
NAMED_PIPE_ACCESS_RIGHT = gdef.FlagMapper(
    gdef.FILE_READ_DATA,
    gdef.FILE_WRITE_DATA,
    gdef.FILE_CREATE_PIPE_INSTANCE,
    gdef.FILE_READ_ATTRIBUTES,
    gdef.FILE_WRITE_ATTRIBUTES,
)

TOKEN_ACCESS_RIGHT = gdef.FlagMapper(
    gdef.TOKEN_ASSIGN_PRIMARY,
    gdef.TOKEN_DUPLICATE,
    gdef.TOKEN_IMPERSONATE,
    gdef.TOKEN_QUERY,
    gdef.TOKEN_QUERY_SOURCE,
    gdef.TOKEN_ADJUST_PRIVILEGES,
    gdef.TOKEN_ADJUST_GROUPS,
    gdef.TOKEN_ADJUST_DEFAULT,
    gdef.TOKEN_ADJUST_SESSIONID,
)

CLUSTER_API_ACCESS_RIGH = gdef.FlagMapper(
    gdef.CLUSAPI_READ_ACCESS,
    gdef.CLUSAPI_CHANGE_ACCESS,
    gdef.CLUSAPI_NO_ACCESS,
)

FAX_ACCESS_RIGHT = gdef.FlagMapper(
    gdef.FAX_JOB_SUBMIT,
    gdef.FAX_JOB_QUERY,
    gdef.FAX_CONFIG_QUERY,
    gdef.FAX_CONFIG_SET,
    gdef.FAX_PORT_QUERY,
    gdef.FAX_PORT_SET,
    gdef.FAX_JOB_MANAGE,
)

CALLBACK_ACCESS_RIGHT = gdef.FlagMapper(
    gdef.CALLBACK_MODIFY_STATE,
)

MUTANT_ACCESS_RIGHT = gdef.FlagMapper(
    gdef.MUTANT_QUERY_STATE,
)

EVENT_ACCESS_RIGHT = gdef.FlagMapper(
    gdef.EVENT_QUERY_STATE,
    gdef.EVENT_MODIFY_STATE,
)

SEMAPHORE_ACCESS_RIGHT = gdef.FlagMapper(
    gdef.SEMAPHORE_QUERY_STATE,
    gdef.SEMAPHORE_MODIFY_STATE,
)

SEMAPHORE_ACCESS_RIGHT = gdef.FlagMapper(
    gdef.TIMER_QUERY_STATE,
    gdef.TIMER_QUERY_STATE,
)

IO_COMPLETION_ACCESS_RIGHT = gdef.FlagMapper(
    gdef.IO_COMPLETION_QUERY_STATE,
    gdef.IO_COMPLETION_MODIFY_STATE,
)

PORT_ACCESS_RIGHT = gdef.FlagMapper(
    gdef.PORT_CONNECT,
)

OBJECT_MANAGER_TYPE_ACCESS_RIGHT = gdef.FlagMapper(
    gdef.OBJECT_TYPE_CREATE
)

OBJECT_MANAGER_DIRECTORY_ACCESS_RIGHT = gdef.FlagMapper(
    gdef.DIRECTORY_QUERY,
    gdef.DIRECTORY_TRAVERSE,
    gdef.DIRECTORY_CREATE_OBJECT,
    gdef.DIRECTORY_CREATE_SUBDIRECTORY,
)

OBJECT_MANAGER_SIMLINK_ACCESS_RIGHT = gdef.FlagMapper(
    gdef.SYMBOLIC_LINK_QUERY,
)

PROCESS_ACCESS_RIGHT = gdef.FlagMapper(
    gdef.PROCESS_TERMINATE                  ,
    gdef.PROCESS_CREATE_THREAD              ,
    gdef.PROCESS_SET_SESSIONID              ,
    gdef.PROCESS_VM_OPERATION               ,
    gdef.PROCESS_VM_READ                    ,
    gdef.PROCESS_VM_WRITE                   ,
    gdef.PROCESS_DUP_HANDLE                 ,
    gdef.PROCESS_CREATE_PROCESS             ,
    gdef.PROCESS_SET_QUOTA                  ,
    gdef.PROCESS_SET_INFORMATION            ,
    gdef.PROCESS_QUERY_INFORMATION          ,
    gdef.PROCESS_SUSPEND_RESUME             ,
    gdef.PROCESS_QUERY_LIMITED_INFORMATION  ,
    gdef.PROCESS_SET_LIMITED_INFORMATION    ,
)

THREAD_ACCESS_RIGHT = gdef.FlagMapper(
    gdef.THREAD_TERMINATE,
    gdef.THREAD_SUSPEND_RESUME,
    gdef.THREAD_GET_CONTEXT,
    gdef.THREAD_SET_CONTEXT,
    gdef.THREAD_QUERY_INFORMATION,
    gdef.THREAD_SET_INFORMATION,
    gdef.THREAD_SET_THREAD_TOKEN,
    gdef.THREAD_IMPERSONATE,
    gdef.THREAD_DIRECT_IMPERSONATION,
)

JOB_ACCESS_RIGHT = gdef.FlagMapper(
    gdef.JOB_OBJECT_ASSIGN_PROCESS         ,
    gdef.JOB_OBJECT_SET_ATTRIBUTES         ,
    gdef.JOB_OBJECT_QUERY                  ,
    gdef.JOB_OBJECT_TERMINATE              ,
    gdef.JOB_OBJECT_SET_SECURITY_ATTRIBUTES,
)

KEY_ACCESS_RIGHT = gdef.FlagMapper(
    gdef.KEY_QUERY_VALUE         ,
    gdef.KEY_SET_VALUE           ,
    gdef.KEY_CREATE_SUB_KEY      ,
    gdef.KEY_ENUMERATE_SUB_KEYS  ,
    gdef.KEY_NOTIFY              ,
    gdef.KEY_CREATE_LINK         ,
    gdef.KEY_WOW64_64KEY         ,
    gdef.KEY_WOW64_32KEY         ,
    # KEY_WOW64_RES           (0x0300) # Just a mask of the 2 last
)

# ACE

ACE_FLAGS = gdef.FlagMapper(
    gdef.OBJECT_INHERIT_ACE        ,
    gdef.CONTAINER_INHERIT_ACE     ,
    gdef.NO_PROPAGATE_INHERIT_ACE  ,
    gdef.INHERIT_ONLY_ACE          ,
    gdef.INHERITED_ACE             ,
    gdef.VALID_INHERIT_FLAGS       ,
    gdef.SUCCESSFUL_ACCESS_ACE_FLAG,
    gdef.FAILED_ACCESS_ACE_FLAG
)

ACE_MASKS = gdef.FlagMapper(
    gdef.GENERIC_READ                     ,
    gdef.GENERIC_WRITE                    ,
    gdef.GENERIC_EXECUTE                  ,
    gdef.GENERIC_ALL                      ,
    gdef.READ_CONTROL                     ,
    gdef.DELETE                           ,
    gdef.WRITE_DAC                        ,
    gdef.WRITE_OWNER                      ,
)

class AceHeader(gdef.ACE_HEADER):
    """Improved ACE_HEADER"""
    def _to_ace_type(self, ace_type):
        return ctypes.cast(ctypes.byref(self), ctypes.POINTER(ace_type))[0]

    @property
    def AceType(self):
        """The type of the Ace header"""
        raw_type = super(AceHeader, self).AceType
        return ACE_CLASS_TYPE_MAPPER[raw_type]

    @property
    def flags(self):
        """The flags of the Ace header

        :type: [:class:`int`] - A list of :class:`int`
        """
        return list(self._flags_generator())

    def _flags_generator(self):
        flags = self.AceFlags
        for i in range(8): # Sizeof(AceFlags) * 8
            v = flags & (1 << i)
            if v:
                yield ACE_FLAGS[v]

    def subclass(self):
        # ACE_CLASS_BY_ACE_TYPE is defined later in this file
        subcls =  ACE_CLASS_BY_ACE_TYPE[self.AceType]
        return self._to_ace_type(subcls)

    def __repr__(self):
        return "<{0} type={1}>".format(type(self).__name__, self.AceType)


class AceBase(object): # Ca ou mettre flags extraction dans le ctypes generated
    """Base object for all ``ACE`` classes. provide access to an improved header"""
    @property
    def Header(self): # Override the ctypes Header for the struct -> return extended header
        """The Header of the ``ACE``

        :type: :class:`AceHeader`
        """
        addr = ctypes.addressof(self)
        sheader = super(AceBase, type(self)).Header
        return AceHeader.from_address(addr + sheader.offset)


class MaskAndSidACE(AceBase):
    """`Virtual` ACE for ACE struct with the following layout:

        - ACE_HEADER Header
        - ACCESS_MASK Mask
        - DWORD SidStart
    """

    def _sid_offset(self):
        return type(self).SidStart.offset

    @property
    def sid(self):
        """The sid described by the ``ACE``

        :type: :class:`windows.generated_def.winstructs.PSID`
        """
        return gdef.PSID(ctypes.addressof(self) + self._sid_offset())

    @property
    def mask(self):
        """The list of flags described by the ``ACE``

        :type: [:class:`int`] - A list of :class:`int`
        """
        return list(self._mask_generator())

    def _mask_generator(self):
        mask = self.Mask
        for i in range(32): # sizeof ACCESS_MASK * 8
            v = mask & (1 << i)
            if v:
                yield ACE_MASKS[v]

    def __repr__(self):
        return "<{0} mask={1}>".format(type(self).__name__, self.Mask)


class CallbackACE(MaskAndSidACE):
    @property
    def application_data(self):
        """The application-specific data

        see : https://msdn.microsoft.com/en-us/library/hh877860.aspx

        :type: :class:`str`
        """
        selfptr = ctypes.cast(ctypes.addressof(self), gdef.PUCHAR)
        datastart = ctypes.sizeof(self) + self.sid.size - 4
        dataend = self.Header.AceSize
        return selfptr[datastart: dataend]


class ObjectRelatedACE(MaskAndSidACE):
    FLAGS_VALUES = (gdef.ACE_OBJECT_TYPE_PRESENT,
                        gdef.ACE_INHERITED_OBJECT_TYPE_PRESENT)

    @property
    def flags(self):
        """The flags of the ``ACE``

        :type: [:class:`int`] - A list of :class:`int`
        """
        flags = self.Flags
        return [x for x in self.FLAGS_VALUES if flags & x]

    @property
    def object_type(self):
        """The ``ObjectType`` described in the ACE. ``None`` if `ACE`` has no ``ObjectType``

        :type: :class:`~windows.generated_def.winstructs.PSID` or ``None``
        """
        if not self.Flags & gdef.ACE_OBJECT_TYPE_PRESENT:
            return None
        return self.ObjectType

    @property
    def inherited_object_type(self):
        """The ``InheritedObjectType`` described in the ACE. ``None`` if `ACE`` has no ``InheritedObjectType``

        :type: :class:`~windows.generated_def.winstructs.PSID` or ``None``
        """
        if not self.Flags & gdef.ACE_INHERITED_OBJECT_TYPE_PRESENT:
            return None
        if self.Flags & gdef.ACE_OBJECT_TYPE_PRESENT:
            # There is an ObjectType so our offset is the good one
            return self.InheritedObjectType
        # No ObjectType -> InheritedObjectType is at ObjectType offset
        # Those are the same type so we can directly use ObjectType
        return self.ObjectType

    def _sid_offset(self):
        base_offset = type(self).SidStart.offset
        if not self.Flags & gdef.ACE_OBJECT_TYPE_PRESENT:
            base_offset -= ctypes.sizeof(gdef.GUID)
        if not self.Flags & gdef.ACE_INHERITED_OBJECT_TYPE_PRESENT:
            base_offset -= ctypes.sizeof(gdef.GUID)
        return base_offset

# DACL related ACE

# Allow the resolution of Header first
class AccessAllowedACE(MaskAndSidACE, gdef.ACCESS_ALLOWED_ACE):
    ACE_TYPE = gdef.ACCESS_ALLOWED_ACE_TYPE

class AccessDeniedACE(MaskAndSidACE, gdef.ACCESS_DENIED_ACE):
    ACE_TYPE = gdef.ACCESS_DENIED_ACE_TYPE

class AccessAllowedCallbackACE(CallbackACE, gdef.ACCESS_ALLOWED_CALLBACK_ACE):
    ACE_TYPE = gdef.ACCESS_ALLOWED_CALLBACK_ACE_TYPE

class AccessDeniedCallbackACE(CallbackACE, gdef.ACCESS_DENIED_CALLBACK_ACE):
    ACE_TYPE = gdef.ACCESS_DENIED_CALLBACK_ACE_TYPE

class AccessAllowedObjectACE(ObjectRelatedACE, gdef.ACCESS_ALLOWED_OBJECT_ACE):
    ACE_TYPE = gdef.ACCESS_ALLOWED_OBJECT_ACE_TYPE

class AccessDeniedObjectACE(ObjectRelatedACE, gdef.ACCESS_DENIED_OBJECT_ACE):
    ACE_TYPE = gdef.ACCESS_DENIED_OBJECT_ACE_TYPE

class AccessAllowedCallbackObjectACE(CallbackACE, gdef.ACCESS_ALLOWED_CALLBACK_OBJECT_ACE):
    ACE_TYPE = gdef.ACCESS_ALLOWED_CALLBACK_OBJECT_ACE_TYPE

# Strangly -> no SDDL for this one
class AccessDeniedCallbackObjectACE(CallbackACE, gdef.ACCESS_DENIED_CALLBACK_OBJECT_ACE):
    ACE_TYPE = gdef.ACCESS_DENIED_CALLBACK_OBJECT_ACE_TYPE


# SACL related ACE

class SystemAuditACE(MaskAndSidACE, gdef.SYSTEM_AUDIT_ACE):
    ACE_TYPE = gdef.SYSTEM_AUDIT_ACE_TYPE

class SystemAlarmACE(MaskAndSidACE, gdef.SYSTEM_ALARM_ACE):
    """reserved for future use."""
    ACE_TYPE = gdef.SYSTEM_ALARM_ACE_TYPE

class SystemAuditObjectACE(ObjectRelatedACE, gdef.SYSTEM_AUDIT_OBJECT_ACE):
    ACE_TYPE = gdef.SYSTEM_AUDIT_OBJECT_ACE_TYPE

class SystemAlarmObjectACE(ObjectRelatedACE, gdef.SYSTEM_ALARM_OBJECT_ACE):
    """reserved for future use."""
    ACE_TYPE = gdef.SYSTEM_ALARM_OBJECT_ACE_TYPE

class SystemAuditCallbackACE(CallbackACE, gdef.SYSTEM_AUDIT_CALLBACK_ACE):
    ACE_TYPE = gdef.SYSTEM_AUDIT_CALLBACK_ACE_TYPE

class SystemAlarmCallbackACE(CallbackACE, gdef.SYSTEM_ALARM_CALLBACK_ACE):
    """reserved for future use."""
    ACE_TYPE = gdef.SYSTEM_ALARM_CALLBACK_ACE_TYPE

class SystemAuditCallbackObjectACE(CallbackACE, gdef.SYSTEM_AUDIT_CALLBACK_OBJECT_ACE):
    ACE_TYPE = gdef.SYSTEM_AUDIT_CALLBACK_OBJECT_ACE_TYPE

class SystemAlarmCallbackObjectACE(CallbackACE, gdef.SYSTEM_ALARM_CALLBACK_OBJECT_ACE):
    """Reserved for future use"""
    ACE_TYPE = gdef.SYSTEM_ALARM_CALLBACK_OBJECT_ACE_TYPE

class SystemMandatoryLabelACE(MaskAndSidACE, gdef.SYSTEM_MANDATORY_LABEL_ACE):
    ACE_TYPE = gdef.SYSTEM_MANDATORY_LABEL_ACE_TYPE

class SystemResourceAttributeACE(MaskAndSidACE, gdef.SYSTEM_RESOURCE_ATTRIBUTE_ACE):
    ACE_TYPE = gdef.SYSTEM_RESOURCE_ATTRIBUTE_ACE_TYPE

    @property
    def attribute(self):
        # Sid-size not in the initial struct
        sid_size_over = self.sid.size - type(self).SidStart.size
        sec_attr_addr = ctypes.addressof(self) + ctypes.sizeof(self) + sid_size_over
        return ClaimSecurityAttributeRelativeV1.from_address(sec_attr_addr)

class SystemScopedPolicyIDACE(MaskAndSidACE, gdef.SYSTEM_SCOPED_POLICY_ID_ACE):
    ACE_TYPE = gdef.SYSTEM_SCOPED_POLICY_ID_ACE_TYPE

class SystemProcessTrustLabelACE(MaskAndSidACE, gdef.SYSTEM_PROCESS_TRUST_LABEL_ACE):
    """Reserved. (from MSDC)"""
    ACE_TYPE = gdef.SYSTEM_PROCESS_TRUST_LABEL_ACE_TYPE


ACE_CLASS_BY_ACE_TYPE = {cls.ACE_TYPE: cls for cls in (
    # DACL
    AccessAllowedACE,
    AccessDeniedACE,
    AccessAllowedCallbackACE,
    AccessDeniedCallbackACE,
    AccessAllowedObjectACE,
    AccessDeniedObjectACE,
    AccessAllowedCallbackObjectACE,
    # SACL
    SystemAuditACE,
    SystemAlarmACE, # reserved for future use.
    SystemAuditObjectACE,
    SystemAlarmObjectACE, # reserved for future use.
    SystemAuditCallbackACE,
    SystemAlarmCallbackACE, # reserved for future use.
    SystemAuditCallbackObjectACE,
    SystemAlarmCallbackObjectACE, # reserved for future use.
    SystemMandatoryLabelACE,
    SystemResourceAttributeACE,
    SystemScopedPolicyIDACE,
    SystemProcessTrustLabelACE,

)}

ACE_CLASS_TYPE_MAPPER = gdef.FlagMapper(*ACE_CLASS_BY_ACE_TYPE.keys())

# CLAIM_SECURITY_ATTRIBUTE_RELATIVE_V1 follow the SYSTEM_RESOURCE_ATTRIBUTE_ACE
# For ACE of type SYSTEM_RESOURCE_ATTRIBUTE_ACE_TYPE

def retrieve_long64_from_addr(addr):
    return gdef.LONG64.from_address(addr).value

def retrieve_ulong64_from_addr(addr):
    return gdef.ULONG64.from_address(addr).value

def retrieve_wstr_from_addr(addr):
    return gdef.LPWSTR(addr).value

# https://msdn.microsoft.com/en-us/library/hh877847.aspx
def retrieve_psid_from_addr(addr):
    psid_addr = addr + gdef.CLAIM_SECURITY_ATTRIBUTE_OCTET_STRING_RELATIVE.OctetString.offset
    return gdef.PSID(psid_addr)

def retrieve_bool_from_addr(addr):
    return bool(gdef.ULONG64.from_address(addr).value)

def retrieve_octet_string_from_addr(addr):
    # Good doc: https://msdn.microsoft.com/en-us/library/hh877833.aspx
    # Doc broken in: https://docs.microsoft.com/en-us/windows/desktop/api/winnt/ns-winnt-_claim_security_attribute_relative_v1
    ostring = gdef.CLAIM_SECURITY_ATTRIBUTE_OCTET_STRING_RELATIVE.from_address(addr)
    # Bypass the array limit
    return ctypes.cast(ostring.OctetString, gdef.PUCHAR)[:ostring.Length]

class ClaimSecurityAttributeRelativeV1(gdef.CLAIM_SECURITY_ATTRIBUTE_RELATIVE_V1):
    VALUE_ARRAY_PTR_BY_TYPE = {
        gdef.CLAIM_SECURITY_ATTRIBUTE_TYPE_INT64:
            ("pInt64", retrieve_long64_from_addr),
        gdef.CLAIM_SECURITY_ATTRIBUTE_TYPE_UINT64:
            ("pUint64", retrieve_ulong64_from_addr),
        gdef.CLAIM_SECURITY_ATTRIBUTE_TYPE_STRING:
            ("ppString", retrieve_wstr_from_addr),
        gdef.CLAIM_SECURITY_ATTRIBUTE_TYPE_SID:
            # ppString is not the good one
            # But none is doc for PSID
            ("ppString", retrieve_psid_from_addr),
        gdef.CLAIM_SECURITY_ATTRIBUTE_TYPE_BOOLEAN:
            ("pUint64", retrieve_bool_from_addr),
        gdef.CLAIM_SECURITY_ATTRIBUTE_TYPE_OCTET_STRING:
            ("pOctetString", retrieve_octet_string_from_addr),
    }

    @property
    def name(self):
        return gdef.LPWSTR(ctypes.addressof(self) + self.Name).value

    @property
    def values(self):
        array_name, get_value = self.VALUE_ARRAY_PTR_BY_TYPE[self.ValueType]
        base = ctypes.addressof(self)
        array = getattr(self.Values, array_name)
        # The pointer allow us to bypass the array _length_ of 1
        array_ptr = ctypes.cast(array, ctypes.POINTER(array._type_))
        offsets = array_ptr[:self.ValueCount]
        # Cast values
        return tuple(get_value(base + off) for off in offsets)


# ACL
class Acl(gdef.ACL):
    """All the ``ACE`` returned by :class:`Acl` methods/property are described in the :ref:`Ace section <security_ace>`"""
    @property
    def size_info(self):
        size_info = gdef.ACL_SIZE_INFORMATION()
        winproxy.GetAclInformation(self, ctypes.byref(size_info), ctypes.sizeof(size_info), gdef.AclSizeInformation)
        return size_info

    def get_ace(self, i):
        """Retrieve ``ACE`` number ``i``

        :return: :class:`Ace`
        """
        ace = gdef.PVOID()
        winproxy.GetAce(self, i, ace)
        # TODO: subclass ACL
        return AceHeader.from_address(ace.value).subclass()

    @property
    def aces(self):
        """The list of ``ACE`` in the ACL :class:`Acl`

        :type: [:class:`Ace`] - A list of ACE
        """
        return list(self)

    def __len__(self):
        """The number of ``ACE`` in the :class:`Acl`"""
        return self.AceCount

    def __getitem__(self, i):
        """Return ``ACE`` nb ``i``

        :return: :class:`Ace`
        """
        try:
            return self.get_ace(i)
        except WindowsError as e:
            if e.winerror == gdef.ERROR_INVALID_PARAMETER:
                raise IndexError("Invalid ACL index {0}".format(i))
            raise

    def __iter__(self):
        """Return an iterable over all the ``ACE`` in the :class:`Acl`

        :yield: :class:`Ace`"""
        for i in range(self.AceCount):
            yield self.get_ace(i)

    def __repr__(self):
        return "<Acl count={0}>".format(self.AceCount)

PAcl = ctypes.POINTER(Acl)

# Security descriptor
class SecurityDescriptor(gdef.PSECURITY_DESCRIPTOR):
    """A Security Descriptor

    .. warning::

        TODO: free the underliying buffer when not needed anymore for now the underliying memory is never freed.
    """
    DEFAULT_SECURITY_INFORMATION = (
        gdef.OWNER_SECURITY_INFORMATION     |
        gdef.GROUP_SECURITY_INFORMATION     |
        gdef.DACL_SECURITY_INFORMATION      |
        gdef.ATTRIBUTE_SECURITY_INFORMATION |
        # gdef.SACL_SECURITY_INFORMATION  | # Need special rights
        gdef.SCOPE_SECURITY_INFORMATION     |
        gdef.PROCESS_TRUST_LABEL_SECURITY_INFORMATION
    )
    """The default ``flags`` value for functions expecting a
    `SECURITY_INFORMATION <https://docs.microsoft.com/en-us/windows/desktop/SecAuthZ/security-information>`_.

    This value regroups the followings flags:

        - ``OWNER_SECURITY_INFORMATION``
        - ``GROUP_SECURITY_INFORMATION``
        - ``DACL_SECURITY_INFORMATION``
        - ``ATTRIBUTE_SECURITY_INFORMATION``
        - ``SCOPE_SECURITY_INFORMATION``
        - ``PROCESS_TRUST_LABEL_SECURITY_INFORMATION``

    .. warning::

        Note that the value ``SACL_SECURITY_INFORMATION`` needed to access the SACL is not present as it require the ``SeSecurityPrivilege``.

        To query the SACL enable the ``SeSecurityPrivilege`` and use the parameter ``query_sacl=True`` on the functions expecting a ``flags``

        see :ref:`Query SACL sample <sample_security_sacl>`
    """

    _close_function = winproxy.LocalFree

    @property
    def control(self):
        """The security descriptor control

        :type: :class:`~windows.generated_def.winstructs.SECURITY_DESCRIPTOR_CONTROL`
        """
        lpdwRevision = gdef.DWORD()
        control = gdef.SECURITY_DESCRIPTOR_CONTROL()
        winproxy.GetSecurityDescriptorControl(self, control, lpdwRevision)
        return control.value

    @property
    def revision(self):
        """The security descriptor's revision

        :type: :class:`int`
        """
        lpdwRevision = gdef.DWORD()
        control = gdef.SECURITY_DESCRIPTOR_CONTROL()
        winproxy.GetSecurityDescriptorControl(self, control, lpdwRevision)
        return lpdwRevision.value

    @property
    def owner(self):
        """The owner of the security descriptor

        :type: :class:`~windows.generated_def.winstructs.PSID` or ``None``
        """
        owner = gdef.PSID()
        lpbOwnerDefaulted = gdef.BOOL()
        winproxy.GetSecurityDescriptorOwner(self, owner, lpbOwnerDefaulted)
        # Return None of owner is NULL
        return owner or None

    @property
    def group(self):
        """The group of the security descriptor

        :type: :class:`~windows.generated_def.winstructs.PSID` or ``None``
        """
        group = gdef.PSID()
        lpbGroupDefaulted = gdef.BOOL()
        winproxy.GetSecurityDescriptorGroup(self, group, lpbGroupDefaulted)
        # Return None of group is NULL
        return group or None


    @property
    def dacl(self):
        """The DACL of the security descriptor.

        :type: :class:`Acl` or ``None`` if the DACL was ``NULL`` or not present
        """
        dacl_present = gdef.BOOL()
        pdacl = gdef.PACL()
        lpbDaclDefaulted = gdef.BOOL()
        winproxy.GetSecurityDescriptorDacl(self, dacl_present, pdacl, lpbDaclDefaulted)
        if not dacl_present or not pdacl:
            return None
        return ctypes.cast(pdacl, PAcl)[0]

    @property
    def sacl(self):
        """The SACL of the security descriptor. You may need special attention to retrieve it (see :any:`DEFAULT_SECURITY_INFORMATION`)

        :type: :class:`Acl` or ``None`` if the SACL was ``NULL`` or not present
        """
        sacl_present = gdef.BOOL()
        psacl = gdef.PACL()
        lpbSaclDefaulted = gdef.BOOL()
        winproxy.GetSecurityDescriptorSacl(self, sacl_present, psacl, lpbSaclDefaulted)
        if not sacl_present or not psacl:
            return None
        return ctypes.cast(psacl, PAcl)[0]

    # Constructors
    @classmethod
    def from_string(cls, sddl):
        """Return a new :class:`SecurityDescriptor` from the ``SDDL``.

        :returns: :class:`SecurityDescriptor`

        .. warning::

            At the moment the underliying buffer is never freed.

            See `ConvertStringSecurityDescriptorToSecurityDescriptorA <https://docs.microsoft.com/en-us/windows/desktop/api/sddl/nf-sddl-convertstringsecuritydescriptortosecuritydescriptora>`_
        """
        self = cls()
        winproxy.ConvertStringSecurityDescriptorToSecurityDescriptorA(
            sddl,
            gdef.SDDL_REVISION_1,
            self,
            None)
        # TODO: we need to free this buffer..
        # Keep track of Security Descritor state ?
        return self

    @classmethod
    def _from_name_and_type(cls, objname, objtype, flags=DEFAULT_SECURITY_INFORMATION, query_sacl=False):
        self = cls()

        if query_sacl:
            flags |= gdef.SACL_SECURITY_INFORMATION

        winproxy.GetNamedSecurityInfoA(
            objname,
            objtype,
            flags,
            None,
            None,
            None,
            None,
            self
        )
        return self

    @classmethod
    def _from_handle_and_type(cls, handle, objtype, flags=DEFAULT_SECURITY_INFORMATION, query_sacl=False):
        self = cls()

        if query_sacl:
            flags |= gdef.SACL_SECURITY_INFORMATION

        winproxy.GetSecurityInfo(
            handle,
            objtype,
            flags,
            None,
            None,
            None,
            None,
            self
        )
        return self

    @classmethod
    def from_filename(cls, filename, query_sacl=False, flags=DEFAULT_SECURITY_INFORMATION):
        """Retrieve the security descriptor for the file ``filename``"""
        return cls._from_name_and_type(filename, gdef.SE_FILE_OBJECT, flags=flags, query_sacl=query_sacl)

    @classmethod
    def from_handle(cls, handle, query_sacl=False, flags=DEFAULT_SECURITY_INFORMATION):
        """Retrieve the security descriptor for the kernel object described by``handle``"""
        return cls._from_handle_and_type(handle, gdef.SE_KERNEL_OBJECT, flags=flags, query_sacl=query_sacl)

    @classmethod
    def from_binary(cls, data):
        """Retrieve the security descriptor described by the binary ``data``.
        Binary security descriptor can be found in the registry for example
        """
        if isinstance(data, basestring):
            data = ctypes.c_buffer(data)
        return ctypes.cast(data, cls)

    def to_string(self, security_information=DEFAULT_SECURITY_INFORMATION):
        """Return the SDDL representation of the security descriptor

        :type: :class:`str`
        """
        result_cstr = gdef.LPSTR()
        winproxy.ConvertSecurityDescriptorToStringSecurityDescriptorA(
            self,
            gdef.SDDL_REVISION_1,
            security_information,
            result_cstr,
            None)
        result = result_cstr.value # Retrieve a python-str copy
        winproxy.LocalFree(result_cstr)
        return result


    # TST

    # def relative(self):
        # return bool(self.control & gdef.SE_SELF_RELATIVE)

    # If we want auto-free we need to handle relf-relative SD
    # We need to keep-track of sub-object of the SD
    # Just a ref to SD from SACL / DACL ?

    # def __del__(self):
        # if self._needs_free and sys.path is not None:
            # print("FREE SELF")
            # self._close_function(self)

