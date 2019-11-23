import urwid

class NuttyGrinderApp:
    
    palette = [
        ('body','','','', 'g0','g100'),
        ('window','','','', 'g0', 'g65'),
        ('background','','','', 'g0', 'g25'),
        ('editbox','','','', 'g0', 'g100')
    ]

    def __init__(self):
        pass
    
    def root_widget(self):
        editing = [
            urwid.AttrWrap(urwid.Edit(('window', "Username: "), ""), 'editbox'),
            urwid.Divider(' '),
            urwid.AttrWrap(urwid.Edit(('window', 'Password: '), ""), 'editbox')
        ]
        text = urwid.Filler(urwid.Pile(editing))
        window = urwid.AttrWrap(urwid.LineBox(text, title='NuttyGrinder v1.2.5', title_align='left'), 'window')
        top = urwid.Overlay(window, urwid.AttrWrap(urwid.SolidFill(),'background'), 'center', ('relative', 90), 'middle', ('relative', 70))
        return top

    def main(self):
        root = self.root_widget()
        self.loop = urwid.MainLoop(root, NuttyGrinderApp.palette, unhandled_input=self.unhandled)
        self.loop.screen.set_terminal_properties(colors=256)
        self.loop.run()

    def unhandled(self, k):
        if k == "f8":
            raise urwid.ExitMainLoop()



def main():
    app = NuttyGrinderApp()
    app.main()

if __name__ == "__main__":
    main()
