#!/usr/bin/env python3
"""把独立的功夫固定姿态 CEM 结果定点追加到既有离线报告。

只写指定报告的 index.html；不重建既有数据、筛选页或原始资产。
重复运行替换自己的标记块，输出字节保持一致。所有图表在 Python 中
生成，新增部分不依赖 JavaScript、网络、服务端或第三方库。

数据布局：study.json、tasks.json、eval/*.json、search/<task>.json、
original/<task>_z.csv、optimized/<task>_z.csv，以及可选 videos/。
"""
from __future__ import annotations

import argparse
import hashlib
import html
from html.parser import HTMLParser
import json
import math
import os
from pathlib import Path
import re
import statistics
from typing import Any
from urllib.parse import quote, unquote, urlsplit


DEFAULT_REPORT = Path("outputs/astro-payload-cem-2026-11-13")
SECTION_ID = "kungfu-payload-cem"
BEGIN = "<!-- BEGIN KUNGFU PAYLOAD CEM APPEND -->"
END = "<!-- END KUNGFU PAYLOAD CEM APPEND -->"
NAV_BEGIN = "<!-- BEGIN KUNGFU PAYLOAD CEM NAV -->"
NAV_END = "<!-- END KUNGFU PAYLOAD CEM NAV -->"
OPTIONAL_METRICS = {
    "root_height_m": ("实际 root 高度 m", 3),
    "actual_root_height_m": ("实际 root 高度 m", 3),
    "lift_height_m": ("抬脚高度 m", 3),
    "support_fraction": ("支撑达标比例", 3),
    "depth_fraction": ("蹲深达标比例", 3),
    "mean_knee_angle_rad": ("平均膝角 rad", 3),
    "left_knee_angle_rad": ("左膝角 rad", 3),
    "right_knee_angle_rad": ("右膝角 rad", 3),
    "knee_angle_rad": ("膝关节角 rad", 3),
    "height_error_m": ("高度误差 m", 3),
    "key_body_error_m": ("局部 body 误差 m", 3),
    "slip_mps": ("脚滑 m/s", 3),
    "tilt_deg": ("平均倾角 °", 2),
    "torque_saturation_fraction": ("力矩饱和比例", 4),
    "undesired_contact_fraction": ("非脚接触比例", 4),
    "final_hold": ("终帧保持比例", 3),
    "last_second_hold_fraction": ("末1秒保持比例", 3),
    "last_second_support_fraction": ("末1秒支撑比例", 3),
    "last_second_depth_fraction": ("末1秒深度比例", 3),
}
TAIL_METRICS = ("last_second_hold_fraction", "last_second_support_fraction",
                "last_second_depth_fraction", "final_hold")


def escape(value: Any) -> str:
    return html.escape(str(value), quote=True)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> Any:
    with path.open(encoding="utf-8") as file:
        return json.load(file)


def finite(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def number(value: Any, digits: int = 3) -> str:
    if finite(value):
        return f"{value:.{digits}f}"
    if isinstance(value, (list, tuple)):
        return " / ".join(number(item, digits) for item in value)
    return "未记录"


def average(rows: list[dict[str, Any]], key: str) -> float | list[float] | None:
    values = [row[key] for row in rows if key in row]
    if values and all(isinstance(value, bool) for value in values):
        return statistics.mean(float(value) for value in values)
    if values and all(finite(value) for value in values):
        return statistics.mean(values)
    if values and all(isinstance(value, list) for value in values):
        widths = {len(value) for value in values}
        if len(widths) == 1 and all(all(finite(x) for x in value) for value in values):
            return [statistics.mean(value[i] for value in values) for i in range(len(values[0]))]
    return None


def normalized_payload(payload: dict[str, Any]) -> tuple[float, tuple[float, ...]]:
    mass, offset = payload.get("mass_kg"), payload.get("offset_m")
    if not finite(mass) or mass < 0:
        raise ValueError(f"无效负载质量：{mass!r}")
    if not isinstance(offset, list) or len(offset) != 3 or not all(finite(x) for x in offset):
        raise ValueError(f"offset_m 必须为三个有限数：{offset!r}")
    # 无负载时安装偏移没有物理含义，避免把同一 A/D 条件显示为多组。
    return round(float(mass), 8), tuple(round(float(x), 8) for x in offset) if mass else (0., 0., 0.)


def payload_label(payload: dict[str, Any]) -> str:
    mass, offset = normalized_payload(payload)
    if mass == 0:
        return "无负载"
    return f"{mass:g} kg；偏移 ({', '.join(f'{x:g}' for x in offset)}) m"


def href(path: Path, report: Path) -> str:
    resolved, root = path.resolve(), report.resolve()
    if not resolved.is_relative_to(root):
        raise ValueError(f"证据文件必须在离线报告目录内：{path}")
    return quote(os.path.relpath(resolved, root).replace(os.sep, "/"), safe="/-._~")


def link(path: Path, report: Path, label: str) -> str:
    if not path.is_file():
        return f'<span class="kfc-muted">{escape(label)}：未归档</span>'
    return f'<a href="{escape(href(path, report))}">{escape(label)}</a>'


def remove_block(page: str, begin: str, end: str) -> str:
    if page.count(begin) != page.count(end) or page.count(begin) > 1:
        raise ValueError(f"追加标记不完整或重复：{begin}")
    if begin in page:
        start, stop = page.index(begin), page.index(end) + len(end)
        return page[:start] + page[stop:]
    return page


def strip_own_blocks(page: str) -> str:
    return remove_block(remove_block(page, BEGIN, END), NAV_BEGIN, NAV_END)


def read_dataset(results: Path, report: Path) -> dict[str, Any]:
    if not results.resolve().is_relative_to(report.resolve()):
        raise ValueError("结果目录必须位于报告目录内，确保离线复制后链接可用")
    study = load(results / "study.json")
    task_data = load(results / "tasks.json")
    tasks = task_data.get("tasks", []) if isinstance(task_data, dict) else task_data
    if not isinstance(tasks, list) or not isinstance(study.get("tasks"), list):
        raise ValueError("tasks.json 与 study.json 必须包含任务列表")
    meta = {str(task["name"]): task for task in tasks}
    if len(meta) != len(tasks):
        raise ValueError("tasks.json 中任务 name 重复")
    evaluations, keys = [], set()
    for path in sorted((results / "eval").glob("*.json")):
        value = load(path)
        if not isinstance(value, dict) or "task" not in value:
            raise ValueError(f"不是 run.py 评估格式：{path}")
        rows, protocol = value.get("rows", []), value.get("protocol", {})
        if not isinstance(rows, list) or not rows:
            raise ValueError(f"评估 rows 为空：{path}")
        if any(not isinstance(row.get("success"), bool) for row in rows):
            raise ValueError(f"评估缺少显式布尔 success，不根据保持比例猜测成功：{path}")
        seeds = protocol.get("seeds")
        if seeds is not None and sorted(seeds) != sorted(row.get("seed") for row in rows):
            raise ValueError(f"protocol.seeds 与逐行 seed 不一致：{path}")
        if len({row.get("seed") for row in rows}) != len(rows):
            raise ValueError(f"同次评估 seed 重复：{path}")
        payload = value.get("physics", {}).get("payload") or protocol.get("physics", {}).get("payload")
        if not payload:
            raise ValueError(f"评估缺少 payload：{path}")
        condition = {"z0": "original", "optimized": "cem", "zstar": "cem"}.get(value.get("condition"), value.get("condition"))
        if condition not in {"original", "cem"}:
            raise ValueError(f"未知 condition：{value.get('condition')!r}，{path}")
        key = (str(value["task"]), condition, normalized_payload(payload))
        if key in keys:
            raise ValueError(f"同任务/条件/负载存在重复评估，必须先明确选用协议：{path}")
        keys.add(key)
        evaluations.append({
            **value, "condition": condition, "payload": payload,
            "source": href(path, report), "n": len(rows),
            "successes": sum(row["success"] for row in rows),
            "hold_fraction": average(rows, "hold_fraction"),
            "joint_mae_rad": average(rows, "joint_mae_rad"),
            "max_drift_m": average(rows, "max_drift_m"),
            "optional_metrics": {key: average(rows, key) for key in OPTIONAL_METRICS},
        })
    searches, provenance = {}, {}
    seen_study_names = set()
    for item in study["tasks"]:
        name = str(item["name"])
        if name in seen_study_names:
            raise ValueError(f"study.json 任务 name 重复：{name}")
        seen_study_names.add(name)
        if name not in meta:
            raise ValueError(f"study.json 任务在 tasks.json 中不存在：{name}")
        if item.get("baseline_eligible") is True:
            normalized_payload(item["main_payload"])
            if item["main_payload"]["mass_kg"] <= 0:
                raise ValueError(f"主实验负载必须大于零：{name}")
        search_path = results / "search" / f"{name}.json"
        if search_path.is_file():
            searches[name] = {**load(search_path), "source": href(search_path, report)}
        original = next((p for p in (results / "original" / f"{name}_z.csv", results / "original" / f"{name}.csv") if p.is_file()), None)
        declared = meta[name].get("original_z_sha256")
        actual = digest(original) if original else None
        if declared and actual and declared != actual:
            raise ValueError(f"原始 z₀ 文件 SHA256 与元数据不同：{name}")
        provenance[name] = {"declared_original_z_sha256": declared, "actual_original_z_sha256": actual,
                            "original_path": href(original, report) if original else None}
    return {"study": study, "tasks": tasks, "evaluations": evaluations,
            "search": searches, "provenance": provenance}


def evaluation_table(rows: list[tuple[str, dict[str, Any] | None]], report: Path) -> str:
    head = "<thead><tr><th>对照 / 负载</th><th>成功</th><th>保持</th><th>关节 MAE rad</th><th>最大位移均值 m</th><th>逐种子证据</th></tr></thead>"
    body = []
    for label, result in rows:
        if result is None:
            body.append(f'<tr><td>{escape(label)}</td><td colspan="5" class="kfc-muted">未测试，不纳入成功率</td></tr>')
            continue
        hold = result.get("hold_fraction")
        body.append(f'<tr><td>{escape(label)}<br><small>{escape(payload_label(result["payload"]))}</small></td>'
                    f'<td><b>{result["successes"]}/{result["n"]}</b></td>'
                    f'<td>{number(100 * hold, 1) + "%" if finite(hold) else "未记录"}</td>'
                    f'<td>{number(result.get("joint_mae_rad"))}</td><td>{number(result.get("max_drift_m"))}</td>'
                    f'<td><a href="{escape(result["source"])}">JSON</a></td></tr>')
    return f'<div class="kfc-scroll"><table>{head}<tbody>{"".join(body)}</tbody></table></div>'


def hold_chart(rows: list[tuple[str, dict[str, Any] | None]], task_title: str) -> str:
    present = [(label, result) for label, result in rows if result is not None and finite(result.get("hold_fraction"))]
    if not present:
        return '<p class="kfc-muted">尚无保持比例，未绘制对照图。</p>'
    width, height = 850, 42 * len(present) + 50
    svg = [f'<svg viewBox="0 0 {width} {height}" role="img" aria-label="{escape(task_title)}四组保持比例"><title>{escape(task_title)}四组保持比例</title>']
    colors = ["#778f9c", "#c67b41", "#218270", "#497da5"]
    for percent in (0, 25, 50, 75, 100):
        x = 245 + percent * 4.9
        svg.append(f'<line x1="{x}" x2="{x}" y1="8" y2="{height-30}" stroke="#dce5e8"/><text x="{x}" y="{height-8}" text-anchor="middle" font-size="13">{percent}%</text>')
    for i, (label, result) in enumerate(present):
        hold = result["hold_fraction"]
        if not 0 <= hold <= 1:
            raise ValueError(f"hold_fraction 超出 [0,1]：{hold}")
        y = i * 42 + 15
        svg.append(f'<text x="230" y="{y+18}" text-anchor="end" font-size="13">{escape(label)}</text>'
                   f'<rect x="245" y="{y}" width="{hold*490}" height="25" rx="3" fill="{colors[i%4]}"/>'
                   f'<text x="{255+hold*490}" y="{y+18}" font-size="13">{hold*100:.1f}%</text>')
    return "".join(svg) + "</svg>"


def search_chart(search: dict[str, Any] | None, title: str) -> str:
    if not search:
        return '<p class="kfc-muted">尚无 CEM 搜索记录，不能据此声称已完成负载优化。</p>'
    history = search.get("history", [])
    if not history:
        return '<p class="kfc-muted">搜索记录 history 为空，未绘制曲线。</p>'
    curves = [("best_score", "最佳候选", "#218270"), ("anchor_score", "原始 z₀", "#c67b41"), ("median_score", "候选中位数", "#758f9e")]
    points = [x[key] for x in history for key, _, _ in curves if finite(x.get(key))]
    if not points:
        return '<p class="kfc-muted">没有有限搜索分数，未绘制曲线。</p>'
    low, high = min(points), max(points)
    padding = max((high - low) * .06, .1)
    low, high = low - padding, high + padding
    X = lambda i: 75 + i * 685 / max(1, len(history) - 1)
    Y = lambda value: 220 - (value - low) * 175 / (high - low)
    svg = [f'<svg viewBox="0 0 850 280" role="img" aria-label="{escape(title)} CEM搜索曲线"><title>{escape(title)} CEM搜索分数，越高越好</title>']
    for j in range(5):
        value = low + j * (high - low) / 4
        svg.append(f'<line x1="75" x2="770" y1="{Y(value)}" y2="{Y(value)}" stroke="#e2e8eb"/><text x="65" y="{Y(value)+4}" text-anchor="end" font-size="12">{value:.2f}</text>')
    for key, label, color in curves:
        commands, previous = [], False
        for i, row in enumerate(history):
            if not finite(row.get(key)):
                previous = False
                continue
            commands.append(f'{"L" if previous else "M"}{X(i):.2f},{Y(row[key]):.2f}')
            previous = True
        if commands:
            svg.append(f'<path d="{" ".join(commands)}" fill="none" stroke="{color}" stroke-width="2.5"/>')
    svg.extend([f'<text x="75" y="245" font-size="12">第 {escape(history[0].get("iteration", 1))} 代</text>',
                f'<text x="760" y="245" text-anchor="end" font-size="12">第 {escape(history[-1].get("iteration",len(history)))} 代</text>'])
    for i, (_, label, color) in enumerate(curves):
        svg.append(f'<text x="{75+i*210}" y="270" fill="{color}" font-size="13">— {label}</text>')
    config = search.get("config", {})
    budget = "；".join(f"{key}={config[key]}" for key in ("population", "elites", "iterations", "sigma", "max_angle", "seed") if key in config)
    source = f'<a href="{escape(search["source"])}">搜索逐代数据</a>'
    return "".join(svg) + f'</svg><p class="kfc-meta">{escape(budget)}；耗时 {number(search.get("elapsed_s"),1)} s。{source}。分数包含姿态与稳定性约束，不能替代独立验证成功率。</p>'


def notes_html(notes: Any) -> str:
    if notes is None:
        return "<p>未提供额外筛选说明。</p>"
    if isinstance(notes, str):
        return f"<p>{escape(notes)}</p>"
    if isinstance(notes, list):
        return "<ul>" + "".join(f"<li>{escape(n) if isinstance(n,str) else escape(json.dumps(n,ensure_ascii=False))}</li>" for n in notes) + "</ul>"
    return f'<pre>{escape(json.dumps(notes,ensure_ascii=False,indent=2))}</pre>'


def render_section(data: dict[str, Any], results: Path, report: Path) -> str:
    study, meta = data["study"], {str(t["name"]): t for t in data["tasks"]}
    css = """#kungfu-payload-cem{scroll-margin-top:20px}#kungfu-payload-cem .kfc-task{border-top:2px solid #d6e2e7;margin-top:32px;padding-top:12px}#kungfu-payload-cem .kfc-grid{display:grid;grid-template-columns:1fr 1fr;gap:18px}#kungfu-payload-cem .kfc-scroll{overflow-x:auto}#kungfu-payload-cem table{width:100%;border-collapse:collapse;white-space:nowrap;font-size:14px}#kungfu-payload-cem th,#kungfu-payload-cem td{padding:9px;text-align:right;border-bottom:1px solid #dce5e8}#kungfu-payload-cem th:first-child,#kungfu-payload-cem td:first-child{text-align:left}#kungfu-payload-cem .kfc-meta,#kungfu-payload-cem .kfc-muted{font-size:14px;color:#546975}#kungfu-payload-cem code,#kungfu-payload-cem pre{white-space:pre-wrap;overflow-wrap:anywhere}#kungfu-payload-cem svg{width:100%;height:auto}#kungfu-payload-cem video,#kungfu-payload-cem img{width:100%;border-radius:8px}#kungfu-payload-cem .kfc-notice{border-left:4px solid #b97a3b;padding-left:14px}#kungfu-payload-cem details{margin:14px 0}@media(max-width:800px){#kungfu-payload-cem .kfc-grid{grid-template-columns:1fr}}"""
    out = [BEGIN, f'<section id="{SECTION_ID}"><style>{css}</style>',
           '<h2>功夫稳定姿态：负载退化与 CEM 恢复（追加实验）</h2>',
           '<div class="kfc-study-summary">'+notes_html(study["summary"])+'</div>' if study.get("summary") else '',
           '<p>本轮继续从原始功夫数据寻找单腿、蹲姿等固定目标。先检查无负载原始 Goal 是否稳定，再比较加载与只调整 z 的结果。这里的数据与上方原三任务、先前8项筛选分别统计。</p>',
           '<p class="kfc-notice">上方8项是早先的小规模抽查；当时6项未通过，不代表整个功夫数据中没有稳定单腿或深蹲。旧节中的“尚未进行负载或 CEM”仅说明上一轮筛选时的进度，本轮新增结果以本节为准。</p>',
           '<p class="kfc-meta">统计口径：每组成功率的分母仅为该组真实验证种子数，不并入上方三任务或旧8项。保持、支撑及深度比例按去掉前2秒后的完整预定时段计算，失败后的剩余时间计0；关节、高度、膝角等误差或状态均值仅在该时段的存活帧计算。均值达标不能替代逐帧保持及完整存活判据。</p>',
           '<details open><summary>本轮筛选结果与未找到的类别</summary>', notes_html(study.get("discovery_notes")), '</details>']
    for index, item in enumerate(study["tasks"]):
        name = str(item["name"])
        task, provenance = meta[name], data["provenance"][name]
        title = str(item.get("title", task.get("title", name)))
        relevant = [r for r in data["evaluations"] if str(r["task"]) == name]
        eligible = item.get("baseline_eligible") is True
        main = normalized_payload(item["main_payload"]) if eligible else None
        find = lambda condition, key: next((r for r in relevant if r["condition"] == condition and normalized_payload(r["payload"]) == key), None)
        original_unloaded, optimized_unloaded = find("original", (0., (0., 0., 0.))), find("cem", (0., (0., 0., 0.)))
        original_loaded = find("original", main) if main else None
        optimized_loaded = find("cem", main) if main else None
        out.extend([f'<article class="kfc-task" id="kfc-task-{index}"><h3>{escape(title)}</h3>',
                    f'<p><b>{"无负载原始 Goal 已通过筛选，纳入负载对照" if eligible else "未纳入负载恢复结论：无负载原始 Goal 未通过或证据未齐"}</b></p>'])
        source_file = task.get("source_file", task.get("file", "未记录"))
        source_frame = task.get("source_frame", "未记录")
        source_fps = task.get("source_fps", task.get("fps"))
        source_time = task.get("source_time_s", task.get("time_s"))
        out.append(f'<p class="kfc-meta">源文件：<code>{escape(source_file)}</code><br>源帧 {escape(source_frame)}；{number(source_fps,3)} FPS；{number(source_time,3)} s。类别：{escape(task.get("category","未记录"))}；目标支撑：{escape(task.get("support","未记录"))}。</p>')
        source_geometry = [("源目标 root 高度 m", task.get("source_root_height_m")),
                           ("源目标膝角 rad", task.get("source_knee_angles_rad")),
                           ("源目标脚底高度差 m", task.get("source_sole_gap_m"))]
        if any(value is not None for _, value in source_geometry):
            out.append('<p class="kfc-meta">'+'；'.join(f'{label}：{number(value)}' for label,value in source_geometry if value is not None)+'。这些是源目标的几何量，不代替下方闭环实际值。</p>')
        if task.get("category") == "deep_squat":
            max_root, min_knee = task.get("max_root_height_m"), task.get("min_mean_knee_angle_rad")
            if finite(max_root) and finite(min_knee):
                out.append(f'<p class="kfc-notice">深蹲附加逐帧约束：root 高度 ≤ {number(max_root)} m，且左右膝平均角 ≥ {number(min_knee)} rad。A/B/C/D 与邻近负载均使用该目标的同一门槛；还须满足姿态、位移、接触等共同条件并完整存活，才计为严格成功，不能通过站高或伸膝换取稳定。</p>')
            else:
                out.append('<p class="kfc-notice">深蹲额外阈值未在该任务元数据完整记录，尚不能仅凭“深蹲”标题确认蹲深语义已受约束。</p>')
        if eligible:
            out.append(f'<p class="kfc-meta">预先指定主负载：{escape(payload_label(item["main_payload"]))}。优化只改变固定 z，目标帧和模型权重保持不变。</p>')
        comparison = [("A 无负载 · 原始 z₀", original_unloaded), ("B 主负载 · 原始 z₀", original_loaded),
                      ("C 主负载 · CEM z*", optimized_loaded), ("D 无负载 · CEM z*", optimized_unloaded)]
        if eligible:
            out.append(hold_chart(comparison, title))
            out.append(evaluation_table(comparison, report))
        else:
            out.append(evaluation_table([("无负载 · 原始 z₀", original_unloaded)], report))
        interpretation = item.get("interpretation", task.get("interpretation"))
        if interpretation:
            out.append('<div class="kfc-interpretation">'+notes_html(interpretation)+'</div>')
        if eligible and original_unloaded and original_unloaded["successes"] != original_unloaded["n"]:
            out.append('<p class="kfc-notice">数据核查：study 标记已通过，但这组无负载逐种子结果未全部成功。不能把它当作完全稳定基线，请结合筛选协议解释。</p>')
        if eligible and original_loaded and original_loaded["successes"] == original_loaded["n"]:
            out.append('<p class="kfc-notice">该主负载下原始 z₀ 已全部成功，不能据此声称“从不稳定恢复稳定”；优化价值需看误差、位移与其他验证条件。</p>')
        paired = [r for _, r in comparison if r]
        seeds = [r.get("protocol", {}).get("seeds") for r in paired]
        horizons = [r.get("protocol", {}).get("horizon_s", r.get("horizon_s")) for r in paired]
        if seeds:
            out.append(f'<p class="kfc-meta">验证种子：{escape(seeds[0])}；每次 {number(horizons[0],1)} s。完整入场、扰动和成功判据见各评估 JSON 的 protocol。</p>')
        if any(s != seeds[0] for s in seeds[1:]) or any(h != horizons[0] for h in horizons[1:]):
            out.append('<p class="kfc-notice">协议核查：各组验证种子或时长不同，不能作为严格配对因果对照。</p>')
        extras = [r for r in relevant if normalized_payload(r["payload"])[0] > 0 and normalized_payload(r["payload"]) != main]
        if extras:
            out.extend(['<h4>邻近负载验证（与主 A/B/C/D 分开）</h4>',
                        evaluation_table([(f'{"原始 z₀" if r["condition"] == "original" else "同一个 CEM z*"}', r) for r in sorted(extras, key=lambda r:(normalized_payload(r["payload"]),r["condition"]))], report)])
        else:
            out.append('<p class="kfc-muted">邻近负载验证：未提供，不推断负载泛化能力。</p>')
        metric_keys = [key for key in OPTIONAL_METRICS if key not in TAIL_METRICS and any(average(r["rows"], key) is not None for r in relevant)]
        if metric_keys:
            out.append('<details><summary>实际高度、支撑语义及补充指标</summary><p class="kfc-meta">均值按逐种子结果计算；“未记录”不会用目标值代替。膝角多值按原 JSON 顺序显示。</p><div class="kfc-scroll"><table><thead><tr><th>负载 / z</th>')
            out.extend(f'<th>{escape(OPTIONAL_METRICS[key][0])}</th>' for key in metric_keys)
            out.append('</tr></thead><tbody>')
            for r in relevant:
                out.append(f'<tr><td>{escape(payload_label(r["payload"]))} · {"z₀" if r["condition"]=="original" else "z*"}</td>')
                out.extend(f'<td>{number(average(r["rows"],key),OPTIONAL_METRICS[key][1])}</td>' for key in metric_keys)
                out.append('</tr>')
            out.append('</tbody></table></div></details>')
        tail_keys = [key for key in TAIL_METRICS if any(key in row for r in relevant for row in r["rows"])]
        if tail_keys:
            out.append('<details><summary>尾段与终帧诊断（逐种子）</summary><p class="kfc-meta">独立列出最后1秒和终帧，避免整体保持率掩盖临近结束的失稳。终帧保持不等同于整次成功；带载通过也不代表卸载或邻近负载安全。</p><div class="kfc-scroll"><table><thead><tr><th>负载 / z</th><th>seed</th>')
            out.extend(f'<th>{escape("终帧保持" if key == "final_hold" else OPTIONAL_METRICS[key][0])}</th>' for key in tail_keys)
            out.append('</tr></thead><tbody>')
            for r in relevant:
                for row in r["rows"]:
                    out.append(f'<tr><td>{escape(payload_label(r["payload"]))} · {"z₀" if r["condition"]=="original" else "z*"}</td><td>{escape(row.get("seed","未记录"))}</td>')
                    for key in tail_keys:
                        value = row.get(key)
                        display = ("是" if value else "否") if key == "final_hold" and isinstance(value,bool) else number(value,3)
                        out.append(f'<td>{display}</td>')
                    out.append('</tr>')
            out.append('</tbody></table></div></details>')
        out.extend(['<details open><summary>CEM 搜索过程</summary>', search_chart(data["search"].get(name), title), '</details>'])
        failed = [(r, row) for r in relevant for row in r["rows"] if row["success"] is False]
        out.append('<details><summary>全部未通过样本（包含原始与优化组）</summary>')
        if failed:
            out.append('<div class="kfc-scroll"><table><thead><tr><th>条件</th><th>seed</th><th>保持</th><th>最大位移 m</th><th>存活 s</th><th>证据</th></tr></thead><tbody>')
            for r, row in failed:
                hold = row.get("hold_fraction")
                out.append(f'<tr><td>{escape(payload_label(r["payload"]))} · {"z₀" if r["condition"]=="original" else "z*"}</td><td>{escape(row.get("seed","未记录"))}</td><td>{number(hold*100,1)+"%" if finite(hold) else "未记录"}</td><td>{number(row.get("max_drift_m"))}</td><td>{number(row.get("survival_s"),1)}</td><td><a href="{escape(r["source"])}">JSON</a></td></tr>')
            out.append('</tbody></table></div>')
        else:
            out.append('<p>现有结果中没有 success=false 的样本；这不代表未测试条件也能成功。</p>')
        out.append('</details>')
        video = results / "videos" / f"{name}_main.mp4"
        if video.is_file():
            out.append(f'<h4>主负载视频</h4><video controls preload="metadata" src="{escape(href(video,report))}"></video>')
            video_note = item.get("video_caption", study.get("video_caption", "视频 seed 与画面顺序未在 study.json 记录，请查视频内标注；不从文件名猜测。"))
            out.append(f'<p class="kfc-meta">{escape(video_note)}</p>')
        else:
            out.append('<p class="kfc-muted">主负载对照视频：尚未导出。</p>')
        for failure_video in sorted((results / "videos").glob(f"{name}_failure*.mp4")):
            out.append(f'<details><summary>失败样本视频：{escape(failure_video.stem)}</summary><video controls preload="metadata" src="{escape(href(failure_video,report))}"></video></details>')
        target_image = next((path for ext in ("jpg","png","webp") if (path := results/"videos"/f"{name}_target.{ext}").is_file()),None)
        if target_image:
            out.append(f'<details><summary>原始目标姿态图</summary><img src="{escape(href(target_image,report))}" alt="{escape(title)}原始目标姿态"></details>')
        original_hash = provenance["actual_original_z_sha256"] or provenance["declared_original_z_sha256"] or "未记录"
        hash_note = "已与 CSV 文件逐字节核验" if provenance["actual_original_z_sha256"] else "仅元数据声明，CSV 未归档，未核验"
        out.append(f'<details><summary>原始 z₀、优化 z* 与来源证据</summary><p>原始 z₀ SHA256（{hash_note}）：<br><code>{escape(original_hash)}</code></p>')
        if provenance["original_path"]:
            out.append(f'<p><a href="{escape(provenance["original_path"])}">原始 z₀ CSV</a>')
        else:
            out.append('<p>原始 z₀ CSV：未归档')
        optimized = next((p for p in (results/"optimized"/f"{name}_z.csv",results/"optimized"/f"{name}.csv") if p.is_file()),results/"optimized"/f"{name}_z.csv")
        out.append(f' · {link(optimized,report,"优化 z* CSV")} · {link(results/"tasks.json",report,"来源帧与目标元数据")}</p></details></article>')
    out.extend(['<details><summary>本轮数据与复现</summary><p>',
                ' · '.join(link(results/file,report,label) for file,label in (("study.json","主负载及筛选说明"),("tasks.json","任务与源帧"),("reproduce.md","运行命令与代码版本"),("verification.json","数据验证记录"))),
                '</p><p class="kfc-meta">本块独立内嵌的数据仅供审计，不参与上方三任务汇总。原始功夫序列未在报告生成时修改；该追加脚本只修改主页面自己的标记块和导航入口。</p></details>'])
    embedded = json.dumps(data,ensure_ascii=False,allow_nan=False,separators=(",",":")).replace("<","\\u003c").replace(">","\\u003e").replace("&","\\u0026")
    out.extend([f'<script type="application/json" id="kfc-data">{embedded}</script>', '</section>', END])
    return "".join(out)


class Links(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.targets: list[str] = []
        self.ids: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str,str|None]]) -> None:
        values = dict(attrs)
        if values.get("id"):
            self.ids.append(values["id"])
        for key in ("href","src"):
            if values.get(key):
                self.targets.append(values[key])


def validate_new_block(section: str, report: Path) -> dict[str, Any]:
    parser = Links()
    parser.feed(section)
    duplicates = sorted({value for value in parser.ids if parser.ids.count(value)>1})
    if duplicates:
        raise ValueError(f"新增块 id 重复：{duplicates}")
    for target in parser.targets:
        parsed = urlsplit(target)
        if parsed.scheme or parsed.netloc or target.startswith("//"):
            raise ValueError(f"新增块存在外部依赖/链接：{target}")
        if not parsed.path:
            continue
        file = (report/unquote(parsed.path)).resolve()
        if not file.is_relative_to(report.resolve()) or not file.is_file():
            raise ValueError(f"新增本地链接无效：{target}")
    return {"local_links_checked":len(parser.targets),"unique_ids":len(parser.ids)}


def append(report: Path, results: Path, *, check: bool = False) -> dict[str, Any]:
    report, results = report.resolve(), results.resolve()
    index = report/"index.html"
    before_bytes = index.read_bytes()
    before = before_bytes.decode("utf-8")
    base = strip_own_blocks(before)
    if f'id="{SECTION_ID}"' in base:
        raise ValueError("发现未带本脚本标记的同名 section，为避免覆盖现有报告已停止")
    data_file = report/"data.json"
    data_sha_before = digest(data_file) if data_file.is_file() else None
    dataset = read_dataset(results,report)
    section = render_section(dataset,results,report)
    checks = validate_new_block(section,report)
    existing_ids, new_ids = Links(), Links()
    existing_ids.feed(base)
    new_ids.feed(section)
    collisions = set(existing_ids.ids).intersection(new_ids.ids)
    if collisions:
        raise ValueError(f"新增块与原页面的 id 冲突：{sorted(collisions)}")
    # 固定锚点；不对已有 section 做正则替换，不触碰原来的 DATA 脚本。
    anchor = '<h2>方法与边界</h2>'
    if base.count(anchor) != 1:
        raise ValueError("主报告中的“方法与边界”锚点缺失或重复，未修改报告")
    output = base.replace(anchor,section+anchor,1)
    nav_link = f'{NAV_BEGIN}<a href="#{SECTION_ID}"><b>功夫负载 CEM（追加）↓</b></a>{NAV_END}'
    nav = re.search(r'<nav\b[^>]*\bid="report-navigation"[^>]*>[\s\S]*?</nav>',output)
    if not nav:
        raise ValueError("主报告缺少唯一 report-navigation，未修改报告")
    if len(re.findall(r'\bid="report-navigation"',output)) != 1:
        raise ValueError("report-navigation 重复，未修改报告")
    closing = nav.end()-len('</nav>')
    output = output[:closing]+nav_link+output[closing:]
    if strip_own_blocks(output) != base:
        raise AssertionError("原页面保护检查失败：新增标记之外有内容变化")
    data_sha_after = digest(data_file) if data_file.is_file() else None
    if data_sha_after != data_sha_before:
        raise AssertionError("既有 data.json 在生成期间变化，已停止")
    changed = output.encode("utf-8") != before_bytes
    if changed and not check:
        if index.read_bytes() != before_bytes:
            raise RuntimeError("主页面在生成期间被其他进程修改，已停止以保护新内容")
        # 同目录原子替换，避免写到一半留下损坏页面。
        temporary = index.with_name(index.name+".kungfu-cem.tmp")
        temporary.write_bytes(output.encode("utf-8"))
        temporary.replace(index)
    return {"report":str(index),"results":str(results),"check_only":check,"changed":changed,
            "study_tasks":len(dataset["study"]["tasks"]),"eval_files":len(dataset["evaluations"]),
            "original_page_without_own_blocks_sha256":hashlib.sha256(base.encode("utf-8")).hexdigest(),
            "original_data_json_sha256":data_sha_before,**checks}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report",type=Path,default=DEFAULT_REPORT,help="已有主报告目录")
    parser.add_argument("--results",type=Path,help="独立新结果目录；默认主报告/kungfu-payload-cem")
    parser.add_argument("--check",action="store_true",help="加载、渲染并校验，不写主页面")
    args = parser.parse_args()
    result = append(args.report,args.results or args.report/"kungfu-payload-cem",check=args.check)
    print(json.dumps(result,ensure_ascii=False,indent=2))


if __name__ == "__main__":
    main()
