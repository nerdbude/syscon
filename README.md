<p align="center"><img src="/img/syscon_logo.png" width="200"></p>
<h1 align="center">[ SYSC0N ]</h1>
<p align="center">sync all your dotfiles with a git repo</p>

<p>We all have this one folder with all our nice and beloved dotfiles. Sometimes you also have more than one PC where you want to use these dotfiles and keep them in sync or just want your dots when you configure a new device. SYSCON is the lightweight python script that do the job.</p>

### Status

alpha (don't use it on productive systems)

### Prerequisite
Keep the `config.ini` in the same directory like the SYSCON tool and enter your credentials:<br>

`machine_name = ` Name of the machine<br> 
`dotfile_repo =`  URL of the remote dotfile repository<br>  
`dotfile_path = ` path to your local dotfile folder (/home/user/.config/)<br> 
`syscon_path = ` path to the syscon folder you created (/home/user/syscon/)<br>

### Usage
`syscon.py -init` start a new SYSCON repo <br>
`syscon.py -add`  add new dotfiles to SYSCON repo<br> 
`syscon.py -push` syncing up (push) to the remote repo<br> 
`syscon.py -pull` syncing down (pull) from existing SYSCON repo<br>

### Installation
#### NixOS
- soon

#### Linux
You can use the `install.sh` script in the repo to make the tool executable.
The script copy SYSCON to a systemfolder, make it executable and create a symlink to SYSCON. When it's done your can use `syscon` in your terminal.

`sh install.sh`

