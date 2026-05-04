"""
Automotive Data Analysis with Python

This script analyzes simulated automotive sensor data.
It reads vehicle data from a CSV file, validates the data, calculates
engineering statistics, detects warning conditions, creates plots,
and generates an automated technical report.

Project: Automotive Data Analysis with Python
Language: Python
Libraries: pandas, matplotlib
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


DATA_FILE = Path("vehicle_data.csv")
OUTPUT_DIR = Path("outputs")
REPORT_FILE = OUTPUT_DIR / "automotive_report.txt"

HIGH_TEMPERATURE_LIMIT = 90.0
LOW_BATTERY_LIMIT = 12.0
HIGH_SPEED_LIMIT = 100.0
HARD_ACCELERATION_LIMIT = 2.5
HARD_BRAKING_LIMIT = -3.0

REQUIRED_COLUMNS = [
    "time_s",
    "vehicle_speed_kmh",
    "engine_rpm",
    "throttle_percent",
    "brake_pressure_bar",
    "battery_voltage_v",
    "motor_temperature_c",
]


def load_vehicle_data(file_path: Path) -> pd.DataFrame:
    """Load and validate automotive sensor data from a CSV file."""
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    data = pd.read_csv(file_path)

    missing_columns = set(REQUIRED_COLUMNS) - set(data.columns)
    if missing_columns:
        raise ValueError(f"Missing columns in CSV file: {sorted(missing_columns)}")

    data = data[REQUIRED_COLUMNS].copy()

    for column in REQUIRED_COLUMNS:
        data[column] = pd.to_numeric(data[column], errors="coerce")

    if data.isna().any().any():
        bad_columns = data.columns[data.isna().any()].tolist()
        raise ValueError(f"Invalid or missing numeric values in: {bad_columns}")

    data = data.sort_values("time_s").reset_index(drop=True)

    if data["time_s"].diff().fillna(1).le(0).any():
        raise ValueError("Time values must not repeat or go backwards.")

    return data


def calculate_acceleration(data: pd.DataFrame) -> pd.DataFrame:
    """Calculate acceleration from vehicle speed and time."""
    data = data.copy()

    speed_mps = data["vehicle_speed_kmh"] / 3.6
    time_diff = data["time_s"].diff()
    speed_diff = speed_mps.diff()

    data["acceleration_mps2"] = speed_diff / time_diff
    data["acceleration_mps2"] = data["acceleration_mps2"].fillna(0)

    return data


def add_warning_columns(data: pd.DataFrame) -> pd.DataFrame:
    """Add warning/event columns based on engineering limits."""
    data = data.copy()

    data["high_temperature_warning"] = (
        data["motor_temperature_c"] > HIGH_TEMPERATURE_LIMIT
    )

    data["low_battery_warning"] = (
        data["battery_voltage_v"] < LOW_BATTERY_LIMIT
    )

    data["high_speed_event"] = (
        data["vehicle_speed_kmh"] > HIGH_SPEED_LIMIT
    )

    data["hard_acceleration_event"] = (
        data["acceleration_mps2"] > HARD_ACCELERATION_LIMIT
    )

    data["hard_braking_event"] = (
        data["acceleration_mps2"] < HARD_BRAKING_LIMIT
    )

    data["braking_event"] = data["brake_pressure_bar"] > 0

    return data


def analyze_data(data: pd.DataFrame) -> dict:
    """Calculate engineering statistics and warning counts."""
    return {
        "total_records": len(data),
        "total_duration_s": data["time_s"].max() - data["time_s"].min(),

        "average_speed": data["vehicle_speed_kmh"].mean(),
        "maximum_speed": data["vehicle_speed_kmh"].max(),
        "minimum_speed": data["vehicle_speed_kmh"].min(),

        "maximum_acceleration": data["acceleration_mps2"].max(),
        "minimum_acceleration": data["acceleration_mps2"].min(),

        "average_rpm": data["engine_rpm"].mean(),
        "maximum_rpm": data["engine_rpm"].max(),
        "minimum_rpm": data["engine_rpm"].min(),

        "average_temperature": data["motor_temperature_c"].mean(),
        "maximum_temperature": data["motor_temperature_c"].max(),
        "minimum_temperature": data["motor_temperature_c"].min(),

        "average_voltage": data["battery_voltage_v"].mean(),
        "maximum_voltage": data["battery_voltage_v"].max(),
        "minimum_voltage": data["battery_voltage_v"].min(),

        "high_temperature_warnings": int(data["high_temperature_warning"].sum()),
        "low_battery_warnings": int(data["low_battery_warning"].sum()),
        "high_speed_events": int(data["high_speed_event"].sum()),
        "hard_acceleration_events": int(data["hard_acceleration_event"].sum()),
        "hard_braking_events": int(data["hard_braking_event"].sum()),
        "braking_events": int(data["braking_event"].sum()),
    }


def create_single_signal_plot(
    data: pd.DataFrame,
    column: str,
    ylabel: str,
    title: str,
    filename: str,
) -> None:
    """Create and save one signal plot."""
    plt.figure(figsize=(9, 5))
    plt.plot(data["time_s"], data[column], linewidth=2)

    if column == "motor_temperature_c":
        plt.axhline(
            HIGH_TEMPERATURE_LIMIT,
            linestyle="--",
            label="High temperature limit",
        )
        plt.legend()

    if column == "battery_voltage_v":
        plt.axhline(
            LOW_BATTERY_LIMIT,
            linestyle="--",
            label="Low battery limit",
        )
        plt.legend()

    plt.xlabel("Time [s]")
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / filename, dpi=300, bbox_inches="tight")
    plt.close()


def create_throttle_brake_plot(data: pd.DataFrame) -> None:
    """Create a plot for throttle and brake pressure."""
    plt.figure(figsize=(9, 5))

    plt.plot(
        data["time_s"],
        data["throttle_percent"],
        linewidth=2,
        label="Throttle [%]",
    )

    plt.plot(
        data["time_s"],
        data["brake_pressure_bar"],
        linewidth=2,
        label="Brake Pressure [bar]",
    )

    plt.xlabel("Time [s]")
    plt.ylabel("Signal Value")
    plt.title("Throttle and Brake Signals")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "throttle_brake_plot.png", dpi=300, bbox_inches="tight")
    plt.close()


def create_dashboard_plot(data: pd.DataFrame) -> None:
    """Create one dashboard plot with the main automotive signals."""
    figure, axes = plt.subplots(4, 1, figsize=(10, 12), sharex=True)

    axes[0].plot(data["time_s"], data["vehicle_speed_kmh"], linewidth=2)
    axes[0].set_ylabel("Speed [km/h]")
    axes[0].set_title("Automotive Sensor Data Dashboard")
    axes[0].grid(True)

    axes[1].plot(data["time_s"], data["engine_rpm"], linewidth=2)
    axes[1].set_ylabel("Engine RPM")
    axes[1].grid(True)

    axes[2].plot(data["time_s"], data["motor_temperature_c"], linewidth=2)
    axes[2].axhline(
        HIGH_TEMPERATURE_LIMIT,
        linestyle="--",
        label="High temperature limit",
    )
    axes[2].set_ylabel("Temp [°C]")
    axes[2].legend()
    axes[2].grid(True)

    axes[3].plot(
        data["time_s"],
        data["throttle_percent"],
        linewidth=2,
        label="Throttle [%]",
    )
    axes[3].plot(
        data["time_s"],
        data["brake_pressure_bar"],
        linewidth=2,
        label="Brake Pressure [bar]",
    )
    axes[3].set_xlabel("Time [s]")
    axes[3].set_ylabel("Input Signals")
    axes[3].legend()
    axes[3].grid(True)

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "automotive_dashboard.png", dpi=300, bbox_inches="tight")
    plt.close(figure)


def create_plots(data: pd.DataFrame) -> None:
    """Create all automotive analysis plots."""
    OUTPUT_DIR.mkdir(exist_ok=True)

    create_single_signal_plot(
        data,
        "vehicle_speed_kmh",
        "Vehicle Speed [km/h]",
        "Vehicle Speed Over Time",
        "speed_plot.png",
    )

    create_single_signal_plot(
        data,
        "engine_rpm",
        "Engine RPM",
        "Engine RPM Over Time",
        "rpm_plot.png",
    )

    create_single_signal_plot(
        data,
        "motor_temperature_c",
        "Motor Temperature [°C]",
        "Motor Temperature Over Time",
        "temperature_plot.png",
    )

    create_single_signal_plot(
        data,
        "battery_voltage_v",
        "Battery Voltage [V]",
        "Battery Voltage Over Time",
        "battery_plot.png",
    )

    create_throttle_brake_plot(data)
    create_dashboard_plot(data)


def generate_report(data: pd.DataFrame, results: dict) -> None:
    """Generate automated automotive analysis report."""
    OUTPUT_DIR.mkdir(exist_ok=True)

    warning_columns = [
        "high_temperature_warning",
        "low_battery_warning",
        "high_speed_event",
        "hard_acceleration_event",
        "hard_braking_event",
    ]

    warning_events = data[data[warning_columns].any(axis=1)]

    warning_table_columns = [
        "time_s",
        "vehicle_speed_kmh",
        "engine_rpm",
        "battery_voltage_v",
        "motor_temperature_c",
        "acceleration_mps2",
        "high_temperature_warning",
        "low_battery_warning",
        "high_speed_event",
        "hard_acceleration_event",
        "hard_braking_event",
    ]

    report_text = f"""
Automotive Data Analysis Report
===============================

Dataset Summary
---------------
Total records: {results["total_records"]}
Total duration: {results["total_duration_s"]:.2f} s

Speed Analysis
--------------
Average speed: {results["average_speed"]:.2f} km/h
Maximum speed: {results["maximum_speed"]:.2f} km/h
Minimum speed: {results["minimum_speed"]:.2f} km/h
Maximum acceleration: {results["maximum_acceleration"]:.2f} m/s^2
Minimum acceleration: {results["minimum_acceleration"]:.2f} m/s^2

Engine RPM Analysis
-------------------
Average RPM: {results["average_rpm"]:.2f}
Maximum RPM: {results["maximum_rpm"]:.2f}
Minimum RPM: {results["minimum_rpm"]:.2f}

Motor Temperature Analysis
--------------------------
Average temperature: {results["average_temperature"]:.2f} °C
Maximum temperature: {results["maximum_temperature"]:.2f} °C
Minimum temperature: {results["minimum_temperature"]:.2f} °C
High temperature warnings: {results["high_temperature_warnings"]}

Battery Voltage Analysis
------------------------
Average battery voltage: {results["average_voltage"]:.2f} V
Maximum battery voltage: {results["maximum_voltage"]:.2f} V
Minimum battery voltage: {results["minimum_voltage"]:.2f} V
Low battery warnings: {results["low_battery_warnings"]}

Driving Behavior Analysis
-------------------------
High speed events: {results["high_speed_events"]}
Braking events: {results["braking_events"]}
Hard acceleration events: {results["hard_acceleration_events"]}
Hard braking events: {results["hard_braking_events"]}

Engineering Limits
------------------
High temperature limit: {HIGH_TEMPERATURE_LIMIT:.2f} °C
Low battery limit: {LOW_BATTERY_LIMIT:.2f} V
High speed limit: {HIGH_SPEED_LIMIT:.2f} km/h
Hard acceleration limit: {HARD_ACCELERATION_LIMIT:.2f} m/s^2
Hard braking limit: {HARD_BRAKING_LIMIT:.2f} m/s^2

Detected Warning Events
-----------------------
{warning_events[warning_table_columns].to_string(index=False) if not warning_events.empty else "No warning events detected."}

Generated Files
---------------
outputs/speed_plot.png
outputs/rpm_plot.png
outputs/temperature_plot.png
outputs/battery_plot.png
outputs/throttle_brake_plot.png
outputs/automotive_dashboard.png

Project Note
------------
This report was generated automatically using Python.
The project demonstrates automotive sensor data analysis, data validation,
warning detection, vehicle behavior evaluation, visualization,
and automated engineering reporting.
"""

    REPORT_FILE.write_text(report_text.strip() + "\n", encoding="utf-8")


def main() -> None:
    """Run the complete automotive data analysis workflow."""
    data = load_vehicle_data(DATA_FILE)
    data = calculate_acceleration(data)
    data = add_warning_columns(data)

    results = analyze_data(data)

    create_plots(data)
    generate_report(data, results)

    print("Automotive analysis completed successfully.")
    print(f"Report saved as: {REPORT_FILE}")
    print(f"Plots saved in: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
