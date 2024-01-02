# LEDDMX-BLE

`LEDDMX-00-0000` BLE Python Script 

I have this led light that is controlled using the `LED LAMP` App.

I didn't find anyone with this RGB LED BAR LIGHT and I don't know the chip either, but I was able to reverse engineer the Bluetooth BLE packages and get the commands to control it.

- TURN_OFF_COMMAND: `7BFF 0400 FFFF FFFF BF`
- TURN_ON_COMMAND: `7BFF 0401 FFFF FFFF BF`
- FILTERING SERVICE: `FFB0`
- BLE SERVICE: `FFE0`
- BLE CHARACTERISTIC: `FFE1`

## Usage

```
" Turn OFF
$ python leddmx-ble.py --status off

" Turn ON
$ python leddmx-ble.py --status on
```

### License
MIT 2024\
Author: [Gaston Morixe](gaston@gastonmorixe.com)

