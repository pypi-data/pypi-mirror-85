import pdfminer
import pdfminer.layout
import pdfminer.high_level
import pdfminer.utils
import sys

OUTPUT_TYPES = (
    (".htm", "html"),
    (".html", "html"),
    (".xml", "xml"),
    (".tag", "tag")
)


def extract_text(
        files=None, outfile='-',
        no_laparams=False, all_texts=None, detect_vertical=None,
        word_margin=None, char_margin=None, line_margin=None,
        boxes_flow=None, output_type='text', # codec='utf-8',
        strip_control=False, maxpages=0, page_numbers=None,
        password="", scale=1.0, rotation=0, layoutmode='normal',
        output_dir=None, debug=False, disable_caching=False,
        **kwargs
):
    files = files or []
    if not files:
        raise ValueError("Must provide files to work upon!")

    # If any LAParams group arguments were passed,
    # create an LAParams object and
    # populate with given args. Otherwise, set it to None.
    if not no_laparams:
        laparams = pdfminer.layout.LAParams()
        params = ("all_texts", "detect_vertical", "word_margin", "char_margin", "line_margin", "boxes_flow")
        for param in params:
            paramv = locals().get(param, None)
            if paramv is not None:
                setattr(laparams, param, paramv)
    else:
        laparams = None

    if output_type == "text" and outfile != "-":
        for override, alttype in OUTPUT_TYPES:
            if outfile.endswith(override):
                output_type = alttype

    if outfile == "-":
        outfp = sys.stdout
        if outfp.encoding is not None:
            codec = 'utf-8'

        for fname in files:
            with open(fname, "rb") as fp:
                pdfminer.high_level.extract_text_to_fp(fp, **locals())
        return outfp

    else:
        with open(outfile, "wb") as outfp:
            for fname in files:
                with open(fname, "rb") as fp:
                    pdfminer.high_level.extract_text_to_fp(fp, **locals())
        return None
