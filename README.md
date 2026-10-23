# Blender Cloud Render

A starter Blender scene that renders a blue beveled cube on a ground plane.
No third-party Python packages or API keys are required.

## Render locally or in Codex Cloud

Blender 4.3.2 is installed in the prepared cloud environment. On Ubuntu, install
Blender using `sudo apt-get update && sudo apt-get install -y blender`.

From this repository directory:

```sh
mkdir -p /workspace/blender-user
export BLENDER_USER_RESOURCES=/workspace/blender-user
blender --background --threads 2 --python-exit-code 1 --python scene.py
test -s output/preview.png
test -s output/scene.blend
```

Outside Codex Cloud, choose a writable directory for `BLENDER_USER_RESOURCES`
or omit the export to use Blender's default configuration location.

The script saves `output/preview.png` and `output/scene.blend`. It uses Cycles
on the CPU with denoising disabled to support builds without OpenImageDenoise.
Generated outputs are ignored by Git. Edit `scene.py` to change the scene.

## GitHub Actions

Pushing changes to `scene.py` or the workflow triggers **Blender Cloud Render**.
You can also run it manually in the repository's Actions tab. After a successful
run, download the **blender-output** artifact for the image and editable scene.
GitHub Actions installs the Ubuntu distribution's Blender version, which can
differ from the cloud environment's version.

The workflow performs one render per run. AI analysis and iterative scene
revision require a separate task; they are not implemented by this workflow.
