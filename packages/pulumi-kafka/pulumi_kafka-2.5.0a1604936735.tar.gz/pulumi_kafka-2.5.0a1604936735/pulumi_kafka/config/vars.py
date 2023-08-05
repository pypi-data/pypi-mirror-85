# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from .. import _utilities, _tables

__all__ = [
    'bootstrap_servers',
    'ca_cert',
    'ca_cert_file',
    'client_cert',
    'client_cert_file',
    'client_key',
    'client_key_file',
    'client_key_passphrase',
    'sasl_mechanism',
    'sasl_password',
    'sasl_username',
    'skip_tls_verify',
    'timeout',
    'tls_enabled',
]

__config__ = pulumi.Config('kafka')

bootstrap_servers = __config__.get('bootstrapServers')
"""
A list of kafka brokers
"""

ca_cert = __config__.get('caCert') or _utilities.get_env('KAFKA_CA_CERT')
"""
CA certificate file to validate the server's certificate.
"""

ca_cert_file = __config__.get('caCertFile')
"""
Path to a CA certificate file to validate the server's certificate.
"""

client_cert = __config__.get('clientCert') or _utilities.get_env('KAFKA_CLIENT_CERT')
"""
The client certificate.
"""

client_cert_file = __config__.get('clientCertFile')
"""
Path to a file containing the client certificate.
"""

client_key = __config__.get('clientKey') or _utilities.get_env('KAFKA_CLIENT_KEY')
"""
The private key that the certificate was issued for.
"""

client_key_file = __config__.get('clientKeyFile')
"""
Path to a file containing the private key that the certificate was issued for.
"""

client_key_passphrase = __config__.get('clientKeyPassphrase')
"""
The passphrase for the private key that the certificate was issued for.
"""

sasl_mechanism = __config__.get('saslMechanism') or (_utilities.get_env('KAFKA_SASL_MECHANISM') or 'plain')
"""
SASL mechanism, can be plain, scram-sha512, scram-sha256
"""

sasl_password = __config__.get('saslPassword') or _utilities.get_env('KAFKA_SASL_PASSWORD')
"""
Password for SASL authentication.
"""

sasl_username = __config__.get('saslUsername') or _utilities.get_env('KAFKA_SASL_USERNAME')
"""
Username for SASL authentication.
"""

skip_tls_verify = __config__.get('skipTlsVerify') or (_utilities.get_env_bool('KAFKA_SKIP_VERIFY') or False)
"""
Set this to true only if the target Kafka server is an insecure development instance.
"""

timeout = __config__.get('timeout')
"""
Timeout in seconds
"""

tls_enabled = __config__.get('tlsEnabled') or (_utilities.get_env_bool('KAFKA_ENABLE_TLS') or True)
"""
Enable communication with the Kafka Cluster over TLS.
"""

