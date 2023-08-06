# scene_cutter
[![](https://img.shields.io/badge/python-3.4+-blue.svg)](https://www.python.org/downloads/)
[![PyPI downloads/month](https://img.shields.io/pypi/dm/scene_cutter?logo=pypi&logoColor=white)](https://pypi.python.org/pypi/scene_cutter)

## Installation

`pip install scene_cutter` or 
`pip3 install scene_cutter`

## Requirements
````bash
`pip install ffmpeg`
`pip install kcu`
````

or
````bash
`pip3 install ffmpeg`
`pip3 install kcu`
````

## Usecase

````python
from scene_cutter import create_scenes
scene_paths = create_scenes(input_path, output_folder_path)
````

#### Optional parameters:

 `threshold` - the scene change detection score values are between [0-1].
 
 `min_scene_duration` - default is 1.5 sec
 
 `max_scene_duration` - default is 30 sec
 
 `debug` - default is False

## Note

In the __create_scene function you can replace `'out' -async 1` with `-c copy 'out' -avoid_negative_ts make_zero` if you don't want to reencode the videos, however frames at the beginning and end of the trimmed clip can get messy this way. 
