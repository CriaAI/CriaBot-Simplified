import sys, os
sys.path.insert(0, os.path.abspath(os.curdir))

import subprocess
import streamlit as st


class Subprocess:
    def __init__(self, script):
        self.script = script
        self.process = None

    def run_subprocess(self):
        self.process = subprocess.Popen(self.script, shell=True, stderr=subprocess.PIPE)
        self.process.wait()
        stderr = self.process.stderr.read().decode('latin-1')

        if self.process.returncode != 0:
            st.error(f"Ocorreu um erro: {stderr}")
        else:
            st.success("Script executado com sucesso!")