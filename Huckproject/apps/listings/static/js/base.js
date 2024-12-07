
// 学部ごとに学科のオプションを変更する関数
function updateDepartments() {
    const faculty = document.getElementById('faculty').value;
    const departmentSelect = document.getElementById('department');
    
    // 学科の選択肢を一旦クリア
    departmentSelect.innerHTML = '';
    
    // 学部ごとの学科リスト
    const departments = {
        '理工学部': [
            "数学科",
            "電気電子工学科",
            "材料機能工学科",
            "応用化学科",
            "機械工学科", 
            "交通機械工学科",
            "メカトロニクス工学科",
            "社会基盤デザイン工学科", 
            "環境創造工学科",
            "建築学科"
        ],
        '情報工学部': [
            '情報工学科'
        ],
        "農学部": [
            "生物資源学科",
            "応用生物化学科",
            "生物環境科学科"
        ],
        "薬学部": [
            "薬学科"
        ],
        "法学部": [
            "法学科"
        ],
        '経営学部': [
            '経営学科',
            '国際経営学科'
        ],
        '経済学部': [
            '経済学科',
            '産業社会学科'
        ],
        "外国語学部": [
            "国際英語学科"
        ],
        "人間学部": [
            "人間学科"
        ],
        "都市情報学部": [
            "都市情報学科"
        ],
    };

    // 学部に対応する学科を動的に追加
    if (departments[faculty]) {
        departments[faculty].forEach(department => {
            const option = document.createElement('option');
            option.value = department;
            option.textContent = department;
            departmentSelect.appendChild(option);
        });
    }
}

// ページロード時に初期化（理工学部が選択されている場合）
window.onload = updateDepartments;

