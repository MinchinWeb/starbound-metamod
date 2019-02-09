# Custom Resolutions

*I found this while trying to get the game to match my native resolution of
3440x1440.*

> Okay, poked around and found the config. Editing in a 21:9 res manually works
> fine.
>
> Open the starbound.config in `xxxx/steamapps/common/Starbound/storage/` and set
>
>     "fullscreen" : true,
>     "fullscreenResolution" : [2560, 1080],
>
> or [3440, 1440] save and load the game and it should be correctly proportioned
> instead of stretched to fill ultrawide.

*via
[Steam](https://steamcommunity.com/app/211820/discussions/0/352788917753874642/)*

## Upping Interface Scale

> Hello people, i wondered if there is some way to play the game on 3440x1440
> (21:9) and to make the interface (toolbar etc.) larger so you can use it
> better on a big screen. Anyone got an idea ? :)

.

> That's easily accomplished via modding. You need an inventory.config.patch
> file.
>
>    [
>        {
>            "op" : "replace",
>            "path" : "/minInterfaceScale",
>            "value" : 3
>        },
>        {
>            "op" : "replace",
>            "path" : "/maxInterfaceScale",
>            "value" : 3
>        }
>    ]

*via
[Reddit](https://www.reddit.com/r/starbound/comments/8uhq2m/219_and_interface_scale/)*
