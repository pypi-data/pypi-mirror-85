from re import search
from base64 import  b64decode
import binascii
import sys
import argparse
from urllib.parse import unquote, urlencode
from urllib.request import urlopen

string = ""
sensitive = True
text_type = str
binary_type = bytes
roter=''
decoded = []
currentstring = 0
loop = 0
listofstrings = []
g = '\033[1;32m[+]\033[1;m'
w = '\033[1;97m'
e = '\033[1;m\033[1;32m'
li = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
def ensure_str(s, encoding='latin-1', errors='strict'):
    """Coerce *s* to `str`.
    For Python 2:
      - `unicode` -> encoded to `str`
      - `str` -> `str`
      - `bytes or bytearray` -> converted to str
    For Python 3:
      - `str` -> `str`
      - `bytes or bytearray` -> decoded to `str`
    """

    if not isinstance(s, (text_type, binary_type, bytearray)):
        raise TypeError("not expecting type '%s'" % type(s))
    if isinstance(s, (binary_type, bytearray)):
        s = s.decode(encoding, errors)
    return s


def check_ascii(s):
    """Sometimes the string is wrongly identified to be in someform of encoding and when it is decoded it gives gibberish this might to help to identify such wrong identification"""

    return all(ord(c) < 128 for c in s)
    '''try:
        s.decode('ascii')
        return True
    except UnicodeDecodeError:
        return False'''


def Quit():
    global currentstring
    global decoded
    decoded = []
    if len(listofstrings) == currentstring:
        quit()
    else:
        print("String number: ", currentstring)
        currentstring += 1
        main(listofstrings[currentstring - 1])
    # raise Exception("Couldnt find better way to quit a recursion")


def reverse(string):
    print('%s %s' % (g, string[::-1]))
    Quit()


def rotifier(string, roter):
    rotated = []

    def rotx(number, x):
        while 1 == 1:
            find = number + roter
            try:
                replace = find - 26 * x
                rotated.append(li[replace])
                break
            except:
                x = x + 1

    rotable = list(string.lower())
    for char in rotable:
        match = search(r'[a-z]', char)
        if match:
            number = 0
            for replace in li:
                if char == replace:
                    x = 1
                    rotx(number, x)
                    break
                else:
                    number = number + 1
        else:
            rotated.append(char)
    string = ''.join(rotated)
    string = ensure_str(string)
    print(g + ' Rot%s : ' % (roter), string)
    if roter == 'all':
        pass
    else:
        try:
            decode(string, 'none')
        except:
            pass


def SHA2(string, base):
    html = urlopen(
        "http://md5decrypt.net/Api/api.php?hash=" + string + "&hash_type=sha256&email=deanna_abshire@proxymail.eu&code=1152464b80a61728")
    string = html.read()
    string = ensure_str(string)
    if len(string) > 0:
        if string in decoded:
            Quit()
        print(g + ' Cracked SHA2 Hash: %s' % string)
        decoded.append(string)
        decode(base, 'sha2')
        Quit()
    else:
        print('\033[1;31m[-]\033[1;m Its a SHA2 Hash but I failed to crack it.')
        Quit()


def SHA1(string, base):
    data = urlencode({"auth": "8272hgt", "hash": string, "string": "", "Submit": "Submit"})
    html = urlopen("http://hashcrack.com/index.php", data)
    find = html.read()
    match = search(r'<span class=hervorheb2>[^<]*</span></div></TD>', find)
    if match:
        string = match.group().split('hervorheb2>')[1][:-18]
        string = ensure_str(string)
        if string in decoded:
            Quit()
        print(g + ' Cracked SHA1 : %s' % string)
        decoded.append(string)
        decode(base, 'sha1')
        Quit()
    else:
        print('\033[1;31m[-]\033[1;m Its a SHA1 Hash but I failed to crack it.')
        Quit()


def MD5(string, base):
    url = "http://www.nitrxgen.net/md5db/" + string
    string = urlopen(url).read()
    string = ensure_str(string)
    if len(string) > 0:
        if string in decoded:
            Quit()
        print(g + ' Cracked MD5 Hash : %s' % string)
        decoded.append(string)
        decode(base, 'md5')
        Quit()
    else:
        print('\033[1;31m[-]\033[1;m Its a MD5 Hash but I failed to crack it.')
        Quit()


def fromchar(string, base):
    string = string.lower()
    string = string.strip('string.fromcharcode(').strip(')').strip(' ')
    jv_list = string.split(',')
    decoded = []
    for i in jv_list:
        i = i.replace(' ', '').replace('97', 'a').replace('98', 'b').replace('99', 'c').replace('100', 'd').replace(
            '101', 'e').replace('102', 'f').replace('103', 'g').replace('104', 'h').replace('105', 'i').replace('106',
                                                                                                                'j').replace(
            '107', 'k').replace('108', 'l').replace('109', 'm').replace('110', 'n').replace('111', 'o').replace('112',
                                                                                                                'p').replace(
            '113', 'q').replace('114', 'r').replace('115', 's').replace('116', 't').replace('117', 'u').replace('118',
                                                                                                                'v').replace(
            '119', 'w').replace('120', 'x').replace('121', 'y').replace('122', 'z').replace('48', '0').replace('49',
                                                                                                               '1').replace(
            '50', '2').replace('51', '3').replace('52', '4').replace('53', '5').replace('54', '6').replace('55',
                                                                                                           '7').replace(
            '56', '8').replace('57', '9').replace('33', '!').replace('64', '@').replace('35', '#').replace('36',
                                                                                                           '$').replace(
            '37', '%').replace('94', '^').replace('38', '&').replace('42', '*').replace('40', '(').replace('41',
                                                                                                           ')').replace(
            '45', '-').replace('61', '=').replace('95', '_').replace('43', '+').replace('91', '[').replace('93',
                                                                                                           ']').replace(
            '92', '\\').replace('59', ';').replace('39', '\'').replace('44', ',').replace('46', '.').replace('47',
                                                                                                             '/').replace(
            '123', '{').replace('125', '}').replace('124', '|').replace('58', ':').replace('34', '"').replace('60',
                                                                                                              '<').replace(
            '62', '>').replace('63', '?').replace('32', ' ').replace(',', '').replace('65', 'A').replace('66',
                                                                                                         'B').replace(
            '67', 'C').replace('68', 'D').replace('69', 'E').replace('70', 'F').replace('71', 'G').replace('72',
                                                                                                           'H').replace(
            '73', 'I').replace('74', 'J').replace('75', 'K').replace('76', 'L').replace('77', 'M').replace('78',
                                                                                                           'N').replace(
            '79', 'O').replace('80', 'P').replace('81', 'Q').replace('82', 'R').replace('83', 'S').replace('84',
                                                                                                           'T').replace(
            '85', 'U').replace('86', 'V').replace('87', 'W').replace('88', 'X').replace('89', 'Y').replace('90',
                                                                                                           'Z').replace(
            '32', ' ')
        decoded.append(i)
    string = ''.join(decoded)
    string = ensure_str(string)
    if string in decoded:
        Quit()
    print(g + ' Decoded from FromChar : %s' % (string))
    decoded.append(string)
    decode(string, 'none')
    decode(base, 'jv_char')
    Quit()


def urle(string, base):
    string = unquote(string)
    string = ensure_str(string)
    if string in decoded:
        Quit()
    print(g + ' Decoded from URL encoding : %s' % (string))
    decoded.append(string)
    decode(string, 'none')
    decode(base, 'url')
    Quit()


def hexenc(string, base):
    string = string.replace('0x', '')
    try:
        string = bytearray.fromhex(string)
    except:
        print('\033[1;31m[-]\033[1;m Failed to detect the encoding.')
        if loop == 0:
            quit()
    string = ensure_str(string)

    if string in decoded:
        Quit()
    print(g + ' Decoded from Hex : %s' % (string))
    decoded.append(string)
    decode(string, 'none')
    decode(base, 'hexx')
    Quit()


def base64(string, base):
    string = b64decode(string)
    string = ensure_str(string)
    if string in decoded:
        Quit()
    print(g + ' Decoded from Base64 : %s' % (string))
    decoded.append(string)
    decode(string, 'none')
    decode(base, 'b64')
    Quit()


def int_to_bytes(i):
    hex_string = '%x' % i
    n = len(hex_string)
    return binascii.unhexlify(hex_string.zfill(n + (n & 1)))


def bin_to_ascii(string, base):
    n = int(string, 2)
    string = int_to_bytes(n).decode()
    string = ensure_str(string)
    if string in decoded:
        Quit()
    print(g + ' Decoded from Binary : %s' % (string))
    decoded.append(string)
    decode(string, 'none')
    decode(base, 'binary')
    Quit()


def decimal(string, base):
    calculated = []
    string = ensure_str(string)
    string = string.replace('&#', '').replace(';', ' ')
    str_list = string.split(' ')
    for i in str_list:
        if i == ' ':
            pass
        else:
            try:
                i = int(i)
                calculated.append(chr(i))
            except:
                pass
    string = ''.join(calculated).encode('utf-8')
    if string in decoded:
        Quit()
    print(g + ' Decoded from Decimal : %s' % (string))
    decoded.append(string)

    decode(string, 'none')
    decode(base, 'deci')
    Quit()


def decode(string, stop):
    string = ensure_str(string)
    global loop
    if check_ascii(string):
        base = string
        binary = search(r'^[01]+$', string)
        if binary and stop != 'binary':
            bin_to_ascii(string, base)
        sha2 = search(r'^([a-f0-9]{64})$', string)
        if sha2 and not sensitive and stop != 'sha2':
            SHA2(string, base)
        sha1 = search(r'^([a-f0-9]{40})$', string)
        if sha1 and not sensitive and stop != 'sha1':
            SHA1(string, base)
        md5 = search(r'^([a-f0-9]{32})$', string)
        if md5 and not sensitive and stop != 'md5':
            MD5(string, base)
        jv_char = search(r'\d*, \d*,', string)
        if jv_char and stop != 'jv_char':
            fromchar(string, base)
        url = search(r'(%..)+', string)
        if url and stop != 'url':
            urle(string, base)
        hexx = search(r'^(0x|0X)?[a-fA-F0-9]+$', string)
        if hexx and stop != 'hexx':
            hexenc(string, base)
        b64 = search(r'^[A-Za-z0-9+\/=]+$', string)
        if len(string) % 4 == 0 and b64 and stop != 'b64':
            base64(string, base)
        deci = search(r'&#.*;+', string)
        if deci and stop != 'deci':
            decimal(string, base)
        elif not decoded:
            print('\033[1;31m[-]\033[1;m Failed to detect the encoding.')
            quit()
        loop += 1
        return 1
string='UEsDBBQACAgIABKoWVEAAAAAAAAAAAAAAAAOAAAAVGFibGUgZGF0YS5jc3aNXNduI0uWfO-vuC8L7ALKQnrzKEN576UXIU0VJcpQnhK_fuOQ6qaoZqF5MdPoOxPJyso8J05EmlqOz2VhGX_891rHl_r5v3x3k29fFo6__9t_j_TXb6CX6_7g4b___Z__Gzf9arP8A_wH9eu4_xrvFgS3YoFXyi1YtyArZ37ZHFPjQ2JcBct0cpGFIByzSbjaFJ-1ENXd3h57YgfvF5-dBSksfsHqBckXXBX0r9pmmbivWaplYloUz3xSDVM6uhJVI4xR1etxlz1sDz_TGl8QeDavtF3QC6LS5lcwsjFaFha54OhCaVjg2bBaGlF7JVLIZvoHjKYf8OMfsL-881n5JjBjTWTaWPSFJ854LtJ4W6tiTNU5X7LD9_y2bfOCVfQKasEs2MrZX8oLoaTkzsnAtRNCm2rntOO5HHy8vXUXFD1HyAWBIZPulw_BGBOCdzbg79oEX3XvFs3gXN2crvYXlMSv8zD6dfETrYwPU2hJg8HxxwL_iRUGYz-F5fTeC27BV0r9Co2NyhdMWAx47ZQ8Cxh0loVNRYbSmCArdS0uV-6XTlf2BgvCo7lfkJg3oX_pYGqZ68I0goJpTTNfQmGpBC1q2zgddVV22Oqt8IsnjxsLYjRtYdTT6SGzTls5NWRCjrFyQVda_wX3zvwNN2r006LOIYS6ZtohCLTjiSWtG1Zs4TE3Javsqhe3rlYPL472urcLYhTSBtPjKht-1a72PgfFpCwa0YA39Mkb5rhTIqvEo26q8tTpLPcfbje7nNrrSprxwwXimzstpTfBYi5EtX9pTK32D716WcDLV_JrBIRVpUbO5FAjcWTULNlGM2G9S8oKnet6avSprZHjtiVri1xjDtGDlEHehFQsS1KkJLmx0YRq_Xn55vLirfNymBc8AtCO2yI2rHZSSEmxpKRxrtpw6_31FK4fBycLNMfID4ExrcwvrjCK3mUmBEdulcaxIFNivmhpmlJKU3z1dPnMil9LN3KwQLTAKdQF_2W1cDk14AaHX9DFIDiCxMSooo1TyKvGVhvn12em2Rg8he4CBQjRw9_dVBjSqW6OYmn8RhSsQmTN6izRR2cV82jKpGt0Ds4oJVN1uLrcqc-27Sm_GLW1v6e78QqBbCyLNNNaF4Wx5ArTbUrKmrtkp-ln1Em1oDCkHM0bZV2xnKm68UxnblmgWXWSe4_Bi0jGarh5cnO36PfOTzpoLirzFSwqOK4lKEAbwYW1RplqZXu4t3huSzxeXBgx5Ti1jcJQGJ5ZYz2yzSBPvcyeJWNFbmqdfW2notISt41DzeqSfIhgxGCbL46WhYPufGyS8bLOuXq6PXveZYPzNd4ZPVeN-1hEtr7hgmWPkdF1jCw5VzPT5EaIpi5Clap-2d1e2-qptYba2sqMn6tB3UEXtNWUjt5gYpTQTBWrYql9wNhOTYyZhLiRwimVMyINj9TFIea4l6xOMTthmohcqa6a3tbmweLyJn9BW1U59TtuQSi-BhuyHGuHbjvHIioJC43IBb9Ql0ZVQW7aO75s1u756NEqEEX_TGKrnJxKYioeYjwrUlojvAtegA0VV5xX6-ViZ_FpsK-7eYSUs5BCC_0XckxfKDiN9LVmhTcS8Sgw0chrFFTFTRQ1otlPFVRqys0CMaDXv0LOrvGgqxoFGJnG8c41jwyPt4EXVLJkphKWatM43zHZKiJBjWB1jWKgkd4sRV2YkcGFggrPvZkKlNEL-lG_a42u1QgyS7VcI2oYzQALFnFbjPP8R5CN2o4nGzPDlQuZoWShbSM1iwg81uRsHa-1965Ug_7gTenBXU4Xo7Zh_FzBtdJaByWVE0p5q2318vS69b69FA73UXxBSHrMKQp8hNQ20CqIfiIwPBBEz11QEZzEpQpVfOkL_vKSl3oXC2ryeqokCaGB3lkKKIt-Bq-QDKg0LjW5pMZNUS611XrU1vGSkkAsKy4amlLEsrKFNamJxTtQcNHVY9edmKPVPd_9autm8aAx3E_x4KiLYgQNTXJBWsdExgDqnAzzCAVWGx7r5IqvG14d1XnwcNR7s6sbo7Z2nKoJPF18lMx6TzyPiYuNR4FB6gudtOXG__V6XxWlgAlqDc7Dqzh6roAQiChsyssSTCOd1BW72VXbfHP4xMfP1aNUtaC3X1BtIeQ6MdsERJ1WjnkPIRG1Qi2stWtQ7Yfrds08vsa19YNRqH9RKALSop8OZB9RYiTNCKVMo1F3kGc8ZDkVOd_bRu1BvIZh-pBpoZZ4AwyfHkVC9jraNEXdI00ivtrGaCFwGIiERAbiKZFurKPgEEFg_wA6GrLdNfm5yYcno7ZB_-YXkH1Q-A-qIOqENVxUp0crj93OSy_7F4BVJdUMQQHmU1Nc9CUVZ1UTb5WcqiaEHc-Y0A5Jo6SVzniNdsbIqn97NNhau1gJ_fEIa_Ub6xRHWCAOkD8YUxeq-mzp0rnB5lqf3kxUXz0w0nkpofitFcZJkL2sdgerHV3etjpnBAU32y8s_IKzUhlNr8e5RJ2MOzzdvew6droz-ln-hW2MiNB_TMdYyCGgxgqUaA6phiDLAZWlWmv6uw87m_vGj9_0Sw0iBHKOFnNUywBqQXQniaRwqVa5UbWoo6pe3szGSozuXt_ScwVE_biAZZmt0TWLGU00zAyUBRi12Do3EDWkS_568FfS62xqEBKiKzXIKEwewztkcClqbqmLSklX-2f16dPmSv_qbGM8PV_PLagCUQmIwQTCaLRgSWmoRPyocyI7VUL1ePr0lt7Wnt63Bt-j2maQBBQkuhshFErNUfSggT1EEjSj5BiNav95b6-77j8HvDsa6K8iZWstGylBVD6B6YxHNknImoZLUEudMLWx2l_K6mnl_fLy6mI0oeMuOwcF2qBVqTM6WjI8lEF-mBgCB0dCZKkp-pdjGTVqmxFT0VlWCukEjn4njkTkjnOfikMdma711OUvfeKhexDDmlkJ3kH4400bHRge6KNBwSwlV3zt7v51p44b1_1xnRzHK0qkF3UDtiDewOui7NQ8MC-ShfCFxIi52lZXp_sHr8u3K4vj546nl-MfqUbawsO1IhZgo1D9nFSIEzCHsaU67iyv9tbf3z_JJdAUzahYUO9cTVUsQcptTDOj5LfWBaedMuAANKmWGsgWcxDWPkZl-3cRBRbuDxkdkE3Co1Bg1O7On65Ur7vpVndGPfiieyFBlaiqGF_lgOTC2WqNHa721UsUW35kVX9nKpwKHq0EQhjaIOA5vrp8Xtm7O748XV2Er1uwv1UqkhRMFTh-El0J6IrT1cFSZ22zx-5e1i9GMoN_QUEPyqJiIy7hhcAB-NlSn10PztbCcl4gV-XsbGozSk9RG72a-M1t-CELw2g0BsKidBpbHZj7-n51K60Mb6d-9ycPeuGmeFC0UiaJ0b-g4g8PUr1URJUeg4YXhCaW9fFzhy2X54vR6H7FvjCwCRZZzQ2sqgCaV_fLj7q_v3HuD15GE6y-oJZzBWejYe0dftei5lZLYW-3LG0NL3sn42Aws7CYaKH-woovBYWxhTgXChoNg4cfdgjI14uV5ds9f_XGR0VrJtJD1s2JhC5rQSZV2-gKQxyORBmSUAbJEBo2Cq2IgKvua_9qceXt9cWM5_rLYEDoqChShqBzYPgmQrUkkJZU1mbfYAxyU_Wa3av1ww2zvrI4euuvcvlDuuNVpgT5tygB62WOuSQ1BYpR0McJwoLxrKUutkD22uqqBN7du2efZuN7KEhtJKc3w-QidiwKQrVx2IfgiJG_d0bQQOlmUKow_QZS1EgIXmsDLR7cdG_f13sPfVTGUZe-WG8a6pRAME5DVcV_F0BkWlDIHaE5Is1YU-k16zprF-L9leLW_M50VWfdQJKyYGJDGhfFC9QDr4d6IOEdCgTk1MoHTcWYqVRTS14cZzXYelxsk4aIszzCccDvgMmr7vXd4_2tPNo143z5srZcSC98YLCToFKTUXUizCbX0cOZat1g0A6vX5eeO49vV6djIvuS9CCabFEB4JaoPkaFasdLZA4B6HPJBnavWltz_cMdfnTw1hnn029HzYvKnEmYHjyWww1I1TAB7dq4gk6Lutqp3Vnn3O7Ys5PvPaak8pRXiDsviWqr_eH63cfNxVDdD74zooUrdFCVQXsEmYVx9xWE-Jn1O_H6bhzNbjyEiCRKWMlKJhWKycW7NJY1xRLjwRCVurq6YutrTw95-W4cZ18qzcGwQUNnlp1FKYPcJ-OsGB7rOMRLwe9WOyv9fRu3Fveu_bjI_C6hmHSVFVROopUoCceZ4Y0gvQXksy0wFtVeb19v3b4-nfS_MnD83GBRylATDOoDnILB-1UH78dxLYl-LuMuflXbAGcm4UE54ko4DVVgq_eTu83N46PF5wf_ncMjj-R4OBQeOgP9A91VN6jsoVgZrYhc879m9YvNYklR1hq2N5J_NhrNLKRBA6dn4XGaJMyUIBAT7YQWQsGMMJWg1LQuDgMIEZMFFIjDC9ZFTgmRb1yUIJlq6GQmuaWFkoRRDJiQJJV09DIN-vxdd41mfhwkiHH8Ax2REe4QE6Q40V9oGiFicA2Ehazix4UfDs_x2-O2YtznXEuVuIAASg5JKxLpF-OYigbNoH9AWtWwL6-37oQbXg2-V4mCqSPdxgTohLgX3QWz0B_IYEgrbZu_Zv4r4mqLQSlNZrJAN2naAghCewZJzVPKUUTYj9CoJff21FUH-fv7ImGjh_tiLlsST5bcEx5uUpZJwqM7Eaqme3y899gfnp98F0-gKChhTmuKHkMBBccSLTNYmjkPtcuL_atcuK9lBmuyR9Kjo5G8QARZJFoZVk1EKXCmaeyUJBeT9cgG_jIZ-FNVkCm6oBxECYLMnCdXY9SDLlPmeiQdxn1uvGmgbw3jpcZQIbbBNBoqG6Fc6wxtB_W1GQ8Hp4vqpuzcjsvUl9E0OtbgJRYtlccaQjUYn0FwhcuS4O2lraBz-m_xMD2r_sKoqi6gXW60gSDNNbJHJ4jyWCT0KXnyqBqXlZoi1XE7PNAWuEvMZiqa1tBB5AhBmqWUfe2KbVKsPtYXzWo8X3_eXfzzQFvXXhVkqqD4N2CgCH-G8UrCweLWjjfV7slT7H6sn3RuTibtGuUS6o00GBedQV-e1iBSI3mdC8R9QCwc597p8h1fOuj-aRcE2BemMNYKpjDSigXMJygTbJshRBEMVUhnbmfjeXnzY9LPaIola2QUBYFFfYvWFxQQCHJ4_ghjWjFzPxgu97b3NifPQ6giMg2DngQn0ZoDKKywJlhYwewDCuQUr_wZ0CJ9XaMmWS5AKvCrDJyMiWmKs6kuPmVXvV9uW3v_cf8I9__7gQXcA9nJ6ugwoGq0yA-boRQsNqZQN1ZU3ZvXznmpX1_eJzMP3ZMCAs1HhXZSIMpRWRjncCqNTpDHrjr46PRyJ63Y3T_PgzCHpMDgWQ67AZVttKge1vWtPV49Pa99G84FcP4cuIBuz8ZB2Bv0SgdSKg4uVVVy9_G1s_UZ35YP2nDaOD4bh9oiKXYtaqnGzDBURot6UGdZsoRxK9WevTw_qLeWN5f993bwbvBCcE8K8wtqrM66_HLvPK2kpds2nEfFnI2ztGkCFc4haoOi-lEN1p5vPjbuV_ngpBUHszUXLmCcZuKC8jZglOAmIL5hIVX1cYhRTd3zR7iPNpyDRJ8DpyAiZ-NyEk0DdgXXIV6TAjMXQdtTLiWf4a9dtfvQ3X7YvXi9cX8S6-dqGCZWTq2G_U4kASUrQPsoWsGCI2CefXW2LdL54btaHkwC-ScO0msunJdtv-cxPBqDAIutYCuRGMt-vThUufedfgvOwALyeXASbnI2DlkDWPAYEYSjJMvpDpduruLqoqlv23DQ-qEFB9vaQAqBxUEM0CqQhxYMDXrwNewqj5XaeencxqHseT1pB5uBmgvDpBEFFkPGK54_P8987_H0sNuGkzCo8-Dg6f1snPUcrMEV_JwSMBEBHpIfHq3tn30cnW604UDjYTYu1qjEjkkpG1rl9bTck5jhSTUQpzYFU62tLz0vvW-sHJ7mP-0kR-ySpw_aIp0kwm7Tl41me-lhWE_C5OdajYXg-75W8yeOfyzUoP9haqGmFQiR2AKUcIDwXZLTEQoPIYiS7Zk1xJJJNk321edNvll_WFo5uP_WZTLBwoGZHWqftQiiqv969_B0Z0-7UrfhnHdyHlyAQpqNm15-ErSm_H35afJi00B6zTagw7t6hVnCf53A36vX1_PTztphsXu33548hVPEDfPgjAwtuOBRUhQ0jue0NgDluqXPlNnZ8vnxpA1nlfXz4JwVbjbOgLzIfyotqb6C5Ko3wy8GW-xycNuKsyC8eXD4OdOCo7VARSsZVkhaGAzVUi3icre7tVguWnF45RYcHsUNbKSBUPDA-8qkRf3Q2_0YdE7acLSmNBcO0rkFBydAK5vCBFrIN0JWvb2lYX_9ZhjkSxsOBGDmwVntWnFIUhhgA1ygiHbVzsD2yuaiO93UbbhAtenfOMwul7NxzqBPilahvENhQuGpbvfWd83Q-fh9PqZxKJF6HpxCIrXgHHIC1tIgvCwEHMblej2xtVq8nx_1Z-McxyiqeXCSNrlm47xX0Cuo7CqQZAmy4hu7W58rx-Jy2G3DwXjyeXC0otaCCwY8ah1inlMCQ_Q9vKwvhafeVrIHbTjDtZ0HZ0kczcQFkIak40PwQKjtmUW0hefToi4j7aWn9lD_EKfiNnjDFSoc_uGGCOLkOD9-XLhzfTMJ3B84a0Fgc-A8EcRM3NSugkciyKldhUkHp4EwCKYFOL334FGKp_YeWoBWQBW1AT2UioGy4HAeiCIE-dnB2uON3l5bftmZvMs0DqTj5sGhi3YeHOSNacHhNQPMNZIBEsgQee69H_c3y16ns92Oo_I9B4605GycqrnSmYmsacFW0coch5rkYPwmu1rDYcmbpd67vHy7Ed_akV2ESuMBckairkOopuHn-tbSxuXFpW7FBTkPDiyJGJqN89JAQIAjwVbCwbdVJx3T33u-Xt9nG204b4WeBwfh7dtwiDVlYG4oIwyUc3V99Xnhd7jMXrfhLBWFOXBQJXY2bnprDWHrprbWJgE-DQzWyjagkdCpGG7YXifx76463ly2R4sfO2G7_-3JUzhJMzcHDprDtuCCppUIiXqAIg2Ppqq7ZrAq707O1hd5C44Kv52NCxK1ypB9l1S18NbVuyump9XT6d1JG47OUc2DQ0FSLThIUu7JaMI90l6ArZ53lp47b5s79UmnFQftNAcOtA3WnoXT3BrQJyiZO9qIFNxX7ODzSfQuP_Y-eRtOQ0zMxtHBFo_MQMYFjsLvRNU1y92zw4-T5U_fhoOetPPgyMfNxlGMBko3bUZb51JWLz6c1Hso7N_WIH7gYJjMPDhD1WwmbnozWdCBj--byX8S5Oeuc4DOaQEaQ64X6gmvQd7PVfb1-GVveXn16eHk25OncKMtvjlwMHFtv-eRILTdaS1eWzqYziV1e32lLjrXl502HMZJz8YZ2mMDRNI-pKHTENXt5-C-u7Zf-vyiFYe_zIOjAjQbB6-Ddx0tqEHlgwmrvc7l-e6-31ds0AZDdZgDZqHhW2AYCU4nlRS0vTKodNXG-k458LsdPzxpwxG_zYVD5W3BTZ29ooWyqbNXk6j6AXTgjXmAChzdAvSWKjSSA6JXYozw6OvVh_72zll_cWMiPH_ivPJz4ZDtLbigYXqhfrxzlsodGPAmfX6-qfxyO2jDkXKfB2ekFrNxIAHHwUYIQpi3QGd59_hHj5-WwfnBRgsO7wKNMAdOCmNm4pA58J6AYMrQBELYVIOn_ur-Z0-sNb4VB_aaA-dI7c3GCfQM5T9QxQRpwVdsPgnxdlKay7vfw8L_wjml5sChExiWFpwToHrYFZQFAZpBnouT9dXFfHE_WOx86x8qm7fkebyBs4Wqrm7s67DsNW95l7fiAp2a-DcO8eJn46QuPkSmJG3FCjrMymvFFK1uc7qLBCXwefN4vlw_rG7wxW8v9vPQDx1E_3boh2Cjcx5_I-ElfyJn_yT0-FxAKXkbcOqEJpmVqROabUDIXNUChA4WXBKNIllhjUdXXuqDpWFYlOuThbKfOKLQOXBgKdWCC5LcOBQhZl2TF6j44dHg4_zenO31v-Mm50wVXaCSU-dMv73I1IFUWhBrAWqOMFeKbmTQQX4Lay1Wz48f9tdu2MqEUX7gLFXm2TgJI-j0SEZSbfG-eri7-9zr2c3Po4tWnMQI_htnBUXNPDgFRp6Jo3NLliAwy0gPOpc0M2OncVRWZ-McRZehE3QW6eQUNNqu3Y97T5d3m8-8DQfn7-fB0dG8Fhy5fe5JchkPDsJzn057D_ppc3X_9KQFh7lDZZkHZxWfjfOSds6kol0f6GuoxEpvP-3lRb6ha96KwxzPg_O03TEHDnNi58DRMR7eglOQD7Ak6BsEs0G7yq9cLQ127gdPh4M2nMOf8-DgAtpw309IEs1NnZCc5OUUDt5dtuACt6P1JKXpDy6hXNe6W3zxJh_0PydK5Mdxy0Bc-f0I5Z8fhMyjQk8rNnQaik6qVicXgwe74y_Ojm6__eAPnLVz4eD1W3A6wHiG0dkVRGOgYyRvx893vWOhrv03nCGhDJGJHPVidOXveVVdDM7u7pbV4gRHO7xwBk7w0VIOSnRVr971rz9uO0-y347De8yBo42e2Tg6IeXpvleQgjbUramuXnwnDM878Yq34aBu9Bw4D7mrWnAoMdGz2tHVPTO6gekC_rA2JiFTdKl62SrX7OZguzxP1nithr4mBQ8mNCS0EJHr_O25vtl8H175VhxtgM_EQbCR95DcoD4h8YWoOF_pP2_2Br2DnTacp_efA0fL2i04A0EMm4f8oyMFKAXV5slZE9fXTtffF1twhs72zoXDVM7GwQbYZJiMxjHNTUMHBTxrkijam9o0WU4d4ZokWiCedcS4JEtkCLJaOSv10evG897nhHF_4BQFwGycNcghuuQHjQPJKu3Mnd0fuNGR8jlwykPYzcJBATe21mx0X45ikMXgJUO-JJmtKKrE6jC-ncanJve7_Fs7qeBVMbiIJ1rmgqc46S_1m4bfPQ0vWnFS-rlwmosWHG3rSlAIiFUq2p6szK3b6Qz6H50l34ojbT8PjlYJZ-IkSRToO0PH_uGmnKzs5VXf7tsjJw7acCLouXCKxq8Fh85L1CRam0QfBW267Fwd3p91NrbacRZEPQcOdKhbcFaTLONwBAgmOudUdZe6O2sv55fy42I2js72Q-HNgaNDIrNxIEra0IEEhFrVSE9eFXv58DzcemPv38zbDyCtGs8HJK3QBrQYN0tVxJA8D7yyvZt6xdwfPS8PvndxgtOcW4iKOXAkbGbjSClCE9EQwTrRSkilzsPbsPbbr4ODNpyHxp0HN9qlmomzSAraoXYWvoCjOpjq4Xbv9IF1h-sXk2UB5-gGhdN0NB6ePlCKbL19Hj0Pr8Lbm27BCdrinwcnabmuBacgdoALZF4Q-Mtd9blWm8fOy8FMFK3gutkoImDdsMbSMbAgOEt0OcDUtUpQy9AjpXp733lRN7d3cn1SXzFAGEKNx0M7EJNqCK-7jf3l4WrRhzutOEzBPDgIOdOCs0hSTUtzo2tZHvSgOrGf4lPMj4M2HG0-zIODO-ezcZbKpXd0ZxPZCu_uzu2GfE5Lm1d6NspQ_P8TBWUy-7cC3ZmjSxkooZ6uprhqsP10d3v8yc82fAuMgnYOGMofnwlL3kVOF9uFsnTbLjDfCMt4Q3sojYSPEdXuR98fL72E4eqEnXJEuUj0WQZBx9aSQxhJxUAuqUSba5fDzPOstQ91bTLjImm6GuxYaLRndHU30aUcnW31cbNz79d39w86k-fVgc7UZ-YifT-EHpUaXxidmRCaFxVcqa7KWdCbH-bgbPJ-jWhGDwCJ0SXiRjPocvqOTUmczjfSJyxmHICm02UctZxOjjnoebqgs_vZe9m2L5ePx7wFBj7g_4YF1IbZvyZqONdSGJgF2rfBm0ahCws8alkraRvw0vPKwYr9OD-_2vij3aD2xzfxUJ208rQDVa3J86ezq8XbdL7TAoPNU3PAFOzObBgQPCZmck5M24YzeJ7ESrE55EJLtaFaXb3wQ75_sbL9J7F-XL5C-k9fvvpdhH7iHHTrbJyjk9cQrsph0GRD3_pIiUFPRGeLVSnHmcJVGqhQULgPtDpryRRUaTjwS2bnXq1N3vMHjPaQ_g1DkOmZMEhg40ZyHG8E-0VH5_62uT9hSKvZMC1zYzVrYkB0J4N8tKlAw6PimBIgXJvq3vIbtf30mDt_skIGWHw6wgA1gFBT6HN1NlivL_suvk_OWP6A4V_MHDAn4ZRmwmDtoP_JIWo6AwYd2h26vuqpw5fXxTYYbRr_E2bI1s6G5Vgrio7RhzsETyzIqJgTMeWsUnIxVlv3t8ebG93Vj83JPIXGZugK-nICoipyw1IIgdXBFKFjjqHIme2iqS3duAEtZtgopeiqOV38cSmFWiae6Ab9jR0uP25uNJPUT0ZHo2qWVaEv1pg0_hpMsHVOpm5UKbx6erMb60_HT7E3iYDaylhMpOsydOEHjaPnEnZZNk7XtEsuK9fs74mzt_7thBdlE6L1kTP4bfqSi6WLQg2Yp44Q_tpQXM26qPHjjiOn-2Lf7zj-Ti4IvdHtKU6HqSV9IktU72uXbD-9b3VPv_3cd1jgyqg5YJLOg82CTd-qtFzKqVuVfzr3A6ddaMGV2qOUsWglJgW1i0Ei0ZenBN3jg3yv5dSnkv40pCt14BM7Ep-Bdp2qnuju8bOD6zz8Uwx_wAzoYB6YEXomDLrQIkUFHbkWGprdVB-xx3rdq7Xn3dsWGAaAzwOjnbI5YJTUM2GSWzC1EmARQ7vInJ8-Xh28Hm0-8Nkg6f4NchIlbBZI4_VRWlBNoZDM6AJk7_ytt7db9098G4zOHc8B81qHmTDDU6TLyMnRSfa6ySyN1lLgfSPcbxPgy97ePz_0ysbH1Up_0o6uadI5AdQxVDpaWLy-7W9tyrt8snsygeH_oMuPytZU55xknhZovEzoWKhjo5pZN4-UibZuBJI806cnGiFYVCUxbnOuEd4iNLHq9d8els3TSqonz4Mlp1VMTTIdZpGOP-02-rRWdw_LE1s-DTOcLp__GwYSkS2wVAreiusI7k3QpBHjxhoOcyJjnelrOTNW_-goqaLda-gWRXtVxlfbxxu7z7TX0NUtMNpLmwcG-zoT5uETJYUzHatE9AhevXrbvB2ljZuNQStMzgMzmr5wNgOWyM6GhhVdRp_loK-B1HQzz0dlgkdJ1DNHKNVaY-LB8PRJDhQUFuijPnQrVLqIoFKy-tg7v-bq-HV9509BUw1veKaLiiqMvuVDmhSlLRmXHRyPlFJUh51hfXu0vhKvNybtap1Q81CTUqYrknSRGz4jkkrwpjEwAdW9GR73bi6Obtkfoa_pkoDwUMzQEiSpMFpK7aqtXJ99bN-2wGhpcw6Yp-9ezoJJTLXlnHukoBjdYqu6172X-vN9pXO40QLzdE7t3zAIODMTpujEplVMyIay09FVQl4wkynRhUDMS10Nt8L7QzjfOPpzVeWX1nQqTBmr8QBu6EOcw5t787702XtY6s5GWbJ__0Q5C8s5EwWJXYxgfvTFHWdpLgNncJhNaWgHHKO_vHq41O0dXN3d8Ek7-jYZ5CBYAWEJpQZLru3nYH_vgbHcArO0IDYHzGnXAvNw_5DzdKJW09JPdXN5en5h3cbQTUZfQyM7ulAeyDZAl7GYMA8ZGkqHnOnLm9WxYnsfN1dnmf_ZKNW0pYNyQJ8FgQal1YTq46LeEqvmxD_ttMDglNy_YY7TxZKZsEhfTKWPokV01nLkX0MfXAoN7e7if5Sl2npbTodqf2d38w-Ha_qIFeZX0VfKAgSEE9Xqyb7vnx-esrtOC8wH6Px_wqD9pG2B4W0Rlo4OdtBhnFA9rx4uds6Zua1zC8zb4GfCHH3iU9EtMkkHfBEbl_LpNYu3i85pdzZKc6T5P1GGtsJnoYLKlq4hF08uHFMDktSK2SLojqekU6Wz7j7rUNeWvtGmyH5iyizzBgGmVOFwEda5GCqeHg9776y-3f4zSUfX_cHNQ_e_1_7jf_CO_z3XL293ry-__h9QSwcIeX8zunYjAABDWAAAUEsDBBQACAgIABKoWVEAAAAAAAAAAAAAAAAOAAAAQ2hhcnQgZGF0YS5jc3almc9O3EAMxu88BQ-wsxp7_l9pV71QoUpV1R4zSRZVRZUKCy08fUMjEc-hmrV94YK_jMfft_6R5f1wmnfvhvvp34_L0zw8zPeX49338cfDBVq0xhaDaecygEO0KWGxPgH4sP_45ZAt_v7z-Hi7w604d4vtVly6xfBW7Oy5T4alHs7t-bUYz23jtdhx2vCcJwfOkyOnuO-g24r7DqatuO9geCuGvoPbNKDvYNyK-w5u0wCOg9B3kBT3HSQX7DtIivsOkuK-g6S47-B2QeR8BrHv4NYGchxEjoN4toPrrovjUI-51OWTXqLxNQ2mFEgmVkhzmPLoAfZ3Nzfml_n09O35sINm-7Hlnq5DtjrR_Sg9e12YbHWgG5StjnSlstWO7ljNvYN45usW1pwtCVuhi5otL3RzK9QgCFuku10xNhCErdDtr-lcELZM-cBWIwWG5t6CsGWKFI1akDVwlDp8ecMhvrwhk6p5Qd6goZc0rivOcsqjy8diQgyD8SHOptq6_HacMOQ4uymE_eHrVXx5Gh-v40j-4l5oxlY3NGOrHaUZW42UZho18tWW0kw685Vmms6DSh1VnQuy5inMNGpB1pDCTKMWZK2BmSJrIMha826j6VyVNRBkLVGYac4WZM1RmCnORlXWULXXUJA1pCBTbAeU77WVYyXgMXiczGCXx_k6HU2xYzAzBpizg1rGsD99vjU_r1-e6wdLKZj56kI5xlYHyjFp5yvH2GpHOaY524nvvXJMow58NTRfjvHlzXuZpndB2mjvgrhlijK2OlGU8VunKFOMDQRxQ4oyjVoQt0hRxlZ7ijLN1ARha1CmSAsKsgYUZYqZoyBriaJMMTUUZM1RlM1xxGrzgr8Zq_EwZZOrOxrnhzQN7gghuP_gZEEZW50oyhTqBWVsdaEok957RRlb7SnKNGrPV0eKMraasigK5IWijC1v_hXEVmdKMsXUQZA2MjcQxK1BmcJyEMQtUJQpLANB3BJFmaZzVdhAELYGZXy_gbJMcTgKwuYpyzRqQdia1zK2Gi_-AlBLBwhChvBqCAMAADcgAABQSwMEFAAICAgAEqhZUQAAAAAAAAAAAAAAAAoAAABUb3RhbHMuY3N2VdBBDoMwDATAe1_BAxYp3jhAzuUjiHKo2hPwf9WoEnaOkzirjefl3PBc9ld3bsux7d36fa-f48HE1Kfac4TSNUGzqyKXWzmB419iBwJWF-_JSxmkS5u7gpJcA0qYtC4hc0IJ7yrUJQl5cEkj6-IpYl0ml8bWUhoNUP-fjMjeU2wvQdbFM9nshRJ7kvc-L1mXcKdX5g9QSwcI3vFKmpUAAACgAQAAUEsBAhQAFAAICAgAEqhZUXl_M7p2IwAAQ1gAAA4AAAAAAAAAAAAAAAAAAAAAAFRhYmxlIGRhdGEuY3N2UEsBAhQAFAAICAgAEqhZUUKG8GoIAwAANyAAAA4AAAAAAAAAAAAAAAAAsiMAAENoYXJ0IGRhdGEuY3N2UEsBAhQAFAAICAgAEqhZUd7xSpqVAAAAoAEAAAoAAAAAAAAAAAAAAAAA9iYAAFRvdGFscy5jc3ZQSwUGAAAAAAMAAwCwAAAAwycAAAAA'
decode(string, 'none')