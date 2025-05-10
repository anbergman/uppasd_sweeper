#!/usr/bin/env python3
"""Module for sweeping temperature simulations.

This script runs simulations over a range of temperatures by
updating input files and executing a binary.
"""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np


def parse_config_file(file_path):
    """
    Parses key=value pairs from a file.

    Args:
        file_path (str): Path to the config file.

    Returns:
        dict: Config keys mapped to values.
    """
    config = {}
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            if "=" in line and not line.strip().startswith("#"):
                key, value = line.strip().split("=", 1)
                config[key.strip()] = value.strip()
    return config


def replace_temperature_strings(folder_path, temperature):
    """
    Replace TEMP with the temperature in input file.

    Args:
        folder_path (Path): The directory path with files to process.
        temperature (float): The temperature to replace 'TEMP' with.

    Raises:
        UnicodeDecodeError: For files that cannot be decoded as text.
    """
    for path in folder_path.rglob("*"):
        if path.is_file() and path.suffix not in [".exe", ".bin"]:  # Skip binary files
            try:
                text = path.read_text()
                new_text = text.replace("TEMP", f"{int(round(temperature))}")
                if new_text != text:
                    path.write_text(new_text)
            except UnicodeDecodeError:
                # Skip non-text files
                continue


def run_simulation(t, base, binary_path):
    """
    Run a simulation and log its output.

    Args:
        t (float): Temperature for the simulation.
        base (str or Path): Directory with base simulation files.
        binary_path (str or Path): Path to the simulation binary.

    Raises:
        subprocess.CalledProcessError: If the simulation fails.
    """
    folder_name = f"T_{int(round(t)):04d}"
    folder_path = Path(folder_name)
    folder_path.mkdir(exist_ok=True)

    # Copy base contents
    base_path = Path(base)
    for item in base_path.iterdir():
        dest = folder_path / item.name
        if item.is_dir():
            shutil.copytree(item, dest, dirs_exist_ok=True)
        else:
            shutil.copy2(item, dest)

    # Replace TEMP with temperature
    replace_temperature_strings(folder_path, t)

    # Run binary in the new folder
    with open(folder_path / "out.log", "w", encoding="utf-8") as out_log:
        subprocess.run(
            [str(binary_path)],
            cwd=folder_path,
            stdout=out_log,
            stderr=subprocess.STDOUT,
            check=True,
        )


def main():
    """Run sweeps of temperature for the spin simulation.

    This routine parses command-line arguments or a config
    file to obtain tmin, tmax, steps, binary, and base paths. It
    calculates temperature steps and runs the simulation using the
    binary tool for each temperature.

    Args:
        None.

    Returns:
        None.
    """
    parser = argparse.ArgumentParser(
        description="Sweep temperature and run spin simulation"
    )
    parser.add_argument(
        "--tmin", type=float, default=0, help="Minimum temperature (default: 0)"
    )
    parser.add_argument(
        "--tmax", type=float, default=500, help="Maximum temperature (default: 500)"
    )

    parser.add_argument(
        "--tstep", type=float, default=100, help="Temperature step (default: 100)"
    )
    parser.add_argument(
        "--steps",
        type=int,
        default=11,
        help="Number of temperature steps (default: 11)",
    )
    parser.add_argument(
        "--binary",
        type=str,
        default="./uppasd",
        help="Path to simulation binary (default: ./uppasd)",
    )
    parser.add_argument(
        "--base",
        type=str,
        default="Base",
        help="Path to base input folder (default: Base)",
    )
    parser.add_argument(
        "--file",
        type=str,
        help="Path to config file with tmin, tmax, steps, binary, base",
    )

    args = parser.parse_args()

    # Override with config file if given
    if args.file:
        config = parse_config_file(args.file)
        print("Using config file:", args.file)
        print("  Config file contents:")
        for key, value in config.items():
            print(f"    {key}: {value}")

        args.tmin = float(config.get("tmin", args.tmin))
        args.tmax = float(config.get("tmax", args.tmax))
        args.tstep = int(config.get("tstep", args.tstep))
        args.steps = int(config.get("steps", args.steps))
        args.binary = config.get("binary", args.binary)
        args.base = config.get("base", args.base)

    if any("tstep" in arg for arg in args.__dict__):
        temperatures = np.arange(args.tmin, args.tmax + args.tstep, args.tstep)
    elif any("steps" in arg for arg in args.__dict__):
        temperatures = np.linspace(args.tmin, args.tmax, args.steps)
    else:
        print("No temperature step or number of steps provided.")
        sys.exit(1)

    print("Temperature mesh:")
    for idx, temp in enumerate(temperatures):
        print(f"  Step {idx:02d}: {temp:6.2f}")

    binary_path = Path(args.binary)
    print(f"Using binary: {binary_path}")

    if sys.platform.startswith("win") and not str(binary_path).lower().endswith(".exe"):
        binary_path = Path(str(binary_path) + ".exe")

    for t in temperatures:
        print(f"Running simulation at T={t:.2f}")
        run_simulation(t, args.base, binary_path)


if __name__ == "__main__":
    main()
