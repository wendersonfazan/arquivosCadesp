import env
from Services import DownloadService, FtpService
import zipfile
import os
import sys


def baixarArquivo(status):
    while True:
        resultado = DownloadService.download(status)
        if resultado:
            break
        else:
            continue

    for filename in os.listdir(env.OUTPUT_DIR):
        filepath = os.path.join(env.OUTPUT_DIR, filename)

        with zipfile.ZipFile(filepath, 'r') as zip_ref:
            zip_ref.extractall(env.DESTINATION_DIR)

        os.remove(filepath)
        break

    FtpService.enviarArquivosFtp()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Informe o status')
        sys.exit(1)

    status = sys.argv[1]

    if status.lower() not in ['ativo', 'inativo']:
        print('O Status precisa ser ativo ou inativo')
        sys.exit(1)

    baixarArquivo(status.lower())

    print('Arquivos baixado e enviados ao FTP com sucesso!')
