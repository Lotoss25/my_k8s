#!/bin/bash
export RUNNER_ALLOW_RUNASROOT=1
# 1. Ловимо токен
RUNNER_TOKEN=$1
# 2. Запитуємо у API номер останньої версії (вирізаємо саме цифри, наприклад 2.311.0)
LATEST_VERSION=$(curl -s https://api.github.com/repos/actions/runner/releases/latest | grep '"tag_name":' | sed -E 's/.*"v([^"]+)".*/\1/')

if [ -z "$RUNNER_TOKEN" ]; then
    echo "❌ Помилка: Не вказано токен!"
    echo "Використання: ./init.sh ВАШ_ТОКЕН"
    exit 1
fi

# 3. Ставимо софт
echo "📦 Встановлюємо Git та Ansible..."
sudo apt update
sudo apt install -y git
sudo apt-add-repository --yes --update ppa:ansible/ansible
sudo apt install -y ansible

# 4. Готуємо ранера
echo "🏃 Налаштовуємо GitHub Runner..."
mkdir -p actions-runner && cd actions-runner

# Скачуємо (це посилання краще брати свіже з сайту GitHub, але для прикладу хай буде)
curl -o actions-runner-linux-x64-${LATEST_VERSION}.tar.gz -L https://github.com/actions/runner/releases/download/v${LATEST_VERSION}/actions-runner-linux-x64-${LATEST_VERSION}.tar.gz

# Розпаковуємо
tar xzf ./actions-runner-linux-x64-${LATEST_VERSION}.tar.gz

# Налаштовуємо (з вашим токеном!)
./config.sh --url https://github.com/Lotoss25/my_k8s --token $RUNNER_TOKEN --unattended

# 5. Запускаємо як службу (Магія svc.sh) ✨
sudo ./svc.sh install
sudo ./svc.sh start

echo "✅ Готово! Ваш сервер заряджений і чекає на команди з GitHub."
