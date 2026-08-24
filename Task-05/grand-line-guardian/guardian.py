#!/usr/bin/env python3
"""
Grand Line Guardian - Terminal-based Process Monitor
A Straw Hat Pirate-themed real-time process observer.
"""

import curses
import os
import signal
import sys
import time
from typing import Dict, List, Optional
import psutil


class ProcessMonitor:
    def __init__(self):
        self.selected_index = 0
        self.scroll_offset = 0
        self.sort_by = "cpu_percent"
        self.sort_reverse = True
        self.status_message = "Ready to navigate the Grand Line! Press 'h' for help."
        self.filter_query = ""
        self.is_filtering = False

    def get_system_metrics(self) -> Dict[str, float]:
        cpu_pct = psutil.cpu_percent(interval=None)
        mem = psutil.virtual_memory()
        swap = psutil.swap_memory()
        active_pids = len(psutil.pids())

        return {
            "cpu_percent": cpu_pct,
            "mem_percent": mem.percent,
            "mem_used_gb": mem.used / (1024**3),
            "mem_total_gb": mem.total / (1024**3),
            "swap_percent": swap.percent,
            "total_ships": active_pids,
        }

    def get_process_list(self) -> List[Dict]:
        processes = []
        for proc in psutil.process_iter(
            ["pid", "name", "username", "cpu_percent", "memory_percent", "status", "num_threads"]
        ):
            try:
                pinfo = proc.info
                pinfo["cpu_percent"] = pinfo["cpu_percent"] or 0.0
                pinfo["memory_percent"] = pinfo["memory_percent"] or 0.0

                if self.filter_query:
                    query = self.filter_query.lower()
                    if query not in str(pinfo["pid"]) and query not in (pinfo["name"] or "").lower():
                        continue

                processes.append(pinfo)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue

        processes.sort(key=lambda p: p.get(self.sort_by) or 0, reverse=self.sort_reverse)
        return processes

    def terminate_process(self, pid: int, force: bool = False) -> str:
        try:
            target_proc = psutil.Process(pid)
            proc_name = target_proc.name()
            sig = signal.SIGKILL if force else signal.SIGTERM
            os.kill(pid, sig)
            action = "Buster Call (SIGKILL)" if force else "Cannon Fire (SIGTERM)"
            return f"Success: Sent {action} to Ship [{proc_name}] (PID: {pid})."
        except psutil.NoSuchProcess:
            return f"Error: Ship (PID: {pid}) has already sunk into the sea."
        except psutil.AccessDenied:
            return f"Permission Denied: Insufficient Marine authority to scuttle Ship {pid} (Run as sudo)."
        except Exception as e:
            return f"Error scuttling Ship {pid}: {str(e)}"


def draw_bar(val: float, max_val: float = 100.0, width: int = 20) -> str:
    filled_len = int(width * (val / max_val))
    filled_len = max(0, min(width, filled_len))
    return f"[{'#' * filled_len}{'.' * (width - filled_len)}] {val:5.1f}%"


def run_guardian(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(500)

    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_CYAN, -1)     # Header / Title
    curses.init_pair(2, curses.COLOR_GREEN, -1)    # Metrics / Normal
    curses.init_pair(3, curses.COLOR_YELLOW, -1)   # Warnings / Table Headers
    curses.init_pair(4, curses.COLOR_RED, -1)      # High Usage / Danger
    curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_CYAN)  # Selected Row
    curses.init_pair(6, curses.COLOR_MAGENTA, -1)  # Accents

    monitor = ProcessMonitor()
    psutil.cpu_percent(interval=None)

    last_refresh = 0.0
    refresh_rate = 0.75
    proc_list = []
    sys_metrics = monitor.get_system_metrics()

    while True:
        current_time = time.time()
        if current_time - last_refresh >= refresh_rate:
            sys_metrics = monitor.get_system_metrics()
            proc_list = monitor.get_process_list()
            last_refresh = current_time

        max_y, max_x = stdscr.getmaxyx()
        stdscr.erase()

        if max_y < 15 or max_x < 80:
            stdscr.addstr(0, 0, "Terminal window too small! Minimum size: 80x15.", curses.color_pair(4))
            stdscr.refresh()
            time.sleep(0.2)
            continue

        # Header: Pirate Flag & Log Pose
        title = " ☠  GRAND LINE GUARDIAN | Straw Hat Navigational Radar ☠ "
        stdscr.attron(curses.color_pair(1) | curses.A_BOLD)
        stdscr.addstr(0, max(0, (max_x - len(title)) // 2), title[:max_x])
        stdscr.attroff(curses.color_pair(1) | curses.A_BOLD)

        # System Metrics Dashboard
        cpu_color = curses.color_pair(4) if sys_metrics["cpu_percent"] > 80 else curses.color_pair(2)
        mem_color = curses.color_pair(4) if sys_metrics["mem_percent"] > 80 else curses.color_pair(2)

        cpu_str = f"Wind Resistance (CPU) : {draw_bar(sys_metrics['cpu_percent'], 100, 16)}"
        mem_str = f"Cargo Load      (RAM) : {draw_bar(sys_metrics['mem_percent'], 100, 16)} ({sys_metrics['mem_used_gb']:.1f}/{sys_metrics['mem_total_gb']:.1f} GB)"
        ships_str = f"Active Fleet    (PIDs): {sys_metrics['total_ships']} ships in transit"

        stdscr.addstr(2, 2, cpu_str[:max_x - 4], cpu_color)
        stdscr.addstr(3, 2, mem_str[:max_x - 4], mem_color)
        stdscr.addstr(4, 2, ships_str[:max_x - 4], curses.color_pair(6) | curses.A_BOLD)

        filter_status = f" | Filter: '{monitor.filter_query}'" if monitor.filter_query else ""
        sort_status = f"Sorted by: {monitor.sort_by} ({'DESC' if monitor.sort_reverse else 'ASC'}){filter_status}"
        stdscr.addstr(4, max(40, max_x - len(sort_status) - 4), sort_status, curses.color_pair(3))

        # Table Header
        table_top = 6
        header = f"{'PID':>8}  {'CAPTAIN (USER)':<14} {'CPU %':>7} {'MEM %':>7} {'STATUS':<10} {'SHIP NAME (COMMAND)':<30}"
        stdscr.attron(curses.color_pair(3) | curses.A_REVERSE)
        stdscr.addstr(table_top, 2, header[:max_x - 4].ljust(max_x - 4))
        stdscr.attroff(curses.color_pair(3) | curses.A_REVERSE)

        # Process Table Rows
        visible_rows = max_y - table_top - 4
        if visible_rows > 0 and proc_list:
            if monitor.selected_index >= len(proc_list):
                monitor.selected_index = max(0, len(proc_list) - 1)

            if monitor.selected_index < monitor.scroll_offset:
                monitor.scroll_offset = monitor.selected_index
            elif monitor.selected_index >= monitor.scroll_offset + visible_rows:
                monitor.scroll_offset = monitor.selected_index - visible_rows + 1

            for idx in range(visible_rows):
                p_idx = monitor.scroll_offset + idx
                if p_idx >= len(proc_list):
                    break

                proc = proc_list[p_idx]
                pid = proc["pid"]
                user = (proc["username"] or "unknown")[:14]
                cpu_p = proc["cpu_percent"]
                mem_p = proc["memory_percent"]
                status = (proc["status"] or "unknown")[:10]
                name = (proc["name"] or "unknown")[:max_x - 55]

                row_str = f"{pid:>8}  {user:<14} {cpu_p:>7.1f} {mem_p:>7.1f} {status:<10} {name:<30}"
                row_y = table_top + 1 + idx

                if p_idx == monitor.selected_index:
                    stdscr.attron(curses.color_pair(5) | curses.A_BOLD)
                    stdscr.addstr(row_y, 2, row_str[:max_x - 4].ljust(max_x - 4))
                    stdscr.attroff(curses.color_pair(5) | curses.A_BOLD)
                else:
                    stdscr.addstr(row_y, 2, row_str[:max_x - 4])

        # Status Bar & Controls Footer
        status_y = max_y - 2
        stdscr.attron(curses.color_pair(6))
        stdscr.addstr(status_y - 1, 2, f"LOG: {monitor.status_message}"[:max_x - 4])
        stdscr.attroff(curses.color_pair(6))

        controls = "[↑/↓/j/k]: Navigate | [k]: Fire (SIGTERM) | [9]: Buster Call (SIGKILL) | [c]: Sort CPU | [m]: Sort MEM | [/]: Filter | [q]: Retreat"
        stdscr.addstr(status_y, 2, controls[:max_x - 4], curses.color_pair(3))

        stdscr.refresh()

        # Input Handling
        try:
            key = stdscr.getch()
        except curses.error:
            key = -1

        if key == -1:
            continue

        if key in (ord('q'), ord('Q')):
            break
        elif key in (curses.KEY_UP, ord('k'), ord('K')):
            if monitor.selected_index > 0:
                monitor.selected_index -= 1
        elif key in (curses.KEY_DOWN, ord('j'), ord('J')):
            if monitor.selected_index < len(proc_list) - 1:
                monitor.selected_index += 1
        elif key == curses.KEY_PPAGE:
            monitor.selected_index = max(0, monitor.selected_index - visible_rows)
        elif key == curses.KEY_NPAGE:
            monitor.selected_index = min(max(0, len(proc_list) - 1), monitor.selected_index + visible_rows)
        elif key in (ord('c'), ord('C')):
            if monitor.sort_by == "cpu_percent":
                monitor.sort_reverse = not monitor.sort_reverse
            else:
                monitor.sort_by = "cpu_percent"
                monitor.sort_reverse = True
            monitor.status_message = f"Sorting by CPU% ({'DESC' if monitor.sort_reverse else 'ASC'})"
        elif key in (ord('m'), ord('M')):
            if monitor.sort_by == "memory_percent":
                monitor.sort_reverse = not monitor.sort_reverse
            else:
                monitor.sort_by = "memory_percent"
                monitor.sort_reverse = True
            monitor.status_message = f"Sorting by MEM% ({'DESC' if monitor.sort_reverse else 'ASC'})"
        elif key in (ord('p'), ord('P')):
            if monitor.sort_by == "pid":
                monitor.sort_reverse = not monitor.sort_reverse
            else:
                monitor.sort_by = "pid"
                monitor.sort_reverse = False
            monitor.status_message = f"Sorting by PID ({'DESC' if monitor.sort_reverse else 'ASC'})"
        elif key == ord('x') or key == ord('k'):
            if proc_list and 0 <= monitor.selected_index < len(proc_list):
                target_pid = proc_list[monitor.selected_index]["pid"]
                monitor.status_message = monitor.terminate_process(target_pid, force=False)
                proc_list = monitor.get_process_list()
        elif key == ord('9'):
            if proc_list and 0 <= monitor.selected_index < len(proc_list):
                target_pid = proc_list[monitor.selected_index]["pid"]
                monitor.status_message = monitor.terminate_process(target_pid, force=True)
                proc_list = monitor.get_process_list()
        elif key == ord('/'):
            # Text prompt for filtering
            curses.echo()
            curses.curs_set(1)
            stdscr.addstr(status_y, 2, "Search Ship / PID (Press Enter): " + " " * 30, curses.color_pair(3))
            stdscr.refresh()
            filter_input = stdscr.getstr(status_y, 35, 20).decode("utf-8").strip()
            monitor.filter_query = filter_input
            monitor.selected_index = 0
            curses.noecho()
            curses.curs_set(0)
            monitor.status_message = f"Filter applied: '{filter_input}'" if filter_input else "Filter cleared."


def main():
    try:
        curses.wrapper(run_guardian)
    except KeyboardInterrupt:
        pass
    print("Grand Line Guardian docked safely. Farewell, Captain!")


if __name__ == "__main__":
    main()