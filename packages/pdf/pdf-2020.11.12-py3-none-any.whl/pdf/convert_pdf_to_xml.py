from disk import Path
from time import sleep
from .exceptions import ConversionError
from .extract_text import extract_text


def convert_pdf_to_xml(pdf_path, xml_path, num_tries=3):
    if isinstance(pdf_path, Path):
        pdf_path = pdf_path.path
    if isinstance(xml_path, Path):
        xml_path = xml_path.path

    for i in range(num_tries):
        try:
            extract_text(
                files=[pdf_path], debug=False, disable_caching=False, page_numbers=None, pagenos=None, maxpages=0,
                password='', rotation=0, no_laparams=False, detect_vertical=False, char_margin=2.0,
                word_margin=0.1, line_margin=0.5, boxes_flow=0.5, all_texts=True, outfile=xml_path,
                output_type='xml', # codec='utf-8',
                output_dir=None, layoutmode='normal', scale=1.0, strip_control=False
            )
            if Path(xml_path).exists():
                break
            else:
                sleep(2 ** i)
        except Exception as e:
            if i < 2:
                continue
            else:
                raise ConversionError(f'error converting "{pdf_path}" to xml: {e}')
    else:
        error_message = f'error converting "{pdf_path}" to xml'
        Path(xml_path).save(obj=error_message)
        raise ConversionError(error_message)
    return xml_path
