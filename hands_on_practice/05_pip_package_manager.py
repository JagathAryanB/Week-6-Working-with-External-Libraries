import importlib.metadata
import subprocess
import sys

def list_installed_packages():
    packages = []
    for dist in importlib.metadata.distributions():
        packages.append((dist.metadata["Name"], dist.version))
    return sorted(packages, key=lambda x: x[0].lower())

def check_package_installed(package_name):
    try:
        version = importlib.metadata.version(package_name)
        return True, version
    except importlib.metadata.PackageNotFoundError:
        return False, None

def inspect_pip_environment():
    details = {
        "Python Executable": sys.executable,
        "Python Version": sys.version.split()[0],
        "In Virtual Environment": hasattr(sys, "real_prefix") or (hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix),
        "Prefix": sys.prefix,
        "Base Prefix": getattr(sys, "base_prefix", sys.prefix)
    }
    return details

def run_pip_command(command_args):
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip"] + command_args,
            capture_output=True,
            text=True,
            timeout=15
        )
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        return -1, "", str(e)

def main():
    print("=" * 60)
    print("PIP AND ENVIRONMENT MANAGEMENT")
    print("=" * 60)
    
    env_info = inspect_pip_environment()
    for k, v in env_info.items():
        print(f"{k:<25}: {v}")
    
    print("-" * 60)
    print("VERIFYING REQUIRED PACKAGES:")
    target_packages = ["requests", "python-dotenv", "colorama", "faker", "pytest"]
    for pkg in target_packages:
        installed, ver = check_package_installed(pkg)
        status = f"INSTALLED (v{ver})" if installed else "NOT INSTALLED"
        print(f"  - {pkg:<20}: {status}")

    print("-" * 60)
    print("FIRST 10 INSTALLED PACKAGES:")
    all_pkgs = list_installed_packages()
    for name, ver in all_pkgs[:10]:
        print(f"  {name:<25} {ver}")
    print(f"Total installed packages found: {len(all_pkgs)}")

    print("-" * 60)
    print("PIP CLI VERSION:")
    code, stdout, stderr = run_pip_command(["--version"])
    if code == 0:
        print(f"  {stdout.strip()}")
    else:
        print(f"  Failed to invoke pip: {stderr.strip()}")
    print("=" * 60)

if __name__ == "__main__":
    main()
