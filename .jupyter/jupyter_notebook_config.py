from traitlets.config import get_config

c = get_config()  # noqa

# Set the notebook directory
c.NotebookApp.notebook_dir = "notebooks"

# Security settings
c.NotebookApp.token = ""  # Disable token authentication for local development
c.NotebookApp.password = ""  # Disable password for local development

# Display settings
c.NotebookApp.show_hidden_files = False
c.NotebookApp.terminals_enabled = True

# Set default URL to the notebooks directory
c.NotebookApp.default_url = "/tree/notebooks"

# Auto-save settings
c.AutoSaveHandler.interval = 120  # Auto-save every 2 minutes

# Set the kernel spec
c.NotebookApp.kernel_spec_manager_class = "jupyter_client.kernelspec.KernelSpecManager"

# Enable nbextensions (if installed)
c.NotebookApp.nbserver_extensions = {}
c.NotebookApp.enable_mathjax = True

# Set the IP and port
c.NotebookApp.ip = "localhost"
c.NotebookApp.port = 8888

# Browser settings
c.NotebookApp.open_browser = True

# File types to show in the notebook interface
c.ContentsManager.hide_globs = [
    "__pycache__",
    "*.pyc",
    "*.pyo",
    ".DS_Store",
    "*.so",
    "*.dylib",
    "*~",
]
