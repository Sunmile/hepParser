import xml.dom.minidom as xml
import binascii
import zlib
import time
import numpy as np


class Peak:
    def __init__(self, mzValue, intensValue):
        self.mzValue = mzValue
        self.intensValue = intensValue


class Spectrum:
    def __init__(self, scan, mslevel, pepmass):
        self.scan = scan
        self.mslevel = mslevel
        self.pepmass = pepmass


class XmlParser:
    def __init__(self, xmlPath):
        # self.xmlPath = "/Users/hou/PycharmProjects/hepParser/mzML/rawdata1.mzML"
        # self.rootPath = "/Users/hou/PycharmProjects/hepParser/mzML/rawdata1.mzML"
        self.xmlPath = "/Users/hou/PycharmProjects/hepParser/mzML/20200818_HEP-F2-HEP-F2_NEG MS.mzML"
        self.rootPath = "/Users/hou/PycharmProjects/hepParser/mzML/hep"

    def loadXML(self):
        DOMTree = xml.parse(self.xmlPath)
        root = DOMTree.documentElement

        times, tics, scans = [], [], []
        maxTic, maxScan = 0.0, 0
        num = 0
        spectrums = root.getElementsByTagName("spectrum")
        peaks = []
        # print('12345 load_xml')
        for spectrum in spectrums:
            tmp_sp = spectrum.getAttribute('id').split('=')
            scan = tmp_sp[-1]
            scan = spectrum.getAttribute("id").split()[2].split('=')[1]

            peaksCount = int(spectrum.getAttribute("defaultArrayLength"))
            # mslevel = spectrum.childNodes[3].attributes['value'].value
            mslevel = spectrum.childNodes[1].attributes['value'].value
            tic = float(spectrum.childNodes[13].attributes['value'].value)
            startTime = float(
                spectrum.getElementsByTagName("scanList")[0].childNodes[3].childNodes[3].attributes['value'].value)
            binary_nodes = spectrum.getElementsByTagName("binary")
            bin1 = spectrum.getElementsByTagName('binaryDataArrayList')
            bin2 = bin1[0].getElementsByTagName('binaryDataArray')
            nbit = bin2[0].childNodes[1].attributes['name'].value
            if mslevel == '1':
                num += 1
                times.append(startTime)
                tics.append(tic)
                scans.append("scan=" + scan)
                if tic > maxTic:
                    maxTic = tic
                    maxScan = int(scan)

                if len(binary_nodes) > 0 and binary_nodes[0].firstChild is not None \
                        and binary_nodes[1].firstChild is not None:
                    mz_data = binary_nodes[0].firstChild.data
                    i_data = binary_nodes[1].firstChild.data
                    mz_list = self.decodeBase64AndDecompressZlib(mz_data, nbit, peaksCount)
                    inten_list = self.decodeBase64AndDecompressZlib(i_data, nbit, peaksCount)
                    peaks.append([mz_list, inten_list])
                else:
                    peaks.append([[], []])
                    mz_list = []
                    inten_list = []
                self.save_mgf(scan, mz_list, inten_list)

        print("mzml:", num)
        # 1400 * 2 * n
        return [times, tics, scans, maxScan, peaks]

    # 先对数据进行zlib压缩，再进行Base64加密，解密时先解Base64，再解zlib
    def decodeBase64AndDecompressZlib(self, data, nbit, peakCount):
        time0 = time.time()
        dec_data = binascii.a2b_base64(data)
        dec_data = zlib.decompress(dec_data)
        if nbit == '32-bit float':
            ret_data = np.frombuffer(dec_data, np.float32)
        else:
            ret_data = np.frombuffer(dec_data, np.float64)

        return ret_data

    def save_mgf(self, scan, mz_list, inten_list):
        print(scan)
        with open(self.rootPath + "/" + str(scan), 'w', newline='') as f:
            for i in range(0, len(mz_list)):
                f.write(str(mz_list[i]) + " " + str(inten_list[i]) + "\n")


def decodeBase64AndDecompressZlib(data, nbit):
    dec_data = binascii.a2b_base64(data)
    dec_data = zlib.decompress(dec_data)
    if nbit == '32-bit float':
        ret_data = np.frombuffer(dec_data, np.float32)
    else:
        ret_data = np.frombuffer(dec_data, np.float64)

    return ret_data


def getPeaksById(xmlPath, spectrumID):
    DOMTree = xml.parse(xmlPath)
    root = DOMTree.documentElement
    spectrums = root.getElementsByTagName("spectrum")
    spectrum = spectrums[spectrumID - 1]
    binary_nodes = spectrum.getElementsByTagName("binary")
    peaks = []
    bin1 = spectrum.getElementsByTagName('binaryDataArrayList')
    bin2 = bin1[0].getElementsByTagName('binaryDataArray')
    nbit = bin2[0].childNodes[1].attributes['name'].value
    maxIntensiy = 0.0
    if len(binary_nodes) > 0 and binary_nodes[0].firstChild is not None \
            and binary_nodes[1].firstChild is not None:
        mz_data = binary_nodes[0].firstChild.data
        i_data = binary_nodes[1].firstChild.data
        mz_list = decodeBase64AndDecompressZlib(mz_data, nbit)
        inten_list = decodeBase64AndDecompressZlib(i_data,nbit)
    else:
        mz_list = []
        inten_list = []
    for (mz, inten) in zip(mz_list, inten_list):
        peaks.append([mz, inten])
        maxIntensiy = max(maxIntensiy, inten)
    return peaks, maxIntensiy

# parser = XmlParser("")
# infos = parser.loadXML()
