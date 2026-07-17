# -*- encoding: utf-8 -*-
# requires a recent enough python with idna support in socket
# pyopenssl, cryptography and idna

from datetime import timezone
from datetime import datetime
from dataclasses import dataclass
from cryptography import x509
from cryptography.x509.oid import NameOID
import idna

import ssl
import socket

type Der = bytes


class Cert:
    """Wrapping some things from cryptography.x509."""

    def __init__(self, data: Der) -> None:
        """Initializes from DER byte sequences."""
        self._cert = x509.load_der_x509_certificate(data)

    @property
    def cert(self) -> x509.Certificate:
        return self._cert

    def get_alt_names(self) -> list[str] | None:
        try:
            ext = self._cert.extensions.get_extension_for_class(
                x509.SubjectAlternativeName
            )
            return ext.value.get_values_for_type(x509.DNSName)
        except x509.ExtensionNotFound:
            return None

    def get_common_name(self) -> str | None:
        try:
            names = self._cert.subject.get_attributes_for_oid(NameOID.COMMON_NAME)
            return str(names[0].value)
        except x509.ExtensionNotFound:
            return None

    def get_issuer(self) -> str | None:
        try:
            names = self._cert.issuer.get_attributes_for_oid(NameOID.COMMON_NAME)
            return names[0].value
        except x509.ExtensionNotFound:
            return None

    def is_valid_now(self) -> bool:
        valid_from = self._cert.not_valid_after_utc()
        valid_until = self._cert.not_valid_after_utc()
        now = datetime.now()

        # all include timezone, so comparison will work
        return valid_from <= now <= valid_until


@dataclass
class HostInfo:
    peername: str
    hostname: str
    cert: Cert

    def basic_info(self) -> str:
        hostname = self.hostname
        peer_name = self.peername
        common_name = self.cert.get_common_name()
        san = self.cert.get_alt_names()
        issuer = self.cert.get_issuer()
        not_before = self.cert.cert.not_valid_before_utc.isoformat()
        not_after = self.cert.cert.not_valid_after_utc.isoformat()

        s = f"""» {hostname} « … {peer_name}
        \tcommonName: {common_name}
        \tSAN: {san}
        \tissuer: {issuer}
        \tnotBefore: {not_before}
        \tnotAfter:  {not_after}
        """
        return s

class CertChecker:
    def __init__(self) -> None:
        self._ctx = self.set_context()

    def set_context(self) -> ssl.SSLContext:
        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        return ctx

    def get_certificate(self, hostname: str, port: int) -> HostInfo:
        hostname_idna = idna.encode(hostname)

        with socket.create_connection((hostname_idna, port)) as sock:
            with self._ctx.wrap_socket(sock, server_hostname=hostname_idna) as sock_ssl:
                # sock_ssl.set_connect_state()
                # sock_ssl.set_tlsext_host_name(hostname_idna)
                sock_ssl.do_handshake()
                der_cert = sock_ssl.getpeercert(binary_form=True)
                peername = sock_ssl.getpeername()
                sock_ssl.close()
                sock.close()
                cert = Cert(der_cert)

        return HostInfo(cert=cert, peername=peername, hostname=hostname)


