import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import pages_main as m, pages_guide as g
out = pathlib.Path(sys.argv[1])
files = {
    "index.html": m.landing(), "architecture.html": m.architecture(), "404.html": m.not_found(),
    "self-host/index.html": g.overview(), "self-host/provision.html": g.provision(),
    "self-host/deploy.html": g.deploy(), "self-host/enroll.html": g.enroll(),
    "self-host/first-machine.html": g.first_machine(), "self-host/operations.html": g.operations(),
}
for name, html in files.items():
    (out / name).parent.mkdir(parents=True, exist_ok=True)
    (out / name).write_text(html)
    print(name, len(html))
