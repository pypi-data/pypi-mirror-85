from ctypes import Structure, Union, c_int, c_long, c_size_t, c_void_p
from typing import Any, Optional

time_t = c_long
size_t = c_size_t
ssize_t = c_long
gnutls_openpgp_keyid_t: Any
gnutls_pkcs7_attrs_t = c_void_p
gnutls_transport_ptr_t = c_void_p
gnutls_typed_vdata_st = c_void_p
gnutls_x509_dn_t = c_void_p
gnutls_x509_trust_list_t = c_void_p
gnutls_alert_description_t = c_int
gnutls_alert_level_t = c_int
gnutls_certificate_import_flags = c_int
gnutls_certificate_print_formats = c_int
gnutls_certificate_request_t = c_int
gnutls_certificate_status_t = c_int
gnutls_certificate_type_t = c_int
gnutls_certificate_verify_flags = c_int
gnutls_cipher_algorithm_t = c_int
gnutls_close_request_t = c_int
gnutls_compression_method_t = c_int
gnutls_connection_end_t = c_int
gnutls_credentials_type_t = c_int
gnutls_digest_algorithm_t = c_int
gnutls_handshake_description_t = c_int
gnutls_ia_apptype_t = c_int
gnutls_kx_algorithm_t = c_int
gnutls_mac_algorithm_t = c_int
gnutls_openpgp_crt_fmt = c_int
gnutls_openpgp_crt_status_t = c_int
gnutls_params_type_t = c_int
gnutls_pk_algorithm_t = c_int
gnutls_pkcs_encrypt_flags_t = c_int
gnutls_privkey_type_t = c_int
gnutls_protocol_t = c_int
gnutls_psk_key_flags = c_int
gnutls_server_name_type_t = c_int
gnutls_sign_algorithm_t = c_int
gnutls_supplemental_data_format_type_t = c_int
gnutls_x509_crt_fmt_t = c_int
gnutls_x509_subject_alt_name_t = c_int
gnutls_certificate_print_formats_t = gnutls_certificate_print_formats
gnutls_openpgp_crt_fmt_t = gnutls_openpgp_crt_fmt

class gnutls_session_int(Structure): ...

gnutls_session_t: Any

class gnutls_ia_server_credentials_st(Structure): ...

gnutls_ia_server_credentials_t: Any

class gnutls_ia_client_credentials_st(Structure): ...

gnutls_ia_client_credentials_t: Any

class gnutls_dh_params_int(Structure): ...

gnutls_dh_params_t: Any

class gnutls_x509_privkey_int(Structure): ...

gnutls_x509_privkey_t: Any
gnutls_rsa_params_t: Any

class params(Union): ...
class gnutls_pkcs11_privkey_st(Structure): ...

gnutls_pkcs11_privkey_t: Any

class gnutls_priority_st(Structure): ...

gnutls_priority_t: Any

class gnutls_datum_t(Structure):
    data: Any = ...
    size: Any = ...
    def __init__(self, buf: Optional[Any] = ...) -> None: ...
    def get_string_and_free(self): ...

class gnutls_params_st(Structure): ...
class gnutls_certificate_credentials_st(Structure): ...

gnutls_certificate_credentials_t: Any
gnutls_certificate_server_credentials = gnutls_certificate_credentials_t
gnutls_certificate_client_credentials = gnutls_certificate_credentials_t

class gnutls_anon_server_credentials_st(Structure): ...

gnutls_anon_server_credentials_t: Any

class gnutls_anon_client_credentials_st(Structure): ...

gnutls_anon_client_credentials_t: Any

class gnutls_x509_crl_int(Structure): ...

gnutls_x509_crl_t: Any

class gnutls_x509_crt_int(Structure): ...

gnutls_x509_crt_t: Any

class gnutls_openpgp_keyring_int(Structure): ...

gnutls_openpgp_keyring_t: Any

class gnutls_srp_server_credentials_st(Structure): ...

gnutls_srp_server_credentials_t: Any

class gnutls_srp_client_credentials_st(Structure): ...

gnutls_srp_client_credentials_t: Any

class gnutls_psk_server_credentials_st(Structure): ...

gnutls_psk_server_credentials_t: Any

class gnutls_psk_client_credentials_st(Structure): ...

gnutls_psk_client_credentials_t: Any

class gnutls_openpgp_crt_int(Structure): ...

gnutls_openpgp_crt_t: Any

class gnutls_openpgp_privkey_int(Structure): ...

gnutls_openpgp_privkey_t: Any

class api_cipher_hd_st(Structure): ...

gnutls_cipher_hd_t: Any

class api_aead_cipher_hd_st(Structure): ...

gnutls_aead_cipher_hd_t: Any

class gnutls_privkey_int(Structure): ...

gnutls_privkey_t: Any

class gnutls_pubkey_int(Structure): ...

gnutls_pubkey_t: Any

class cert(Union): ...
class key(Union): ...
class gnutls_retr2_st(Structure): ...
class gnutls_x509_ava_st(Structure): ...
class gnutls_pkcs7_int(Structure): ...

gnutls_pkcs7_t: Any

class gnutls_pkcs7_signature_info_st(Structure): ...

gnutls_pkcs7_signature_info_t: Any

class gnutls_x509_crq_int(Structure): ...

gnutls_x509_crq_t: Any
gnutls_alloc_function: Any
gnutls_calloc_function: Any
gnutls_certificate_retrieve_function: Any
gnutls_db_remove_func: Any
gnutls_db_retr_func: Any
gnutls_db_store_func: Any
gnutls_free_function: Any
gnutls_handshake_post_client_hello_func: Any
gnutls_ia_avp_func: Any
gnutls_is_secure_function: Any
gnutls_log_func: Any
gnutls_openpgp_recv_key_func: Any
gnutls_oprfi_callback_func: Any
gnutls_params_function: Any
gnutls_psk_client_credentials_function: Any
gnutls_psk_server_credentials_function: Any
gnutls_pull_func: Any
gnutls_push_func: Any
gnutls_realloc_function: Any
gnutls_sign_func: Any
gnutls_srp_client_credentials_function: Any
gnutls_srp_server_credentials_function: Any
