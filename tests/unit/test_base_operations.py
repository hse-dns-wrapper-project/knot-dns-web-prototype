"""
Тесты для базовых операций с Knot DNS.
Проверяем корректность формирования команд.
"""
import pytest
from knot_wrapper.implementation.base_operations.config import get_config, set_config, unset_config
from knot_wrapper.implementation.base_operations.zone import get_zone, set_zone, unset_zone


class TestBaseOperations:
    """Тестируем базовые операции"""
    
    def test_get_config_command_format(self, knot_ctl_mock):
        """Проверяем формат команды conf-read"""

        get_config(
            knot_ctl_mock,
            section="server",
            identifier="listen",
            item="address",
            flags="verbose",
            filters="active"
        )
        
        knot_ctl_mock.send_block.assert_called_once_with(
            cmd="conf-read",
            section="server",
            identifier="listen",
            item="address",
            flags="verbose",
            filters="active"
        )
        knot_ctl_mock.receive_block.assert_called_once()
    
    def test_set_config_command_format(self, knot_ctl_mock):
        """Проверяем формат команды conf-set"""
        set_config(
            knot_ctl_mock,
            section="zone",
            identifier="example.com",
            item="file",
            data="/var/lib/knot/example.com.zone"
        )
        
        knot_ctl_mock.send_block.assert_called_once_with(
            cmd="conf-set",
            section="zone",
            identifier="example.com",
            item="file",
            data="/var/lib/knot/example.com.zone"
        )
        knot_ctl_mock.receive_block.assert_called_once()
    
    def test_unset_config_command_format(self, knot_ctl_mock):
        """Проверяем формат команды conf-unset"""
        unset_config(
            knot_ctl_mock,
            section="zone",
            identifier="old.com",
            item="file"
        )
        
        knot_ctl_mock.send_block.assert_called_once_with(
            cmd="conf-unset",
            section="zone",
            identifier="old.com",
            item="file"
        )
        knot_ctl_mock.receive_block.assert_called_once()
    
    def test_get_zone_command_format(self, knot_ctl_mock):
        """Проверяем формат команды zone-read"""
        get_zone(
            knot_ctl_mock,
            zone="example.com",
            owner="@",
            type="A"
        )
        
        knot_ctl_mock.send_block.assert_called_once_with(
            cmd="zone-read",
            zone="example.com",
            owner="@",
            rtype="A"
        )
        knot_ctl_mock.receive_block.assert_called_once()
    
    def test_set_zone_command_format(self, knot_ctl_mock):
        """Проверяем формат команды zone-set"""
        set_zone(
            knot_ctl_mock,
            zone="example.com",
            owner="www",
            type="A",
            ttl="3600",
            data="192.168.1.100"
        )
        
        knot_ctl_mock.send_block.assert_called_once_with(
            cmd="zone-set",
            zone="example.com",
            owner="www",
            rtype="A",
            ttl="3600",
            data="192.168.1.100"
        )
        knot_ctl_mock.receive_block.assert_called_once()
    
    def test_unset_zone_command_format(self, knot_ctl_mock):
        """Проверяем формат команды zone-unset"""
        unset_zone(
            knot_ctl_mock,
            zone="example.com",
            owner="www",
            type="A",
            data="192.168.1.100"
        )
        
        knot_ctl_mock.send_block.assert_called_once_with(
            cmd="zone-unset",
            zone="example.com",
            owner="www",
            rtype="A",
            data="192.168.1.100"
        )
        knot_ctl_mock.receive_block.assert_called_once()
    
    def test_get_config_default_params(self, knot_ctl_mock):
        """Проверяем работу с параметрами по умолчанию"""
        get_config(knot_ctl_mock)
        
        knot_ctl_mock.send_block.assert_called_once_with(
            cmd="conf-read",
            section=None,
            identifier=None,
            item=None,
            flags=None,
            filters=None
        )
    
    def test_get_zone_default_params(self, knot_ctl_mock):
        """Проверяем zone-read с параметрами по умолчанию"""
        get_zone(knot_ctl_mock)
        
        knot_ctl_mock.send_block.assert_called_once_with(
            cmd="zone-read",
            zone=None,
            owner=None,
            rtype=None
        )