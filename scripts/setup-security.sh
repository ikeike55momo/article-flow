#!/bin/bash

# セキュリティ設定スクリプト
# APIキーの安全な管理とローテーションを支援

set -euo pipefail

# カラー出力用
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== Article Flow セキュリティセットアップ ===${NC}"

# 1. 環境変数ファイルのパーミッション設定
if [ -f ".env" ]; then
    chmod 600 .env
    echo -e "${GREEN}✓ .envファイルのパーミッションを設定しました（600）${NC}"
else
    echo -e "${YELLOW}! .envファイルが見つかりません。.env.exampleからコピーしてください${NC}"
    cp .env.example .env
    chmod 600 .env
fi

# 2. APIキーの検証
check_api_key() {
    if [ -f ".env" ]; then
        if grep -q "your_api_key_here" .env; then
            echo -e "${RED}✗ デフォルトのAPIキーが設定されています。実際のAPIキーに変更してください${NC}"
            return 1
        fi
        
        if grep -q "GOOGLE_AI_API_KEY=" .env && ! grep -q "GOOGLE_AI_API_KEY=$" .env; then
            echo -e "${GREEN}✓ APIキーが設定されています${NC}"
            return 0
        else
            echo -e "${RED}✗ APIキーが設定されていません${NC}"
            return 1
        fi
    fi
}

# 3. gitの設定確認
setup_git_security() {
    # pre-commitフックの作成
    mkdir -p .git/hooks
    cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
# APIキーの漏洩を防ぐpre-commitフック

# APIキーのパターンをチェック
if git diff --cached --name-only | xargs grep -E "(AIza[0-9A-Za-z-_]{35}|[0-9a-zA-Z]{32,})" 2>/dev/null; then
    echo "エラー: APIキーらしき文字列がコミットに含まれています"
    echo "環境変数を使用してください"
    exit 1
fi

# .envファイルがステージングされていないか確認
if git diff --cached --name-only | grep -E "^\.env$"; then
    echo "エラー: .envファイルはコミットできません"
    exit 1
fi

exit 0
EOF
    chmod +x .git/hooks/pre-commit
    echo -e "${GREEN}✓ git pre-commitフックを設定しました${NC}"
}

# 4. APIキーローテーションリマインダー
setup_rotation_reminder() {
    if [ -f ".env" ]; then
        # 最終更新日を記録
        echo "API_KEY_LAST_ROTATED=$(date +%Y-%m-%d)" >> .env.metadata
        echo -e "${GREEN}✓ APIキーローテーションの追跡を開始しました${NC}"
        echo -e "${YELLOW}  30日ごとにAPIキーを更新することを推奨します${NC}"
    fi
}

# 5. 使用量モニタリング設定
setup_monitoring() {
    cat > scripts/check-usage.sh << 'EOF'
#!/bin/bash
# Google AI API使用量チェックスクリプト

source .env

if [ -z "$GOOGLE_AI_API_KEY" ]; then
    echo "エラー: APIキーが設定されていません"
    exit 1
fi

# 簡易的な使用量チェック（実際のAPIエンドポイントに置き換える）
echo "API使用量の確認:"
echo "1. https://console.cloud.google.com にアクセス"
echo "2. 請求 > 予算とアラート で確認"
echo "3. 月間予算: $${MONTHLY_BUDGET_USD:-50}"
EOF
    chmod +x scripts/check-usage.sh
    echo -e "${GREEN}✓ 使用量モニタリングスクリプトを作成しました${NC}"
}

# 6. セキュリティチェックリスト
security_checklist() {
    echo -e "\n${YELLOW}=== セキュリティチェックリスト ===${NC}"
    echo "□ APIキーは環境変数で管理"
    echo "□ .envファイルは.gitignoreに含まれている"
    echo "□ APIキーに使用制限を設定"
    echo "□ HTTPSでの通信のみ許可"
    echo "□ 定期的なキーローテーション（30日）"
    echo "□ 使用量の監視とアラート設定"
    echo "□ チームメンバーへの最小権限付与"
}

# メイン実行
main() {
    check_api_key || echo -e "${YELLOW}APIキーの設定を完了してください${NC}"
    setup_git_security
    setup_rotation_reminder
    setup_monitoring
    security_checklist
    
    echo -e "\n${GREEN}セキュリティ設定が完了しました！${NC}"
    echo -e "${YELLOW}定期的に 'bash scripts/check-usage.sh' で使用量を確認してください${NC}"
}

main