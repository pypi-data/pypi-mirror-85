import zipfile

def extract_zip(input_zip):
    input_zip=zipfile.ZipFile(input_zip)
    return {name: input_zip.read(name) for name in input_zip.namelist()}

def is_float(number) -> bool:
    try:
        float(number)
        return True
    except ValueError:
        return False