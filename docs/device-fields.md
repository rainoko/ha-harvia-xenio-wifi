# Harvia device fields

Fields seen in messages from the Harvia cloud. Meanings were inferred from observed data, not from official
documentation, so entries marked "probably" are guesses.

## Device state (`getDeviceState` / `onStateUpdated`, `reported` JSON)

| Field | Meaning |
|---|---|
| `deviceId` | Unique identifier of the device. |
| `active` | Sauna is on (0 = off, probably 1 = on). |
| `light` | Light state (0 = off, 1 = on). |
| `fan` | Fan state (0 = off, 1 = on). |
| `steamEn` | Steamer enabled (0 = off, 1 = on). |
| `targetTemp` | Target temperature (°C). |
| `targetRh` | Target relative humidity (%). |
| `heatUpTime` | Expected heat-up time in minutes. |
| `tz` | Device time zone, e.g. `UTC+1 dst`. |
| `onTime` | Session length in minutes. |
| `dehumEn` | Dehumidifier enabled (0 = off, 1 = on). |
| `autoLight` | Automatic light enabled (0 = off, 1 = on). |
| `tempUnit` | Temperature unit (0 is probably Celsius). |
| `timedStart` | Encoded value, probably the scheduled start time. |
| `displayName` | Name given to the device, e.g. "Sauna boven". |
| `cmd` | A command or message sent to or from the device. |
| `autoFan` | Automatic fan enabled (0 = off, 1 = on). |
| `aromaEn` | Aroma function enabled (0 = off, 1 = on). |
| `aromaLevel` | Aroma level. |
| `wClkEn` | Wall clock function enabled (0 = off, 1 = on). |
| `wClk` | Wall clock value. |
| `otaId` | Identifier for over-the-air updates. |
| `maxOnTime` | Maximum time in minutes the device may stay on. |
| `errorCodes` | Indicates whether errors occurred. |
| `online` | Device is online (`true` = online). |
| `otaChecked` | Timestamp of the last OTA update check. |
| `maxTemp` | Maximum temperature setting. |
| `minTemp` | Minimum temperature setting. |
| `serialNum` | Serial number. |
| `msgId` | Identifier of the message or command. |
| `statusCodes` | Current status codes. The second digit is 9 when the door is open (used by the door sensor). |
| `hwVer` | Hardware version. |
| `devType` | Device type. |
| `swVer` | Software version. |
| `hwProperties` | Hardware properties. |
| `macAddr` | MAC address. |
| `expired` | Whether some status or licence has expired (`false` = not expired). |

## Measurements (`getLatestData` / `onDataUpdates`, `data` JSON)

| Field | Meaning |
|---|---|
| `temperature` | Current measured temperature (°C). |
| `humidity` | Current measured humidity (%). 0 may mean no sensor or no reading. |
| `heatOn` | Heater is on (`false` = off). |
| `steamOn` | Steamer is on (`false` = off). |
| `remainingTime` | Remaining session time, in minutes (e.g. 357 of `onTime` 360). |
| `targetTemp` | Target temperature (°C). |
| `wifiRSSI` | WiFi signal strength in dBm, e.g. -73 (moderate to good). |
| `timestamp` | When the data was generated or last updated. |
| `heatOnCounter`, `heatOnCounterLT` | How often the heater was switched on; `LT` probably means long-term. |
| `steamOnCounter`, `steamOnCounterLT` | How often the steamer was switched on; `LT` probably means long-term. |
| `ph1RelayCounter`, `ph2RelayCounter`, `ph3RelayCounter` | Counters for the phase 1–3 relays. |
| `ph1RelayCounterLT`, `ph2RelayCounterLT`, `ph3RelayCounterLT` | Long-term counters for the phase 1–3 relays. |
| `testVar1`, `testVar2` | Test variables, possibly for troubleshooting. |
