from __future__ import annotations

from pathlib import Path
import shutil
import time
import subprocess
import sys
from typing import Optional, List

from deoldify.visualize import get_video_colorizer


# === Paths ===
IN_DIR = Path("/path/to/your")
OUT_DIR = Path("/path/to/clips_color")

# === Params ===
RENDER_FACTOR = 10            
SKIP_EXISTING = True          
DELETE_INTERNAL_RESULT = False  


def ensure_ffmpeg_available() -> None:
    """DeOldify requires system ffmpeg."""
    try:
        subprocess.run(["ffmpeg", "-version"], check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        raise RuntimeError(
            "ffmpeg not found on PATH. Download ffmpeg "
            "or import PATH."
        )


def list_mp4s_under(root: Path) -> List[Path]:
    return [p for p in root.rglob("*.mp4") if p.is_file()]


def newest_mp4_after(root: Path, t0: float) -> Optional[Path]:
    """Find newest mp4 in repo written after t0 (mtime)."""
    candidates = []
    for p in list_mp4s_under(root):
        try:
            if p.stat().st_mtime >= t0:
                candidates.append(p)
        except FileNotFoundError:
            continue
    if not candidates:
        return None
    candidates.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return candidates[0]


def safe_stem(stem: str) -> str:
    """Normalize filename stem (avoid spaces/special chars)."""
    out = []
    for ch in stem:
        if ch.isalnum() or ch in ("-", "_"):
            out.append(ch)
        elif ch.isspace():
            out.append("_")
    s = "".join(out).strip("_")
    return s or "clip"


def main() -> None:
    if not IN_DIR.exists():
        raise FileNotFoundError(f"Input folder not found: {IN_DIR}")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    ensure_ffmpeg_available()

    repo_dir = Path(__file__).resolve().parent

    mp4s = sorted(IN_DIR.glob("*.mp4"))
    if not mp4s:
        print(f"[WARN] No .mp4 found in {IN_DIR}")
        return

    print(f"Repo:   {repo_dir}")
    print(f"Input:  {IN_DIR}")
    print(f"Output: {OUT_DIR}")
    print(f"Render factor: {RENDER_FACTOR}")
    print(f"Clips found: {len(mp4s)}")

    video_colorizer = get_video_colorizer()

    for i, src in enumerate(mp4s, start=1):
        out_name = f"{safe_stem(src.stem)}_color.mp4"
        out_path = OUT_DIR / out_name

        if SKIP_EXISTING and out_path.exists() and out_path.stat().st_size > 1_000_000:
            print(f"[{i}/{len(mp4s)}] SKIP existing: {out_path.name}")
            continue

        print(f"[{i}/{len(mp4s)}] Colorizing: {src.name}")
        t0 = time.time()

        video_colorizer.colorize_from_file_name(
            file_name=str(src),
            render_factor=RENDER_FACTOR,
            watermarked=False
        )

        produced = newest_mp4_after(repo_dir, t0)
        if produced is None:
            # 
            time.sleep(2)
            produced = newest_mp4_after(repo_dir, t0)

        if produced is None:
            raise RuntimeError(
                "didnt find mp4 after colorization"
            )

        # copy to final location
        if out_path.exists():
            out_path.unlink()
        shutil.copy2(produced, out_path)
        print(f"      -> saved: {out_path}")

        if DELETE_INTERNAL_RESULT:
            try:
                produced.unlink()
            except Exception:
                pass

    print("\n[DONE] Finished.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n[ERROR] {e}", file=sys.stderr)
        sys.exit(1)
