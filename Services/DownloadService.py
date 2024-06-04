import time
import os
import env
from Services.OcrService import ocrService
from playwright.sync_api import sync_playwright


def download(status):
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            timeout=100000
        )

        page = browser.new_page()

        page.goto(env.URL_CADESP)

        page.wait_for_selector("#ctl00_conteudoPaginaPlaceHolder_LinkButton4").click()

        hash_value = page.url.split('/')[3]
        ocr = ocrService(f"{env.URL_CADESP}/{hash_value}/imagemDinamica.aspx")
        text_image = ocr.getText()

        ocrValidate = ocrService(f"{env.URL_CADESP}/{hash_value}/imagemDinamica.aspx")
        textImageValidate = ocrValidate.getText()

        if text_image.strip() != textImageValidate.strip():
            print('Texto da imagem de segurança não confere. Rode o script novamente.')
            print(f'Texto da imagem: {text_image.strip()}')
            print(f'Texto da imagem validado: {textImageValidate.strip()}')
            browser.close()
            return False

        page.fill("#ctl00_conteudoPaginaPlaceHolder_imagemDinamicaTextBox", text_image)

        with page.expect_download() as download_info:
            if status == 'ativo':
                page.click("#ctl00_conteudoPaginaPlaceHolder_contribuintesAtivosLinkButton")
            elif status == 'inativo':
                page.click("#ctl00_conteudoPaginaPlaceHolder_contribuintesNaoAtivosLinkButton")

        if page.get_by_text('O texto digitado não confere com a imagem de segurança.').is_visible():
            print('O texto digitado não confere com a imagem de segurança. Rode o script novamente.')
            browser.close()
            return False

        download = download_info.value
        download.save_as(env.OUTPUT_DIR + download.suggested_filename)

        print('Download concluído.')
        return True
