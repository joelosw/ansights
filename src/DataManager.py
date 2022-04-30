import requests


def get_data(film_id:str,image_id:str, debug=False):
    check_local = False
    data = None

    if check_local:
        data=None
        print('Data exists locally')
    else:
        url = f'https://digi.bib.uni-mannheim.de/periodika/reichsanzeiger/ocr/film/tesseract-4.0.0-20181201/{film_id}/{image_id}.hocr'
        r = requests.get(url, allow_redirects=True)
        if debug:
            print(r.content)
        data=r.content

    return data
    
#get_data(film_id='001-7920', image_id='0005')