# -*- coding: utf-8 -*-

PDF = ["pdf"]
ADOBE = PDF + [".ps"]
OFFICE = ["ppt", "pptx", "doc", "docx"]
MEDIA = ["mp4", "bittorrent", "mp3"]
DOCS = PDF + OFFICE


def filt_by_filetype(filetypes, value):
    """
    filt the urls of filetypes
    """
    for ftype in filetypes:
        if value.endswith(ftype):
            return True
    return False


def filt_by_pdf(value):
    """
    filt the urls of pdf file
    value:
        url
    If the value matches, return True, else return False
    """
    return filt_by_filetype(PDF, value)

def filt_by_domain(domain, value):
    """
    filt the url by domain name
    """
    if domain in value:
        return True
    else:
        return False

def filt_opentrain(value):
    """
    filt the url for opentraining
    """
    return filt_by_domain("http://opensecuritytraining.info", value)
