r"""
Copyright &copy; 2020 NetApp Inc.
All rights reserved.


"""

from marshmallow import EXCLUDE, fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ImpreciseDateTime, Size


__all__ = ["CifsServiceSecurity", "CifsServiceSecuritySchema"]
__pdoc__ = {
    "CifsServiceSecuritySchema.resource": False,
    "CifsServiceSecurity": False,
}


class CifsServiceSecuritySchema(ResourceSchema):
    """The fields of the CifsServiceSecurity object"""

    encrypt_dc_connection = fields.Boolean(data_key="encrypt_dc_connection")
    r""" Specifies whether encryption is required for domain controller connections. """

    kdc_encryption = fields.Boolean(data_key="kdc_encryption")
    r""" Specifies whether AES-128 and AES-256 encryption is enabled for all Kerberos-based communication with the Active Directory KDC.
To take advantage of the strongest security with Kerberos-based communication, AES-256 and AES-128 encryption can be enabled on the CIFS server.
Kerberos-related communication for CIFS is used during CIFS server creation on the SVM, as well
as during the SMB session setup phase.
The CIFS server supports the following encryption types for Kerberos communication:

    * RC4-HMAC
    * DES
    * AES
When the CIFS server is created, the domain controller creates a computer machine account in
Active Directory. After a newly created machine account authenticates, the KDC and the CIFS server
negotiates encryption types. At this time, the KDC becomes aware of the encryption capabilities of
the particular machine account and uses those capabilities in subsequent communication with the
CIFS server.
In addition to negotiating encryption types during CIFS server creation, the encryption types are
renegotiated when a machine account password is reset. """

    lm_compatibility_level = fields.Str(data_key="lm_compatibility_level")
    r""" It is CIFS server minimum security level, also known as the LMCompatibilityLevel. The minimum security level is the minimum level of the security tokens that        the CIFS server accepts from SMB clients.
The available values are:

* lm_ntlm_ntlmv2_krb          Accepts LM, NTLM, NTLMv2 and Kerberos
* ntlm_ntlmv2_krb             Accepts NTLM, NTLMv2 and Kerberos
* ntlmv2_krb                  Accepts NTLMv2 and Kerberos
* krb                         Accepts Kerberos only


Valid choices:

* lm_ntlm_ntlmv2_krb
* ntlm_ntlmv2_krb
* ntlmv2_krb
* krb """

    restrict_anonymous = fields.Str(data_key="restrict_anonymous")
    r""" Specifies what level of access an anonymous user is granted. An anonymous user (also known as a "null user") can list or enumerate certain types of system information from Windows hosts on the network, including user names and details, account policies, and share names. Access for the anonymous user can be controlled by specifying one of three access restriction settings.
 The available values are:

 * no_restriction   - No access restriction for an anonymous user.
 * no_enumeration   - Enumeration is restricted for an anonymous user.
 * no_access        - All access is restricted for an anonymous user.


Valid choices:

* no_restriction
* no_enumeration
* no_access """

    smb_encryption = fields.Boolean(data_key="smb_encryption")
    r""" Specifies whether encryption is required for incoming CIFS traffic. """

    smb_signing = fields.Boolean(data_key="smb_signing")
    r""" Specifies whether signing is required for incoming CIFS traffic. SMB signing helps to ensure that network traffic between the CIFS server and the client is not compromised. """

    @property
    def resource(self):
        return CifsServiceSecurity

    gettable_fields = [
        "encrypt_dc_connection",
        "kdc_encryption",
        "lm_compatibility_level",
        "restrict_anonymous",
        "smb_encryption",
        "smb_signing",
    ]
    """encrypt_dc_connection,kdc_encryption,lm_compatibility_level,restrict_anonymous,smb_encryption,smb_signing,"""

    patchable_fields = [
        "encrypt_dc_connection",
        "kdc_encryption",
        "restrict_anonymous",
        "smb_encryption",
        "smb_signing",
    ]
    """encrypt_dc_connection,kdc_encryption,restrict_anonymous,smb_encryption,smb_signing,"""

    postable_fields = [
        "encrypt_dc_connection",
        "kdc_encryption",
        "restrict_anonymous",
        "smb_encryption",
        "smb_signing",
    ]
    """encrypt_dc_connection,kdc_encryption,restrict_anonymous,smb_encryption,smb_signing,"""


class CifsServiceSecurity(Resource):

    _schema = CifsServiceSecuritySchema
