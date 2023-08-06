# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if parse_version(kaitaistruct.__version__) < parse_version('0.9'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

class Bobcat1(KaitaiStruct):
    """:field callsign: frame.basic.callsign
    :field bat_v: frame.basic.bat_v
    :field bat_i_out: frame.basic.bat_i_out
    :field bat_i_in: frame.basic.bat_i_in
    :field bootcount_a3200: frame.basic.bootcount_a3200
    :field resetcause_a3200: frame.basic.resetcause_a3200
    :field bootcause_a3200: frame.basic.bootcause_a3200
    :field uptime_a3200: frame.basic.uptime_a3200
    :field bootcount_ax100: frame.basic.bootcount_ax100
    :field bootcause_ax100: frame.basic.bootcause_ax100
    :field i_pwm: frame.basic.i_pwm
    :field fs_mounted: frame.basic.fs_mounted
    :field antennas_deployed: frame.basic.antennas_deployed
    :field deploy_attempts1: frame.basic.deploy_attempts1
    :field deploy_attempts2: frame.basic.deploy_attempts2
    :field deploy_attempts3: frame.basic.deploy_attempts3
    :field deploy_attempts4: frame.basic.deploy_attempts4
    :field gyro_x: frame.basic.gyro_x
    :field gyro_y: frame.basic.gyro_y
    :field gyro_z: frame.basic.gyro_z
    :field timestamp: frame.basic.timestamp
    :field checksum: frame.hk_data.a3200_hktable0.checksum
    :field callsign: frame.hk_data.callsign
    :field bat_v: frame.hk_data.bat_v
    :field bat_i_in: frame.hk_data.bat_i_in
    :field bat_i_out: frame.hk_data.bat_i_out
    :field solar1_i: frame.hk_data.solar1_i
    :field solar1_v: frame.hk_data.solar1_v
    :field solar2_i: frame.hk_data.solar2_i
    :field solar2_v: frame.hk_data.solar2_v
    :field solar3_i: frame.hk_data.solar3_i
    :field solar3_v: frame.hk_data.solar3_v
    :field novatel_i: frame.hk_data.novatel_i
    :field sdr_i: frame.hk_data.sdr_i
    :field bootcount_p31: frame.hk_data.bootcount_p31
    :field bootcause_p31: frame.hk_data.bootcause_p31
    :field bootcount_a3200: frame.hk_data.bootcount_a3200
    :field bootcause_a3200: frame.hk_data.bootcause_a3200
    :field resetcause_a3200: frame.hk_data.resetcause_a3200
    :field uptime_a3200: frame.hk_data.uptime_a3200
    :field temp_mcu: frame.hk_data.temp_mcu
    :field i_gssb1: frame.hk_data.i_gssb1
    :field i_pwm: frame.hk_data.i_pwm
    :field panel_temp1: frame.hk_data.panel_temp1
    :field panel_temp2: frame.hk_data.panel_temp2
    :field panel_temp3: frame.hk_data.panel_temp3
    :field panel_temp4: frame.hk_data.panel_temp4
    :field panel_temp5: frame.hk_data.panel_temp5
    :field panel_temp6: frame.hk_data.panel_temp6
    :field panel_temp7: frame.hk_data.panel_temp7
    :field panel_temp8: frame.hk_data.panel_temp8
    :field panel_temp9: frame.hk_data.panel_temp9
    :field p31_temp1: frame.hk_data.p31_temp1
    :field p31_temp2: frame.hk_data.p31_temp2
    :field p31_temp3: frame.hk_data.p31_temp3
    :field p31_temp4: frame.hk_data.p31_temp4
    :field p31_temp5: frame.hk_data.p31_temp5
    :field p31_temp6: frame.hk_data.p31_temp6
    :field flash0_free: frame.hk_data.flash0_free
    :field flash1_free: frame.hk_data.flash1_free
    :field collection_running: frame.hk_data.coll_running
    :field temp_brd: frame.hk_data.temp_brd
    :field temp_pa: frame.hk_data.temp_pa
    :field bgnd_rssi: frame.hk_data.bgnd_rssi
    :field tot_tx_count: frame.hk_data.tot_tx_count
    :field tot_rx_count: frame.hk_data.tot_rx_count
    :field tot_tx_bytes: frame.hk_data.tot_tx_bytes
    :field tot_rx_bytes: frame.hk_data.tot_rx_bytes
    :field bootcount_ax100: frame.hk_data.bootcount_ax100
    :field bootcause_ax100: frame.hk_data.bootcause_ax100
    :field callsign: frame.data.basic.callsign
    :field bat_v: frame.data.basic.bat_v
    :field bat_i_out: frame.data.basic.bat_i_out
    :field bat_i_in: frame.data.basic.bat_i_in
    :field bootcount_a3200: frame.data.basic.bootcount_a3200
    :field resetcause_a3200: frame.data.basic.resetcause_a3200
    :field bootcause_a3200: frame.data.basic.bootcause_a3200
    :field uptime_a3200: frame.data.basic.uptime_a3200
    :field bootcount_ax100: frame.data.basic.bootcount_ax100
    :field bootcause_ax100: frame.data.basic.bootcause_ax100
    :field i_pwm: frame.data.basic.i_pwm
    :field fs_mounted: frame.data.basic.fs_mounted
    :field antennas_deployed: frame.data.basic.antennas_deployed
    :field deploy_attempts1: frame.data.basic.deploy_attempts1
    :field deploy_attempts2: frame.data.basic.deploy_attempts2
    :field deploy_attempts3: frame.data.basic.deploy_attempts3
    :field deploy_attempts4: frame.data.basic.deploy_attempts4
    :field gyro_x: frame.data.basic.gyro_x
    :field gyro_y: frame.data.basic.gyro_y
    :field gyro_z: frame.data.basic.gyro_z
    :field timestamp: frame.data.basic.timestamp
    :field callsign: frame.hk_frame.hk_data.callsign
    :field bat_v: frame.hk_frame.hk_data.bat_v
    :field bat_i_in: frame.hk_frame.hk_data.bat_i_in
    :field bat_i_out: frame.hk_frame.hk_data.bat_i_out
    :field solar1_i: frame.hk_frame.hk_data.solar1_i
    :field solar1_v: frame.hk_frame.hk_data.solar1_v
    :field solar2_i: frame.hk_frame.hk_data.solar2_i
    :field solar2_v: frame.hk_frame.hk_data.solar2_v
    :field solar3_i: frame.hk_frame.hk_data.solar3_i
    :field solar3_v: frame.hk_frame.hk_data.solar3_v
    :field novatel_i: frame.hk_frame.hk_data.novatel_i
    :field sdr_i: frame.hk_frame.hk_data.sdr_i
    :field bootcount_p31: frame.hk_frame.hk_data.bootcount_p31
    :field bootcause_p31: frame.hk_frame.hk_data.bootcause_p31
    :field bootcount_a3200: frame.hk_frame.hk_data.bootcount_a3200
    :field bootcause_a3200: frame.hk_frame.hk_data.bootcause_a3200
    :field resetcause_a3200: frame.hk_frame.hk_data.resetcause_a3200
    :field uptime_a3200: frame.hk_frame.hk_data.uptime_a3200
    :field temp_mcu: frame.hk_frame.hk_data.temp_mcu
    :field i_gssb1: frame.hk_frame.hk_data.i_gssb1
    :field i_pwm: frame.hk_frame.hk_data.i_pwm
    :field panel_temp1: frame.hk_frame.hk_data.panel_temp1
    :field panel_temp2: frame.hk_frame.hk_data.panel_temp2
    :field panel_temp3: frame.hk_frame.hk_data.panel_temp3
    :field panel_temp4: frame.hk_frame.hk_data.panel_temp4
    :field panel_temp5: frame.hk_frame.hk_data.panel_temp5
    :field panel_temp6: frame.hk_frame.hk_data.panel_temp6
    :field panel_temp7: frame.hk_frame.hk_data.panel_temp7
    :field panel_temp8: frame.hk_frame.hk_data.panel_temp8
    :field panel_temp9: frame.hk_frame.hk_data.panel_temp9
    :field p31_temp1: frame.hk_frame.hk_data.p31_temp1
    :field p31_temp2: frame.hk_frame.hk_data.p31_temp2
    :field p31_temp3: frame.hk_frame.hk_data.p31_temp3
    :field p31_temp4: frame.hk_frame.hk_data.p31_temp4
    :field p31_temp5: frame.hk_frame.hk_data.p31_temp5
    :field p31_temp6: frame.hk_frame.hk_data.p31_temp6
    :field flash0_free: frame.hk_frame.hk_data.flash0_free
    :field flash1_free: frame.hk_frame.hk_data.flash1_free
    :field coll_running: frame.hk_frame.hk_data.coll_running
    :field temp_brd: frame.hk_frame.hk_data.temp_brd
    :field temp_pa: frame.hk_frame.hk_data.temp_pa
    :field bgnd_rssi: frame.hk_frame.hk_data.bgnd_rssi
    :field tot_tx_count: frame.hk_frame.hk_data.tot_tx_count
    :field tot_rx_count: frame.hk_frame.hk_data.tot_rx_count
    :field tot_tx_bytes: frame.hk_frame.hk_data.tot_tx_bytes
    :field tot_rx_bytes: frame.hk_frame.hk_data.tot_rx_bytes
    :field bootcount_ax100: frame.hk_frame.hk_data.bootcount_ax100
    :field bootcause_ax100: frame.hk_frame.hk_data.bootcause_ax100
    """
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        _on = self._root.framelength
        if _on == 57:
            self.frame = Bobcat1.Bc1BasicFrame(self._io, self, self._root)
        elif _on == 144:
            self.frame = Bobcat1.Bc1HkFrame(self._io, self, self._root)
        elif _on == 69:
            self.frame = Bobcat1.Bc1BasicFrameCsp(self._io, self, self._root)
        elif _on == 156:
            self.frame = Bobcat1.Bc1HkFrameCsp(self._io, self, self._root)

    class BeaconElementHeader(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.checksum = self._io.read_u2be()
            self.timestamp = self._io.read_u4be()
            self.source = self._io.read_u2be()


    class Cspheader(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.data = self._io.read_u4be()


    class Bc1HkFrame(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.hk_header = Bobcat1.HkHeader(self._io, self, self._root)
            self.hk_data = Bobcat1.HkData(self._io, self, self._root)


    class Bc1HkFrameCsp(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.cspheader = Bobcat1.Cspheader(self._io, self, self._root)
            self.hk_frame = Bobcat1.Bc1HkFrame(self._io, self, self._root)


    class HkData(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.a3200_hktable0 = Bobcat1.BeaconElementHeader(self._io, self, self._root)
            self.callsign = (KaitaiStream.bytes_terminate(self._io.read_bytes(6), 0, False)).decode(u"ASCII")
            self.bobcat1 = (KaitaiStream.bytes_terminate(self._io.read_bytes(9), 0, False)).decode(u"ASCII")
            self.bat_v = self._io.read_u2be()
            self.bat_i_in = self._io.read_u2be()
            self.bat_i_out = self._io.read_u2be()
            self.solar1_i = self._io.read_u2be()
            self.solar1_v = self._io.read_u2be()
            self.solar2_i = self._io.read_u2be()
            self.solar2_v = self._io.read_u2be()
            self.solar3_i = self._io.read_u2be()
            self.solar3_v = self._io.read_u2be()
            self.novatel_i = self._io.read_u2be()
            self.sdr_i = self._io.read_u2be()
            self.bootcount_p31 = self._io.read_u4be()
            self.bootcause_p31 = self._io.read_u1()
            self.bootcount_a3200 = self._io.read_u2be()
            self.bootcause_a3200 = self._io.read_u1()
            self.resetcause_a3200 = self._io.read_u1()
            self.uptime_a3200 = self._io.read_u4be()
            self.temp_mcu = self._io.read_s2be()
            self.i_gssb1 = self._io.read_u2be()
            self.i_pwm = self._io.read_u2be()
            self.panel_temp1 = self._io.read_s2be()
            self.panel_temp2 = self._io.read_s2be()
            self.panel_temp3 = self._io.read_s2be()
            self.panel_temp4 = self._io.read_s2be()
            self.panel_temp5 = self._io.read_s2be()
            self.panel_temp6 = self._io.read_s2be()
            self.panel_temp7 = self._io.read_s2be()
            self.panel_temp8 = self._io.read_s2be()
            self.panel_temp9 = self._io.read_s2be()
            self.p31_temp1 = self._io.read_s2be()
            self.p31_temp2 = self._io.read_s2be()
            self.p31_temp3 = self._io.read_s2be()
            self.p31_temp4 = self._io.read_s2be()
            self.p31_temp5 = self._io.read_s2be()
            self.p31_temp6 = self._io.read_s2be()
            self.flash0_free = self._io.read_u4be()
            self.flash1_free = self._io.read_u4be()
            self.coll_running = self._io.read_u1()
            self.ax100_telemtable = Bobcat1.BeaconElementHeader(self._io, self, self._root)
            self.temp_brd = self._io.read_s2be()
            self.temp_pa = self._io.read_s2be()
            self.bgnd_rssi = self._io.read_s2be()
            self.tot_tx_count = self._io.read_u4be()
            self.tot_rx_count = self._io.read_u4be()
            self.tot_tx_bytes = self._io.read_u4be()
            self.tot_rx_bytes = self._io.read_u4be()
            self.bootcount_ax100 = self._io.read_u2be()
            self.bootcause_ax100 = self._io.read_u4be()


    class HkHeader(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.protocol_version = self._io.read_u1()
            self.type = self._io.read_u1()
            self.version = self._io.read_u1()
            self.satid = self._io.read_u2be()


    class Basic(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.callsign = (KaitaiStream.bytes_terminate(self._io.read_bytes(6), 0, False)).decode(u"ASCII")
            self.bobcat1 = (KaitaiStream.bytes_terminate(self._io.read_bytes(9), 0, False)).decode(u"ASCII")
            self.bat_v = self._io.read_u2be()
            self.bat_i_out = self._io.read_u2be()
            self.bat_i_in = self._io.read_u2be()
            self.bootcount_a3200 = self._io.read_u2be()
            self.resetcause_a3200 = self._io.read_u1()
            self.bootcause_a3200 = self._io.read_u1()
            self.uptime_a3200 = self._io.read_u4be()
            self.bootcount_ax100 = self._io.read_u2be()
            self.bootcause_ax100 = self._io.read_u4be()
            self.i_pwm = self._io.read_u2be()
            self.fs_mounted = self._io.read_u1()
            self.antennas_deployed = self._io.read_u1()
            self.deploy_attempts1 = self._io.read_u2be()
            self.deploy_attempts2 = self._io.read_u2be()
            self.deploy_attempts3 = self._io.read_u2be()
            self.deploy_attempts4 = self._io.read_u2be()
            self.gyro_x = self._io.read_s2be()
            self.gyro_y = self._io.read_s2be()
            self.gyro_z = self._io.read_s2be()
            self.timestamp = self._io.read_u4be()


    class Bc1BasicFrameCsp(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.cspheader = Bobcat1.Cspheader(self._io, self, self._root)
            self.data = Bobcat1.Bc1BasicFrame(self._io, self, self._root)


    class Bc1BasicFrame(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.basic = Bobcat1.Basic(self._io, self, self._root)


    @property
    def framelength(self):
        if hasattr(self, '_m_framelength'):
            return self._m_framelength if hasattr(self, '_m_framelength') else None

        self._m_framelength = self._io.size()
        return self._m_framelength if hasattr(self, '_m_framelength') else None


