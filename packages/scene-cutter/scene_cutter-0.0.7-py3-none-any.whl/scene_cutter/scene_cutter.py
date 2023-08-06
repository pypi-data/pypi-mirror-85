import os
from typing import Optional, List

from kcu import sh, kpath

def create_scenes(
    in_path: str, 
    output_folder_path: str, 
    threshold: float=0.5, 
    min_scene_duration: float=1.5, 
    max_scene_duration: float=30,
    debug: bool=False
) -> Optional[List[str]]:
    sh.rmrf(output_folder_path)
    os.makedirs(output_folder_path, exist_ok=True)
    timestamps_path = os.path.join(output_folder_path, 'timestamps')
    scene_paths = []

    if __create_timestamp_file(in_path, timestamps_path, threshold=threshold, debug=debug):
        timestamps = __get_timestamps_from_file(timestamps_path)

        if timestamps:
            timestamps.insert(0, 0)

            for index, start_ts in enumerate(timestamps[:-1]):
                start_ts += 0.05
                duration = timestamps[index+1] - start_ts -0.05

                if duration < min_scene_duration or duration > max_scene_duration:
                    continue

                scene_path = os.path.join(output_folder_path, str(index) + 'video.mp4')
                __create_scene(in_path, scene_path, start_ts, duration, debug=debug)
                scene_paths.append(scene_path)

            os.remove(timestamps_path)
            return scene_paths

    return None

# Threshold - the scene change detection score values are between [0-1].

# PRIVATE METHODS
def __create_timestamp_file(in_path: str, out_path: str, threshold: float, debug: bool=False) -> bool:
    sh.sh(
        'ffmpeg -y -i {} -filter:v "select=\'gt(scene,{})\',showinfo" -f null - 2> {}'.format(in_path, threshold, out_path),
        debug=debug
    )

    return os.path.exists(out_path)

def __get_timestamps_from_file(in_path: str) -> Optional[List[float]]:
    with open(in_path, 'r') as file:
        video_data = file.read().replace('\n', '')

    return [float(x.split(' ')[0]) for x in video_data.split('pts_time:')[1:]]

def __create_scene(in_path: str, out_path: str, start_ts: str, duration: str, debug: bool=False) -> bool:
    sh.sh(
        'ffmpeg -y -ss {} -t {} -i {} {} -async 1'.format(start_ts, duration, in_path, out_path), 
        debug=debug
    )

    return os.path.exists(out_path)