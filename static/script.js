//点击otherButton跳转到https://www.ggrmm.top/%E6%B8%B8%E6%88%8F/%E9%AD%94%E7%81%B5%E5%8F%AC%E5%94%A4/

        // 获取弹窗元素
        const historyModal = document.getElementById('historyModal');
        const rewardModal = document.getElementById('rewardModal');

        // 点击其他功能按钮时，跳转到指定的URL
        document.getElementById('otherButton').addEventListener('click', function() {       
            window.location.href = 'https://www.ggrmm.top/游戏/魔灵召唤/';
        });
        // 点击考验之塔按钮时，跳转到指定的URL
        document.getElementById('coaButton').addEventListener('click', function() {
            window.location.href = 'https://kdocs.cn/l/cheUAqx2JKLJ';
        });
        // 点击建议反馈按钮时，跳转到指定的URL
        document.getElementById('feedbackButton').addEventListener('click', function() {
            window.location.href = 'https://docs.qq.com/form/page/DSnJnaVNzdGpndWtv';
        });
        // 获取关闭按钮
        const closeBtn = document.getElementsByClassName('close');
        // 当用户点击关闭按钮时，关闭弹窗
        for (let i = 0; i < closeBtn.length; i++) {
            closeBtn[i].onclick = function() {
                historyModal.style.display = 'none';
                rewardModal.style.display = 'none';
            }
        }
        // 获取load弹窗元素
        const loader = document.querySelector('.loader');
        const loadingMessage = document.querySelector('.loading-message');

        // 获取绑定页面中的各个元素
        const hiveidInput = document.getElementById('hiveid');
        const hiveidError = document.getElementById('hiveid-error');
        const serverSelect = document.getElementById('server');
        const serverError = document.getElementById('server-error');
        const vipcodeInput = document.getElementById('vipcode');
        const vipcodeError = document.getElementById('vipcode-error');
        const submitButton = document.getElementById('submitButton');

        // 获取状态消息元素
        const statusMessage = document.getElementById('status-message');
        // 设置状态消息内容并显示
        function setStatusMessage(message) {
            statusMessage.textContent = message;
            statusMessage.classList.add('show'); // 添加显示类

            // 一段时间后隐藏状态消息
            setTimeout(() => {
                statusMessage.classList.remove('show'); // 移除显示类
            }, 3000); // 3秒后隐藏
        }

        // 显示加载动画和加载提示信息
        function showLoading() {
            loader.style.display = 'block';
            loadingMessage.style.display = 'block';
        }
        // 隐藏加载动画和加载提示信息
        function hideLoading() {
            loader.style.display = 'none';
            loadingMessage.style.display = 'none';
        }

        let isSubmitting = false;
        // 监听输入框和选择框的变化事件
        hiveidInput.addEventListener('input', validateInputs);
        serverSelect.addEventListener('change', validateInputs);
        vipcodeInput.addEventListener('input', validateInputs);
        // 监听提交按钮的点击事件
        submitButton.addEventListener('click', handleSubmit);
        // 设置自定义验证消息
        hiveidInput.setCustomValidity('');  // 初始时设置为空
        serverSelect.setCustomValidity('');  // 初始时设置为空
        vipcodeInput.setCustomValidity('');  // 初始时设置为空

        // 监听表单提交事件
        document.getElementById('bindForm').addEventListener('submit', handleSubmit);

        // 验证输入框中的内容是否有效
        function validateInputs() {
            const hiveId = hiveidInput.value.trim();
            const server = serverSelect.value;
            const vipCode = vipcodeInput.value.trim();
            const isHiveIdValid = /^[\w.]+$/.test(hiveId);
            const isVipCodeValid = /^\w+$/.test(vipCode);

            if (!isHiveIdValid) {
                console.log('HiveID验证失败，即将设置自定义错误消息');

                hiveidInput.setCustomValidity('HiveID只能包含字母和数字，请重新输入');
                hiveidError.style.display = 'block'; // 显示错误消息
                hiveidError.textContent = 'HiveID只能包含字母和数字，请重新输入';
                console.log('自定义错误消息已设置');
            } else {
                hiveidInput.setCustomValidity('');
                hiveidError.style.display = 'none'; // 隐藏错误消息
                hiveidError.textContent = '';
            }
            if (!server) {
                serverSelect.setCustomValidity('请选择服务器');
                serverError.style.display = 'block'; // 显示错误消息
                serverError.textContent = '请选择服务器';
            } else {
                serverSelect.setCustomValidity('');
                serverError.style.display = 'none'; // 隐藏错误消息

                serverError.textContent = '';
            }
            if (!isVipCodeValid) {
                vipcodeInput.setCustomValidity('VIP Code只能包含字母和数字，请重新输入');
                vipcodeError.style.display = 'block'; // 显示错误消息
                vipcodeError.textContent = 'VIP Code只能包含字母和数字，请重新输入';
            } else {
                vipcodeInput.setCustomValidity('');
                vipcodeError.style.display = 'none'; // 隐藏错误消息
                vipcodeError.textContent = '';
            }
            // 根据验证结果启用或禁用提交按钮
            submitButton.disabled = !(isHiveIdValid && server && isVipCodeValid);
            return isHiveIdValid && server && isVipCodeValid;
        }





        // 处理绑定表单提交事件
        function handleSubmit(event) {
            event.preventDefault(); // 阻止表单默认提交行为

            if (isSubmitting) return; // 如果正在提交，忽略重复提交

            if (!validateInputs()) return; // 如果输入无效，不提交表单

            isSubmitting = true;
            showLoading(); // 显示加载动画和加载提示信息
            submitButton.disabled = true; // 禁用提交按钮
            
            // 去除hiveid中的空格
            const hiveid = hiveidInput.value.replace(/\s/g, '');
            // 构造表单数据
            const formData = {
                wxid: 'player_wxid', // 假设wxid固定为'player_wxid'
                hiveid: hiveid,
                autonum: '10', // 假设autonum固定为'10'
                server: serverSelect.value,
                email: 'player_email', // 假设email固定为'player_email'
                vip: '0', // 假设vip固定为'0'
                vipcode: vipcodeInput.value
            };
            // 使用Fetch API发送数据到bind.py
            fetch('/bind', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            })
            .then(response => {
                // 检查响应是否成功
                if (!response.ok) {
                    throw new Error('Network response was not ok'+ response.statusText);
                }
                // 服务器返回的是字符串，直接读取文本内容，转为JSON对象
                // 然后获取message属性的值
                // 然后使用服务器返回的来设置状态消息
                return response.text();
            })
           .then(text => {
                // 使用服务器返回的字符串转码后来设置状态消息
                const jsonData = JSON.parse(text);
                setStatusMessage(jsonData.message);
            })
           .catch(error => {
                console.error('Error:', error);
                setStatusMessage('发生错误，请重试。');
            })
           .finally(() => {
                isSubmitting = false;
                // 隐藏加载动画和加载提示信息
                hideLoading();
                submitButton.disabled = false; // 恢复提交按钮状态
                //重置表单hiveid
                hiveidInput.value = '';
            });
        }
            // 监听表单提交事件
            const bindForm = document.getElementById('bindForm');
            bindForm.addEventListener('submit', handleSubmit);
                // 表单提交后重新计算并设置弹窗大小
            bindForm.addEventListener('submit', function() {
                const modalContent = document.querySelector('.modal-content');
                modalContent.style.width = '80%';
                modalContent.style.maxWidth = '700px';
            });
        ;
        //历史领取数据
        // 获取历史领取按钮
        const historyButton = document.getElementById('historyButton');
        // 为按钮添加点击事件监听器
        historyButton.addEventListener('click', fetchHistory);
        // 绑定点击事件到历史领取按钮
        document.getElementById('historyButton').addEventListener('click', fetchHistory);
        // 当用户点击历史领取按钮时，显示弹窗
        historyButton.onclick = function() {
            historyModal.style.display = "block";
        }

        // 当用户点击任何地方时，关闭弹窗
        window.onclick = function(event) {
            if (event.target == historyModal || event.target == rewardModal) {
                historyModal.style.display = "none";
                rewardModal.style.display = "none";
            }
        }
        // 获取历史领取数据并显示在弹窗中
        function fetchHistory() {
            fetch('/history')
                .then(response => response.text())  // 获取CSV文件内容
                .then(csvText => {
                    const csvData = parseCSV(csvText);  // 解析CSV
                    displayCSV(csvData);  // 显示CSV数据
                })
                .catch(error => console.error('Error:', error));
        }
        // 解析CSV文本
function parseCSV(csvText) {
    const rows = csvText.split('\n');
    const result = [];
    for (let i = 0; i < rows.length; i++) {
        result.push(rows[i].split(/,(?=(?:(?:[^"]*"){2})*[^"]*$)/));
    }
    return result;
}
// 显示CSV数据
function displayCSV(csvData) {
    // 获取用于显示 CSV 数据的元素
    const csvTableContainer = document.getElementById('csvData');
    const dataAnalysisContainer = document.getElementById('dataAnalysis');
    
    // 清除之前的内容
    csvTableContainer.innerHTML = '';
    dataAnalysisContainer.innerHTML = '';
    
    // 保存表头行
    const headerRow = csvData[0];
    
    // 跳过表头行，只处理数据行
    const dataRows = csvData.slice(1).filter(row => row && row.length > 0);
    
    // 数据分析
    const analysisData = analyzeData(dataRows);
    
    // 显示数据分析
    displayDataAnalysis(analysisData);
    
    // 排序数据，最新的数据在最上面
    dataRows.sort((a, b) => {
        const dateA = new Date(a[4]); // 假设日期在第5列
        const dateB = new Date(b[4]);
        return dateB - dateA; // 降序
    });

    const pageSize = 20; // 每页显示的行数
    let currentPage = 1; // 当前页码

    function displayPage(page) {
        const startRow = (page - 1) * pageSize;
        const endRow = Math.min(startRow + pageSize, dataRows.length);

        // 清除表格内容
        csvTableContainer.innerHTML = '';
        const csvTable = document.createElement('table');
        const fragment = document.createDocumentFragment();

        // 遍历CSV数据
        for (let i = startRow; i < endRow; i++) {
            const row = dataRows[i];
            
            // 只显示有内容的列，去掉空白列
            // 假设列顺序是: 兑换码, (空白), 用户ID, 服务器, 日期, 状态
            // 我们去掉空白列（索引1）
            const columnsToShow = [0, 2, 3, 4, 5]; // 只显示需要的列
            
            // 每个字段占一行
            for (let j = 0; j < columnsToShow.length; j++) {
                const colIndex = columnsToShow[j];
                if (colIndex >= row.length) continue;
                
                const cell = row[colIndex];
                const tr = document.createElement('tr');
                const td = document.createElement('td');
                
                // 日期列（索引4）完整显示，不截断
                if (colIndex === 4) {
                    td.textContent = cell;
                    td.style.whiteSpace = 'nowrap';
                } else {
                    td.textContent = cell;
                }
                
                tr.appendChild(td);
                fragment.appendChild(tr);
            }

            // 每5个记录后添加一个分隔行（一个记录有5行）
            if ((i - startRow + 1) % 5 === 0 && i !== endRow - 1) {
                const separatorTr = document.createElement('tr');
                const separatorTd = document.createElement('td');
                separatorTd.style.height = '20px';
                separatorTd.style.background = 'linear-gradient(90deg, transparent, #475569, transparent)';
                separatorTd.style.borderBottom = 'none';
                separatorTr.appendChild(separatorTd);
                fragment.appendChild(separatorTr);
            }
        }

        csvTable.appendChild(fragment);
        csvTableContainer.appendChild(csvTable);

        // 显示弹窗
        historyModal.style.display = "block";
    }

    displayPage(currentPage);
}



        // 最新兑换码
        // 获取最新兑换码按钮
        const rewardButton = document.getElementById('rewardButton');
        // 为按钮添加点击事件监听器
        rewardButton.addEventListener('click', fetchReward);
        // 当用户点击最新兑换码按钮时，显示弹窗
        rewardButton.onclick = function() {
            fetchReward();
        }

        // 获取最新兑换码数据并显示在弹窗中
        function fetchReward() {
           
            fetch('/reward')
               .then(response => response.text())  // 获取CSV文件内容
               .then(csvText => {
                    const csvData = parseCSV(csvText);  // 解析CSV
                    displayReward(csvData);  // 显示CSV数据
                })
              .catch(error => console.error('Error:', error));
        }
        // 解析CSV文本
        function parseCSV(csvText) {
            const rows = csvText.split('\n');
            return rows.map(row => {
                return row.split(/,(?=(?:(?:[^"]*"){2})*[^"]*$)/);
            });
        }
// 显示最新兑换码数据
function displayReward(csvData) {
    // 强制修改标题
    const rewardModalTitle = document.querySelector('#rewardModal h2');
    if (rewardModalTitle) {
        rewardModalTitle.textContent = '可用兑换码';
    }
    
    // 获取用于显示 CSV 数据的元素
    const csvTableContainer = document.getElementById('rewardData');
    // 清除之前的内容
    csvTableContainer.innerHTML = '';
    const csvTable = document.createElement('table');
    const fragment = document.createDocumentFragment(); // 创建 DOM Fragment

    // 遍历CSV数据，跳过表头行（i从1开始）
    for (let i = 1; i < csvData.length; i++) {
        const row = csvData[i];
        if (!row || row.length === 0) continue; // 跳过空行
        // 跳过只有一个空单元格的行
        if (row.length === 1 && (!row[0] || row[0].trim() === '')) continue;
        
        const tr = document.createElement('tr');

        // 显示所有有内容的列，只跳过完全空白的列
        for (let j = 0; j < row.length; j++) {
            const cell = row[j];
            // 跳过完全空白的列
            if (!cell || cell.trim() === '') continue;
            
            const td = document.createElement('td');
            td.textContent = cell;
            tr.appendChild(td);
        }
        fragment.appendChild(tr);
    }

    // 对CSV数据进行倒序排序
    const rows = Array.from(fragment.childNodes);
    rows.reverse();

    // 清除表格内容并重新添加排序后的行
    csvTable.innerHTML = '';
    for (let i = 0; i < rows.length; i++) {
        csvTable.appendChild(rows[i]);
    }

    // 将排序后的表格添加到容器中
    csvTableContainer.appendChild(csvTable);

    // 显示CSV数据
    rewardModal.style.display = "block";
}

        // 增加兑换码
        // 获取增加兑换码提交按钮
        const addCodeSubmitButton = document.getElementById('addCodeSubmitButton');
        // 监听增加兑换码表单提交事件
        addCodeSubmitButton.addEventListener('click', handleAddCodeSubmit);
        
        // 监听增加兑换码表单提交事件
        const addCodeForm = document.getElementById('addCodeForm');
        addCodeForm.addEventListener('submit', handleAddCodeSubmit);
        
        // 监听兑换码输入框变化
        const codeInput = document.getElementById('code');
        codeInput.addEventListener('input', valicodeInputs);
        
        //兑换码需要是英文字符串，不能包含中文
        function valicodeInputs() {
            const code = document.getElementById('code').value.trim();
            const isCodeValid = /^[a-zA-Z0-9]+$/.test(code);
            if (!isCodeValid) {
                document.getElementById('code').setCustomValidity('兑换码不能包含中文，请重新输入');
            } else {
                document.getElementById('code').setCustomValidity('');
            }
            addCodeSubmitButton.disabled = !(isCodeValid);
            return isCodeValid;
        }

        // 处理增加兑换码表单提交事件
        function handleAddCodeSubmit(event) {
            event.preventDefault(); // 阻止表单默认提交行为
            if (isSubmitting) return; // 如果正在提交，忽略重复提交

            if (!valicodeInputs()) return; // 如果输入无效，兑换码需要是英文字符串，不能包含中文，不提交表单

            isSubmitting = true;
            loader.style.display = 'block';
            loadingMessage.style.display = 'block';

            addCodeSubmitButton.disabled = true; // 禁用提交按钮

            // 构造表单数据
            const formData = {
                code: document.getElementById('code').value
            };  

            // 使用Fetch API发送数据到add_code
            fetch('/add_code', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            })
            .then(response => {
                // 检查响应是否成功
                if (!response.ok) {
                    throw new Error('Network response was not ok'+ response.statusText);
                }
                // 服务器返回的是字符串，直接读取文本内容，转为JSON对象
                // 然后获取message属性的值
                // 然后使用服务器返回的来设置状态消息
                return response.text();
            })
           .then(text => {
                // 使用服务器返回的字符串转码后来设置状态消息
                const jsonData = JSON.parse(text);
                setStatusMessage(jsonData.message);
            })
           .catch(error => {
                console.error('Error:', error);
                setStatusMessage('发生错误，请重试。');
            })
           .finally(() => {
                isSubmitting = false;
                 // 请求完成后，隐藏加载动画和提示信息，并启用按钮
                loader.style.display = 'none';
                loadingMessage.style.display = 'none';
                addCodeSubmitButton.disabled = false; // 重新启用提交按钮
                addCodeForm.reset(); // 重置表单
            });
        }
        
        var script = document.createElement("script");
        script.setAttribute("type","text/javascript");
        script.setAttribute("id","myhk");
        // script.setAttribute("src","https://myhkw.cn/api/player/174158352560"); // Disabled as per request
        script.setAttribute("key","174158352560");
        script.setAttribute("m","1");
        document.documentElement.appendChild(script);

// 获取RTA分数线数据
function updateRTARank() {
    fetch('/get_rta_rank')
        .then(response => response.json())
        .then(data => {
            const rankText = document.getElementById('rta-rank-text');
            if (rankText) {
                rankText.textContent = data.message;
            }
        })
        .catch(error => {
            console.error('获取RTA分数线失败:', error);
        });
}

// 解析CSV数据（支持包含逗号的字段）
function parseCSV(csvText) {
    const lines = csvText.split('\n');
    const dataRows = [];
    
    // 跳过表头
    for (let i = 1; i < lines.length; i++) {
        const line = lines[i].trim();
        if (!line) continue;
        
        // 使用正则表达式解析CSV，支持包含逗号的字段
        const regex = /(?:^|,)("(?:[^"]*(?:""[^"]*)*)"|[^,]*)/g;
        const row = [];
        let match;
        
        while ((match = regex.exec(line)) !== null) {
            let value = match[1] || match[0];
            // 移除开头的逗号
            if (value.startsWith(',')) {
                value = value.substring(1);
            }
            // 移除引号
            if (value.startsWith('"') && value.endsWith('"')) {
                value = value.substring(1, value.length - 1).replace(/""/g, '"');
            }
            row.push(value);
        }
        
        dataRows.push(row);
    }
    
    return dataRows;
}

// 数据分析函数
function analyzeData(dataRows) {
    const totalRecords = dataRows.length;
    const serverCounts = {};
    const statusCounts = {};
    const codeCounts = {};
    const rewardCounts = {};
    const dates = [];
    const autoDates = [];
    const autoDateCounts = {};
    const allDatesSet = new Set();
    const autoRedeemCodes = new Set();
    let latestAutoDate = null;
    
    dataRows.forEach(row => {
        // 服务器 (索引3)
        const server = row[3];
        if (server) {
            serverCounts[server] = (serverCounts[server] || 0) + 1;
        }
        
        // 状态 (索引5)
        const status = row[5];
        if (status) {
            statusCounts[status] = (statusCounts[status] || 0) + 1;
        }
        
        // 兑换码 (索引0)
        const code = row[0];
        if (code) {
            codeCounts[code] = (codeCounts[code] || 0) + 1;
        }
        
        // 奖励 (索引1)
        const reward = row[1];
        if (reward && reward.trim()) {
            rewardCounts[reward] = (rewardCounts[reward] || 0) + 1;
        }
        
        // 日期 (索引4)
        const dateStr = row[4];
        if (dateStr) {
            const date = new Date(dateStr);
            // 检查日期是否有效
            if (!isNaN(date.getTime())) {
                dates.push(date);
                
                // 格式化为 YYYY-MM-DD 日期字符串
                const dateKey = date.toISOString().split('T')[0];
                allDatesSet.add(dateKey);
                
                // 如果是自动领取，记录日期和兑换码
                if (status && status.includes('自动')) {
                    autoDates.push(date);
                    autoDateCounts[dateKey] = (autoDateCounts[dateKey] || 0) + 1;
                    if (code) {
                        autoRedeemCodes.add(code);
                    }
                    
                    // 更新最新自动领取时间
                    if (!latestAutoDate || date > latestAutoDate) {
                        latestAutoDate = date;
                    }
                }
            }
        }
    });
    
    // 找出最热门的兑换码
    let mostPopularCode = '';
    let maxCodeCount = 0;
    for (const [code, count] of Object.entries(codeCounts)) {
        if (count > maxCodeCount) {
            maxCodeCount = count;
            mostPopularCode = code;
        }
    }
    
    // 找出最热门奖励
    let mostPopularReward = '';
    let maxRewardCount = 0;
    for (const [reward, count] of Object.entries(rewardCounts)) {
        if (count > maxRewardCount) {
            maxRewardCount = count;
            mostPopularReward = reward;
        }
    }
    
    // 计算自动领取和手动领取的数量
    let autoCount = 0;
    let manualCount = 0;
    for (const [status, count] of Object.entries(statusCounts)) {
        if (status && status.includes('自动')) {
            autoCount += count;
        } else if (status && status.includes('手动')) {
            manualCount += count;
        }
    }
    
    // 计算时间相关统计
    let totalDays = 0;
    let earliestDate = null;
    let latestDate = null;
    let mostAutoDay = '';
    let mostAutoDayCount = 0;
    
    if (dates.length > 0) {
        // 找出最早和最晚的日期（使用时间戳比较）
        const timestamps = dates.map(date => date.getTime());
        
        // 过滤掉无效的时间戳
        const validTimestamps = timestamps.filter(ts => !isNaN(ts));
        
        if (validTimestamps.length > 0) {
            const minTimestamp = Math.min(...validTimestamps);
            const maxTimestamp = Math.max(...validTimestamps);
            
            earliestDate = new Date(minTimestamp);
            latestDate = new Date(maxTimestamp);
            
            // 计算总天数
            const timeDiff = maxTimestamp - minTimestamp;
            totalDays = Math.ceil(timeDiff / (1000 * 3600 * 24)) + 1;
            
            // 找出自动领取次数最多的一天
            for (const [dateKey, count] of Object.entries(autoDateCounts)) {
                if (count > mostAutoDayCount) {
                    mostAutoDayCount = count;
                    mostAutoDay = dateKey;
                }
            }
        }
    }
    
    return {
        totalRecords,
        serverCounts,
        statusCounts,
        mostPopularCode,
        mostPopularCodeCount: maxCodeCount,
        mostPopularReward,
        mostPopularRewardCount: maxRewardCount,
        autoCount,
        manualCount,
        totalDays,
        earliestDate,
        latestDate,
        latestAutoDate,
        mostAutoDay,
        mostAutoDayCount,
        autoRedeemCodeCount: autoRedeemCodes.size
    };
}

// 显示数据分析
function displayDataAnalysis(analysisData) {
    const container = document.getElementById('dataAnalysis');
    
    // 生成状态统计HTML
    let statusHtml = '';
    for (const [status, count] of Object.entries(analysisData.statusCounts)) {
        statusHtml += `<div class="analysis-item">
            <div class="analysis-value">${count}</div>
            <div class="analysis-label">${status}</div>
        </div>`;
    }
    
    // 格式化日期显示
    function formatDate(date) {
        if (!date) return '-';
        const d = new Date(date);
        return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')} ${String(d.getHours()).padStart(2, '0')}:${String(d.getMinutes()).padStart(2, '0')}`;
    }
    
    const html = `
        <h3>📊 数据统计</h3>
        <div class="analysis-grid">
            <div class="analysis-item">
                <div class="analysis-value">${analysisData.totalRecords}</div>
                <div class="analysis-label">总领取次数</div>
            </div>
            <div class="analysis-item">
                <div class="analysis-value">${analysisData.autoCount}</div>
                <div class="analysis-label">自动领取次数</div>
            </div>
            <div class="analysis-item">
                <div class="analysis-value">${analysisData.autoRedeemCodeCount || 0}</div>
                <div class="analysis-label">自动领取过的<br>兑换码数</div>
            </div>
            <div class="analysis-item">
                <div class="analysis-value">${analysisData.totalDays || 0}</div>
                <div class="analysis-label">数据覆盖天数</div>
            </div>
        </div>
        
        <h3 style="margin-top: 20px; font-size: 1em;">⏰ 时间信息</h3>
        <div class="analysis-grid">
            <div class="analysis-item">
                <div class="analysis-value" style="font-size: 0.9em;">${formatDate(analysisData.latestAutoDate)}</div>
                <div class="analysis-label">最新自动领取时间</div>
            </div>
            <div class="analysis-item">
                <div class="analysis-value">${analysisData.mostAutoDayCount || 0}</div>
                <div class="analysis-label">最多自动领取<br>最多一天</div>
            </div>
        </div>
        
        <h3 style="margin-top: 20px; font-size: 1em;">📈 状态分布</h3>
        <div class="analysis-grid">
            ${statusHtml}
        </div>
    `;
    
    container.innerHTML = html;
}

// 更新统计信息显示
function updateMarquee(analysisData) {
    const marqueeText = document.querySelector('.marquee-text');
    if (!marqueeText) return;
    
    const text = `🎉 总领取 <span class="marquee-highlight">${analysisData.totalRecords}</span> 次 🤖 自动领取 <span class="marquee-highlight">${analysisData.autoCount}</span> 次 🎁 已自动领取过 <span class="marquee-highlight">${analysisData.autoRedeemCodeCount}</span> 个兑换码 📅 覆盖 <span class="marquee-highlight">${analysisData.totalDays || 0}</span> 天 ⚡ 稳定运行中...`;
    
    marqueeText.innerHTML = text;
}

// 加载跑马灯数据
function loadMarqueeData() {
    fetch('/history')
        .then(response => response.text())
        .then(csvText => {
            const dataRows = parseCSV(csvText);
            const analysisData = analyzeData(dataRows);
            updateMarquee(analysisData);
        })
        .catch(error => {
            console.error('加载跑马灯数据失败:', error);
        });
}

// 显示CSV数据
function displayCSV(csvData) {
    const csvTableContainer = document.getElementById('csvData');
    const dataAnalysisContainer = document.getElementById('dataAnalysis');
    
    // 清除之前的内容
    csvTableContainer.innerHTML = '';
    dataAnalysisContainer.innerHTML = '';
    
    // 保存表头行
    const headerRow = csvData[0];
    
    // 跳过表头行，只处理数据行
    const dataRows = csvData.slice(1).filter(row => row && row.length > 0);
    
    // 数据分析
    const analysisData = analyzeData(dataRows);
    
    // 显示数据分析
    displayDataAnalysis(analysisData);
    
    // 排序数据，最新的数据在最上面
    dataRows.sort((a, b) => {
        const dateA = new Date(a[4]); // 假设日期在第5列
        const dateB = new Date(b[4]);
        return dateB - dateA; // 降序
    });

    const pageSize = 20; // 每页显示的行数
    let currentPage = 1; // 当前页码

    function displayPage(page) {
        const startRow = (page - 1) * pageSize;
        const endRow = Math.min(startRow + pageSize, dataRows.length);

        // 清除表格内容
        csvTableContainer.innerHTML = '';
        const csvTable = document.createElement('table');
        const fragment = document.createDocumentFragment();

        // 遍历CSV数据
        for (let i = startRow; i < endRow; i++) {
            const row = dataRows[i];
            
            // 只显示有内容的列，去掉空白列
            // 假设列顺序是: 兑换码, (空白), 用户ID, 服务器, 日期, 状态
            // 我们去掉空白列（索引1）
            const columnsToShow = [0, 2, 3, 4, 5]; // 只显示需要的列
            
            // 每个字段占一行
            for (let j = 0; j < columnsToShow.length; j++) {
                const colIndex = columnsToShow[j];
                if (colIndex >= row.length) continue;
                
                const value = row[colIndex];
                if (!value || value.trim() === '') continue;
                
                const dataRow = document.createElement('tr');
                
                // 字段名称
                const fieldName = headerRow[colIndex];
                const fieldCell = document.createElement('td');
                fieldCell.className = 'field-name';
                fieldCell.textContent = fieldName + ':';
                dataRow.appendChild(fieldCell);
                
                // 字段值
                const valueCell = document.createElement('td');
                valueCell.className = 'field-value';
                valueCell.textContent = value;
                dataRow.appendChild(valueCell);
                
                fragment.appendChild(dataRow);
            }
            
            // 每5条记录添加一个分隔行
            if ((i + 1) % 5 === 0 && i < endRow - 1) {
                const separatorRow = document.createElement('tr');
                const separatorCell = document.createElement('td');
                separatorCell.colSpan = 2;
                separatorCell.className = 'separator';
                separatorRow.appendChild(separatorCell);
                fragment.appendChild(separatorRow);
            }
        }

        csvTable.appendChild(fragment);
        csvTableContainer.appendChild(csvTable);

        // 显示分页信息
        const totalPages = Math.ceil(dataRows.length / pageSize);
        const pagination = document.createElement('div');
        pagination.className = 'pagination';
        
        // 上一页按钮
        const prevButton = document.createElement('button');
        prevButton.textContent = '上一页';
        prevButton.disabled = currentPage === 1;
        prevButton.onclick = () => {
            if (currentPage > 1) {
                currentPage--;
                displayPage(currentPage);
            }
        };
        pagination.appendChild(prevButton);
        
        // 页码信息
        const pageInfo = document.createElement('span');
        pageInfo.textContent = `第 ${currentPage} 页，共 ${totalPages} 页`;
        pageInfo.className = 'page-info';
        pagination.appendChild(pageInfo);
        
        // 下一页按钮
        const nextButton = document.createElement('button');
        nextButton.textContent = '下一页';
        nextButton.disabled = currentPage === totalPages;
        nextButton.onclick = () => {
            if (currentPage < totalPages) {
                currentPage++;
                displayPage(currentPage);
            }
        };
        pagination.appendChild(nextButton);
        
        csvTableContainer.appendChild(pagination);
    }

    // 显示第一页
    displayPage(currentPage);
}

document.addEventListener('DOMContentLoaded', function() {
    // 强制修改HiveID标签
    const hiveidLabel = document.querySelector('label[for="hiveid"]');
    if (hiveidLabel) {
        hiveidLabel.textContent = 'HiveID';
    }
    
    // 初始化兑换码按钮状态
    const addCodeSubmitBtn = document.getElementById('addCodeSubmitButton');
    const codeInput = document.getElementById('code');
    if (addCodeSubmitBtn && codeInput) {
        const code = codeInput.value.trim();
        const isCodeValid = /^[a-zA-Z0-9]+$/.test(code);
        addCodeSubmitBtn.disabled = !isCodeValid;
    }
    
    // 加载并更新跑马灯
    loadMarqueeData();
    
    // 初始获取RTA分数线数据
    updateRTARank();
    // 每60秒更新一次数据
    setInterval(updateRTARank, 60000);
});

