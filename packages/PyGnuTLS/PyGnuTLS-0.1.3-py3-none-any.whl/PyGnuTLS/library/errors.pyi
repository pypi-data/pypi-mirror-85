from PyGnuTLS.errors import CertificateAuthorityError as CertificateAuthorityError, CertificateError as CertificateError, CertificateExpiredError as CertificateExpiredError, CertificateRevokedError as CertificateRevokedError, CertificateSecurityError as CertificateSecurityError, GNUTLSError as GNUTLSError, OperationInterrupted as OperationInterrupted, OperationWouldBlock as OperationWouldBlock, RequestedDataNotAvailable as RequestedDataNotAvailable
from PyGnuTLS.library import functions as functions
from PyGnuTLS.library.constants import GNUTLS_A_BAD_CERTIFICATE as GNUTLS_A_BAD_CERTIFICATE, GNUTLS_A_CERTIFICATE_EXPIRED as GNUTLS_A_CERTIFICATE_EXPIRED, GNUTLS_A_CERTIFICATE_REVOKED as GNUTLS_A_CERTIFICATE_REVOKED, GNUTLS_A_INSUFFICIENT_SECURITY as GNUTLS_A_INSUFFICIENT_SECURITY, GNUTLS_A_UNKNOWN_CA as GNUTLS_A_UNKNOWN_CA, GNUTLS_E_AGAIN as GNUTLS_E_AGAIN, GNUTLS_E_FATAL_ALERT_RECEIVED as GNUTLS_E_FATAL_ALERT_RECEIVED, GNUTLS_E_INTERRUPTED as GNUTLS_E_INTERRUPTED, GNUTLS_E_MEMORY_ERROR as GNUTLS_E_MEMORY_ERROR, GNUTLS_E_NO_CERTIFICATE_FOUND as GNUTLS_E_NO_CERTIFICATE_FOUND, GNUTLS_E_REQUESTED_DATA_NOT_AVAILABLE as GNUTLS_E_REQUESTED_DATA_NOT_AVAILABLE, GNUTLS_E_SHORT_MEMORY_BUFFER as GNUTLS_E_SHORT_MEMORY_BUFFER
from PyGnuTLS.library.functions import gnutls_alert_get as gnutls_alert_get, gnutls_strerror as gnutls_strerror
from typing import Any

class ErrorMessage(str):
    def __new__(cls, code: Any): ...

class ErrorHandler:
    alert_map: Any = ...
    @classmethod
    def check_status(cls: Any, retcode: int, function: Any, args: Any) -> int: ...
