#!/usr/bin/env python3
"""Simple package manager CLI for Tombo: `to`.

Commands:
- init <name>: create a package skeleton
- publish <name>: publish package directory into ./packages/<name>
- install <name>: install package from ./packages into ./vendor/<name>
- list: list published packages
"""
from __future__ import annotations
import argparse
import shutil
import os
import sys


def init_package(name: str) -> None:
    os.makedirs(name, exist_ok=True)
    meta = os.path.join(name, "package.toml")
    if not os.path.exists(meta):
        with open(meta, "w", encoding="utf-8") as f:
            f.write(f"name = \"{name}\"\nversion = \"0.0.1\"\n")
    readme = os.path.join(name, "README.md")
    if not os.path.exists(readme):
        with open(readme, "w", encoding="utf-8") as f:
            f.write(f"# {name}\n\nA Tombo package named {name}.\n")
    print(f"Initialized package: {name}")


def publish_package(name: str, src: str = None) -> None:
    src = src or name
    if not os.path.isdir(src):
        print(f"Source package directory not found: {src}")
        sys.exit(1)
    packages_dir = os.path.join(os.getcwd(), "packages")
    os.makedirs(packages_dir, exist_ok=True)
    dest = os.path.join(packages_dir, name)
    if os.path.exists(dest):
        shutil.rmtree(dest)
    shutil.copytree(src, dest)
    print(f"Published package '{name}' to {dest}")


def install_package(name: str) -> None:
    packages_dir = os.path.join(os.getcwd(), "packages")
    src = os.path.join(packages_dir, name)
    if not os.path.isdir(src):
        print(f"Package '{name}' not found in {packages_dir}")
        sys.exit(1)
    vendor_dir = os.path.join(os.getcwd(), "vendor")
    os.makedirs(vendor_dir, exist_ok=True)
    dest = os.path.join(vendor_dir, name)
    if os.path.exists(dest):
        shutil.rmtree(dest)
    shutil.copytree(src, dest)
    print(f"Installed package '{name}' to {dest}")


def list_packages() -> None:
    packages_dir = os.path.join(os.getcwd(), "packages")
    if not os.path.isdir(packages_dir):
        print("No packages directory found.")
        return
    items = sorted(os.listdir(packages_dir))
    if not items:
        print("No published packages.")
        return
    for it in items:
        print(it)


def info_package(name: str) -> None:
    # Show package metadata from package.toml in packages/
    packages_dir = os.path.join(os.getcwd(), "packages")
    pkgdir = os.path.join(packages_dir, name)
    if not os.path.isdir(pkgdir):
        print(f"Package '{name}' not found in {packages_dir}")
        return
    meta = os.path.join(pkgdir, "package.toml")
    if not os.path.exists(meta):
        print("No package.toml found for package", name)
        return
    with open(meta, "r", encoding="utf-8") as f:
        print(f.read())


def search_packages(query: str) -> None:
    packages_dir = os.path.join(os.getcwd(), "packages")
    if not os.path.isdir(packages_dir):
        print("No packages directory found.")
        return
    items = sorted(os.listdir(packages_dir))
    matches = [it for it in items if query.lower() in it.lower()]
    if not matches:
        print("No packages match query")
        return
    for m in matches:
        print(m)


def integrate_package(name: str) -> None:
    # Add installed package path to tombo_packages.txt for interpreter to read
    vendor_dir = os.path.join(os.getcwd(), "vendor")
    pkg = os.path.join(vendor_dir, name)
    if not os.path.isdir(pkg):
        print(f"Installed package '{name}' not found in {vendor_dir}")
        sys.exit(1)
    out = os.path.join(os.getcwd(), "tombo_packages.txt")
    line = os.path.abspath(pkg)
    existing = []
    if os.path.exists(out):
        with open(out, "r", encoding="utf-8") as f:
            existing = [l.strip() for l in f if l.strip()]
    if line in existing:
        print(f"Package '{name}' already integrated")
        return
    with open(out, "a", encoding="utf-8") as f:
        f.write(line + "\n")
    print(f"Integrated package '{name}' into interpreter config ({out})")


def main(argv=None):
    parser = argparse.ArgumentParser(prog="to", description="Tombo package manager")
    sub = parser.add_subparsers(dest="cmd")

    p_init = sub.add_parser("init", help="Create a package skeleton")
    p_init.add_argument("name")

    p_publish = sub.add_parser("publish", help="Publish a package from a directory")
    p_publish.add_argument("name")
    p_publish.add_argument("--src", help="Source directory (defaults to name)")

    p_install = sub.add_parser("install", help="Install published package into ./vendor")
    p_install.add_argument("name")

    p_list = sub.add_parser("list", help="List published packages")
    p_info = sub.add_parser("info", help="Show package metadata (from packages/<name>/package.toml)")
    p_info.add_argument("name")

    p_search = sub.add_parser("search", help="Search published packages by substring")
    p_search.add_argument("query")

    p_integrate = sub.add_parser("integrate", help="Integrate installed package into interpreter config")
    p_integrate.add_argument("name")

    args = parser.parse_args(argv)
    if args.cmd == "init":
        init_package(args.name)
    elif args.cmd == "publish":
        publish_package(args.name, src=args.src)
    elif args.cmd == "install":
        install_package(args.name)
    elif args.cmd == "list":
        list_packages()
    elif args.cmd == "info":
        info_package(args.name)
    elif args.cmd == "search":
        search_packages(args.query)
    elif args.cmd == "integrate":
        integrate_package(args.name)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
