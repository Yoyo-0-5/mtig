#!/bin/bash
# MQTT 測試資料發布器 - 快速啟動腳本

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# 顏色定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 檢查 Python 是否安裝
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ 錯誤: 未找到 Python3${NC}"
    exit 1
fi

# 檢查並安裝依賴
check_dependencies() {
    echo -e "${BLUE}🔍 檢查依賴...${NC}"
    if ! python3 -c "import paho.mqtt.client" &> /dev/null; then
        echo -e "${YELLOW}📦 安裝 paho-mqtt...${NC}"
        pip3 install paho-mqtt
    fi
    echo -e "${GREEN}✅ 依賴檢查完成${NC}\n"
}

# 顯示選單
show_menu() {
    echo -e "${BLUE}╔══════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║     MQTT 測試資料發布器 - 快速啟動選單         ║${NC}"
    echo -e "${BLUE}╚══════════════════════════════════════════════════╝${NC}\n"
    
    echo -e "${GREEN}📡 持續發布模式:${NC}"
    echo "  1) 持續發布測試資料 (每 0.5 秒)"
    echo ""
    
    echo -e "${GREEN}📦 批量發布模式:${NC}"
    echo "  2) 快速測試 (100 條消息)"
    echo "  3) 小規模測試 (1000 條消息, 50 msg/s)"
    echo "  4) 中規模測試 (5000 條消息, 100 msg/s)"
    echo "  5) 大規模測試 (10000 條消息, 200 msg/s)"
    echo "  6) 超大規模測試 (50000 條消息, 500 msg/s)"
    echo ""
    
    echo -e "${GREEN}📅 歷史資料填充:${NC}"
    echo "  7) 填充 24 小時歷史資料 (5 分鐘間隔)"
    echo "  8) 填充 7 天歷史資料 (15 分鐘間隔)"
    echo "  9) 填充 30 天歷史資料 (30 分鐘間隔)"
    echo ""
    
    echo -e "${GREEN}🔧 其他:${NC}"
    echo "  10) 自訂參數"
    echo "  0) 退出"
    echo ""
}

# 執行持續發布
run_continuous() {
    echo -e "${GREEN}🚀 啟動持續發布模式...${NC}"
    echo -e "${YELLOW}按 Ctrl+C 停止${NC}\n"
    python3 mqtt_test_publisher.py
}

# 執行批量發布
run_batch() {
    local messages=$1
    local rate=$2
    local devices=${3:-10}
    
    echo -e "${GREEN}🚀 啟動批量發布...${NC}"
    echo -e "   消息數: ${messages}"
    echo -e "   速率: ${rate} msg/s"
    echo -e "   設備數: ${devices}\n"
    
    python3 mqtt_batch_publisher.py --mode batch --messages "$messages" --rate "$rate" --devices "$devices"
}

# 執行歷史資料填充
run_historical() {
    local hours=$1
    local interval=$2
    local devices=${3:-10}
    
    echo -e "${GREEN}📅 啟動歷史資料填充...${NC}"
    echo -e "   時間範圍: ${hours} 小時"
    echo -e "   資料間隔: ${interval} 分鐘"
    echo -e "   設備數: ${devices}\n"
    
    python3 mqtt_batch_publisher.py --mode historical --hours "$hours" --interval "$interval" --devices "$devices"
}

# 自訂參數
custom_parameters() {
    echo -e "${BLUE}🔧 自訂參數${NC}\n"
    
    echo "選擇模式:"
    echo "  1) 批量發布"
    echo "  2) 歷史資料填充"
    read -p "請選擇 [1-2]: " mode_choice
    
    case $mode_choice in
        1)
            read -p "消息總數 (預設 1000): " messages
            messages=${messages:-1000}
            read -p "每秒速率 (預設 100): " rate
            rate=${rate:-100}
            read -p "設備數量 (預設 10): " devices
            devices=${devices:-10}
            run_batch "$messages" "$rate" "$devices"
            ;;
        2)
            read -p "往前追溯小時數 (預設 24): " hours
            hours=${hours:-24}
            read -p "資料間隔分鐘數 (預設 5): " interval
            interval=${interval:-5}
            read -p "設備數量 (預設 10): " devices
            devices=${devices:-10}
            run_historical "$hours" "$interval" "$devices"
            ;;
        *)
            echo -e "${RED}❌ 無效選擇${NC}"
            ;;
    esac
}

# 主程式
main() {
    check_dependencies
    
    while true; do
        show_menu
        read -p "請選擇操作 [0-10]: " choice
        echo ""
        
        case $choice in
            1)
                run_continuous
                ;;
            2)
                run_batch 100 10
                ;;
            3)
                run_batch 1000 50
                ;;
            4)
                run_batch 5000 100
                ;;
            5)
                run_batch 10000 200
                ;;
            6)
                run_batch 50000 500
                ;;
            7)
                run_historical 24 5
                ;;
            8)
                run_historical 168 15
                ;;
            9)
                run_historical 720 30
                ;;
            10)
                custom_parameters
                ;;
            0)
                echo -e "${GREEN}👋 再見！${NC}"
                exit 0
                ;;
            *)
                echo -e "${RED}❌ 無效選擇，請重新輸入${NC}\n"
                ;;
        esac
        
        echo ""
        read -p "按 Enter 繼續..."
        clear
    done
}

# 執行主程式
main
