import env
from ftplib import FTP
import os


def enviarArquivosFtp():
    print('Subindo arquivos no FTP')
    ftp = FTP(env.FTP_SERVER)
    ftp.login(user=env.FTP_USERNAME, passwd=env.FTP_PASSWORD)
    ftp.cwd('secretariaFazenda')
    ftp.cwd('cadesp')

    if 'arquivos-fazenda' not in ftp.nlst():
        ftp.mkd('arquivos-fazenda')

    ftp.cwd('arquivos-fazenda')

    files = os.listdir(env.DESTINATION_DIR)

    for file in files:
        print('Enviando arquivo: ' + file)
        with open(env.DESTINATION_DIR + file, 'rb') as f:
            ftp.storbinary('STOR ' + file, f)

    ftp.quit()

    print('Arquivos enviados ao FTP com sucesso!')
