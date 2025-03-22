// 获取最新排名按钮
const rankingButton = document.getElementById('rankingButton');
// 获取最新排名弹窗
const rankingModal = document.getElementById('rankingModal');
// 获取用于显示排名数据的元素
const rankingDataContainer = document.getElementById('rankingData');

// 为按钮添加点击事件监听器
rankingButton.addEventListener('click', fetchRankingData);

// 获取最新排名数据并显示在弹窗中
function fetchRankingData() {
    fetch('https://m.swranking.com/api/player/nowline')
        .then(response => response.json())
        .then(data => {
            displayRankingData(data);
        })
        .catch(error => console.error('Error:', error));
}

// 显示最新排名数据
function displayRankingData(data) {
    // 清除之前的内容
    rankingDataContainer.innerHTML = '';

    // 创建表格
    const table = document.createElement('table');
    table.style.width = '100%';
    table.style.borderCollapse = 'collapse';
    table.style.color = '#fff';

    // 创建表头
    const thead = table.createTHead();
    const headerRow = thead.insertRow();

    const headers = ['颜色', '等级', '排名', '分数'];
    headers.forEach(headerText => {
        const th = document.createElement('th');
        th.textContent = headerText;
        th.style.padding = '8px';
        th.style.textAlign = 'left';
        th.style.borderBottom = '1px solid #ddd';
        headerRow.appendChild(th);
    });

    // 创建表体
    const tbody = table.createTBody();

    // 添加数据行
    const colors = ['金', '绿', '红'];
    const dataKeys = ['c', 's', 'g'];

    for (let i = 0; i < colors.length; i++) {
        const color = colors[i];
        const dataKey = dataKeys[i];

        for (let j = 1; j <= 3; j++) {
            const key = dataKey + j;
            const ranking = data.data[key];

            const tr = tbody.insertRow();

            // 颜色
            const colorCell = tr.insertCell();
            colorCell.textContent = color;
            colorCell.style.padding = '8px';
            colorCell.style.textAlign = 'left';
            colorCell.style.borderBottom = '1px solid #ddd';

            // 分数
            const scoreCell = tr.insertCell();
            scoreCell.textContent = ranking.score;
            scoreCell.style.padding = '8px';
            scoreCell.style.textAlign = 'left';
            scoreCell.style.borderBottom = '1px solid #ddd';
        }
    }

    // 将表格添加到容器中
    rankingDataContainer.appendChild(table);

    // 显示弹窗
    rankingModal.style.display = "block";
}
