# Конфигурация виртуальной машины devops-vm

## 1. Параметры машины
- Гипервизор: VirtualBox 7.x; тип/версия: Linux / Ubuntu (64-bit)
- ОЗУ 2048 МБ, 2 ядра, диск 25 ГБ (динамический)
- ОС: Ubuntu Server 24.04 LTS (не minimized), разметка <Use an entire disk>
- Установка: язык English, имя узла devops-vm, пользователь student,
  OpenSSH server установлен, Featured snaps не выбирались
- После установки: `sudo apt update && sudo apt upgrade -y`

## 2. Сетевые интерфейсы
| Адаптер | Тип | Адрес | Назначение |
|---|---|---|---|
| 1 | NAT | 10.0.2.15 | доступ в интернет, пробросы портов |
| 2 | Host-only | <192.168.56.xxx> | доступ с хоста (SSH, веб) |

- Имя на хосте: в hosts хоста добавлена строка `<192.168.56.xxx> devops.local`
- Имя на сервере: `sudo hostnamectl set-hostname devops-vm`;
  в /etc/hosts строка `127.0.1.1 devops-vm.devops.local devops-vm`
  (`sudo sed -i 's/^127.0.1.1.*/127.0.1.1 devops-vm.devops.local devops-vm/' /etc/hosts`);
  `hostname -f`  devops-vm.devops.local

## 3. Правило проброса портов
Адаптер 1 (NAT), правило `ssh`: TCP, хост 127.0.0.1:2222  гость порт 2222
(изначально гость 22, изменён на 2222 после смены порта SSH).

## 4. Учётные записи
| Имя | Группы | Аутентификация |
|---|---|---|
| student | sudo (создан установщиком) | пароль; по SSH не допускается (AllowUsers devops) |
| devops | devops, sudo | только ключ ed25519 |

Создание devops:
```
sudo adduser devops
sudo usermod -aG sudo devops
```
Ключ создан на хосте: `ssh-keygen -t ed25519 -C "devops-vm-key" -f ~/.ssh/devops_vm`,
открытый ключ в `/home/devops/.ssh/authorized_keys` (права каталога 700, файла 600),
установлен командой `ssh-copy-id -i ~/.ssh/devops_vm.pub -p 2222 devops@127.0.0.1`.
Клиентский `~/.ssh/config` на хосте: Host devops  HostName 127.0.0.1, Port 2222,
User devops, IdentityFile ~/.ssh/devops_vm, IdentitiesOnly yes.

## 5. Служба SSH
Основной файл `/etc/ssh/sshd_config` не изменялся (копия: sshd_config.backup).
Настройки в `/etc/ssh/sshd_config.d/99-hardening.conf`:
```
Port 2222
PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes
PermitEmptyPasswords no
MaxAuthTries 3
LoginGraceTime 30
AllowUsers devops
X11Forwarding no
ClientAliveInterval 300
ClientAliveCountMax 2
```
Дополнительно:
- В `/etc/ssh/sshd_config.d/50-cloud-init.conf` закомментирована строка `PasswordAuthentication yes` (<если была>)
- Отключена активация по сокету:
  `sudo systemctl disable --now ssh.socket && sudo systemctl enable --now ssh.service && sudo systemctl restart ssh`
- Проверка: `sudo sshd -t`, `sudo sshd -T`, `sudo ss -tlnp | grep sshd` (0.0.0.0:2222)

## 6. Правила межсетевого экрана
Политики: `default deny incoming`, `default allow outgoing`.
```
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw limit 2222/tcp comment 'SSH rate-limited'
sudo ufw allow 80/tcp comment 'HTTP'
sudo ufw allow 443/tcp comment 'HTTPS'
sudo ufw logging medium
sudo ufw enable
```
Правила SSH, HTTP, HTTPS создаются до `ufw enable`.
Лог блокировок: /var/log/ufw.log.

## 7. Снимки состояния
| Имя | Состояние | Дата |
|---|---|---|
| 01-clean-install | чистая установка, обновления, адреса получены | <дата> |
| 02-keys-configured | пользователь devops, ключи, ~/.ssh/config | <дата> |
| 03-ssh-hardened | SSH-hardening и UFW | <дата> |# Конфигурация виртуальной машины devops-vm

## 1. Параметры машины
- Гипервизор: VirtualBox 7.x; тип/версия: Linux / Ubuntu (64-bit)
- ОЗУ 2048 МБ, 2 ядра, диск 25 ГБ (динамический)
- ОС: Ubuntu Server 24.04 LTS (не minimized), разметка <Use an entire disk>
- Установка: язык English, имя узла devops-vm, пользователь student,
  OpenSSH server установлен, Featured snaps не выбирались
- После установки: `sudo apt update && sudo apt upgrade -y`

## 2. Сетевые интерфейсы
| Адаптер | Тип | Адрес | Назначение |
|---|---|---|---|
| 1 | NAT | 10.0.2.15 | доступ в интернет, пробросы портов |
| 2 | Host-only | <192.168.56.xxx> | доступ с хоста (SSH, веб) |

- Имя на хосте: в hosts хоста добавлена строка `<192.168.56.xxx> devops.local`
- Имя на сервере: `sudo hostnamectl set-hostname devops-vm`;
  в /etc/hosts строка `127.0.1.1 devops-vm.devops.local devops-vm`
  (`sudo sed -i 's/^127.0.1.1.*/127.0.1.1 devops-vm.devops.local devops-vm/' /etc/hosts`);
  `hostname -f`  devops-vm.devops.local

## 3. Правило проброса портов
Адаптер 1 (NAT), правило `ssh`: TCP, хост 127.0.0.1:2222  гость порт 2222
(изначально гость 22, изменён на 2222 после смены порта SSH).

## 4. Учётные записи
| Имя | Группы | Аутентификация |
|---|---|---|
| student | sudo (создан установщиком) | пароль; по SSH не допускается (AllowUsers devops) |
| devops | devops, sudo | только ключ ed25519 |

Создание devops:
```
sudo adduser devops
sudo usermod -aG sudo devops
```
Ключ создан на хосте: `ssh-keygen -t ed25519 -C "devops-vm-key" -f ~/.ssh/devops_vm`,
открытый ключ в `/home/devops/.ssh/authorized_keys` (права каталога 700, файла 600),
установлен командой `ssh-copy-id -i ~/.ssh/devops_vm.pub -p 2222 devops@127.0.0.1`.
Клиентский `~/.ssh/config` на хосте: Host devops  HostName 127.0.0.1, Port 2222,
User devops, IdentityFile ~/.ssh/devops_vm, IdentitiesOnly yes.

## 5. Служба SSH
Основной файл `/etc/ssh/sshd_config` не изменялся (копия: sshd_config.backup).
Настройки в `/etc/ssh/sshd_config.d/99-hardening.conf`:
```
Port 2222
PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes
PermitEmptyPasswords no
MaxAuthTries 3
LoginGraceTime 30
AllowUsers devops
X11Forwarding no
ClientAliveInterval 300
ClientAliveCountMax 2
```
Дополнительно:
- В `/etc/ssh/sshd_config.d/50-cloud-init.conf` закомментирована строка `PasswordAuthentication yes` (<если была>)
- Отключена активация по сокету:
  `sudo systemctl disable --now ssh.socket && sudo systemctl enable --now ssh.service && sudo systemctl restart ssh`
- Проверка: `sudo sshd -t`, `sudo sshd -T`, `sudo ss -tlnp | grep sshd` (0.0.0.0:2222)

## 6. Правила межсетевого экрана
Политики: `default deny incoming`, `default allow outgoing`.
```
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw limit 2222/tcp comment 'SSH rate-limited'
sudo ufw allow 80/tcp comment 'HTTP'
sudo ufw allow 443/tcp comment 'HTTPS'
sudo ufw logging medium
sudo ufw enable
```
Правила SSH, HTTP, HTTPS создаются до `ufw enable`.
Лог блокировок: /var/log/ufw.log.

## 7. Снимки состояния
| Имя | Состояние | Дата |
|---|---|---|
| 01-clean-install | чистая установка, обновления, адреса получены | <дата> |
| 02-keys-configured | пользователь devops, ключи, ~/.ssh/config | <дата> |
| 03-ssh-hardened | SSH-hardening и UFW | <дата> |
