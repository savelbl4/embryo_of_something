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

; клавиша винды меняется на контрол (не работает)
;sc05b::Send("{sc01d}")

; Клавиша SC056 ("§/±" перед "1") 
sc056::Send(IsRussian() ? ">" : "§")
+sc056::Send(IsRussian() ? "<" : "±")
; Клавиша SC056 ("Ё" после "Э") 
sc02b::Send(IsRussian() ? "ё" : "\")
+sc02b::Send(IsRussian() ? "Ё" : "|")
; Клавиша SC029 ("]/["перед "я/z")
sc029::Send(IsRussian() ? "]" : "``")
+sc029::Send(IsRussian() ? "[" : "[")
; sc035 ("'/'/'?'" после "Ю")
sc035::Send("/")
+sc035::Send("?")

+sc006::Send(IsRussian() ? ":" : "%")   ; 5
+sc007::Send(IsRussian() ? "," : "{^}") ; 6
+sc008::Send(IsRussian() ? "." : "&")   ; 7
+sc009::Send(IsRussian() ? ";" : "*")   ; 8

IsRussian() {
    try {
        hwnd := WinGetID("A")
        threadId := DllCall("GetWindowThreadProcessId", "Ptr", hwnd, "Ptr", 0)
        lid := DllCall("GetKeyboardLayout", "UInt", threadId)
        return (lid & 0xFFFF) = 0x0419
    }
    catch {
        return false
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
