def extract_text_and_get_list(elements):
    t = []
    for e in elements:
        t.append(e.css('::text').extract_first())
    return t

def strip_crlf(txt):
    return txt.replace('\r', '').replace('\t', '').replace('\n', '')