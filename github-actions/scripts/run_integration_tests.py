#!/usr/bin/env python3
"""
Integration Tests for HTML Validation Pipeline
HTML validation パイプラインの統合テストスクリプト
"""

import os
import sys
import json
import tempfile
import subprocess
from datetime import datetime
from typing import Dict, List, Tuple, Optional

class IntegrationTester:
    """統合テストクラス"""
    
    def __init__(self):
        self.test_results = []
        self.scripts_dir = "github-actions/scripts"
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # テスト結果保存ディレクトリ
        self.results_dir = f"test_results_{self.timestamp}"
        os.makedirs(self.results_dir, exist_ok=True)
        
        print(f"🧪 Integration tests starting...")
        print(f"📁 Results will be saved to: {self.results_dir}")
    
    def run_all_tests(self) -> bool:
        """全ての統合テストを実行"""
        print("=" * 80)
        print("🚀 RUNNING COMPREHENSIVE INTEGRATION TESTS")
        print("=" * 80)
        
        # テストスイート実行
        test_methods = [
            ("Normal Cases", self.test_normal_cases),
            ("Error Cases", self.test_error_cases),
            ("Performance Tests", self.test_performance),
            ("Script Compatibility", self.test_script_compatibility)
        ]
        
        total_tests = 0
        passed_tests = 0
        
        for suite_name, test_method in test_methods:
            print(f"\n🧪 Running {suite_name}...")
            print("-" * 60)
            
            try:
                suite_results = test_method()
                total_tests += len(suite_results)
                passed_tests += sum(1 for result in suite_results if result["passed"])
                
                self.test_results.extend(suite_results)
                
                # スイート結果サマリー
                suite_passed = sum(1 for result in suite_results if result["passed"])
                print(f"📊 {suite_name}: {suite_passed}/{len(suite_results)} tests passed")
                
            except Exception as e:
                print(f"❌ Error in {suite_name}: {e}")
                self.test_results.append({
                    "test_name": f"{suite_name} (Suite Error)",
                    "passed": False,
                    "error": str(e),
                    "execution_time": 0
                })
                total_tests += 1
        
        # 最終結果
        print("\n" + "=" * 80)
        print(f"📋 INTEGRATION TESTS SUMMARY")
        print("=" * 80)
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {total_tests - passed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests*100):.1f}%" if total_tests > 0 else "N/A")
        
        # 結果保存
        self.save_test_results()
        
        return passed_tests == total_tests
    
    def test_normal_cases(self) -> List[Dict]:
        """正常ケースのテスト"""
        results = []
        
        # Test 1: Markdown リスト変換テスト
        results.append(self.test_markdown_list_conversion())
        
        # Test 2: ショートコード変換テスト
        results.append(self.test_shortcode_conversion())
        
        # Test 3: HTML バリデーションテスト
        results.append(self.test_html_validation())
        
        # Test 4: 統合ワークフローテスト
        results.append(self.test_integrated_workflow())
        
        return results
    
    def test_error_cases(self) -> List[Dict]:
        """エラーケースのテスト"""
        results = []
        
        # Test 1: 存在しないファイルテスト
        results.append(self.test_nonexistent_file_handling())
        
        # Test 2: 不正HTMLテスト
        results.append(self.test_malformed_html_handling())
        
        # Test 3: 環境変数未設定テスト  
        results.append(self.test_missing_env_var_handling())
        
        return results
    
    def test_performance(self) -> List[Dict]:
        """パフォーマンステスト"""
        results = []
        
        # Test 1: 大容量HTMLファイルテスト
        results.append(self.test_large_html_processing())
        
        # Test 2: 処理時間測定テスト
        results.append(self.test_processing_time_limits())
        
        return results
    
    def test_script_compatibility(self) -> List[Dict]:
        """スクリプト互換性テスト"""
        results = []
        
        # Test 1: 全スクリプト実行可能性テスト
        results.append(self.test_all_scripts_executable())
        
        # Test 2: Python依存関係テスト
        results.append(self.test_python_dependencies())
        
        return results
    
    def test_markdown_list_conversion(self) -> Dict:
        """Markdownリスト変換テスト"""
        test_name = "Markdown List Conversion"
        start_time = datetime.now()
        
        try:
            # テスト用HTMLファイル作成
            test_content = '''<div class="article-content">
<h2>テスト記事</h2>
<p>以下の手順で実行してください：</p>

1. 最初の手順です
2. 二番目の手順です
3. 三番目の手順です

<p>また、以下も重要です：</p>

1. 重要な点その1
2. 重要な点その2

<p>単発の例: 1. これは変換されない</p>
</div>'''
            
            with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
                f.write(test_content)
                test_file = f.name
            
            try:
                # 変換スクリプト実行
                cmd = [sys.executable, f"{self.scripts_dir}/convert_markdown_lists_to_html.py", test_file]
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
                
                success = result.returncode == 0
                
                if success:
                    # 変換結果確認
                    with open(test_file, 'r') as f:
                        converted_content = f.read()
                    
                    # <ol><li> タグの存在確認
                    has_ol_tags = '<ol>' in converted_content and '<li>' in converted_content
                    # 元のMarkdown記法の削除確認
                    remaining_markdown = len([line for line in converted_content.split('\n') 
                                            if line.strip().startswith(tuple('123456789'))])
                    
                    success = has_ol_tags and remaining_markdown < 3  # 単発の「1.」は残る
                
                execution_time = (datetime.now() - start_time).total_seconds()
                
                return {
                    "test_name": test_name,
                    "passed": success,
                    "execution_time": execution_time,
                    "details": {
                        "exit_code": result.returncode,
                        "has_ol_tags": has_ol_tags if success else False,
                        "remaining_markdown_lines": remaining_markdown if success else "N/A"
                    },
                    "output": result.stdout,
                    "error": result.stderr if result.stderr else None
                }
                
            finally:
                # テンポラリファイル削除
                if os.path.exists(test_file):
                    os.unlink(test_file)
                    
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            return {
                "test_name": test_name,
                "passed": False,
                "execution_time": execution_time,
                "error": str(e)
            }
    
    def test_shortcode_conversion(self) -> Dict:
        """ショートコード変換テスト"""
        test_name = "Shortcode Conversion"
        start_time = datetime.now()
        
        try:
            # テスト用HTMLファイル作成
            test_content = '''<div class="article-content">
<h2>ショートコードテスト</h2>
<p>関連記事をご覧ください：</p>

[blog_card url="https://example.com/article1"]

<p>動画もどうぞ：</p>

[video url="https://example.com/video.mp4"]

<p>テキストのみの段落</p>
</div>'''
            
            with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
                f.write(test_content)
                test_file = f.name
            
            try:
                # 変換スクリプト実行
                cmd = [sys.executable, f"{self.scripts_dir}/convert_shortcodes_to_html.py", test_file]
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
                
                success = result.returncode == 0
                
                if success:
                    # 変換結果確認
                    with open(test_file, 'r') as f:
                        converted_content = f.read()
                    
                    # HTMLタグの存在確認
                    has_figure_tags = '<figure class="link-card">' in converted_content
                    has_video_tags = '<figure class="video-embed">' in converted_content
                    # ショートコードの削除確認
                    remaining_shortcodes = '[blog_card' in converted_content or '[video' in converted_content
                    
                    success = has_figure_tags and has_video_tags and not remaining_shortcodes
                
                execution_time = (datetime.now() - start_time).total_seconds()
                
                return {
                    "test_name": test_name,
                    "passed": success,
                    "execution_time": execution_time,
                    "details": {
                        "exit_code": result.returncode,
                        "has_figure_tags": has_figure_tags if success else False,
                        "has_video_tags": has_video_tags if success else False,
                        "remaining_shortcodes": remaining_shortcodes if success else "N/A"
                    },
                    "output": result.stdout,
                    "error": result.stderr if result.stderr else None
                }
                
            finally:
                if os.path.exists(test_file):
                    os.unlink(test_file)
                    
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            return {
                "test_name": test_name,
                "passed": False,
                "execution_time": execution_time,
                "error": str(e)
            }
    
    def test_html_validation(self) -> Dict:
        """HTML validation テスト"""
        test_name = "HTML Validation"
        start_time = datetime.now()
        
        try:
            # 正常なHTMLファイル作成
            valid_content = '''<div class="article-content">
<h2>正常なHTML</h2>
<p>この記事は完全にHTMLで書かれています。</p>
<ul>
  <li>リスト項目1</li>
  <li>リスト項目2</li>
</ul>
</div>'''
            
            with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
                f.write(valid_content)
                valid_file = f.name
            
            try:
                # バリデーションスクリプト実行
                cmd = [sys.executable, f"{self.scripts_dir}/validate_html_output.py", valid_file]
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
                
                # 正常なHTMLでは validation が成功すべき
                success = result.returncode == 0
                
                execution_time = (datetime.now() - start_time).total_seconds()
                
                return {
                    "test_name": test_name,
                    "passed": success,
                    "execution_time": execution_time,
                    "details": {
                        "exit_code": result.returncode,
                        "validation_passed": success
                    },
                    "output": result.stdout,
                    "error": result.stderr if result.stderr else None
                }
                
            finally:
                if os.path.exists(valid_file):
                    os.unlink(valid_file)
                    
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            return {
                "test_name": test_name,
                "passed": False,
                "execution_time": execution_time,
                "error": str(e)
            }
    
    def test_integrated_workflow(self) -> Dict:
        """統合ワークフローテスト"""
        test_name = "Integrated Workflow"
        start_time = datetime.now()
        
        try:
            # Markdown記法とショートコードを含むHTMLファイル作成
            mixed_content = '''<div class="article-content">
<h2>統合テスト用記事</h2>
<p>以下の手順で進めてください：</p>

1. 最初のステップ
2. 次のステップ
3. 最終ステップ

<p>関連記事もチェック：</p>

[blog_card url="https://example.com/related"]

<p>完了です。</p>
</div>'''
            
            with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
                f.write(mixed_content)
                test_file = f.name
            
            try:
                # Step 1: ショートコード変換
                cmd1 = [sys.executable, f"{self.scripts_dir}/convert_shortcodes_to_html.py", test_file]
                result1 = subprocess.run(cmd1, capture_output=True, text=True, timeout=30)
                
                # Step 2: Markdownリスト変換
                cmd2 = [sys.executable, f"{self.scripts_dir}/convert_markdown_lists_to_html.py", test_file]
                result2 = subprocess.run(cmd2, capture_output=True, text=True, timeout=30)
                
                # Step 3: バリデーション
                cmd3 = [sys.executable, f"{self.scripts_dir}/validate_html_output.py", test_file]
                result3 = subprocess.run(cmd3, capture_output=True, text=True, timeout=30)
                
                # 各ステップの成功確認
                step1_success = result1.returncode == 0
                step2_success = result2.returncode == 0
                step3_success = result3.returncode == 0  # 完全に変換されていればパス
                
                # 最終コンテンツ確認
                with open(test_file, 'r') as f:
                    final_content = f.read()
                
                has_ol_tags = '<ol>' in final_content
                has_figure_tags = '<figure class="link-card">' in final_content
                no_markdown = not any(line.strip().startswith(('1.', '2.', '3.')) 
                                   for line in final_content.split('\n'))
                no_shortcodes = '[blog_card' not in final_content
                
                workflow_success = (step1_success and step2_success and 
                                  has_ol_tags and has_figure_tags and 
                                  no_markdown and no_shortcodes)
                
                execution_time = (datetime.now() - start_time).total_seconds()
                
                return {
                    "test_name": test_name,
                    "passed": workflow_success,
                    "execution_time": execution_time,
                    "details": {
                        "step1_shortcode_conversion": step1_success,
                        "step2_markdown_conversion": step2_success,
                        "step3_validation": step3_success,
                        "has_ol_tags": has_ol_tags,
                        "has_figure_tags": has_figure_tags,
                        "no_remaining_markdown": no_markdown,
                        "no_remaining_shortcodes": no_shortcodes
                    },
                    "step_outputs": {
                        "step1": result1.stdout,
                        "step2": result2.stdout,
                        "step3": result3.stdout
                    }
                }
                
            finally:
                if os.path.exists(test_file):
                    os.unlink(test_file)
                    
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            return {
                "test_name": test_name,
                "passed": False,
                "execution_time": execution_time,
                "error": str(e)
            }
    
    def test_nonexistent_file_handling(self) -> Dict:
        """存在しないファイルの処理テスト"""
        test_name = "Nonexistent File Handling"
        start_time = datetime.now()
        
        try:
            nonexistent_file = "/tmp/nonexistent_file_12345.html"
            
            # バリデーションスクリプトで存在しないファイルをテスト
            cmd = [sys.executable, f"{self.scripts_dir}/validate_html_output.py", nonexistent_file]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            # 存在しないファイルの場合、エラー終了すべき
            success = result.returncode != 0 and "not found" in result.stderr.lower()
            
            execution_time = (datetime.now() - start_time).total_seconds()
            
            return {
                "test_name": test_name,
                "passed": success,
                "execution_time": execution_time,
                "details": {
                    "exit_code": result.returncode,
                    "error_handling": success
                },
                "output": result.stdout,
                "error": result.stderr
            }
            
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            return {
                "test_name": test_name,
                "passed": False,
                "execution_time": execution_time,
                "error": str(e)
            }
    
    def test_malformed_html_handling(self) -> Dict:
        """不正HTMLの処理テスト"""
        test_name = "Malformed HTML Handling"
        start_time = datetime.now()
        
        try:
            # 不正なHTMLファイル作成
            malformed_content = '''<div class="article-content">
<h2>不正なHTML
<p>閉じタグなし
<div><span>入れ子エラー</div></span>
<ol><p>間違った子要素</p></ol>
</div>'''
            
            with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
                f.write(malformed_content)
                test_file = f.name
            
            try:
                # バリデーションスクリプト実行
                cmd = [sys.executable, f"{self.scripts_dir}/validate_html_output.py", test_file]
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
                
                # 不正なHTMLでは validation が失敗すべき
                success = result.returncode != 0
                
                execution_time = (datetime.now() - start_time).total_seconds()
                
                return {
                    "test_name": test_name,
                    "passed": success,
                    "execution_time": execution_time,
                    "details": {
                        "exit_code": result.returncode,
                        "validation_failed_as_expected": success
                    },
                    "output": result.stdout,
                    "error": result.stderr if result.stderr else None
                }
                
            finally:
                if os.path.exists(test_file):
                    os.unlink(test_file)
                    
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            return {
                "test_name": test_name,
                "passed": False,
                "execution_time": execution_time,
                "error": str(e)
            }
    
    def test_missing_env_var_handling(self) -> Dict:
        """環境変数未設定の処理テスト"""
        test_name = "Missing Environment Variable Handling"
        start_time = datetime.now()
        
        try:
            # テスト用HTMLファイル作成
            test_content = '''<div class="article-content">
<h2>環境変数テスト</h2>
<p>このテストはAPIキーなしで実行されます。</p>
</div>'''
            
            with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
                f.write(test_content)
                test_file = f.name
            
            try:
                # 環境変数をクリアしてauto_fix_html_output.py実行
                env = os.environ.copy()
                env.pop('ANTHROPIC_API_KEY', None)  # APIキーを削除
                
                cmd = [sys.executable, f"{self.scripts_dir}/auto_fix_html_output.py", test_file]
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=30, env=env)
                
                # APIキーがない場合、適切なエラー終了すべき
                success = (result.returncode != 0 and 
                          "ANTHROPIC_API_KEY" in result.stdout and
                          "environment variable not set" in result.stdout)
                
                execution_time = (datetime.now() - start_time).total_seconds()
                
                return {
                    "test_name": test_name,
                    "passed": success,
                    "execution_time": execution_time,
                    "details": {
                        "exit_code": result.returncode,
                        "proper_error_handling": success
                    },
                    "output": result.stdout,
                    "error": result.stderr if result.stderr else None
                }
                
            finally:
                if os.path.exists(test_file):
                    os.unlink(test_file)
                    
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            return {
                "test_name": test_name,
                "passed": False,
                "execution_time": execution_time,
                "error": str(e)
            }
    
    def test_large_html_processing(self) -> Dict:
        """大容量HTML処理テスト"""
        test_name = "Large HTML Processing"
        start_time = datetime.now()
        
        try:
            # 大容量HTMLファイル作成 (約50KB)
            large_content_parts = ['<div class="article-content">']
            large_content_parts.append('<h1>大容量HTMLテスト</h1>')
            
            for i in range(100):
                large_content_parts.append(f'''
<h2>セクション {i+1}</h2>
<p>これは大容量HTMLファイルのテストです。セクション{i+1}の内容です。</p>

1. 項目{i*3+1}
2. 項目{i*3+2}  
3. 項目{i*3+3}

<p>追加の説明文です。' + 'A' * 100 + f'</p>

[blog_card url="https://example.com/article{i+1}"]
''')
            
            large_content_parts.append('</div>')
            large_content = '\n'.join(large_content_parts)
            
            with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
                f.write(large_content)
                test_file = f.name
            
            try:
                file_size = os.path.getsize(test_file)
                print(f"   📊 Test file size: {file_size} bytes ({file_size/1024:.1f} KB)")
                
                # Markdownリスト変換テスト（時間制限あり）
                cmd = [sys.executable, f"{self.scripts_dir}/convert_markdown_lists_to_html.py", test_file]
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)  # 2分制限
                
                success = result.returncode == 0
                
                execution_time = (datetime.now() - start_time).total_seconds()
                
                # パフォーマンス基準: 60秒以内
                performance_ok = execution_time <= 60.0
                
                return {
                    "test_name": test_name,
                    "passed": success and performance_ok,
                    "execution_time": execution_time,
                    "details": {
                        "file_size_bytes": file_size,
                        "exit_code": result.returncode,
                        "performance_within_limits": performance_ok,
                        "time_limit_seconds": 60.0
                    },
                    "output": result.stdout[-500:] if result.stdout else None,  # 最後500文字のみ
                    "error": result.stderr if result.stderr else None
                }
                
            finally:
                if os.path.exists(test_file):
                    os.unlink(test_file)
                    
        except subprocess.TimeoutExpired:
            execution_time = (datetime.now() - start_time).total_seconds()
            return {
                "test_name": test_name,
                "passed": False,
                "execution_time": execution_time,
                "error": "Processing timeout (>120 seconds)"
            }
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            return {
                "test_name": test_name,
                "passed": False,
                "execution_time": execution_time,
                "error": str(e)
            }
    
    def test_processing_time_limits(self) -> Dict:
        """処理時間制限テスト"""
        test_name = "Processing Time Limits"
        start_time = datetime.now()
        
        try:
            # 標準サイズのHTMLファイル作成
            normal_content = '''<div class="article-content">
<h2>標準的な記事</h2>
<p>このテストは標準的な処理時間を測定します。</p>

1. 手順その1
2. 手順その2
3. 手順その3

[blog_card url="https://example.com/sample"]

<p>終了です。</p>
</div>'''
            
            with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
                f.write(normal_content)
                test_file = f.name
            
            try:
                # 各スクリプトの実行時間測定
                scripts_to_test = [
                    "convert_shortcodes_to_html.py",
                    "convert_markdown_lists_to_html.py", 
                    "validate_html_output.py"
                ]
                
                times = {}
                all_passed = True
                
                for script in scripts_to_test:
                    script_start = datetime.now()
                    cmd = [sys.executable, f"{self.scripts_dir}/{script}", test_file]
                    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
                    script_time = (datetime.now() - script_start).total_seconds()
                    
                    times[script] = script_time
                    
                    # 各スクリプト10秒以内の基準
                    if result.returncode != 0 or script_time > 10.0:
                        all_passed = False
                
                execution_time = (datetime.now() - start_time).total_seconds()
                
                return {
                    "test_name": test_name,
                    "passed": all_passed,
                    "execution_time": execution_time,
                    "details": {
                        "script_times": times,
                        "time_limit_per_script": 10.0,
                        "all_within_limits": all_passed
                    }
                }
                
            finally:
                if os.path.exists(test_file):
                    os.unlink(test_file)
                    
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            return {
                "test_name": test_name,
                "passed": False,
                "execution_time": execution_time,
                "error": str(e)
            }
    
    def test_all_scripts_executable(self) -> Dict:
        """全スクリプト実行可能性テスト"""
        test_name = "All Scripts Executable"
        start_time = datetime.now()
        
        try:
            scripts_to_check = [
                "convert_shortcodes_to_html.py",
                "convert_markdown_lists_to_html.py",
                "validate_html_output.py",
                "auto_fix_html_output.py",
                "generate_validation_report.py",
                "save_debug_artifacts.py"
            ]
            
            results = {}
            all_executable = True
            
            for script in scripts_to_check:
                script_path = f"{self.scripts_dir}/{script}"
                
                # ファイル存在確認
                exists = os.path.exists(script_path)
                
                # 実行権限確認
                executable = os.access(script_path, os.X_OK) if exists else False
                
                # Python構文チェック
                syntax_ok = False
                if exists:
                    try:
                        cmd = [sys.executable, "-m", "py_compile", script_path]
                        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
                        syntax_ok = result.returncode == 0
                    except:
                        syntax_ok = False
                
                script_status = exists and syntax_ok
                results[script] = {
                    "exists": exists,
                    "executable": executable,
                    "syntax_ok": syntax_ok,
                    "overall_ok": script_status
                }
                
                if not script_status:
                    all_executable = False
            
            execution_time = (datetime.now() - start_time).total_seconds()
            
            return {
                "test_name": test_name,
                "passed": all_executable,
                "execution_time": execution_time,
                "details": {
                    "scripts_checked": len(scripts_to_check),
                    "scripts_results": results,
                    "all_executable": all_executable
                }
            }
            
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            return {
                "test_name": test_name,
                "passed": False,
                "execution_time": execution_time,
                "error": str(e)
            }
    
    def test_python_dependencies(self) -> Dict:
        """Python依存関係テスト"""
        test_name = "Python Dependencies"
        start_time = datetime.now()
        
        try:
            required_modules = [
                "json", "os", "sys", "re", "requests", 
                "datetime", "tempfile", "shutil", "subprocess"
            ]
            
            optional_modules = [
                "bs4"  # BeautifulSoup
            ]
            
            missing_required = []
            missing_optional = []
            
            # 必須モジュールチェック
            for module in required_modules:
                try:
                    __import__(module)
                except ImportError:
                    missing_required.append(module)
            
            # オプショナルモジュールチェック
            for module in optional_modules:
                try:
                    __import__(module)
                except ImportError:
                    missing_optional.append(module)
            
            success = len(missing_required) == 0
            
            execution_time = (datetime.now() - start_time).total_seconds()
            
            return {
                "test_name": test_name,
                "passed": success,
                "execution_time": execution_time,
                "details": {
                    "required_modules": required_modules,
                    "optional_modules": optional_modules,
                    "missing_required": missing_required,
                    "missing_optional": missing_optional,
                    "python_version": sys.version
                }
            }
            
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            return {
                "test_name": test_name,
                "passed": False,
                "execution_time": execution_time,
                "error": str(e)
            }
    
    def save_test_results(self):
        """テスト結果の保存"""
        try:
            # 詳細結果をJSONで保存
            results_file = f"{self.results_dir}/integration_test_results.json"
            test_report = {
                "test_session": self.timestamp,
                "executed_at": datetime.now().isoformat(),
                "total_tests": len(self.test_results),
                "passed_tests": sum(1 for r in self.test_results if r["passed"]),
                "failed_tests": sum(1 for r in self.test_results if not r["passed"]),
                "total_execution_time": sum(r.get("execution_time", 0) for r in self.test_results),
                "test_results": self.test_results
            }
            
            with open(results_file, 'w', encoding='utf-8') as f:
                json.dump(test_report, f, indent=2, ensure_ascii=False)
            
            # サマリーレポートをテキストで保存
            summary_file = f"{self.results_dir}/test_summary.txt"
            with open(summary_file, 'w', encoding='utf-8') as f:
                f.write("HTML VALIDATION PIPELINE - INTEGRATION TEST SUMMARY\n")
                f.write("=" * 60 + "\n")
                f.write(f"Test Session: {self.timestamp}\n")
                f.write(f"Executed At: {datetime.now().isoformat()}\n")
                f.write("\n")
                
                f.write(f"RESULTS:\n")
                f.write(f"Total Tests: {test_report['total_tests']}\n")
                f.write(f"Passed: {test_report['passed_tests']}\n")
                f.write(f"Failed: {test_report['failed_tests']}\n")
                f.write(f"Success Rate: {(test_report['passed_tests']/test_report['total_tests']*100):.1f}%\n")
                f.write(f"Total Execution Time: {test_report['total_execution_time']:.2f} seconds\n")
                f.write("\n")
                
                f.write("INDIVIDUAL TEST RESULTS:\n")
                f.write("-" * 60 + "\n")
                for result in self.test_results:
                    status = "PASS" if result["passed"] else "FAIL"
                    time_str = f"{result.get('execution_time', 0):.2f}s"
                    f.write(f"[{status}] {result['test_name']} ({time_str})\n")
                    if not result["passed"] and "error" in result:
                        f.write(f"       Error: {result['error']}\n")
                
            print(f"\n📊 Test results saved:")
            print(f"   📄 Detailed results: {results_file}")
            print(f"   📝 Summary report: {summary_file}")
            
        except Exception as e:
            print(f"❌ Failed to save test results: {e}")

def main():
    """メイン処理"""
    print("🧪 HTML Validation Pipeline Integration Tests")
    print(f"🐍 Python version: {sys.version}")
    print(f"📂 Working directory: {os.getcwd()}")
    
    # スクリプトディレクトリの存在確認
    if not os.path.exists("github-actions/scripts"):
        print("❌ Scripts directory not found: github-actions/scripts")
        print("Please run this from the project root directory")
        sys.exit(1)
    
    try:
        tester = IntegrationTester()
        success = tester.run_all_tests()
        
        if success:
            print("\n🎉 All integration tests passed!")
            sys.exit(0)
        else:
            print("\n❌ Some integration tests failed!")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n⚠️  Tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error running integration tests: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()