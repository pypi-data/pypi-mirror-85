import serial
import time
import sys
import binascii
import struct

class TMC5160_UART:

    def __init__(self, dconf):

        while(1):
            try:
                self.sport = serial.Serial(dconf['comm_dev'],dconf['baud'],timeout=1)
                break
            except serial.SerialException as e:
                print("{} trying again".format(e), file=sys.stderr)

            time.sleep(7)    

        self.rFrame  = [0x55, 0, 0, 0  ]
        self.wFrame  = [0x55, 0, 0, 0 , 0, 0, 0, 0 ]    


    ## ---------------------------------------------
    ##  Acknowledge these folks
    ## https://techoverflow.net/2020/02/22/computing-the-crc8-atm-crc-in-python/
    ## ---------------------------------------------
    def compute_crc8_atm(self,datagram, initial_value=0):
        crc = initial_value
        # Iterate bytes in data
        for byte in datagram:
            # Iterate bits in byte
            for _ in range(0, 8):
                if (crc >> 7) ^ (byte & 0x01):
                    crc = ((crc << 1) ^ 0x07) & 0xFF
                else:
                    crc = (crc << 1) & 0xFF
                # Shift to next bit
                byte = byte >> 1
        return crc

    # -------------------------------
    def read_reg(self,mtr_id,reg):

        self.rFrame[1] = mtr_id
        self.rFrame[2] = reg
        self.rFrame[3] = self.compute_crc8_atm(self.rFrame[:-1])

        rtn = self.sport.write(self.rFrame)
        if rtn != len(self.rFrame):
            print("Err in write {}".format(__), file=sys.stderr)
            return False

        rtn = self.sport.read(8)

        time.sleep(.000005)  # adjust per baud and hardware. Sequential reads without some delay fail.
        
        return(rtn[3:7])

    # -------------------------------
    def read_int(self,mtr_id,reg):

        rtn = self.read_reg(mtr_id,reg)
        
        val = struct.unpack(">i",rtn)[0]
        return(val)

    # -------------------------------
    def write_reg(self,mtr_id,reg,val):

        self.wFrame[1] = mtr_id
        self.wFrame[2] =  reg | 0x80;  # set write bit
        
        self.wFrame[3] = 0xFF & (val>>24)
        self.wFrame[4] = 0xFF & (val>>16)
        self.wFrame[5] = 0xFF & (val>>8)
        self.wFrame[6] = 0xFF & val

        self.wFrame[7] = self.compute_crc8_atm(self.wFrame[:-1])

        rtn = self.sport.write(self.wFrame)
        if rtn != len(self.wFrame):
            print("Err in write {}".format(__), file=sys.stderr)
            return False

        time.sleep(.000002)  # adjust per baud and hardware. 

        return(True)

# Unit Test code... 
if __name__ == "__main__":

    import signal
      
    # --- need to stop motor if cntl-c
    def signal_handler(sig, frame):
        drv.write_reg(mtr_id, reg.VMAX, 0)
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    # check for required comm device input
    try:
        dev_file = sys.argv[1]
    except:
        print("\nSpecify device eg:\n >python tmc_uart.py COM7")
        sys.exit(1)

    drvconf = { 'comm_dev':dev_file, 'baud':500000 }
    drv = TMC5160_UART(drvconf)

    mtr_id = 0
    
    rst = drv.write_reg(0,reg.GCONF,0x0000000C)
    rst = drv.read_reg(0, reg.GCONF)
    print("GONF = ",rst)

    # MULTISTEP_FILT=1, EN_PWM_MODE=1 enables stealthChop™
    drv.write_reg(mtr_id, reg.GCONF, 0x0000000C);

    # TOFF=3, HSTRT=4, HEND=1, TBL=2, CHM=0 (spreadCycle™)
    drv.write_reg(mtr_id, reg.CHOPCONF, 0x000100C3);

    # IHOLD=8, IRUN=15 (max. current), IHOLDDELAY=6
    #drv.write_reg(mtr_id, reg.IHOLD_IRUN, 0x00080F0A);
    drv.write_reg(mtr_id, reg.IHOLD_IRUN, 0x00087F0A);

    # TPOWERDOWN=10: Delay before power down in stand still
    drv.write_reg(mtr_id, reg.TPOWERDOWN, 0x0000000A);

    # TPWMTHRS=500
    drv.write_reg(mtr_id, reg.TPWMTHRS, 0x000001F4); 

    # Values for speed and acceleration
    drv.write_reg(mtr_id, reg.VSTART, 4);
    drv.write_reg(mtr_id, reg.A1, 5000);
    drv.write_reg(mtr_id, reg.V1, 1000);
    drv.write_reg(mtr_id, reg.AMAX, 3000);   
    drv.write_reg(mtr_id, reg.VMAX, 10000);
    drv.write_reg(mtr_id, reg.DMAX, 5000);
    drv.write_reg(mtr_id, reg.D1, 1000);
    drv.write_reg(mtr_id, reg.VSTOP, 5);

    rst =  drv.read_int(0, reg.IFCNT)
    print("IFCNT reg = ",rst)


    cnt = 0
    vmode_dir = 2
    while(1):

        swmode = drvstatus = drv.read_reg(mtr_id,reg.SWMODE)
        gstat = drv.read_reg(mtr_id, reg.GSTAT)
        lost = drv.read_int(mtr_id,reg.LOST_STEPS)
        xactual = drv.read_int(mtr_id,reg.XACTUAL)
        xactual_reg = drv.read_reg(mtr_id,reg.XACTUAL)
        
        dvrstatus = drvstatus = drv.read_reg(mtr_id,reg.DRVSTATUS)
        print("gstat dvrstatus {} {} {} {} |{}| {}".format(gstat.hex(),dvrstatus.hex(),swmode.hex(),lost,xactual,xactual_reg.hex()))
      
        if cnt % 2:

            if vmode_dir == 2:
                vmode_dir = 1
            else:
                vmode_dir = 2

        drv.write_reg(mtr_id,reg.RAMPMODE, vmode_dir )
        drv.write_reg(mtr_id, reg.VMAX, 10000);
       
        cnt =+ 1
        
        time.sleep(10)

        if cnt >= 100: 
            drv.write_reg(mtr_id, reg.VMAX, 0);
            sys.exit(1)