#Requires AutoHotkey v2.0
#SingleInstance Force

;==========================================
; CapsLock: короткое нажатие - переключение раскладки
;           длинное нажатие - обычный CapsLock
;==========================================

CapsLock::
{
    KeyWait "CapsLock"  ; Ждем отпускания клавиши
    if (A_TimeSinceThisHotkey < 200)  ; Короткое нажатие (< 200ms)
    {
        SwitchKeyboardLayout()
    }
    else  ; Длинное нажатие
    {
        SetCapsLockState !GetKeyState("CapsLock", "T")  ; Переключаем состояние CapsLock
    }
}

; Функция переключения раскладки
SwitchKeyboardLayout()
{
    try
    {
        ; Активное окно
        activeHwnd := WinGetID("A")
        
        ; Получаем раскладку активного окна
        threadId := DllCall("GetWindowThreadProcessId", "Ptr", activeHwnd, "Ptr", 0)
        currentLayout := DllCall("GetKeyboardLayout", "UInt", threadId)
        
        ; Переключаем раскладку
        PostMessage(0x50, 0, 0, , activeHwnd)  ; WM_INPUTLANGCHANGEREQUEST
    }
    catch Error as e
    {
        ; Альтернативный способ если основной не работает
        Send("{Alt Down}{Shift}{Alt Up}")
    }
}

;==========================================
; macOS-подобные горячие клавиши (Cmd = Win)
;==========================================

;#z::Send("^z")  ; Undo
;#x::Send("^x")  ; Cut
;#c::Send("^c")  ; Copy
;#v::Send("^v")  ; Paste
;#a::Send("^a")  ; Select All
;#s::Send("^s")  ; Save
;#f::Send("^f")  ; Find
;#n::Send("^n")  ; New
;#o::Send("^o")  ; Open
;#w::Send("{F4}") ; Close window
;#t::Send("^t")  ; New Tab
;#r::Send("^r")  ; Reload;

;; Дополнительные полезные комбинации
;#+t::Send("^+t")  ; Restore closed tab
;#l::Send("^l")    ; Address bar
;#+r::Send("^+r")  ; Hard reload

;==========================================
; Исправление символов для Apple Keyboard
;==========================================

; клавиша винды меняется на контрол
sc05b::Send("{sc01d}")

; Клавиша SC056 ("§/±" перед "1") 
sc056::CheckRus(">", "§")
+sc056::CheckRus("<", "±")
; Клавиша SC056 ("Ё" после "Э") 
sc02b::CheckRus("ё", "\")
+sc02b::CheckRus("Ё", "|")
; Клавиша SC029 ("]/["перед "я/z")
sc029::CheckRus("]", "``")
+sc029::CheckRus("[", "[")
; sc035 ("'/'/'?'" после "Ю")
sc035::Send("/")
+sc035::Send("?")

+5::CheckRus(":", "%")
+6::CheckRus(",", "^") 
+7::CheckRus(".", "&")
+8::CheckRus(";", "*")

CheckRus(rus, eng)
{
    try
    {
        activeHwnd := WinGetID("A")
        threadId := DllCall("GetWindowThreadProcessId", "Ptr", activeHwnd, "Ptr", 0)
        currentLayout := DllCall("GetKeyboardLayout", "UInt", threadId)
        
        ; 0x4190419 - Russian, 0x4090409 - English
        if (currentLayout = 0x4190419)
            Send(rus)
        else
            Send(eng)
    }
    catch
    {
        Send(eng)  ; По умолчанию английский символ
    }
}

;==========================================
; Настройки
;==========================================

#HotIf
Persistent()  ; Скрипт не завершается автоматически

; Информация о скрипте (раскомментируйте если нужно)
; !i:: {
;     MsgBox("CapsLock Script Active!`n`nShort press: Switch layout`nLong press: Toggle CapsLock", "Info", "T2")
; }
