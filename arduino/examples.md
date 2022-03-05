# Example Code

## ArdunioJSON

Library code [here](https://github.com/bblanchon/ArduinoJson). (imported in ArduinoJSON.h file)

Serialization

```cpp
DynamicJsonDocument doc(1024);

doc["sensor"] = "gps";
doc["time"]   = 1351824120;
doc["data"][0] = 48.756080;
doc["data"][1] = 2.302038;

serializeJson(doc, Serial);
// This prints:
// {"sensor":"gps","time":1351824120,"data":[48.756080,2.302038]}
```

Deserialization

```cpp
char json[] = "{\"sensor\":\"gps\",\"time\":1351824120,\"data\":[48.756080,2.302038]}";

DynamicJsonDocument doc(1024);
// deserializeJson(doc, json);
// You can ALSO deserialize from a Serial port
deserializeJson(doc, Serial);

const char* sensor = doc["sensor"];
long time          = doc["time"];
double latitude    = doc["data"][0];
double longitude   = doc["data"][1];
```
