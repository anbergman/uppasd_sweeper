# Temperature Sweep Runner for Spin Simulations

This Python script automates running a spin simulation binary across a range of temperatures.  
It prepares input folders, modifies them, runs the binary, and logs output.

## 🚀 Features

- Cross-platform (Windows, macOS, Linux)
- Temperature sweep with custom steps
- Replaces `TEMP` placeholder in `inpsd.dat` with actual temperature
- Optional config file for easy reuse
- Saves output to `T_xxxx/out.log` per temperature

---

## 🧱 Installation

Install the script with `pip`

```bash
pip install git+https://github.com/anbergman/t_sweeper.git
```

or optionally

```bash
python -m pip install git+https://github.com/anbergman/t_sweeper.git
```

---

## 🧱 Requirements

Install dependencies with:

```bash
pip install -r requirements.txt
```

Only `numpy` is needed.

---

## 📦 Usage

```bash
python t_sweeper.py --tmin 0 --tmax 1000 --tstep 100 --binary ./uppasd --base Base
```

Or using a config file:

```bash
python t_sweeper.py --file config.txt
```

### Command-Line Options

| Option        | Description                                      | Default     |
|---------------|--------------------------------------------------|-------------|
| `--tmin`      | Minimum temperature (float)                      | `0`         |
| `--tmax`      | Maximum temperature (float)                      | `500`       |
| `--tstep`     | Temperature step between points                  | `100`       |
| `--steps`     | Number of steps between tmin and tmax (optional) | `11`        |
| `--binary`    | Path to simulation binary                        | `./uppasd`  |
| `--base`      | Folder containing base input files               | `Base`      |
| `--file`      | Config file with key=value lines (see below)     | *(optional)*|

---

## 📝 Config File Format

Use key-value pairs in a `.txt` file like:

```ini
tmin = 100
tmax = 600
tstep = 100
binary = ./uppasd
base = ./BaseInput
```

Command-line arguments **override** these values if provided.

---

## 📁 What It Does

1. Loops over temperatures from `tmin` to `tmax` in `steps` steps.
2. For each temperature `T`, creates a folder `T_xxxx`.
3. Copies all contents of `base` into that folder.
4. Replaces `TEMP` in `inpsd.dat` with the float value of `T` (minimum 1e-6).
5. Runs the binary inside the folder.
6. Logs output to `T_xxxx/out.log`.

---
## 📁 What It Needs

1. A full set of UppASD input files in the `base` folder.
2. The original `inpsd.dat` file should have the token `TEMP` where the temperature is to be replaced.
3. A compatible `binary` of UppASD should be available and given as argument.

---

## 💡 Examples

**Basic example:**
```bash
python t_sweeper.py
```

**Custom binary and input folder:**
```bash
python t_sweeper.py --tmin 50 --tmax 200 --steps 4 --binary ./uppasd.exe --base Base
```

**Using config file only:**
```bash
python t_sweeper.py --file run_config.txt
```

---

## 🖥 Compatibility

- Script automatically adds `.exe` on Windows if needed.
- Uses only POSIX-safe paths with `pathlib`.

---

## 📬 Output Structure

After running, you’ll see folders like:

```
T_0000/
T_0100/
T_0200/
...
```

Each contains:
- A copy of the `Base` input files
- Modified `inpsd.dat` (with `TEMP` → actual value)
- `out.log` with run output

---

## 🧩 Known Assumptions

- A complete setup for the system should be available in the `--base` directory
- The `inpsd.dat` input file should have the token TEMP for any occasion where the temperature should be replaced.

---

