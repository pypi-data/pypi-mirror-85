#!/usr/bin/env python

import unittest
import os
import time

from PyGnuTLS.crypto import X509Certificate, X509CRL

certs_path = os.path.join("PyGnuTLS", "tests", "certs")


class TestCertificates(unittest.TestCase):
    def test_crl_is_revoked(self):

        cert = X509Certificate(open(os.path.join(certs_path, "valid.crt"), "rb").read())
        crl = X509CRL(open(os.path.join(certs_path, "crl.pem"), "rb").read())

        print("CRL certs/crl.pem:")
        print("CRL issuer:")
        print("  CN = %s" % crl.issuer.CN)  # or crl.issuer.common_name
        print("  O  = %s" % crl.issuer.O)  # or crl.issuer.organization
        print("  OU = %s" % crl.issuer.OU)  # or crl.issuer.organization_unit
        print("  C  = %s" % crl.issuer.C)  # or crl.issuer.country
        print("  ST = %s" % crl.issuer.ST)  # or crl.issuer.state
        print("  L  = %s" % crl.issuer.L)  # or crl.issuer.locality
        print("  EMAIL = %s" % crl.issuer.EMAIL)  # or crl.issuer.email
        print("CRL version:", crl.version)
        print("CRL count:  ", crl.count)

        print("Certificate certs/valid.crt:")
        print("Cert subject:")
        print("  CN = %s" % cert.subject.CN)  # or cert.subject.common_name
        print("  O  = %s" % cert.subject.O)  # or cert.subject.organization
        print("  OU = %s" % cert.subject.OU)  # or cert.subject.organization_unit
        print("  C  = %s" % cert.subject.C)  # or cert.subject.country
        print("  ST = %s" % cert.subject.ST)  # or cert.subject.state
        print("  L  = %s" % cert.subject.L)  # or cert.subject.locality
        print("  EMAIL = %s" % cert.subject.EMAIL)  # or cert.subject.email
        print("Cert issuer:")
        print("  CN = %s" % cert.issuer.CN)  # or cert.issuer.common_name
        print("  O  = %s" % cert.issuer.O)  # or cert.issuer.organization
        print("  OU = %s" % cert.issuer.OU)  # or cert.issuer.organization_unit
        print("  C  = %s" % cert.issuer.C)  # or cert.issuer.country
        print("  ST = %s" % cert.issuer.ST)  # or cert.issuer.state
        print("  L  = %s" % cert.issuer.L)  # or cert.issuer.locality
        print("  EMAIL = %s" % cert.issuer.EMAIL)  # or cert.issuer.email
        print("Cert serial:    ", cert.serial_number)
        print("Cert version:   ", cert.version)
        print("Cert activation:", time.ctime(cert.activation_time))
        print("Cert expiration:", time.ctime(cert.expiration_time))
        self.assertFalse(crl.is_revoked(cert))

        cert = X509Certificate(
            open(os.path.join(certs_path, "revoked.crt"), "rb").read()
        )
        print("Certificate certs/revoked.crt:")
        print("Cert subject:")
        print("  CN = %s" % cert.subject.common_name)  # here we use long names
        print("  O  = %s" % cert.subject.organization)
        print("  OU = %s" % cert.subject.organization_unit)
        print("  C  = %s" % cert.subject.country)
        print("  ST = %s" % cert.subject.state)
        print("  L  = %s" % cert.subject.locality)
        print("  EMAIL = %s" % cert.subject.email)
        print("Cert issuer:")
        print("  CN = %s" % cert.issuer.common_name)
        print("  O  = %s" % cert.issuer.organization)
        print("  OU = %s" % cert.issuer.organization_unit)
        print("  C  = %s" % cert.issuer.country)
        print("  ST = %s" % cert.issuer.state)
        print("  L  = %s" % cert.issuer.locality)
        print("  EMAIL = %s" % cert.issuer.email)
        print("Cert serial:    ", cert.serial_number)
        print("Cert version:   ", cert.version)
        print("Cert activation:", time.ctime(cert.activation_time))
        print("Cert expiration:", time.ctime(cert.expiration_time))
        self.assertTrue(crl.is_revoked(cert))


if __name__ == "__main__":
    unittest.main()
