# TWAuthenticator

TWAuthenticator — это десктопное приложение для генерации одноразовых кодов двухфакторной аутентификации (TOTP). Программа позволяет создавать и хранить коды 2FA непосредственно на компьютере, избавляя от необходимости использовать мобильное устройство при входе в аккаунты.

### Основные возможности

* Генерация TOTP: Создание стандартных 6-значных кодов, полностью совместимых с Google Authenticator, Яндекс.Ключом и другими популярными сервисами.
* Буфер обмена: Копирование кода в буфер обмена одним кликом для быстрой авторизации.
* Безопасность: Локальное хранение данных с использованием шифрования и возможность установки PIN-кода для защиты доступа к приложению.
* Интерфейс: Поддержка нескольких тем оформления и переключение между русским и английским языками.
* Индикация времени: Визуальный таймер, отображающий время жизни текущего кода.

### Как установить

1. Перейдите в раздел **Releases** в этом репозитории.
2. Скачайте актуальный файл установщика (TWAuthenticatorSetup.exe).
3. Запустите файл и следуйте инструкциям мастера установки.
4. Программа автоматически создаст ярлык на рабочем столе.

### Как пользоваться

1. Откройте приложение через ярлык на рабочем столе.
2. Нажмите кнопку добавления аккаунта (+), введите название сервиса и вставьте секретный ключ, полученный при настройке 2FA.
3. Нажмите на нужный код для его копирования в буфер обмена.
4. Используйте меню аккаунта (три точки) для изменения или удаления данных.
5. Перейдите в настройки (иконка шестеренки) для изменения темы оформления, языка или установки PIN-кода.

### Стек технологий

* Язык программирования: Python
* Графический интерфейс: CustomTkinter
* Логика генерации кодов: PyOTP

**Важно:** Сохраняйте секретные ключи в надежном месте. При потере доступа к компьютеру и отсутствии копий ключей восстановить доступ к учетным записям будет невозможно.

---

### English Summary

**TWAuthenticator** is a secure desktop client for generating TOTP 2FA codes. It allows users to store and manage authentication keys locally on their PC, providing a fast and convenient way to log into accounts without a mobile device.

**Features:** TOTP generation (compatible with standard services), one-click copy to clipboard, local data encryption, optional PIN protection, and customizable themes.

**Installation & Usage:** Download the installer from the **Releases** tab and follow the setup wizard. Add accounts by entering the service name and secret key, then click on any code to copy it to the clipboard. Use the settings menu to configure themes, language, or PIN protection.
