"""Tests for xiaomi."""
import asyncio
from unittest import mock

import pytest

from zhaquirks.const import OFF, ON, ZONE_STATE
from zhaquirks.xiaomi import BasicCluster
import zhaquirks.xiaomi.aqara.motion_aq2
import zhaquirks.xiaomi.aqara.motion_aq2b
import zhaquirks.xiaomi.mija.motion

from tests.common import ZCL_OCC_ATTR_RPT_OCC, ClusterListener


def test_basic_cluster_deserialize_wrong_len():
    """Test attr report with model and xiaomi attr."""
    cluster = BasicCluster(mock.MagicMock())

    data = b"\x1c_\x11\x12\n"
    data += b'\x05\x00B\x15lumi.sensor_wleak.aq1\x01\xffB"\x01!\xb3\x0b\x03('
    data += b"\x17\x04!\xa8C\x05!\xa7\x00\x06$\x00\x00\x00\x00\x00\x08!\x04"
    data += b"\x02\n!\x00\x00d\x10\x01"

    deserialized = cluster.deserialize(data)
    assert deserialized[1]


def test_basic_cluster_deserialize_wrong_len_2():
    """Test attr report with xiaomi attr."""
    cluster = BasicCluster(mock.MagicMock())

    data = b"\x1c_\x11\x12\n"
    data += b'\x01\xffB"\x01!\xb3\x0b\x03(\x17\x04!\xa8C\x05!\xa7\x00\x06$\x15'
    data += b"\x00\x14\x00\x00\x08!\x04\x02\n!\x00\x00d\x10\x01"

    deserialized = cluster.deserialize(data)
    assert deserialized[1]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "quirk",
    (
        zhaquirks.xiaomi.aqara.motion_aq2.MotionAQ2,
        zhaquirks.xiaomi.aqara.motion_aq2b.MotionAQ2,
        zhaquirks.xiaomi.mija.motion.Motion,
    ),
)
async def test_konke_motion(zigpy_device_from_quirk, quirk):
    """Test Orvibo motion sensor."""

    motion_dev = zigpy_device_from_quirk(quirk)

    motion_cluster = motion_dev.endpoints[1].ias_zone
    motion_listener = ClusterListener(motion_cluster)

    occupancy_cluster = motion_dev.endpoints[1].occupancy
    occupancy_listener = ClusterListener(occupancy_cluster)

    p1 = mock.patch.object(motion_cluster, "reset_s", 0)
    p2 = mock.patch.object(occupancy_cluster, "reset_s", 0)
    # send motion on IAS zone command
    hdr, args = occupancy_cluster.deserialize(ZCL_OCC_ATTR_RPT_OCC)
    with p1, p2:
        occupancy_cluster.handle_message(hdr, args)

    assert len(motion_listener.cluster_commands) == 1
    assert len(motion_listener.attribute_updates) == 0
    assert motion_listener.cluster_commands[0][1] == ZONE_STATE
    assert motion_listener.cluster_commands[0][2][0] == ON

    assert len(occupancy_listener.cluster_commands) == 0
    assert len(occupancy_listener.attribute_updates) == 1
    assert occupancy_listener.attribute_updates[0][0] == 0x0000
    assert occupancy_listener.attribute_updates[0][1] == 1

    await asyncio.sleep(0.1)

    assert len(motion_listener.cluster_commands) == 2
    assert motion_listener.cluster_commands[1][1] == ZONE_STATE
    assert motion_listener.cluster_commands[1][2][0] == OFF

    assert len(occupancy_listener.cluster_commands) == 0
    assert len(occupancy_listener.attribute_updates) == 2
    assert occupancy_listener.attribute_updates[1][0] == 0x0000
    assert occupancy_listener.attribute_updates[1][1] == 0
