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

SPEED_PLOT_FILE = OUTPUT_DIR / "speed_plot.png"
RPM_PLOT_FILE = OUTPUT_DIR / "rpm_plot.png"
TEMPERATURE_PLOT_FILE = OUTPUT_DIR / "temperature_plot.png"
BATTERY_PLOT_FILE = OUTPUT_DIR / "battery_plot.png"
THROTTLE_BRAKE_PLOT_FILE = OUTPUT_DIR / "throttle_brake_plot.png"
DASHBOARD_FILE = OUTPUT_DIR / "automotive_dashboard.png"

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
        raise FileNotFoundError(f"Input file not found: {file_path}")

    dataframe = pd.read_csv(file_path)

    missing_columns = [
        column for column in REQUIRED_COLUMNS if column not in dataframe.columns
    ]

    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    dataframe = dataframe.copy()

    for column in REQUIRED_COLUMNS:
        dataframe[column] = pd.to_numeric(dataframe[column], errors="coerce")

    if dataframe[REQUIRED_COLUMNS].isnull().any().any():
        raise ValueError("The dataset contains missing or non-numeric values.")

    dataframe = dataframe.sort_values("time_s").reset_index(drop=True)

    if dataframe["time_s"].duplicated().any():
        raise ValueError("Duplicate time values detected.")

    if (dataframe["time_s"].diff().dropna() <= 0).any():
        raise ValueError("Time values must be strictly increasing.")

    return dataframe


def calculate_acceleration(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Calculate acceleration from vehicle speed and time data."""
    dataframe = dataframe.copy()

    speed_mps = dataframe["vehicle_speed_kmh"] / 3.6
    time_diff = dataframe["time_s"].diff()
    speed_diff = speed_mps.diff()

    dataframe["acceleration_mps2"] = speed_diff / time_diff
    dataframe["acceleration_mps2"] = dataframe["acceleration_mps2"].fillna(0)

    return dataframe


def detect_warning_conditions(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Add warning columns based on engineering limits."""
    dataframe = dataframe.copy()

    dataframe["high_temperature_warning"] = (
        dataframe["motor_temperature_c"] > HIGH_TEMPERATURE_LIMIT
    )

    dataframe["low_battery_warning"] = (
        dataframe["battery_voltage_v"] < LOW_BATTERY_LIMIT
    )

    dataframe["high_speed_event"] = (
        dataframe["vehicle_speed_kmh"] > HIGH_SPEED_LIMIT
    )

    dataframe["hard_acceleration_event"] = (
        dataframe["acceleration_mps2"] > HARD_ACCELERATION_LIMIT
    )

    dataframe["hard_braking_event"] = (
        dataframe["acceleration_mps2"] < HARD_BRAKING_LIMIT
    )

    return dataframe


def analyze_vehicle_data(dataframe: pd.DataFrame) -> dict:
    """Calculate main automotive engineering statistics."""
    analysis = {
        "total_records": len(dataframe),
        "total_duration_s": dataframe["time_s"].max() - dataframe["time_s"].min(),
        "average_speed_kmh": dataframe["vehicle_speed_kmh"].mean(),
        "maximum_speed_kmh": dataframe["vehicle_speed_kmh"].max(),
        "minimum_speed_kmh": dataframe["vehicle_speed_kmh"].min(),
        "average_rpm": dataframe["engine_rpm"].mean(),
        "maximum_rpm": dataframe["engine_rpm"].max(),
        "minimum_rpm": dataframe["engine_rpm"].min(),
        "average_temperature_c": dataframe["motor_temperature_c"].mean(),
        "maximum_temperature_c": dataframe["motor_temperature_c"].max(),
        "average_battery_voltage_v": dataframe["battery_voltage_v"].mean(),
        "minimum_battery_voltage_v": dataframe["battery_voltage_v"].min(),
        "maximum_acceleration_mps2": dataframe["acceleration_mps2"].max(),
        "minimum_acceleration_mps2": dataframe["acceleration_mps2"].min(),
        "high_temperature_warnings": int(
            dataframe["high_temperature_warning"].sum()
        ),
        "low_battery_warnings": int(dataframe["low_battery_warning"].sum()),
        "high_speed_events": int(dataframe["high_speed_event"].sum()),
        "hard_acceleration_events": int(
            dataframe["hard_acceleration_event"].sum()
        ),
        "hard_braking_events": int(dataframe["hard_braking_event"].sum()),
    }

    return analysis


def create_line_plot(
    dataframe: pd.DataFrame,
    y_column: str,
    title: str,
    y_label: str,
    output_file: Path,
) -> None:
    """Create and save a simple line plot."""
    plt.figure(figsize=(9, 5))
    plt.plot(dataframe["time_s"], dataframe[y_column])
    plt.title(title)
    plt.xlabel("Time [s]")
    plt.ylabel(y_label)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output_file, dpi=300)
    plt.close()


def create_throttle_brake_plot(dataframe: pd.DataFrame) -> None:
    """Create a plot for throttle and brake pressure."""
    plt.figure(figsize=(9, 5))
    plt.plot(dataframe["time_s"], dataframe["throttle_percent"], label="Throttle [%]")
    plt.plot(dataframe["time_s"], dataframe["brake_pressure_bar"], label="Brake Pressure [bar]")
    plt.title("Throttle and Brake Signals")
    plt.xlabel("Time [s]")
    plt.ylabel("Signal Value")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(THROTTLE_BRAKE_PLOT_FILE, dpi=300)
    plt.close()


def create_dashboard(dataframe: pd.DataFrame) -> None:
    """Create one dashboard-style figure with the most important vehicle signals."""
    fig, axes = plt.subplots(3, 2, figsize=(14, 10))

    axes[0, 0].plot(dataframe["time_s"], dataframe["vehicle_speed_kmh"])
    axes[0, 0].set_title("Vehicle Speed")
    axes[0, 0].set_ylabel("km/h")
    axes[0, 0].grid(True)

    axes[0, 1].plot(dataframe["time_s"], dataframe["engine_rpm"])
    axes[0, 1].set_title("Engine RPM")
    axes[0, 1].set_ylabel("rpm")
    axes[0, 1].grid(True)

    axes[1, 0].plot(dataframe["time_s"], dataframe["motor_temperature_c"])
    axes[1, 0].axhline(HIGH_TEMPERATURE_LIMIT, linestyle="--")
    axes[1, 0].set_title("Motor Temperature")
    axes[1, 0].set_ylabel("°C")
    axes[1, 0].grid(True)

    axes[1, 1].plot(dataframe["time_s"], dataframe["battery_voltage_v"])
    axes[1, 1].axhline(LOW_BATTERY_LIMIT, linestyle="--")
    axes[1, 1].set_title("Battery Voltage")
    axes[1, 1].set_ylabel("V")
    axes[1, 1].grid(True)

    axes[2, 0].plot(dataframe["time_s"], dataframe["throttle_percent"], label="Throttle [%]")
    axes[2, 0].plot(dataframe["time_s"], dataframe["brake_pressure_bar"], label="Brake [bar]")
    axes[2, 0].set_title("Throttle and Brake")
    axes[2, 0].set_xlabel("Time [s]")
    axes[2, 0].legend()
    axes[2, 0].grid(True)

    axes[2, 1].plot(dataframe["time_s"], dataframe["acceleration_mps2"])
    axes[2, 1].axhline(HARD_ACCELERATION_LIMIT, linestyle="--")
    axes[2, 1].axhline(HARD_BRAKING_LIMIT, linestyle="--")
    axes[2, 1].set_title("Acceleration")
    axes[2, 1].set_xlabel("Time [s]")
    axes[2, 1].set_ylabel("m/s²")
    axes[2, 1].grid(True)

    fig.suptitle("Automotive Sensor Data Dashboard", fontsize=16)
    plt.tight_layout()
    plt.savefig(DASHBOARD_FILE, dpi=300)
    plt.close()


def create_plots(dataframe: pd.DataFrame) -> None:
    """Create all project plots."""
    OUTPUT_DIR.mkdir(exist_ok=True)

    create_line_plot(
        dataframe,
        "vehicle_speed_kmh",
        "Vehicle Speed Over Time",
        "Speed [km/h]",
        SPEED_PLOT_FILE,
    )

    create_line_plot(
        dataframe,
        "engine_rpm",
        "Engine RPM Over Time",
        "Engine RPM",
        RPM_PLOT_FILE,
    )

    create_line_plot(
        dataframe,
        "motor_temperature_c",
        "Motor Temperature Over Time",
        "Temperature [°C]",
        TEMPERATURE_PLOT_FILE,
    )

    create_line_plot(
        dataframe,
        "battery_voltage_v",
        "Battery Voltage Over Time",
        "Battery Voltage [V]",
        BATTERY_PLOT_FILE,
    )

    create_throttle_brake_plot(dataframe)
    create_dashboard(dataframe)


def generate_report(dataframe: pd.DataFrame, analysis: dict) -> None:
    """Generate an automated engineering report."""
    OUTPUT_DIR.mkdir(exist_ok=True)

    warning_rows = dataframe[
        dataframe[
            [
                "high_temperature_warning",
                "low_battery_warning",
                "high_speed_event",
                "hard_acceleration_event",
                "hard_braking_event",
            ]
        ].any(axis=1)
    ]

    report_text = f"""
Automotive Data Analysis Report
========================================

Dataset Summary
----------------------------------------
Total records: {analysis["total_records"]}
Total duration: {analysis["total_duration_s"]:.2f} s

Speed Analysis
----------------------------------------
Average speed: {analysis["average_speed_kmh"]:.2f} km/h
Maximum speed: {analysis["maximum_speed_kmh"]:.2f} km/h
Minimum speed: {analysis["minimum_speed_kmh"]:.2f} km/h

Engine RPM Analysis
----------------------------------------
Average RPM: {analysis["average_rpm"]:.2f}
Maximum RPM: {analysis["maximum_rpm"]:.2f}
Minimum RPM: {analysis["minimum_rpm"]:.2f}

Temperature Analysis
----------------------------------------
Average motor temperature: {analysis["average_temperature_c"]:.2f} °C
Maximum motor temperature: {analysis["maximum_temperature_c"]:.2f} °C
High temperature warnings: {analysis["high_temperature_warnings"]}

Battery Analysis
----------------------------------------
Average battery voltage: {analysis["average_battery_voltage_v"]:.2f} V
Minimum battery voltage: {analysis["minimum_battery_voltage_v"]:.2f} V
Low battery warnings: {analysis["low_battery_warnings"]}

Driving Behavior Analysis
----------------------------------------
Maximum acceleration: {analysis["maximum_acceleration_mps2"]:.2f} m/s²
Minimum acceleration: {analysis["minimum_acceleration_mps2"]:.2f} m/s²
High-speed events: {analysis["high_speed_events"]}
Hard acceleration events: {analysis["hard_acceleration_events"]}
Hard braking events: {analysis["hard_braking_events"]}

Engineering Limits
----------------------------------------
High temperature limit: {HIGH_TEMPERATURE_LIMIT:.2f} °C
Low battery limit: {LOW_BATTERY_LIMIT:.2f} V
High speed limit: {HIGH_SPEED_LIMIT:.2f} km/h
Hard acceleration limit: {HARD_ACCELERATION_LIMIT:.2f} m/s²
Hard braking limit: {HARD_BRAKING_LIMIT:.2f} m/s²

Detected Warning Events
----------------------------------------
{warning_rows.to_string(index=False) if not warning_rows.empty else "No warning events detected."}

Generated Files
----------------------------------------
{SPEED_PLOT_FILE}
{RPM_PLOT_FILE}
{TEMPERATURE_PLOT_FILE}
{BATTERY_PLOT_FILE}
{THROTTLE_BRAKE_PLOT_FILE}
{DASHBOARD_FILE}

Project Note
----------------------------------------
This project demonstrates CSV-based automotive sensor data analysis,
data validation, warning detection, engineering calculations,
visualization, and automated report generation with Python.
"""

    REPORT_FILE.write_text(report_text.strip() + "\n", encoding="utf-8")


def main() -> None:
    dataframe = load_vehicle_data(DATA_FILE)
    dataframe = calculate_acceleration(dataframe)
    dataframe = detect_warning_conditions(dataframe)

    analysis = analyze_vehicle_data(dataframe)

    create_plots(dataframe)
    generate_report(dataframe, analysis)

    print("Automotive analysis completed successfully.")
    print(f"Report saved as: {REPORT_FILE}")
    print(f"Plots saved in: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
