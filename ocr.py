import pytesseract
import cv2
import re


def ocr_with_gray_filter(im, threshold=160):
    try:
        #print(f'Tentando abrir a imagem em {im}')
        try:
            captcha_image = cv2.imread(im)
        except Exception as e:
            print(f'Erro ao ler imagem {im}: {str(e)}')

        # Converter a imagem para escala de cinza
        gray_image = cv2.cvtColor(captcha_image, cv2.COLOR_BGR2GRAY)

        # Aplicar um limiar para manter apenas o tom de cinza
        _, binary_image = cv2.threshold(gray_image, threshold, 255, cv2.THRESH_BINARY)

        # Usar pytesseract para realizar OCR na imagem em tons de cinza
        captcha_text = pytesseract.image_to_string(binary_image, config='--psm 6')
        #print(f'Texto do Captcha {im}:', captcha_text)
        # Filtrar apenas letras e números usando expressão regular
        captcha_text_filtered = re.sub(r'[^a-zA-Z0-9]', '', captcha_text)
        return captcha_text_filtered
    except Exception as e:
        print(f'Erro ao processar a imagem {im}: {str(e)}')
        return None


if __name__ == '__main__':
    image_path = 'img.png'
    best_captcha_text = None
    best_threshold = None
    best_score = float('inf')

    for threshold in range(80, 256, 5):
        captcha_text = ocr_with_gray_filter(image_path, threshold)
        if captcha_text and len(captcha_text) == 5:
            # Calcula uma pontuação com base na diferença entre o valor atual e "hjqy"
            score = sum(1 for a, b in zip(captcha_text, 'hjqy') if a != b)

            if score < best_score:
                best_score = score
                best_captcha_text = captcha_text
                best_threshold = threshold

    if best_captcha_text:
        print(f'Melhor Threshold: {best_threshold}, Melhor Captcha Text: {best_captcha_text}')
    else:
        print('Nenhum valor de 4 letras encontrado.')
