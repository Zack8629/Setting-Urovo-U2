# Flash and Settings U2

## Описание
**Flash and Settings U2** — это инструмент для автоматизации процесса прошивки и настройки устройств **Urovo U2**. Программа упрощает выполнение конфигураций, включая установку приложений, настройку параметров системы и импорт пользовательских данных. Все действия выполняются с использованием **ADB** (Android Debug Bridge).

Программа предназначена для инженеров и специалистов по настройке оборудования, которым требуется быстро и последовательно подготовить устройства к использованию.

---

## Основные функции
- **Прошивка и установка приложений**:
  - Установка приложений, необходимых для работы устройства.
  - Импорт пользовательских данных, таких как обои и конфигурационные файлы.

- **Настройка параметров системы**:
  - Настройка яркости экрана, времени его отключения и других системных параметров.
  - Отключение ненужных системных сервисов и упрощение интерфейса.

- **Импорт настроек**:
  - Импорт пользовательских конфигураций через предустановленные файлы.

- **Установка обоев и конфигурация клавиш**:
  - Установка обоев из файла.
  - Настройка горячих клавиш устройства.

- **Выключение и перезагрузка устройств**:
  - Автоматическое завершение работы устройств.

---

## Как использовать
1. Убедитесь, что на вашем ПК установлены все необходимые драйверы для устройства **Urovo U2**.
2. Подключите устройство к компьютеру.
3. Запустите приложение и следуйте инструкциям.
4. Настройка выполняется в несколько шагов:
   - Шаг 1: Установка приложений и системных файлов.
   - Шаг 2: Настройка параметров интерфейса.
   - Шаг 3: Установка обоев.
   - Шаг 4: Конфигурация клавиш.
   - Шаг 5: Импорт настроек.
   - Шаг 6: Завершение работы устройств.

---

## Системные требования
- **Операционная система**: Windows 10/11.

---

## Сборка приложения
Для создания исполняемого файла используйте следующую команду:

```bash
pyinstaller --onefile --icon=icons/main.ico --name="Flash and Settings U2 vX.X.X.X" --add-data "texts;texts" --add-data "icons;icons" run.py