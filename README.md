# NewGate Video Processor

Thanks to Jumpcutter for the algo! 

## Table of Contents

- [Gated Video Editor](#gated-video-editor)
  - [Table of Contents](#table-of-contents)
  - [Prerequisites](#prerequisites)
  - [Quick install](#quick-install)
  - [Standalone](#standalone)
  - [TOOLS](#tools)
  - [Installation](#installation)
  - [Usage](#usage)
  - [License](#license)

## Prerequisites

- Python 3.6+
- FFmpeg

## Quick install - Coming Soon

```pip3 install -r requirements.txt
```

## TOOLS

>python gate_engine.py --input_file Video.mp4

| Argument | Description |
| --- | --- |
| --input_file | The file you want to process as input. |
| --sounded_speed, default=999999 | The speed at which frames with sound should be played. Typically set to 1 (normal speed). |
| --frame_margin, default=1 | This variable determines the number of silent frames included on either side of sounded frames to provide context. It specifies how many frames adjacent to speech should be included. |

## Installation

1. Clone the repository:

```bash
git clone https://github.com/your_username/Gated-Video-Editor.git
```

2. Navigate to the project directory:

```bash
cd NewGate-Video-Processor
```

3. Install the required packages:

```bash
pip install -r requirements.txt
```

## Usage

1. Alternatively, you can use the Gate-Engine.py script with command line arguments. See below for a list of arguments:

```bash	
python Gate-Engine.py --input_file "Video File"
```

## License

This project is released under the MIT License.
