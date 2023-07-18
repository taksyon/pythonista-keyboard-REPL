import keyboard
import ui
import code
import sys
import io


class REPLView(ui.View):

    def __init__(self, *args, **kwargs):
        ui.View.__init__(self, *args, **kwargs)
        self.inpt_bffr = ''
        self.prmpt = '>>> '
        self.mlti_prmpt = '• • • '

    def did_load(self):
        self['eval_btn'].action = self.eval_actn
        self['tab_fwd_btn'].action = self.tab_fwd_actn
        self['tab_back_btn'].action = self.tab_back_actn
        self.repl_start()

    def repl_start(self):
        keyboard.insert_text(self.prmpt)

    def eval_actn(self, sender):
        line = self.get_eval_line()
        self.exec_line(line)

    def get_eval_line(self):
        before, after = keyboard.get_input_context()
        line = (before.replace(self.prmpt, '').replace(self.mlti_prmpt,
                                                       '').split('\n'))
        return line[-1]

    def exec_line(self, line):
        keyboard.insert_text('\n')
        self.inpt_bffr += line + '\n'
        prev_stdout = sys.stdout
        redir_out = io.StringIO()
        sys.stdout = redir_out
        txt = self.obsrv_txt().split('\n')
        try:
            if (self.inpt_bffr.endswith('\n\n')):
                if (txt[-2] == self.prmpt):
                    self.inpt_bffr = ''
                    keyboard.insert_text(self.prmpt)
                else:
                    c = code.compile_command(self.inpt_bffr, '<string>',
                                             'exec')
                    if c is not None:
                        exec(c, globals())
                        self.inpt_bffr = ''
                        keyboard.insert_text(self.prmpt)
                    else:
                        self.inpt_bffr = ''
                        keyboard.insert_text('Error')
            elif not self.inpt_bffr.endswith('\n\n'):
                if (txt[-2] == self.prmpt):
                    self.inpt_bffr = ''
                    keyboard.insert_text(
                        self.prmpt)  # in case user runs empty string
                elif txt[-2].startswith(self.prmpt):
                    c = code.compile_command(self.inpt_bffr, '<string>',
                                             'exec')
                    if c is not None:
                        exec(c, globals())
                        self.inpt_bffr = ''
                        keyboard.insert_text(self.prmpt)
                    else:
                        keyboard.insert_text(self.mlti_prmpt)
                elif txt[-2].startswith(self.mlti_prmpt):
                    keyboard.insert_text(self.mlti_prmpt)

        except Exception:
            import traceback
            traceback.print_exc(file=redir_out)
        finally:
            sys.stdout = prev_stdout
        output = redir_out.getvalue()
        if len(output) > 1000:
            output = '[...]\n' + output[-990:]
        if output:
            keyboard.backspace(times=4)
            keyboard.insert_text(output + self.prmpt)

    def obsrv_txt(self):
        before, after = keyboard.get_input_context()
        return before

    def tab_fwd_actn(self, sender):
        keyboard.insert_text('    ')

    def tab_back_actn(self, sender):
        keyboard.backspace(times=4)


def main():
    if keyboard.is_keyboard():
        v = ui.load_view('REPLView.pyui')
        keyboard.set_view(v, 'minimized')
    else:
        print(
            'This script is meant to be run in the custom Pythonista Keyboard.'
        )


if __name__ == '__main__':
    main()
