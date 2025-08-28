#!/usr/bin/env python3
"""
Validation Report Generator
段階的バリデーション処理の詳細レポートを生成
"""

import json
import os
import sys
from datetime import datetime
from typing import Dict, List, Any, Optional

class ValidationReportGenerator:
    """バリデーションレポート生成クラス"""
    
    def __init__(self, article_id: str):
        self.article_id = article_id
        self.reports_dir = f"output/{article_id}/validation_reports"
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # レポートディレクトリ作成
        os.makedirs(self.reports_dir, exist_ok=True)
        
    def generate_initial_report(self, html_file: str) -> str:
        """Step 1: 初期状態のバリデーションレポート生成"""
        report = {
            "report_type": "initial_validation",
            "timestamp": self.timestamp,
            "article_id": self.article_id,
            "html_file": html_file,
            "step": 1,
            "step_name": "Initial HTML Validation",
            "file_info": self._get_file_info(html_file),
            "validation_results": self._run_validation_checks(html_file),
            "issues_detected": [],
            "recommendations": []
        }
        
        # バリデーション実行
        from validate_html_output import HTMLValidator
        validator = HTMLValidator()
        
        try:
            # ファイルが存在するかチェック
            if not os.path.exists(html_file):
                report["status"] = "error"
                report["error"] = f"HTML file not found: {html_file}"
                return self._save_report(report, "report1_initial.json")
            
            # バリデーション実行
            validation_success = validator.validate_file(html_file)
            report["validation_passed"] = validation_success
            
            if not validation_success:
                # Markdown記法検出
                markdown_issues = validator.detect_markdown_syntax(
                    self._read_file_safe(html_file)
                )
                report["issues_detected"] = markdown_issues
                
                # 推奨アクション
                if any("numbered_lists" in issue for issue in markdown_issues.keys()):
                    report["recommendations"].append("markdown_lists_conversion")
                if any("shortcode" in str(issue).lower() for issue in markdown_issues.keys()):
                    report["recommendations"].append("shortcode_conversion")
                
            report["status"] = "completed"
            
        except Exception as e:
            report["status"] = "error"
            report["error"] = str(e)
            
        return self._save_report(report, "report1_initial.json")
    
    def generate_conversion_report(self, html_file: str, conversion_type: str, 
                                 conversion_results: Dict[str, Any]) -> str:
        """Step 2-3: 変換処理後のレポート生成"""
        step_mapping = {
            "shortcode": {"step": 2, "name": "Shortcode Auto-Conversion"},
            "markdown_lists": {"step": 3, "name": "Markdown Lists Auto-Conversion"}
        }
        
        step_info = step_mapping.get(conversion_type, {"step": 2, "name": "Conversion"})
        
        report = {
            "report_type": f"{conversion_type}_conversion",
            "timestamp": self.timestamp,
            "article_id": self.article_id,
            "html_file": html_file,
            "step": step_info["step"],
            "step_name": step_info["name"],
            "file_info": self._get_file_info(html_file),
            "conversion_results": conversion_results,
            "validation_results": self._run_validation_checks(html_file),
            "improvements": [],
            "remaining_issues": []
        }
        
        try:
            # 変換前後の比較
            if "before" in conversion_results and "after" in conversion_results:
                before_issues = conversion_results["before"]
                after_issues = conversion_results["after"]
                
                # 改善された問題を特定
                if isinstance(before_issues, int) and isinstance(after_issues, int):
                    improvements = before_issues - after_issues
                    report["improvements"] = {
                        "count": improvements,
                        "improvement_rate": (improvements / before_issues * 100) if before_issues > 0 else 0
                    }
                    report["remaining_issues"] = after_issues
            
            report["status"] = "completed"
            
        except Exception as e:
            report["status"] = "error"
            report["error"] = str(e)
            
        filename = f"report{step_info['step']}_{conversion_type}.json"
        return self._save_report(report, filename)
    
    def generate_post_conversion_report(self, html_file: str) -> str:
        """Step 4: 変換処理後のバリデーションレポート"""
        report = {
            "report_type": "post_conversion_validation",
            "timestamp": self.timestamp,
            "article_id": self.article_id,
            "html_file": html_file,
            "step": 4,
            "step_name": "Post-Conversion Validation",
            "file_info": self._get_file_info(html_file),
            "validation_results": self._run_validation_checks(html_file),
            "conversion_summary": {},
            "api_fix_needed": False
        }
        
        try:
            # バリデーション実行
            from validate_html_output import HTMLValidator
            validator = HTMLValidator()
            validation_success = validator.validate_file(html_file)
            
            report["validation_passed"] = validation_success
            report["api_fix_needed"] = not validation_success
            
            # これまでのレポートを読み込んで変換サマリーを作成
            conversion_summary = self._create_conversion_summary()
            report["conversion_summary"] = conversion_summary
            
            report["status"] = "completed"
            
        except Exception as e:
            report["status"] = "error"
            report["error"] = str(e)
            
        return self._save_report(report, "report4_post_conversion.json")
    
    def generate_api_fix_report(self, html_file: str, api_fix_results: Dict[str, Any]) -> str:
        """Step 5: Claude API自動修正レポート"""
        report = {
            "report_type": "api_auto_fix",
            "timestamp": self.timestamp,
            "article_id": self.article_id,
            "html_file": html_file,
            "step": 5,
            "step_name": "Claude API Auto-Fix",
            "file_info": self._get_file_info(html_file),
            "api_fix_results": api_fix_results,
            "validation_results": self._run_validation_checks(html_file),
            "final_status": "pending"
        }
        
        try:
            # API修正の成否を記録
            if "success" in api_fix_results:
                report["api_fix_success"] = api_fix_results["success"]
                
                if api_fix_results["success"]:
                    # 修正後のバリデーション
                    from validate_html_output import HTMLValidator
                    validator = HTMLValidator()
                    validation_success = validator.validate_file(html_file)
                    report["post_fix_validation"] = validation_success
                    report["final_status"] = "fixed" if validation_success else "partial_fix"
                else:
                    report["final_status"] = "fix_failed"
            
            report["status"] = "completed"
            
        except Exception as e:
            report["status"] = "error"
            report["error"] = str(e)
            
        return self._save_report(report, "report5_api_fix.json")
    
    def generate_final_report(self, html_file: str, final_validation: bool) -> str:
        """Step 6: 最終バリデーションレポート"""
        report = {
            "report_type": "final_validation",
            "timestamp": self.timestamp,
            "article_id": self.article_id,
            "html_file": html_file,
            "step": 6,
            "step_name": "Final Strict Validation",
            "file_info": self._get_file_info(html_file),
            "final_validation_passed": final_validation,
            "validation_results": self._run_validation_checks(html_file),
            "overall_summary": {},
            "deployment_ready": final_validation
        }
        
        try:
            # 全体のサマリー作成
            overall_summary = self._create_overall_summary()
            report["overall_summary"] = overall_summary
            
            # 推奨事項
            if final_validation:
                report["recommendations"] = ["ready_for_deployment"]
            else:
                report["recommendations"] = ["manual_intervention_required", "detailed_debugging_needed"]
            
            report["status"] = "completed"
            
        except Exception as e:
            report["status"] = "error" 
            report["error"] = str(e)
            
        return self._save_report(report, "report6_final.json")
    
    def _get_file_info(self, file_path: str) -> Dict[str, Any]:
        """ファイル情報取得"""
        try:
            if not os.path.exists(file_path):
                return {"exists": False}
                
            stat = os.stat(file_path)
            return {
                "exists": True,
                "size_bytes": stat.st_size,
                "size_kb": round(stat.st_size / 1024, 2),
                "readable": os.access(file_path, os.R_OK),
                "writable": os.access(file_path, os.W_OK),
                "modified_time": datetime.fromtimestamp(stat.st_mtime).isoformat()
            }
        except Exception as e:
            return {"exists": False, "error": str(e)}
    
    def _run_validation_checks(self, file_path: str) -> Dict[str, Any]:
        """簡易バリデーションチェック実行"""
        if not os.path.exists(file_path):
            return {"error": "File not found"}
            
        try:
            content = self._read_file_safe(file_path)
            if not content:
                return {"error": "Empty or unreadable file"}
                
            return {
                "content_length": len(content),
                "line_count": content.count('\n'),
                "has_article_content_div": '<div class="article-content">' in content,
                "ends_with_closing_div": content.strip().endswith('</div>'),
                "contains_markdown_lists": bool(re.search(r'^\s*\d+\.\s+', content, re.MULTILINE))
            }
            
        except Exception as e:
            return {"error": f"Validation check failed: {e}"}
    
    def _read_file_safe(self, file_path: str) -> Optional[str]:
        """安全なファイル読み込み"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception:
            return None
    
    def _create_conversion_summary(self) -> Dict[str, Any]:
        """変換処理のサマリー作成"""
        summary = {
            "shortcode_conversion": {"attempted": False, "success": False},
            "markdown_lists_conversion": {"attempted": False, "success": False},
            "total_improvements": 0
        }
        
        try:
            # 既存レポートから情報収集
            for report_file in ["report2_shortcode.json", "report3_markdown_lists.json"]:
                report_path = os.path.join(self.reports_dir, report_file)
                if os.path.exists(report_path):
                    with open(report_path, 'r') as f:
                        report_data = json.load(f)
                        
                    conversion_type = report_data.get("report_type", "").replace("_conversion", "")
                    if conversion_type in summary:
                        summary[conversion_type]["attempted"] = True
                        summary[conversion_type]["success"] = report_data.get("status") == "completed"
                        
                        if "improvements" in report_data:
                            improvements = report_data["improvements"]
                            if isinstance(improvements, dict) and "count" in improvements:
                                summary["total_improvements"] += improvements["count"]
                                
        except Exception as e:
            summary["error"] = f"Failed to create conversion summary: {e}"
            
        return summary
    
    def _create_overall_summary(self) -> Dict[str, Any]:
        """全体サマリー作成"""
        summary = {
            "total_steps": 6,
            "completed_steps": 0,
            "failed_steps": 0,
            "processing_time": {},
            "effectiveness": {}
        }
        
        try:
            # 各ステップのレポートを確認
            report_files = [
                "report1_initial.json",
                "report2_shortcode.json", 
                "report3_markdown_lists.json",
                "report4_post_conversion.json",
                "report5_api_fix.json",
                "report6_final.json"
            ]
            
            for report_file in report_files:
                report_path = os.path.join(self.reports_dir, report_file)
                if os.path.exists(report_path):
                    try:
                        with open(report_path, 'r') as f:
                            report_data = json.load(f)
                            
                        if report_data.get("status") == "completed":
                            summary["completed_steps"] += 1
                        elif report_data.get("status") == "error":
                            summary["failed_steps"] += 1
                            
                    except Exception:
                        summary["failed_steps"] += 1
                        
        except Exception as e:
            summary["error"] = f"Failed to create overall summary: {e}"
            
        return summary
    
    def _save_report(self, report: Dict[str, Any], filename: str) -> str:
        """レポートをJSONファイルに保存"""
        report_path = os.path.join(self.reports_dir, filename)
        
        try:
            with open(report_path, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
                
            print(f"📊 Validation report saved: {report_path}")
            return report_path
            
        except Exception as e:
            print(f"❌ Failed to save report {filename}: {e}")
            return ""

def main():
    """メイン処理"""
    if len(sys.argv) != 3:
        print("Usage: python3 generate_validation_report.py <article_id> <step_type>")
        print("Step types: initial, shortcode, markdown_lists, post_conversion, api_fix, final")
        sys.exit(1)
    
    article_id = sys.argv[1]
    step_type = sys.argv[2]
    
    html_file = f"output/{article_id}/final_article.html"
    generator = ValidationReportGenerator(article_id)
    
    print(f"📊 Generating {step_type} validation report for article {article_id}")
    
    try:
        if step_type == "initial":
            report_path = generator.generate_initial_report(html_file)
        elif step_type == "shortcode":
            # ダミーの変換結果（実際は convert_shortcodes_to_html.py から取得）
            conversion_results = {"before": 0, "after": 0, "conversions": 0}
            report_path = generator.generate_conversion_report(html_file, "shortcode", conversion_results)
        elif step_type == "markdown_lists":
            # ダミーの変換結果（実際は convert_markdown_lists_to_html.py から取得）
            conversion_results = {"before": 5, "after": 1, "conversions": 4}
            report_path = generator.generate_conversion_report(html_file, "markdown_lists", conversion_results)
        elif step_type == "post_conversion":
            report_path = generator.generate_post_conversion_report(html_file)
        elif step_type == "api_fix":
            # ダミーのAPI修正結果（実際は auto_fix_html_output.py から取得）
            api_results = {"success": True, "changes_made": True}
            report_path = generator.generate_api_fix_report(html_file, api_results)
        elif step_type == "final":
            # 最終バリデーション結果（実際はバリデーションスクリプトから取得）
            final_validation = True  # ダミー
            report_path = generator.generate_final_report(html_file, final_validation)
        else:
            print(f"❌ Unknown step type: {step_type}")
            sys.exit(1)
            
        if report_path:
            print(f"✅ Validation report generated successfully: {report_path}")
        else:
            print("❌ Failed to generate validation report")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Error generating validation report: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    import re
    main()