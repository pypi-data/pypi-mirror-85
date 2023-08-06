# nr.powerline

Simple powerline implementation, only tested in Bash. It is recommended that
you use a font from [NerdFonts](https://nerdfonts.com/#downloads) in order to
have proper support for special characters (like the right triangle).

![](screenshot.png)

__Requirements__

- Bash
- Pipx
- Python 3.5+
- Linux/macOS
- jq (If not available, the environment variables cannot be sent from Bash to the powerline server)

__Installation__

    $ pipx install nr.powerline
    $ source <(nr-powerline --src bash)

On OSX, sourcing a Bash script from `/dev/<fd>` seems to have some issues, so you
may need to write it to a temporary file instead.

```sh
if which nr-powerline >/dev/null; then
  function _activate_powerline() {
    local TMP=`mktemp`; trap "rm -f $TMP" RETURN
    nr-powerline --src bash>$TMP
    source $TMP
  }
  _activate_powerline
fi
```

---

<p align="center">Copyright &copy; 2020 Niklas Rosenstein</p>
