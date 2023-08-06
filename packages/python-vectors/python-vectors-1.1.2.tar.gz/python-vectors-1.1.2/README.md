### Usage
- To import everything:<br>
`import vectors`<br>
- To import only 2D and 3D points:<br>
`from vectors import Vector2, Vector3`<br>
- Get point information:<br>
`_.x` or `_.y` or if Vector3, `_.z`<br>
- Get all points as a tuple:<br>
`_.tuple()`<br>
- Get all points as an array list:<br>
`_.list()`<br>
- Get all points as a dictionary:<br>
`_.dict()`<br>
- Add two points:<br>
`vectors.add(<v1>, <v2>)`<br>
- Subtract two points:<br>
`vectors.subtract(<v1>, <v2>)`<br>
- Multiply two points:<br>
`vectors.multiply(<v1>, <v2>)`<br>
- Divide two points:<br>
`vectors.divide(<v1>, <v2>)`<br>

### Usage Notes:
- You can add, subtract, multiply, and divide a `Vector2` and a `Vector3` (and vice versa). The output will be converted to a Vector3, using `0 <operator> <second_param>.z` as the z value
- IMPORTANT: Remember when dividing, you cannot divide by zero. `0 / 2` is valid, however `2 / 0` is not. If your second parameter has a 0, you WILL get an error

### Updates
**11/18/2020 - 1.1.1-1.1.2**<br>
Updated README.md<br>
**11/18/2020 - 1.1.0**<br>
Added add, subtract, multiply, and dividing of Vector2 and Vector3<br>
**11/18/2020 - 1.0.0**<br>
Fixed `Vector3.tuple()` showing as `(x, y, x)` instead of `(x, y, z)`<br>
**11/17/2020 - 0.0.1**<br>
Package published<br>

### Other Information
See my other projects at https://fosterreichert.com