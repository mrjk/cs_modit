# Please source me:
# . env.sh

# Default config
# ======================
VENV_DIR=.venv
SECRET_ENV_FILE=secrets.env.sh

# Functions
# ======================

import_secrets()
{
  local file=$1

  if [[ -f "$file" ]]; then
    . "$file"
  else
    echo "WARN: You need to create the '$file' file"
  fi
}

# Install venv
install_venv()
{
  local dest=$1

  if [[ ! -d "$dest" ]]; then
    virtualenv -p python3 "$dest"
    . "$dest/bin/activate"
    pip install --upgrade pip
    pip install -r requirements.txt
    echo "INFO: Python3 virtual env installed"
  fi
}

# Load virtualenv and install it if necessary
load_venv()
{
  local dest=$1
  install_venv "$dest"

  # Enable virtualenv if not already enabled
  if [[ -z "$VIRTUAL_ENV" ]]; then
    . $dest/bin/activate
  fi

  echo "INFO: Python3 virtual env enabled"
}


# Main loading
# ======================
load_venv $VENV_DIR
import_secrets "$SECRET_ENV_FILE"

echo "INFO: Environment loaded"

