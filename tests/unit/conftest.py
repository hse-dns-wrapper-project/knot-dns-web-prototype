"""
Фикстуры для unit-тестов Knot DNS Wrapper.
"""
import pytest
from datetime import datetime, timezone
from unittest.mock import Mock


@pytest.fixture
def knot_ctl_mock():
    """
    мок для KnotCtl.
    """
    mock = Mock()
    mock.send_block = Mock()
    mock.receive_block = Mock()
    return mock


@pytest.fixture
def sample_zone_data():
    """Реальные данные зоны для тестирования парсинга"""
    return {
        "zone": {
            "example.com": [
                "@ 3600 IN SOA ns1.example.com. admin.example.com. 1 3600 1800 604800 3600",
                "@ 3600 IN NS ns1.example.com.",
                "@ 3600 IN A 192.168.1.1",
                "www 3600 IN A 192.168.1.100",
                "mail 3600 IN A 192.168.1.200",
                "@ 3600 IN MX 10 mail.example.com."
            ],
            "test.org": [
                "@ 3600 IN SOA ns1.test.org. admin.test.org. 1 3600 1800 604800 3600"
            ]
        }
    }


@pytest.fixture
def sample_config_data():
    """Реальные данные конфигурации для тестирования"""
    return {
        "server": {
            "listen": ["0.0.0.0@53", "[::1]@53"],
            "rundir": "/run/knot"
        },
        "log": [
            {"target": "syslog", "any": "error"},
            {"target": "stderr", "any": "info"}
        ]
    }


@pytest.fixture
def versions_controller():
    """контроллер версий"""
    from knot_wrapper.implementation.asynchronous.versions.controller import VersionsController
    return VersionsController()


@pytest.fixture
def versions_storage():
    """хранилище версий"""
    from knot_wrapper.implementation.asynchronous.versions.storage import VersionsStorage
    return VersionsStorage()


@pytest.fixture
def command_binder():
    """биндер команд"""
    from knot_wrapper.implementation.asynchronous.processor.binder import create_command_binder
    return create_command_binder()


@pytest.fixture
def processor(command_binder):
    """процессор"""
    from knot_wrapper.implementation.asynchronous.processor.processor import Processor
    return Processor(command_binder)


@pytest.fixture
def current_timestamp():
    """текущая временная метка"""
    return datetime.now(timezone.utc)


@pytest.fixture
def reset_transaction_registry():
    """
    Сброс глобальных регистров транзакций перед тестом.
    """
    import knot_wrapper.transaction as tx_module
    
    original = {
        'path': tx_module.global_knot_path,
        'ctl': tx_module.global_knot_ctl_transaction_impl,
        'config': tx_module.global_knot_config_transaction_impl,
        'zone': tx_module.global_knot_zone_transaction_impl
    }

    tx_module.global_knot_path = None
    tx_module.global_knot_ctl_transaction_impl = None
    tx_module.global_knot_config_transaction_impl = None
    tx_module.global_knot_zone_transaction_impl = None
    
    yield
    tx_module.global_knot_path = original['path']
    tx_module.global_knot_ctl_transaction_impl = original['ctl']
    tx_module.global_knot_config_transaction_impl = original['config']
    tx_module.global_knot_zone_transaction_impl = original['zone']