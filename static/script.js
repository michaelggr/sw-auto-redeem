//点击otherButton跳转到https://ggrmm.top/%E6%B8%B8%E6%88%8F/%E9%AD%94%E7%81%B5%E5%8F%AC%E5%94%A4/

        // 点击其他功能按钮时，跳转到指定的URL
        document.getElementById('otherButton').addEventListener('click', function() {       
            window.location.href = 'https://ggrmm.top/%E6%B8%B8%E6%88%8F/%E9%AD%94%E7%81%B5%E5%8F%AC%E5%94%A4/';
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
                addCodeModal.style.display = 'none';
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
        // 获取历史领取弹窗
        const historyModal = document.getElementById('historyModal');
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
            if (event.target == modal) {
                historyModal.style.display = "none";
            }
        }
        // 获取历史领取数据并显示在弹窗中
        function fetchHistory() {
            fetch('/history')
                .then(response => response.text())  // 获取CSV文件内容
                .then(csvText => {
                    const csvData = parseCSV(csvText);  // 解析CSV
                    const totalRows = csvData.length - 1; // 减去标题行
                    displayCSV(csvData, totalRows);  // 显示CSV数据
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
function displayCSV(csvData, totalRows) {
    // 获取用于显示 CSV 数据的元素
    const csvTableContainer = document.getElementById('csvData');
    // 清除之前的内容
    csvTableContainer.innerHTML = '';
    const csvTable = document.createElement('table');
    const fragment = document.createDocumentFragment(); // 创建 DOM Fragment

    const rowsToDisplay = 20; // 每次显示的行数
    let startRow = 1; // 从第二行开始（忽略表头）
    let endRow = Math.min(startRow + rowsToDisplay, totalRows + 1);

    // 遍历CSV数据，从第二行开始（忽略表头）
    for (let i = startRow; i < endRow; i++) {
        const row = csvData[i];
        const tr = document.createElement('tr');

        for (let j = 0; j < row.length; j++) {
            const cell = row[j];
            const td = document.createElement('td');
            td.textContent = cell;
            tr.appendChild(td);
        }

        fragment.appendChild(tr); // 将 tr 添加到 fragment
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

    // 显示弹窗
    historyModal.style.display = "block";
}



        // 最新兑换码
        // 获取最新兑换码按钮
        const rewardButton = document.getElementById('rewardButton');
        // 获取最新兑换码弹窗
        const rewardModal = document.getElementById('rewardModal');
        // 为按钮添加点击事件监听器
        rewardButton.addEventListener('click', fetchReward);
        // 绑定点击事件到最新兑换码按钮
        document.getElementById('rewardButton').addEventListener('click', fetchReward);
        // 当用户点击最新兑换码按钮时，显示弹窗
        rewardButton.onclick = function() {
            rewardModal.style.display = "block";
        }

        // 当用户点击任何地方时，关闭弹窗
        window.onclick = function(event) {
            if (event.target == rewardModal) {
                rewardModal.style.display = "none";
            }
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
    // 获取用于显示 CSV 数据的元素
    const csvTableContainer = document.getElementById('rewardData');
    // 清除之前的内容
    csvTableContainer.innerHTML = '';
    const csvTable = document.createElement('table');
    const fragment = document.createDocumentFragment(); // 创建 DOM Fragment

    // 遍历CSV数据
    for (let i = 0; i < csvData.length; i++) {
        const row = csvData[i];
        const tr = document.createElement(i === 0 ? 'th' : 'tr');

        for (let j = 0; j < row.length; j++) {
            const cell = row[j];
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


        // 获取增加兑换码按钮
        const addCodeButton = document.getElementById('addCodeButton');
        // 获取增加兑换码弹窗
        const addCodeModal = document.getElementById('addCodeModal');
        // 为按钮添加点击事件监听器
        addCodeButton.addEventListener('click', openAddCodeModal);
        // 绑定点击事件到增加兑换码按钮
        document.getElementById('addCodeButton').addEventListener('click', openAddCodeModal);
        // 当用户点击增加兑换码按钮时，显示弹窗
        addCodeButton.onclick = function() {
            addCodeModal.style.display = "block";
        }
        // 当用户点击任何地方时，关闭弹窗
        window.onclick = function(event) {
            if (event.target == addCodeModal) {
                addCodeModal.style.display = "none";
            }
        }
        // 打开增加兑换码弹窗
        function openAddCodeModal() {
            addCodeModal.style.display = "block";
        }
        // 监听增加兑换码表单提交事件
        const addCodeForm = document.getElementById('addCodeForm');
        addCodeForm.addEventListener('submit', handleAddCodeSubmit);
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
                addCodeModal.style.display = "none"; // 关闭弹窗
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
        script.setAttribute("src","https://myhkw.cn/api/player/174158352560");
        script.setAttribute("key","174158352560");
        script.setAttribute("m","1");
        document.documentElement.appendChild(script);
