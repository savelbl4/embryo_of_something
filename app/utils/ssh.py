import subprocess


def test_ssh():
    result = subprocess.run(
        [
            "ssh", "-o", "StrictHostKeyChecking=no",
            "botctl@host.docker.internal",
            "ls", "-la"
        ],
        capture_output=True,
        text=True,
        timeout=20,
    )

    if result.returncode == 0:
        return f"✅\n{result.stdout.strip()}"

    return f"❌\n{result.stderr.strip() or result.stdout.strip()}"
