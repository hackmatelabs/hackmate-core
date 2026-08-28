# Third-party assets

## Acidanthera — OpenCorePkg / OcBinaryData

`Resources/Font/` and `Resources/Label/` are copied verbatim from
[OcBinaryData](https://github.com/acidanthera/OcBinaryData). The chrome icons in
`Resources/Image/HackMate/Core/` (`Cursor`, `Selected`, `Selector`,
`SetDefault`, `Left`, `Right`, `HardDrive`, `Windows`, `Shell`, `Tool`,
`AppleRecv`, `FirmwareSettings`, `Restart`, etc.) are derived from Acidanthera's
`GoldenGate` icon set; `Selected` / `Selector` / `SetDefault` are recoloured,
`Apple.icns` is original to this project.

`OpenCanopy.efi` is **not** included here — it ships with every OpenCore release
and must match your `OpenCore.efi` version.

OpenCorePkg and OcBinaryData are licensed BSD-3-Clause:

```
Copyright (c) 2016-2024, Acidanthera. All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.
3. Neither the name of the copyright holder nor the names of its contributors
   may be used to endorse or promote products derived from this software
   without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
```

## Background image

`Resources/Image/HackMate/Core/Background*.icns` is a heavily blurred and
darkened rendering of an Apple macOS "Tahoe" desktop wallpaper, composited with
original text. Apple wallpapers are Apple's copyright; this derivative is
included the way OpenCanopy themes across the hackintosh community customarily
ship wallpaper-derived backgrounds. Regenerate with your own image via
`tools/build_theme.py --wallpaper ...` if you'd rather not use it.
