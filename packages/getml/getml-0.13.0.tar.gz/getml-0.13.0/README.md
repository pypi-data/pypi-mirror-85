# Private repositoy for the getML Python API

## Testing

The handling of all scripts (unit tests, test scripts located in
[tests](tests/), and all examples in
[getml-examples](https://github.com/getml/getml-examples)), will be
handled by the [test.sh](test.sh) script.

``` bash
./test
```

All options of the `build.sh` script can be found below. (If none is
present, `all` is invoked).

| Command (short) | Command (long) | Description                                                 |
| ---------       | -------        | ----                                                        |
| a               | all            | run both the Python API tests as well as the getml-examples |
| e               | examples       | run the getml-examples                                      |
| h               | help           | print out the different options of execution                |
| p               | python         | run the Python API tests                                    |
=======
