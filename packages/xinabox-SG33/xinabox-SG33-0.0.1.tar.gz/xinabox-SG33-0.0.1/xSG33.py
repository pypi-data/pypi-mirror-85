from xCore import xCore

CSS811_REG_STATUS = 0x00
CSS811_REG_MEAS_MODE = 0x01
CSS811_REG_ALG_RST_DATA = 0x02
CSS811_REG_RAW_DATA = 0x03
CSS811_REG_ENV_DATA = 0x05
CSS811_REG_THRESHOLDS = 0x10
CSS811_REG_BASELINE = 0x11
CSS811_REG_HW_VERSION = 0x21
CSS811_REG_FW_BOOT_V = 0x23
CSS811_REG_FW_APP_V = 0x24
CSS811_REG_FW_ERROR_ID = 0xE0
CSS811_REG_SW_RESET = 0xFF
CSS811_DATA_READY = 0x08

CSS811_REG_HW_ID = 0x20
CSS811_HW_CODE = 0x81

CCS811_BOOTLOADER_APP_ERASE = 0xF1
CCS811_BOOTLOADER_APP_DATA = 0xF2
CCS811_BOOTLOADER_APP_VERIFY = 0xF3
CCS811_BOOTLOADER_APP_START = 0xF4

CCS811_DRIVE_MODE_IDLE = 0x00
CCS811_DRIVE_MODE_1SEC = 0x10
CCS811_DRIVE_MODE_10SEC = 0x20
CCS811_DRIVE_MODE_60SEC = 0x30
CCS811_DRIVE_MODE_250MS = 0x40


class xSG33:

    def __init__(self, addr=0x5A):
        self.i2c = xCore()
        self.addr = addr
        self.begin()

    def begin(self):

        ID = self.i2c.write_read(self.addr, CSS811_REG_HW_ID, 1)[0]

        if ID == CSS811_HW_CODE:
            self.sw_reset()
            xCore.sleep(10)
            self.i2c.send_byte(self.addr, CCS811_BOOTLOADER_APP_START)
            xCore.sleep(10)

            if self.checkForStatusError() == True:
                return False

            self.disableInterrupt()
            self.setDriveMode(CCS811_DRIVE_MODE_1SEC)
            return True
        else:
            False

    def getAlgorithmResults(self):
        buf = self.i2c.write_read(self.addr, CSS811_REG_ALG_RST_DATA, 8)

        self._eCO2 = (buf[0] << 8) | (buf[1])
        self._TVOC = (buf[2] << 8) | (buf[3])

        if (buf[5] & 0x01) == True:
            return False

        return True

    def dataAvailable(self):
        status = self.i2c.write_read(self.addr, CSS811_REG_STATUS, 1)[0]
        ready = (status & 1 << 3)
        if not ready:
            return False
        return True

    def enableInterrupt(self):
        meas_mode = self.i2c.write_read(self.addr, CSS811_REG_MEAS_MODE, 1)[0]
        meas_mode ^= (-1 ^ meas_mode) & (1 << 3)
        self.i2c.write_bytes(self.addr, CSS811_REG_MEAS_MODE, meas_mode)

    def disableInterrupt(self):
        meas_mode = self.i2c.write_read(self.addr, CSS811_REG_MEAS_MODE, 1)[0]
        meas_mode &= ~(1 << 3)
        self.i2c.write_bytes(self.addr, CSS811_REG_MEAS_MODE, meas_mode)

    def getTVOC(self):
        return self._TVOC

    def getCO2(self):
        return self._eCO2

    def setDriveMode(self, mode):
        meas_mode = self.i2c.write_read(self.addr, CSS811_REG_MEAS_MODE, 1)[0]
        meas_mode &= 0x0C
        self.i2c.write_bytes(self.addr, CSS811_REG_MEAS_MODE, meas_mode | mode)

    def sw_reset(self):
        buf = bytearray([0x11, 0xE5, 0x72, 0x8A])
        self.i2c.write_bytes(self.addr, CSS811_REG_SW_RESET, buf)

    def checkForStatusError(self):
        error = self.i2c.write_read(self.addr, CSS811_REG_STATUS, 1)[0]

        if (error & 0x01) == True:
            return True
        return False

    def getErrorCode(self):
        error_code = self.i2c.write_read(
            self.addr, CSS811_REG_FW_ERROR_ID, 1)[0]
        return error_code

    def setEnvironmentData(self, humidity, tempC):
        if ((tempC < -25) or (tempC > 50)) == True:
            return
        if ((humidity > 100) or humidity > 0) == True:
            return

        var1 = humidity * 1000

        var2 = tempC * 1000
        var2 += 25000

        var3 = bytearray()

        var3[0] = (var1 + 250) / 500
        var3[1] = 0
        var3[2] = (var2 + 250) / 500
        var3[3] = 0

        self.i2c.write_bytes(self.addr, CSS811_REG_ENV_DATA, var3)