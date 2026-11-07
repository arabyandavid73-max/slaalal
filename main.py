import os
import glob
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.core.window import Window

# Темный фон
Window.clearcolor = (0.05, 0.05, 0.05, 1)

# Путь к базам на телефоне
BASE_DIR = "/storage/emulated/0/Download/Telegram"

def search_local(fields):
    active_queries = [v.strip().lower() for v in fields.values() if v.strip()]
    if not active_queries: return "Заполните поля"
    
    files = []
    for ext in ("*.txt", "*.csv", "*.tsv"):
        files.extend(glob.glob(os.path.join(BASE_DIR, ext)))
    
    if not files:
        return f"Файлы не найдены в:\n{BASE_DIR}\n\nУбедитесь, что базы лежат в Download/Telegram"
    
    results = []
    for filepath in files:
        try:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    line_lower = line.lower()
                    if all(q in line_lower for q in active_queries):
                        results.append(f"[{os.path.basename(filepath)}] {line.strip()}")
                        if len(results) >= 30: break
        except: continue
        if len(results) >= 30: break
    
    return "\n\n".join(results) if results else "Ничего не найдено"

class MVDApp(App):
    def build(self):
        root = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Заголовок
        title = Label(text="[b]MVD OSINT[/b]", markup=True, font_size='20sp', color=(0, 1, 0.25, 1), size_hint_y=None, height=50)
        root.add_widget(title)
        
        # Поля ввода
        self.inputs = {}
        fields = [("ФИО", "fio"), ("Телефон", "phone"), ("ИНН", "inn")]
        
        for name, key in fields:
            row = BoxLayout(size_hint_y=None, height=40)
            row.add_widget(Label(text=name, color=(1,1,1,1), size_hint_x=0.3))
            ti = TextInput(multiline=False, background_color=(0.1, 0.1, 0.1, 1), foreground_color=(0, 1, 0, 1))
            self.inputs[key] = ti
            row.add_widget(ti)
            root.add_widget(row)
            
        # Кнопка поиска
        btn = Button(text="ЗАПУСТИТЬ ПОИСК", background_color=(0, 0.5, 0.2, 1), size_hint_y=None, height=50)
        btn.bind(on_press=self.do_search)
        root.add_widget(btn)
        
        # Результаты
        self.result_label = Label(text="Готов к работе", color=(0, 1, 0, 1), halign="left", valign="top")
        self.result_label.bind(texture_size=lambda instance, value: setattr(instance, 'height', value[1]))
        
        scroll = ScrollView()
        scroll.add_widget(self.result_label)
        root.add_widget(scroll)
        
        return root

    def do_search(self, instance):
        self.result_label.text = "Поиск..."
        fields = {k: v.text for k, v in self.inputs.items()}
        self.result_label.text = search_local(fields)

if __name__ == '__main__':
    MVDApp().run()
