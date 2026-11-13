"""仅使用自动清理的临时虚构数据；不修改、引用或填充真实实验结果。"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from append_report import append, strip_own_blocks, validate_new_block, BEGIN, END


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value,ensure_ascii=False),encoding="utf-8")


def fixture(report: Path) -> Path:
    """虚构的单腿任务和未达标深蹲；数值不能进入真实报告。"""
    report.mkdir()
    (report/"index.html").write_text('<!doctype html><html lang="zh-CN"><main>'
        '<nav id="report-navigation"><a href="#kungfu">旧入口</a></nav>'
        '<h2 id="payload-comparison">旧三任务</h2><p id="old-result">旧实验 14/15</p>'
        '<section id="kungfu"><h2>旧8项筛选</h2><p>旧原始筛选字节保持</p></section>'
        '<h2>方法与边界</h2><p>旧方法</p></main>'
        '<script>const DATA={"results":[{"source":"旧数据"}]};</script></html>',encoding="utf-8")
    (report/"data.json").write_bytes(b'{"original_three_task_data":true}\n')
    results = report/"kungfu-payload-cem"
    z = ("0,"*255+"16\n").encode()
    (results/"original").mkdir(parents=True)
    (results/"optimized").mkdir()
    (results/"original"/"fixture_leg_z.csv").write_bytes(z)
    (results/"original"/"fixture_squat_z.csv").write_bytes(z)
    (results/"optimized"/"fixture_leg_z.csv").write_bytes(z)
    zsha = hashlib.sha256(z).hexdigest()
    write_json(results/"tasks.json",[
        {"name":"fixture_leg","title":"虚构单腿 <fixture>","source_file":"虚构源.pkl",
         "source_frame":101,"source_fps":70,"source_time_s":101/70,"support":"left",
         "category":"single_leg","original_z_sha256":zsha,"source_root_height_m":.54,
         "source_knee_angles_rad":[.4,.7],"source_sole_gap_m":.13},
        {"name":"fixture_squat","title":"虚构深蹲未达标","file":"fixture.pkl","source_frame":70,
         "fps":70,"time_s":1.,"support":"both","category":"deep_squat","original_z_sha256":zsha,
         "max_root_height_m":.50,"min_mean_knee_angle_rad":1.05},
    ])
    main = {"mass_kg":8.,"offset_m":[.3,0,.1]}
    write_json(results/"study.json",{
        "summary":["虚构总结：带载通过不代表卸载安全。","<script>虚构文本应转义</script>"],
        "tasks":[{"name":"fixture_leg","main_payload":main,"baseline_eligible":True,
                  "interpretation":"虚构解读：D 组必须独立检查 <b>不渲染HTML</b>。"},
                 {"name":"fixture_squat","baseline_eligible":False}],
        "discovery_notes":["虚构fixture：没有找到合格深蹲；不得当作实验结论。","</script><script>不执行</script>"],
    })
    def evaluation(task: str, condition: str, payload: dict, failure: bool = False) -> dict:
        return {"task":task,"title":"虚构测试","condition":condition,"physics":{"payload":payload},
                "protocol":{"seeds":[101,202],"horizon_s":30.,"entry":"fixture"},
                "rows":[{"seed":101,"success":not failure,"hold_fraction":.5 if failure else .99,
                         "joint_mae_rad":.1,"max_drift_m":.8 if failure else .05,"survival_s":30.,
                         "actual_root_height_m":.55,"lift_height_m":.12,"support_fraction":.98,"knee_angle_rad":[.5,.8]},
                        {"seed":202,"success":True,"hold_fraction":.99,"joint_mae_rad":.11,
                         "max_drift_m":.06,"survival_s":30.,"actual_root_height_m":.56,"lift_height_m":.13,
                         "support_fraction":.99,"knee_angle_rad":[.6,.9]}]}
    # 真实 rollout 字段与旧字段均验证；同一虚构结果中的值仅用于渲染测试。
    def with_actual_metrics(value: dict) -> dict:
        for i,row in enumerate(value["rows"]):
            row.update(root_height_m=.55+i*.01,mean_knee_angle_rad=.65+i*.1,
                       left_knee_angle_rad=.5+i*.1,right_knee_angle_rad=.8+i*.1,depth_fraction=.96+i*.02,
                       final_hold=(i==1),last_second_hold_fraction=.7+i*.2,
                       last_second_support_fraction=.8+i*.1,last_second_depth_fraction=.9+i*.05)
        return value
    zero = {"mass_kg":0.,"offset_m":[0,0,.1]}
    for task, cond, payload, label, failure in [
        ("fixture_leg","original",zero,"a",False),("fixture_leg","original",main,"b",True),
        ("fixture_leg","cem",main,"c",False),("fixture_leg","cem",zero,"d",False),
        ("fixture_leg","original",{"mass_kg":6.,"offset_m":[.25,0,.1]},"near_o",True),
        ("fixture_leg","cem",{"mass_kg":6.,"offset_m":[.25,0,.1]},"near_c",False),
        ("fixture_squat","original",zero,"squat",True),
    ]:
        write_json(results/"eval"/f"{label}.json",with_actual_metrics(evaluation(task,cond,payload,failure)))
    write_json(results/"search"/"fixture_leg.json",{"config":{"population":128,"elites":16,"iterations":2,"seed":123},
        "history":[{"iteration":1,"best_score":-5.,"anchor_score":-25.,"median_score":-15.},
                   {"iteration":2,"best_score":-2.,"anchor_score":-25.,"median_score":-10.}],"elapsed_s":15.})
    return results


class AppendReportFixtureTests(unittest.TestCase):
    def test_links_idempotence_and_exact_preservation(self) -> None:
        with tempfile.TemporaryDirectory(prefix="kungfu-report-fixture-") as directory:
            report=Path(directory)/"report"
            results=fixture(report)
            before=(report/"index.html").read_bytes()
            data_before=(report/"data.json").read_bytes()
            dry=append(report,results,check=True)
            self.assertTrue(dry["changed"])
            self.assertEqual((report/"index.html").read_bytes(),before)
            first=append(report,results)
            first_page=(report/"index.html").read_bytes()
            second=append(report,results)
            self.assertTrue(first["changed"])
            self.assertFalse(second["changed"])
            self.assertEqual((report/"index.html").read_bytes(),first_page)
            self.assertEqual(strip_own_blocks(first_page.decode()),before.decode())
            self.assertEqual((report/"data.json").read_bytes(),data_before)
            page=first_page.decode()
            section=page[page.index(BEGIN):page.index(END)+len(END)]
            self.assertGreater(validate_new_block(section,report)["local_links_checked"],15)
            self.assertIn("A 无负载 · 原始 z₀",section)
            self.assertIn("D 无负载 · CEM z*",section)
            self.assertIn("邻近负载验证（与主 A/B/C/D 分开）",section)
            self.assertIn("主负载对照视频：尚未导出",section)
            self.assertIn("未纳入负载恢复结论",section)
            self.assertIn("膝关节角 rad",section)
            self.assertIn("平均膝角 rad",section)
            self.assertIn("左膝角 rad",section)
            self.assertIn("右膝角 rad",section)
            self.assertIn("蹲深达标比例",section)
            self.assertIn("源目标 root 高度 m：0.540",section)
            self.assertIn("源目标膝角 rad：0.400 / 0.700",section)
            self.assertIn("源目标脚底高度差 m：0.130",section)
            self.assertIn("0.550 / 0.850",section)
            self.assertIn("全部未通过样本",section)
            self.assertIn("早先的小规模抽查",section)
            self.assertIn("root 高度 ≤ 0.500 m",section)
            self.assertIn("左右膝平均角 ≥ 1.050 rad",section)
            self.assertIn("不并入上方三任务或旧8项",section)
            self.assertIn("失败后的剩余时间计0",section)
            self.assertIn("虚构总结：带载通过不代表卸载安全",section)
            self.assertIn("虚构解读：D 组必须独立检查 &lt;b&gt;不渲染HTML&lt;/b&gt;",section)
            self.assertNotIn("<script>虚构文本应转义</script>",section)
            self.assertIn("尾段与终帧诊断（逐种子）",section)
            self.assertIn("末1秒支撑比例",section)
            self.assertIn("末1秒深度比例",section)
            self.assertIn("<td>否</td>",section)
            self.assertIn("<td>是</td>",section)
            self.assertNotIn("</script><script>不执行",section)

    def test_optional_video_is_local_and_checked(self) -> None:
        with tempfile.TemporaryDirectory(prefix="kungfu-report-fixture-") as directory:
            report=Path(directory)/"report"
            results=fixture(report)
            (results/"videos").mkdir()
            # 仅验证HTML本地链接；这是假文件，不作为视频内容/物理证据。
            (results/"videos"/"fixture_leg_main.mp4").write_bytes(b"not-a-real-video-fixture")
            (results/"videos"/"fixture_leg_failure_seed101.mp4").write_bytes(b"not-a-real-video-fixture")
            checks=append(report,results)
            page=(report/"index.html").read_text()
            self.assertIn('src="kungfu-payload-cem/videos/fixture_leg_main.mp4"',page)
            self.assertIn("失败样本视频",page)
            self.assertGreater(checks["local_links_checked"],15)

    def test_hash_mismatch_prevents_writing(self) -> None:
        with tempfile.TemporaryDirectory(prefix="kungfu-report-fixture-") as directory:
            report=Path(directory)/"report"
            results=fixture(report)
            before=(report/"index.html").read_bytes()
            (results/"original"/"fixture_leg_z.csv").write_bytes(b"corrupted-fixture")
            with self.assertRaisesRegex(ValueError,"SHA256"):
                append(report,results)
            self.assertEqual((report/"index.html").read_bytes(),before)

    def test_protocol_mismatch_is_not_silently_accepted(self) -> None:
        with tempfile.TemporaryDirectory(prefix="kungfu-report-fixture-") as directory:
            report=Path(directory)/"report"
            results=fixture(report)
            file=results/"eval"/"a.json"
            value=json.loads(file.read_text())
            value["protocol"]["seeds"]=[101,999]
            write_json(file,value)
            with self.assertRaisesRegex(ValueError,"seeds"):
                append(report,results)


if __name__ == "__main__":
    unittest.main(verbosity=2)
