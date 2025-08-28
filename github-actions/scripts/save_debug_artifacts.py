#!/usr/bin/env python3
"""
Debug Artifacts Saver
デバッグ用アーティファクト保存スクリプト
"""

import os
import sys
import shutil
import json
from datetime import datetime
from typing import Dict, List, Optional

class DebugArtifactsSaver:
    """デバッグアーティファクト保存クラス"""
    
    def __init__(self, article_id: str):
        self.article_id = article_id
        self.article_dir = f"output/{article_id}"
        self.debug_dir = f"output/{article_id}/debug_artifacts"
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # デバッグディレクトリ作成
        os.makedirs(self.debug_dir, exist_ok=True)
        
        print(f"🔍 Debug artifacts will be saved to: {self.debug_dir}")
    
    def save_html_snapshot(self, step_name: str, description: str = "") -> bool:
        """HTML状態のスナップショット保存"""
        html_file = f"{self.article_dir}/final_article.html"
        
        if not os.path.exists(html_file):
            print(f"⚠️  HTML file not found for snapshot: {html_file}")
            return False
        
        try:
            # スナップショットファイル名生成
            safe_step_name = step_name.lower().replace(" ", "_").replace("-", "_")
            snapshot_file = f"{self.debug_dir}/html_snapshot_{safe_step_name}_{self.timestamp}.html"
            
            # HTMLファイルをコピー
            shutil.copy2(html_file, snapshot_file)
            
            # メタデータファイル作成
            metadata = {
                "step_name": step_name,
                "description": description,
                "timestamp": self.timestamp,
                "original_file": html_file,
                "snapshot_file": snapshot_file,
                "file_size": os.path.getsize(snapshot_file),
                "created_at": datetime.now().isoformat()
            }
            
            metadata_file = f"{snapshot_file}.meta.json"
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
            
            print(f"📸 HTML snapshot saved: {os.path.basename(snapshot_file)}")
            print(f"📝 Metadata saved: {os.path.basename(metadata_file)}")
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to save HTML snapshot for {step_name}: {e}")
            return False
    
    def save_processing_log(self, step_name: str, log_content: str, 
                          exit_code: int = 0, error_details: Optional[str] = None) -> bool:
        """処理ログの保存"""
        try:
            safe_step_name = step_name.lower().replace(" ", "_").replace("-", "_")
            log_file = f"{self.debug_dir}/processing_log_{safe_step_name}_{self.timestamp}.log"
            
            # ログヘッダー作成
            header = f"""
================================================================================
DEBUG LOG: {step_name}
================================================================================
Article ID: {self.article_id}
Timestamp: {datetime.now().isoformat()}
Exit Code: {exit_code}
Status: {'SUCCESS' if exit_code == 0 else 'FAILED'}
================================================================================

"""
            
            # ログ内容の整理
            full_log = header + log_content
            
            if error_details:
                full_log += f"\n\n=== ERROR DETAILS ===\n{error_details}\n"
            
            # フッター追加
            footer = f"\n\n================================================================================\nLog saved at: {datetime.now().isoformat()}\n================================================================================\n"
            full_log += footer
            
            # ログファイル保存
            with open(log_file, 'w', encoding='utf-8') as f:
                f.write(full_log)
            
            print(f"📋 Processing log saved: {os.path.basename(log_file)}")
            
            # エラー時は専用ディレクトリにもコピー
            if exit_code != 0:
                error_dir = f"{self.debug_dir}/errors"
                os.makedirs(error_dir, exist_ok=True)
                
                error_log = f"{error_dir}/error_{safe_step_name}_{self.timestamp}.log"
                shutil.copy2(log_file, error_log)
                print(f"🚨 Error log also saved: {os.path.basename(error_log)}")
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to save processing log for {step_name}: {e}")
            return False
    
    def save_script_output(self, script_name: str, stdout: str, 
                          stderr: str = "", exit_code: int = 0) -> bool:
        """スクリプト実行結果の保存"""
        try:
            safe_script_name = os.path.basename(script_name).replace(".py", "")
            output_file = f"{self.debug_dir}/script_output_{safe_script_name}_{self.timestamp}.json"
            
            output_data = {
                "script_name": script_name,
                "article_id": self.article_id,
                "timestamp": self.timestamp,
                "execution_time": datetime.now().isoformat(),
                "exit_code": exit_code,
                "success": exit_code == 0,
                "stdout": stdout,
                "stderr": stderr,
                "stdout_lines": len(stdout.splitlines()) if stdout else 0,
                "stderr_lines": len(stderr.splitlines()) if stderr else 0
            }
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, indent=2, ensure_ascii=False)
            
            print(f"⚙️  Script output saved: {os.path.basename(output_file)}")
            
            # エラー出力がある場合は別途テキストファイルにも保存
            if stderr:
                stderr_file = f"{self.debug_dir}/script_stderr_{safe_script_name}_{self.timestamp}.txt"
                with open(stderr_file, 'w', encoding='utf-8') as f:
                    f.write(f"STDERR from {script_name}\n")
                    f.write(f"Exit code: {exit_code}\n")
                    f.write(f"Timestamp: {datetime.now().isoformat()}\n")
                    f.write("=" * 80 + "\n")
                    f.write(stderr)
                
                print(f"⚠️  STDERR saved: {os.path.basename(stderr_file)}")
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to save script output for {script_name}: {e}")
            return False
    
    def save_validation_details(self, validation_results: Dict, 
                              validation_type: str = "standard") -> bool:
        """バリデーション詳細結果の保存"""
        try:
            details_file = f"{self.debug_dir}/validation_details_{validation_type}_{self.timestamp}.json"
            
            detailed_results = {
                "validation_type": validation_type,
                "article_id": self.article_id,
                "timestamp": self.timestamp,
                "validation_time": datetime.now().isoformat(),
                "results": validation_results,
                "file_info": self._get_current_file_info(),
                "system_info": self._get_system_info()
            }
            
            with open(details_file, 'w', encoding='utf-8') as f:
                json.dump(detailed_results, f, indent=2, ensure_ascii=False)
            
            print(f"🔍 Validation details saved: {os.path.basename(details_file)}")
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to save validation details: {e}")
            return False
    
    def create_debug_summary(self) -> bool:
        """デバッグサマリーレポート作成"""
        try:
            summary_file = f"{self.debug_dir}/debug_summary_{self.timestamp}.json"
            
            # デバッグディレクトリ内のファイル一覧
            debug_files = []
            for file in os.listdir(self.debug_dir):
                if file != os.path.basename(summary_file):
                    file_path = os.path.join(self.debug_dir, file)
                    file_info = {
                        "filename": file,
                        "size": os.path.getsize(file_path),
                        "created": datetime.fromtimestamp(os.path.getctime(file_path)).isoformat(),
                        "type": self._get_file_type(file)
                    }
                    debug_files.append(file_info)
            
            summary = {
                "article_id": self.article_id,
                "debug_session": self.timestamp,
                "created_at": datetime.now().isoformat(),
                "debug_directory": self.debug_dir,
                "total_files": len(debug_files),
                "debug_files": debug_files,
                "file_types": self._categorize_files(debug_files),
                "total_size_bytes": sum(f["size"] for f in debug_files),
                "instructions": {
                    "html_snapshots": "Check *.html files for HTML content at different processing stages",
                    "processing_logs": "Check *.log files for detailed processing information",
                    "script_outputs": "Check *_output*.json files for individual script execution results",
                    "validation_details": "Check *_details*.json files for validation specifics",
                    "error_logs": "Check errors/ subdirectory for failed operation details"
                }
            }
            
            with open(summary_file, 'w', encoding='utf-8') as f:
                json.dump(summary, f, indent=2, ensure_ascii=False)
            
            print(f"📊 Debug summary created: {os.path.basename(summary_file)}")
            print(f"📁 Total debug files: {len(debug_files)}")
            print(f"💾 Total size: {summary['total_size_bytes']} bytes")
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to create debug summary: {e}")
            return False
    
    def cleanup_old_artifacts(self, keep_days: int = 7) -> bool:
        """古いアーティファクトのクリーンアップ"""
        try:
            if not os.path.exists(self.debug_dir):
                return True
                
            cutoff_time = datetime.now().timestamp() - (keep_days * 24 * 60 * 60)
            cleaned_count = 0
            
            for file in os.listdir(self.debug_dir):
                file_path = os.path.join(self.debug_dir, file)
                
                if os.path.isfile(file_path):
                    file_mtime = os.path.getmtime(file_path)
                    if file_mtime < cutoff_time:
                        try:
                            os.remove(file_path)
                            cleaned_count += 1
                        except Exception as e:
                            print(f"⚠️  Failed to remove old file {file}: {e}")
            
            if cleaned_count > 0:
                print(f"🧹 Cleaned up {cleaned_count} old debug artifacts (older than {keep_days} days)")
            else:
                print(f"✅ No old debug artifacts to clean up")
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to cleanup old artifacts: {e}")
            return False
    
    def _get_current_file_info(self) -> Dict:
        """現在のHTMLファイル情報取得"""
        html_file = f"{self.article_dir}/final_article.html"
        
        if not os.path.exists(html_file):
            return {"error": "HTML file not found"}
        
        try:
            stat = os.stat(html_file)
            return {
                "file_path": html_file,
                "size_bytes": stat.st_size,
                "size_kb": round(stat.st_size / 1024, 2),
                "modified_time": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                "permissions": oct(stat.st_mode)[-3:]
            }
        except Exception as e:
            return {"error": str(e)}
    
    def _get_system_info(self) -> Dict:
        """システム情報取得"""
        return {
            "python_version": sys.version,
            "working_directory": os.getcwd(),
            "environment_vars": {
                "GITHUB_WORKFLOW": os.environ.get("GITHUB_WORKFLOW", "Not set"),
                "GITHUB_ACTION": os.environ.get("GITHUB_ACTION", "Not set"),
                "RUNNER_OS": os.environ.get("RUNNER_OS", "Not set")
            }
        }
    
    def _get_file_type(self, filename: str) -> str:
        """ファイル種別判定"""
        if filename.endswith('.html'):
            return 'html_snapshot'
        elif filename.endswith('.log'):
            return 'processing_log'
        elif filename.endswith('.json') and 'output' in filename:
            return 'script_output'
        elif filename.endswith('.json') and 'details' in filename:
            return 'validation_details'
        elif filename.endswith('.json') and 'summary' in filename:
            return 'debug_summary'
        elif filename.endswith('.txt'):
            return 'text_log'
        else:
            return 'other'
    
    def _categorize_files(self, files: List[Dict]) -> Dict:
        """ファイル種別ごとの統計"""
        categories = {}
        for file in files:
            file_type = file['type']
            if file_type not in categories:
                categories[file_type] = {"count": 0, "total_size": 0}
            categories[file_type]["count"] += 1
            categories[file_type]["total_size"] += file["size"]
        
        return categories

def main():
    """メイン処理"""
    if len(sys.argv) < 3:
        print("Usage: python3 save_debug_artifacts.py <article_id> <action> [args...]")
        print("Actions:")
        print("  snapshot <step_name> [description]   - Save HTML snapshot")
        print("  log <step_name> <log_file>          - Save processing log")
        print("  script <script_name> <stdout_file>  - Save script output")
        print("  validation <results_file> [type]   - Save validation details")
        print("  summary                             - Create debug summary")
        print("  cleanup [days]                      - Cleanup old artifacts (default: 7 days)")
        sys.exit(1)
    
    article_id = sys.argv[1]
    action = sys.argv[2]
    
    saver = DebugArtifactsSaver(article_id)
    
    try:
        if action == "snapshot":
            step_name = sys.argv[3] if len(sys.argv) > 3 else "unknown_step"
            description = sys.argv[4] if len(sys.argv) > 4 else ""
            success = saver.save_html_snapshot(step_name, description)
            
        elif action == "log":
            step_name = sys.argv[3] if len(sys.argv) > 3 else "unknown_step"
            log_file = sys.argv[4] if len(sys.argv) > 4 else ""
            
            if log_file and os.path.exists(log_file):
                with open(log_file, 'r') as f:
                    log_content = f.read()
            else:
                log_content = "Log file not provided or not found"
            
            success = saver.save_processing_log(step_name, log_content)
            
        elif action == "script":
            script_name = sys.argv[3] if len(sys.argv) > 3 else "unknown_script"
            stdout_file = sys.argv[4] if len(sys.argv) > 4 else ""
            
            stdout = ""
            stderr = ""
            if stdout_file and os.path.exists(stdout_file):
                with open(stdout_file, 'r') as f:
                    stdout = f.read()
            
            success = saver.save_script_output(script_name, stdout, stderr)
            
        elif action == "validation":
            results_file = sys.argv[3] if len(sys.argv) > 3 else ""
            validation_type = sys.argv[4] if len(sys.argv) > 4 else "standard"
            
            results = {}
            if results_file and os.path.exists(results_file):
                with open(results_file, 'r') as f:
                    import json
                    results = json.load(f)
            
            success = saver.save_validation_details(results, validation_type)
            
        elif action == "summary":
            success = saver.create_debug_summary()
            
        elif action == "cleanup":
            keep_days = int(sys.argv[3]) if len(sys.argv) > 3 else 7
            success = saver.cleanup_old_artifacts(keep_days)
            
        else:
            print(f"❌ Unknown action: {action}")
            sys.exit(1)
        
        if success:
            print(f"✅ Debug artifacts action '{action}' completed successfully")
            sys.exit(0)
        else:
            print(f"❌ Debug artifacts action '{action}' failed")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Error during debug artifacts {action}: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()