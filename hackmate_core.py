"""
HackMate-Core: enable OpenCore's OpenCanopy graphical picker with the HackMate
theme. OpenCore itself is not modified.

Library:
    import hackmate_core
    hackmate_core.apply_to_config(cfg_dict, style="full")      # patch a parsed config
    hackmate_core.install_resources("/path/to/EFI/OC")         # copy the theme in

CLI:
    python hackmate_core.py apply   /path/to/EFI/OC/config.plist [--minimal]
    python hackmate_core.py install /path/to/EFI/OC [--minimal] [--resolution 2560x1440]
                                    [--oc-release /path/to/OpenCore-X.Y.Z-RELEASE]
"""

import shutil
from pathlib import Path

THEME = "HackMate\\Core"
RESOURCES = Path(__file__).resolve().parent / "Resources"
EXTRA_DRIVERS = ["OpenCanopy.efi"]

_VOLUME_ICON = 0x0001
_POINTER = 0x0010
_MINIMAL_UI = 0x0040
_FLAVOUR = 0x0080

PICKER_ATTRIBUTES = _VOLUME_ICON | _POINTER | _FLAVOUR
STYLES = {
    "full": PICKER_ATTRIBUTES,
    "minimal": PICKER_ATTRIBUTES | _MINIMAL_UI,
}


def available() -> bool:
    return (RESOURCES / "Image" / "HackMate" / "Core" / "Background.icns").is_file()


def apply_to_config(config: dict, style: str = "full") -> None:
    attrs = STYLES.get(style, PICKER_ATTRIBUTES)

    boot = config.setdefault("Misc", {}).setdefault("Boot", {})
    boot["PickerMode"] = "External"
    boot["PickerVariant"] = THEME
    boot["PickerAttributes"] = int(boot.get("PickerAttributes", 0)) | attrs
    boot["PickerAudioAssist"] = bool(boot.get("PickerAudioAssist", False))

    uefi = config.setdefault("UEFI", {})
    drivers = uefi.setdefault("Drivers", [])
    present = {d.get("Path") for d in drivers if isinstance(d, dict)}
    for name in EXTRA_DRIVERS:
        if name not in present:
            drivers.append({
                "Arguments": "", "Comment": "HackMate-Core graphical picker",
                "Enabled": True, "LoadEarly": False, "Path": name,
            })

    out = uefi.setdefault("Output", {})
    out["ProvideConsoleGop"] = True
    if out.get("Resolution", "Max") in ("", "Auto"):
        out["Resolution"] = "Max"


def _pick_background(core_dir, resolution, log):
    if not resolution or "x" not in str(resolution).lower():
        return
    try:
        height = int(str(resolution).lower().split("x")[1].split("@")[0])
    except (ValueError, IndexError):
        return
    variants = {1080: "Background.icns", 1440: "Background_1440p.icns", 2160: "Background_2160p.icns"}
    best = min(variants, key=lambda h: abs(h - height))
    src = core_dir / variants[best]
    if best != 1080 and src.is_file():
        shutil.copy(src, core_dir / "Background.icns")
        log(f"  background set to {best}p for {resolution}", "ok")


def _merge_tree(src, dst):
    dst.mkdir(parents=True, exist_ok=True)
    for item in src.iterdir():
        target = dst / item.name
        if item.is_dir():
            _merge_tree(item, target)
        else:
            shutil.copy2(item, target)


def install_resources(oc_dir, oc_release_root=None, resolution=None, log=None) -> list[str]:
    if log is None:
        def log(msg, level="info"):
            print(msg)

    oc_dir = Path(oc_dir)
    if not (oc_dir / "config.plist").is_file():
        raise FileNotFoundError(f"{oc_dir} is not an EFI/OC directory (no config.plist)")
    installed = []

    dst_res = oc_dir / "Resources"
    _merge_tree(RESOURCES, dst_res)
    _pick_background(dst_res / "Image" / "HackMate" / "Core", resolution, log)
    installed.append("Resources/ (merged)")
    log("  Resources/ merged into EFI/OC/Resources", "ok")

    driver_dir = oc_dir / "Drivers"
    driver_dir.mkdir(parents=True, exist_ok=True)
    for name in EXTRA_DRIVERS:
        if (driver_dir / name).is_file():
            log(f"  {name} already present", "ok")
            installed.append(name + " (present)")
            continue
        found = list(Path(oc_release_root).rglob(name)) if oc_release_root else []
        if found:
            shutil.copy(str(found[0]), str(driver_dir / name))
            installed.append(name)
            log(f"  {name} copied from OpenCore release", "ok")
        else:
            log(f"  {name} NOT found - copy it from your OpenCore release into "
                f"{driver_dir} (it ships with every release) and enable it in "
                f"UEFI>Drivers", "warn")
    return installed


def _cli():
    import argparse
    import plistlib

    ap = argparse.ArgumentParser(description="Enable the HackMate-Core OpenCanopy picker.")
    sub = ap.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("apply", help="patch a config.plist in place")
    a.add_argument("config")
    a.add_argument("--minimal", action="store_true", help="hide the shutdown/restart buttons")

    i = sub.add_parser("install", help="patch config.plist + copy the theme into an EFI/OC dir")
    i.add_argument("oc_dir")
    i.add_argument("--minimal", action="store_true")
    i.add_argument("--resolution", default=None, help='e.g. "2560x1440" - picks the matching Background')
    i.add_argument("--oc-release", default=None, help="path to an extracted OpenCore-X.Y.Z-RELEASE (for OpenCanopy.efi)")

    args = ap.parse_args()
    style = "minimal" if args.minimal else "full"

    if args.cmd == "apply":
        p = Path(args.config)
        with open(p, "rb") as f:
            cfg = plistlib.load(f)
        apply_to_config(cfg, style=style)
        with open(p, "wb") as f:
            plistlib.dump(cfg, f, sort_keys=False)
        print(f"patched {p}: PickerMode=External PickerVariant={THEME} style={style}")
        return

    oc_dir = Path(args.oc_dir)
    cfg_path = oc_dir / "config.plist"
    with open(cfg_path, "rb") as f:
        cfg = plistlib.load(f)
    apply_to_config(cfg, style=style)
    if args.resolution:
        cfg.setdefault("UEFI", {}).setdefault("Output", {})["Resolution"] = args.resolution
    with open(cfg_path, "wb") as f:
        plistlib.dump(cfg, f, sort_keys=False)
    done = install_resources(oc_dir, args.oc_release, resolution=args.resolution)
    print(f"patched {cfg_path} and installed: {', '.join(done)}")
    print("If OpenCanopy.efi was not already present, add it from your OpenCore "
          "release and make sure it's enabled in UEFI>Drivers.")


if __name__ == "__main__":
    _cli()
