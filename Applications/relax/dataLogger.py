import sys
from parameters import params
from datetime import datetime

class DataLogger:

    def init(self):
        self.log = ['Relax-Log\n']
        self.log.append(datetime.now().strftime('%m/%d/%Y, %H:%M:%S')+'\n\n')
        self.log.append('IP-address of host: '+params.host+'\n')

    def acquisition(self, seq, peak, fwhm, snr):
        self.log.append('\n____________________________\n')
        self.log.append(datetime.now().strftime("%H:%M:%S")+'\n')
        self.log.append('Measurement: Spectrometry\n\n')

        self.log.append('---Settings---\n')
        self.log.append('Sequence:\t'+seq+'\n')
        if seq == 'IR': self.log.append('TI [ms]:\t'+str(params.ti)+'\n')
        if seq == 'SE': self.log.append('TE [ms]:\t'+str(params.te)+'\n')
        self.log.append('Frequency [MHz]:\t'+str(params.freq*10e6)+'\n')
        self.log.append('Attenuation [dB]:\t'+str(params.at)+'\n')
        if params.avgFlag: self.log.append('Averages:\t'+str(params.avgCyc)+'\n')

        self.log.append('---Results---\n')
        self.log.append('Peak:\t'+str(peak)+'\n')
        self.log.append('FWHM [Hz]:\t'+str(fwhm)+'\n')
        self.log.append('SNR:\t'+str(snr)+'\n')

    def flipangle(self):
        self.log.append('\n____________________________\n')
        self.log.append(datetime.now().strftime("%H:%M:%S")+'\n')
        self.log.append('Tool: Flipangle\n\n')

        self.log.append('---Settings---\n')
        self.log.append('Start [dB]:\t'+str(params.flipStart)+'\n')
        self.log.append('Stop [dB]:\t'+str(params.flipEnd)+'\n')
        self.log.append('Steps:\t'+str(params.flipStep)+'\n')
        self.log.append('Timeout [ms]:\t'+str(params.flipTimeout)+'\n')

    def autocenter(self):
        self.log.append('\n____________________________\n')
        self.log.append(datetime.now().strftime("%H:%M:%S")+'\n')
        self.log.append('Tool: Autocenter\n\n')

        self.log.append('---Settings---\n')
        self.log.append('Center [MHz]:\t'+str(params.freq)+'\n')
        self.log.append('Span [MHz]:\t'+str(params.autoSpan)+'\n')
        self.log.append('Steps:\t'+str(params.autoStep)+'\n')
        self.log.append('Timeout [ms]:\t'+str(params.autoTimeout)+'\n')

    def t1(self, result, error, values):
        self.log.append('\n____________________________\n')
        self.log.append(datetime.now().strftime("%H:%M:%S")+'\n')
        self.log.append('Measurement: T1 Relaxometry\n\n')

        self.log.append('---Settings---\n')
        self.log.append('Frequency [MHz]:\t'+str(params.freq*10e6)+'\n')
        self.log.append('Attenuation [dB]:\t'+str(params.at)+'\n')
        self.log.append('TI values [ms]:\t'+str(values)+'\n')

        self.log.append('---Results---\n')
        self.log.append('T1 [ms]:\t'+str(result)+'\n')
        self.log.append('R2 error:\t'+str(error)+'\n')

    def t2(self, result, error, values):
        self.log.append('\n____________________________\n')
        self.log.append(datetime.now().strftime("%H:%M:%S")+'\n')
        self.log.append('Measurement: T2 Relaxometry\n\n')

        self.log.append('---Settings---\n')
        self.log.append('Frequency [MHz]:\t'+str(params.freq*10e6)+'\n')
        self.log.append('Attenuation [dB]:\t'+str(params.at)+'\n')
        self.log.append('TE values [ms]:\t'+str(values)+'\n')

        self.log.append('---Results---\n')
        self.log.append('T1 [ms]:\t'+str(result)+'\n')
        self.log.append('R2 error:\t'+str(error)+'\n')

    def temp(self):
        print("Adding temperature setting to log.")
        self.log.append('\n____________________________\n\n')
        self.log.append('Set temperature\n')
        self.log.append('Temperatur [°C]:\t'+str(params.temp)+'nan')

    def pause(self, dur):
        self.log.append('\n____________________________\n\n')
        self.log.append('Pause\n\n')
        self.log.append('Duration [s]:\t'+str(dur)+'\n')

    def add(self, log_type, *args, **kwargs):
        seq = kwargs.get('seq', None)
        peak = kwargs.get('peak', None)
        fwhm = kwargs.get('fwhm', None)
        snr = kwargs.get('snr', None)
        dur = kwargs.get('dur', None)
        val = kwargs.get('val', None)
        res = kwargs.get('res', None)
        err = kwargs.get('err', None)

        if log_type == 'ACQ': self.acquisition(seq, peak, fwhm, snr)
        elif log_type == 'FLA': self.flipangle()
        elif log_type == 'AUC': self.autocenter()
        elif log_type == 'T1': self.t1(res, err, val)
        elif log_type == 'T2': self.t2(res, err, val)
        elif log_type == 'TEMP': self.temp()
        elif log_type == 'PAUSE': self.pause(dur)
        else: return



logger = DataLogger()