import base58
import binascii
import datetime
import datetime as dt
import ecdsa
import hashlib
import multiprocessing
import os
import time
from multiprocessing import cpu_count

import pandas as pd
from rich.console import Console

console = Console()


def ripemd160(x):
    d = hashlib.new('ripemd160')
    d.update(x)
    return d


r = 0


def seek(r, df_handler):
    global num_threads
    LOG_EVERY_N = 1000
    start_time = dt.datetime.today().timestamp()
    i = 0
    console.clear()
    console.print("Core " + str(
        r) + " [gold1]For Generated[/][red1] & [/][gold1]Searching Private Key...[[/][b white on green]READY[/][gold1]][/]")
    while True:
        i += 1
        # generate private key , uncompressed WIF starts with "5"
        priv_key = os.urandom(32)
        fullkey = '80' + binascii.hexlify(priv_key).decode()
        sha256a = hashlib.sha256(binascii.unhexlify(fullkey)).hexdigest()
        sha256b = hashlib.sha256(binascii.unhexlify(sha256a)).hexdigest()
        WIF = base58.b58encode(binascii.unhexlify(fullkey + sha256b[:8]))

        # get public key , uncompressed address starts with "1"
        sk = ecdsa.SigningKey.from_string(priv_key, curve=ecdsa.SECP256k1)
        vk = sk.get_verifying_key()
        publ_key = '04' + binascii.hexlify(vk.to_string()).decode()
        hash160 = ripemd160(hashlib.sha256(binascii.unhexlify(publ_key)).digest()).digest()
        publ_addr_a = b"\x00" + hash160
        checksum = hashlib.sha256(hashlib.sha256(publ_addr_a).digest()).digest()[:4]
        publ_addr_b = base58.b58encode(publ_addr_a + checksum)
        priv = WIF.decode()
        pub = publ_addr_b.decode()
        time_diff = dt.datetime.today().timestamp() - start_time
        ntimx = datetime.datetime.now()

        if int(i % LOG_EVERY_N) == 0:
            console.print('[gold1]~ Mmdrza.Com:[/][red1][[/][gold1 on grey7]' + str(
                ntimx.strftime('%H:%M:%S')) + '[/][red1]][/]' + ' [b green]Total Key Genrated [/][cyan]' + str(
                i) + '[/][green] With Core :[/][cyan]' + str(
                r) + '[/][green] K/s = [/][white on grey7]' + str(i / time_diff)[0:12])


        pub = pub + '\n'
        filename = 'btc.txt'
        with open(filename) as f:
            for line in f:
                if pub in line:
                    msg = "\nPublic: " + str(pub) + " ---- Private: " + str(priv) + "  ~{MMDRZA.COM}"
                    text = msg
                    print(text)
                    with open('WinnerWallets.txt', 'a') as f:
                        f.write('\nAddress: ' + str(pub))
                        f.write('\nPrivate Key : ' + str(priv))
                        f.write(
                            '\n---------------------------------[ M M D R Z A . C o M ]---------------------------------')
                        f.close()
                    time.sleep(0.1)
                    print('WINNER WINNER!!! ---- [MMDRZA.CoM] ' + dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                          pub, priv)
                    break


contador = 0
if __name__ == '__main__':
    jobs = []
    df_handler = pd.read_csv(open('btc.csv', 'r'))
    cor = cpu_count()
    cores = int(input('[*] How Many Cores Do You Want to Use (Available Core: ' + str(cor) + '): '))
    for r in range(cores):
        p = multiprocessing.Process(target=seek, args=(r, df_handler))
        jobs.append(p)
        p.start()
