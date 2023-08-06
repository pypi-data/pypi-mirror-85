# -*- coding: utf-8 -*-
import time
from pinpong.board import gboard,I2C

class PN532:
  PN532_PREAMBLE                        = 0x00
  PN532_STARTCODE1                      = 0x00
  PN532_STARTCODE2                      = 0xFF
  PN532_POSTAMBLE                       = 0x00
  HOSTTOPN532                           = 0xD4
  PN532TOHOST                           = 0XD5
  
  COMMAND_SAMCONFIGURATION              = 0x14
  COMMAND_INLISTPASSIVETARGET           = 0x4A
  COMMAND_INDATAEXCHANGE                = 0x40
#  I2C_ADDRESS                           = 0x48 >> 1
  MIFARE_ISO14443A                      = 0x00
  
  CARD_CMD_READING                      = 0x30
  CARD_CMD_WRITEINGTOMIFARECLASSIC      = 0xA0
  CARD_CMD_WRITEINGTONTGE               = 0xA2
  CARD_CMD_WRITEINGTOULTRALIGHT         = 0xA2
  CARD_CMD_AUTHENTICATION_A             = 0x60
  CARD_CMD_AUTHENTICATION_B             = 0x61
  
  def __init__(self, board=None, i2c_addr=0x24, bus_num=0):
    if isinstance(board, int):
      i2c_addr = board
      board = gboard
    elif board is None:
      board = gboard
    self.i2c_addr = i2c_addr
    self.board = board
    self.i2c = I2C(bus_num)
    
    self.nfc_password = [0]
    self.nfc_enable = None
    self.receive_ACK = [0]
    self.nfc_uid = [0]
    self.block_data = [0 for i in range(16)]
    
  def begin(self):
    self.nfc_password = [0xff, 0xff, 0xff, 0xff, 0xff, 0xff]
    cmd_write = [0,0,0,0]
    cmd_write[0] = self.COMMAND_SAMCONFIGURATION
    cmd_write[1] = 0x01
    cmd_write[2] = 0x14
    cmd_write[3] = 0x01
    self.nfc_enable = True
    self.write_command(cmd_write, 4)
    time.sleep(0.01)
    if not self.read_ack(14):
      return False
    return self.receive_ACK[12] == 0x15
  
  def scan(self):
     if not self.nfc_enable:
       return False
     cmdnfc_uid = [self.COMMAND_INLISTPASSIVETARGET, 1, self.MIFARE_ISO14443A]
     self.write_command(cmdnfc_uid, 3)
     if not self.read_ack(25):
       return False
     self.nfc_uid = self.receive_ACK[19:23]
     if self.receive_ACK[13] != 1:
       return False
     return True
  
  def write_index_data(self, block, index, data):
    if not self.nfc_enable:
      return False
    if isinstance(data, str):
      real_val = []
      for i in data:
        real_val.append(int(ord(i)))
      if len(real_val) < 16:
        for i in range(16-len(real_val)):
          real_val.append(0)
      elif len(real_val) > 16:
        return False
    if isinstance(data,list):
      real_val = []
      if len(data) < 16:
        for i in range(16-len(data)):
          data.append(0)
      elif len(data) > 16:
        return False
      real_val = data
    index = max(min(index,16),1)
    self.read_data(block)
    block_data = [0 for i in range(index - 1)]
    block_data[index:] = real_val
    self.write_data(block, block_data)
    
  def write_data(self, block, data):
    if isinstance(data, tuple):
      data = list(data)
    if isinstance(data, str):
      real_val = []
      for i in data:
        real_val.append(int(ord(i)))
      if len(real_val) < 16:
        for i in range(16-len(real_val)):
          real_val.append(0)
      elif len(real_val) > 16:
        return False
    if isinstance(data,list):
      real_val = []
      if len(data) < 16:
        for i in range(16-len(data)):
          data.append(0)
      elif len(data) > 16:
        return False
      real_val = data
    if block < 128 and ((block+1)%4==0 or block==0):
      return False
    if block > 127 and block < 256 and (block+1)%16==0:
      return False
    if block > 255:
      return False
    if not self.nfc_enable:
      return False
    if not self.scan():
      return False
    if not self.passwork_check(block, self.nfc_uid, self.nfc_password):
      return False
    cmd_write = [self.COMMAND_INDATAEXCHANGE, 1, self.CARD_CMD_WRITEINGTOMIFARECLASSIC, block]
    cmd_write[4:] = real_val
    self.write_command(cmd_write, 20)
    if not self.read_ack(16):
      return False
    return True
  
  def read_data(self, block):
    if not self.nfc_enable:
      return None
    error = self._read_data(block)
    if error=="no card!" or error=="read error!" or error=="read timeout!" or error=="wake up error!" or error=="false":
      return None
    return self.block_data
  
  def _read_data(self, page):
    if page > 255:
      return "false"
    if not self.nfc_enable:
      return "wake up error!"
    if not self.scan():
      return "no card!"
    if not self.passwork_check(page, self.nfc_uid, self.nfc_password):
      return "read error!"
    cmd_read = [self.COMMAND_INDATAEXCHANGE, 1, self.CARD_CMD_READING, page]
    self.write_command(cmd_read, 4)
    if not self.read_ack(32):
      return "read timeout!"
    dataSrt = ""
    if self.check_DCS(32) == 1 and self.receive_ACK[12] == 0x41 and self.receive_ACK[13] == 0x00:
      for i in range(16):
        self.block_data[i] = self.receive_ACK[i+14]
        if self.receive_ACK[i+14] <= 0x0f:
          dataSrt += "0"
          dataSrt += str(hex(self.receive_ACK[i+14]))
        else:
          dataSrt += str(hex(self.receive_ACK[i+14]))
        if i < 15:
          dataSrt += "."
    else:
      return "read error!"
    return dataSrt
  
  def passwork_check(self, block, nfc_uid, nfc_password):
    cmd_password = [self.COMMAND_INDATAEXCHANGE, 1, 0x60, block]
    cmd_password[4:] = nfc_password[:6]
    cmd_password[10:] = nfc_uid[:5]
    self.write_command(cmd_password, 14)
    if not self.read_ack(16):
      return False
    if self.check_DCS(16) == 1 and self.receive_ACK[12] == 0x41 and self.receive_ACK[13] == 0x00:
      return True
    else:
      return False
  
  def check_DCS(self, x):
    if not self.nfc_enable:
      return False
    sum_num = sum(self.receive_ACK[6:x-2])
    dcs = 0xff - (sum_num % 256)&0xff
    if dcs == self.receive_ACK[x - 2]:
      return 1
    else:
      return 0
  
  def get_information(self):
    info = RET()
    cmdnfc_uid = [self.COMMAND_INLISTPASSIVETARGET, 1, self.MIFARE_ISO14443A]
    self.write_command(cmdnfc_uid, 3)
    if not self.read_ack(28):
      return False
    self.nfc_uid = self.receive_ACK[19:self.receive_ACK[18]]
    AQTA = [self.receive_ACK[15], self.receive_ACK[16]]
    SAK = self.receive_ACK[17]
    uid = self.receive_ACK[19:19+self.receive_ACK[18]]
    info.AQTA = AQTA
    info.sak = SAK
    info.uid = uid
    if AQTA[0] == 0x00 and AQTA[1] == 0x04:
      info.RF = "ISO/IEC1443-3,Type A"
      info.types = "MIFARE Classic 1k"
      info.lenght = 4
      info.manu = "NXP"
      info.size_total = 1024
      info.size_available = 752
      info.block = 16
      info.num_block = 64
      sector_size = 16
      return info
      
    if AQTA[0] == 0x00 and AQTA[1] == 0x44 and self.get_ultra_version(230) == 1:
      info.RF = "ISO/IEC1443-3,Type A"
      info.types = "NTAG 216"
      info.manu = "NXP"
      uid_lenght = 7
      info.size_total = 924
      info.size_available = 888
      info.block = 4
      info.num_block = 231
      sector_size = 1
      return info
      
    if AQTA[0] == 0x00 and AQTA[1] == 0x44 and self.get_ultra_version(230) != 1 and self.get_ultra_version(134) == 1:
      info.RF = "ISO/IEC1443-3,Type A"
      info.types = "NTAG 215"
      info.manu = "NXP"
      uid_lenght = 7
      info.size_total = 540
      info.size_available = 504
      info.block = 4
      info.num_block = 135
      sector_size = 1
      return info
      
    if AQTA[0] == 0x00 and AQTA[1] == 0x44 and self.get_ultra_version(134) != 1 and self.get_ultra_version(44) == 1:
      info.RF = "ISO/IEC1443-3,Type A"
      info.types = "NTAG 213"
      info.manu = "NXP"
      uid_lenght = 7
      info.size_total = 180
      info.size_available = 144
      info.block = 4
      info.num_block = 45
      sector_size = 1
      return info
      
    if AQTA[0] == 0x00 and AQTA[1] == 0x44 and self.get_ultra_version(44) != 1 and self.get_ultra_version(40) == 1:
      info.RF = "ISO/IEC1443-3,Type A"
      info.types = "Ultralight"
      info.manu = "NXP"
      uid_lenght = 7
      info.size_total = 164
      info.size_available = 128
      info.block = 4
      info.num_block = 41
      sector_size = 1
      return info
      
    if AQTA[0] == 0x00 and AQTA[1] == 0x44 and self.get_ultra_version(40) != 1 and self.get_ultra_version(19) == 1:
      info.RF = "ISO/IEC1443-3,Type A"
      info.types = "Ultralight"
      info.manu = "NXP"
      uid_lenght = 7
      info.size_total = 80
      info.size_available = 48
      info.block = 4
      info.num_block = 20
      sector_size = 1
      return info
      
    if AQTA[0] == 0x00 and AQTA[1] == 0x44 and self.get_ultra_version(19) != 1 and self.get_ultra_version(14) == 1:
      info.RF = "ISO/IEC1443-3,Type A"
      info.types = "Ultralight"
      info.manu = "NXP"
      uid_lenght = 7
      info.size_total = 448
      info.size_available = 320
      info.block = 4
      info.num_block = 41
      sector_size = 1
      return info
      
    if AQTA[0] == 0x00 and AQTA[1] == 0x02:
      info.RF = "ISO/IEC1443-3,Type A"
      info.types = "MIFARE Classic 4k"
      info.manu = "NXP"
      uid_lenght = 7
      info.size_total = 4096
      info.size_available = 3440
      info.block = 16
      info.num_block = 256
      sector_size = 39
      return info
    return None
      
  def get_ultra_version(self, block):
    if not self.nfc_enable():
      return False
    if not self.scan():
      return False
    cmd_read = [self.COMMAND_INDATAEXCHANGE, 1, self.CARD_CMD_READING, block]
    self.write_command(cmd_read, 4)
    if not self.read_ack(32):
      return False
    if self.receive_ACK[12] == 0x41 and self.receive_ACK[13] == 0x00:
      return 1
    else:
      return -1
  
  def read_ack(self, x, timeout= 1):
    pn532_ack = [0x00,0x00,0xFF,0x00,0xFF,0x00]
    time.sleep(0.03)
    value1 = self.read_to_addr(8)
    value1.pop(0)
    value1.pop()
    time.sleep(0.03)
    value2 = self.read_to_addr(x - 4)
    value2.pop(0)
    value2.pop()
    self.receive_ACK = value1 + value2
    if pn532_ack != self.receive_ACK[:6]:
      return False
    return True
    
  def write_command(self, cmd, cmd_len):
    cmd_len = cmd_len + 1
    time.sleep(0.002)
    checksum = self.PN532_PREAMBLE + self.PN532_STARTCODE1 + self.PN532_STARTCODE2
    value = [self.PN532_PREAMBLE]
    value.append(self.PN532_STARTCODE1)
    value.append(self.PN532_STARTCODE2)
    value.append(cmd_len)
    value.append(~cmd_len + 1)
    value.append(self.HOSTTOPN532)
    checksum += self.HOSTTOPN532
    for i in range(cmd_len - 1):
      value.append(cmd[i])
      checksum += cmd[i]
    tmp = checksum % 256
    value.append((~tmp)&0xff)
    value.append(self.PN532_POSTAMBLE)
    self.write_to_addr(value)
    
  def write_to_addr(self, value):
    self.i2c.writeto(self.i2c_addr, value)
    
  def read_to_addr(self, lens):
    return self.i2c.readfrom(self.i2c_addr, lens)
    
class RET():
  def __init__(self):
    self.lenght = 0
    self.uid = []
    self.AQTA = []
    self.sak = 0
    self.types = 0
    self.manu = 0
    self.RF = 0
    self.size_total = 0
    self.size_available = 0
    self.block = 0
    self.num_block = 0
    