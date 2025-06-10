<p align="center"><img src="/img/yscon_logo.png" width="200"></p>
<h1 align="center">[ SYSC0N ]</h1>
<p align="center">sync all your dotfiles with a git repo</p>

<p>We all have this one folder with all our nice and beloved dotfiles. Sometimes you also have more than one PC where you want to use these dotfiles and keep them in sync or just want your dots when you configure a new device. SYSCON is the lightweight python script that do the job.</p>

### Prerequisite
Keep the `config.ini` in the same directory like the SYSC0N tool and enter your credentials:<br>
`machine = ` Name of the machine 
`dotfile_repo =`  enter the URL of the remote repository  
`dotfile_path = ` enter the path to your local dotfile folder 


### Usage
`syscon.py -init` start a new SYSC0N repo 
`syscon.py -add`  add new dotfiles to SYSC0N repo 
`syscon.py -push` syncing up (push) to the remote repo 
`syscon.py -pull` syncing down (pull) from existing SYSC0N repo

### Installation
#### NixOS
- soon - 

#### Linux
You can use the `install.sh` script in the repo to make the tool executable.
The script copy SYSC0N to a systemfolder, make it executable and create a symlink to SYSC0N.

`sh install.sh`

