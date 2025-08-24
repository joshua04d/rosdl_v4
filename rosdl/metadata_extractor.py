# rosdl/core/metadata_extractor.py
import os, sys, datetime

try:
    import magic
except ImportError:
    magic = None
try:
    from PyPDF2 import PdfReader
except ImportError:
    PdfReader = None
try:
    from PIL import Image, ExifTags
except ImportError:
    Image, ExifTags = None, {}
try:
    from mutagen import File as MutagenFile
except ImportError:
    MutagenFile = None


def fmt_time(ts): 
    return datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S") if ts else "N/A"

def get_ctime(path):
    if sys.platform.startswith("win"): return os.path.getctime(path)
    try:
        st = os.stat(path)
        return getattr(st, "st_birthtime", None)
    except: return None

def get_mime(path):
    if magic:
        try: return magic.from_file(path, mime=True)
        except: pass
    return {
        ".pdf":"application/pdf",".txt":"text/plain",".md":"text/markdown",
        ".jpg":"image/jpeg",".jpeg":"image/jpeg",".png":"image/png",".gif":"image/gif",
        ".bmp":"image/bmp",".csv":"text/csv",".mp3":"audio/mpeg",".wav":"audio/wav",".flac":"audio/flac"
    }.get(os.path.splitext(path)[1].lower(),"unknown")

def pdf_meta(path):
    if not PdfReader: return {}
    try:
        info = PdfReader(path).metadata
        return {k.strip("/").lower(): str(v) for k,v in info.items()}
    except: return {}

def img_exif(path):
    if not Image: return {}
    try:
        exif = Image.open(path)._getexif() or {}
        return {ExifTags.TAGS.get(k,k): str(v) for k,v in exif.items()}
    except: return {}

def audio_meta(path):
    if not MutagenFile: return {}
    try:
        a = MutagenFile(path)
        return {k: str(v) for k,v in (a.items() if a else {})}
    except: return {}

def extract(path):
    if not os.path.isfile(path): return None
    st = os.stat(path)
    meta = {
        "filepath": path,
        "size_bytes": st.st_size,
        "created": fmt_time(get_ctime(path)),
        "modified": fmt_time(st.st_mtime),
        "format": get_mime(path),
        "extension": os.path.splitext(path)[1].lower()
    }
    if meta["format"]=="application/pdf": meta.update(pdf_meta(path))
    elif meta["format"].startswith("image/"): meta["exif"]=img_exif(path)
    elif meta["format"].startswith("audio/"): meta["audio"]=audio_meta(path)
    return meta

def scan_folder(folder, recursive=True):
    metas=[]
    for r,_,fs in os.walk(folder):
        for f in fs:
            m=extract(os.path.join(r,f))
            if m: metas.append(m)
        if not recursive: break
    return metas

def build_report(metas):
    lines=[]
    for m in metas:
        lines.append(f"\nFile: {m['filepath']}")
        for k,v in m.items():
            if k!="filepath": lines.append(f"  {k}: {v}")
    return "\n".join(lines)

def ask_path(default_dir, default_name):
    print(f"\nLocation to save? ")
    p=input("Path: ").strip()
    return p if p else os.path.join(default_dir,default_name)

def export_report(metas, output=None, interactive=True):
    if not metas: return None
    d=os.path.dirname(metas[0]["filepath"])
    def_name="metadata_report.txt"
    path=output or (ask_path(d,def_name) if interactive else os.path.join(d,def_name))
    with open(path,"w",encoding="utf-8") as f: f.write(build_report(metas))
    return path

def extract_file(file_path, output=None, interactive=True):
    m=extract(file_path)
    return export_report([m], output, interactive)

def extract_folder(folder_path, output=None, recursive=True, interactive=True):
    metas=scan_folder(folder_path,recursive)
    return export_report(metas, output, interactive)
