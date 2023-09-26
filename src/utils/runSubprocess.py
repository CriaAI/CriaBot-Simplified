import sys, os
sys.path.insert(0, os.path.abspath(os.curdir))

import subprocess
import streamlit as st

def run_subprocess(script):
    process = subprocess.Popen(script, shell=True, stderr=subprocess.PIPE)
    process.wait()
    stderr = process.stderr.read().decode('latin-1')

    if process.returncode != 0:
        st.error(f"Ocorreu um erro: {stderr}")
    else:
        st.success("Script executado com sucesso!")        