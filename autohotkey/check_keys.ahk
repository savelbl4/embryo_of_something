#Requires AutoHotkey v2.0
#SingleInstance Force

; --- GUI ---
g := Gui("+AlwaysOnTop", "Просмотр нажатий (только при фокусе окна)")
g.SetFont("s10")
g.AddText(, "Нажимайте клавиши, пока это окно активно.")
lv := g.AddListView("w520 h320", ["Символ", "Код"])

grp := g.AddGroupBox("w520 h60", "Действия")
btnSave := g.AddButton("x+10 yp+18 w150", "Сохранить в файл")
btnClear := g.AddButton("x+10 w120", "Очистить")
cbPause := g.AddCheckBox("x+10 w160", "Пауза (не писать)")
cbPause.Value := 0

btnSave.OnEvent("Click", (*) => SaveToFile(lv))
btnClear.OnEvent("Click", (*) => lv.Delete())

; --- Перехват клавиш (только когда окно активно) ---
handler := (wParam, lParam, msg, hwnd) => MsgHandler(lv, g, cbPause, wParam, lParam)
OnMessage(0x100, handler)   ; WM_KEYDOWN
OnMessage(0x104, handler)   ; WM_SYSKEYDOWN (Alt)

g.Show("AutoSize")

; --------- Функции ----------
MsgHandler(lv, g, cbPause, wParam, lParam) {
    if !WinActive("ahk_id " g.Hwnd) || cbPause.Value
        return

    sc := (lParam >> 16) & 0xFF             ; scan code (8 бит)
    scStr := Format("SC{:03X}", sc)

    name := ""
    try name := GetKeyName("sc" . Format("{:03X}", sc))
    if (name = "")
        name := "{?}"

    lv.Add(, name, scStr)
    lv.ModifyCol()
}

SaveToFile(lv) {
    path := FileSelect("S16",, "Сохранить журнал", "Текст (*.txt;*.csv)")
    if !path
        return
    f := FileOpen(path, "w", "UTF-8-RAW")
    Loop lv.GetCount() {
        sym := lv.GetText(A_Index, 1)
        sc  := lv.GetText(A_Index, 2)
        f.WriteLine(Format("{} - {}", sym, sc))  ; нужный формат
    }
    f.Close()
    MsgBox "Сохранено: " path
}

; Горячая клавиша, чтобы быстро вернуть окно
^!k:: g.Show()
