# DCProj
> ### Traffic detection and notify C&amp;C (prototype)

## Description
> In this project(demo stage) \
we have tried to detect the traffic in the simplest way \
using city traffic cameras and inform the control center.

> In this project, we have tried to detect the vehicles by using ***[Yolo](https://pjreddie.com/darknet/yolo/) (You Only Look Once)*** architecture,\
and we have informed the control center about the current state by considering \
the current traffic volume in the desired route. \
In this project, we have used \
Yolo [V9](https://github.com/WongKinYiu/yolov9) ,\
UDP protocol, \
and the network has been defined locally


## Getting Started

### Dependencies
- [ ] virtual environment   
 > We need to run a separate virtual environment to install packages and run them, the following suggested code to create a `.venv`
```sh
 $ python -m venv .venv
```
- [ ] [clone Project](https://github.com/saeidEmadi/DCProj.git)
- [ ] make [config.ini](#configini) file
- [ ] install `pip` requirements
- [ ]  add videos in directory
```sh
 $ pip install -r requirements.txt
```
- [ ] Executing program

### Executing Program
- `Virtual Environment`  activate a virtual environment
```bash
 # linux bash
 $ source .venv/bin/activate
 ```
 ```bash
  # windows CMD
  > .venv\Scripts\activate
```

- [`driver.py`](#driver)
```sh
 $ python driver.py --help
```
* [`server.py`](#server)
```sh
 $ python server.py --help
```
* [define camera's (add videos)](#videoController)
```sh
 $ python videoController.py --help
```
* simulator run *`just only test [debug mode : enable]`*
```sh
 $ python driver.py 0 0 --test --device cuda:0
```

# Help. Code Usage

## ***`config.ini`***
#### ```config.ini```
> rename config.ini.example to config.ini  
> We use this to set some default settings   

> * `Traffic Camera`   
>    + `yoloVersion` To determine the yolo version  
   **Params :** `yolov9e`,`yolov9t`,`yolov9s`,`yolov9m`,`yolov9c`
>   + `confidence` Sets the minimum confidence threshold for detections. Objects detected with confidence below this threshold will be disregarded. Adjusting this value can help reduce false positives.     
**Params :** `float`

> * `Server`   
>   * `server IP` IP address for connecting clients to the server    
    **Params :** `IPV4`, `IPV6`
>   * `port` Server Port number for connection  
    **Params :** `Port Valid number`         
>    * `backlogListenVal` It specifies the number of unaccepted connections  
that the system will allow before refusing new connections  
    **Params :** `Integer Value (max : 100)`

> * `DEBUG`
>   * `debug mode` Enable debug mode and show system logs    
    **Params :** `True or False`
```bash
[Traffic Camera]
yoloVersion = YOLO_VERSION
confidence = YOLO_CONFIDENCE

[Server]
server IP = IP_ADDRESS
port = PORT_NUMBER
backlogListenVal = IntegerValue 
#It specifies the number of unaccepted connections
#that the system will allow before refusing new connections

[DEBUG]
debug mode = BOOLEAN VALUE | True or False
```
## ***`driver`***
#### `driver.py`
> ### Starting the simulation and setting up the server and clients (cameras)    

> * ***`positional arguments`***    
 >      * `host`   IP address for connecting clients to the server    
    **Params :** `IPV4`, `IPV6`
    **Default :** `Config.ini value`
 >   * `port` Server Port number for connection  
    **Params :** `Port Valid number`        
    **Default :** `Config.ini value`

> * ***`options`***   *optional values*   
> If these options are not selected, the default values will be replaced (the default values are in the description)   
>      *  `-h`,`--help` show this help message and exit
>      * `-v`,`--yolov` To determine the version of yolo   
>   **Params :** `yolov9e`,`yolov9t`,`yolov9s`,`yolov9m`,`yolov9c`
>      **Default :** `yolov9e`
>      * `-yc`,`--yoloConf` Sets the minimum confidence threshold for detections.   
  Objects detected with confidence below this threshold will be disregarded. Adjusting this value can help reduce false positives.     
**Params :** `float`
**Default :** `0.6`
>      * `-tc`,`--trafficConf` Sets the minimum confidence threshold for Traffic.  
   Objects `(vehicles)` count with confidence below this threshold will be disregarded. Adjusting this value can help reduce false positives.     
**Params :** `Integer Value (min : 3)`    
**Default :** `8`
>      * `-d`,`--detect` labels for model detection     
using ms coco : MS Common Objects in Context   
>   **Params :** `str list lables` [MS-COCO list](https://github.com/saeidEmadi/DCProj/blob/main/trafficCamera/msCocoLablesPaper.txt) , `all`,`vehicles`
**Default :** `vehicles`
>     * `-c`,`--client` Used to specify the number of clients (cameras)
**Params :** `Integer Value (min : 1)`    
**Default :**  `5`
>      + `--test` This ***flag*** is used for simulation testing (default values)
         **Params :** `True or False`
         **Default :**  `False | if call : True`         
>    + `--stream` stream traffic camera real-Time
         **Params :** `True or False`
         **Default :**  `False | if call : True`         
>     + `--debug` show CLI logs
         **Params :** `True or False`
         **Default :**  `False | if call : True`         
>     + `--device` yolo gpu core or CPU 
>              **Params :** `0`,`1`,`2`,`3`,`cuda:0`,`cuda:1`,`cuda:2`,`cuda:3`,`cpu`
         **Default :**  `cpu`         
```sh
 $ python driver.py --help
 > usage: driver.py [-h] [-v yoloVersion] [-yc yoloConf] [-tc trafficConf]
                  [-d [coco class name's ...]] [-c INT] [--test] [--stream]
                  [--debug] --device core
                  host port

   positional arguments:
     host                  Server Address for listening clients
     port                  port number
 
   options:
     -h, --help            show this help message and exit
     -v yoloVersion, --yolov yoloVersion
                           Yolo pre-Train Model version (default : yolov9e)
     -yc yoloConf, --yoloConf yoloConf
                           Yolo pre-Train Model confidence (default : 0.6)
     -tc trafficConf, --trafficConf trafficConf
                           traffic Max confidence (default : 8)
     -d [coco class name's ...], --detect [coco class name's ...]
                           detect all objects in ms-COCO or only vehicles
                           (example : vehicles person [etc.]], default =
                           vehicles)
     -c INT, --client INT  number of clients ,[default = 5]
     --test                flag for Enable defaults parameters run :: 127.0.0.1
                           1919 -v yolov9e, -c 5
     --stream              stream traffic camera real-Time
     --debug               flag for Enable Debug mode [show CLI logs]
     --device core         yolo gpu core or CPU [ex. cpu , cuda:0]

```
## ***`server`***
#### `server.py`
> ### Running a server to receive data and connect clients

> * ***`positional arguments`***    
 >      * `host`   IP address for connecting clients to the server    
    **Params :** `IPV4`, `IPV6`
    **Default :** `Config.ini value`
 >   * `port` Server Port number for connection  
    **Params :** `Port Valid number`        
    **Default :** `Config.ini value`

> * ***`options`***   *optional values*   
> If these options are not selected, the default values will be replaced (the default values are in the description)   
>      *  `-h`,`--help` show this help message and exit
>      + `--test` This ***flag*** is used for simulation testing (default values)
         **Params :** `True or False`
         **Default :**  `False | if call : True`         
>     + `--debug` show CLI logs
         **Params :** `True or False`
         **Default :**  `False | if call : True`         
```sh
 $ python server.py --help
 > [Server Running : CLI Mode]
   usage: Server [-h] [--test] [--debug] host port
   
   Server runner Script | run script for receive Camera Packets
   positional arguments:
     host        Server Address for listening clients
     port        port number

   options:
     -h, --help  show this help message and exit
     --test      flag for Enable defaults parameters run :: 127.0.0.1 1919
     --debug     flag for Enable Debug mode [show CLI logs]

```
## ***`trafficCamera\runMain`***
#### `trafficCamera\runMain.py` 
> ### Development act.
```python
 # import library 
In [1]: from trafficCamera.runMain import Camera

In [2]: camera = Camera(serverIP='127.0.0.1', portNumber=1919, yoloVersion='yolov9e',show=False,device='cuda:0',detecti
   ...: onLabels=['vehicles'],yoloConf=0.6,trafficConf=8,stream=False,DEBUG=True)
 Camera : convert class Names : ['bicycle', 'car', 'motorbike', 'aeroplane', 'bus', 'train', 'truck', 'boat']
 Camera : to
 Camera : [1, 2, 3, 4, 5, 6, 7, 8]

++[new Camera object]++

 Camera : [server IP : 127.0.0.1]
[ Camera Port Number : 1919]
 Camera : [yolo Version : yolov9e.pt]
 Camera : [detection Labels : ['bicycle', 'car', 'motorbike', 'aeroplane', 'bus', 'train', 'truck', 'boat']]
 Camera : [detection : [1, 2, 3, 4, 5, 6, 7, 8]]
 Camera : [yolo conf : 0.6]
 Camera : [traffic conf : 8]

```
## ***`videoController`***
#### `videoController.py` 
> ###  We use it to transfer and add videos used by clients (cameras)

> * ***`positional arguments`***    
 >      * `source address`   video source address (folder or video name)
    **Params :** `Path (String)`


> * ***`options`***   *optional values*   
> If these options are not selected, the default values will be replaced (the default values are in the description)   
>      *  `-h`,`--help` show this help message and exit
>      * `-d`,`--dest` video destination address folder (video folder)
>     **Params :** `Path (String)`
>      **Default :** `'.'` *current folder*
>      * `-f`,`--format` find this formats in directory
**Params :** `.mp4`,`.mkv`,`other video format`
**Default :** `.mp4`
```sh 
 $ python videoController.py --help
 > [ video controller Running : CLI Mode]
   usage: videoController [-h] [--dest destination address] --format format
                          [format ...]
                          source address

   video controller runner Script | run script for input controlling video for
   camera's

   positional arguments:
     source address        video source address (folder or video name)

   options:
     -h, --help            show this help message and exit
     --dest destination address, -d destination address
                           video destination address folder (video folder)
     --format format [format ...], -f format [format ...]
                           find this formats in directory [.mp4|.mkv|etc]

```

## Authors

> Contributors names and contact info

[@Amir Reza](https://github.com/Amirreza-Afra)

## Version History


 * 0.1
   > This version is only a prototype and a student project

## License

> This project is licensed under the Apache-2.0 License - see the LICENSE.md file for details
