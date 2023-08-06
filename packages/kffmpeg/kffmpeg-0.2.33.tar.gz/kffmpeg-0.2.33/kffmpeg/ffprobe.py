from typing import List, Optional

from kcu import sh, kpath

def get_duration(video_path: str) -> float:
    res = sh.sh(
        'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 ' + sh.path(video_path)
    )

    try:
        return float(res.strip())
    except:
        return 0

def get_folder_video_duration(folder_path: str, allowed_extensions: List[str] = ['mp4']) -> float:
    total = 0

    for video_path in kpath.file_paths_from_folder(folder_path, allowed_extensions=allowed_extensions):
        total += get_duration(video_path)
    
    return total

def has_only_silence(path: str) -> bool:
    return '2 kb/s (default)' in __audio_data(path)

def has_video(path: str) -> bool:
    return len(
        sh.sh(
            'ffprobe -i ' + sh.path(path) + ' -show_streams -select_streams v -loglevel error'
        ).strip()
    ) > 0

def has_audio(path: str) -> bool:
    return len(__audio_data(path)) > 0

def video_resolution(
    path: str
) -> (Optional[float], Optional[float]):
    res = sh.sh(
        'ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=s=x:p=0 ' + sh.path(path)
    ).strip()

    try:
        comps = res.split('x')

        if len(comps) == 2:
            return float(comps[0]), float(comps[1])
    except:
        pass

    return None, None

def __audio_data(path: str) -> str:
    return sh.sh(
        'ffprobe -i ' + sh.path(path) + ' -show_streams 2>&1 | grep \'Stream #0:1\''
    ).strip()